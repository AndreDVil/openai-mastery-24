from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal, TypedDict


# We keep the message schema compatible with OpenAI Chat Completions:
# {"role": "...", "content": "..."}
Role = Literal["system", "user", "assistant"]


class Message(TypedDict):
    role: Role
    content: str


@dataclass(frozen=True)
class PromptSpec:
    """
    PromptSpec is a versioned prompt bundle referenced by prompt_id.
    It stores the exact messages we send to the API for reproducibility.
    """
    prompt_id: str
    messages: List[Message]


def get_prompts() -> Dict[str, PromptSpec]:
    """
    Returns a dictionary keyed by prompt_id.

    Prompts are treated as data, not embedded in benchmark logic, so that:
    - prompt changes are explicit (via prompt_id version bump)
    - runs remain reproducible
    """
    prompts: List[PromptSpec] = [
        PromptSpec(
            prompt_id="A_short_objective_v1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente direto e objetivo. "
                        "Siga as restrições do usuário exatamente."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Explique o que é “overfitting” em machine learning.\n\n"
                        "Restrições obrigatórias:\n"
                        "- Responda em exatamente 2 frases.\n"
                        "- Não use listas, bullets, nem quebras de linha.\n"
                        "- Não use analogias.\n"
                        "- Use linguagem simples, como se fosse para alguém inteligente mas iniciante."
                    ),
                },
            ],
        ),
        PromptSpec(
            prompt_id="B_mid_bullets_v1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente técnico e conciso. "
                        "Siga as restrições do usuário exatamente."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Dê um plano de ação para detectar e reduzir anomalias "
                        "em um portfólio de crédito ao consumidor usando machine learning.\n\n"
                        "Restrições obrigatórias:\n"
                        "- Responda em 8 bullets, exatamente.\n"
                        "- Cada bullet deve ter no máximo 12 palavras.\n"
                        "- Não use sub-bullets.\n"
                        "- Não use texto fora dos bullets.\n"
                        "- Não mencione bibliotecas específicas (sklearn, xgboost, etc.)."
                    ),
                },
            ],
        ),
        PromptSpec(
            prompt_id="C_json_strict_v1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um gerador de JSON estrito. "
                        "Retorne apenas JSON válido. Sem texto extra."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Crie um JSON com recomendações para melhorar a disciplina de estudos em 7 dias.\n\n"
                        "Regras obrigatórias:\n"
                        "- Retorne APENAS um objeto JSON (sem markdown, sem texto fora do JSON).\n"
                        "- O objeto JSON deve seguir exatamente este schema:\n\n"
                        '{\n'
                        '  "title": string,\n'
                        '  "summary": string,\n'
                        '  "actions": array de 5 strings,\n'
                        '  "risk_level": "low" | "medium" | "high"\n'
                        '}\n\n'
                        "Restrições adicionais:\n"
                        '- "title" deve ter no máximo 60 caracteres.\n'
                        '- "summary" deve ter entre 200 e 260 caracteres.\n'
                        '- "actions" deve ter exatamente 5 itens, cada string com 8 a 14 palavras.\n'
                        '- "risk_level" deve ser "low", "medium" ou "high".'
                    ),
                },
            ],
        ),
    ]

    return {p.prompt_id: p for p in prompts}


def get_prompt(prompt_id: str) -> PromptSpec:
    prompts = get_prompts()
    if prompt_id not in prompts:
        raise KeyError(f"Unknown prompt_id: {prompt_id}")
    return prompts[prompt_id]
