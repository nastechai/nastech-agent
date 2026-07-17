# Nastech Agent — Full Hermes Parity & Branding Plan

> Generated: 2026-07-16  
> Source: NousResearch/hermes-agent @ main (v0.18.2)  
> Target: nastechai/nastech-agent (currently v0.18.0)

This document catalogs every commit Hermes has that Nastech is missing, organizes them into actionable work streams, and defines the complete branding strategy.

---

## 1. BRANDING STRATEGY

### 1.1 What Nastech is / Identity

| Property | Hermes (upstream) | Nastech (fork) |
|---|---|---|
| Package name | `hermes-agent` | `nastech-agent` ✅ |
| CLI command | `hermes` | `nastech` ✅ |
| Author org | Nous Research | Nastechai Research ✅ |
| GitHub org | `NousResearch` | `nastechai` ✅ |
| Home dir | `~/.hermes` | `~/.nastech` ✅ |
| Env var | `HERMES_HOME` | `NASTECH_HOME` ✅ |
| Docs URL | hermes-agent.nousresearch.com | nastech-agent.nastechairesearch.com ✅ |
| Portal URL | portal.nousresearch.com | portal.nastechairesearch.com ✅ |
| Discord | discord.gg/NousResearch | discord.gg/nastechai ✅ |

### 1.2 Branding Audit Tasks (per file / area)

Every time a Hermes commit is ported, apply these substitutions consistently:

| Find | Replace with |
|---|---|
| `hermes-agent` (package slug) | `nastech-agent` |
| `hermes` (CLI command) | `nastech` |
| `HERMES_HOME` | `NASTECH_HOME` |
| `HERMES_WRITE_SAFE_ROOT` | `NASTECH_WRITE_SAFE_ROOT` |
| `HERMES_OPTIONAL_SKILLS` | `NASTECH_OPTIONAL_SKILLS` |
| `~/.hermes` | `~/.nastech` |
| `Hermes Agent` (product name) | `Nastech Agent` |
| `Nous Research` / `NousResearch` | `Nastechai Research` / `nastechai` |
| `hermes_cli/` | `nastech_cli/` |
| `hermes_constants.py` | `nastech_constants.py` |
| `hermes_state.py` | `nastech_state.py` |
| `hermes_time.py` | `nastech_time.py` |
| `hermes_logging.py` | `nastech_logging.py` |
| `hermes_bootstrap.py` | `nastech_bootstrap.py` |
| `setup-hermes.sh` | `setup-nastech.sh` |
| `hermes-already-has-routines.md` | `nastech-already-has-routines.md` |
| `nousresearch.com` | `nastechairesearch.com` |
| `hermes-agent.nousresearch.com` | `nastech-agent.nastechairesearch.com` |
| `portal.nousresearch.com` | `portal.nastechairesearch.com` |
| `discord.gg/NousResearch` | `discord.gg/nastechai` |
| `@nous-research/ui` | `@nastechai-research/ui` |
| `hermes-parser` | `nastech-parser` |
| `hermes-desktop-plugins` (skill) | `nastech-desktop-plugins` |
| `apps/bootstrap-installer/src-tauri/hermes-setup.manifest` | rename to `nastech-setup.manifest` |
| `apps/bootstrap-installer/public/nous-girl.jpg` | replace with Nastechai brand image |
| `acp_registry/icon.svg` | replace with Nastechai icon |

### 1.3 Assets to Create/Replace

- [ ] `assets/banner.png` — Replace Hermes banner with Nastech-branded banner (same layout, Nastechai Research logo + "Nastech Agent ☤")
- [ ] `apps/bootstrap-installer/public/nous-girl.jpg` → Nastechai equivalent mascot/brand image
- [ ] `apps/bootstrap-installer/src-tauri/icons/` — Replace all Hermes icons (128×128, 32×32, .icns, .ico) with Nastech icons
- [ ] `acp_registry/icon.svg` — Replace NousResearch icon with Nastechai icon

