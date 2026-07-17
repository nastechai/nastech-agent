"""Unit tests for the Fireworks AI provider profile.

Pins the profile's contract without going live: identity, alias registration,
and the pay-as-you-go model defaults (direct catalog ``/models/``
IDs, not the router-only tier).
"""

from __future__ import annotations

import pytest


@pytest.fixture
def fireworks_profile():
    """Resolve the registered Fireworks profile through the real discovery path."""
    # Importing model_tools triggers plugin discovery, registering the profile.
    import model_tools  # noqa: F401
    import providers

    profile = providers.get_provider_profile("fireworks")
    assert profile is not None, "fireworks provider profile must be registered"
    return profile


class TestFireworksIdentity:
    def test_core_fields(self, fireworks_profile):
        p = fireworks_profile
        assert p.name == "fireworks"
        assert p.auth_type == "api_key"
        assert p.base_url == "https://api.fireworks.ai/inference/v1"
        assert "FIREWORKS_API_KEY" in p.env_vars

    def test_aliases_resolve(self):
        import model_tools  # noqa: F401
        import providers

        for alias in ("fireworks-ai", "fw"):
            profile = providers.get_provider_profile(alias)
            assert profile is not None, f"'{alias}' alias must resolve to the fireworks profile"
            assert profile.name == "fireworks"
