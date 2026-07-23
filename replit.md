# Nastech Agent — Project Overview & Branding Plan

## What This Project Is

**Nastech Agent** is a rebranded fork of [Hermes Agent](https://github.com/NousResearch/hermes-agent) by NousResearch.  
It is a self-improving AI agent CLI/TUI/web tool built by **Nastechai Research**.

- **GitHub**: https://github.com/nastechai/nastech-agent  
- **Website**: https://nastech-agent.nastechairesearch.com  
- **Docs**: https://nastech-agent.nastechairesearch.com/docs  
- **Discord**: https://discord.gg/nastechai  
- **Portal**: https://portal.nastechairesearch.com  
- **CLI command**: `nastech`  
- **Config dir**: `~/.nastech`  
- **Python package**: `nastech-agent`

---

## User Preferences

- All branding must match Hermes Agent's structure exactly, with Nastech substitutions applied consistently.
- Do not restructure or migrate the project — maintain existing stack.

---

## Current Version Status

| | Nastech (this repo) | Hermes (upstream) |
|---|---|---|
| **Version** | `0.18.0` | `0.19.0` |
| **Release name** | The Judgment Release | The Quicksilver Release |
| **Release date** | July 1, 2026 | July 20, 2026 |
| **Behind by** | 3 releases | — (latest) |

---

## Full Hermes Version History (All Releases)

All releases below are from the upstream Hermes Agent repo. Nastech should track these, rebrand them, and keep in sync.

| Version | Date | Name | Key Features |
|---------|------|------|--------------|
| **v0.19.0** | 2026.7.20 | The Quicksilver Release | ~80% faster first-token on all platforms; reasoning streams live by default; 14× faster desktop streaming markdown; Bitwarden & 1Password integration; smart approvals by default; live subagent monitoring; durable delivery ledger (survives gateway crash); subscription management in terminal; TUI incremental markdown |
| v0.18.2 | 2026.7.7.2 | Infrastructure patch | Infra patch on top of v0.18.1 |
| v0.18.1 | 2026.7.7 | Infrastructure patch | 667 commits: installer/updater self-healing on Windows, dashboard & gateway fixes, WhatsApp dashboard pairing, MCP/provider fixes, stability work |
| **v0.18.0** ← *Nastech is here* | 2026.7.1 | The Judgment Release | ~1,720 commits, 998 PRs, 949 issues closed, 370+ contributors |
| v0.17.0 | 2026.6.19 | — | Feature release |
| v0.16.0 | 2026.6.5 | The Surface Release | Feature release |
| v0.15.2 | 2026.5.29.2 | Patch | — |
| v0.15.1 | 2026.5.29 | Patch | — |
| v0.15.0 | 2026.5.28 | The Velocity Release | Dramatically faster agent; 1,302 commits, 747 PRs, 321 contributors |
| v0.14.0 | 2026.5.16 | — | Feature release |
| v0.13.0 | 2026.5.7 | The Tenacity Release | Multi-agent Kanban board (heartbeat, reclaim, zombie detection, retry); `/goal` Ralph loop; Checkpoints v2; Gateway auto-resume; 20th platform: Google Chat; pluggable providers; 7 i18n locales |
| v0.12.0 | 2026.4.30 | — | Feature release |
| v0.11.0 | 2026.4.23 | — | Feature release |
| v0.10.0 | 2026.4.16 | Tool Gateway release | Nous Tool Gateway for paid subscribers (web search, image gen, TTS, browser automation via subscription) |
| v0.9.0 | 2026.4.13 | The Everywhere Release | Local web dashboard; Fast Mode (`/fast`) for OpenAI/Anthropic priority queues; iMessage via BlueBubbles; Termux/Android support; WeChat; background process monitoring |
| v0.8.0 and earlier | — | — | Earlier versions (see releases page 3+) |

---

## Branding Substitution Map

Every occurrence of the left column in Hermes should appear as the right column in Nastech:

| Hermes (original) | Nastech (rebranded) |
|---|---|
| `Hermes Agent` | `Nastech Agent` |
| `Hermes` (standalone agent name) | `Nastech` |
| `hermes` (CLI command) | `nastech` |
| `Nous Research` | `Nastechai Research` |
| `NousResearch` | `nastechai` |
| `nousresearch` | `nastechai` |
| `hermes-agent` (package/repo) | `nastech-agent` |
| `hermes-agent.nousresearch.com` | `nastech-agent.nastechairesearch.com` |
| `portal.nousresearch.com` | `portal.nastechairesearch.com` |
| `discord.gg/NousResearch` | `discord.gg/nastechai` |
| `github.com/NousResearch/hermes-agent` | `github.com/nastechai/nastech-agent` |
| `nousresearch.com` | `nastechairesearch.com` |
| `~/.hermes` | `~/.nastech` |
| `HERMES_HOME` | `NASTECH_HOME` |
| `hermes model`, `hermes setup`, `hermes update` etc. | `nastech model`, `nastech setup`, `nastech update` etc. |
| `hermes claw migrate` | `nastech claw migrate` |
| `Built by Nous Research` | `Built by Nastechai Research` |
| `pip install hermes-agent` | `pip install nastech-agent` |
| `hermes update` | `nastech update` |
| `Hermes Desktop` | `Nastech Desktop` |

### ⚠️ DO NOT REBRAND — Legitimate Hermes Model Name References

The following references to "hermes" or "NousResearch" are **actual AI model identifiers** on OpenRouter and other providers. They describe the *Hermes LLM model family* made by Nous Research, NOT the Hermes Agent app. **Leave these untouched:**

- `NousResearch/Hermes-3-Llama-3.1-70B`
- `NousResearch/Hermes-3-Llama-3.1-405B`
- `hermes-3`, `hermes-4`, `hermes-4-405b`, `openrouter/hermes3:70b`
- Any model ID containing `hermes` that refers to the LLM model family
- Detection logic in `nastech_cli/model_switch.py` and `tests/nastech_cli/test_nous_nastech_non_agentic.py` (these test detection of Hermes-3/4 model family usage as a feature of Nastech)

---

## Branding Audit: What Still Needs Fixing

Based on a full codebase grep, the following files still contain unbranded Hermes/NousResearch references that **must be updated**:

### 🔴 Critical — User-visible strings

| File | Issue | Fix |
|------|-------|-----|
| `scripts/whatsapp-bridge/bridge.js` line 93 | `DEFAULT_REPLY_PREFIX = '⚕ *Hermes Agent*\n────────────\n'` | → `'⚕ *Nastech Agent*\n────────────\n'` |
| `scripts/whatsapp-bridge/bridge.js` line 247 | `browser: ['Hermes Agent', 'Chrome', '120.0']` | → `['Nastech Agent', 'Chrome', '120.0']` |

### 🟡 Medium — Code comments & documentation

| File | Issue | Fix |
|------|-------|-----|
| `scripts/whatsapp-bridge/bridge.js` line 81 | Comment `` `hermes update` updates bridge.js `` | → `` `nastech update` updates bridge.js `` |
| `scripts/whatsapp-bridge/bridge.js` lines 340, 493 | Comments mentioning "Hermes" as the agent name | → "Nastech" |
| `tests/plugins/model_providers/test_custom_profile.py` line 4 | Comment says "Hermes at — local Ollama, vLLM" (referring to running Hermes Agent, not Hermes model) | → "Nastech at — local Ollama, vLLM" |

### 🟢 Keep As-Is (backward compat / model names)

| File | Reason to keep |
|------|---------------|
| `cron/lifecycle_guard.py` line 54 | Regex detects both `nastech` and `hermes` CLI commands — backward compat for users migrating from Hermes |
| `nastech_cli/model_switch.py` lines 89–93 | Comments/regex reference `NousResearch/Hermes-3` and `hermes3` — these are actual AI model IDs |
| All of `tests/nastech_cli/test_nous_nastech_non_agentic.py` | Tests for detecting Nous Hermes LLM model family — model names, not app branding |

---

## Full Branding Plan — File Categories

### 1. Root Documentation (README, CONTRIBUTING, AGENTS.md, etc.)

**Files:**
- `README.md` — ✅ Already rebranded to Nastech
- `README.es.md` — check for Hermes refs
- `CONTRIBUTING.md` — check for Hermes refs
- `CONTRIBUTING.es.md` — check for Hermes refs
- `AGENTS.md` — check for Hermes refs
- `nastech-already-has-routines.md` — check

**What to do:** Do a pass over each file and apply the substitution map above. Make sure all links, badge URLs, install scripts, and command examples say `nastech` / `nastechai`.

### 2. Python Package Metadata

**Files:**
- `pyproject.toml` — ✅ Already shows `nastech-agent`, `Nastechai Research`

**What to do:** Bump version from `0.18.0` → `0.19.0` when syncing to Hermes v0.19.0.

### 3. Scripts & Bridges

**Files:**
- `scripts/whatsapp-bridge/bridge.js` — 🔴 **Needs fixes** (see table above)
- Any other files in `scripts/`

**What to do:** Apply exact fixes from the Critical and Medium tables above.

### 4. Web UI (`web/src/`)

**Files:** All `.tsx` and `.ts` files under `web/src/`

The grep for `hermes/NousResearch` in `web/src/` returned no hits, meaning the web UI appears to be fully rebranded already. ✅

**What to do:** Verify no `hermes`/`nousresearch` strings appear in page titles, page content, API calls, or config references.

### 5. Desktop App (`apps/desktop/`)

**What to do:** Check `apps/desktop/package.json`, electron config, window titles, and any about dialogs.

### 6. ACP / Registry

**Files:**
- `acp_registry/agent.json` — check for agent name/description
- `acp_adapter/` — check for branding

**What to do:** Ensure agent name, description, and all metadata say Nastech.

### 7. CLI Module (`nastech_cli/`)

**What to do:** Full scan; most already rebranded. Watch out for help text strings and error messages.

### 8. Gateway (`gateway/`)

**What to do:** Check all gateway config templates, help strings, and Telegram/Discord/Slack message templates for agent name references.

### 9. Localization (`locales/`)

**What to do:** Check all locale files (`.json` or `.yaml`) for hardcoded "Hermes Agent" strings.

### 10. Docker / CI / Infrastructure

**Files:**
- `Dockerfile`
- `docker-compose.yml`
- `docker-compose.windows.yml`
- `.github/` workflows
- `flake.nix`

**What to do:** Check labels, image names, env var names, and workflow titles.

### 11. Install Scripts (`nastech_bootstrap.py`, `nastech` binary)

**What to do:** These are already named `nastech*` — verify all user-visible strings inside reference Nastech, not Hermes.

---

## Upgrade Plan: v0.18.0 → v0.19.0

### What's in v0.18.1 + v0.18.2 (infrastructure patches)
- Installer/updater self-healing on Windows
- Dashboard & gateway bug fixes
- WhatsApp dashboard pairing
- MCP and provider stability fixes
- ~660+ commits of hardening

### What's new in v0.19.0 — The Quicksilver Release (must implement)
1. **~80% faster first-token** on every platform (TTFT optimization)
2. **Reasoning streams live by default** (was opt-in before)
3. **Desktop app** — 14× faster streaming markdown, virtualized diffs, snappy session switching
4. **TUI incremental markdown rendering**
5. **Bitwarden & 1Password integration** — plug password managers into the agent
6. **Smart approvals by default** — auto-judges flagged commands using LLM
7. **Live subagent monitoring** — watch subagents work in real time
8. **Durable delivery ledger** — finished responses survive a gateway crash
9. **Subscription management in terminal** — manage Nastechai Portal plan without leaving CLI
10. Version bump: `pyproject.toml` `version = "0.19.0"`

### Sync Strategy
1. Pull the upstream Hermes v0.19.0 diff vs v0.18.0
2. Apply all non-branding changes (new features, bug fixes, dependencies)
3. Re-apply the Nastech branding substitution map to any new strings introduced in the diff
4. Update `pyproject.toml` version to `0.19.0`
5. Update README release section and badges

---

## Release Naming Convention

Mirror Hermes release names with Nastech branding:

| Hermes Name | Nastech Equivalent |
|---|---|
| "The Quicksilver Release" | "Nastech Agent — The Quicksilver Release" |
| "The Judgment Release" | "Nastech Agent — The Judgment Release" |
| etc. | Prefix with "Nastech Agent —" |

---

## How to Run (for reference)

This project is a CLI/TUI tool — it is not a web server. To run it on Replit:

```bash
# Install Python deps
uv pip install -e ".[all]"

# Run the CLI
python cli.py --help

# Or install as a package
pip install -e .
nastech --help
```

The web UI (in `web/`) can be run separately with:
```bash
cd web && npm install && npm run dev
```
