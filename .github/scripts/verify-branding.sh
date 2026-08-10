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
# Check 1: No "hermes-agent" or "Hermes Agent" references in code
# ============================================================================
log_section "Check 1: Hermes product-name references in code"

HERMES_REFS=$(count_files_with \
  '\( -name "*.json" -o -name "*.py" -o -name "*.js" -o -name "*.ts" \)' \
  "hermes-agent")
HERMES_REFS2=$(count_files_with \
  '\( -name "*.json" -o -name "*.py" -o -name "*.js" -o -name "*.ts" \)' \
  "Hermes Agent")
TOTAL_HERMES=$(( HERMES_REFS + HERMES_REFS2 ))

if [[ "$TOTAL_HERMES" -gt 0 ]]; then
  log_fail "Found $TOTAL_HERMES file(s) with 'hermes-agent' / 'Hermes Agent' references"
  ERRORS=$((ERRORS + 1))
else
  log_ok "No 'hermes-agent' / 'Hermes Agent' references found in code"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 2: No "@nous-research" npm scope in package.json files
# ============================================================================
log_section "Check 2: npm @nous-research scope"

NOUS_REFS=$(count_files_with '-name "package.json"' "@nous-research")

if [[ "$NOUS_REFS" -gt 0 ]]; then
  log_fail "Found $NOUS_REFS package.json file(s) with '@nous-research'"
  ERRORS=$((ERRORS + 1))
else
  log_ok "No '@nous-research' references found in package.json files"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 3: No "nousresearch/hermes" Docker image references
# ============================================================================
log_section "Check 3: Docker image naming"

DOCKER_REFS=$(count_files_with \
  '\( -name "Dockerfile*" -o -name "*.yml" -o -name "*.yaml" \)' \
  "nousresearch/hermes")

if [[ "$DOCKER_REFS" -gt 0 ]]; then
  log_fail "Found $DOCKER_REFS file(s) with 'nousresearch/hermes' Docker references"
  ERRORS=$((ERRORS + 1))
else
  log_ok "No 'nousresearch/hermes' Docker references found"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 4: No filenames containing "hermes"
# ============================================================================
log_section "Check 4: Filenames with 'hermes'"

HERMES_FILES=$(
  find "$REPO_ROOT" -type f \( -name "*hermes*" -o -name "*Hermes*" \) \
    -not -path "*/.git/*" 2>/dev/null | wc -l
) || HERMES_FILES=0

if [[ "$HERMES_FILES" -gt 0 ]]; then
  log_fail "Found $HERMES_FILES file(s) with 'hermes' in filename:"
  find "$REPO_ROOT" -type f \( -name "*hermes*" -o -name "*Hermes*" \) \
    -not -path "*/.git/*" 2>/dev/null | head -10
  ERRORS=$((ERRORS + 1))
else
  log_ok "No filenames containing 'hermes' found"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 5: No directories containing "hermes"
# ============================================================================
log_section "Check 5: Directories with 'hermes'"

HERMES_DIRS=$(
  find "$REPO_ROOT" -type d \( -name "*hermes*" -o -name "*Hermes*" \) \
    -not -path "*/.git/*" 2>/dev/null | wc -l
) || HERMES_DIRS=0

if [[ "$HERMES_DIRS" -gt 0 ]]; then
  log_fail "Found $HERMES_DIRS directory/ies with 'hermes' in name:"
  find "$REPO_ROOT" -type d \( -name "*hermes*" -o -name "*Hermes*" \) \
    -not -path "*/.git/*" 2>/dev/null | head -10
  ERRORS=$((ERRORS + 1))
else
  log_ok "No directories containing 'hermes' found"
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
  elif [[ "$PKG_NAME" == *"hermes"* || "$PKG_NAME" == *"Hermes"* ]]; then
    log_fail "package.json name still references Hermes: '$PKG_NAME'"
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
  elif [[ "$REPO_URL" == *"NousResearch/hermes-agent"* ]]; then
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
