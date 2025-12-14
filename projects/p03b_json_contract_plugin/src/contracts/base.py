from dataclasses import dataclass
from typing import Any, List, Protocol


@dataclass
class ValidationResult:
    """
    Result of a contract validation.

    Attributes:
        ok: Indicates whether the payload is valid.
        errors: List of human-readable validation error messages.
    """
    ok: bool
    errors: List[str]


class Contract(Protocol):
    """
    Protocol defining a pluggable JSON contract.

    A contract encapsulates:
    - The governing system prompt
    - The semantic validation logic for the JSON payload

    The chat client must treat contracts as opaque objects and
    interact with them only through this interface.
    """

    # Human-readable unique name of the contract
    name: str

    # System prompt enforcing behavior and JSON contract
    system_prompt: str

    def validate(self, payload: Any) -> ValidationResult:
        """
        Validate a parsed JSON payload against the contract.

        Parameters:
            payload: Parsed JSON object (already syntactically valid).

        Returns:
            ValidationResult indicating success or listing validation errors.
        """
        ...
