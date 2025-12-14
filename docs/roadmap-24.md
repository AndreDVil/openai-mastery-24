# ROADMAP-24 — Complete AI Engineering Journey  
*openai-mastery-24 official roadmap (HQ CENTRAL approved)*

This document presents the macro-level vision of the 24 projects that compose the complete AI Engineering journey.  
Each module follows a logical progression, covering all modern pillars of AI Engineering, OpenAI APIs, RAG, agents, and real-world products.

**SDK note:** All projects in this roadmap use the modern OpenAI Python SDK 2.9.0 (`OpenAI()` client + `chat.completions.create`). Legacy / 1.x patterns are intentionally not used.

---

# 📊 Overview Table (High-Level Map)

| #  | Project Name                              | Objective (1 line)                                           | Core Feature / Skill |
|----|-------------------------------------------|---------------------------------------------------------------|---------------------|
| 00 | Foundations                               | Understand models, tokens, costs, and basic responses          | API fundamentals    |
| 01 | Basic Chat (CLI)                          | Build a simple CLI chat client with optional state             | Chat completions    |
| 02 | Streaming Chat                            | Implement real-time token streaming                            | Streaming responses |
| 03 | JSON Mode Chat                            | Enforce strictly structured responses                          | JSON mode + schemas |
| 04 | Token Cost Analyzer                      | Compare cost and latency across models                         | Benchmarking        |
| 05 | Summarization Memory                     | Implement long-term memory via summaries                       | Compression         |
| 06 | Chat with File Uploads                   | Upload files and chat with documents                           | File API            |
| 07 | Tool Calling: Local Tools                | Execute local Python functions                                 | Tool calling (basic)|
| 08 | Tool Calling: External APIs              | Integrate real external APIs                                   | Tool calling (adv.) |
| 09 | Image Generation Client                  | Generate images dynamically                                    | Image models        |
| 10 | Vision Chat                              | Interpret images                                               | Vision multimodal   |
| 11 | Audio Transcription & TTS                | Convert audio ↔ text                                           | Whisper + TTS       |
| 12 | Basic RAG                                | Implement minimal RAG with embeddings                          | Retrieval           |
| 13 | Local Vector DB RAG                      | Integrate a vector database (FAISS/Chroma)                     | Indexing pipelines  |
| 14 | Advanced RAG                             | Robust RAG with metadata and reranking                         | Hybrid retrieval    |
| 15 | Fine-Tuning Small Models                 | Fine-tune small models for specific tasks                      | Fine-tuning         |
| 16 | Function-Calling Agent                  | Conversational agent with tools                                | Orchestration       |
| 17 | Web Automation Agent                    | Agent that navigates the web via planning + tools              | Planning loops      |
| 18 | AI Workflow Orchestrator                | Build automated LLM pipelines                                  | Multi-step reasoning|
| 19 | Multi-Agent Collaboration               | Multiple agents debating and reaching consensus                | Multi-agent loops   |
| 20 | Personal Knowledge Base Agent            | Agent using personal notes as source of truth                  | Personalized RAG    |
| 21 | Domain-Specific Assistant               | Specialized assistant for a technical domain                   | Constraints + RAG   |
| 22 | Realtime API Voice Assistant             | Real-time voice-based assistant                                 | Realtime API        |
| 23 | Full Multi-Modal Application             | Complete app combining text, image, audio, and tools           | Multimodal systems  |
| 24 | Life OS — Autonomous Multi-Agent System  | Persistent autonomous system with memory and tools             | System architecture |

---

# 📚 Detailed Sections (Project by Project)

---

## 00 — Foundations
**Objective:** Master models, tokens, costs, latency, and basic API calls.  
**Core feature:** sampling, token usage, cost awareness.

---

## 01 — Basic Chat (CLI Chat Client)
**Objective:** Build a terminal-based chat client with optional state.  
**Core feature:** chat completions + context window management.

---

## 02 — Streaming Chat Client
**Objective:** Implement token streaming with incremental UX.  
**Core feature:** streaming responses + callbacks.

---

## 03 — JSON Mode Chat
**Objective:** Guarantee strictly structured responses.  
**Core feature:** JSON mode + schema validation.

---

## 04 — Multi-Model Token Cost Analyzer
**Objective:** Automatically compare cost, latency, and token usage across models.  
**Core feature:** benchmarking + controlled experiments.

---

## 05 — Stateful Chat with Summarization Memory
**Objective:** Create long-term memory using automatic summaries.  
**Core feature:** summarization + context compression.

