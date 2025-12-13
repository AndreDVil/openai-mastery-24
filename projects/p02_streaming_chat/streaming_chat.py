#!/usr/bin/env python3
"""
Project 02 - Streaming Chat Client (Stateless)
openai-mastery-24

This client implements streaming responses using:
- OpenAI Python SDK 2.9.0
- Chat Completions API
- stream=True

The design is stateless: each user input is sent as a fresh request.
"""

import argparse
import os
import sys
import time
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI


# ─────────────────────────────────────────────────────────────
# Environment & client
# ─────────────────────────────────────────────────────────────

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY not set.")
    sys.exit(1)

client = OpenAI()

LOG_DIR = "logs"

# ANSI colors
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREY = "\033[90m"
RESET = "\033[0m"


# ─────────────────────────────────────────────────────────────
# Logging (minimal)
# ─────────────────────────────────────────────────────────────

def init_log_file(args):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = os.path.join(LOG_DIR, f"project02-streaming-{ts}.log")
        f = open(path, "a", encoding="utf-8")

        f.write("# Project 02 - Streaming Chat Client\n")
        f.write(f"# Started: {datetime.now().isoformat(timespec='seconds')}\n")
        f.write(f"# Model: {args.model}\n")
        f.write("# -----------------------------------\n\n")
        f.flush()
        return f
    except Exception:
        return None


def log_line(log_file, label, content):
    if not log_file:
        return
    ts = datetime.now().isoformat(timespec="seconds")
    log_file.write(f"[{ts}] {label.upper()}: {content}\n")
    log_file.flush()


# ─────────────────────────────────────────────────────────────
# CLI config
# ─────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Project 02 - Streaming Chat Client (Chat Completions)"
    )

    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top_p", type=float, default=1.0)
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--system", type=str, default=None)
    parser.add_argument("--no-color", action="store_true")

    args = parser.parse_args()
    args.use_colors = not args.no_color
    return args


def c(text, color, enabled):
    if not enabled:
        return text
    return f"{color}{text}{RESET}"


def print_header(args):
    line = "─" * 60
    print(line)
    print("Project 02 · Streaming Chat Client (stateless)")
    print(line)
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature} · top_p: {args.top_p}")
    print(f"Max tokens: {args.max_tokens}")
    if args.system:
        print(f"System: {args.system}")
    else:
        print("System: (none)")
    print("Commands: /help · /config · /exit")
    print()


# ─────────────────────────────────────────────────────────────
# Core logic
# ─────────────────────────────────────────────────────────────

def build_messages(user_input, args):
    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": user_input})
    return messages


def stream_chat_once(user_input, args, log_file):
    messages = build_messages(user_input, args)

    t0 = time.perf_counter()
    first_token_time = None
    chunks = []

    try:
        stream = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=args.max_tokens,
            stream=True,
        )

        print(f"\n{c('Assistant', CYAN, args.use_colors)} (streaming...)\n")

        for chunk in stream:
            choice = chunk.choices[0]
            delta = getattr(choice.delta, "content", None)

            if delta:
                if first_token_time is None:
                    first_token_time = time.perf_counter()
                print(delta, end="", flush=True)
                chunks.append(delta)

        print()

        t1 = time.perf_counter()
        total_latency = t1 - t0
        ft_latency = (
            first_token_time - t0 if first_token_time else None
        )

        if ft_latency:
            latency = f"(first token: {ft_latency:.3f}s · total: {total_latency:.3f}s)"
        else:
            latency = f"(total: {total_latency:.3f}s)"

        print(c(f"  {latency}", GREY, args.use_colors))

        text = "".join(chunks)
        log_line(log_file, "assistant", text)
        log_line(log_file, "latency", latency)

    except Exception as e:
        print(f"\n[ERROR] {e}")
        log_line(log_file, "error", str(e))


# ─────────────────────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────────────────────

def print_help():
    print("Commands:")
    print("  /help   Show this help")
    print("  /config Show current configuration")
    print("  /exit   Exit the client")


def print_config(args):
    print("\n--- Configuration ---")
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"top_p: {args.top_p}")
    print(f"Max tokens: {args.max_tokens}")
    print(f"System: {args.system}")
    print(f"Colors: {args.use_colors}")
    print("---------------------\n")


def handle_command(cmd, args):
    cmd = cmd.lower().strip()
    if cmd == "/help":
        print_help()
        return True
    if cmd == "/config":
        print_config(args)
        return True
    if cmd == "/exit":
        print("Goodbye!")
        sys.exit(0)
    print("Unknown command. Try /help.")
    return True


# ─────────────────────────────────────────────────────────────
# Main loop
# ─────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    print_header(args)

    log_file = init_log_file(args)
    log_line(log_file, "info", "session started")

    user_label = c("You", YELLOW, args.use_colors)

    while True:
        try:
            user_input = input(f"{user_label}: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not user_input.strip():
            print("Empty input. Type a message or /exit.")
            continue

        if user_input.startswith("/"):
            handled = handle_command(user_input, args)
            if handled:
                continue

        log_line(log_file, "user", user_input)
        stream_chat_once(user_input, args, log_file)

    log_line(log_file, "info", "session closed")
    if log_file:
        log_file.close()


if __name__ == "__main__":
    main()
