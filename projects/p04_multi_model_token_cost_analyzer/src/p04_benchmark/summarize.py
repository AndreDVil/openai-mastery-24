from __future__ import annotations

import json
import math
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Tuple


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def _percentile(sorted_values: List[float], p: float) -> float:
    """
    Nearest-rank percentile (simple and stable for small N).
    p in [0, 100].
    """
    if not sorted_values:
        return 0.0
    if p <= 0:
        return float(sorted_values[0])
    if p >= 100:
        return float(sorted_values[-1])

    k = math.ceil((p / 100.0) * len(sorted_values)) - 1
    k = max(0, min(k, len(sorted_values) - 1))
    return float(sorted_values[k])


def _median(sorted_values: List[float]) -> float:
    if not sorted_values:
        return 0.0
    n = len(sorted_values)
    mid = n // 2
    if n % 2 == 1:
        return float(sorted_values[mid])
    return float((sorted_values[mid - 1] + sorted_values[mid]) / 2.0)


def _mean_bool(values: List[bool]) -> float:
    if not values:
        return 0.0
    return float(sum(1 for v in values if v) / len(values))


def summarize(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Produces a machine-readable summary object.

    Excludes warm-up runs (is_warmup = true).
    """
    measured = [r for r in records if not bool(r.get("is_warmup", False))]

    # group by (model, prompt_id)
    groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for r in measured:
        groups[(str(r["model"]), str(r["prompt_id"]))].append(r)

    by_pair: List[Dict[str, Any]] = []

    for (model, prompt_id), rs in sorted(groups.items()):
        latencies = sorted(float(r.get("latency_e2e_ms", 0)) for r in rs)
        costs = sorted(float(r.get("estimated_cost_usd", 0.0)) for r in rs)

        input_tokens = sorted(float(r.get("input_tokens", 0)) for r in rs)
        output_tokens = sorted(float(r.get("output_tokens", 0)) for r in rs)

        format_ok_rate = _mean_bool([bool(r.get("format_ok", False)) for r in rs])

        entry: Dict[str, Any] = {
            "model": model,
            "prompt_id": prompt_id,
            "n": len(rs),
            "latency_e2e_ms": {
                "median": _median(latencies),
                "p95": _percentile(latencies, 95),
            },
            "estimated_cost_usd": {
                "median": _median(costs),
                "p95": _percentile(costs, 95),
            },
            "tokens": {
                "input_median": _median(input_tokens),
                "output_median": _median(output_tokens),
            },
            "format_ok_rate": format_ok_rate,
        }

        # JSON-only metrics (Prompt C)
        if str(prompt_id).startswith("C_"):
            entry["json_parse_ok_rate"] = _mean_bool([bool(r.get("json_parse_ok", False)) for r in rs])
            entry["schema_ok_rate"] = _mean_bool([bool(r.get("schema_ok", False)) for r in rs])

        by_pair.append(entry)

    # top-level summary
    summary: Dict[str, Any] = {
        "total_runs": len(records),
        "measured_runs": len(measured),
        "excluded_warmup_runs": len(records) - len(measured),
        "by_model_prompt": by_pair,
    }
    return summary


def _format_money(x: float) -> str:
    # keep compact; costs are often small
    if x >= 0.01:
        return f"${x:.4f}"
    if x >= 0.001:
        return f"${x:.5f}"
    return f"${x:.6f}"


def render_summary_md(summary: Dict[str, Any]) -> str:
    """
    Renders a short, human-readable summary in Markdown.
    """
    lines: List[str] = []
    lines.append("# Benchmark Summary")
    lines.append("")
    lines.append(f"- total_runs: {summary.get('total_runs')}")
    lines.append(f"- measured_runs: {summary.get('measured_runs')}")
    lines.append(f"- excluded_warmup_runs: {summary.get('excluded_warmup_runs')}")
    lines.append("")

    lines.append("## Per (model × prompt)")
    lines.append("")
    lines.append("| model | prompt_id | n | latency_median_ms | latency_p95_ms | cost_median | cost_p95 | format_ok_rate | json_parse_ok_rate | schema_ok_rate |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")

    for row in summary.get("by_model_prompt", []):
        model = row["model"]
        prompt_id = row["prompt_id"]
        n = row["n"]

        lat_med = row["latency_e2e_ms"]["median"]
        lat_p95 = row["latency_e2e_ms"]["p95"]

        cost_med = row["estimated_cost_usd"]["median"]
        cost_p95 = row["estimated_cost_usd"]["p95"]

        format_rate = row.get("format_ok_rate", 0.0)

        jpr = row.get("json_parse_ok_rate", "")
        skr = row.get("schema_ok_rate", "")

        def fmt_rate(v: Any) -> str:
            if v == "":
                return ""
            return f"{float(v):.2f}"

        lines.append(
            f"| {model} | {prompt_id} | {n} | "
            f"{lat_med:.0f} | {lat_p95:.0f} | "
            f"{_format_money(float(cost_med))} | {_format_money(float(cost_p95))} | "
            f"{float(format_rate):.2f} | {fmt_rate(jpr)} | {fmt_rate(skr)} |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("- Warm-up runs are excluded from all statistics.")
    lines.append("- p95 uses a nearest-rank method (stable for small N).")
    lines.append("- JSON compliance rates are only applicable to Prompt C.")
    lines.append("")

    return "\n".join(lines)
