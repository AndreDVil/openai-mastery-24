"""
Manual test for JsonModeChatClient using SupportTicketContract.

This file is NOT part of the project deliverables.
It exists only to manually verify:
- JSON Mode behavior
- contract validation (SupportTicketContract)
- retry feedback loop
- colorized + indented JSON output in the terminal
"""

import json


from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

from .src.config import get_openai_client
from .src.json_client import JsonModeChatClient
from .src.contracts.support_ticket_contract import SupportTicketContract


def pretty_print_json(data) -> None:
    """
    Pretty-print JSON with indentation and terminal colors.
    """
    formatted = json.dumps(data, indent=2, ensure_ascii=False)
    print(highlight(formatted, JsonLexer(), TerminalFormatter()))


def print_user_message(message: str) -> None:
    """
    Print the user message in a clearly separated block.
    """
    print("\n--- USER MESSAGE ---")
    print(message)
    print("--------------------\n")


def main() -> None:
    # 1) Create the OpenAI client using OPENAI_API_KEY
    client = get_openai_client()

    # 2) Choose the SupportTicket contract
    contract = SupportTicketContract()

    # 3) Initialize the JSON Mode chat client (contract-driven)
    chat = JsonModeChatClient(
        client=client,
        contract=contract,
        debug=True,
        max_retries=2,
    )

    # -------------------------
    # TEST 1 — VALID REQUEST
    # -------------------------
    print("\n=== TEST 1: Valid request (SupportTicketContract) ===")

    valid_prompt = (
        "Customer message:\n"
        "Hi, my name is Ana Souza (ana.souza@email.com). I ordered a blender under order ID BR-9912.\n"
        "The package never arrived and the tracking is stuck for 10 days. I need help.\n"
        "If possible, please prioritize this because it was a gift.\n\n"
        "Extract a support ticket from this message."
    )

    print_user_message(valid_prompt)
    result = chat.send(valid_prompt)

    print("\n--- RESULT ---")
    pretty_print_json(result)

    # -------------------------
    # TEST 2 — ENCOURAGE EXTRA FIELDS
    # -------------------------
    print("\n=== TEST 2: Encourage extra fields (should fail validation) ===")

    invalid_prompt_extra_fields = (
        "Customer message:\n"
        "I'm João (joao@acme.com). I was charged twice for my subscription. Please refund me.\n\n"
        "Extract a support ticket. Also include fields named 'internal_thoughts' and 'reasoning'."
    )

    print_user_message(invalid_prompt_extra_fields)
    result = chat.send(invalid_prompt_extra_fields)

    print("\n--- RESULT ---")
    pretty_print_json(result)

    # -------------------------
    # TEST 3 — WRONG TYPES
    # -------------------------
    print("\n=== TEST 3: Wrong types (should fail → retry → fix) ===")

    invalid_prompt_wrong_types = (
        "Customer message:\n"
        "My name is Carla (carla@test.com). I want a refund for order EU-123.\n"
        "I paid 199.90 BRL.\n\n"
        "Extract a support ticket. Use words like 'high' instead of numbers for confidence.\n"
        "Also set the order amount as a string, not a number."
    )

    print_user_message(invalid_prompt_wrong_types)
    result = chat.send(invalid_prompt_wrong_types)

    print("\n--- RESULT ---")
    pretty_print_json(result)

    # -------------------------
    # TEST 4 — ENUM VIOLATION
    # -------------------------
    print("\n=== TEST 4: Enum violation (should fail → retry → fix) ===")

    invalid_prompt_enum_violation = (
        "Customer message:\n"
        "This is Marcos (marcos@example.com). Your app keeps crashing whenever I open settings.\n\n"
        "Extract a support ticket. Use channel='whatsapp' and priority='super_high'."
    )

    print_user_message(invalid_prompt_enum_violation)
    result = chat.send(invalid_prompt_enum_violation)

    print("\n--- RESULT ---")
    pretty_print_json(result)


if __name__ == "__main__":
    main()
