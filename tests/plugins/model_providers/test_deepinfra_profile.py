"""Unit tests for the DeepInfra provider profile.

DeepInfra is an OpenAI-compatible multi-model provider. This verifies the
profile is registered correctly with the right endpoint, auth type, and
alias resolution.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def deepinfra_profile():
    """Resolve the registered DeepInfra profile through the real discovery path."""
    import model_tools  # noqa: F401
    import providers

    profile = providers.get_provider_profile("deepinfra")
    assert profile is not None, "deepinfra provider profile must be registered"
    return profile


class TestDeepInfraProfile:
    def test_core_fields(self, deepinfra_profile):
        p = deepinfra_profile
        assert p.name == "deepinfra"
        assert p.auth_type == "api_key"
        assert p.base_url == "https://api.deepinfra.com/v1/openai"
        assert "DEEPINFRA_API_KEY" in p.env_vars

    def test_base_url_env_var_override(self, deepinfra_profile):
        assert deepinfra_profile.base_url_env_var == "DEEPINFRA_BASE_URL"

    def test_aliases_resolve(self):
        import model_tools  # noqa: F401
        import providers

        for alias in ("deep-infra", "deepinfra-ai"):
            profile = providers.get_provider_profile(alias)
            assert profile is not None, f"'{alias}' alias must resolve to the deepinfra profile"
            assert profile.name == "deepinfra"
