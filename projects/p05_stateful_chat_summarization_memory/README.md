Project 05 — Stateful Chat with Summarization Memory

Overview
--------

This project explores how to build a stateful conversational system that maintains
long-running interactions without unbounded context growth.

Instead of treating conversation history as raw context, the system introduces
summarization-based memory, where past interactions are deliberately rewritten
into a compact, durable state.

The project emphasizes explicit memory governance, debuggability, and cost-aware design.


Objectives
----------

- Distinguish clearly between context window, history, and memory
- Treat memory as explicit state, not accumulated logs
- Implement summarization-based context compression
- Control when and how memory is updated
- Prevent silent loss of information
- Observe and reason about system behavior over long conversations


OpenAI Features Used
-------------------

- Chat Completions API
- Separate model calls for:
  - chat interaction
  - memory summarization
- Temperature control for deterministic summarization

SDK version: openai==2.9.0  
Client pattern: client = OpenAI()  
Endpoint used: client.chat.completions.create


Architecture
------------

Core State:
- memory_summary: compact textual representation of durable conversational state
- recent_messages: verbatim message buffer for local coherence
- user_turn_count: counter for safety-based summarization triggers

Memory Policy:
- K (verbatim window): 6 messages
- B (buffer overflow): 4 messages
- Maximum buffer size: 10 messages
- Summarization triggers:
  - buffered overflow
  - safety trigger (every 10 user turns)
  - token trigger (stubbed for learning purposes)

Key Principle:
Memory is rewritten, not appended.
Raw messages are disposable; state is durable.


Summarization Flow
------------------

1. Messages accumulate in recent_messages
2. When a trigger fires:
   - messages that would be dropped are folded into memory
   - memory is rewritten via a dedicated summarization call
3. Only the most recent K messages remain verbatim
4. Conversation continues using:
   - system prompt
   - memory summary
   - recent messages

Invariant:
No message may be dropped without first being summarized.


Debug & Observability
---------------------

A debug mode makes memory behavior transparent.

When summarization occurs, the system prints:
- messages folded into memory
- memory state before summarization
- memory state after summarization
- trigger reason


How to Run
----------

pip install openai==2.9.0
export OPENAI_API_KEY=your_key_here

cd project05
python -m src.main

Available commands:
- /memory   -> display current memory summary
- exit      -> quit the program


Results & Observations
----------------------

- Memory behaves as explicit state, not implicit model behavior
- Recency bias must be handled explicitly
- Summarization without validation may drift semantically
- The model does not govern state unless instructed
- Debug visibility is critical for trust


Skills Developed
----------------

- Stateful system design with LLMs
- Memory governance and invariants
- Summarization-based compression
- Trigger-based state transitions
- Debuggable AI system architecture


Limitations
-----------

- Memory stored as free-form text
- No schema validation of memory
- Token-based trigger not fully implemented
- No persistence across sessions

These limitations are intentional for educational clarity.


Next Steps
----------

- Introduce structured (JSON) memory with schema validation
- Implement real token estimation
- Add explicit recall modes
- Persist memory across runs
