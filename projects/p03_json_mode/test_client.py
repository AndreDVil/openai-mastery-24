"""
Quick manual test for the JsonModeChatClient (Project 03).

This file is NOT part of the project deliverables.
It exists only to manually verify:
- JSON Mode behavior
- schema validation
- error handling
"""

from projects.p03_json_mode.src.config import get_openai_client
from projects.p03_json_mode.src.json_client import JsonModeChatClient


def main():
    # 1) Create the OpenAI client using OPENAI_API_KEY
    client = get_openai_client()

    # 2) Initialize the JSON Mode chat client
    chat = JsonModeChatClient(client, debug=True)

    # -------------------------
    # TEST 1 — VALID REQUEST
    # -------------------------
    print("\n=== TEST 1: Valid request ===\n")

    valid_prompt = (
        "Explain what JSON Mode is in the OpenAI Python SDK 2.9 "
        "and how it should be used in a production system."
    )

    result = chat.send(valid_prompt)
    print("Result:\n", result)

    # -------------------------
    # TEST 2 — PROMPT THAT ENCOURAGES EXTRA FIELDS
    # -------------------------
    print("\n=== TEST 2: Encourage extra fields (should fail validation) ===\n")

    invalid_prompt_extra_fields = (
        "Explain JSON Mode, and also include your reasoning process "
        "and any internal thoughts you used to generate the answer."
    )

    result = chat.send(invalid_prompt_extra_fields)
    print("Result:\n", result)

    # -------------------------
    # TEST 3 — PROMPT THAT ENCOURAGES WRONG TYPES
    # -------------------------
    print("\n=== TEST 3: Encourage wrong types (should fail validation) ===\n")

    invalid_prompt_wrong_types = (
        "Explain JSON Mode. "
        "For confidence, use words like 'high' or 'low' instead of numbers."
    )

    result = chat.send(invalid_prompt_wrong_types)
    print("Result:\n", result)


if __name__ == "__main__":
    main()

