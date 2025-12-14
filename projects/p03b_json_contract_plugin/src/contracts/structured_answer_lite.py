import json
from typing import Any, Dict, List, Set

from .base import ValidationResult


class StructuredAnswerLiteContract:
    """
    Default contract for Project 03.

    Single source of truth:
    - CONTRACT_SPEC drives the system prompt contract block
    - Validation logic enforces the semantic rules
    """

    name = "structured_answer_lite"

    SCHEMA_VERSION: str = "1.0"

    CONTRACT_SPEC: Dict[str, Any] = {
        "task": {
            "type": "qa | extraction | classification | summarization | other",
            "user_intent": "string (non-empty)",
        },
        "answer": {"text": "string (non-empty)"},
        "quality": {
            "confidence": "number between 0.0 and 1.0",
            "assumptions": ["string"],
            "risks": ["string"],
        },
        "debug": {"schema_version": "1.0", "model": "string (model name)"},
    }

    ALLOWED_TASK_TYPES: Set[str] = {"qa", "extraction", "classification", "summarization", "other"}

    BASE_PROMPT: str = (
        "You are an AI assistant that must respond using STRICT JSON only.\n\n"
        "Your output MUST be a single JSON object that follows EXACTLY the contract below.\n"
        "Do NOT include explanations, markdown, comments, or any text outside the JSON object.\n"
        "Do NOT add extra keys.\n"
        "Do NOT omit required keys.\n"
        "Do NOT change key names.\n"
        "Do NOT nest fields differently.\n\n"
        "JSON CONTRACT (StructuredAnswerLite v1.0):\n"
    )

    RULES: str = (
        "\nRules:\n"
        "- Output JSON only.\n"
        "- All required fields must be present.\n"
        "- Arrays may be empty but must exist.\n"
        "- confidence must be between 0.0 and 1.0.\n"
        "- schema_version must be exactly \"1.0\".\n"
        "- Use the same model name you are running as the value for debug.model.\n"
    )

    @property
    def system_prompt(self) -> str:
        """
        Render the system prompt from CONTRACT_SPEC to avoid drift.
        """
        contract_block = self._render_contract_spec()
        return f"{self.BASE_PROMPT}\n{contract_block}\n{self.RULES}"

    def validate(self, payload: Any) -> ValidationResult:
        """
        Strict validation for StructuredAnswerLite v1.0.
        """
        errors: List[str] = []

        if not isinstance(payload, dict):
            return ValidationResult(ok=False, errors=["payload must be an object"])

        # --- top-level ---
        expected_top = {"task", "answer", "quality", "debug"}
        self._validate_exact_keys(payload, expected_top, "payload", errors)

        # --- task ---
        task = payload.get("task")
        if not isinstance(task, dict):
            errors.append("task must be an object")
        else:
            self._validate_exact_keys(task, {"type", "user_intent"}, "task", errors)

            ttype = task.get("type")
            if ttype not in self.ALLOWED_TASK_TYPES:
                errors.append(f"task.type must be one of {sorted(self.ALLOWED_TASK_TYPES)}")

            user_intent = task.get("user_intent")
            if not self._is_non_empty_str(user_intent):
                errors.append("task.user_intent must be a non-empty string")

        # --- answer ---
        answer = payload.get("answer")
        if not isinstance(answer, dict):
            errors.append("answer must be an object")
        else:
            self._validate_exact_keys(answer, {"text"}, "answer", errors)

            text = answer.get("text")
            if not self._is_non_empty_str(text):
                errors.append("answer.text must be a non-empty string")

        # --- quality ---
        quality = payload.get("quality")
        if not isinstance(quality, dict):
            errors.append("quality must be an object")
        else:
            self._validate_exact_keys(quality, {"confidence", "assumptions", "risks"}, "quality", errors)

            conf = quality.get("confidence")
            if not isinstance(conf, (int, float)):
                errors.append("quality.confidence must be a number")
            else:
                if float(conf) < 0.0 or float(conf) > 1.0:
                    errors.append("quality.confidence must be between 0.0 and 1.0")

            self._validate_string_array(quality.get("assumptions"), "quality.assumptions", errors)
            self._validate_string_array(quality.get("risks"), "quality.risks", errors)

        # --- debug ---
        debug = payload.get("debug")
        if not isinstance(debug, dict):
            errors.append("debug must be an object")
        else:
            self._validate_exact_keys(debug, {"schema_version", "model"}, "debug", errors)

            if debug.get("schema_version") != self.SCHEMA_VERSION:
                errors.append(f"debug.schema_version must be '{self.SCHEMA_VERSION}'")

            model = debug.get("model")
            if not self._is_non_empty_str(model):
                errors.append("debug.model must be a non-empty string")

        return ValidationResult(ok=not errors, errors=errors)

    def _render_contract_spec(self) -> str:
        """
        Render CONTRACT_SPEC as deterministic JSON for prompt stability.
        """
        return json.dumps(self.CONTRACT_SPEC, indent=2, ensure_ascii=False)

    def _validate_exact_keys(self, obj: Dict[str, Any], expected: Set[str], path: str, errors: List[str]) -> None:
        actual = set(obj.keys())
        if actual != expected:
            errors.append(f"{path} must have exactly keys {sorted(expected)}")

    def _validate_string_array(self, value: Any, path: str, errors: List[str]) -> None:
        if not isinstance(value, list):
            errors.append(f"{path} must be an array")
            return
        for i, item in enumerate(value):
            if not isinstance(item, str):
                errors.append(f"{path}[{i}] must be a string")

    def _is_non_empty_str(self, value: Any) -> bool:
        return isinstance(value, str) and len(value.strip()) > 0
