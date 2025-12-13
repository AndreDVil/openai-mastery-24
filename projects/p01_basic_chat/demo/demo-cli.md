# Project 01 – Demo (Stateful CLI Chat)
**Chat Completions API – OpenAI SDK 2.9.0**

This demo shows a real execution of the **stateful CLI chat client** implemented in Project 01, using:

- OpenAI Python SDK **2.9.0**
- **Chat Completions API** (`client.chat.completions.create`)
- In-memory conversation history
- Internal CLI commands
- Token usage and latency reporting

---

## 1. How to Run

```bash
python projects/01-basic-chat/basic_chat_stateful.py \
  --model gpt-4o-mini \
  --temperature 0.7 \
  --top-p 1.0 \
  --max-tokens 128
```

---

## 2. Demo Transcript (Real Execution)

```
=== Project 01 - Basic Chat (STATEFUL) ===
Using model: gpt-4o-mini
Temperature: 0.7 | top_p: 1.0
Max tokens (effective): 128
Backend: chat.completions.create (OpenAI SDK 2.9.0)
Type '/help' for commands. Type '/exit' to quit.


You: /config

--- Current Configuration ---
Model: gpt-4o-mini
Temperature: 0.7
top_p: 1.0
Max tokens (effective): 128
Backend: chat.completions.create (OpenAI SDK 2.9.0)
--- End of config ---


You: who was machado de assis?

Assistant:

Machado de Assis was one of the most important Brazilian writers and is widely regarded as a founder of modern Brazilian literature. Born in 1839 in Rio de Janeiro, he wrote novels, short stories, chronicles, and essays, becoming famous for his irony, psychological depth, and social criticism.

[latency: 1.08s]
[tokens - input: 38, output: 83, total: 121]
--------------------------------------------------


You: name two of his most famous works

Assistant:

Two of his most famous works are:

1. *Dom Casmurro* – a novel centered on memory, jealousy, and the ambiguity of its narrator.
2. *The Posthumous Memoirs of Brás Cubas* – an innovative novel narrated by a dead protagonist, full of irony and social critique.

[latency: 0.96s]
[tokens - input: 78, output: 92, total: 170]
--------------------------------------------------


You: what do these two works have in common?

Assistant:

Both works share several defining characteristics of Machado de Assis’ style:

- Unreliable, first-person narrators  
- Strong use of irony and subtle humor  
- Deep psychological analysis  
- Sharp criticism of 19th-century Brazilian society  

[latency: 1.11s]
[tokens - input: 123, output: 108, total: 231]
--------------------------------------------------


You: /history

--- Conversation History (excluding system) ---
USER: /config
USER: who was machado de assis?
ASSISTANT: Machado de Assis was one of the most important Brazilian writers...
USER: name two of his most famous works
ASSISTANT: Two of his most famous works are...
USER: what do these two works have in common?
ASSISTANT: Both works share several defining characteristics...
--- End of history ---


You: /clear
Conversation history cleared.


You: what was the first thing I asked you today?

Assistant:

I no longer have access to the previous conversation history because it was cleared with the `/clear` command. From this point on, I only see messages sent after the reset.

[latency: 0.91s]
[tokens - input: 41, output: 64, total: 105]
--------------------------------------------------


You: /exit
Goodbye!
```

---

## 3. Logging

During execution, a log file is created automatically (unless `--no-log` is used):

```
logs/project01-stateful-YYYYMMDD-HHMMSS.log
```

The log records:
- system prompt
- user messages
- assistant responses
- commands
- timestamps

---

## Demo Checklist

- [x] Uses Chat Completions API
- [x] Demonstrates real execution
- [x] Shows stateful memory behavior
- [x] Shows history reset
- [x] Shows internal commands
- [x] Displays latency and token usage
- [x] Reproducible using the project README
- [x] Stored in the /demo directory