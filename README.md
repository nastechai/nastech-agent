# NasTech Updates Repository

> **High-End Branding Transformation System**  
> Production-grade automation for syncing and rebranding NasTech → NasTech across 40+ ecosystems

---

## 📋 Overview

This repository is a **staging hub** for synchronizing and rebranding **nastech-agent** (NasTech) as **nastech-agent** (NasTech). It implements a comprehensive, multi-stage branding transformation system that handles:

- ✅ **Content transformation** across all file types
- ✅ **File/directory renaming** with dependency tracking
- ✅ **40+ ecosystem validators** (Python, Node.js, Go, Rust, Java, Ruby, PHP, .NET, Docker, Kubernetes, etc.)
- ✅ **npm package management** validation and transformation
- ✅ **Docker/container** image and configuration validation
- ✅ **Configuration files** (YAML, TOML, JSON, INI, environment)
- ✅ **CI/CD pipelines** (GitHub Actions, GitLab CI, CircleCI, Jenkins, etc.)
- ✅ **Infrastructure-as-Code** (Terraform, Ansible, Helm, Kubernetes)
- ✅ **Build systems** (Make, CMake, Bazel, Gradle, Maven, etc.)
- ✅ **Documentation** and markdown files
- ✅ **Git-aware** diff tracking and reporting

---

## 🏗️ Architecture

### Workflow

```
nastechai/nastech-agent (upstream)
         ↓
    [Fetch commits]
         ↓
nastechai/Updates (this repo)
         ↓
    [Orchestrator]
         ├─→ Content Transformation (Python)
         ├─→ File/Directory Renaming (Bash)
         ├─→ npm Validation (Node.js)
         ├─→ Docker Validation (Bash)
         ├─→ Config Validation (Python)
         ├─→ Ecosystem Validation (Python)
         └─→ Final Verification (Python)
         ↓
    [Create PR]
         ↓
nastechai/nastech-agent (main repo)
```

### Components

| Component | Language | Purpose |
|-----------|----------|---------|
| `branding-orchestrator.sh` | Bash | Master orchestrator; coordinates all validators |
| `branding_engine.py` | Python | Core transformation engine; handles all file types |
| `validate-npm-branding.js` | Node.js | npm/package manager ecosystem validator |
| `validate-docker-branding.sh` | Bash | Docker/container ecosystem validator |
| `validate-config-branding.py` | Python | Configuration files (YAML, TOML, JSON, INI) |
| `validate-ecosystem-branding.py` | Python | 40+ language/framework ecosystems |
| `rebrand.sh` | Bash | Legacy text-based rebrand script (enhanced v3) |
| `verify-branding.sh` | Bash | Legacy branding verification (enhanced v3) |

---

## 🎯 Supported Ecosystems (40+)

### Languages & Runtimes
- **Python**: setup.py, pyproject.toml, requirements.txt, Pipfile, poetry.lock, tox.ini
- **Node.js**: package.json, package-lock.json, yarn.lock, pnpm-lock.yaml, .npmrc
- **Go**: go.mod, go.sum, *.go files
- **Rust**: Cargo.toml, Cargo.lock
- **Java**: pom.xml, build.gradle, gradle.properties, settings.gradle
- **Ruby**: Gemfile, Gemfile.lock, .gemrc
- **PHP**: composer.json, composer.lock
- **.NET**: .csproj, .fsproj, .vbproj, packages.config
- **Kotlin**: build.gradle.kts
- **Scala**: build.sbt
- **Clojure**: project.clj, deps.edn
- **Elixir**: mix.exs, mix.lock
- **Haskell**: cabal.project, stack.yaml
- **R**: DESCRIPTION, renv.lock
- **Perl**: Makefile.PL, cpanfile
- **Swift**: Package.swift

### Build Systems
- **Make**: Makefile, makefile
- **CMake**: CMakeLists.txt
- **Bazel**: BUILD, BUILD.bazel, WORKSPACE
- **Maven**: pom.xml
- **Gradle**: build.gradle, gradle.properties
- **SBT**: build.sbt
- **Ant**: build.xml

