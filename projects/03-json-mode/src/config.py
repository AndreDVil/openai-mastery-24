import os
from openai import OpenAI


# Default model used for this project.
DEFAULT_MODEL = "gpt-4.1-mini"


def get_openai_client() -> OpenAI:
    """
    Create and return an OpenAI client using the API key from the environment.

    The environment variable OPENAI_API_KEY must be defined.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("Environment variable OPENAI_API_KEY is not defined.")

    return OpenAI(api_key=api_key)


def get_default_params() -> dict:
    """
    Return the default parameters used for JSON Mode requests in this project.
    """
    return {
        "model": DEFAULT_MODEL,
        # Always force JSON Mode
        "response_format": {"type": "json_object"},
        # Lower temperature for more stable, deterministic outputs
        "temperature": 0.2,
        "top_p": 1.0,
    }
