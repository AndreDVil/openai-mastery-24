# Project 01 – Basic Chat (CLI)
**Stateless and Stateful Chat Client using OpenAI SDK 2.9.0**

---

## 1. Overview

Project 01 is the first fully functional application in the **openai-mastery-24** journey.

The goal of this project is to build a **professional-grade CLI chat client** using the **OpenAI Python SDK 2.9.0**, strictly following the **Chat Completions API** pattern:

- `client.chat.completions.create`
- Explicit `messages` structure (`role`, `content`)
- No usage of the Responses API

Two versions are implemented:

- **Stateless CLI chat**  
- **Stateful CLI chat with memory, commands, and logging**

This project establishes the technical and architectural foundation for all subsequent projects.

---

## 2. Objectives

### Technical Objectives
- [x] Use OpenAI SDK 2.9.0 unified client
- [x] Use `chat.completions.create` exclusively
- [x] Implement a stateless CLI chat loop
- [x] Implement a stateful CLI chat with conversation memory
- [x] Support model selection via CLI
- [x] Support sampling controls (`temperature`, `top_p`)
- [x] Support output token limits
- [x] Display latency per request
- [x] Display token usage (prompt / completion / total)
- [x] Add internal slash commands
- [x] Add optional logging to disk
- [x] Follow clean CLI engineering practices

### Learning Objectives
- [x] Understand the Chat Completions mental model
- [x] Master the `messages` schema (`role`, `content`)
- [x] Understand stateless vs stateful conversations
- [x] Learn how memory is simulated by resending context
- [x] Build reusable CLI architecture for LLM apps

---

## 3. OpenAI Features Explored

| Feature | Status |
|------|------|
| Chat Completions API | ✅ |
| `messages` schema | ✅ |
| System / User / Assistant roles | ✅ |
| Sampling (`temperature`, `top_p`) | ✅ |
| Token usage | ✅ |
| Latency measurement | ✅ |
| Conversation memory (manual) | ✅ |
| Streaming | ❌ (Project 02) |
| JSON Mode | ❌ (Project 03) |
| Tool calling | ❌ (Later projects) |
| Multimodal input | ❌ (Later projects) |

---

## 4. Architecture

### Stateless Version (`basic_chat.py`)
- Sends one user message per request
- No conversation history is preserved
- Each request is independent

### Stateful Version (`basic_chat_stateful.py`)
- Maintains an in-memory `messages` list
- Sends full conversation history on each request
- Supports internal commands
- Logs the session to disk (optional)

### Data Flow
```
User input → CLI → messages[] → OpenAI Chat Completions API → Assistant output
```

---

## 5. How to Run

### Install dependencies
```bash
pip install openai python-dotenv
```

### Set environment variable
Create a `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
```

### Run stateless client
```bash
python projects/01-basic-chat/basic_chat.py
```

### Run stateful client
```bash
python projects/01-basic-chat/basic_chat_stateful.py
```

### Optional CLI arguments
```bash
--model gpt-4o-mini
--temperature 0.7
--top-p 1.0
--max-tokens 128
--no-log
```

---

## 6. Stateful Commands

Available only in the stateful version:

| Command | Description |
|------|------|
| `/help` | Show available commands |
| `/history` | Print conversation history |
| `/clear` | Clear memory (keeps system prompt) |
| `/config` | Show runtime configuration |
| `/exit` | Exit the application |

---

## 7. Logging

When enabled, logs are written to:

```
logs/project01-stateful-YYYYMMDD-HHMMSS.log
```

Logged information includes:
- system prompt
- user messages
- assistant responses
- commands
- timestamps

The `logs/` directory is excluded via `.gitignore`.

---

## 8. Demo

A full CLI demo transcript is available at:

```
projects/01-basic-chat/demo/demo-cli.md
```

The demo shows:
- multi-turn stateful conversation
- memory behavior
- internal commands
- latency and token usage
- log file example

---

## 9. Skills Developed

### OpenAI API
- Chat Completions API (SDK 2.9.0)
- Message-based prompting
- Token accounting
- Sampling control

### Python & Engineering
- CLI design with argparse
- Stateful vs stateless architecture
- Memory management
- Logging
- Clean control flow
- Professional repository structure

### Conceptual
- LLM context handling
- Cost vs latency trade-offs
- Foundations for agents and RAG

---

## 10. Future Improvements

- Streaming responses (Project 02)
- JSON-structured outputs (Project 03)
- Tool calling and function execution
- Multimodal input
- Long-term memory strategies

---

**Project 01 establishes the canonical CLI + Chat Completions pattern  
used throughout the rest of the openai-mastery-24 track.**
