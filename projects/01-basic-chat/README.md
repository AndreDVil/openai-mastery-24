# Project 01 – Basic Chat (CLI Chat Client)

## 1. Overview

This project delivers the first real OpenAI-powered application of the **openai-mastery-24** journey:  
a professional-grade **Command-Line Chat Client**, implemented in two versions:

- **`basic_chat.py`** → stateless chat loop  
- **`basic_chat_stateful.py`** → stateful chat with memory + internal commands + logging  

Both clients use the modern **OpenAI Responses API** and follow software engineering best practices:
argument parsing, structured logging, clear UX, and extensible architecture.

This project builds the foundation for more complex LLM applications later (agents, tools, RAG, streaming, assistants).

---

## 2. Objectives

### ✔ Technical Objectives
- [x] Build a fully functional stateless CLI chat client  
- [x] Add model selection via CLI arguments  
- [x] Implement sampling controls (`temperature`, `top_p`)  
- [x] Show per-response latency  
- [x] Show token usage  
- [x] Add output colorization for better UX  
- [x] Add *stateful* chat with full conversation history  
- [x] Add internal commands: `/help`, `/clear`, `/config`, `/history`, `/exit`  
- [x] Add conversation logging to timestamped files  
- [x] Enforce minimum `max_output_tokens`  
- [x] Provide professional-grade CLI structure using `argparse`

### ✔ Learning Objectives
- [x] Understand stateless vs. stateful chat patterns  
- [x] Learn the structure of OpenAI’s Responses API  
- [x] Build an interactive LLM application end-to-end  
- [x] Practice clean CLI UX and loop design  
- [x] Learn how to measure and interpret latency  
- [x] Understand cost implications of token usage and long history  
- [x] Establish a reusable boilerplate for Projects 02–24  

---

## 3. OpenAI Features Explored

| Feature | Status |
|--------|--------|
| Responses API (`client.responses.create`) | ✅ Used extensively |
| Latency measurement | ✅ Implemented |
| Token usage (`response.usage`) | ✅ Implemented |
| Model selection | ✅ via `--model` |
| Temperature | ✅ via `--temperature` |
| Top-p | ✅ via `--top_p` |
| Max output tokens | ✅ via `--max-tokens` |
| Stateful memory | ✅ in `basic_chat_stateful.py` |
| Commands (`/clear`, `/history`…) | ✅ Implemented |
| Logging | ✅ Implemented |
| Streaming responses | ❌ Planned for Project 02 |
| JSON mode | ❌ Not required in this project |
| Tool calling | ❌ Will appear in later projects |
| Realtime API | ❌ Out of scope here |

---

## 4. Architecture

### Stateless Version (`basic_chat.py`)
- Reads user input in a loop  
- Sends **only the latest** prompt to the model  
- Shows assistant output, latency, and token usage  

### Stateful Version (`basic_chat_stateful.py`)
- Maintains and sends **full conversation history** on every request  
- Supports internal commands:
  - `/help`
  - `/clear` (resets memory)
  - `/history`
  - `/config`
  - `/exit`
- Logs every action (system, user, assistant, commands) into timestamped files

### Data Flow (Stateful)
```
User → CLI → command handler? → (if not) history updated → OpenAI Responses API  
→ assistant output → console + log file
```

### External Dependencies
- `openai` SDK  
- `python-dotenv`  
- A valid `OPENAI_API_KEY` in `.env`

---

## 5. How to Run the Demo

### 1. Install dependencies
```bash
pip install openai python-dotenv
```

### 2. Create your `.env`
```bash
OPENAI_API_KEY=your_key_here
```

### 3. Run the **stateless** client
```bash
python projects/01-basic-chat/basic_chat.py
```

### 4. Run the **stateful** client
```bash
python projects/01-basic-chat/basic_chat_stateful.py
```

### Optional arguments
```
--model gpt-4o-mini
--temperature 0.7
--top_p 1.0
--max-tokens 128
```

Example:
```bash
python basic_chat_stateful.py --model gpt-4o --temperature 0.3 --max-tokens 64
```

---

## 6. Commands (Stateful Version Only)

| Command | Description |
|---------|-------------|
| `/help` | Shows all commands |
| `/clear` | Clears conversation history (keeps system prompt) |
| `/history` | Prints the full conversation so far |
| `/config` | Shows current model + sampling settings |
| `/exit` | Exits the program immediately |

---

## 7. Logging

All logs are stored under:

```
logs/project01-stateful-YYYYMMDD-HHMMSS.log
```

Each line includes a timestamp and message role:

```
[2025-12-10T17:34:32] USER: quem é machado de assis?
[2025-12-10T17:34:33] ASSISTANT: Machado de Assis foi...
[2025-12-10T17:34:40] COMMAND: /history
```

Logging provides:

- replayability  
- debugging  
- data for future fine-tuning  
- transparency for model behavior  
- useful audit trail for multi-turn interactions  

---

## 8. Results & Examples

### Example (Stateful)
```
=== Project 01 — Basic Chat (STATEFUL) ===
Using model: gpt-4o-mini
Temperature: 0.7 | top_p: 1.0
Max tokens (effective): model default
Type '/help' for commands.

You: quem é machado de assis?
Assistant:
Machado de Assis foi um escritor brasileiro...

[latency: 1.213s]
[tokens - input: 23, output: 42, total: 65]
--------------------------------------------------

You: cite duas obras dele
Assistant:
Duas obras famosas são "Dom Casmurro" e "Memórias Póstumas de Brás Cubas".
```

---

## 9. Skills Developed

### 🔹 OpenAI API Skills
- Using the **Responses API** in real applications  
- Working with `response.output_text` & `response.usage`  
- Managing history as a list of `{role, content}` objects  
- Structuring arguments for LLM sampling behavior  

### 🔹 Python Engineering Skills
- Building interactive CLI tools  
- Using `argparse` professionally  
- Implementing `while True` control flow with `break` and `continue`  
- Memory management in chat systems  
- Timestamps, files, logging design  
- Colorized terminal output  
- Handling user commands cleanly  

### 🔹 Conceptual Understanding
- Stateless vs. stateful LLM interactions  
- Why LLMs “remember” only if **we resend the history**  
- Latency & token cost implications  
- Clean software architecture for multi-project LLM repos  

---

## 10. Future Improvements

| Feature | Status |
|---------|--------|
| Add streaming responses | ⏳ Upcoming in Project 02 |
| Add JSON mode | To be explored in Project 03 |
| Add structured error handling | Planned |
| Add retries & rate-limit protection | Planned |
| Add global config file | Planned |
| Add async version | Possible |
| Add TTS output for audio chat | Future project |
| Add benchmarking tool | Future project |
| Add unit tests | Eventually |

---

**Project 01 now provides a complete, professional foundation for all next projects.**  
It demonstrates engineering discipline, OpenAI mastery, and practical application design—exactly the goal of the *openai-mastery-24* repository.
