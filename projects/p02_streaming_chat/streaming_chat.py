#!/usr/bin/env python3
"""
Project 02 - Streaming Chat Client (STATLESS)
openai-mastery-24

This script implements a CLI chat client that uses OpenAI's Responses API
with streaming enabled. It is stateless by design: each user message is sent
as a fresh request, without retaining conversation history.
"""

import argparse
import os
import sys
import time
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI


# ─────────────────────────────────────────────────────────────────────────────
# Environment & client initialization
# ─────────────────────────────────────────────────────────────────────────────

load_dotenv()
client = OpenAI()

LOG_DIR = "logs"

# ANSI color codes (simple, inspired by Project 01)
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
GREY = "\033[90m"


# ─────────────────────────────────────────────────────────────────────────────
# Logging (simplified)
# ─────────────────────────────────────────────────────────────────────────────

def init_log_file(args):
    """
    Initialize a simplified log file for the streaming chat session.
    Returns an open file handle or None if logging fails.
    """
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(LOG_DIR, f"project02-streaming-{timestamp}.log")

        log_file = open(filename, "a", encoding="utf-8")

        # Minimal header
        log_file.write("# Project 02 - Streaming Chat (stateless)\n")
        log_file.write(f"# Started at: {datetime.now().isoformat(timespec='seconds')}\n")
        log_file.write(f"# Model: {args.model}\n")
        log_file.write(f"# Temperature: {args.temperature}\n")
        log_file.write(f"# top_p: {args.top_p}\n")
        log_file.write(f"# Max output tokens (arg): {args.max_output_tokens}\n")
        log_file.write("# ----------------------------------------\n\n")
        log_file.flush()

        return log_file
    except Exception as e:
        print(f"{MAGENTA}[log disabled: {e}]{RESET}", file=sys.stderr)
        return None


def log_line(log_file, label: str, content: str) -> None:
    """
    Log a single line with a timestamp and a label (USER / ASSISTANT / INFO / ERROR).
    """
    if log_file is None:
        return
    timestamp = datetime.now().isoformat(timespec="seconds")
    log_file.write(f"[{timestamp}] {label.upper()}: {content}\n")
    log_file.flush()


# ─────────────────────────────────────────────────────────────────────────────
# CLI configuration
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    """Parse command-line arguments for the stateless streaming chat client."""
    parser = argparse.ArgumentParser(
        description="Project 02 - Streaming Chat Client (stateless, OpenAI Responses API)."
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
        "--max-output-tokens",
        type=int,
        default=None,
        help="Maximum number of output tokens (min 16, default: None = model default)",
    )

    parser.add_argument(
        "--system",
        type=str,
        default=None,
        help="Optional system prompt to steer the assistant behavior.",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colors in the terminal output.",
    )

    args = parser.parse_args()

    # Attach a derived attribute for color usage
    args.use_colors = not args.no_color

    return args


def colorize(text: str, color: str, enabled: bool) -> str:
    """Return colored text if colors are enabled, otherwise plain text."""
    if not enabled:
        return text
    return f"{color}{text}{RESET}"


def print_header(args) -> None:
    """Print a simple project header with configuration info."""
    line = "─" * 60
    print(line)
    print("Project 02 · Streaming Chat Client (stateless)")
    print(line)
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature} · top_p: {args.top_p}")
    if args.max_output_tokens is not None:
        print(f"Max output tokens: {args.max_output_tokens}")
    else:
        print("Max output tokens: (model default)")
    if args.system:
        preview = args.system[:60]
        suffix = "..." if len(args.system) > 60 else ""
        print(f"System prompt: {preview}{suffix}")
    else:
        print("System prompt: (none)")
    print("Commands: /help · /config · /exit")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Core helpers
# ─────────────────────────────────────────────────────────────────────────────

def build_input_messages(user_input: str, args) -> list[dict]:
    """
    Build the 'input' list for the Responses API using a stateless design:
    optional system message + a single user message.
    """
    messages: list[dict] = []
    if args.system:
        messages.append(
            {
                "role": "system",
                "content": args.system,
            }
        )
    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )
    return messages


