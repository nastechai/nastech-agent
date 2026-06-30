"""Nastechai Portal provider profile."""

from typing import Any

from agent.portal_tags import nastechai_portal_tags
from providers import register_provider
from providers.base import ProviderProfile


class NastechaiProfile(ProviderProfile):
    """Nastechai Portal — product tags, reasoning with Nastechai-specific omission."""

    def build_extra_body(
        self, *, session_id: str | None = None, **context
    ) -> dict[str, Any]:
        return {"tags": nastechai_portal_tags()}

    def build_api_kwargs_extras(
        self,
        *,
        reasoning_config: dict | None = None,
        supports_reasoning: bool = False,
        **context,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Nastechai: passes full reasoning_config, but OMITS when disabled."""
        extra_body = {}
        if supports_reasoning:
            if reasoning_config is not None:
                rc = dict(reasoning_config)
                if rc.get("enabled") is False:
                    pass  # Nastechai omits reasoning when disabled
                else:
                    extra_body["reasoning"] = rc
            else:
                extra_body["reasoning"] = {"enabled": True, "effort": "medium"}
        return extra_body, {}


nastechai = NastechaiProfile(
    name="nastechai",
    aliases=("nastechai-portal", "nastechairesearch"),
    env_vars=("NASTECHAI_API_KEY",),
    display_name="Nastechai Research",
    description="Nastechai Research — Nastech model family",
    signup_url="https://nastechairesearch.com/",
    fallback_models=(
        "nastech-3-405b",
        "nastech-3-70b",
    ),
    base_url="https://inference.nastechairesearch.com/v1",
    auth_type="oauth_device_code",
)

register_provider(nastechai)
