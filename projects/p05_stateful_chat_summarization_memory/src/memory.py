# src/memory.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal, Tuple

from openai import OpenAI

from prompts import SUMMARIZER_SYSTEM_PROMPT


Role = Literal["system", "user", "assistant"]
Message = Dict[str, str]


@dataclass(frozen=True)
class MemoryPolicy:
    # Contract Spec (v2.1)
    k_verbatim: int = 6
    b_buffer: int = 4
    token_budget_ratio: float = 0.70
    safety_user_turns: int = 10

    @property
    def max_recent(self) -> int:
        return self.k_verbatim + self.b_buffer


@dataclass
class ChatState:
    memory_summary: str = ""
    recent_messages: List[Message] = field(default_factory=list)
    user_turn_count: int = 0  # counts ONLY user messages seen by the system


@dataclass(frozen=True)
class TriggerResult:
    triggered: bool
    reason: Optional[str] = None  # "token" | "overflow" | "safety"
    details: Optional[str] = None

def _debug_print_summarization(
    *,
    reason: str,
    details: str | None,
    messages_to_summarize: list[Message],
    before_summary: str,
    after_summary: str,
    ) -> None:
    print("\n========== SUMMARIZATION DEBUG ==========")
    print(f"reason: {reason}")
    if details:
        print(f"details: {details}")

    print("\n--- MESSAGES FOLDED INTO MEMORY ---")
    print(format_messages_for_summarizer(messages_to_summarize) or "(none)")

    print("\n--- MEMORY BEFORE ---")
    print(before_summary.strip() or "(empty)")

    print("\n--- MEMORY AFTER ---")
    print(after_summary.strip() or "(empty)")

    print("========================================\n")



def _count_user_turns_in_messages(messages: List[Message]) -> int:
    return sum(1 for m in messages if m.get("role") == "user")


def check_overflow_trigger(state: ChatState, policy: MemoryPolicy) -> TriggerResult:
    if len(state.recent_messages) > policy.max_recent:
        return TriggerResult(True, reason="overflow", details=f"len(recent_messages)={len(state.recent_messages)} > {policy.max_recent}")
    return TriggerResult(False)


def check_safety_trigger(state: ChatState, policy: MemoryPolicy) -> TriggerResult:
    # Fires every N user turns
    if policy.safety_user_turns <= 0:
        return TriggerResult(False)
    if state.user_turn_count > 0 and (state.user_turn_count % policy.safety_user_turns == 0):
        return TriggerResult(True, reason="safety", details=f"user_turn_count={state.user_turn_count} hits {policy.safety_user_turns}")
    return TriggerResult(False)


def estimate_token_trigger_stub(*, enabled: bool = False) -> TriggerResult:
    """
    Token trigger is intentionally a stub in the minimal version.
    In the next step we will add token estimation (e.g., via a tokenizer or simple heuristic).
    """
    if enabled:
        # Placeholder: never true in minimal version unless you force it.
        return TriggerResult(False)
    return TriggerResult(False)


def choose_trigger(
    *,
    token_tr: TriggerResult,
    overflow_tr: TriggerResult,
    safety_tr: TriggerResult,
) -> TriggerResult:
    """
    Contract Spec v2.1 priority:
    1) token
    2) overflow
    3) safety
    """
    if token_tr.triggered:
        return token_tr
    if overflow_tr.triggered:
        return overflow_tr
    if safety_tr.triggered:
        return safety_tr
    return TriggerResult(False)


def build_chat_context(system_prompt: str, state: ChatState) -> List[Message]:
    """
    Context Construction Contract:
      1) system prompt
      2) memory_summary (if any)
      3) recent_messages (<= K+B)
    """
    messages: List[Message] = [{"role": "system", "content": system_prompt}]

    if state.memory_summary.strip():
        # Put memory as a system message to make it authoritative.
        messages.append({"role": "system", "content": f"MEMORY SUMMARY:\n{state.memory_summary}"})

    messages.extend(state.recent_messages)
    return messages


def _select_overflow_messages(state: ChatState, policy: MemoryPolicy) -> Tuple[List[Message], List[Message]]:
    """
    Returns (overflow_messages, kept_messages).

    Overflow = oldest messages beyond max_recent.
    Kept = remaining newest messages (still may exceed K until we truncate after summarization).
    """
    excess = len(state.recent_messages) - policy.max_recent
    if excess <= 0:
        return [], state.recent_messages

    overflow = state.recent_messages[:excess]
    kept = state.recent_messages[excess:]
    return overflow, kept


