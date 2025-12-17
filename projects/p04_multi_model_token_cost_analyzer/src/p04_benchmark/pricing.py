from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Pricing:
    """
    Pricing defines the USD cost per 1M tokens for a model.
    Rates are intentionally static to ensure reproducibility.
    """
    input_rate_per_million: float
    output_rate_per_million: float


# Pricing table used for the MVP benchmark.
# IMPORTANT:
# - Values are estimates for educational comparison.
# - Any change here MUST update the pricing_label in config.py.
PRICING_TABLE: Dict[str, Pricing] = {
    "gpt-5.2": Pricing(
        input_rate_per_million=3.00,
        output_rate_per_million=12.00,
    ),
    "gpt-4.1": Pricing(
        input_rate_per_million=1.50,
        output_rate_per_million=6.00,
    ),
    "gpt-4.1-nano": Pricing(
        input_rate_per_million=0.60,
        output_rate_per_million=2.40,
    ),
}


def get_pricing(model: str) -> Pricing:
    """
    Returns pricing information for a given model.

    Raises:
        KeyError if the model is not defined in the pricing table.
    """
    if model not in PRICING_TABLE:
        raise KeyError(f"Pricing not defined for model: {model}")
    return PRICING_TABLE[model]