### 1.4 Version Bump

- Hermes is at **v0.18.2**, Nastech is at **v0.18.0**
- After porting all commits, bump `pyproject.toml` → `version = "0.18.2"`
- Update `package.json` npm package version accordingly
- Update npm bridge `package.json` if separate

---

## 2. MISSING COMMITS BY FEATURE AREA

The following sections list all Hermes commits Nastech has not yet merged, ordered by priority.

---

### 2.1 Terminal — Per-session CWD Refactor (4 steps)

**Why it matters:** The current env-side cwd tracking is shared across sessions, causing `cd` in one session to bleed into another. This refactor makes cwd truly per-session.

| Commit | Title |
|---|---|
| `be2a1290` | refactor(terminal): introduce per-session cwd records (step 1: dual-write) |
| `5461e0e0` | refactor(file-tools): resolve paths against per-session cwd records (step 2) |
| `4d30b05d` | refactor(terminal): resolve command cwd from per-session records (step 3) |
| `4c4c52d6` | refactor(terminal): delete legacy env-side cwd tracking (step 4) |

**Files affected:** `tools/` terminal/shell tools, `tools/file_tools.py` or similar  
**Branding note:** None needed — pure logic change.

---

### 2.2 Webhook — Dual-Stack IPv6 Bind Fixes

**Why it matters:** Webhook adapter failed under IPv6-only (6PN) networks; fixes make address binding exclusive and dual-stack by default.

| Commit | Title |
|---|---|
| `d542894a` | fix(webhook): default to dual-stack bind so 6PN (IPv6) can reach the adapter |
| `92876eff` | fix(webhook): make dual-stack bind exclusive |

**Files affected:** `gateway/` webhook/adapter code

---

### 2.3 TUI — Notification Routing & Dashboard Fixes

**Why it matters:** Background process notifications were being broadcast to all sessions; fixes route them to the owning session only.

| Commit | Title |
|---|---|
| `81fc2486` | fix(tui): route bg process notifications to owning session, drop orphaned events |
| `54d0948d` | fix(tui): route post-turn completions by owner |
| `ca803523` | test(tui): cover live notification ownership routing |
| `a16ac37d` | fix(tui): redraw dashboard after new session |

**Files affected:** `ui-tui/`, `tui_gateway/`

---

### 2.4 Gateway — Multiplex, API Drain, Session Recovery

**Why it matters:** Several race conditions and resource leaks in the gateway — relay adapter sharing, API drain on shutdown, session recovery from orphaned websockets.

| Commit | Title |
|---|---|
| `2ae39dae` | fix(gateway): share relay adapter in multiplex mode |
| `6a35f9e6` | fix(container): keep named multiplex gateway slots down |
| `ca907480` | fix(gateway): allow ws_orphan_reap rows in session recovery |
| `7452467f` | test(gateway): cover ws_orphan_reap session recovery |
| `ca559a78` | fix(gateway): never prune sessions when active-process check fails |
| `021ee345` | fix(gateway): drain in-flight api_server runs on shutdown |
| `ffc10cc6` | fix(gateway): quiesce API and cron work during drains |
| `fix(api)` | fix(api): reserve cron fire work during drain |
| `bd740f20` | fix(gateway): deduplicate completion delivery |

**Files affected:** `gateway/run.py`, `gateway/` adapters

---

### 2.5 Auth — OAuth Normalization & Bootstrap

**Why it matters:** Manually-added Anthropic sk-ant-oat tokens were not being normalized to OAuth format, causing auth failures.

| Commit | Title |
|---|---|
| `77763f00` | fix(auth): normalize Anthropic sk-ant-oat pool creds to OAuth |
| `1215fbbd` | test(auth): cover sk-ant-oat OAuth normalization |
| `0512f06a` | fix(auth): centralize pool auth normalization |
| `3f2a389c` | fix(auth): apply newer hosted bootstrap session |
| `96a07084` | fix(auth): preserve provider fallback during refresh |
| `f9e35e6e` | fix(auth): route session refresh with provider hint cookie |

