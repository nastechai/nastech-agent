"""
brand.py — Hermes → Nastech branding substitution engine.

Applies text & path substitutions so any file pulled verbatim from
NousResearch/hermes-agent becomes correctly branded as nastechai/nastech-agent.

Rules are ordered from most-specific to least-specific so that longer/exact
matches are applied before shorter wildcard ones (preventing double-substitution).

MODEL-NAME EXCEPTIONS (must NOT be branded):
  NousResearch/Hermes-3-*   — OpenRouter / HuggingFace model IDs
  hermes3:70b               — Ollama model tags
  Hermes-3-*, Hermes3       — model short names in prompts/comments
  hermes-2-*                — previous generation model names
"""

from __future__ import annotations

import re
from pathlib import Path

# ── Path branding ──────────────────────────────────────────────────────────────
# Maps hermes path segments to their nastech equivalents.
# Used when renaming files/directories pulled from upstream.

PATH_SUBS: list[tuple[str, str]] = [
    # Python package
    ("hermes_cli/",          "nastech_cli/"),
    ("hermes_cli\\",         "nastech_cli\\"),
    # Named files
    ("hermes_constants.py",  "nastech_constants.py"),
    ("hermes_state.py",      "nastech_state.py"),
    ("hermes_time.py",       "nastech_time.py"),
    ("hermes_logging.py",    "nastech_logging.py"),
    ("hermes_bootstrap.py",  "nastech_bootstrap.py"),
    ("hermes_prompt.py",     "nastech_prompt.py"),
    ("hermes_meta.py",       "nastech_meta.py"),
    # Shell / installer scripts
    ("setup-hermes.sh",      "setup-nastech.sh"),
    ("hermes-setup.sh",      "nastech-setup.sh"),
    ("hermes-setup.manifest","nastech-setup.manifest"),
    # CI / workflow artefacts
    ("hermes-lockfile-diff", "nastech-lockfile-diff"),
    ("hermes-parity-",       "nastech-parity-"),
]


def brand_path(path: str) -> str:
    """Return path with Hermes segments replaced by Nastech equivalents."""
    for old, new in PATH_SUBS:
        path = path.replace(old, new)
    return path


# ── Content branding ───────────────────────────────────────────────────────────
# Each entry is (compiled_regex, replacement_string).
# Build from a declarative table so the table is easy to audit.

