# ROADMAP-24 — Complete AI Engineering Journey  
*openai-mastery-24 official roadmap (HQ CENTRAL approved)*

Este documento apresenta a visão macro dos 24 projetos que compõem a trilha completa de engenharia de IA.  
Cada módulo segue progressão lógica, cobrindo todos os pilares modernos de AI Engineering, OpenAI APIs, RAG, agentes e produtos reais.

**SDK note:** All projects in this roadmap use the modern OpenAI Python SDK 2.9.0 (`OpenAI()` client + `chat.completions.create`). Legacy/1.x patterns are intentionally not used.
---

# 📊 **Overview Table (High-Level Map)**

| #  | Project Name                                | Objective (1 line)                                         | Core Feature / Skill |
|----|----------------------------------------------|-------------------------------------------------------------|-----------------------|
| 00 | Foundations                                  | Entender modelos, tokens, custos e respostas básicas        | Responses API basics  |
| 01 | Basic Chat (CLI)                              | Criar um cliente de chat simples com estado opcional        | Chat completions       |
| 02 | Streaming Chat                                | Implementar streaming de tokens em tempo real               | Streaming responses    |
| 03 | JSON Mode Chat                                | Forçar respostas estruturadas via JSON Mode                 | JSON mode + schemas    |
| 04 | Token Cost Analyzer                           | Comparar custo/latência entre modelos                       | Benchmarking + batches |
| 05 | Summarization Memory                          | Implementar memória longa via resumos                       | Summaries + compression |
| 06 | Chat with File Uploads                        | Enviar arquivos e conversar com documentos                  | File API               |
| 07 | Tool Calling: Local Tools                     | Executar funções Python locais                              | Tool calling (basic)   |
| 08 | Tool Calling: External APIs                   | Integrar APIs externas reais                                | Tool calling (advanced)|
| 09 | Image Generation Client                       | Criar imagens dinamicamente                                 | gpt-image models       |
| 10 | Vision Chat                                   | Interpretar imagens                                          | Vision multimodal      |
| 11 | Audio Transcription & TTS                     | Converter áudio ↔ texto                                     | Whisper + TTS          |
| 12 | Basic RAG                                     | Implementar RAG minimalista com embeddings                  | Embeddings + retrieval |
| 13 | Local Vector DB RAG                           | Integrar banco vetorial (FAISS/Chroma)                      | Indexing + pipelines   |
| 14 | Advanced RAG                                  | RAG robusto com metadados e reranking                       | Hybrid retrieval        |
| 15 | Fine-Tuning Small Models                      | Treinar modelos pequenos específicos                        | Fine-tuning pipeline   |
| 16 | Function-Calling Agent                        | Agente conversacional com ferramentas                       | Context + orchestration |
| 17 | Web Automation Agent                          | Agente que navega a web via *LLM Planning + Tool Execution* | Planning + browser tools |
| 18 | AI Workflow Orchestrator                      | Construir pipelines automáticos com LLM                     | Multi-step reasoning    |
| 19 | Multi-Agent Collaboration                     | Dois ou mais agentes debatendo e gerando consenso           | Multi-agent loops       |
| 20 | Personal Knowledge Base Agent                 | Agente usando notas pessoais como fonte de verdade          | RAG personalizado       |
| 21 | Domain-Specific Assistant                     | Assistente especializado em um domínio técnico              | Retrieval + constraints |
| 22 | Realtime API Voice Assistant                  | Agente que conversa por voz em tempo real                   | Realtime API            |
| 23 | Full Multi-Modal Application                  | App completo combinando texto, imagem, áudio e ferramentas  | Multimodal orchestration|
| 24 | Life OS — Autonomous Multi-Agent System       | Sistema autônomo persistente com memória e ferramentas      | Multi-agent architecture |

---

# 📚 **Detailed Sections (Project by Project)**

---

## **00 — Foundations**
**Objetivo:** dominar modelos, tokens, custos, latência e chamadas básicas.  
**Feature principal:** Responses API, sampling, token usage.

---

## **01 — Basic Chat (CLI Chat Client)**
**Objetivo:** criar um cliente de chat no terminal com estado opcional.  
**Feature:** chat completions + context window.

---

## **02 — Streaming Chat Client**
**Objetivo:** implementar streaming de tokens e UX incremental.  
**Feature:** stream responses + callbacks.

---

## **03 — JSON Mode Chat**
**Objetivo:** garantir respostas estritamente estruturadas.  
**Feature:** JSON mode + schema validation.

---

