#!/bin/bash
# NasTech Agent Branding Verification Script (Enhanced v2)
# Comprehensive verification of branding compliance

set -euo pipefail

REPO_ROOT="${1:-.}"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[✓]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[⚠]${NC} $*"; }
log_error() { echo -e "${RED}[✗]${NC} $*"; }
log_section() { echo -e "\n${BLUE}=== $* ===${NC}"; }

if [ ! -d "$REPO_ROOT/.git" ]; then
  log_error "Not a git repository: $REPO_ROOT"
  exit 1
fi

log_info "Starting branding verification in $REPO_ROOT"

ERRORS=0
WARNINGS=0
CHECKS_PASSED=0

# ============================================================================
# Check 1: No "NasTech" references in code
# ============================================================================
log_section "Check 1: NasTech references in code"

NASTECH_REFS=$(find "$REPO_ROOT" -type f \( -name "*.json" -o -name "*.py" -o -name "*.js" -o -name "*.ts" \) \
  -not -path "*/.git/*" -not -path "*/node_modules/*" -not -path "*/.venv/*" \
  -exec grep -l "nastech-agent\|NasTech Agent" {} \; 2>/dev/null | wc -l || echo 0)

if [ "$NASTECH_REFS" -gt 0 ]; then
  log_error "Found $NASTECH_REFS files with 'NasTech' references"
  ERRORS=$((ERRORS + 1))
else
  log_info "No 'NasTech' references found"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 2: No "@nastech-research" in npm packages
# ============================================================================
log_section "Check 2: npm @nastech-research scope"

NOUS_REFS=$(find "$REPO_ROOT" -type f -name "package.json" \
  -not -path "*/.git/*" -not -path "*/node_modules/*" \
  -exec grep -l "@nastech-research" {} \; 2>/dev/null | wc -l || echo 0)

if [ "$NOUS_REFS" -gt 0 ]; then
  log_error "Found $NOUS_REFS package.json files with '@nastech-research'"
  ERRORS=$((ERRORS + 1))
else
  log_info "No '@nastech-research' references found"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 3: Verify @nastech-research usage
# ============================================================================
log_section "Check 3: npm @nastech-research scope"

NASTECH_REFS=$(find "$REPO_ROOT" -type f -name "package.json" \
  -not -path "*/.git/*" -not -path "*/node_modules/*" \
  -exec grep -l "@nastech-research" {} \; 2>/dev/null | wc -l || echo 0)

if [ "$NASTECH_REFS" -gt 0 ]; then
  log_info "Found @nastech-research in $NASTECH_REFS package.json files"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
  log_warn "No @nastech-research references found (may be expected)"
  WARNINGS=$((WARNINGS + 1))
fi

# ============================================================================
# Check 4: No "nastechairesearch" Docker references
# ============================================================================
log_section "Check 4: Docker image naming"

DOCKER_REFS=$(find "$REPO_ROOT" -type f \( -name "Dockerfile*" -o -name "*.yml" -o -name "*.yaml" \) \
  -not -path "*/.git/*" \
  -exec grep -l "nastechairesearch/nastech" {} \; 2>/dev/null | wc -l || echo 0)

if [ "$DOCKER_REFS" -gt 0 ]; then
  log_error "Found $DOCKER_REFS files with 'nastechairesearch/nastech' Docker references"
  ERRORS=$((ERRORS + 1))
else
  log_info "No 'nastechairesearch/nastech' Docker references found"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 5: Verify nastechairesearch Docker org
# ============================================================================
log_section "Check 5: nastechairesearch Docker org"

NASTECH_DOCKER=$(find "$REPO_ROOT" -type f \( -name "Dockerfile*" -o -name "*.yml" -o -name "*.yaml" \) \
  -not -path "*/.git/*" \
  -exec grep -l "nastechairesearch" {} \; 2>/dev/null | wc -l || echo 0)

if [ "$NASTECH_DOCKER" -gt 0 ]; then
  log_info "Found nastechairesearch in $NASTECH_DOCKER files"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
  log_warn "No nastechairesearch Docker references found (may be expected)"
  WARNINGS=$((WARNINGS + 1))
fi

# ============================================================================
# Check 6: Verify package.json name
# ============================================================================
log_section "Check 6: Root package.json name"

