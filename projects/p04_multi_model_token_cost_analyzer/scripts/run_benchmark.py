from __future__ import annotations

import os

from openai import OpenAI

from p04_benchmark import config
from p04_benchmark.io import ensure_dir, write_json, write_text
from p04_benchmark.runner import run_benchmark
from p04_benchmark.summarize import read_jsonl, render_summary_md, summarize


def main() -> None:
    # Ensure output directory exists
    ensure_dir(config.RUNS_DIR)

    # Instantiate OpenAI client (expects OPENAI_API_KEY in env)
    client = OpenAI()

    # Run benchmark (writes results incrementally to JSONL)
    run_benchmark(client=client, results_jsonl_path=config.RESULTS_JSONL)

    # Summarize results from disk (source of truth)
    records = read_jsonl(config.RESULTS_JSONL)
    summary_obj = summarize(records)
    summary_md = render_summary_md(summary_obj)

    # Write artifacts
    write_json(config.SUMMARY_JSON, summary_obj)
    write_text(config.SUMMARY_MD, summary_md)

    print("Benchmark completed.")
    print(f"- results: {config.RESULTS_JSONL}")
    print(f"- summary: {config.SUMMARY_JSON}")
    print(f"- report : {config.SUMMARY_MD}")


if __name__ == "__main__":
    main()
