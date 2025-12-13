# src/schemas.py

from __future__ import annotations

from typing import Any, Dict


SCHEMA_VERSION = "1.0"

# -----------------------------
# v1.0 — StructuredAnswerLite
# -----------------------------
STRUCTURED_ANSWER_LITE_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "StructuredAnswerLite",
    "type": "object",
    "additionalProperties": False,
    "required": ["task", "answer", "quality", "debug"],
    "properties": {
        "task": {
            "type": "object",
            "additionalProperties": False,
            "required": ["type", "user_intent"],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["qa", "extraction", "classification", "summarization", "other"],
                },
                "user_intent": {"type": "string", "minLength": 1},
            },
        },
        "answer": {
            "type": "object",
            "additionalProperties": False,
            "required": ["text"],
            "properties": {
                "text": {"type": "string", "minLength": 1},
            },
        },
        "quality": {
            "type": "object",
            "additionalProperties": False,
            "required": ["confidence", "assumptions", "risks"],
            "properties": {
                "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "assumptions": {"type": "array", "items": {"type": "string"}},
                "risks": {"type": "array", "items": {"type": "string"}},
            },
        },
        "debug": {
            "type": "object",
            "additionalProperties": False,
            "required": ["schema_version", "model"],
            "properties": {
                "schema_version": {"type": "string", "const": SCHEMA_VERSION},
                "model": {"type": "string", "minLength": 1},
            },
        },
    },
}

# -----------------------------
# v1.0 — StructuredAnswer (Full)
# (kept as future improvement)
# -----------------------------
STRUCTURED_ANSWER_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "StructuredAnswer",
    "type": "object",
    "additionalProperties": False,
    "required": ["task", "answer", "quality", "debug"],
    "properties": {
        "task": {
            "type": "object",
            "additionalProperties": False,
            "required": ["type", "user_intent"],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["qa", "extraction", "classification", "summarization", "other"],
                },
                "user_intent": {"type": "string", "minLength": 1},
            },
        },
        "answer": {
            "type": "object",
            "additionalProperties": False,
            "required": ["text", "bullets", "next_actions"],
            "properties": {
                "text": {"type": "string", "minLength": 1},
                "bullets": {"type": "array", "items": {"type": "string"}},
                "next_actions": {"type": "array", "items": {"type": "string"}},
            },
        },
        "quality": {
            "type": "object",
            "additionalProperties": False,
            "required": ["confidence", "assumptions", "risks"],
            "properties": {
                "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "assumptions": {"type": "array", "items": {"type": "string"}},
                "risks": {"type": "array", "items": {"type": "string"}},
            },
        },
        "debug": {
            "type": "object",
            "additionalProperties": False,
            "required": ["schema_version", "model"],
            "properties": {
                "schema_version": {"type": "string", "const": SCHEMA_VERSION},
                "model": {"type": "string", "minLength": 1},
            },
        },
    },
}


def get_structured_answer_lite_schema() -> Dict[str, Any]:
    """
    Return the JSON Schema for the StructuredAnswerLite contract (v1.0).

    This should be the default contract used in Project 03 to keep the first
    implementation simple, while still enforcing strong structure guarantees.
    """
    return STRUCTURED_ANSWER_LITE_SCHEMA


def get_structured_answer_schema() -> Dict[str, Any]:
    """
    Return the JSON Schema for the full StructuredAnswer contract (v1.0).

    This is kept for future upgrades after the initial implementation is stable.
    """
    return STRUCTURED_ANSWER_SCHEMA
