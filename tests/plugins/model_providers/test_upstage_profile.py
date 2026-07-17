"""Unit tests for the Upstage Solar provider profile.

Upstage Solar is a plain OpenAI-compatible api-key provider, so this verifies
the profile is registered correctly and wires the expected identity, endpoint,
auth, and catalog fields — the contract every downstream layer (auth, models,
doctor, runtime_provider, transport) reads from.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def upstage_profile():
    """Resolve the registered Upstage profile via the provider registry.

    Importing ``model_tools`` triggers plugin discovery, which registers the
    Upstage profile. Going through ``get_provider_profile`` keeps the test
    honest about the actual registration path (name + alias resolution).
    """
    import model_tools  # noqa: F401
    import providers

    profile = providers.get_provider_profile("upstage")
    assert profile is not None, "upstage provider profile must be registered"
    return profile


class TestUpstageProfile:
    def test_identity_and_endpoint(self, upstage_profile):
        assert upstage_profile.name == "upstage"
        assert upstage_profile.api_mode == "chat_completions"
        assert upstage_profile.auth_type == "api_key"
        assert upstage_profile.base_url == "https://api.upstage.ai/v1"
        assert upstage_profile.get_hostname() == "api.upstage.ai"

    def test_solar_alias_resolves(self):
        import model_tools  # noqa: F401
        import providers

        profile = providers.get_provider_profile("solar")
        assert profile is not None, "'solar' alias must resolve to the upstage profile"
        assert profile.name == "upstage"

    def test_api_key_env_var(self, upstage_profile):
        assert "UPSTAGE_API_KEY" in upstage_profile.env_vars

    def test_base_url_env_var_override(self, upstage_profile):
        assert upstage_profile.base_url_env_var == "UPSTAGE_BASE_URL"
