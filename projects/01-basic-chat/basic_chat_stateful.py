#!/usr/bin/env python3

"""
Project 01 : Basic Chat (CLI) - Stateful version
Stateful CLI chat using the OpenAI Responses API.
Keeps full conversation history in memory during the session and logs it to file.
"""

import argparse
import time
from datetime import datetime
import os

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

# Log directory
LOG_DIR = "logs"


def init_log_file(args, stateful: bool = True):
    """
    Initialize a log file for the current chat session.
    Returns an open file handle.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    mode = "stateful" if stateful else "stateless"
    filename = os.path.join(LOG_DIR, f"project01-{mode}-{timestamp}.log")

    log_file = open(filename, "a", encoding="utf-8")

    # Write header with configuration
    log_file.write(f"# Project 01 - Basic Chat ({mode})\n")
    log_file.write(f"# Started at: {datetime.now().isoformat(timespec='seconds')}\n")
    log_file.write(f"# Model: {args.model}\n")
    log_file.write(f"# Temperature: {args.temperature}\n")
    log_file.write(f"# top_p: {args.top_p}\n")
    log_file.write(f"# Max tokens (arg): {args.max_tokens}\n")
    log_file.write("# ------------------------------\n\n")
    log_file.flush()

    return log_file


def log_message(log_file, role: str, content: str):
    """
    Log a single message (user/assistant/system/command) to the log file.
    """
    if log_file is None:
        return

    timestamp = datetime.now().isoformat(timespec="seconds")
    role_upper = role.upper()
    log_file.write(f"[{timestamp}] {role_upper}: {content}\n")
    log_file.flush()


def initial_conversation():
    """Return a fresh conversation history with the system prompt."""
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant in a terminal chat session.",
        }
    ]


def handle_command(cmd: str, conversation: list, args) -> bool:
    """
    Handle internal slash commands.
    Returns True if the command was handled and the main loop should continue
    (i.e., skip the model call), or False if it is an unknown command.
    """
    cmd_clean = cmd.strip().lower()

    if cmd_clean == "/clear":
        # Reset conversation to only the system prompt
        conversation.clear()
        conversation.extend(initial_conversation())
        print("Conversation history cleared.")
        return True

    if cmd_clean == "/history":
        print("\n--- Conversation History (excluding system) ---")
        for msg in conversation:
            if msg["role"] == "system":
                continue
            role = msg["role"].upper()
            print(f"{role}: {msg['content']}")
        print("--- End of history ---\n")
        return True

    if cmd_clean == "/config":
        print("\n--- Current Configuration ---")
        print(f"Model: {args.model}")
        print(f"Temperature: {args.temperature}")
        print(f"top_p: {args.top_p}")
        print(f"Max tokens (arg): {args.max_tokens}")
        print("--- End of config ---\n")
        return True

    if cmd_clean == "/help":
        print("\n--- Available Commands ---")
        print("/help    - show this help message")
        print("/clear   - clear conversation history (reset context)")
        print("/history - print conversation history (excluding system)")
        print("/config  - show current configuration")
        print("/exit    - exit the program")
        print("--- End of help ---\n")
        return True

    return False  # Unknown command


def parse_args():
    """Parse command-line arguments for the stateful CLI chat tool."""
    parser = argparse.ArgumentParser(
        description="Project 01 - Basic Chat (STATEFUL CLI) using the OpenAI Responses API."
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
    # Enforce minimum max_tokens when provided
    max_tokens = args.max_tokens
    if max_tokens is not None and max_tokens < 16:
        print("max-tokens is below the API minimum (16); using 16 instead.")
        max_tokens = 16

    print("=== Project 01 - Basic Chat (STATEFUL) ===")
    print(f"Using model: {args.model}")
    print(f"Temperature: {args.temperature} | top_p: {args.top_p}")
    display_max_tokens = max_tokens if max_tokens is not None else "model default"
    print(f"Max tokens (effective): {display_max_tokens}")
    print("Type '/help' for commands. Type '/exit' to quit.\n")

    # Initialize log file for this session
    log_file = init_log_file(args, stateful=True)

    # ---- Conversation history ----
    conversation = initial_conversation()
    # Log initial system message
    log_message(log_file, "system", conversation[0]["content"])

    while True:
        try:
            user_input = input(f"{YELLOW}You:{RESET} ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            log_message(log_file, "command", "EOF/KeyboardInterrupt")
            break

        # Exit command
        if user_input.strip().lower() == "/exit":
            print("Goodbye!")
            log_message(log_file, "command", "/exit")
            break

        # Empty input check
        if not user_input.strip():
            print("(empty input, type something or '/exit')")
            continue

        # Slash commands handling (internal commands)
        if user_input.strip().startswith("/"):
            handled = handle_command(user_input, conversation, args)
            if handled:
                # Log handled command
                log_message(log_file, "command", user_input)
                # Command was processed; skip the model call
                continue
            else:
                print("Unknown command. Available: /help, /clear, /history, /config, /exit")
                log_message(log_file, "command", f"UNKNOWN {user_input}")
                continue

        # Append user message to the conversation history
        conversation.append({"role": "user", "content": user_input})
        log_message(log_file, "user", user_input)

        # ---- Call to OpenAI API with full history ----
        start = time.time()
        response = client.responses.create(
            model=args.model,
            input=conversation,
            temperature=args.temperature,
            top_p=args.top_p,
            max_output_tokens=max_tokens,
        )
        elapsed = time.time() - start

        # Extract assistant message text
        assistant_text = response.output_text

        # Append assistant message to the conversation history
        conversation.append({"role": "assistant", "content": assistant_text})
        log_message(log_file, "assistant", assistant_text)

        # ---- Output formatting with colors ----
        print(f"\n{CYAN}Assistant:{RESET}\n")
        print(assistant_text)

        # ---- Token usage ----
        usage = response.usage
        print(f"\n{MAGENTA}[latency: {elapsed:.3f}s]{RESET}")
        print(
            f"{MAGENTA}[tokens - input: {usage.input_tokens}, "
            f"output: {usage.output_tokens}, total: {usage.total_tokens}]{RESET}"
        )
        print("-" * 50)

    # Close log file on exit
    if log_file is not None:
        log_file.close()


if __name__ == "__main__":
    cli_args = parse_args()
    main(cli_args)