## **04 — Multi-Model Token Cost Analyzer**
**Objetivo:** comparar automaticamente custo, latência e tokens por modelo.  
**Feature:** batch requests + benchmarking.

---

## **05 — Stateful Chat with Summarization Memory**
**Objetivo:** criar memória longa via resumos automáticos.  
**Feature:** summarization + context compression.

---

## **06 — Chat with File Uploads & Document Handling**
**Objetivo:** enviar arquivos e conversar com documentos locais.  
**Feature:** File API + multimodal file inputs.

---

## **07 — Tool Calling: Local Tools**
**Objetivo:** chamar funções Python locais com segurança.  
**Feature:** tool-calling básico + execução controlada.

---

## **08 — Tool Calling: External API Integrations**
**Objetivo:** integrar APIs reais (clima, mapas, finanças).  
**Feature:** tool calling avançado + retorno estruturado.

---

## **09 — Image Generation Client**
**Objetivo:** gerar imagens baseadas em prompts dinâmicos.  
**Feature:** gpt-image models.

---

## **10 — Vision Chat Client**
**Objetivo:** interpretar imagens enviadas pelo usuário.  
**Feature:** vision multimodal inputs.

---

## **11 — Audio Transcription & TTS Client**
**Objetivo:** converter áudio ↔ texto.  
**Feature:** Whisper + text-to-speech.

---

## **12 — Retrieval with Embeddings (Basic RAG)**
**Objetivo:** criar RAG simples usando embeddings locais.  
**Feature:** embeddings + cosine similarity.

---

## **13 — Local Vector Database RAG**
**Objetivo:** usar FAISS/Chroma como banco vetorial.  
**Feature:** indexing + vector search pipelines.

---

## **14 — Advanced RAG with Reranking and Metadata**
**Objetivo:** implementar RAG moderno usando metadados e reranking.  
**Feature:** hybrid retrieval + scoring.

---

## **15 — Fine-Tuning Small Models**
**Objetivo:** treinar modelos pequenos e medir ganhos reais.  
**Feature:** fine-tuning pipeline + evals.

---

## **16 — Function-Calling Conversational Agent**
**Objetivo:** montar agente conversacional com ferramentas reais.  
**Feature:** orchestration + context manager.

---

## **17 — Web Automation Agent (LLM Planning Loop)**
**Objetivo:** criar um agente capaz de navegar websites, executar ações e extrair dados  
através de um ciclo moderno de:

1. **LLM Planning:** o modelo cria um plano estruturado de ações  
2. **Tool Execution:** navegador headless executa o plano  
3. **State Feedback:** estado da página volta para o modelo  
4. **Iteration Loop:** o modelo decide próximo passo até o objetivo ser atingido

**Feature principal:** planning + browser automation tool + controlled agent loop.

---

## **18 — AI Workflow Orchestrator**
**Objetivo:** construir pipelines automáticos com LLM.  
**Feature:** multi-step reasoning + chained instructions.

---

## **19 — Multi-Agent Collaboration**
**Objetivo:** agentes conversando entre si via debate, crítica e consenso.  
**Feature:** multi-agent loops + arbitration.

---

## **20 — Personal Knowledge Base Agent**
**Objetivo:** integrar um agente às notas pessoais como memória de longo prazo.  
**Feature:** embeddings + RAG personalizado.

---

## **21 — Domain-Specific Assistant**
**Objetivo:** configurar um assistente especializado (ex: financeiro, médico, jurídico).  
**Feature:** domain constraints + formatting rules + retrieval.

---

## **22 — Assistant with Realtime API**
**Objetivo:** criar agente de voz em tempo real.  
**Feature:** Realtime API (audio input/output streaming).

---

## **23 — Custom Multi-Modal Application**
**Objetivo:** combinar texto, imagem, áudio e ferramentas em um único app.  
**Feature:** multimodal messages + orchestration.

---

## **24 — Life OS — Autonomous Multi-Agent System**
**Objetivo:** criar um sistema completo, autônomo, persistente, com memória, ferramentas, agenda e múltiplos agentes especializados.  
**Feature:** multi-agent architecture + embeddings memory + RAG + scheduling.

---

# ✔ FINAL NOTES

Este roadmap é a visão oficial do HQ CENTRAL.  
Todos os projetos devem seguir:

- **Definition of Done**  
- Padrões de documentação  
- Padrões de Git + PR  
- Templates oficiais  
- CERTIFICATE.md para registrar progresso

Boa jornada — ao completar isso, você literalmente se torna **AI Engineer Senior por mérito real**.

