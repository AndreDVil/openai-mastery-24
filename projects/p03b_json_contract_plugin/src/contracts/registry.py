from typing import Dict

from .base import Contract
from .structured_answer_lite import StructuredAnswerLiteContract

_REGISTRY: Dict[str, Contract] = {
    "structured_answer_lite": StructuredAnswerLiteContract(),
}

def get_contract(name: str) -> Contract:
    if name not in _REGISTRY:
        raise ValueError(f"Unknown contract: {name}")
    return _REGISTRY[name]
