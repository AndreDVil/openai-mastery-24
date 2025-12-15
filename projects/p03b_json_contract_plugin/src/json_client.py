import json
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI

from .config import get_default_params
from .contracts.base import Contract, ValidationResult


def _parse_json(raw_text: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Parse raw JSON text into a Python dict.

    Returns:
        (data, error_message)
    """
    try:
        data = json.loads(raw_text)
        if not isinstance(data, dict):
            return None, "Top-level JSON value must be an object (dict)."
        return data, None
    except Exception as e:
        return None, str(e)


class JsonModeChatClient:
    """
    JSON Mode chat client (Chat Completions API) with contract-driven validation and controlled retry.
    """

    def __init__(
        self,
        client: OpenAI,
        contract: Contract,
        model: Optional[str] = None,
        max_retries: int = 2,
        debug: bool = False,
    ):
        """
        Initialize the JSON Mode chat client.

        Parameters:
            client: OpenAI SDK client instance.
            contract: Contract object defining system prompt and validation logic.
            model: Optional model override.
            max_retries: Number of corrective retries (default: 2).
            debug: Enable debug logging (default: False).
        """
        self.client = client
        self.contract = contract
        self.default_params = get_default_params()

        # Override model if explicitly provided
        if model:
            self.default_params["model"] = model

        self.max_retries = max_retries
        self.debug = debug

        # Message history for multi-turn conversations
        self.messages: List[Dict[str, str]] = []

        # Inject contract-governed system prompt
        self.messages.append(
            {
                "role": "system",
                "content": self.contract.system_prompt,
            }
        )

    def _debug(self, message: str) -> None:
        """
        Print debug messages only when debug mode is enabled.
        """
        if self.debug:
            print(f"[DEBUG] {message}")

    def _call_model(self) -> str:
        """
        Perform a single Chat Completions call and return raw assistant content (expected JSON string).
        """
        completion = self.client.chat.completions.create(
            model=self.default_params["model"],
            messages=self.messages,
            response_format=self.default_params["response_format"],  # {"type":"json_object"}
            temperature=self.default_params["temperature"],
            top_p=self.default_params.get("top_p", 1.0),
        )

        # Chat Completions: assistant text is in choices[0].message.content
        raw_text = completion.choices[0].message.content or ""
        return raw_text

    def send(self, user_input: str) -> Dict[str, Any]:
        """
        Send user input, enforce JSON-only output, validate the contract, and optionally retry.

        Returns:
            A dict matching the active contract, or a structured error object.
        """
        # Add user message to history
        self.messages.append({"role": "user", "content": user_input})

        last_raw: str = ""
        last_parse_error: Optional[str] = None
        last_validation_errors: List[str] = []

        for attempt in range(self.max_retries + 1):
            self._debug(f"Attempt {attempt + 1}/{self.max_retries + 1}")

            last_raw = self._call_model()

            # Attempt to parse JSON
            data, parse_error = _parse_json(last_raw)
            if parse_error:
                last_parse_error = parse_error

                if attempt < self.max_retries:
                    self._inject_corrective_system_message(
                        error_code="INVALID_JSON",
                        details=[f"JSON parse error: {parse_error}"],
                        raw_response=last_raw,
                    )
                    continue

                return {
                    "error": "INVALID_JSON",
                    "raw_response": last_raw,
                    "details": parse_error,
                }

            # Contract-driven semantic validation
            result: ValidationResult = self.contract.validate(data)
            if result.ok:
                self._debug("Validation passed. Returning final JSON response.")

                # Store assistant message in history (as the raw JSON string)
                self.messages.append({"role": "assistant", "content": last_raw})
                return data

            last_validation_errors = result.errors
            self._debug(f"Contract validation failed with errors: {result.errors}")

            if attempt < self.max_retries:
                self._inject_corrective_system_message(
                    error_code="SCHEMA_VALIDATION_FAILED",
                    details=result.errors,
                    raw_response=last_raw,
                )
                continue

            return {
                "error": "SCHEMA_VALIDATION_FAILED",
                "raw_response": last_raw,
                "details": result.errors,
            }

        # Defensive fallback (should never happen)
        return {
            "error": "UNKNOWN",
            "raw_response": last_raw,
            "details": last_validation_errors or last_parse_error or "Unknown failure",
        }

    def _inject_corrective_system_message(
        self,
        error_code: str,
        details: List[str],
        raw_response: str,
    ) -> None:
        """
        Inject a corrective system message to guide the model to fix its output on the next attempt.
        """
        # Keep the corrective message explicit and contract-focused.
        # Do not include long raw responses (can bloat context); include only a short excerpt if needed.
        excerpt = raw_response[:400].replace("\n", " ").strip()

        corrective = (
            "CORRECTION REQUIRED.\n"
            "You MUST return ONLY a valid JSON object that EXACTLY matches the required contract.\n"
            "No markdown, no backticks, no extra keys, no missing keys, no renamed fields.\n"
            f"Active contract: {getattr(self.contract, 'name', 'unknown')}\n"
            f"Previous failure type: {error_code}\n"
            "Validation errors:\n"
            + "\n".join([f"- {e}" for e in details])
            + "\n"
            f"Previous response excerpt (first 400 chars): {excerpt}\n"
            "Now return the corrected JSON object only."
        )

        self.messages.append({"role": "system", "content": corrective})
