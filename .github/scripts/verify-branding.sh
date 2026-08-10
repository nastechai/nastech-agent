#!/usr/bin/env bash
# NasTech Agent Branding Verification Script (High-End v3)
# Comprehensive verification of branding compliance after rebrand.sh runs.
#
# Usage:
#   ./verify-branding.sh [REPO_ROOT]
#   REPO_ROOT – path to the repository root (default: .)
#
# Exit codes:
#   0 – all critical checks passed (warnings are non-fatal)
#   1 – one or more critical checks failed

set -euo pipefail

REPO_ROOT="${1:-.}"

# ── Color helpers ─────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_ok()      { echo -e "${GREEN}[✓]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[⚠]${NC} $*"; }
log_fail()    { echo -e "${RED}[✗]${NC} $*" >&2; }
log_section() { echo -e "\n${BLUE}════════════════════════════════════════${NC}"; \
                echo -e "${CYAN}  $*${NC}"; \
                echo -e "${BLUE}════════════════════════════════════════${NC}"; }

# ── Guard: must be a git repository ──────────────────────────────────────────
if [[ ! -d "$REPO_ROOT/.git" ]]; then
  log_fail "Not a git repository: $REPO_ROOT"
  exit 1
fi

log_ok "Starting branding verification in $REPO_ROOT"

ERRORS=0
WARNINGS=0
CHECKS_PASSED=0

# ── Helper: count files matching a pattern containing a text string ───────────
count_files_with() {
  # $1 = find name pattern(s) as a string passed to -name, $2 = grep pattern
  local result=0
  result=$(
    find "$REPO_ROOT" -type f $1 \
      -not -path "*/.git/*" -not -path "*/node_modules/*" -not -path "*/.venv/*" \
      -exec grep -lIF -- "$2" {} \; 2>/dev/null | wc -l
  ) || result=0
  echo "$result"
}

# ============================================================================
# Check 1: No "nastech-agent" or "NasTech Agent" references in code
# ============================================================================
log_section "Check 1: NasTech product-name references in code"

NASTECH_REFS=$(count_files_with \
  '\( -name "*.json" -o -name "*.py" -o -name "*.js" -o -name "*.ts" \)' \
  "nastech-agent")
NASTECH_REFS2=$(count_files_with \
  '\( -name "*.json" -o -name "*.py" -o -name "*.js" -o -name "*.ts" \)' \
  "NasTech Agent")
TOTAL_HERMES=$(( NASTECH_REFS + NASTECH_REFS2 ))

if [[ "$TOTAL_HERMES" -gt 0 ]]; then
  log_fail "Found $TOTAL_HERMES file(s) with 'nastech-agent' / 'NasTech Agent' references"
  ERRORS=$((ERRORS + 1))
else
  log_ok "No 'nastech-agent' / 'NasTech Agent' references found in code"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 2: No "@nastech-research" npm scope in package.json files
# ============================================================================
log_section "Check 2: npm @nastech-research scope"

NOUS_REFS=$(count_files_with '-name "package.json"' "@nastech-research")

if [[ "$NOUS_REFS" -gt 0 ]]; then
  log_fail "Found $NOUS_REFS package.json file(s) with '@nastech-research'"
  ERRORS=$((ERRORS + 1))
else
  log_ok "No '@nastech-research' references found in package.json files"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 3: No "nastechairesearch/nastech" Docker image references
# ============================================================================
log_section "Check 3: Docker image naming"

DOCKER_REFS=$(count_files_with \
  '\( -name "Dockerfile*" -o -name "*.yml" -o -name "*.yaml" \)' \
  "nastechairesearch/nastech")

if [[ "$DOCKER_REFS" -gt 0 ]]; then
  log_fail "Found $DOCKER_REFS file(s) with 'nastechairesearch/nastech' Docker references"
  ERRORS=$((ERRORS + 1))
else
  log_ok "No 'nastechairesearch/nastech' Docker references found"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 4: No filenames containing "nastech"
# ============================================================================
log_section "Check 4: Filenames with 'nastech'"

NASTECH_FILES=$(
  find "$REPO_ROOT" -type f \( -name "*nastech*" -o -name "*NasTech*" \) \
    -not -path "*/.git/*" 2>/dev/null | wc -l
) || NASTECH_FILES=0

if [[ "$NASTECH_FILES" -gt 0 ]]; then
  log_fail "Found $NASTECH_FILES file(s) with 'nastech' in filename:"
  find "$REPO_ROOT" -type f \( -name "*nastech*" -o -name "*NasTech*" \) \
    -not -path "*/.git/*" 2>/dev/null | head -10
  ERRORS=$((ERRORS + 1))
else
  log_ok "No filenames containing 'nastech' found"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 5: No directories containing "nastech"
# ============================================================================
log_section "Check 5: Directories with 'nastech'"

NASTECH_DIRS=$(
  find "$REPO_ROOT" -type d \( -name "*nastech*" -o -name "*NasTech*" \) \
    -not -path "*/.git/*" 2>/dev/null | wc -l
) || NASTECH_DIRS=0

if [[ "$NASTECH_DIRS" -gt 0 ]]; then
  log_fail "Found $NASTECH_DIRS directory/ies with 'nastech' in name:"
  find "$REPO_ROOT" -type d \( -name "*nastech*" -o -name "*NasTech*" \) \
    -not -path "*/.git/*" 2>/dev/null | head -10
  ERRORS=$((ERRORS + 1))