**Files affected:** `agent/` auth-related files, `gateway/` auth

---

### 2.6 Slack — Agent View & Workspace Routing

**Why it matters:** Full Slack Agent View API support (not just regular messaging). Required for Slack's June 30 Agent Messaging spec.

| Commit | Title |
|---|---|
| `9a3b676f` | feat(slack): support agent view manifests |
| `1328a6b` | feat(slack): cover agent view assistant APIs |
| `4554fe12` | feat(slack): complete agent view workspace routing |
| `38cfae9b` | fix(slack): scope Agent View workspace state |
| `f1328a6b` | fix(slack): clear uniquely scoped assistant status |
| `f1328a6b` | fix(slack): gate feedback buttons behind rich_blocks |
| `d6590f8b` | chore(slack): bump slack-bolt to 1.29.0 and slack-sdk to 3.43.0 |

**Files affected:** `plugins/platforms/slack/` or `gateway/platforms/slack/`  
**Branding note:** None — pure functionality.

---

### 2.7 Telegram — Polling, Rich Messages, DNS

**Why it matters:** Multiple reliability fixes: polling health gating, rich_messages config respect, DNS hang diagnosis.

| Commit | Title |
|---|---|
| `8295cf6b` | fix(telegram): gate polling health on getUpdates progress |
| `202be02a` | test(telegram): define polling progress contract |
| `adf62065` | test(telegram): guard PTB integration tests with importorskip |
| `e16743b0` | fix(telegram): diagnose blocked-loop init hangs, unbind DoH from system DNS |
| `2d71e2f1` | fix(telegram): classify and dedup post-reconnect probe failures |
| `34d07732` | fix(telegram): respect rich_messages config for pipe table routing |
| `b45a217e` | fix(agent): gate Telegram rich-Markdown hint on rich_messages config |
| `4e6e5181` | refactor(telegram): drop dead _content_is_pipe_table_primary helper |

**Files affected:** `plugins/platforms/telegram/` or `gateway/platforms/telegram/`

---

### 2.8 MCP — Resource Blocks & Version Pinning

**Why it matters:** MCP tool results that returned ResourceLink, EmbeddedResource, or Audio blocks were silently dropped. Now materialized properly.

| Commit | Title |
|---|---|
| `d1b8fd0` | fix(mcp): materialize ResourceLink/EmbeddedResource/Audio blocks |
| `284a3cd4` | fix(mcp): use real wire name in ResourceLink marker |
| `9df5f879` | feat(mcp): enforce exact version pins across the whole MCP catalog |
| `a52393a3` | fix(mcp): pin blender-mcp to 1.6.4 per catalog dependency policy |
| `9be941da` | feat(mcp): add Blender to the MCP catalog |

**Files affected:** `tools/mcp_tool.py` or similar, `optional-mcps/`

---

### 2.9 Models & Providers — New Providers + Reasoning Overrides

**Why it matters:** Adds Upstage Solar and DeepInfra as providers. Per-model reasoning_effort overrides let users fine-tune cost/quality per task.

