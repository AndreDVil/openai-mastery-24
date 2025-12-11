#!/usr/bin/env python3

"""
Project 01 : Basic Chat (CLI)
Simple CLI for the OpenAI Responses API with basic sampling controls.
"""

import argparse
import time
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables and initialize OpenAI client
load_dotenv()
client = OpenAI()

# ANSI color codes for terminal output
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


def parse_args():
    """Parse command-line arguments for the CLI chat tool."""
    parser = argparse.ArgumentParser(
        description="Project 01 - Basic Chat (CLI) using the OpenAI Responses API."
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
        "--top_p",
        type=float,
        default=1.0,
        help="Nucleus sampling top_p (0.0-1.0, default: 1.0)",
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Maximum number of output tokens (min 16, default: None = model default)",
    )

    return parser.parse_args()


def main(args):
    max_tokens = args.max_tokens
    if max_tokens is not None and max_tokens < 16:
        print("max-tokens is below the API minimum (16); using 16 instead.")
        max_tokens = 16

    print("=== Project 01 - Basic Chat ===")
    print(f"Using model: {args.model}")
    print(f"Temperature: {args.temperature} | top_p: {args.top_p}")
    display_max_tokens = max_tokens if max_tokens is not None else "model default"
    print(f"Max tokens: {display_max_tokens}")
    print("Type '/exit' to quit.\n")

    while True:
        try:
            user_input = input(f"{YELLOW}You:{RESET} ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if user_input.strip().lower() == "/exit":
            print("Goodbye!")
            break

        if not user_input.strip():
            print("(empty input, type something or '/exit')")
            continue

        # ---- Call to OpenAI API ----
        start = time.time()
        response = client.responses.create(
            model=args.model,
            input=user_input,
            temperature=args.temperature,
            top_p=args.top_p,
            max_output_tokens=max_tokens,
        )
        elapsed = time.time() - start

        # ---- Output formatting with colors ----
        print(f"\n{CYAN}Assistant:{RESET}\n")
        print(response.output_text)

        # ---- Token usage ----
        usage = response.usage
        print(f"\n{MAGENTA}[latency: {elapsed:.3f}s]{RESET}")
        print(
            f"{MAGENTA}[tokens - input: {usage.input_tokens}, "
            f"output: {usage.output_tokens}, total: {usage.total_tokens}]{RESET}"
        )
        print("-" * 50)


if __name__ == "__main__":
    cli_args = parse_args()
    main(cli_args)
