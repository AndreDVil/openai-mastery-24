from __future__ import annotations

import json
import re
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

from openai import OpenAI

from . import config
from .pricing import get_pricing
from .prompts import Message


# -------------------------
# Time / IDs
# -------------------------

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def utc_now_compact() -> str:
    # e.g. 20251217T014501Z
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def make_run_id(model: str, prompt_id: str, trial_index: int, is_warmup: bool) -> str:
    # Timestamp + short uuid to guarantee uniqueness even in fast loops
    suffix = uuid.uuid4().hex[:8]
    wflag = "w1" if is_warmup else "w0"
    return f"{utc_now_compact()}_{model}_{prompt_id}_t{trial_index}_{wflag}_{suffix}"


# -------------------------
# Format Validators (MVP)
# -------------------------

_SENTENCE_END_RE = re.compile(r"[.!?]+(?:\s|$)")


def validate_prompt_a(output: str) -> bool:
    # Exactly 2 sentences, no newline.
    if "\n" in output:
        return False
    endings = _SENTENCE_END_RE.findall(output.strip())
    return len(endings) == 2


def _is_bullet_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    return s.startswith("- ") or s.startswith("* ") or re.match(r"^\d+\.\s+", s) is not None


def validate_prompt_b(output: str) -> bool:
    # Exactly 8 bullet lines. No non-bullet text.
    lines = [ln for ln in output.splitlines() if ln.strip()]
    if len(lines) != 8:
        return False
    for ln in lines:
        if not _is_bullet_line(ln):
            return False
        text = re.sub(r"^(\- |\* |\d+\.\s+)", "", ln.strip())
        words = [w for w in text.split() if w]
        if len(words) > 12:
            return False
    return True


def _count_words(s: str) -> int:
    return len([w for w in s.strip().split() if w])


def validate_prompt_c_json(output: str) -> Tuple[bool, bool]:
    """
    Returns (json_parse_ok, schema_ok) for Prompt C.

    Schema rules:
      - object with keys: title (str), summary (str), actions (list[str] len=5), risk_level in {low,medium,high}
      - title <= 60 chars
      - summary length 200..260 chars
      - actions: exactly 5 items; each item 8..14 words
    """
    try:
        obj = json.loads(output)
    except Exception:
        return (False, False)

    if not isinstance(obj, dict):
        return (True, False)

    required_keys = {"title", "summary", "actions", "risk_level"}
    if set(obj.keys()) != required_keys:
        return (True, False)

    title = obj.get("title")
    summary = obj.get("summary")
    actions = obj.get("actions")
    risk_level = obj.get("risk_level")

    if not isinstance(title, str) or len(title) > 60:
        return (True, False)

    if not isinstance(summary, str) or not (200 <= len(summary) <= 260):
        return (True, False)

    if not isinstance(actions, list) or len(actions) != 5:
        return (True, False)

    for a in actions:
        if not isinstance(a, str):
            return (True, False)
        wc = _count_words(a)
        if wc < 8 or wc > 14:
            return (True, False)

    if risk_level not in {"low", "medium", "high"}:
        return (True, False)

    return (True, True)


def evaluate_compliance(prompt_id: str, output_text: str) -> Dict[str, Any]:
    """
    Returns compliance fields:
      - format_ok (bool)
      - json_parse_ok (bool, only for C)
      - schema_ok (bool, only for C)
    """
    if prompt_id.startswith("A_"):
        return {"format_ok": validate_prompt_a(output_text)}
    if prompt_id.startswith("B_"):
        return {"format_ok": validate_prompt_b(output_text)}
    if prompt_id.startswith("C_"):
        json_parse_ok, schema_ok = validate_prompt_c_json(output_text)
        return {
            "format_ok": bool(json_parse_ok and schema_ok),
            "json_parse_ok": json_parse_ok,
            "schema_ok": schema_ok,
        }
    return {"format_ok": False}


# -------------------------
# Single Run Measurement
# -------------------------

def _extract_output_text(resp: Any) -> str:
    """
    MVP output extractor: first choice only.
    Defensive against non-string content representations.
    """
    try:
        msg = resp.choices[0].message
        content = getattr(msg, "content", None)

        if isinstance(content, str):
            return content
        if content is None:
            return ""
        return str(content)
    except Exception:
        return ""


