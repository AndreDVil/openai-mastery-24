#!/usr/bin/env python3

"""
Project 01 : Basic Chat (CLI) - Stateless
Simple stateless CLI chat client using the OpenAI Python SDK 2.9.0
and the modern Chat Completions endpoint (client.chat.completions.create).
"""

import argparse
import os
import time

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (.env should contain OPENAI_API_KEY)
load_dotenv()

# Unified OpenAI client (SDK 2.x pattern)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# ANSI color codes for terminal output
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


def parse_args():
    """Parse command-line arguments for the stateless CLI chat tool."""
    parser = argparse.ArgumentParser(
        description=(
            "Project 01 - Basic Chat (Stateless CLI) using the "
            "OpenAI Chat Completions API (SDK 2.9.0)."
        )
    )

    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        help="OpenAI model ID to use (default: gpt-4o-mini)",
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature (0.0-2.0, default: 0.7)",
    )

    parser.add_argument(
        "--top-p",
        type=float,
        default=1.0,
        help="Nucleus sampling top_p (0.0-1.0, default: 1.0)",
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Maximum number of output tokens (min 16, default: model default)",
    )

    return parser.parse_args()


def main(args):
    """
    Main stateless chat loop.

    Each user message is sent independently to the model.
    No conversation history is preserved between turns.
    """
    max_tokens = args.max_tokens
    if max_tokens is not None and max_tokens < 16:
        print("max-tokens is below the API minimum (16); using 16 instead.")
        max_tokens = 16

    print("=== Project 01 - Basic Chat (STATELESS) ===")
    print(f"Using model: {args.model}")
    print(f"Temperature: {args.temperature} | top_p: {args.top_p}")
    effective_max = max_tokens if max_tokens is not None else "model default"
    print(f"Max tokens (effective): {effective_max}")
    print("Backend: chat.completions.create (OpenAI SDK 2.9.0)\n")
    print("Type '/exit' to quit.\n")

    while True:
        try:
            user_input = input(f"{YELLOW}You:{RESET} ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        # Exit command
        if user_input.strip().lower() == "/exit":
            print("Goodbye!")
            break

        # Ignore empty input
        if not user_input.strip():
            print("(empty input, type something or '/exit')")
            continue

        # --- Call to OpenAI Chat Completions API (stateless) ---
        start = time.time()
        completion = client.chat.completions.create(
            model=args.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant in a terminal chat session.",
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=max_tokens,
        )
        elapsed = time.time() - start

        # Extract assistant message text
        assistant_message = completion.choices[0].message
        assistant_text = assistant_message.content

        # --- Output formatting with colors ---
        print(f"\n{CYAN}Assistant:{RESET}\n")
        print(assistant_text)

        # --- Token usage and latency ---
        usage = completion.usage
        # For chat.completions: prompt_tokens, completion_tokens, total_tokens
        print(f"\n{MAGENTA}[latency: {elapsed:.3f}s]{RESET}")
        print(
            f"{MAGENTA}[tokens - input: {usage.prompt_tokens}, "
            f"output: {usage.completion_tokens}, total: {usage.total_tokens}]{RESET}"
        )
        print("-" * 50)


if __name__ == "__main__":
    cli_args = parse_args()
    main(cli_args)