if [ -f "$REPO_ROOT/package.json" ]; then
  PKG_NAME=$(grep '"name"' "$REPO_ROOT/package.json" | head -1 | grep -o '"[^"]*"' | tr -d '"' || echo "")
  if [ "$PKG_NAME" = "nastech-agent" ]; then
    log_info "package.json name is correct: $PKG_NAME"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  else
    log_error "package.json name is incorrect: $PKG_NAME (expected: nastech-agent)"
    ERRORS=$((ERRORS + 1))
  fi
else
  log_warn "No root package.json found"
  WARNINGS=$((WARNINGS + 1))
fi

# ============================================================================
# Check 7: Verify repository URL
# ============================================================================
log_section "Check 7: Repository URL"

if [ -f "$REPO_ROOT/package.json" ]; then
  REPO_URL=$(grep -o '"url"[^}]*' "$REPO_ROOT/package.json" | head -1 | grep -o 'github.com[^"]*' || echo "")
  if [[ "$REPO_URL" == *"nastechai/nastech-agent"* ]]; then
    log_info "Repository URL is correct: $REPO_URL"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  elif [[ "$REPO_URL" == *"nastechai/nastech-agent"* ]]; then
    log_error "Repository URL still points to upstream: $REPO_URL"
    ERRORS=$((ERRORS + 1))
  else
    log_warn "Repository URL is unexpected: $REPO_URL"
    WARNINGS=$((WARNINGS + 1))
  fi
fi

# ============================================================================
# Check 8: No filenames with "nastech"
# ============================================================================
log_section "Check 8: Filenames with 'nastech'"

NASTECH_FILES=$(find "$REPO_ROOT" -type f \( -name "*nastech*" -o -name "*NasTech*" \) \
  -not -path "*/.git/*" 2>/dev/null | wc -l || echo 0)

if [ "$NASTECH_FILES" -gt 0 ]; then
  log_error "Found $NASTECH_FILES files with 'nastech' in filename"
  find "$REPO_ROOT" -type f \( -name "*nastech*" -o -name "*NasTech*" \) \
    -not -path "*/.git/*" 2>/dev/null | head -5
  ERRORS=$((ERRORS + 1))
else
  log_info "No filenames with 'nastech' found"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 9: No directories with "nastech"
# ============================================================================
log_section "Check 9: Directories with 'nastech'"

NASTECH_DIRS=$(find "$REPO_ROOT" -type d \( -name "*nastech*" -o -name "*NasTech*" \) \
  -not -path "*/.git/*" 2>/dev/null | wc -l || echo 0)

if [ "$NASTECH_DIRS" -gt 0 ]; then
  log_error "Found $NASTECH_DIRS directories with 'nastech' in name"
  find "$REPO_ROOT" -type d \( -name "*nastech*" -o -name "*NasTech*" \) \
    -not -path "*/.git/*" 2>/dev/null | head -5
  ERRORS=$((ERRORS + 1))
else
  log_info "No directories with 'nastech' found"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# ============================================================================
# Check 10: npm audit (informational)
# ============================================================================
log_section "Check 10: npm audit"

if [ -f "$REPO_ROOT/package.json" ] && command -v npm &> /dev/null; then
  cd "$REPO_ROOT"
  AUDIT_RESULT=$(npm audit --json 2>/dev/null | grep -o '"vulnerabilities"' | wc -l || echo 0)
  if [ "$AUDIT_RESULT" -gt 0 ]; then
    log_warn "npm audit found issues (review logs for details)"
    WARNINGS=$((WARNINGS + 1))
  else
    log_info "npm audit passed"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  fi
fi

# ============================================================================
# SUMMARY
# ============================================================================
log_section "Verification Summary"

TOTAL_CHECKS=$((CHECKS_PASSED + WARNINGS + ERRORS))
log_info "Checks passed: $CHECKS_PASSED/$TOTAL_CHECKS"
[ "$WARNINGS" -gt 0 ] && log_warn "Warnings: $WARNINGS"
[ "$ERRORS" -gt 0 ] && log_error "Errors: $ERRORS"

if [ "$ERRORS" -eq 0 ]; then
  log_info "✓ All critical checks passed!"
  exit 0
else
  log_error "✗ Verification failed with $ERRORS errors"
  exit 1
fi
