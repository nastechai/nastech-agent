# Updates Repository

This is a **staging repository** for synchronizing and rebranding **nastech-agent** (NasTech) as **nastech-agent** (NasTech).

## Purpose

The Updates repository handles:

1. **Syncing** from upstream `nastechai/nastech-agent`
2. **Rebranding** all files, folders, and code to NasTech standards
3. **Verification** of branding compliance
4. **PR Creation** to `nastechai/nastech-agent` with verified changes

## Workflow

```
nastechai/nastech-agent (upstream)
         ↓
    [Fetch commits]
         ↓
nastechai/Updates (this repo)
         ↓
    [Rebrand & Verify]
         ↓
    [Create PR]
         ↓
nastechai/nastech-agent (main repo)
```

## Branding Rules

| Source | Target |
|--------|--------|
| `NasTech` | `NasTech` |
| `nastech` | `nastech` |
| `@nastech-research` | `@nastech-research` |
| `nastechairesearch` | `nastechairesearch` |
| `nastechai` | `nastechai` |

## Workflows

- **sync-and-rebrand.yml** - Syncs upstream, applies branding, creates PR
- **verify-branding.yml** - Verifies branding compliance on PRs

## Setup

See `.github/workflows/` for workflow definitions.

## Status

🚀 Ready for deployment