def stream_chat_once(user_input: str, args, log_file) -> str:
    """
    Send a single stateless request to the Responses API with stream=True
    and print assistant tokens as they arrive.

    Returns the full assistant text (useful for logging).
    """
    # Enforce minimum max_output_tokens if provided
    max_output_tokens = args.max_output_tokens
    if max_output_tokens is not None and max_output_tokens < 16:
        print(
            colorize(
                "[max-output-tokens below minimum (16); using 16 instead]",
                MAGENTA,
                args.use_colors,
            )
        )
        max_output_tokens = 16

    input_messages = build_input_messages(user_input, args)

    start_time = time.perf_counter()
    first_token_time: float | None = None
    full_text_chunks: list[str] = []

    try:
        stream = client.responses.create(
            model=args.model,
            input=input_messages,
            temperature=args.temperature,
            top_p=args.top_p,
            max_output_tokens=max_output_tokens,
            stream=True,
        )

        assistant_label = colorize("Assistant", CYAN, args.use_colors)
        print(f"\n{assistant_label} (streaming...)\n")

        for event in stream:
            # We focus on the text delta events for streaming chunks.
            if event.type == "response.output_text.delta":
                if first_token_time is None:
                    first_token_time = time.perf_counter()
                delta = event.delta
                print(delta, end="", flush=True)
                full_text_chunks.append(delta)

            elif event.type == "response.error":
                # If any error event is emitted by the stream, we show it.
                print(f"\n[ERROR] {event.error}", file=sys.stderr)
                log_line(log_file, "error", str(event.error))

        # After the stream finishes, compute latencies
        end_time = time.perf_counter()
        total_latency = end_time - start_time
        first_token_latency = (
            first_token_time - start_time if first_token_time is not None else None
        )

        print()  # final newline after streaming

        # Print a small, subtle latency summary
        if first_token_latency is not None:
            latency_info = (
                f"(first token: {first_token_latency:.3f}s · "
                f"total: {total_latency:.3f}s)"
            )
        else:
            latency_info = f"(total: {total_latency:.3f}s)"

        print(colorize(f"  {latency_info}", GREY, args.use_colors))

        full_text = "".join(full_text_chunks)
        log_line(log_file, "assistant", full_text)
        log_line(log_file, "info", latency_info)

        return full_text

    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        log_line(log_file, "error", f"{type(e).__name__}: {e}")
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# Command handling and main loop
# ─────────────────────────────────────────────────────────────────────────────

def print_help(args) -> None:
    """Print a short inline help message."""
    print("Available commands:")
    print("  /help   - Show this help message")
    print("  /config - Show current configuration")
    print("  /exit   - Exit the streaming chat client")
    print()
    print("Notes:")
    print("  - This client is stateless: each message is sent independently.")
    print("  - Responses are streamed token-by-token from the OpenAI API.")
    print("  - Use Ctrl+C or Ctrl+D to terminate the session if needed.")


def print_config(args) -> None:
    """Print current runtime configuration."""
    print("\n--- Current Configuration ---")
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"top_p: {args.top_p}")
    print(f"Max output tokens: {args.max_output_tokens}")
    print(f"System prompt: {args.system}")
    print(f"Colors enabled: {args.use_colors}")
    print("--- End of config ---\n")


def handle_command(cmd: str, args) -> bool:
    """
    Handle internal slash commands.
    Returns True if the command was handled and the main loop should continue.
    """
    cmd_clean = cmd.strip().lower()

    if cmd_clean == "/help":
        print_help(args)
        return True

    if cmd_clean == "/config":
        print_config(args)
        return True

    if cmd_clean == "/exit":
        print("Goodbye!")
        sys.exit(0)

    print(f"Unknown command: {cmd_clean}. Try /help.")
    return True  # command line was handled (no API call)


def main():
    """Entry point for the CLI application."""
    # Basic API key presence check
    if not os.getenv("OPENAI_API_KEY"):
        print(
            "ERROR: OPENAI_API_KEY is not set. "
            "Please configure your environment (e.g. in a .env file)."
        )
        sys.exit(1)

    args = parse_args()
    print_header(args)

    log_file = init_log_file(args)
    log_line(log_file, "info", "Session started")

    user_label = colorize("You", YELLOW, args.use_colors)

    while True:
        try:
            user_input = input(f"{user_label}: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting streaming chat. Goodbye!")
            log_line(log_file, "info", "EOF/KeyboardInterrupt - exiting")
            break

        stripped = user_input.strip()

        if not stripped:
            print("Empty input. Type a message or '/exit'.")
            continue

        if stripped.startswith("/"):
            handled = handle_command(stripped, args)
            if handled:
                log_line(log_file, "command", stripped)
                continue

        # Stateless request: no conversation history, just this message
        log_line(log_file, "user", stripped)
        stream_chat_once(stripped, args, log_file)

    if log_file is not None:
        log_line(log_file, "info", "Session closed")
        log_file.close()


if __name__ == "__main__":
    main()