| Commit | Title |
|---|---|
| `20502b40` | feat(agent): add Upstage Solar as a model provider |
| `0031c5c3` | refactor: treat unknown Solar models as reasoning-capable |
| `c1e36f43` | fix(agent): register Upstage keys in the env-var catalog |
| `35d3fc3b` | refactor(agent): drop solar-pro rolling alias, default to solar-pro3 |
| `5f3d5740` | refactor(agent): drop solar-open2-preview from Solar context fallbacks |
| `899e420a` | refactor(upstage): drop manual auth/models registrations |
| `f88cac71` | fix(upstage): map 'ultra' reasoning effort to Solar's high |
| `0d018319` | chore: add changhyun.min to AUTHOR_MAP |
| `fe002eb1` | feat(providers): Support DeepInfra as an LLM provider |
| `10dc1571` | fix(deepinfra): align refresh and TTS availability |
| `2fc3f9c1` | fix(deepinfra): harden multimodal provider routing |
| `094f2b55` | feat(cli): promote Fireworks AI to #2 in provider list |
| `b34e5659` | feat(models): GLM-5.2 marked as catalog default |
| `97375e0f` | fix(models): route bare-provider /model switch through cost-safe default |
| `d9cdb819` | feat(config): support per-model reasoning_effort overrides |
| `e81d18df` | refactor(reasoning): unify per-model reasoning resolution |
| `7bb409b2` | test: update stale _load_reasoning_config mocks |
| `df5700eb` | feat(auxiliary): per-task reasoning_effort for auxiliary models |
| `1f41bdbe` | fix(upstage): collapse unknown future efforts to high |
| `33dfb7e4` | docs: add Upstage Solar to provider docs |

**Files affected:** `providers/`, `agent/`, `cli.py`, `.env.example`  
**Branding note:** `.env.example` entries for new providers — no rebrand needed, just add.

---

### 2.10 Codex — Reliability & Reasoning Fixes

**Why it matters:** Large Codex requests could hang indefinitely. Reasoning-only turns failed silently. Finish_reason was misclassified.

| Commit | Title |
|---|---|
| `7af59f47` | fix(codex): raise hard-ceiling default above the max stale floor |
| `bcd7e2ce` | fix(agent): add finite hard ceiling on openai-codex request time |
| `d6c14a95` | fix(codex): keep large-request ttfb watchdog active |
| `306a3774` | fix: finish_reason misclassified as incomplete for codex_responses |
| `07443ea2` | test(codex): pin codex_backend issuer in summary-only reasoning sibling test |
| `05d1ca54` | fix(codex): rescue reasoning-only turns that die with 'remained incomplete' |
| `01b76092` | fix(codex): keep GitHub/Copilot Responses on the reasoning-only path |
| `2fc0e3d1` | fix(codex): guard continuation nudge against role-alternation violations |
| `8aafa0f8` | test(codex): pin codex_backend issuer in xai-scoped salvage test |

**Files affected:** `agent/codex` or similar codex handling files

---

### 2.11 Agent — Tool Batching, Status Line, Background Review

**Why it matters:** Mixed tool batches (text + tool calls together) lost concurrency. Provider wait time now shown live. Background review inherits reasoning config.

| Commit | Title |
|---|---|
| `271a9d8e` | perf(agent): segment mixed tool batches to recover lost concurrency |
| `092a97ef` | fix(agent): explain long provider waits on the live status line |
| `17cfa0f0` | fix(background_review): inherit parent's reasoning_config |
| `8ef00693` | fix(background_review): gate reasoning_config inheritance on not-routed |
| `c2a3b9ce` | fix(state): use PASSIVE checkpoint for periodic WAL flush |
| `779c0dd8` | fix(compressor): unwrap web_extract dict URLs in tool-result summaries |

**Files affected:** `agent/`, `run_agent.py`

---

### 2.12 Delegation — Persistent Background Completions

**Why it matters:** Background agent completions could be lost if the gateway restarted before delivery. Now persisted durably.

| Commit | Title |
|---|---|
| `94a7705b` | feat(delegation): persist background completions |
| `67f4e1b4` | fix(delegation): harden durable completion delivery |
| `af250d84` | docs(delegation): clarify background lifetime |

**Files affected:** `agent/delegation` or similar

---

### 2.13 Session Management — Import Flow & Validation

**Why it matters:** Users can now import session exports via the dashboard. Imported sessions are validated before loading.

| Commit | Title |
|---|---|
| `b51d365e` | feat(dashboard): add session import flow |
| `ac705b52` | fix(sessions): validate imported session payloads |
| `56ab9951` | fix(dashboard): add MCP auth to profile builder |
| `bdb1c872` | fix(dashboard): pass backup output with -o |
| `d1be769b` | feat(dashboard): clarify manual Telegram bot setup |
| `3ffd8b3d` | fix(dashboard): persist Discord toolsets to Discord platform |
| `4a69a662` | test(dashboard): use valid Telegram tokens in profile tests |

