# src/main.py

from openai import OpenAI

from memory import ChatState, MemoryPolicy, build_chat_context, apply_summarization_if_needed

CHAT_SYSTEM_PROMPT = """\
You are a helpful assistant.

You may receive a MEMORY SUMMARY that represents durable state from earlier conversation.
You may also receive recent verbatim messages.

RULES FOR USING MEMORY
- Treat MEMORY SUMMARY as the durable state. Recent messages are the most up-to-date local context.
- When the user asks about past context, preferences, plans, or "what I said" (recall questions),
  you MUST consult BOTH the MEMORY SUMMARY and the recent messages.
- If recent messages and MEMORY SUMMARY differ, you MUST mention both:
  - what is true recently, and
  - what was true earlier per memory,
  and explain the difference briefly (e.g., "Recently X, earlier we also discussed Y.").
- Do not ignore MEMORY SUMMARY in recall questions.

Keep responses concise and clear.
"""


CHAT_MODEL = "gpt-4.1-mini"  # pick your model
SUMMARIZER_MODEL = "gpt-4.1-mini"  # can be same or cheaper


def main() -> None:
    client = OpenAI()

    policy = MemoryPolicy(k_verbatim=6, b_buffer=4, safety_user_turns=10)
    state = ChatState()

    print("Project 05 — Stateful Chat with Summarization Memory (minimal)")
    print("Type 'exit' to quit.\n")

    while True:
        user_text = input("you> ").strip()

        if user_text.lower() == "/memory":
            print("----- MEMORY SUMMARY (current state) -----")
            print(state.memory_summary or "(empty)")
            print("------------------------------------------\n")
            continue
        
        if user_text.lower() in {"exit", "quit"}:
            break

        # Update user turn count (user turns only)
        state.user_turn_count += 1

        # Before adding the new user message to recent_messages,
        # apply summarization triggers based on current state (v2.1).
        trig = apply_summarization_if_needed(
            client=client,
            model=SUMMARIZER_MODEL,
            system_prompt=CHAT_SYSTEM_PROMPT,
            state=state,
            policy=policy,
            enable_token_trigger=False,  # stubbed for now
            debug=True
        )

        # Add new user message to recent buffer
        state.recent_messages.append({"role": "user", "content": user_text})

        # Build chat context and call chat completion
        messages = build_chat_context(CHAT_SYSTEM_PROMPT, state)

        resp = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=0.7,
        )
        assistant_text = (resp.choices[0].message.content or "").strip()
        print(f"assistant> {assistant_text}\n")

        # Append assistant response to recent buffer
        state.recent_messages.append({"role": "assistant", "content": assistant_text})

        # OPTIONAL: show trigger info for learning/debug
        if trig.triggered:
            print(f"[summarization triggered] reason={trig.reason} details={trig.details}\n")


if __name__ == "__main__":
    main()
