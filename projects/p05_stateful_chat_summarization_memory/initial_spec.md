PROJECT 05 — Stateful Chat with Summarization Memory
Summarization & State Transition Contract (v2.2)

This document refines v2.1 by clarifying the buffered overflow behavior to
guarantee the "no-drop-without-fold" invariant when truncating from (K+B) to K.
Architecture remains unchanged.

----------------------------------------------------------------
1) Core Principle
----------------------------------------------------------------

- The memory summary IS the state.
- State is rewritten, not appended.
- Raw message history is not memory.
- Context is a temporary view derived from state + recent messages.

----------------------------------------------------------------
2) State Components
----------------------------------------------------------------

A) memory_summary: str
   - Compact, structured representation of durable conversational state.
   - Single source of truth.

B) recent_messages: list[Message]
   - Verbatim buffer for local coherence.
   - Contains both user and assistant messages.

C) policies (immutable at runtime):
   - K (verbatim window): 6 messages
   - B (buffer overflow): 4 messages
   - Max recent_messages length: K + B = 10 messages
   - Primary trigger: token budget (~70%)
   - Safety trigger: 10 user turns
   - Summary format: headings + bullets
   - Rewrite strategy: full rewrite (no append)

----------------------------------------------------------------
3) Important Distinction: Messages vs User Turns
----------------------------------------------------------------

- "Message count" refers to individual messages (user OR assistant).
- "User turn count" refers only to user messages.

Example:
- 10 messages ≈ 5 user turns (typical).
- 10 user turns ≈ ~20 messages.

Triggers based on these counters are NOT equivalent.

----------------------------------------------------------------
4) Context Construction Contract
----------------------------------------------------------------

For every chat completion request, the context MUST be built as:

1) System prompt
2) memory_summary (if non-empty)
3) recent_messages (verbatim, up to K + B)
4) New user message

Notes:
- memory_summary is always included once it exists.
- recent_messages MAY temporarily exceed K.
- recent_messages MUST NOT exceed K + B.

----------------------------------------------------------------
5) Buffered Overflow Policy (Anti-Gap Mechanism)
----------------------------------------------------------------

Goal:
Prevent loss of information without importance classification.

Rules:

- recent_messages may grow up to (K + B).
- Exceeding K alone does NOT trigger summarization.
- When recent_messages exceeds (K + B):

  a) Identify overflow_messages:
     - The oldest messages exceeding the allowed buffer.

  b) Identify drop_set (messages that would be discarded when truncating to K):
     - After removing overflow_messages, recent_messages will be at most (K + B).
     - If truncation to the most recent K messages is required, the messages being dropped
       MUST be included in summarization.

  c) Trigger summarization using:
     - current memory_summary
     - (overflow_messages + drop_set)

  d) Replace memory_summary with the updated summary.

  e) Drop (overflow_messages + drop_set) permanently.

  f) Keep only the most recent K messages in recent_messages.

Invariant (explicit):
- No message may be dropped without first being folded into memory_summary.

----------------------------------------------------------------
6) Summarization Triggers
----------------------------------------------------------------

Summarization is triggered if ANY of the following are true:

Primary Trigger (Hard Constraint):
- Estimated input tokens exceed ~70% of the target model budget.

Buffered Overflow Trigger (Structural Safety):
- recent_messages length exceeds (K + B).

Safety Trigger (Semantic Hygiene):
- Every 10 user turns, regardless of token usage.

Triggers operate on different dimensions and are not redundant.

----------------------------------------------------------------
7) Trigger Priority & Execution Rule
----------------------------------------------------------------

When multiple triggers are true at the same time:

Priority order:
1) Token budget trigger
2) Buffered overflow trigger
3) Safety trigger

Execution rules:
- Only ONE summarization is executed per cycle.
- The highest-priority active trigger is applied.
- After summarization, the system proceeds with chat completion.
- Optional re-checks may be performed in future versions,
  but are not required for correctness.

----------------------------------------------------------------
8) Summarization Function Contract
----------------------------------------------------------------

summarize_memory(
    current_memory_summary: str,
    messages_to_summarize: list[Message]
) -> updated_memory_summary: str

Responsibilities:
- Rewrite the entire memory summary.
- Deduplicate information.
- Resolve conflicts by preferring the most recent explicit decisions.
- Preserve only durable, action-guiding information.

Non-responsibilities:
- Do NOT generate chat replies.
- Do NOT include transcripts.
- Do NOT invent facts.
- Do NOT alter policies.

----------------------------------------------------------------
9) Summary Content Policy
----------------------------------------------------------------

memory_summary MAY contain:
- Facts / Constraints
- Goals / Preferences
- Decisions Made
- Open Items / Pending Commitments
- Key Artifacts / References

memory_summary MUST NOT contain:
- Verbatim dialogue
- Emotional tone or filler
- Ephemeral details
- Assistant opinions or reasoning traces

----------------------------------------------------------------
10) Invariants
----------------------------------------------------------------

- memory_summary is the only durable memory.
- recent_messages are disposable.
- No message is dropped without prior summarization.
- State size is bounded.
- Behavior is reproducible given the same state and inputs.

----------------------------------------------------------------
11) Design Intent
----------------------------------------------------------------

This architecture favors:
- explicit state
- debuggability
- cost predictability
- educational clarity

The safety trigger is not required for correctness,
but exists to enforce periodic semantic reconciliation.

----------------------------------------------------------------
End of Contract Spec (v2.2)