**Files affected:** `web/` dashboard, `nastech_cli/` or `nastech_state.py`

---

### 2.14 File Safety

**Why it matters:** Safe-root write denial errors were indistinguishable from credential-block errors. Now returns actionable error messages.

| Commit | Title |
|---|---|
| `55d826cc` | fix(file-safety): distinguish safe-root write denial from credential blocks |
| `320e886f` | test(file-safety): add integration tests for safe-root denial messages |
| `2a0dd95c` | docs: clarify write safety, NASTECH_WRITE_SAFE_ROOT, and file-mutation verifier |

**Files affected:** `tools/` file safety checker  
**Branding note:** docs reference `HERMES_WRITE_SAFE_ROOT` → rename to `NASTECH_WRITE_SAFE_ROOT`

---

### 2.15 Cron — SessionDB Timeout & Deduplication

**Why it matters:** Scheduled scripts could run twice if they took longer than their interval. SessionDB init could hang cron forever.

| Commit | Title |
|---|---|
| `cd537187` | fix(cron): prevent long-running scheduled scripts from running twice |
| `c675e7c7` | fix(cron): bound SessionDB init so a hang can't wedge cron forever |
| `ccb045ba` | fix(cron): resolve SessionDB timeout from config.yaml |

**Files affected:** `cron/`

---

### 2.16 Approval — Smart Deny & WhatsApp

**Why it matters:** Smart deny owner overrides were being applied globally instead of per-operation. WhatsApp Cloud interactive taps gated on DM allowlist.

| Commit | Title |
|---|---|
| `d48bf743` | fix(approval): scope smart deny owner overrides to one operation |
| `b03c94db` | fix(approval): emit observer hooks for smart verdicts |
| `ac705b52` | fix(whatsapp_cloud): gate interactive taps on DM allowlist |
| `bd740f20` | test(approval): isolate smart observer redaction failure |
| `dfeedf61` | fix(patch): ignore inert context-only hunks |

**Files affected:** `agent/approval`, `gateway/platforms/whatsapp/`

---

### 2.17 CLI — npm Install Skip on Unchanged Lockfile

**Why it matters:** `nastech update` was always running `npm install` even when `package-lock.json` hadn't changed — slowing updates significantly.

| Commit | Title |
|---|---|
| `aa56243a` | perf(cli): skip npm install during update when lockfile is unchanged |
| `71e91f89` | test(update): document shared npm cache scope |
| `d426b9dd` | fix: derive skip-key manifests from npm workspaces config |

**Files affected:** `nastech_cli/` update command

---

### 2.18 Config — Partial Save Preservation

**Why it matters:** Partial `save_config` writes were discarding platform entries that weren't included in the partial payload.

| Commit | Title |
|---|---|
| `0ab90040` | fix(config): preserve platforms on partial save_config writes |
| `1b059d1a` | test(config): regression for merge_existing partial saves |

**Files affected:** `nastech_cli/config` or `nastech_constants.py`

---

### 2.19 MoA (Mixture of Agents) Fixes

**Why it matters:** Aggregator incorrectly resolved reasoning when acting model slot was unset. Empty user turns in advisory view caused 400 errors with strict providers.

| Commit | Title |
|---|---|
| `0a940972` | fix(moa): aggregator resolves reasoning like an acting model when slot is unset |
| `b4c2c4f9` | fix: drop empty user turns from MoA advisory view |
| `b013ed03` | fix(moa): scope the non-text placeholder to structured content only |

**Files affected:** `agent/moa_loop.py`

---

### 2.20 Desktop App — Full Electron Feature Set (Largest work stream)

**Why it matters:** Hermes Desktop is now a major differentiator — full multi-session tiling, session tabs, plugin system, command palette, and more. This is the largest work stream.