def _max_tokens_param_for_model(model: str) -> str:
    """
    Returns the correct max-tokens parameter name for the given model,
    using config.MODEL_CAPABILITIES.

    Expected config structure:
      MODEL_CAPABILITIES = {
        "gpt-4.1": {"max_tokens_param": "max_tokens"},
        "gpt-5.2": {"max_tokens_param": "max_completion_tokens"},
      }
    """
    caps = getattr(config, "MODEL_CAPABILITIES", {})
    if isinstance(caps, dict) and model in caps and isinstance(caps[model], dict):
        param = caps[model].get("max_tokens_param")
        if param in {"max_tokens", "max_completion_tokens"}:
            return param
    # safe default for many chat models
    return "max_tokens"


def run_once(
    *,
    client: OpenAI,
    model: str,
    prompt_id: str,
    messages: list[Message],
    trial_index: int,
    is_warmup: bool,
    temperature: float,
    top_p: float,
    max_tokens: int,
    pricing_label: str,
) -> Dict[str, Any]:
    """
    Executes a single Chat Completions call and returns a run record dict
    conforming to measurement_spec.md.
    """
    run_id = make_run_id(model=model, prompt_id=prompt_id, trial_index=trial_index, is_warmup=is_warmup)
    timestamp_utc = utc_now_iso()

    pricing = get_pricing(model)
    input_rate = pricing.input_rate_per_million
    output_rate = pricing.output_rate_per_million

    start = time.perf_counter()

    status = "ok"
    error_type: Optional[str] = None
    error_message: Optional[str] = None

    output_text = ""
    input_tokens = 0
    output_tokens = 0
    total_tokens = 0

    max_tokens_param = _max_tokens_param_for_model(model)

    try:
        params: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
        }
        params[max_tokens_param] = max_tokens

        resp = client.chat.completions.create(**params)

        output_text = _extract_output_text(resp)

        if resp.usage is not None:
            input_tokens = int(getattr(resp.usage, "prompt_tokens", 0) or 0)
            output_tokens = int(getattr(resp.usage, "completion_tokens", 0) or 0)
            total_tokens = int(getattr(resp.usage, "total_tokens", 0) or 0)

        if total_tokens == 0:
            total_tokens = input_tokens + output_tokens

        # Optional diagnostics (kept minimal): if output is empty but status ok
        if not output_text.strip():
            # Don’t flip status to error; just mark as suspicious
            error_type = "empty_output"
            error_message = f"Empty output_text extracted (max_tokens_param={max_tokens_param})."

    except Exception as e:
        status = "error"
        error_type = e.__class__.__name__
        error_message = str(e)[:300]

    end = time.perf_counter()
    latency_e2e_ms = int(round((end - start) * 1000))

    output_chars = len(output_text) if output_text else 0
    compliance = evaluate_compliance(prompt_id=prompt_id, output_text=output_text)

    estimated_cost_usd = ((input_tokens * input_rate) + (output_tokens * output_rate)) / 1_000_000

    record: Dict[str, Any] = {
        # Identity
        "run_id": run_id,
        "timestamp_utc": timestamp_utc,
        "model": model,
        "prompt_id": prompt_id,
        "trial_index": int(trial_index),
        "is_warmup": bool(is_warmup),

        # Request params (experiment budget)
        "temperature": float(temperature),
        "top_p": float(top_p),
        "max_tokens": int(max_tokens),

        # Latency
        "latency_e2e_ms": int(latency_e2e_ms),

        # Token usage
        "input_tokens": int(input_tokens),
        "output_tokens": int(output_tokens),
        "total_tokens": int(total_tokens),

        # Pricing / Cost
        "pricing_label": str(pricing_label),
        "input_rate_per_million": float(input_rate),
        "output_rate_per_million": float(output_rate),
        "estimated_cost_usd": float(estimated_cost_usd),

        # Output observables
        "output_chars": int(output_chars),

        # Compliance
        "format_ok": bool(compliance.get("format_ok", False)),

        # Error handling
        "status": status,
        "error_type": error_type,
        "error_message": error_message,
    }

    if prompt_id.startswith("C_"):
        record["json_parse_ok"] = bool(compliance.get("json_parse_ok", False))
        record["schema_ok"] = bool(compliance.get("schema_ok", False))

    return record
