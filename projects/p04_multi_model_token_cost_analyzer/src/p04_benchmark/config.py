from __future__ import annotations

# Benchmark identity / reproducibility
BENCHMARK_VERSION = "v1"
PRICING_LABEL = "pricing_2025-12-16"  # bump whenever pricing table changes
SHUFFLE_SEED = 42  # fixed seed for reproducible interleaving

# Models under test (TOP / MID / ECON)
MODELS = [
    "gpt-5.2",
    "gpt-4.1",
    "gpt-4.1-nano",
]

MODEL_CAPABILITIES = {
    "gpt-4.1": {
        "max_tokens_param": "max_tokens",
    },
    "gpt-4.1-nano": {
        "max_tokens_param": "max_tokens",
    },
    "gpt-5.2": {
        "max_tokens_param": "max_completion_tokens",
    },
}


# Prompt set (must match prompts.py prompt_id values)
PROMPT_IDS = [
    "A_short_objective_v1",
    "B_mid_bullets_v1",
    "C_json_strict_v1",
]

# Controlled conditions (held constant across all runs and models)
TEMPERATURE = 0.0
TOP_P = 1.0
MAX_TOKENS = 250

# Experiment plan
WARMUP_RUNS_PER_PAIR = 1      # per (model x prompt_id)
MEASURE_RUNS_PER_PAIR = 7     # per (model x prompt_id)

# Output locations (repository-relative)
RUNS_DIR = "runs"
RESULTS_JSONL = f"{RUNS_DIR}/results.jsonl"
SUMMARY_JSON = f"{RUNS_DIR}/summary.json"
SUMMARY_MD = f"{RUNS_DIR}/summary.md"
