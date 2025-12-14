
---

## Architecture

### Contract Interface

Each contract must provide:

- `name`
- `system_prompt`
- `validate(payload) -> ValidationResult`

Contracts are defined using **Protocol**, not inheritance, enabling
duck-typed, low-coupling extensibility.

---

### Client Responsibilities

The `JsonModeChatClient` is responsible for:

- maintaining message history
- enforcing JSON Mode
- parsing raw JSON
- calling contract validation
- injecting corrective feedback
- retrying in a controlled manner

The client **never imports schemas, prompts, or validators directly**.

---

## Included Contracts

### StructuredAnswerLiteContract

A minimal, general-purpose contract used for:
- explanations
- QA
- summarization
- extraction

It serves as the default example and baseline contract.

---

### SupportTicketContract

A realistic, production-style contract that extracts structured
customer support tickets from free-form messages.

This example demonstrates:
- enum enforcement
- nested objects
- optional fields via `null`
- semantic validation
- retry-based self-correction

---

## What This Project Is (and Is Not)

### This project **is**:
- an architectural exploration
- a learning artifact
- a foundation for future agent systems
- intentionally explicit and verbose

### This project **is not**:
- a polished product
- a finalized API
- optimized for brevity
- meant to replace Project 03

Project 03 remains the **official deliverable**.
Project 03b is an **extension and abstraction layer**.

---

## Relationship to Future Projects

This contract-driven approach directly prepares the ground for:

- Tool Calling
- Agent orchestration
- RAG pipelines with structured outputs
- Governance and safety layers
- Autonomous workflows

Many future projects will reuse this mental model.

---

## Status

This project is considered **complete for its exploratory purpose**.

No additional demos or skill reports are required at this stage.
Further refinement may happen organically as future projects build on it.