#### 2.20.1 Layout & Session Tiling
| Commit | Title |
|---|---|
| `c388daa6` | feat(desktop): layout-tree model + store + workspace geometry |
| `63a9bde7` | feat(desktop): layout-tree renderer — splits, zones, drag-session, tab strip |
| `f1379bd6` | feat(desktop): multi-session tiles — per-profile state, tile pane, pane mirror |
| `ac4f596c` | feat(desktop): pointer session drag/drop + row/tab menus |
| `0f922002` | feat(desktop): contribution controller, surfaces, and wiring |
| `7f74b324` | feat(desktop): store + lib — layout/preview/session atoms, escape-layers, keybind helpers |

#### 2.20.2 Session Tabs
| Commit | Title |
|---|---|
| `eae1d7d1` | feat(desktop): ⌘W close-tab, ⌘⇧T reopen, ⌘T new tab, ⌘1-9 + ⌃Tab tab switching |
| `860a3f67` | feat(desktop): session hooks — open-in-tile, per-session actions, resilient resume |
| `10fbade6` | feat(desktop): electron — openDir IPC + ⌘W menu bridge |
| `2afbe777` | feat(desktop): focused-session-aware titlebar + statusbar |

#### 2.20.3 Chat & Composer
| Commit | Title |
|---|---|
| `eea1d7d1` | feat(desktop): chat view — drop overlays, composer scoping, tile integration |
| `1813d304` | feat(desktop): add a chat backdrop on/off toggle |
| `bccc827d` | refactor(desktop): trim backdrop store to match tool-view style |

#### 2.20.4 Plugin System
| Commit | Title |
|---|---|
| `aefb3629` | feat(desktop): contribution registry — namespaced areas, keybinds, palette |
| `29b8cacf` | feat(desktop): plugin SDK surface — rest door, socket, react-query, UI kit |
| `7af59f47` | feat(desktop): plugin manager, runtime loader, and plugins settings |
| `aae35c5e` | feat(desktop): routes, nav, and command palette as contributions |
| `369d0eee` | refactor(desktop): retire desktop-controller for the contribution shell |

#### 2.20.5 Reasoning & i18n
| Commit | Title |
|---|---|
| `8bd4a419` | fix(desktop): render reasoning text in the Thinking widget |
| `3510b188` | feat(desktop): add profile-aware approval mode control |
| `d14bf23f` | chore(desktop): build config — keep tsc emit out of src |
| `a57b3378` | docs(desktop): hermes-desktop-plugins skill + starter template → rebrand to nastech-desktop-plugins |
| `aff295dc` | chore(desktop): i18n strings for tabs, zones, and session menus |

#### 2.20.6 Desktop Bug Fixes
| Commit | Title |
|---|---|
| `2d0f2185` | fix(desktop): clear stale compaction status across session switches |
| `305e2655` | fix(desktop): composer progressively collapses on narrow tiles |
| `b5aef05e` | fix(desktop): layout reset reopens collapsed sidebars |
| `092a97ef` | fix(desktop): session-tab drag, focus sync, and pop-out isolation |
| `7c84d13f` | fix(desktop): clear the transcript on every cold resume |
| `3615545b` | fix(desktop): keep draft fallback rows across autosave echo |
| `7f7a4038` | fix(desktop): keep draft fallback rows (autosave echo follow-up) |
| `7fdae5d2` | fix(desktop): ensure node-pty spawn-helper is executable |
| `5d691374` | fix(desktop): recognize little-endian Mach-O magic in native binary classifier |
| `47d56b80` | fix(desktop): prevent staging wrong-platform node-pty binary for cross targets |
| `9f7a3cb1` | test(desktop): cover restorePersistedZoomLevel renderer notification |
| `10dc1571` | fix(desktop): sync UI Scale setting after zoom restore on window load |
| `39230d17` | refactor(desktop): funnel zoom apply+notify so restore can't desync |

