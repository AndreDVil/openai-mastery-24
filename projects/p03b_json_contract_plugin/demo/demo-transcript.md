# Demo — Project 03: JSON Mode Safety Pipeline

This demo illustrates how the JSON Mode Chat Client enforces strict contracts,
detects violations, and self-corrects via a controlled retry mechanism.

---

## Demo Setup

- OpenAI SDK: 2.9.0
- API: Chat Completions
- JSON Mode: Enabled
- Contract: StructuredAnswerLite v1.0
- max_retries: 2
- debug: Enabled (for demonstration purposes)

---

## Demo 1 — Valid Request (No Retry)

### User Input
Explain what JSON Mode is in OpenAI Python SDK 2.9.

### Debug Output
[DEBUG] Attempt 1/3  
[DEBUG] Validation passed. Returning final JSON response.

### Final Response (JSON)
{
  "task": {
    "type": "qa",
    "user_intent": "Explain what JSON Mode is in OpenAI Python SDK 2.9"
  },
  "answer": {
    "text": "JSON Mode is a feature in the OpenAI Python SDK that guides the model to produce strictly JSON-formatted output, enabling reliable parsing and downstream processing."
  },
  "quality": {
    "confidence": 0.9,
    "assumptions": [
      "The user is referring to the JSON output enforcement feature."
    ],
    "risks": [
      "The model may still occasionally deviate without validation."
    ]
  },
  "debug": {
    "schema_version": "1.0",
    "model": "gpt-4o-mini"
  }
}

---

## Demo 2 — Schema Violation (Type Error → Retry)

### User Input
Explain JSON Mode, but express confidence in words.

### Debug Output
[DEBUG] Attempt 1/3  
[DEBUG] Schema validation failed with errors:  
- quality.confidence must be a number  

[DEBUG] Attempt 2/3  
[DEBUG] Validation passed. Returning final JSON response.

### Corrected Final Response (JSON)
{
  "task": {
    "type": "qa",
    "user_intent": "Explain JSON Mode"
  },
  "answer": {
    "text": "JSON Mode ensures that model outputs are strictly formatted as JSON, making them easier to validate and consume in production systems."
  },
  "quality": {
    "confidence": 0.9,
    "assumptions": [
      "JSON Mode is intended for structured outputs."
    ],
    "risks": [
      "Relying solely on JSON Mode without validation can still cause failures."
    ]
  },
  "debug": {
    "schema_version": "1.0",
    "model": "gpt-4o-mini"
  }
}

---

## Demo Summary

This demo demonstrates:

- Enforcement of JSON-only output
- Detection of semantic schema violations
- Automatic corrective retry with explicit feedback
- Silent convergence to a valid contract-compliant response

The client behaves as a reliable API component, not a free-form text generator.
