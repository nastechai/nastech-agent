"""Tests for agent.portal_tags — Nastechai Portal request tag contract."""

from __future__ import annotations


def test_nastech_client_tag_includes_current_version():
    """The client tag must reflect nastech_cli.__version__ verbatim."""
    from nastech_cli import __version__
    from agent.portal_tags import nastech_client_tag

    assert nastech_client_tag() == f"client=nastech-client-v{__version__}"


def test_nastech_client_tag_format():
    """The client tag has the exact shape Nastechai Portal expects."""
    from agent.portal_tags import nastech_client_tag

    tag = nastech_client_tag()
    assert tag.startswith("client=nastech-client-v")
    # No spaces, no commas — single tag value
    assert " " not in tag
    assert "," not in tag


def test_nastechai_portal_tags_contains_product_and_client():
    """Every Nastechai Portal request gets BOTH the product tag and the version tag."""
    from agent.portal_tags import nastech_client_tag, nastechai_portal_tags

    tags = nastechai_portal_tags()
    assert "product=nastech-agent" in tags
    assert nastech_client_tag() in tags
    assert len(tags) == 2


def test_nastechai_portal_tags_returns_fresh_list():
    """Callers mutate the returned list; we must not share state across calls."""
    from agent.portal_tags import nastechai_portal_tags

    a = nastechai_portal_tags()
    a.append("client=test-mutation")
    b = nastechai_portal_tags()
    assert "client=test-mutation" not in b


def test_auxiliary_client_nastechai_extra_body_uses_helper():
    """auxiliary_client.NASTECHAI_EXTRA_BODY must match the canonical helper output."""
    from agent.auxiliary_client import NASTECHAI_EXTRA_BODY
    from agent.portal_tags import nastechai_portal_tags

    assert NASTECHAI_EXTRA_BODY == {"tags": nastechai_portal_tags()}


def test_nastechai_provider_profile_uses_helper():
    """The Nastechai provider profile (main agent loop) must use the canonical tags."""
    from agent.portal_tags import nastechai_portal_tags
    from providers import get_provider_profile

    profile = get_provider_profile("nastechai")
    assert profile is not None
    body = profile.build_extra_body()
    assert body["tags"] == nastechai_portal_tags()
