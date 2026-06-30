"""Tests for credential_pool .env fallback and auth credential_pool lookup.

Covers the fix from #15914 / PR #15920 and the rotation fix from #20591:
- _seed_from_env reads API keys from ~/.nastech/.env when not in os.environ
- _resolve_api_key_provider_secret falls back to credential_pool when env vars are empty
- ~/.nastech/.env takes priority over os.environ for Nastech-managed credentials
  (so a deliberate rotation in .env wins over a stale shell export)
- env / dotenv values take priority over credential pool (pool fires only when both are empty)
"""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


def _make_pconfig(provider_id="deepseek", env_vars=None):
    """Create a minimal ProviderConfig for testing.

    Default provider_id is 'deepseek' because it's a real api_key provider
    in PROVIDER_REGISTRY (needed for _seed_from_env's generic path).
    """
    from nastech_cli.auth import ProviderConfig
    return ProviderConfig(
        id=provider_id,
        name=provider_id.title(),
        auth_type="api_key",
        api_key_env_vars=tuple(env_vars or [f"{provider_id.upper()}_API_KEY"]),
    )


@pytest.fixture
def isolated_nastech_home(tmp_path, monkeypatch):
    """Point NASTECH_HOME at a temp dir and clear known API key env vars.

    Also invalidates any cached get_env_value state by patching Path.home().
    """
    home = tmp_path / ".nastech"
    home.mkdir()
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setenv("NASTECH_HOME", str(home))

    # Clear all known API key env vars so get_env_value falls through to .env
    for key in [
        "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "OPENROUTER_API_KEY",
        "ZAI_API_KEY", "DEEPSEEK_API_KEY", "ANTHROPIC_TOKEN",
        "CLAUDE_CODE_OAUTH_TOKEN", "OPENAI_BASE_URL",
    ]:
        monkeypatch.delenv(key, raising=False)

    return home


def _write_env_file(home: Path, **kwargs) -> None:
    """Write key=value pairs to ~/.nastech/.env."""
    lines = [f"{k}={v}" for k, v in kwargs.items()]
    (home / ".env").write_text("\n".join(lines) + "\n")


class TestCredentialPoolSeedsFromDotEnv:
    """_seed_from_env must read keys from ~/.nastech/.env, not just os.environ.

    This is the load-bearing behaviour for the fix: when a user adds a key to
    .env mid-session or via a non-CLI entry point that doesn't run
    load_nastech_dotenv, the credential pool must still discover it.
    """

    def test_deepseek_key_from_dotenv_only(self, isolated_nastech_home):
        """Key in .env but not os.environ → _seed_from_env adds a pool entry."""
        _write_env_file(isolated_nastech_home, DEEPSEEK_API_KEY="sk-dotenv-only-12345")
        assert "DEEPSEEK_API_KEY" not in os.environ

        from agent.credential_pool import _seed_from_env
        entries = []
        changed, active_sources = _seed_from_env("deepseek", entries)

        assert changed is True
        assert "env:DEEPSEEK_API_KEY" in active_sources
        assert any(
            e.access_token == "sk-dotenv-only-12345"
            and e.source == "env:DEEPSEEK_API_KEY"
            for e in entries
        ), f"Expected seeded entry with dotenv key, got: {[(e.source, e.access_token) for e in entries]}"

    def test_openrouter_key_from_dotenv_only(self, isolated_nastech_home):
        """OpenRouter path has its own branch — verify it also reads .env."""
        _write_env_file(isolated_nastech_home, OPENROUTER_API_KEY="sk-or-dotenv-abc")
        assert "OPENROUTER_API_KEY" not in os.environ

        from agent.credential_pool import _seed_from_env
        entries = []
        changed, active_sources = _seed_from_env("openrouter", entries)

        assert changed is True
        assert "env:OPENROUTER_API_KEY" in active_sources
        assert any(
            e.access_token == "sk-or-dotenv-abc" for e in entries
        )

    def test_empty_dotenv_no_entries(self, isolated_nastech_home):
        """No .env file, no env vars → no entries seeded (and no crash)."""
        from agent.credential_pool import _seed_from_env
        entries = []
        changed, active_sources = _seed_from_env("deepseek", entries)
        assert changed is False
        assert active_sources == set()
        assert entries == []

    def test_dotenv_wins_over_stale_os_environ(self, isolated_nastech_home, monkeypatch):
        """Regression for #20591: a fresh key rotated into ~/.nastech/.env must
        win over a stale value inherited from os.environ (parent shell export
        from Codex CLI, test runner, login profile, etc.). Without this, key
        rotation produces persistent 401s.
        """
        _write_env_file(isolated_nastech_home, DEEPSEEK_API_KEY="sk-dotenv-fresh")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-env-stale-xyz")

        from agent.credential_pool import _seed_from_env
        entries = []
        changed, _ = _seed_from_env("deepseek", entries)

        assert changed is True
        seeded = [e for e in entries if e.source == "env:DEEPSEEK_API_KEY"]
        assert len(seeded) == 1
        assert seeded[0].access_token == "sk-dotenv-fresh"


