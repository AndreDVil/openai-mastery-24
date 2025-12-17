# Project 04 — Multi-Model Token Cost & Latency Analyzer

This project is part of the **openai-mastery-24** engineering track.

Its purpose is to build a **reproducible, measurement-driven benchmark** to compare OpenAI models under controlled conditions, focusing on:

- token usage
- estimated cost
- end-to-end latency
- output robustness and format compliance

Rather than treating models as interchangeable, this project treats them as **engineering components with distinct trade-offs**.

---

## Objectives

### Primary Objectives
- Measure real-world trade-offs between OpenAI models
- Build intuition around **cost vs latency vs robustness**
- Develop discipline around **controlled experiments**
- Understand how model contracts differ in practice

### Secondary Objectives
- Practice clean separation of concerns
- Build auditable, reproducible experiments
- Learn to detect silent failures in LLM outputs

---

## Models Evaluated

The benchmark compares three models representing different tiers:

| Tier | Model |
|-----:|------|
| TOP  | gpt-5.2 |
| MID  | gpt-4.1 |
| ECON | gpt-4.1-nano |

Each model is treated as a **black-box API component**, evaluated under identical prompts and conditions whenever possible.

---

## What Is Measured

For each run, the following metrics are collected:

### Latency
- **latency_e2e_ms**  
  Wall-clock time from request dispatch to response receipt.

### Token Usage
- input_tokens
- output_tokens
- total_tokens

### Cost (Estimated)
Using a static pricing table (USD per 1M tokens):
- input cost
- output cost
- total estimated cost per run

> Pricing is intentionally static to ensure reproducibility.  
> Any pricing change requires a new `pricing_label`.

### Output Observables
- output_chars (length of generated text)

### Robustness / Compliance
Depending on the prompt:
- `format_ok` (did the model respect structural constraints?)
- For JSON prompts:
  - `json_parse_ok`
  - `schema_ok`

---

## Prompt Set

The benchmark uses **three prompts**, each designed to stress a different capability.

### Prompt A — Short, Objective Text
- Exactly 2 sentences
- No newlines
- No lists
- Simple language

Purpose:
- Test minimal generation latency
- Test basic instruction-following

---

### Prompt B — Medium Text with Structural Constraints
- Exactly 8 bullet points
- Each bullet ≤ 12 words
- No extra text outside bullets

Purpose:
- Test compression + structure
- Reveal silent failures in smaller models

---

### Prompt C — Strict JSON Contract
- JSON only, no extra text
- Fixed schema:
  - title
  - summary (200–260 chars)
  - 5 actions (8–14 words each)
  - risk_level enum

Purpose:
- Test **contract reliability**
- Measure schema adherence vs cost

---

## Benchmark Design

### Controlled Conditions

All runs share the same generation parameters:
- temperature = 0.0
- top_p = 1.0
- max token budget = 250

The only variable is **the model**.

---

### Run Plan Structure

For each `(model × prompt)` pair:

1. **Warm-up phase**
   - 1 run
   - Recorded, but excluded from statistics
   - Purpose: reduce cold-start effects

2. **Measurement phase**
   - 7 runs
   - Included in all summaries

Total runs:
- 3 models × 3 prompts × (1 warm-up + 7 measured) = **72 runs**

Measured runs:
- **63**

---

### Interleaving Strategy

Measurement runs are **interleaved**:

- For each trial index:
  - prompts are fixed
  - model order is shuffled
- Shuffle uses a fixed seed for reproducibility

This prevents:
- one model consistently benefiting from cache/warm state
- temporal bias in latency measurements

---

## Architecture Overview

### Key Modules

- `prompts.py`  
  Versioned prompt definitions treated as data.

- `pricing.py`  
  Static pricing table with explicit labels.

- `config.py`  
  Freezes the experiment definition.

- `measure.py`  
  Executes **one single run**:
  - API call
  - timing
  - token extraction
  - cost estimation
  - compliance validation

- `runner.py`  
  Builds the run plan and orchestrates execution.

- `io.py`  
  Safe, incremental persistence (JSONL).

- `summarize.py`  
  Aggregates results:
  - median
  - p95
  - compliance rates

---

## Persistence Strategy

Each run is written **immediately** to disk as one JSON line:

- format: `results.jsonl`
- flushed after every write

Benefits:
- crash-safe
- auditable
- partial results are never lost

The disk is treated as the **source of truth**.

---

## Summary Metrics

For each `(model × prompt)` pair, the summary reports:

- latency median and p95
- cost median and p95
- median input/output tokens
- format compliance rates
- JSON parse and schema adherence (Prompt C only)

---

## Key Findings (High-Level)

- **Models are not interchangeable**
- Smaller models fail silently under strict constraints
- Robustness is significantly more expensive than speed
- Latency variance (p95) is often more important than median latency
- JSON schema adherence is the most expensive capability

These insights directly inform **model selection in production systems**.

---

## How to Run

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate  # or Windows equivalent
pip install -r requirements.txt

Then:

cd projects/p04_multi_model_token_cost_analyzer
export PYTHONPATH=src  # Windows: set PYTHONPATH=src
python -m scripts.run_benchmark


Artifacts will be written to:

runs/results.jsonl
runs/summary.json
runs/summary.md

Educational Value

This project demonstrates that:

Benchmarking LLMs is not about “which model is best”,
but about which model is appropriate for a given engineering constraint.

It reinforces disciplined experimentation, defensive design, and evidence-based decision-making.