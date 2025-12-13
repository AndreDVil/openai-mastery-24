# Project 02 — Streaming Chat Client (Chat Completions)
openai-mastery-24

## 1. Overview
This project implements a **stateless streaming chat CLI** using the **OpenAI Python SDK 2.9.0** and the **Chat Completions API**:

- `client.chat.completions.create(..., stream=True)`
- incremental token rendering in the terminal

The focus is on event-driven streaming output, improved perceived latency, and clean CLI UX.

---

## 2. Objectives
- Implement **token-by-token** streaming output in a terminal client.
- Measure **first-token latency** and **total latency**.
- Keep the client **stateless**: each user message is an independent request.
- Follow Project 01 engineering standards (CLI structure, commands, logging, docs).

---

## 3. OpenAI Features Explored
- Chat Completions API via `client.chat.completions.create`
- Streaming responses via `stream=True`
- Delta handling:
  - `chunk.choices[0].delta.content`
- Finish handling:
  - `chunk.choices[0].finish_reason`

---

## 4. Architecture

### 4.1 High-level flow
User input → build messages[] → Chat Completions (stream=True)  
→ iterate chunks → print `delta.content` as it arrives  
→ compute latencies → optionally log output

### 4.2 Stateless message payload
Each request uses a fresh messages array:

- optional system message
- single user message

Example:
[
  { "role": "system", "content": "<optional system prompt>" },
  { "role": "user",   "content": "<your message>" }
]

### 4.3 Core streaming loop (conceptual)
- Start timer
- Call `client.chat.completions.create(..., stream=True)`
- For each streamed chunk:
  - read `choices[0].delta.content`
  - print immediately and accumulate
- Compute first-token and total latency

---

## 5. How to Run

### Install dependencies
pip install openai==2.9.0 python-dotenv

### Configure environment
Set:
OPENAI_API_KEY="your_key"

### Run
python projects/02-streaming-chat/streaming_chat.py --model gpt-4o-mini

### Common flags
--model gpt-4o-mini
--temperature 0.7
--top_p 1.0
--max-tokens 256
--system "You are a helpful assistant."
--no-color

---

## 6. Results & Examples

Example (simplified):

You: Explain streaming in one paragraph.

Assistant (streaming...):
Streaming means the model sends partial text as it is generated, allowing the UI to render output incrementally.

(first token: 0.410s · total: 1.920s)

---

## 7. Skills Developed
- Implementing streaming with `stream=True` in Chat Completions
- Delta event processing (`choices[].delta.content`)
- Latency instrumentation (first-token vs total)
- Stateless request design
- CLI UX improvements for streamed output
- Minimal logging for observability

---

## 8. Future Improvements
- Optional stateful mode (`--stateful`)
- Include usage telemetry (if supported in the chosen SDK/model)
- Improved formatting and line wrapping
- Export transcripts to demo artifacts automatically

End of README.
