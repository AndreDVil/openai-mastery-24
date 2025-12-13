# Project 03 — JSON Mode Chat Client

## 1. Overview

Project 03 builds a **minimal but robust JSON Mode chat client** using the **OpenAI Python SDK 2.9.0** and the **Chat Completions API**. The client enforces strict JSON-only outputs, validates responses against an explicit contract, and applies a controlled retry mechanism with corrective feedback.

This project is intentionally designed as a **foundational building block** for more advanced systems such as tool-calling agents, RAG pipelines, and autonomous workflows.

Beyond functionality, a core goal of this project is **deep understanding**: every layer (prompting, parsing, validation, retry) is implemented manually and transparently.

---

## 2. Key Technical Decisions

* **OpenAI SDK**: `openai==2.9.0`
* **API**: `client.chat.completions.create`
* **Responses API**: *explicitly not used*
* **JSON Mode**: enabled via `response_format={"type": "json_object"}`
* **Validation**: manual (no external schema libraries)
* **Retry policy**: deterministic, bounded, self-correcting

This project follows the modern OpenAI API paradigm (2.x).

---

## 3. JSON Contract — StructuredAnswerLite v1.0

All model responses must conform **exactly** to the following contract:

```json
{
  "task": {
    "type": "qa | extraction | classification | summarization | other",
    "user_intent": "string"
  },
  "answer": {
    "text": "string"
  },
  "quality": {
    "confidence": "number between 0.0 and 1.0",
    "assumptions": ["string"],
    "risks": ["string"]
  },
  "debug": {
    "schema_version": "1.0",
    "model": "string"
  }
}
```

### Design rules

* All fields are **required**
* `additionalProperties` are **forbidden** at every level
* Arrays may be empty but must exist
* `schema_version` enables controlled future evolution

---

## 4. Safety Pipeline Architecture

The client implements a **four-layer safety pipeline**:

### 1. System Prompt (Governance)

A mandatory system prompt:

* Demands **JSON-only output**
* Embeds the contract verbatim
* Forbids extra keys, renamed fields, or explanations
* Enforces the exact schema version

This layer prevents most structural violations before they happen.

---

### 2. JSON Mode (Format Enforcement)

JSON Mode is enabled at the API level:

```python
response_format={"type": "json_object"}
```

This forces the model to return a JSON object instead of free text.

---

### 3. Manual Parsing

The raw model output is parsed using:

```python
json.loads(raw_text)
```

This detects **syntactic JSON errors** (malformed JSON, wrong top-level type).

---

### 4. Manual Schema Validation

A custom validator enforces:

* Required fields
* Absence of extra fields
* Correct data types
* Enum constraints (`task.type`)
* Numeric bounds (`confidence` ∈ [0.0, 1.0])
* Exact schema version

Validation failures return **structured error information**, not exceptions.

---

## 5. Controlled Retry Strategy

When validation fails, the client performs a **single controlled retry** (configurable via `max_retries`).

### Retry triggers

* `INVALID_JSON` (parsing failure)
* `SCHEMA_VALIDATION_FAILED` (contract violation)

### Retry mechanism

* A corrective **system message** is injected
* Validation errors are listed explicitly
* The model is instructed to return **only a corrected JSON object**

This creates a **self-correcting system** without infinite loops.

---

## 6. Debug Mode

The client supports an optional debug flag:

```python
JsonModeChatClient(..., debug=True)
```

When enabled, it logs:

* Attempt count
* Validation failures
* Successful convergence

Debug output is **observational only** and does not affect behavior or returned data.

---

## 7. Project Structure

```
projects/p03_json_mode/
├── README.md
├── skills-report.md
├── demo/
│   └── demo-transcript.md
└── src/
    ├── config.py
    ├── prompts.py
    ├── schemas.py
    ├── validators.py
    ├── json_client.py
    └── __init__.py
```

---

## 8. Known Limitations & Future Improvements

### Current limitations (intentional)

* Text-only answers (`answer.text`)
* Manual validation (no `jsonschema`)
* No CLI interface
* No advanced error handling (timeouts, rate limits)

### Future improvements

* Structured payloads (`answer.data`)
* `jsonschema` integration
* Configurable retry policies
* CLI with `--debug` and `--model`
* Extension for tool-calling and agents

---

## 9. Conclusion

Project 03 demonstrates how to move from **prompting** to **contract-driven AI systems**. By combining JSON Mode, explicit schemas, validation, and corrective retries, the client behaves like a reliable API component rather than a text generator.

This project serves as a strong foundation for all subsequent projects in the openai-mastery-24 track.