class TestAuthResolvesFromDotEnv:
    """_resolve_api_key_provider_secret must also read from ~/.nastech/.env."""

    def test_key_from_dotenv_only(self, isolated_nastech_home):
        """Key in .env but not os.environ → _resolve returns it with the env var source."""
        _write_env_file(isolated_nastech_home, DEEPSEEK_API_KEY="sk-dotenv-resolve-789")
        assert "DEEPSEEK_API_KEY" not in os.environ

        from nastech_cli.auth import _resolve_api_key_provider_secret
        key, source = _resolve_api_key_provider_secret(
            provider_id="deepseek",
            pconfig=_make_pconfig(),
        )
        assert key == "sk-dotenv-resolve-789"
        assert source == "DEEPSEEK_API_KEY"

    def test_dotenv_wins_over_stale_os_environ_on_resolve(
        self, isolated_nastech_home, monkeypatch
    ):
        """Regression for #20591: when both ~/.nastech/.env and os.environ define
        the key, the .env value wins. Symmetric with the pool seeding rule —
        without this, the pool gets re-seeded with the fresh .env key while the
        live request path keeps returning the stale shell export, producing
        persistent 401s after rotation.
        """
        _write_env_file(isolated_nastech_home, DEEPSEEK_API_KEY="dotenv-fresh-deepseek")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "stale-shell-deepseek")

        from nastech_cli.auth import _resolve_api_key_provider_secret
        key, source = _resolve_api_key_provider_secret(
            provider_id="deepseek",
            pconfig=_make_pconfig(),
        )
        assert key == "dotenv-fresh-deepseek"
        assert source == "DEEPSEEK_API_KEY"

    def test_get_anthropic_key_prefers_dotenv_over_stale_os_environ(
        self, isolated_nastech_home, monkeypatch
    ):
        """Regression for #20591 (sibling site): get_anthropic_key() must also
        prefer ~/.nastech/.env over a stale shell export. This path resolves
        ANTHROPIC_API_KEY/ANTHROPIC_TOKEN/CLAUDE_CODE_OAUTH_TOKEN and had the
        identical os.environ-first rotation bug that the api-key resolution
        path did, just for Anthropic.
        """
        _write_env_file(isolated_nastech_home, ANTHROPIC_API_KEY="dotenv-fresh-anthropic")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "stale-shell-anthropic")

        from nastech_cli.auth import get_anthropic_key
        assert get_anthropic_key() == "dotenv-fresh-anthropic"


class TestAuthCredentialPoolFallback:
    """_resolve_api_key_provider_secret falls back to credential pool when env + dotenv are empty."""

    def test_credential_pool_fallback_structure(self, isolated_nastech_home):
        """Empty env + empty .env → auth falls back to credential pool."""
        mock_entry = MagicMock()
        mock_entry.access_token = "test-pool-key-12345"
        mock_entry.runtime_api_key = ""

        mock_pool = MagicMock()
        mock_pool.has_credentials.return_value = True
        mock_pool.peek.return_value = mock_entry

        from nastech_cli.auth import _resolve_api_key_provider_secret
        with patch("agent.credential_pool.load_pool", return_value=mock_pool):
            key, source = _resolve_api_key_provider_secret(
                provider_id="deepseek",
                pconfig=_make_pconfig(),
            )
        assert "test-pool-key-12345" in key
        assert "credential_pool" in source

    def test_credential_pool_empty_returns_empty(self, isolated_nastech_home):
        """Empty env + empty .env + empty pool → empty string."""
        mock_pool = MagicMock()
        mock_pool.has_credentials.return_value = False

        from nastech_cli.auth import _resolve_api_key_provider_secret
        with patch("agent.credential_pool.load_pool", return_value=mock_pool):
            key, source = _resolve_api_key_provider_secret(
                provider_id="deepseek",
                pconfig=_make_pconfig(),
            )
        assert key == ""

    def test_env_var_takes_priority_over_pool(self, isolated_nastech_home, monkeypatch):
        """os.environ key wins — credential pool is NEVER consulted."""
        monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-env-key-first-abc123")

        mock_pool = MagicMock()
        mock_pool.has_credentials.return_value = True

        from nastech_cli.auth import _resolve_api_key_provider_secret
        with patch("agent.credential_pool.load_pool", return_value=mock_pool) as mp:
            key, source = _resolve_api_key_provider_secret(
                provider_id="deepseek",
                pconfig=_make_pconfig(),
            )
        assert key == "sk-env-key-first-abc123"
        assert source == "DEEPSEEK_API_KEY"
        # Pool should not even have been loaded — env var satisfied the request first
        mp.assert_not_called()

    def test_dotenv_takes_priority_over_pool(self, isolated_nastech_home):
        """Key in .env beats credential pool — pool only fires when both env sources are empty."""
        _write_env_file(isolated_nastech_home, DEEPSEEK_API_KEY="sk-dotenv-priority-xyz")
        assert "DEEPSEEK_API_KEY" not in os.environ

        mock_pool = MagicMock()
        mock_pool.has_credentials.return_value = True

        from nastech_cli.auth import _resolve_api_key_provider_secret
        with patch("agent.credential_pool.load_pool", return_value=mock_pool) as mp:
            key, source = _resolve_api_key_provider_secret(
                provider_id="deepseek",
                pconfig=_make_pconfig(),
            )
        assert key == "sk-dotenv-priority-xyz"
        assert source == "DEEPSEEK_API_KEY"
        mp.assert_not_called()