**Files affected:** `web/` (Electron app), desktop skill file  
**Branding note:** `docs(desktop): hermes-desktop-plugins skill` → rename to `nastech-desktop-plugins`

---

### 2.21 Bootstrap Installer (Tauri/Rust) — New App

**Why it matters:** A native GUI installer for first-time users on Windows/macOS, replacing the raw shell-script experience. Built with Tauri (Rust + React).

**This is a complete new directory: `apps/bootstrap-installer/`**

Key files to port and rebrand:
- `src-tauri/hermes-setup.manifest` → `nastech-setup.manifest`
- `src-tauri/tauri.conf.json` — update `productName`, `identifier`, URLs
- `src/components/brand-mark.tsx` — replace Hermes logo with Nastech logo
- `public/nous-girl.jpg` — replace with Nastechai brand image
- All icon files — replace with Nastechai icons
- `src/routes/welcome.tsx` — update product name/description copy
- `src/theme.ts` — update brand colors to Nastechai palette
- `src/styles.css` — update any hardcoded brand colors

**Branding note:** This is the biggest branding job in the whole plan. Every UI string, icon, color, and manifest identifier must be Nastechai.

---

### 2.22 JS Testing Infrastructure — `tests-js/` Workspace

**Why it matters:** Hermes moved several Python tests (package.json invariants, macOS entitlements, desktop tests) into a Vitest workspace. These catch JS/npm regressions in CI.

| File | Purpose |
|---|---|
| `tests-js/package.json` | Vitest workspace package |
| `tests-js/vitest.config.ts` | Vitest config |
| `tests-js/eslint.config.mjs` | ESLint for test files |
| `tests-js/tsconfig.json` | TypeScript config |
| `tests-js/assistant-ui-tap-compat.test.ts` | @assistant-ui compatibility |
| `tests-js/desktop-mac-entitlements.test.ts` | macOS entitlement checks |
| `tests-js/package-json-lazy-deps.test.ts` | Lazy-dep invariant tests |

Also:
- `eslint.config.shared.mjs` — shared ESLint config across workspaces
- `.prettierrc` + `.prettierignore` — Prettier config

**Branding note:** Update any strings that reference `hermes` in test descriptions/imports.

---

### 2.23 CI/CD Improvements

**Why it matters:** Better CI visibility (per-job timing, wait times), safer JS autofix (via PR not direct push), semantic lockfile diffs.

| Commit | Title |
|---|---|
| `f8ddf4fd` | feat(ci): semantic package-lock.json diff as an upserted PR comment |
| `f0b7cf38` | feat(ci): show per-job wait times in timing report |
| `79061f44` | feat(ci): show passed/failed jobs in summary |
| `727025a2` | feat(ci): load npm workspaces from package.json |
| `75f45a06` | fmt(js): npm run fix on merge |
| `64389a2c` | fix(ci): js-autofix pushes via PR instead of direct push to main |
| `5222d24f` | fix(ci): gh pr create doesn't support --json flag |
| `0c1adb48` | fix(ci): handle merge race in js-autofix poll loop |
| `75778342` | fix(ci): fail closed when workspace matrix discovery produces empty list |
| `29b8cacf` | fix(ci): add missing Δ Wait column to skipped job rows |
| `e117478e` | fix(ci): align baseline gantt bars to current job start |
| `6800ec9d` | change(ci/desktop): move desktop app build into check job |

**Files affected:** `.github/workflows/`  
**Branding note:** Any workflow names/comments referencing `hermes` → `nastech`

---

### 2.24 Nix & Flake Fixes

| Commit | Title |
|---|---|
| `f8b6d381` | fix(nix): dirty-tree wrapper bug + filtered rebuild scope + overlay alias |

**Files affected:** `flake.nix`, `nix/`

---

### 2.25 ACP & Windows

