DEMO — Project 02 · Streaming Chat Client (Chat Completions, stateless)

============================================================
Command Used
============================================================

python projects/02-streaming-chat/streaming_chat.py \
  --model gpt-4o-mini \
  --temperature 0.7 \
  --top_p 1.0 \
  --max-tokens 256 \
  --system "You are a helpful assistant. Answer concisely."

============================================================
Session Transcript (simplified)
============================================================

[Startup]
Project 02 · Streaming Chat Client (stateless)
Model: gpt-4o-mini
Commands: /help · /config · /exit

[Question 1]
You: What is streaming in LLM APIs?

Assistant (streaming...):
Streaming returns partial text as it is generated, allowing incremental rendering and lower perceived latency.

(first token: 0.412s · total: 1.883s)

[Command]
You: /config
Model: gpt-4o-mini
temperature: 0.7
top_p: 1.0
max-tokens: 256

[Empty Input]
You:
Empty input. Type a message or '/exit'.

[Exit]
You: /exit
Goodbye!

============================================================
Notes
============================================================
- Stateless: each message is independent.
- Streaming delta extraction: chunk.choices[0].delta.content
- Completion: finish_reason or stream end.