def _truncate_to_k(messages: List[Message], policy: MemoryPolicy) -> List[Message]:
    """Keep only the most recent K messages."""
    if len(messages) <= policy.k_verbatim:
        return messages
    return messages[-policy.k_verbatim:]


def summarize_memory(
    *,
    client: OpenAI,
    model: str,
    current_memory_summary: str,
    messages_to_summarize: List[Message],
) -> str:
    """
    Summarization Function Contract:
    - rewrite full memory_summary
    - no transcripts
    - no invention
    Output: updated memory summary only
    """
    # We pass both the existing summary and the messages to fold.
    # We do NOT ask for JSON mode here; keep it plain text and strict formatting.
    summarizer_input = [
        {"role": "system", "content": SUMMARIZER_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "EXISTING MEMORY SUMMARY (may be empty):\n"
                f"{current_memory_summary.strip()}\n\n"
                "MESSAGES TO FOLD INTO MEMORY:\n"
                f"{format_messages_for_summarizer(messages_to_summarize)}\n\n"
                "Produce the updated memory summary only."
            ),
        },
    ]

    resp = client.chat.completions.create(
        model=model,
        messages=summarizer_input,
        temperature=0.2,
    )
    text = (resp.choices[0].message.content or "").strip()
    return text


def format_messages_for_summarizer(messages: List[Message]) -> str:
    """
    Lightweight formatting. Not a transcript requirement; it's input to summarizer only.
    Keep it minimal and readable.
    """
    lines = []
    for m in messages:
        role = m.get("role", "unknown")
        content = m.get("content", "")
        lines.append(f"- {role.upper()}: {content}")
    return "\n".join(lines)


def apply_summarization_if_needed(
    *,
    client: OpenAI,
    model: str,
    system_prompt: str,
    state: ChatState,
    policy: MemoryPolicy,
    enable_token_trigger: bool = False,
    debug: bool = False,
) -> TriggerResult:
    """
    Checks triggers and applies at most one summarization per cycle (v2.1).
    Mutates state in place.
    """
    token_tr = estimate_token_trigger_stub(enabled=enable_token_trigger)
    overflow_tr = check_overflow_trigger(state, policy)
    safety_tr = check_safety_trigger(state, policy)

    chosen = choose_trigger(token_tr=token_tr, overflow_tr=overflow_tr, safety_tr=safety_tr)
    if not chosen.triggered:
        return chosen

    # Decide what messages to summarize depending on reason.
    if chosen.reason == "overflow":
        overflow, kept = _select_overflow_messages(state, policy)

        # kept has at most K+B messages.
        # If we are going to truncate kept down to K, we MUST fold the dropped part too.
        if len(kept) > policy.k_verbatim:
            drop_set = kept[:-policy.k_verbatim]   # these would be lost otherwise (typically size B)
            keep_final = kept[-policy.k_verbatim:] # last K messages
        else:
            drop_set = []
            keep_final = kept

        messages_to_fold = overflow + drop_set

        before = state.memory_summary
        if messages_to_fold:
            updated = summarize_memory(
                client=client,
                model=model,
                current_memory_summary=before,
                messages_to_summarize=messages_to_fold,
            )
        else:
            updated = before

        state.memory_summary = updated
        state.recent_messages = keep_final

        if debug:
            _debug_print_summarization(
                reason=chosen.reason,
                details=chosen.details,
                messages_to_summarize=messages_to_fold,
                before_summary=before,
                after_summary=updated,
            )

    elif chosen.reason == "safety":
        if len(state.recent_messages) > policy.k_verbatim:
            to_fold = state.recent_messages[:-policy.k_verbatim]
            kept = state.recent_messages[-policy.k_verbatim:]
        else:
            to_fold = []
            kept = state.recent_messages

        if to_fold:
            before = state.memory_summary
            updated = summarize_memory(
                client=client,
                model=model,
                current_memory_summary=before,
                messages_to_summarize=to_fold,
            )
            state.memory_summary = updated
            state.recent_messages = kept

            if debug:
                _debug_print_summarization(
                    reason=chosen.reason,
                    details=chosen.details,
                    messages_to_summarize=to_fold,
                    before_summary=before,
                    after_summary=updated,
                )


    elif chosen.reason == "token":
        # Token trigger is stubbed for now; keep placeholder behavior.
        # Later we will implement a strategy to fold the oldest chunk until under budget.
        pass

    return chosen
