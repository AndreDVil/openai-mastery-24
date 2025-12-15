import json
from typing import Any, Dict, List, Set

from .base import ValidationResult


class SupportTicketContract:
    """
    Contract for extracting a structured customer support ticket
    from free-form user messages.

    This contract uses a single source of truth (CONTRACT_SPEC) to render the
    system prompt contract block, reducing drift between prompt and validation.
    """

    name = "support_ticket"

    # Single source of truth for the contract structure shown to the model.
    # Notes:
    # - Types and constraints are expressed as strings for human/model readability.
    # - Validation logic enforces the real semantics (enums, required keys, types, bounds).
    CONTRACT_SPEC: Dict[str, Any] = {
        "ticket": {
            "channel": "email | chat | phone | other",
            "customer": {"name": "string", "email": "string"},
            "intent": "refund | delivery_issue | billing | bug | feature_request | other",
            "priority": "low | medium | high | urgent",
            "summary": "string",
            "order": {
                "order_id": "string | null",
                "amount": "number | null",
                "currency": "BRL | USD | EUR | null",
            },
            "entities": ["string"],
            "suggested_actions": ["string"],
        },
        "quality": {
            "confidence": "number between 0.0 and 1.0",
            "assumptions": ["string"],
            "risks": ["string"],
        },
        "debug": {"schema_version": "1.0", "model": "string"},
    }

    # Enumerations used by the validator (and implicitly documented by CONTRACT_SPEC).
    ALLOWED_CHANNELS: Set[str] = {"email", "chat", "phone", "other"}
    ALLOWED_INTENTS: Set[str] = {
        "refund",
        "delivery_issue",
        "billing",
        "bug",
        "feature_request",
        "other",
    }
    ALLOWED_PRIORITIES: Set[str] = {"low", "medium", "high", "urgent"}
    ALLOWED_CURRENCIES: Set[str] = {"BRL", "USD", "EUR"}
    SCHEMA_VERSION: str = "1.0"

    BASE_PROMPT: str = (
        "You are a system that extracts customer support tickets from user messages.\n\n"
        "You MUST return ONLY a valid JSON object.\n"
        "No markdown, no explanations, no extra text.\n\n"
        "The JSON MUST strictly follow this contract:\n"
    )

    RULES: str = (
        "\nRules:\n"
        "- All fields MUST be present.\n"
        "- No extra fields are allowed.\n"
        "- Arrays may be empty, but must exist.\n"
        "- Use null explicitly when information is missing.\n"
        "- confidence MUST be between 0.0 and 1.0.\n"
        "- schema_version MUST be exactly \"1.0\".\n"
    )

    @property
    def system_prompt(self) -> str:
        """
        Render the system prompt from a single source of truth (CONTRACT_SPEC).

        Using a property ensures the prompt stays consistent with CONTRACT_SPEC.
        """
        contract_block = self._render_contract_spec()
        return f"{self.BASE_PROMPT}\n{contract_block}\n{self.RULES}"

    # --- Public API -------------------------------------------------

    def validate(self, payload: Any) -> ValidationResult:
        """
        Validate payload against the SupportTicket contract.

        Parameters:
            payload: Parsed JSON object (already syntactically valid JSON).

        Returns:
            ValidationResult indicating whether the payload matches the contract.
        """
        errors: List[str] = []

        if not isinstance(payload, dict):
            return ValidationResult(ok=False, errors=["Top-level JSON must be an object."])

        self._validate_root(payload, errors)
        self._validate_ticket(payload.get("ticket"), errors)
        self._validate_quality(payload.get("quality"), errors)
        self._validate_debug(payload.get("debug"), errors)

        return ValidationResult(ok=not errors, errors=errors)

    # --- Prompt rendering ------------------------------------------

    def _render_contract_spec(self) -> str:
        """
        Render CONTRACT_SPEC as deterministic JSON for prompt stability.
        """
        return json.dumps(self.CONTRACT_SPEC, indent=2, ensure_ascii=False)

    # --- Validation helpers ----------------------------------------

    def _validate_root(self, payload: Dict[str, Any], errors: List[str]) -> None:
        expected_keys = {"ticket", "quality", "debug"}
        self._validate_exact_keys(payload, expected_keys, "root", errors)

    def _validate_ticket(self, ticket: Any, errors: List[str]) -> None:
        if not isinstance(ticket, dict):
            errors.append("ticket must be an object.")
            return

        expected_keys = {
            "channel",
            "customer",
            "intent",
            "priority",
            "summary",
            "order",
            "entities",
            "suggested_actions",
        }
        self._validate_exact_keys(ticket, expected_keys, "ticket", errors)

        self._validate_enum(ticket.get("channel"), self.ALLOWED_CHANNELS, "ticket.channel", errors)
        self._validate_customer(ticket.get("customer"), errors)
        self._validate_enum(ticket.get("intent"), self.ALLOWED_INTENTS, "ticket.intent", errors)
        self._validate_enum(ticket.get("priority"), self.ALLOWED_PRIORITIES, "ticket.priority", errors)
        self._validate_string(ticket.get("summary"), "ticket.summary", errors)
        self._validate_order(ticket.get("order"), errors)
        self._validate_string_array(ticket.get("entities"), "ticket.entities", errors)
        self._validate_string_array(ticket.get("suggested_actions"), "ticket.suggested_actions", errors)

    def _validate_customer(self, customer: Any, errors: List[str]) -> None:
        if not isinstance(customer, dict):
            errors.append("ticket.customer must be an object.")
            return

        expected_keys = {"name", "email"}
        self._validate_exact_keys(customer, expected_keys, "ticket.customer", errors)

        self._validate_string(customer.get("name"), "ticket.customer.name", errors)
        self._validate_string(customer.get("email"), "ticket.customer.email", errors)

    def _validate_order(self, order: Any, errors: List[str]) -> None:
        if not isinstance(order, dict):
            errors.append("ticket.order must be an object.")
            return

        expected_keys = {"order_id", "amount", "currency"}
        self._validate_exact_keys(order, expected_keys, "ticket.order", errors)

        self._validate_string_or_null(order.get("order_id"), "ticket.order.order_id", errors)
        self._validate_number_or_null(order.get("amount"), "ticket.order.amount", errors)
        self._validate_enum_or_null(
            order.get("currency"),
            self.ALLOWED_CURRENCIES,
            "ticket.order.currency",
            errors,
        )

    def _validate_quality(self, quality: Any, errors: List[str]) -> None:
        if not isinstance(quality, dict):
            errors.append("quality must be an object.")
            return

        expected_keys = {"confidence", "assumptions", "risks"}
        self._validate_exact_keys(quality, expected_keys, "quality", errors)

        conf = quality.get("confidence")
        if not isinstance(conf, (int, float)) or not (0.0 <= float(conf) <= 1.0):
            errors.append("quality.confidence must be a number between 0.0 and 1.0.")

        self._validate_string_array(quality.get("assumptions"), "quality.assumptions", errors)
        self._validate_string_array(quality.get("risks"), "quality.risks", errors)

    def _validate_debug(self, debug: Any, errors: List[str]) -> None:
        if not isinstance(debug, dict):
            errors.append("debug must be an object.")
            return

        expected_keys = {"schema_version", "model"}
        self._validate_exact_keys(debug, expected_keys, "debug", errors)

        if debug.get("schema_version") != self.SCHEMA_VERSION:
            errors.append(f'debug.schema_version must be exactly "{self.SCHEMA_VERSION}".')

        self._validate_string(debug.get("model"), "debug.model", errors)

    # --- Generic validators ----------------------------------------

    def _validate_exact_keys(
        self,
        obj: Dict[str, Any],
        expected: Set[str],
        path: str,
        errors: List[str],
    ) -> None:
        actual = set(obj.keys())
        if actual != expected:
            errors.append(f"{path} must have exactly keys {sorted(expected)}.")

    def _validate_string(self, value: Any, path: str, errors: List[str]) -> None:
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path} must be a non-empty string.")

    def _validate_string_or_null(self, value: Any, path: str, errors: List[str]) -> None:
        if value is not None and not isinstance(value, str):
            errors.append(f"{path} must be a string or null.")

    def _validate_number_or_null(self, value: Any, path: str, errors: List[str]) -> None:
        if value is not None and not isinstance(value, (int, float)):
            errors.append(f"{path} must be a number or null.")

    def _validate_enum(self, value: Any, allowed: Set[str], path: str, errors: List[str]) -> None:
        if value not in allowed:
            errors.append(f"{path} must be one of {sorted(allowed)}.")

    def _validate_enum_or_null(self, value: Any, allowed: Set[str], path: str, errors: List[str]) -> None:
        if value is not None and value not in allowed:
            errors.append(f"{path} must be one of {sorted(allowed)} or null.")

    def _validate_string_array(self, value: Any, path: str, errors: List[str]) -> None:
        if not isinstance(value, list):
            errors.append(f"{path} must be an array.")
            return

        for i, item in enumerate(value):
            if not isinstance(item, str):
                errors.append(f"{path}[{i}] must be a string.")
