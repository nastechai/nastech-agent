"""Tests for the Nastechai-Nastech-3/4 non-agentic warning detector.

Prior to this check, the warning fired on any model whose name contained
``"nastech"`` anywhere (case-insensitive). That false-positived on unrelated
local Modelfiles such as ``nastech-brain:qwen3-14b-ctx16k`` — a tool-capable
Qwen3 wrapper that happens to live under the "nastech" tag namespace.

``is_nastechai_nastech_non_agentic`` should only match the actual Nastechai Research
Nastech-3 / Nastech-4 chat family.
"""

from __future__ import annotations

import pytest

from nastech_cli.model_switch import (
    _NASTECH_MODEL_WARNING,
    _check_nastech_model_warning,
    is_nastechai_nastech_non_agentic,
)


@pytest.mark.parametrize(
    "model_name",
    [
        "NastechaiResearch/Nastech-3-Llama-3.1-70B",
        "NastechaiResearch/Nastech-3-Llama-3.1-405B",
        "nastech-3",
        "Nastech-3",
        "nastech-4",
        "nastech-4-405b",
        "nastech_4_70b",
        "openrouter/nastech3:70b",
        "openrouter/nastechairesearch/nastech-4-405b",
        "NastechaiResearch/Nastech3",
        "nastech-3.1",
    ],
)
def test_matches_real_nastechai_nastech_chat_models(model_name: str) -> None:
    assert is_nastechai_nastech_non_agentic(model_name), (
        f"expected {model_name!r} to be flagged as Nastechai Nastech 3/4"
    )
    assert _check_nastech_model_warning(model_name) == _NASTECH_MODEL_WARNING


@pytest.mark.parametrize(
    "model_name",
    [
        # Kyle's local Modelfile — qwen3:14b under a custom tag
        "nastech-brain:qwen3-14b-ctx16k",
        "nastech-brain:qwen3-14b-ctx32k",
        "nastech-honcho:qwen3-8b-ctx8k",
        # Plain unrelated models
        "qwen3:14b",
        "qwen3-coder:30b",
        "qwen2.5:14b",
        "claude-opus-4-6",
        "anthropic/claude-sonnet-4.5",
        "gpt-5",
        "openai/gpt-4o",
        "google/gemini-2.5-flash",
        "deepseek-chat",
        # Non-chat Nastech models we don't warn about
        "nastech-llm-2",
        "nastech2-pro",
        "nastechai-nastech-2-mistral",
        # Edge cases
        "",
        "nastech",  # bare "nastech" isn't the 3/4 family
        "nastech-brain",
        "brain-nastech-3-impostor",  # "3" not preceded by /: boundary
    ],
)
def test_does_not_match_unrelated_models(model_name: str) -> None:
    assert not is_nastechai_nastech_non_agentic(model_name), (
        f"expected {model_name!r} NOT to be flagged as Nastechai Nastech 3/4"
    )
    assert _check_nastech_model_warning(model_name) == ""


def test_none_like_inputs_are_safe() -> None:
    assert is_nastechai_nastech_non_agentic("") is False
    # Defensive: the helper shouldn't crash on None-ish falsy input either.
    assert _check_nastech_model_warning("") == ""
