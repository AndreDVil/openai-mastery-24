from __future__ import annotations

import json
import os
from typing import Any, Dict


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def append_jsonl(path: str, record: Dict[str, Any]) -> None:
    """
    Appends a single JSON record as one line (JSONL).
    Writes are flushed to reduce loss on interruptions.
    """
    ensure_dir(os.path.dirname(path) or ".")
    line = json.dumps(record, ensure_ascii=False)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
        f.flush()


def write_json(path: str, obj: Any) -> None:
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def write_text(path: str, text: str) -> None:
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")