else
  log_ok "No directories containing 'nastech' found"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 6: Root package.json name (informational if absent)
# ============================================================================
log_section "Check 6: Root package.json name"

if [[ -f "$REPO_ROOT/package.json" ]]; then
  # Use Python for reliable JSON parsing (avoids grep/sed fragility)
  PKG_NAME=$(python3 -c \
    "import json,sys; d=json.load(open('$REPO_ROOT/package.json')); print(d.get('name',''))" \
    2>/dev/null || echo "")

  if [[ "$PKG_NAME" == "nastech-agent" ]]; then
    log_ok "package.json name is correct: $PKG_NAME"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  elif [[ "$PKG_NAME" == *"nastech"* || "$PKG_NAME" == *"NasTech"* ]]; then
    log_fail "package.json name still references NasTech: '$PKG_NAME'"
    ERRORS=$((ERRORS + 1))
  else
    log_warn "package.json name is unexpected: '$PKG_NAME' (expected: nastech-agent)"
    WARNINGS=$((WARNINGS + 1))
  fi
else
  log_warn "No root package.json found (skipping name check)"
  WARNINGS=$((WARNINGS + 1))
fi

# ============================================================================
# Check 7: Repository URL in package.json
# ============================================================================
log_section "Check 7: Repository URL in package.json"

if [[ -f "$REPO_ROOT/package.json" ]]; then
  REPO_URL=$(python3 -c \
    "import json,sys; d=json.load(open('$REPO_ROOT/package.json')); \
     r=d.get('repository',{}); \
     print(r.get('url','') if isinstance(r,dict) else r)" \
    2>/dev/null || echo "")

  if [[ "$REPO_URL" == *"nastechai/nastech-agent"* ]]; then
    log_ok "Repository URL is correct: $REPO_URL"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  elif [[ "$REPO_URL" == *"nastechai/nastech-agent"* ]]; then
    log_fail "Repository URL still points to upstream: $REPO_URL"
    ERRORS=$((ERRORS + 1))
  else
    log_warn "Repository URL is unexpected or absent: '$REPO_URL'"
    WARNINGS=$((WARNINGS + 1))
  fi
fi

# ============================================================================
# Check 8: @nastech-research npm scope presence (informational)
# ============================================================================
log_section "Check 8: @nastech-research npm scope"

NASTECH_REFS=$(count_files_with '-name "package.json"' "@nastech-research")

if [[ "$NASTECH_REFS" -gt 0 ]]; then
  log_ok "Found @nastech-research in $NASTECH_REFS package.json file(s)"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
  log_warn "No @nastech-research references found (expected only if npm packages are used)"
  WARNINGS=$((WARNINGS + 1))
fi

# ============================================================================
# Check 9: nastechairesearch Docker org presence (informational)
# ============================================================================
log_section "Check 9: nastechairesearch Docker org"

NASTECH_DOCKER=$(count_files_with \
  '\( -name "Dockerfile*" -o -name "*.yml" -o -name "*.yaml" \)' \
  "nastechairesearch")

if [[ "$NASTECH_DOCKER" -gt 0 ]]; then
  log_ok "Found nastechairesearch in $NASTECH_DOCKER file(s)"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
  log_warn "No nastechairesearch Docker references found (expected only if Docker images are published)"
  WARNINGS=$((WARNINGS + 1))
fi

# ============================================================================
# Check 10: npm audit (runs in a subshell to avoid cwd side-effects)
# ============================================================================
log_section "Check 10: npm audit"

if [[ -f "$REPO_ROOT/package.json" ]] && command -v npm &>/dev/null; then
  AUDIT_EXIT=0
  (cd "$REPO_ROOT" && npm audit --json 2>/dev/null) | python3 -c \
    "import json,sys
data=json.load(sys.stdin)
vulns=data.get('metadata',{}).get('vulnerabilities',{})
total=sum(vulns.values()) if isinstance(vulns,dict) else 0
sys.exit(0 if total==0 else 1)" 2>/dev/null || AUDIT_EXIT=$?

  if [[ "$AUDIT_EXIT" -eq 0 ]]; then
    log_ok "npm audit: no vulnerabilities found"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  else
    log_warn "npm audit found vulnerabilities — review 'npm audit' output for details"
    WARNINGS=$((WARNINGS + 1))
  fi
else
  log_warn "Skipping npm audit (no package.json or npm not available)"
  WARNINGS=$((WARNINGS + 1))
fi

# ============================================================================
# SUMMARY
# ============================================================================
log_section "Verification Summary"

TOTAL_CHECKS=$((CHECKS_PASSED + WARNINGS + ERRORS))
log_ok  "Checks passed : $CHECKS_PASSED / $TOTAL_CHECKS"
[[ "$WARNINGS" -gt 0 ]] && log_warn "Warnings      : $WARNINGS"
[[ "$ERRORS"   -gt 0 ]] && log_fail "Errors        : $ERRORS"

if [[ "$ERRORS" -eq 0 ]]; then
  log_ok "✓ All critical checks passed!"
  exit 0
else
  log_fail "✗ Verification failed with $ERRORS critical error(s)"
  exit 1
fi
