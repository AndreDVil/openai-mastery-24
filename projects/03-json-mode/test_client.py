"""
Quick manual test for the minimal JsonModeChatClient.

This file is NOT part of the project deliverables.
It only exists to help you verify that the basic client works end-to-end.
"""

from projects._03_json_mode.src.config import get_openai_client
from projects._03_json_mode.src.json_client import JsonModeChatClient


def main():
    # Create the OpenAI client using the environment variable OPENAI_API_KEY
    client = get_openai_client()

    # Initialize the minimal JSON Mode chat client
    chat = JsonModeChatClient(client)

    # Send a simple test request
    print("Sending test message to the model...\n")

    result = chat.send("Say hello in a JSON object with a field named 'message'.")

    # Print the parsed JSON result (or the error structure)
    print("Model response:\n")
    print(result)


if __name__ == "__main__":
    main()
