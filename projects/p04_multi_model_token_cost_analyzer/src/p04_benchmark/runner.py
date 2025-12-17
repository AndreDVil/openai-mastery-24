from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Dict, List

from openai import OpenAI

from . import config
from .io import append_jsonl
from .measure import run_once
from .prompts import get_prompt


@dataclass(frozen=True)
class RunPlanItem:
    prompt_id: str
    model: str
    trial_index: int
    is_warmup: bool


def build_run_plan() -> List[RunPlanItem]:
    """
    Builds an ordered run plan:
      - warm-up: 1 run per (model x prompt_id), trial_index=0, is_warmup=True
      - measurement: MEASURE_RUNS_PER_PAIR runs per (model x prompt_id), interleaved
    """
    rng = random.Random(config.SHUFFLE_SEED)
    plan: List[RunPlanItem] = []

    # Warm-up runs (recorded but excluded from summaries)
    for prompt_id in config.PROMPT_IDS:
        for model in config.MODELS:
            plan.append(
                RunPlanItem(
                    prompt_id=prompt_id,
                    model=model,
                    trial_index=0,
                    is_warmup=True,
                )
            )

    # Measurement runs (interleaved, model order shuffled per (trial, prompt))
    for trial_index in range(1, config.MEASURE_RUNS_PER_PAIR + 1):
        for prompt_id in config.PROMPT_IDS:
            models = list(config.MODELS)
            rng.shuffle(models)
            for model in models:
                plan.append(
                    RunPlanItem(
                        prompt_id=prompt_id,
                        model=model,
                        trial_index=trial_index,
                        is_warmup=False,
                    )
                )

    return plan


def run_benchmark(
    *,
    client: OpenAI,
    results_jsonl_path: str = config.RESULTS_JSONL,
) -> List[Dict[str, Any]]:
    """
    Executes the benchmark plan and appends each run record to results.jsonl.

    Returns:
        A list of run records (also written to disk).
    """
    plan = build_run_plan()
    records: List[Dict[str, Any]] = []

    for item in plan:
        prompt = get_prompt(item.prompt_id)

        record = run_once(
            client=client,
            model=item.model,
            prompt_id=item.prompt_id,
            messages=prompt.messages,
            trial_index=item.trial_index,
            is_warmup=item.is_warmup,
            temperature=config.TEMPERATURE,
            top_p=config.TOP_P,
            max_tokens=config.MAX_TOKENS,
            pricing_label=config.PRICING_LABEL,
        )

        append_jsonl(results_jsonl_path, record)
        records.append(record)

    return records