| Commit | Title |
|---|---|
| `ed8ce1f9` | fix(windows): survive broken login bash on Windows |
| `3f0b0e20` | Merge: make @assistant-ui tap invariant workspace-nesting aware |
| `9baa7d46` | chore(desktop): upgrade @assistant-ui to 0.14 |
| `c91e6510` | fix(desktop): restore @esbuild platform entries in lockfile for CI |

---

## 3. IMPLEMENTATION ORDER (Recommended)

Port these streams roughly in this order — earlier items unblock or de-risk later ones:

1. **Version bump** — `pyproject.toml` v0.18.0 → v0.18.2, `package.json` version
2. **Branding consistency audit** — grep entire codebase, ensure all substitutions in §1.2 are applied
3. **JS/Prettier/ESLint config** — `.prettierrc`, `.prettierignore`, `eslint.config.shared.mjs` (tiny, unblocks everything JS)
4. **`tests-js/` workspace** — port all 4 test files + configs
5. **CI/CD workflows** — `.github/workflows/` updates
6. **Terminal CWD refactor** (steps 1–4) — core reliability
7. **Webhook dual-stack** — 2 commits, small
8. **File safety** — 3 commits, small
9. **Config partial save** — 2 commits, small
10. **Cron fixes** — 3 commits, small
11. **MoA fixes** — 3 commits, small
12. **Approval fixes** — 5 commits, small
13. **Auth normalization** — 6 commits, medium
14. **Codex reliability** — 9 commits, medium
15. **Agent batching + status line** — 6 commits, medium
16. **Delegation persistence** — 3 commits, small
17. **Telegram fixes** — 8 commits, medium
18. **Slack agent view** — 7 commits, medium
19. **TUI notification routing** — 4 commits, medium
20. **Gateway multiplex + drain** — 9 commits, medium
21. **MCP resource blocks** — 5 commits, medium
22. **Models: Upstage Solar + DeepInfra** — 20 commits, large
23. **Session import + validation** — 7 commits, medium
24. **CLI npm skip** — 3 commits, small
25. **Desktop: full feature set** — 40+ commits, very large (can be parallelized across sub-streams)
26. **Bootstrap installer** — entirely new app, rebrand-heavy, very large

---

## 4. BRANDING CONSISTENCY CHECKLIST (run before marking any stream complete)

- [ ] `grep -r "hermes" . --include="*.py" --include="*.ts" --include="*.tsx" --include="*.md" --include="*.yaml" --include="*.yml" --include="*.json" --include="*.toml" --include="*.sh" -i | grep -v ".git" | grep -v "node_modules"` — find any remaining references
- [ ] CLI help text (`nastech --help`) shows Nastechai branding, not Hermes/Nous
- [ ] Error messages don't reference `HERMES_HOME`
- [ ] Docs skill files don't reference hermes-desktop-plugins
- [ ] `pyproject.toml` author is `Nastechai Research`, package is `nastech-agent`
- [ ] `package.json` package name is `nastech-agent` (or appropriate Nastechai name)
- [ ] Installer (Tauri) `tauri.conf.json` identifier doesn't contain `nousresearch` or `hermes`

---

## 5. SUMMARY COUNTS

| Category | Commits |
|---|---|
| Desktop (Electron) | ~45 |
| Bootstrap Installer | ~25 (new app) |
| Models/Providers | ~20 |
| CI/CD | ~12 |
| Gateway | ~9 |
| Codex | ~9 |
| Slack | ~7 |
| Auth | ~6 |
| Terminal CWD | 4 |
| Telegram | ~8 |
| Agent | ~6 |
| MCP | ~5 |
| Session | ~7 |
| TUI | ~4 |
| Approval | ~5 |
| MoA | ~3 |
| File Safety | ~3 |
| Delegation | ~3 |
| Cron | ~3 |
| Webhook | ~2 |
| CLI | ~3 |
| Config | ~2 |
| JS Testing Infra | ~8 |
| Nix | ~1 |
| **TOTAL** | **~200+** |

All 200+ commits require the branding substitution table in §1.2 applied before merging.