_RAW_SUBS: list[tuple[str, str]] = [
    # ── GitHub / package slugs (most specific first) ──────────────────────────
    (r"NousResearch/hermes-agent",         "nastechai/nastech-agent"),
    (r"nousresearch/hermes-agent",         "nastechai/nastech-agent"),

    # npm scoped package  (@nous-research/ui  →  @nastechai-research/ui)
    # NOTE: kept as nastechai-research/ui because @nous-research/ui is a REAL
    # published package; the fork hasn't published its own.  Comment this out
    # if/when the fork publishes its own.
    (r"@nous-research/([\w.-]+)",          r"@nastechai-research/\1"),

    # ── Python module / directory names ───────────────────────────────────────
    (r"\bhermes_cli\b",                    "nastech_cli"),
    (r"\bhermes_constants\b",              "nastech_constants"),
    (r"\bhermes_state\b",                  "nastech_state"),
    (r"\bhermes_time\b",                   "nastech_time"),
    (r"\bhermes_logging\b",                "nastech_logging"),
    (r"\bhermes_bootstrap\b",              "nastech_bootstrap"),
    (r"\bhermes_prompt\b",                 "nastech_prompt"),
    (r"\bhermes_meta\b",                   "nastech_meta"),

    # ── Environment variables  (HERMES_FOO  →  NASTECH_FOO) ──────────────────
    # Specific ones first to avoid double-hit from the wildcard below.
    (r"\bHERMES_HOME\b",                   "NASTECH_HOME"),
    (r"\bHERMES_WRITE_SAFE_ROOT\b",        "NASTECH_WRITE_SAFE_ROOT"),
    (r"\bHERMES_OPTIONAL_SKILLS\b",        "NASTECH_OPTIONAL_SKILLS"),
    (r"\bHERMES_CRON_SESSION_DB_TIMEOUT\b","NASTECH_CRON_SESSION_DB_TIMEOUT"),
    (r"\bHERMES_EXEC_ASK\b",               "NASTECH_EXEC_ASK"),
    (r"\bHERMES_UID\b",                    "NASTECH_UID"),
    (r"\bHERMES_GID\b",                    "NASTECH_GID"),
    # Catch-all: any remaining HERMES_* token
    (r"\bHERMES_([A-Z][A-Z0-9_]*)\b",     r"NASTECH_\1"),

    # ── Class / type identifiers ───────────────────────────────────────────────
    (r"\bHermesOverlay\b",                 "NastechOverlay"),
    (r"\bHermesAgent\b",                   "NastechAgent"),
    (r"\bHermesCLI\b",                     "NastechCLI"),
    (r"\bHermesConfig\b",                  "NastechConfig"),
    (r"\bHermesError\b",                   "NastechError"),
    (r"\bHermesEvent\b",                   "NastechEvent"),
    (r"\bHermesSession\b",                 "NastechSession"),

    # ── File-system paths ─────────────────────────────────────────────────────
    (r"~/\.hermes\b",                      "~/.nastech"),
    # .hermes as a path component (surrounded by / or " or ')
    (r"(?<=[\"'/])\.hermes(?=[\"'/\\\n])", ".nastech"),
    # $HOME/.hermes
    (r"\$HOME/\.hermes\b",                 "$HOME/.nastech"),
    # Literal strings inside code: "/root/.hermes", "~/.hermes/config.yaml"
    (r"(?<=[\"'])(/[^\"']*)?/\.hermes\b",  r"\1/.nastech"),

    # ── URLs / domains ─────────────────────────────────────────────────────────
    (r"hermes-agent\.nousresearch\.com",   "nastech-agent.nastechairesearch.com"),
    (r"portal\.nousresearch\.com",         "portal.nastechairesearch.com"),
    (r"docs\.nousresearch\.com",           "docs.nastechairesearch.com"),
    (r"nousresearch\.com",                 "nastechairesearch.com"),
    (r"discord\.gg/NousResearch\b",        "discord.gg/nastechai"),

    # ── Org names ─────────────────────────────────────────────────────────────
    # NousResearch NOT followed by /Hermes- (model IDs) or /hermes- (repo slug already handled above)
    (r"NousResearch(?!/[Hh]ermes)",        "Nastechai Research"),
    (r"Nous Research\b",                   "Nastechai Research"),
    (r"\bnousresearch\b",                  "nastechai"),

    # ── kebab-case identifiers ─────────────────────────────────────────────────
    # CI artefacts / HTML comment markers
    (r"\bhermes-lockfile-diff\b",          "nastech-lockfile-diff"),
    (r"\bhermes-parity\b",                 "nastech-parity"),
    # Named tools / packages
    (r"\bhermes-cli\b",                    "nastech-cli"),
    (r"\bhermes-agent\b",                  "nastech-agent"),
    (r"\bhermes-desktop-plugins\b",        "nastech-desktop-plugins"),
    (r"\bhermes-parser\b",                 "nastech-parser"),
    (r"\bhermes-already-has-routines\b",   "nastech-already-has-routines"),
    # Shell / installer scripts
    (r"\bsetup-hermes\b",                  "setup-nastech"),
    (r"\bhermes-setup\b",                  "nastech-setup"),
    # General kebab-case catch-all: hermes-foo → nastech-foo
    # Guard: NOT followed by digit (protects hermes-3, hermes-2 model names)
    (r"\bhermes-([a-z][a-z0-9-]*)(?![-\d])\b", r"nastech-\1"),

    # ── snake_case identifiers (catch-all after the specific ones above) ───────
    # hermes_foo → nastech_foo  (but only lowercase, to avoid hitting class names)
    (r"\bhermes_([a-z][a-z0-9_]*)\b",     r"nastech_\1"),

    # ── "Hermes" as product name ──────────────────────────────────────────────
    # Must come AFTER all model-name guards (those patterns are longer and
    # more specific, so they were applied earlier in the table).
    #
    # Guard: do NOT replace "Hermes" when:
    #   - followed by -3, -2, 3, 2 (model series numbers)  →  Hermes-3, Hermes3
    #   - followed by :  →  hermes3:70b  (Ollama tag)
    #   - part of NousResearch/Hermes-*  (already handled above)
    #
    # \bHermes\b matches word boundary on both sides, so "Hermes-3" does NOT
    # match (the '-' is not a word boundary on the right, making the \b fail).
    (r"\bHermes\b(?![-:\d])",              "Nastech"),

    # hermes (lowercase) as standalone word — NOT hermes3 or hermes-2 or hermes:
    (r"\bhermes\b(?![-:\d])",              "nastech"),

    # HERMES standalone (after HERMES_* env-var rule consumed the underscored ones)
    (r"\bHERMES\b",                        "NASTECH"),
]

# Compile once at import time.
_COMPILED: list[tuple[re.Pattern[str], str]] = [
    (re.compile(pat), repl) for pat, repl in _RAW_SUBS
]

# Extensions / filenames that must never be text-processed (binary assets).
BINARY_EXTENSIONS: frozenset[str] = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".bmp", ".tiff",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".pdf", ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
    ".mp3", ".mp4", ".wav", ".ogg", ".flac",
    ".exe", ".dll", ".so", ".dylib", ".a",
    ".pyc", ".pyo", ".pyd",
    ".db", ".sqlite", ".sqlite3",
})

# Filenames whose content should be left alone (lockfiles, generated manifests).
SKIP_CONTENT_FILES: frozenset[str] = frozenset({
    "uv.lock",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "Cargo.lock",
})


def apply_branding(content: str) -> str:
    """Return *content* with all Hermes references replaced by Nastech ones."""
    for pattern, repl in _COMPILED:
        content = pattern.sub(repl, content)
    return content


def brand_file_content(path: Path, raw: bytes) -> bytes:
    """Brand file bytes; skip binary files and known lockfiles."""
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return raw
    if path.name in SKIP_CONTENT_FILES:
        return raw
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        # Treat as binary if not valid UTF-8.
        return raw
    branded = apply_branding(text)
    return branded.encode("utf-8")


def brand_commit_message(msg: str) -> str:
    """Brand a git commit message (plain text — no binary guards needed)."""
    return apply_branding(msg)
