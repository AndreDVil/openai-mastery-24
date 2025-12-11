# Project 01 – Skills Report  
**Basic Chat (Stateless & Stateful CLI Client)**  
Repository: *openai-mastery-24*

---

## 1. Overview

This skill report summarizes all capabilities learned and implemented during **Project 01**, including:

- Stateless chat client  
- Stateful chat client with memory  
- Internal command system  
- Logging engine  
- Sampling configuration  
- Token usage  
- Latency measurement  
- Model selection  

This project forms the foundation for all upcoming CLI, agent, and multi-modal interfaces in Projects 02–24.

---

## 2. OpenAI API Skills Acquired

### ✔ Responses API (core)
- Constructing requests with `client.responses.create`
- Understanding input schema:  
  - Single string (stateless)  
  - List of `{role, content}` messages (stateful)
- Extracting:
  - `response.output_text`
  - `response.usage.input_tokens`
  - `response.usage.output_tokens`
  - `response.usage.total_tokens`
- Handling sampling parameters:
  - `temperature`
