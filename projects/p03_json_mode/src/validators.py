"""
Strict validators for Project 03 JSON Mode.

No external libraries are used on purpose (learning clarity).
We enforce the StructuredAnswerLite contract strictly:
- required fields present at every level
- no extra fields (additionalProperties is forbidden)
- correct data types
- numeric bounds (confidence)
- enum constraints (task.type)
- exact schema_version
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .schemas import SCHEMA_VERSION, get_structured_answer_lite_schema


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str] = field(default_factory=list)


def _is_non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and len(value.strip()) > 0


def _check_required_keys(obj: Dict[str, Any], required: List[str], path: str, errors: List[str]) -> None:
    for key in required:
        if key not in obj:
            errors.append(f"{path}.{key} is missing")


def _check_no_extra_keys(obj: Dict[str, Any], allowed: List[str], path: str, errors: List[str]) -> None:
    for key in obj.keys():
        if key not in allowed:
            errors.append(f"{path} has unexpected key '{key}'")


def validate_structured_answer_lite(payload: Any) -> ValidationResult:
    """
    Strict validation for StructuredAnswerLite v1.0.

    Contract:
    {
      "task": {"type": "...", "user_intent": "..."},
      "answer": {"text": "..."},
      "quality": {"confidence": 0.0-1.0, "assumptions": [...], "risks": [...]},
      "debug": {"schema_version": "1.0", "model": "..."}
    }
    """
    schema = get_structured_answer_lite_schema()
    errors: List[str] = []

    if not isinstance(payload, dict):
        return ValidationResult(ok=False, errors=["payload must be an object"])

    # --- top-level ---
    top_allowed = list(schema["properties"].keys())
    top_required = schema["required"]

    _check_required_keys(payload, top_required, "payload", errors)
    _check_no_extra_keys(payload, top_allowed, "payload", errors)

    task = payload.get("task")
    answer = payload.get("answer")
    quality = payload.get("quality")
    debug = payload.get("debug")

    # --- task ---
    task_schema = schema["properties"]["task"]
    task_allowed = list(task_schema["properties"].keys())
    task_required = task_schema["required"]
    allowed_task_types = task_schema["properties"]["type"]["enum"]

    if not isinstance(task, dict):
        errors.append("task must be an object")
        task = {}
    _check_required_keys(task, task_required, "task", errors)
    _check_no_extra_keys(task, task_allowed, "task", errors)

    ttype = task.get("type")
    if ttype not in allowed_task_types:
        errors.append(f"task.type must be one of {allowed_task_types}")

    user_intent = task.get("user_intent")
    if not _is_non_empty_str(user_intent):
        errors.append("task.user_intent must be a non-empty string")

    # --- answer ---
    answer_schema = schema["properties"]["answer"]
    answer_allowed = list(answer_schema["properties"].keys())
    answer_required = answer_schema["required"]

    if not isinstance(answer, dict):
        errors.append("answer must be an object")
        answer = {}
    _check_required_keys(answer, answer_required, "answer", errors)
    _check_no_extra_keys(answer, answer_allowed, "answer", errors)

    text = answer.get("text")
    if not _is_non_empty_str(text):
        errors.append("answer.text must be a non-empty string")

    # --- quality ---
    quality_schema = schema["properties"]["quality"]
    quality_allowed = list(quality_schema["properties"].keys())
    quality_required = quality_schema["required"]

    if not isinstance(quality, dict):
        errors.append("quality must be an object")
        quality = {}
    _check_required_keys(quality, quality_required, "quality", errors)
    _check_no_extra_keys(quality, quality_allowed, "quality", errors)

    confidence = quality.get("confidence")
    if not isinstance(confidence, (int, float)):
        errors.append("quality.confidence must be a number")
    else:
        if confidence < 0.0 or confidence > 1.0:
            errors.append("quality.confidence must be between 0.0 and 1.0")

    assumptions = quality.get("assumptions")
    if not isinstance(assumptions, list):
        errors.append("quality.assumptions must be an array")
    else:
        for i, item in enumerate(assumptions):
            if not isinstance(item, str):
                errors.append(f"quality.assumptions[{i}] must be a string")

    risks = quality.get("risks")
    if not isinstance(risks, list):
        errors.append("quality.risks must be an array")
    else:
        for i, item in enumerate(risks):
            if not isinstance(item, str):
                errors.append(f"quality.risks[{i}] must be a string")

    # --- debug ---
    debug_schema = schema["properties"]["debug"]
    debug_allowed = list(debug_schema["properties"].keys())
    debug_required = debug_schema["required"]

    if not isinstance(debug, dict):
        errors.append("debug must be an object")
        debug = {}
    _check_required_keys(debug, debug_required, "debug", errors)
    _check_no_extra_keys(debug, debug_allowed, "debug", errors)

    version = debug.get("schema_version")
    if version != SCHEMA_VERSION:
        errors.append(f"debug.schema_version must be '{SCHEMA_VERSION}'")

    model = debug.get("model")
    if not _is_non_empty_str(model):
        errors.append("debug.model must be a non-empty string")

    return ValidationResult(ok=(len(errors) == 0), errors=errors)
