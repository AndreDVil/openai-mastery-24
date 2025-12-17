# Measurement Spec — Project 04 (Multi-Model Token Cost & Latency Analyzer)

This document defines the measurement contract for Project 04.
It specifies what is measured, units, output formats, and aggregation rules.
It is intentionally minimal and implementation-agnostic.

## 1. Definitions

### 1.1 Run
A **run** is a single call to `client.chat.completions.create(...)` for:
- one model
- one prompt variant (prompt_id)
- one trial index

### 1.2 Cost (Estimated)
**Estimated cost (USD)** is computed from token usage and a static pricing table:

`estimated_cost_usd = (input_tokens * input_rate + output_tokens * output_rate) / 1_000_000`

Where:
- `input_rate` = USD per 1M input tokens for that model
- `output_rate` = USD per 1M output tokens for that model

Cost is an estimate for comparability and reproducibility, not billing truth.

### 1.3 Latency (E2E)
**E2E latency** is wall-clock time measured on the client:
- start: immediately before calling the SDK method
- end: when the full response object is received

Unit: milliseconds.

### 1.4 Format Compliance
- **format_ok**: boolean indicating whether the output met the requested formatting constraints.
- For JSON prompt(s):
  - **json_parse_ok**: JSON parsed successfully
  - **schema_ok**: output matches the defined minimal schema constraints

## 2. Controlled Conditions (Benchmark Defaults)

All runs MUST use identical params across models:
- temperature: 0
- top_p: 1
- max_tokens: 250
- presence_penalty: 0 (or omitted)
- frequency_penalty: 0 (or omitted)

All prompts are fixed and versioned by `prompt_id`.

## 3. Prompt Set (MVP)

This spec assumes 3 prompts:
- A_short_objective_v1
- B_mid_bullets_v1
- C_json_strict_v1

Prompts are stored as data (not hardcoded inside benchmark logic) and referenced by `prompt_id`.

## 4. Experiment Plan (MVP)

- Models: 3 (TOP, MID, ECON)
- Warm-up: 1 run per (model × prompt_id), recorded but excluded from summary stats
- Measurement: 7 runs per (model × prompt_id)
- Execution order: interleaved across models to reduce time-based bias

## 5. Output Artifacts

### 5.1 results.jsonl (Required)
A newline-delimited JSON file where each line is one run record.

File path (recommended):
- `runs/results.jsonl`

Each line MUST be a single JSON object matching the schema below.

### 5.2 summary.json (Optional but Recommended)
A machine-readable aggregation output.

File path (recommended):
- `runs/summary.json`

### 5.3 summary.md (Recommended)
A human-readable summary, short and actionable.

File path (recommended):
- `runs/summary.md`

## 6. Run Record Schema (results.jsonl)

### 6.1 Required Fields

#### Identity
- run_id: string (unique)
- timestamp_utc: string (ISO 8601, UTC)
- model: string
- prompt_id: string
- trial_index: integer (1..N)
- is_warmup: boolean

#### Request Params
- temperature: number
- top_p: number
- max_tokens: integer

#### Latency
- latency_e2e_ms: integer (>= 0)

#### Token Usage
- input_tokens: integer (>= 0)
- output_tokens: integer (>= 0)
- total_tokens: integer (>= 0)

#### Pricing / Cost
- pricing_label: string (e.g., "pricing_YYYY-MM-DD")
- input_rate_per_million: number (USD per 1M)
- output_rate_per_million: number (USD per 1M)
- estimated_cost_usd: number (>= 0)

#### Output Observables
- output_chars: integer (>= 0)

#### Compliance
- format_ok: boolean

For JSON prompts ONLY:
- json_parse_ok: boolean
- schema_ok: boolean

#### Error Handling
- status: string enum: "ok" | "error"
- error_type: string | null
- error_message: string | null

### 6.2 Optional Fields (Allowed)
- output_text: string (store only if you accept storing model outputs)
- output_json: object (for JSON prompt if you store parsed output)
- retry_count: integer (if you implement retries later)
- notes: string (manual quality notes)

## 7. Summary Aggregation Rules (summary.*)

All summary statistics MUST exclude warm-up runs (`is_warmup = true`).

For each (model × prompt_id), compute:
- latency_e2e_ms: median, p95
- estimated_cost_usd: median, p95
- input_tokens: median
- output_tokens: median
- format_ok_rate: mean (0..1)

For JSON prompts, additionally:
- json_parse_ok_rate: mean (0..1)
- schema_ok_rate: mean (0..1)

Overall per model (across prompts), you MAY compute:
- weighted medians (by equal prompt weight), or simply report per-prompt only (preferred for MVP).

## 8. Pricing Table (MVP)

This spec requires a static pricing table embedded in the repo (as data), keyed by model.

Required for this MVP:
- gpt-5.2
- gpt-4.1
- gpt-4.1-nano

The actual USD rates must be recorded in each run record (input_rate_per_million, output_rate_per_million)
to preserve reproducibility even if the pricing table changes later.

## 9. Non-Goals (MVP)

- No external benchmarking frameworks
- No dashboards
- No streaming TTFT measurement
- No quality scoring rubric (manual notes only, optional)

## 10. Versioning

Any change to:
- prompts,
- benchmark params,
- run schema,
- pricing table

MUST bump a label in:
- pricing_label (if prices changed)
- prompt_id versions (if prompt text changed)
- a top-level BENCHMARK_VERSION constant (implementation detail)
