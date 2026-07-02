# Langfuse Observability Plugin

This plugin ships bundled with Nastech but is **opt-in** — it only loads when
you explicitly enable it.

## Enable

Pick one:

```bash
# Interactive: walks you through credentials + SDK install + enable
nastech tools  # → Langfuse Observability

# Manual
pip install langfuse
nastech plugins enable observability/langfuse
```

## Required credentials

Set these in `~/.nastech/.env` (or via `nastech tools`):

```bash
NASTECH_LANGFUSE_PUBLIC_KEY=pk-lf-...
NASTECH_LANGFUSE_SECRET_KEY=sk-lf-...
NASTECH_LANGFUSE_BASE_URL=https://cloud.langfuse.com   # or your self-hosted URL
```

Without the SDK or credentials the hooks no-op silently — the plugin fails
open.

## Verify

```bash
nastech plugins list                 # observability/langfuse should show "enabled"
nastech chat -q "hello"              # then check Langfuse for a "Nastech turn" trace
```

## Optional tuning

```bash
NASTECH_LANGFUSE_ENV=production       # environment tag
NASTECH_LANGFUSE_RELEASE=v1.0.0       # release tag
NASTECH_LANGFUSE_SAMPLE_RATE=0.5      # sample 50% of traces
NASTECH_LANGFUSE_MAX_CHARS=12000      # max chars per field (default: 12000)
NASTECH_LANGFUSE_DEBUG=true           # verbose plugin logging
```

## Disable

```bash
nastech plugins disable observability/langfuse
```