### CI/CD Platforms
- **GitHub Actions**: .github/workflows/*.yml
- **GitLab CI**: .gitlab-ci.yml
- **CircleCI**: .circleci/config.yml
- **Jenkins**: Jenkinsfile
- **Travis CI**: .travis.yml
- **Azure Pipelines**: azure-pipelines.yml

### Infrastructure & DevOps
- **Docker**: Dockerfile, docker-compose.yml, .dockerignore
- **Kubernetes**: *.yaml, *.yml in k8s/
- **Terraform**: *.tf files
- **Ansible**: playbooks, roles
- **Helm**: Chart.yaml, values.yaml

### Configuration & Docs
- **YAML**: *.yml, *.yaml
- **TOML**: *.toml (pyproject.toml, Cargo.toml, etc.)
- **JSON**: *.json (package.json, tsconfig.json, etc.)
- **INI**: *.ini, *.conf, .env files
- **Markdown**: *.md, README files

### Web Technologies
- **HTML**: *.html
- **CSS/SCSS/LESS**: *.css, *.scss, *.less
- **JavaScript**: *.js
- **TypeScript**: *.ts, *.tsx
- **Vue**: *.vue
- **React**: *.jsx

---

## 🚀 Usage

### Prerequisites

```bash
# Required
- bash (4.0+)
- git
- python3 (3.7+)
- node.js (12+)

# Optional (for specific ecosystems)
- Go, Rust, Java, Ruby, PHP, etc.
```

### Installation

```bash
# Clone the repository
git clone https://github.com/nastechai/Updates.git
cd Updates

# Make scripts executable
chmod +x .github/scripts/*.sh
chmod +x .github/scripts/*.py
chmod +x .github/scripts/*.js
```

### Quick Start

#### Full Transformation (Recommended)

```bash
# Transform everything (content, files, directories, all ecosystems)
./.github/scripts/branding-orchestrator.sh --repo . --mode transform

# Dry-run (preview changes without writing)
./.github/scripts/branding-orchestrator.sh --repo . --mode transform --dry-run

# Parallel execution (faster)
./.github/scripts/branding-orchestrator.sh --repo . --mode transform --parallel
```

#### Validation Only

```bash
# Validate branding compliance
./.github/scripts/branding-orchestrator.sh --repo . --mode validate

# Generate detailed report
./.github/scripts/branding-orchestrator.sh --repo . --mode report
```

#### Individual Validators

```bash
# Python engine (core transformation)
python3 .github/scripts/branding_engine.py --repo . --mode transform --fix

# npm ecosystem
node .github/scripts/validate-npm-branding.js --repo . --fix

# Docker ecosystem
bash .github/scripts/validate-docker-branding.sh . true

# Configuration files
python3 .github/scripts/validate-config-branding.py --repo . --fix

# All 40+ ecosystems
python3 .github/scripts/validate-ecosystem-branding.py --repo . --fix
```

---

## 🔧 Branding Rules

All transformations follow these rules (applied in priority order):

| Source | Target | Priority | Context |
|--------|--------|----------|---------|
| `github.com/nastechai/nastech-agent` | `github.com/nastechai/nastech-agent` | 100 | URLs |
| `nastechairesearch/nastech` | `nastechairesearch/nastech` | 95 | Docker |
| `NasTech Agent` | `NasTech Agent` | 90 | Product names |
| `nastech-agent` | `nastech-agent` | 90 | Package names |
| `@nastech-research` | `@nastech-research` | 85 | npm scopes |
| `NasTech` | `NasTech` | 80 | Organization |
| `nastechai` | `nastechai` | 80 | GitHub org |
| `nastechairesearch` | `nastechairesearch` | 80 | Docker org |
| `NASTECH_` | `NASTECH_` | 75 | Environment vars |
| `/opt/nastech` | `/opt/nastech` | 75 | Paths |
| `NasTech` | `NasTech` | 50 | Generic |
| `nastech` | `nastech` | 50 | Generic |

**Priority matters**: Longer, more-specific patterns are applied first to prevent partial replacements.

---

## 📊 Features

### ✨ Advanced Capabilities

- **AST-based transformation**: Preserves code structure and formatting
- **Safe replacements**: Escapes regex special characters; prevents injection
- **Dependency tracking**: Renames files/dirs deepest-first to avoid broken paths
- **Dry-run mode**: Preview all changes before committing
- **Parallel execution**: Run multiple validators concurrently
- **Detailed reporting**: Per-file, per-ecosystem statistics
- **Git integration**: Automatic diff summary and change tracking
- **Error handling**: Graceful fallbacks; continues on individual file failures
- **Idempotent**: Safe to run multiple times; skips already-transformed content

### 🎯 Quality Assurance

- **Multi-stage validation**: Content → Files → Ecosystems → Final verification
- **Comprehensive checks**: NasTech refs, Docker images, npm scopes, paths, env vars
- **Context-aware**: Different rules for different file types
- **Logging**: Full audit trail in timestamped log files
- **Exit codes**: Proper status codes for CI/CD integration

---

## 🔄 Workflow Integration

### GitHub Actions (auto-sync-test-rebrand-pr.yml)

Runs automatically:
- **Daily** at 02:00 UTC
- **On push** to main (when scripts change)
- **On workflow_dispatch** (manual trigger)
- **On repository_dispatch** (webhook from upstream monitor)

```yaml
# Triggers sync, rebrand, verify, and creates PR to nastech-agent
jobs:
  sync-test-rebrand-pr:
    steps:
      - Checkout Updates repo
      - Fetch upstream (nastechai/nastech-agent)
      - Apply branding transformations
      - Verify compliance
      - Create PR to nastechai/nastech-agent
```

### Issue Tracker (issue-tracker.yml)

Maintains a single tracking issue with:
- Latest sync status
- Run history
- Failure notifications

---

## 🔐 Secrets & Configuration

### Required Secrets

Set these in your GitHub repository settings:

```
NAS_TOKEN          # GitHub token with repo access to nastechai/nastech-agent
                   # Fallback: uses GITHUB_TOKEN if not set
```

### Optional Configuration

Create `.github/branding.config` (JSON):

```json
{
  "upstream_repo": "nastechai/nastech-agent",
  "upstream_branch": "main",
  "target_repo": "nastechai/nastech-agent",
  "target_branch": "main",
  "sync_schedule": "0 2 * * *",
  "dry_run": false,
  "parallel": true,
  "ecosystems": ["python", "nodejs", "go", "rust", "docker"]
}
```

---

## 📈 Metrics & Reporting

### Generated Reports

Each run produces:

```
/tmp/branding-orchestrator-YYYYMMDD-HHMMSS.log
├── Phase 1: Content Transformation
│   ├── Files scanned: N
│   ├── Files modified: N
│   └── Total replacements: N
├── Phase 2: File/Directory Renaming
│   └── Items renamed: N
├── Phase 3: npm Validation
│   ├── Violations: N
│   └── Transformations: N
├── Phase 4: Docker Validation
│   ├── Violations: N
│   └── Transformations: N
├── Phase 5: Configuration Validation
│   ├── Violations: N
│   └── Transformations: N
├── Phase 6: Ecosystem Validation (40+)
│   ├── Violations: N
│   └── Transformations: N
└── Phase 7: Final Verification
    └── Status: PASS/FAIL
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `Not a git repository` | Ensure `.git` directory exists; run from repo root |
| `Permission denied` | Run `chmod +x .github/scripts/*.sh` |
| `Python3 not found` | Install Python 3.7+; or skip Python-based validators |
| `Node.js not found` | Install Node.js 12+; or skip npm validator |
| `Merge conflict` | Workflow aborts; manual resolution required |
| `Dry-run doesn't match actual` | Check file permissions; some files may be read-only |

### Debug Mode

```bash
# Enable verbose output
bash -x .github/scripts/branding-orchestrator.sh --repo . --mode transform

# Check individual log file
tail -f /tmp/branding-orchestrator-*.log
```

---

## 📚 Documentation

- **[Branding Rules](./docs/BRANDING_RULES.md)** — Detailed rule definitions
- **[Architecture](./docs/ARCHITECTURE.md)** — System design and components
- **[API Reference](./docs/API.md)** — Script interfaces and options
- **[Examples](./docs/EXAMPLES.md)** — Common use cases

---

## 🤝 Contributing

To improve the branding system:

1. **Add new ecosystem**: Edit `validate-ecosystem-branding.py`
2. **Add new rule**: Update `BRANDING_RULES` in any validator
3. **Improve validation**: Enhance checks in individual validators
4. **Report issues**: Create an issue with details and logs

---

## 📝 License

This repository is part of the NasTech project. See LICENSE for details.

---

## 🎓 Status

| Component | Status | Coverage |
|-----------|--------|----------|
| Content Transformation | ✅ Production | All file types |
| File Renaming | ✅ Production | Deepest-first ordering |
| npm Ecosystem | ✅ Production | package.json, lock files, scopes |
| Docker Ecosystem | ✅ Production | Dockerfile, compose, registries |
| Configuration Files | ✅ Production | YAML, TOML, JSON, INI, .env |
| 40+ Ecosystems | ✅ Production | Python, Go, Rust, Java, Ruby, PHP, .NET, etc. |
| CI/CD Integration | ✅ Production | GitHub Actions, GitLab CI, CircleCI, etc. |
| Verification | ✅ Production | Multi-stage validation |
| Reporting | ✅ Production | Detailed metrics and logs |

---

## 🚀 Ready for Production

**Status**: ✅ Ready for deployment  
**Last Updated**: 2026-08-10  
**Version**: 3.0 (High-End)

---

## 📞 Support

For issues or questions:
- Check the [troubleshooting guide](#-troubleshooting)
- Review [examples](./docs/EXAMPLES.md)
- Open an issue on GitHub
- Contact: sync@nastechai.dev