---

## 06 — Chat with File Uploads & Document Handling
**Objective:** Upload files and interact with local documents.  
**Core feature:** File API + document processing.

---

## 07 — Tool Calling: Local Tools
**Objective:** Safely call local Python functions.  
**Core feature:** basic tool calling + controlled execution.

---

## 08 — Tool Calling: External API Integrations
**Objective:** Integrate real external APIs (weather, finance, maps).  
**Core feature:** advanced tool calling + structured outputs.

---

## 09 — Image Generation Client
**Objective:** Generate images from dynamic prompts.  
**Core feature:** image generation models.

---

## 10 — Vision Chat Client
**Objective:** Interpret images provided by the user.  
**Core feature:** vision multimodal inputs.

---

## 11 — Audio Transcription & TTS Client
**Objective:** Convert audio ↔ text.  
**Core feature:** speech-to-text and text-to-speech.

---

## 12 — Retrieval with Embeddings (Basic RAG)
**Objective:** Build a simple RAG system using embeddings.  
**Core feature:** embeddings + similarity search.

---

## 13 — Local Vector Database RAG
**Objective:** Use FAISS or Chroma as a vector database.  
**Core feature:** indexing + retrieval pipelines.

---

## 14 — Advanced RAG with Reranking and Metadata
**Objective:** Implement a modern RAG system with metadata and reranking.  
**Core feature:** hybrid retrieval + scoring.

---

## 15 — Fine-Tuning Small Models
**Objective:** Fine-tune small models and measure real gains.  
**Core feature:** fine-tuning pipeline + evaluation.

---

## 16 — Function-Calling Conversational Agent
**Objective:** Build a conversational agent with real tools.  
**Core feature:** orchestration + context management.

---

## 17 — Web Automation Agent (LLM Planning Loop)
**Objective:** Create an agent capable of navigating websites, executing actions, and extracting data through a modern loop:

1. **LLM Planning:** the model generates a structured action plan  
2. **Tool Execution:** a headless browser executes the plan  
3. **State Feedback:** page state is returned to the model  
4. **Iteration Loop:** the model decides the next step until completion  

**Core feature:** planning + browser automation + controlled agent loop.

---

## 18 — AI Workflow Orchestrator
**Objective:** Build automated pipelines using LLMs.  
**Core feature:** multi-step reasoning + chained instructions.

---

## 19 — Multi-Agent Collaboration
**Objective:** Multiple agents debating, criticizing, and reaching consensus.  
**Core feature:** multi-agent loops + arbitration.

---

## 20 — Personal Knowledge Base Agent
**Objective:** Integrate an agent with personal notes as long-term memory.  
**Core feature:** embeddings + personalized RAG.

---

## 21 — Domain-Specific Assistant
**Objective:** Configure a specialized assistant (e.g. finance, medical, legal).  
**Core feature:** domain constraints + formatting rules + retrieval.

---

## 22 — Assistant with Realtime API
**Objective:** Build a real-time voice assistant.  
**Core feature:** Realtime API (audio input/output streaming).

---

## 23 — Custom Multi-Modal Application
**Objective:** Combine text, image, audio, and tools into a single application.  
**Core feature:** multimodal messages + orchestration.

---

## 24 — Life OS — Autonomous Multi-Agent System
**Objective:** Build a complete, autonomous, persistent system with memory, tools, scheduling, and multiple specialized agents.  
**Core feature:** multi-agent architecture + embeddings memory + RAG + scheduling.

---

## Cross-Cutting Concerns: Observability, Evaluation, and Cost Awareness

Starting from **Project 04 onward**, observability and evaluation are considered **expected engineering concerns**, not standalone projects.

This includes, when relevant:
- logging of prompts and responses  
- token usage and cost tracking  
- latency measurement  
- failure mode analysis  
- output quality assessment  
- reproducibility of experiments  

Evaluation and observability practices should evolve naturally as project complexity increases, becoming more explicit in later projects involving:
- RAG systems  
- agents  
- workflows  
- long-running or autonomous systems  

These concerns are intentionally integrated into the projects themselves to reflect real-world AI system engineering, rather than treated as isolated topics.

---

# ✔ FINAL NOTES

This roadmap is the official vision approved by **HQ CENTRAL**.  
All projects must follow:

- Definition of Done  
- Documentation standards  
- Git & PR standards  
- Official templates  
- `CERTIFICATE.md` to track progress  

Good journey — completing this track genuinely qualifies you as a **Senior AI Engineer by real merit**, not by title.
