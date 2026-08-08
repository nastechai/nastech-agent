"""Tests for the NasTechai-NasTech-3/4 non-agentic warning detector.

Prior to this check, the warning fired on any model whose name contained
``"nastech"`` anywhere (case-insensitive). That false-positived on unrelated
local Modelfiles such as ``nastech-brain:qwen3-14b-ctx16k`` — a tool-capable
Qwen3 wrapper that happens to live under the "nastech" tag namespace.

``is_nous_nastech_non_agentic`` should only match the actual Nastechai Research
NasTech-3 / NasTech-4 chat family.
"""

from __future__ import annotations

import pytest

from nastech_cli.model_switch import (
    _NASTECH_MODEL_WARNING,
    _check_nastech_model_warning,
    is_nous_nastech_non_agentic,
)


@pytest.mark.parametrize(
    "model_name",
    [
        "NasTechaiResearch/NasTech-3-Llama-3.1-70B",
        "NasTechaiResearch/NasTech-3-Llama-3.1-405B",
        "nastech-3",
        "NasTech-3",
        "nastech-4",
        "nastech-4-405b",
        "nastech_4_70b",
        "openrouter/nastech3:70b",
        "openrouter/nousresearch/nastech-4-405b",
        "NasTechaiResearch/NasTech3",
        "nastech-3.1",
    ],
)
def test_matches_real_nous_nastech_chat_models(model_name: str) -> None:
    assert is_nous_nastech_non_agentic(model_name), (
        f"expected {model_name!r} to be flagged as NasTechai NasTech 3/4"
    )
    assert _check_nastech_model_warning(model_name) == _NASTECH_MODEL_WARNING


