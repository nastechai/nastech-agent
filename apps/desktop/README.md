# Nastech Desktop ☤

<p align="center">
  <a href="https://github.com/NastechaiResearch/nastech-agent/releases"><img src="https://img.shields.io/badge/Download-macOS%20%C2%B7%20Windows%20%C2%B7%20Linux-FFD700?style=for-the-badge" alt="Download"></a>
  <a href="https://nastech-agent.nastechai.com/docs/"><img src="https://img.shields.io/badge/Docs-nastech--agent.nastechairesearch.com-FFD700?style=for-the-badge" alt="Documentation"></a>
  <a href="https://discord.gg/NastechaiResearch"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/NastechaiResearch/nastech-agent/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
</p>

**The native desktop app for [Nastech Agent](../../README.md) — the self-improving AI agent from [Nastechai Research](https://nastechairesearch.com).** Same agent, same skills, same memory as the CLI and gateway, in a polished native window — chat with streaming tool output, side-by-side previews, a file browser, voice, and settings, no terminal required. Available for **macOS, Windows, and Linux**.

<table>
<tr><td><b>Chat with the full agent</b></td><td>Streaming responses, live tool activity, structured tool summaries, and the same conversation history as every other Nastech surface.</td></tr>
<tr><td><b>Side-by-side previews</b></td><td>Render web pages, files, and tool outputs in a right-hand pane while you keep chatting.</td></tr>
<tr><td><b>File browser</b></td><td>Explore and preview the working directory without leaving the app.</td></tr>
<tr><td><b>Voice</b></td><td>Talk to Nastech and hear it back.</td></tr>
<tr><td><b>Settings & onboarding</b></td><td>Manage providers, models, tools, and credentials from a real UI. First-run setup gets you to your first message in seconds.</td></tr>
<tr><td><b>Stays current</b></td><td>Built-in updates pull the latest agent and rebuild the app in place.</td></tr>
</table>

---

## Install

### Install with Nastech (recommended)

Already have the Nastech CLI? Just run:

```bash
nastech desktop
```

It builds and launches the GUI against your existing install — same config, keys, sessions, and skills. On first launch Nastech walks you through picking a provider and model; nothing else to configure.

### Prebuilt installers

Prebuilt installers are built and distributed via [the Nastech Desktop website.](https://nastech-agent.nastechai.com/).

---

## Updating

The app checks for updates in the background and offers a one-click update when one is ready. You can also update any time from the CLI:

```bash
nastech update
```

---

## Requirements

The installer handles everything for you (Python 3.11+, a portable Git, ripgrep).

---

## Development

Want to hack on the app itself? Install workspace deps from the repo root once, then run the dev server from this directory:

```bash
npm install          # from repo root — links apps/desktop, web, apps/shared
cd apps/desktop
npm run dev          # Vite renderer + Electron, which boots the Python backend
```

Point the app at a specific source checkout, or sandbox it away from your real config:

```bash
NASTECH_DESKTOP_NASTECH_ROOT=/path/to/clone npm run dev
NASTECH_HOME=/tmp/throwaway npm run dev
npm run dev:fake-boot   # exercise the startup overlay with deterministic delays
```

### Building installers

```bash
npm run dist:mac     # DMG + zip
npm run dist:win     # NSIS + MSI
npm run dist:linux   # AppImage + deb + rpm
npm run pack         # unpacked app under release/ (no installer)
```

Installers are built and uploaded to GitHub Releases manually. macOS/Windows signing & notarization happen automatically when the relevant credentials are present in the environment (`CSC_LINK` / `CSC_KEY_PASSWORD` / `APPLE_*` for macOS, `WIN_CSC_*` for Windows).

### How it works

The packaged app ships the Electron shell and a native React chat surface. On first launch it can install the Nastech Agent runtime into `NASTECH_HOME` (`~/.nastech`, or `%LOCALAPPDATA%\nastech` on Windows) — the **same layout a CLI install uses**, so the two are interchangeable. Backend resolution first honours `NASTECH_DESKTOP_NASTECH_ROOT`, then a completed managed install, then a probed `nastech` on `PATH` (unless `NASTECH_DESKTOP_IGNORE_EXISTING=1` is set), and finally an explicit `NASTECH_DESKTOP_NASTECH` command override for packagers/troubleshooting. The renderer (React, in `src/`) talks to a headless backend the app launches for you — a `nastech serve` process that serves the `tui_gateway` JSON-RPC/WebSocket API — through the framework-agnostic client in [`apps/shared`](../shared/) (the same client the web dashboard consumes), and reuses the agent runtime rather than embedding `nastech --tui`. The app is **self-contained**: it runs its own `nastech serve` backend and never opens or requires the web dashboard UI. (For backward compatibility, a runtime that predates the `serve` command automatically falls back to a headless `dashboard --no-open` — see `electron/backend-command.cjs` — so mid-upgrade installs never break.) The install, backend-resolution, and self-update logic all live in `electron/main.cjs`.

### Verification

Run before opening a PR (lint may surface pre-existing warnings but must exit cleanly):

```bash
npm run fix
npm run typecheck
npm run lint
npm run test:desktop:all
```

### Troubleshooting

Boot logs land in `NASTECH_HOME/logs/desktop.log` (includes backend output and recent Python tracebacks) — check it first if the app reports a boot failure.

**macOS / Linux:**

```bash
# Force a clean first-launch setup
rm "$HOME/.nastech/nastech-agent/.nastech-bootstrap-complete"
# Rebuild a broken Python venv
rm -rf "$HOME/.nastech/nastech-agent/venv"
# Reset a stuck macOS microphone prompt (macOS only)
tccutil reset Microphone com.nastechairesearch.nastech
```

**Windows (PowerShell):**

```powershell
# Force a clean first-launch setup
Remove-Item "$env:LOCALAPPDATA\nastech\nastech-agent\.nastech-bootstrap-complete"
# Rebuild a broken Python venv
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\nastech\nastech-agent\venv"
```

> The default Nastech home on Windows is `%LOCALAPPDATA%\nastech`. Set the `NASTECH_HOME` env var if you've relocated it.

---

## Community

- 💬 [Discord](https://discord.gg/NastechaiResearch)
- 📖 [Documentation](https://nastech-agent.nastechai.com/docs/)
- 🐛 [Issues](https://github.com/NastechaiResearch/nastech-agent/issues)

---

## License

MIT — see [LICENSE](../../LICENSE).

Built by [Nastechai Research](https://nastechairesearch.com).
