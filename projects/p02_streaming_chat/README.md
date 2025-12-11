# Project 02 — Streaming Chat Client  
openai-mastery-24

## 1. Overview
This project implements a stateless streaming chat client using the OpenAI Responses API with `stream=True`.  
It displays assistant responses token-by-token, providing a real-time experience similar to interactive web chat interfaces.

This project builds upon the architecture of Project 01 but focuses entirely on:

- streaming UX  
- incremental rendering  
- token-level events  
- latency measurement  
- clean CLI ergonomics  

The client runs in the terminal and accepts several configuration parameters.

---

## 2. Objectives
- Implement a fully functioning streaming client using OpenAI's Responses API  
- Process token-level delta events in real time  
- Build a professional terminal UX for streamed responses  
- Maintain a stateless architecture  
- Add minimal logging for observability  

---

## 3. OpenAI Features Explored
- Responses API in streaming mode  
- `response.output_text.delta` events  
- Error events (`response.error`)  
- Optional system-level prompt injection (`--system`)  
- First-token latency measurement  
- Total latency measurement  

---

## 4. Architecture

### 4.1 High-Level Flow
User input → Build request payload → Send request with `stream=True`  
           → Receive delta events → Print chunks incrementally  
           → Compute latency → Log session data  

### 4.2 File Structure
streaming_chat.py  
  - parse_args()  
  - print_header()  
  - init_log_file()  
  - build_input_messages()  
  - stream_chat_once()  
  - handle_command()  
  - main()  

### 4.3 Request Format
Each request is stateless:

[
  { "role": "system", "content": "<optional system prompt>" },
  { "role": "user",   "content": "<user message>" }
]

### 4.4 Event Processing
Core events processed:

- response.output_text.delta → streamed text  
- response.error → error during generation  

---

## 5. How to Run

### Install dependencies
pip install openai python-dotenv

### Environment variable
OPENAI_API_KEY="your_key"

### Run
python projects/p02_streaming_chat/streaming_chat.py

### Useful flags
--model gpt-4o-mini  
--temperature 0.7  
--top_p 1.0  
--max-output-tokens 256  
--system "You are a concise assistant."  
--no-color  

### Example
python streaming_chat.py --model gpt-4o-mini --system "Respond in Portuguese."

---

## 6. Results & Examples

Example streaming output (simplified):

You: Explique o que é streaming.

Assistant (streaming...):

Streaming é um modo de resposta no qual o modelo envia pequenos fragmentos de texto conforme eles são gerados, oferecendo uma experiência mais rápida e fluida.

  (first token: 0.412s · total: 1.983s)

---

## 7. Skills Developed
- Real-time streaming processing  
- Token-level event handling  
- CLI engineering for interactive AI tools  
- Stateless request patterns  
- Latency instrumentation  
- Logging design for minimal overhead  

---

## 8. Future Improvements
- Stateful streaming mode  
- Pause/resume streaming  
- Real-time token counters  
- JSON-mode streaming  
- Dark/light UI themes  
- Export conversation to file  
- Integration with telemetry modules  

---

End of README.

