#!/usr/bin/env python3

"""
Project 01 : Basic Chat (CLI) - Stateful
Stateful CLI chat client using the OpenAI Python SDK 2.9.0 and
the Chat Completions endpoint (client.chat.completions.create).

This version keeps full conversation history in memory during the session
and supports internal slash commands. It can also log the session to disk.
"""

import argparse
import os
import time
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (.env should contain OPENAI_API_KEY)
load_dotenv()

# Unified OpenAI client (SDK 2.9.0 pattern)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# ANSI color codes for terminal output
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

LOG_DIR = "logs"


def parse_args():
    """Parse command-line arguments for the stateful CLI chat tool."""
    parser = argparse.ArgumentParser(
        description=(
            "Project 01 - Basic Chat (Stateful CLI) using the "
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

    parser.add_argument(
        "--no-log",
        action="store_true",
        help="Disable writing a session log file to disk.",
    )

    return parser.parse_args()


def init_log_file(args):
    """Create and open a timestamped log file for the current session."""
    os.makedirs(LOG_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(LOG_DIR, f"project01-stateful-{ts}.log")
    f = open(path, "a", encoding="utf-8")

    f.write("# Project 01 - Basic Chat (stateful)\n")
    f.write(f"# Started at: {datetime.now().isoformat(timespec='seconds')}\n")
    f.write(f"# Model: {args.model}\n")
    f.write(f"# Temperature: {args.temperature}\n")
    f.write(f"# top_p: {args.top_p}\n")
    f.write(f"# Max tokens (arg): {args.max_tokens}\n")
    f.write("# ------------------------------\n\n")
    f.flush()

    return f, path


def log_line(log_file, role: str, content: str):
    """Write a single timestamped line to the log file."""
    if log_file is None:
        return
    ts = datetime.now().isoformat(timespec="seconds")
    log_file.write(f"[{ts}] {role.upper()}: {content}\n")
    log_file.flush()


def initial_messages(system_prompt: str):
    """Create the initial messages list with a system prompt."""
    return [{"role": "system", "content": system_prompt}]


def print_config(args, effective_max_tokens):
    """Pretty print current runtime configuration."""
    print("\n--- Current Configuration ---")
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"top_p: {args.top_p}")
    print(f"Max tokens (effective): {effective_max_tokens}")
    print("Backend: chat.completions.create (OpenAI SDK 2.9.0)")
    print("--- End of config ---\n")


def print_help():
    """Print available slash commands."""
    print("\n--- Available Commands ---")
    print("/help    - show this help message")
    print("/history - print conversation history (excluding system)")
    print("/clear   - clear conversation history (reset to system prompt)")
    print("/config  - show current configuration")
    print("/exit    - exit the program")
    print("--- End of help ---\n")


def print_history(messages):
    """Print conversation history excluding the system prompt."""
    print("\n--- Conversation History (excluding system) ---")
    for msg in messages:
        if msg.get("role") == "system":
            continue
        role = msg.get("role", "").upper()
        content = msg.get("content", "")
        print(f"{role}: {content}")
    print("--- End of history ---\n")


def handle_command(user_input: str, messages: list, args, effective_max_tokens, log_file):
    """
    Handle internal commands.
    Returns True if a command was handled and the main loop should continue,
    False otherwise.
    """
    cmd = user_input.strip().lower()

    if cmd == "/help":
        print_help()
        log_line(log_file, "command", user_input)
        return True

    if cmd == "/config":
        print_config(args, effective_max_tokens)
        log_line(log_file, "command", user_input)
        return True

    if cmd == "/history":
        print_history(messages)
        log_line(log_file, "command", user_input)
        return True

    if cmd == "/clear":
        # Keep only the first system message (index 0)
        system_msg = messages[0]
        messages.clear()
        messages.append(system_msg)
        print("Conversation history cleared.")
        log_line(log_file, "command", user_input)
        return True

    return False


def main(args):
    max_tokens = args.max_tokens
    if max_tokens is not None and max_tokens < 16:
        print("max-tokens is below the API minimum (16); using 16 instead.")
        max_tokens = 16

    effective_max = max_tokens if max_tokens is not None else "model default"

    print("=== Project 01 - Basic Chat (STATEFUL) ===")
    print(f"Using model: {args.model}")
    print(f"Temperature: {args.temperature} | top_p: {args.top_p}")
    print(f"Max tokens (effective): {effective_max}")
    print("Backend: chat.completions.create (OpenAI SDK 2.9.0)")
    print("Type '/help' for commands. Type '/exit' to quit.\n")

    log_file = None
    log_path = None
    if not args.no_log:
        log_file, log_path = init_log_file(args)
        print(f"{MAGENTA}[logging enabled → {log_path}]{RESET}")

    system_prompt = "You are a helpful assistant in a terminal chat session."
    messages = initial_messages(system_prompt)
    log_line(log_file, "system", system_prompt)

    while True:
        try:
            user_input = input(f"{YELLOW}You:{RESET} ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            log_line(log_file, "command", "EOF/KeyboardInterrupt")
            break

        # Exit command
        if user_input.strip().lower() == "/exit":
            print("Goodbye!")
            log_line(log_file, "command", user_input)
            break

        # Empty input
        if not user_input.strip():
            print("(empty input, type something or '/exit')")
            continue

        # Commands
        if user_input.strip().startswith("/"):
            handled = handle_command(
                user_input=user_input,
                messages=messages,
                args=args,
                effective_max_tokens=effective_max,
                log_file=log_file,
            )
            if handled:
                continue

            print("Unknown command. Available: /help, /history, /clear, /config, /exit")
            log_line(log_file, "command", f"UNKNOWN {user_input}")
            continue

        # Append user message to memory
        messages.append({"role": "user", "content": user_input})
        log_line(log_file, "user", user_input)

        # Call OpenAI (stateful: send full message history)
        start = time.time()
        completion = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=max_tokens,
        )
        elapsed = time.time() - start

        choice = completion.choices[0]
        assistant_text = choice.message.content or ""

        # Append assistant message to memory
        messages.append({"role": "assistant", "content": assistant_text})
        log_line(log_file, "assistant", assistant_text)

        # Output
        print(f"\n{CYAN}Assistant:{RESET}\n")
        print(assistant_text)

        # Token usage
        usage = completion.usage
        print(f"\n{MAGENTA}[latency: {elapsed:.3f}s]{RESET}")
        print(
            f"{MAGENTA}[tokens - input: {usage.prompt_tokens}, "
            f"output: {usage.completion_tokens}, total: {usage.total_tokens}]{RESET}"
        )

        # Finish reason (useful for debugging)
        if choice.finish_reason:
            print(f"{MAGENTA}[finish_reason: {choice.finish_reason}]{RESET}")

        print("-" * 50)

    if log_file is not None:
        log_file.close()


if __name__ == "__main__":
    cli_args = parse_args()
    main(cli_args)
