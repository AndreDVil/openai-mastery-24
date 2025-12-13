import json
from openai import OpenAI
from typing import Dict, Any, Optional

from .config import get_default_params


class JsonModeChatClient:
    """
    Minimal JSON Mode chat client.

    This version sends a single request to the OpenAI API using JSON Mode
    and attempts to parse the response as a Python dictionary.
    """

    def __init__(
        self,
        client: OpenAI,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ):
        """
        Initialize the chat client.

        Parameters:
            client (OpenAI): The OpenAI client instance.
            model (str | None): Override model name if desired.
            system_prompt (str | None): Optional system instruction for the model.
        """
        self.client = client
        self.default_params = get_default_params()

        # Override model only if user provides a custom one
        if model:
            self.default_params["model"] = model

        # Internal message history list
        self.messages = []

        # Optional system instruction (helps the model understand the context)
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def send(self, user_input: str) -> Dict[str, Any]:
        """
        Send a user message to the model and return the parsed JSON response.

        This minimal version performs exactly one API call.
        No retries, no schema validation.
        """
        # Add user message to the history
        self.messages.append({"role": "user", "content": user_input})

        # Build request
        payload = {
            "model": self.default_params["model"],
            "response_format": self.default_params["response_format"],
            "temperature": self.default_params["temperature"],
            "input": self.messages,
        }

        # Perform the API request (Responses API)
        response = self.client.responses.create(**payload)

        # Extract raw text from the response (JSON string)
        raw_text = response.output_text

        # Try to parse JSON
        try:
            parsed = json.loads(raw_text)
            return parsed
        except Exception as e:
            # We do NOT retry here (this comes later)
            return {
                "error": "INVALID_JSON",
                "raw_response": raw_text,
                "details": str(e),
            }
