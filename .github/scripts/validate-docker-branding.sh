#!/usr/bin/env bash
# NasTech Docker Branding Validator (v3.0)
# 
# Validates and transforms Docker-related branding:
# - Dockerfile base images
# - docker-compose.yml services
# - .dockerignore patterns
# - GitHub Actions Docker steps
# - Container registry references
#
# Usage:
#   ./validate-docker-branding.sh [--repo ROOT] [--fix] [--report]

set -euo pipefail

REPO_ROOT="${1:-.}"
FIX="${2:-false}"
REPORT="${3:-false}"

# ─────────────────────────────────────────────────────────────────────────────
# Colors
# ─────────────────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_ok()      { echo -e "${GREEN}[✓]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[⚠]${NC} $*" >&2; }
log_fail()    { echo -e "${RED}[✗]${NC} $*" >&2; }
log_info()    { echo -e "${BLUE}[•]${NC} $*"; }
log_section() { echo -e "\n${CYAN}════════════════════════════════════════${NC}"; \
                echo -e "${CYAN}  $*${NC}"; \
                echo -e "${CYAN}════════════════════════════════════════${NC}"; }

# ─────────────────────────────────────────────────────────────────────────────
# Counters
# ─────────────────────────────────────────────────────────────────────────────
VIOLATIONS=0
TRANSFORMATIONS=0

# ─────────────────────────────────────────────────────────────────────────────
# Dockerfile Validation
# ─────────────────────────────────────────────────────────────────────────────
validate_dockerfiles() {
  log_section "Dockerfile Validation"

  while IFS= read -r -d '' dockerfile; do
    [[ -z "$dockerfile" ]] && continue

    log_info "Checking: $dockerfile"

    # Check for nousresearch/hermes base images
    if grep -qE "FROM.*nousresearch/hermes" "$dockerfile" 2>/dev/null; then
      log_warn "  Found nousresearch/hermes base image"
      VIOLATIONS=$((VIOLATIONS + 1))

      if [[ "$FIX" == "true" ]]; then
        sed -i 's|nousresearch/hermes|nastechairesearch/nastech|g' "$dockerfile"
        sed -i 's|nousresearch/hermes-agent|nastechairesearch/nastech-agent|g' "$dockerfile"
        log_ok "  Fixed base image references"
        TRANSFORMATIONS=$((TRANSFORMATIONS + 1))
      fi
    fi

    # Check for HERMES environment variables
    if grep -qE "ENV.*HERMES_|ARG.*HERMES_" "$dockerfile" 2>/dev/null; then
      log_warn "  Found HERMES_ environment variables"
      VIOLATIONS=$((VIOLATIONS + 1))

      if [[ "$FIX" == "true" ]]; then
        sed -i 's/HERMES_/NASTECH_/g' "$dockerfile"
        log_ok "  Fixed environment variables"
        TRANSFORMATIONS=$((TRANSFORMATIONS + 1))
      fi
    fi

    # Check for /opt/hermes paths
    if grep -qE "/opt/hermes" "$dockerfile" 2>/dev/null; then
      log_warn "  Found /opt/hermes path references"
      VIOLATIONS=$((VIOLATIONS + 1))

      if [[ "$FIX" == "true" ]]; then
        sed -i 's|/opt/hermes|/opt/nastech|g' "$dockerfile"
        log_ok "  Fixed path references"
        TRANSFORMATIONS=$((TRANSFORMATIONS + 1))
      fi
    fi

  done < <(
    find "$REPO_ROOT" \
      -type f \( -name "Dockerfile*" -o -name "*.dockerfile" \) \
      -not -path "*/.git/*" -print0 2>/dev/null
  )
}

# ─────────────────────────────────────────────────────────────────────────────
# Docker Compose Validation
# ─────────────────────────────────────────────────────────────────────────────
validate_docker_compose() {
  log_section "Docker Compose Validation"

  while IFS= read -r -d '' compose_file; do
    [[ -z "$compose_file" ]] && continue

    log_info "Checking: $compose_file"

    # Check for nousresearch/hermes images
    if grep -qE "image:.*nousresearch/hermes" "$compose_file" 2>/dev/null; then
      log_warn "  Found nousresearch/hermes image references"
      VIOLATIONS=$((VIOLATIONS + 1))

      if [[ "$FIX" == "true" ]]; then
        sed -i 's|nousresearch/hermes|nastechairesearch/nastech|g' "$compose_file"
        sed -i 's|nousresearch/hermes-agent|nastechairesearch/nastech-agent|g' "$compose_file"
        log_ok "  Fixed image references"
        TRANSFORMATIONS=$((TRANSFORMATIONS + 1))
      fi
    fi

    # Check for HERMES environment variables
    if grep -qE "HERMES_" "$compose_file" 2>/dev/null; then
      log_warn "  Found HERMES_ environment variables"
      VIOLATIONS=$((VIOLATIONS + 1))

      if [[ "$FIX" == "true" ]]; then
        sed -i 's/HERMES_/NASTECH_/g' "$compose_file"
        log_ok "  Fixed environment variables"
        TRANSFORMATIONS=$((TRANSFORMATIONS + 1))
      fi
    fi

  done < <(
    find "$REPO_ROOT" \
      -type f \( -name "docker-compose*.yml" -o -name "docker-compose*.yaml" \) \
      -not -path "*/.git/*" -print0 2>/dev/null
  )
}

# ─────────────────────────────────────────────────────────────────────────────
# GitHub Actions Validation
# ─────────────────────────────────────────────────────────────────────────────
validate_github_actions() {
  log_section "GitHub Actions Workflow Validation"

  while IFS= read -r -d '' workflow; do
    [[ -z "$workflow" ]] && continue

    log_info "Checking: $workflow"

    # Check for nousresearch/hermes Docker steps
    if grep -qE "nousresearch/hermes" "$workflow" 2>/dev/null; then
      log_warn "  Found nousresearch/hermes Docker references"
      VIOLATIONS=$((VIOLATIONS + 1))

      if [[ "$FIX" == "true" ]]; then
        sed -i 's|nousresearch/hermes|nastechairesearch/nastech|g' "$workflow"
        sed -i 's|nousresearch/hermes-agent|nastechairesearch/nastech-agent|g' "$workflow"
        log_ok "  Fixed Docker references"
        TRANSFORMATIONS=$((TRANSFORMATIONS + 1))
      fi
    fi

  done < <(
    find "$REPO_ROOT/.github/workflows" \
      -type f \( -name "*.yml" -o -name "*.yaml" \) \
      -print0 2>/dev/null
  )
}

# ─────────────────────────────────────────────────────────────────────────────
# .dockerignore Validation
# ─────────────────────────────────────────────────────────────────────────────
validate_dockerignore() {
  log_section ".dockerignore Validation"

  while IFS= read -r -d '' dockerignore; do
    [[ -z "$dockerignore" ]] && continue

    log_info "Checking: $dockerignore"

    # Check for hermes-related patterns
    if grep -qE "hermes|Hermes" "$dockerignore" 2>/dev/null; then
      log_warn "  Found hermes-related patterns"
      VIOLATIONS=$((VIOLATIONS + 1))

      if [[ "$FIX" == "true" ]]; then
        sed -i 's/hermes/nastech/g; s/Hermes/NasTech/g' "$dockerignore"
        log_ok "  Fixed patterns"
        TRANSFORMATIONS=$((TRANSFORMATIONS + 1))
      fi
    fi

  done < <(
    find "$REPO_ROOT" \
      -type f -name ".dockerignore" \
      -not -path "*/.git/*" -print0 2>/dev/null
  )
}

# ─────────────────────────────────────────────────────────────────────────────
# Registry Configuration Validation
# ─────────────────────────────────────────────────────────────────────────────
validate_registry_config() {
  log_section "Registry Configuration Validation"

  # Check for .docker/config.json
  if [[ -f "$REPO_ROOT/.docker/config.json" ]]; then
    log_info "Checking: .docker/config.json"

    if grep -qE "nousresearch|hermes" "$REPO_ROOT/.docker/config.json" 2>/dev/null; then
      log_warn "  Found branding references in Docker config"
      VIOLATIONS=$((VIOLATIONS + 1))

      if [[ "$FIX" == "true" ]]; then
        sed -i 's/nousresearch/nastechairesearch/g; s/hermes/nastech/g' "$REPO_ROOT/.docker/config.json"
        log_ok "  Fixed Docker config"
        TRANSFORMATIONS=$((TRANSFORMATIONS + 1))
      fi
    fi
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Build Script Validation
# ─────────────────────────────────────────────────────────────────────────────
validate_build_scripts() {
  log_section "Build Script Validation"

  while IFS= read -r -d '' script; do
    [[ -z "$script" ]] && continue

    log_info "Checking: $script"

    if grep -qE "nousresearch/hermes|HERMES_" "$script" 2>/dev/null; then
      log_warn "  Found branding references in build script"
      VIOLATIONS=$((VIOLATIONS + 1))

      if [[ "$FIX" == "true" ]]; then
        sed -i 's|nousresearch/hermes|nastechairesearch/nastech|g' "$script"
        sed -i 's/HERMES_/NASTECH_/g' "$script"
        log_ok "  Fixed build script"
        TRANSFORMATIONS=$((TRANSFORMATIONS + 1))
      fi
    fi

  done < <(
    find "$REPO_ROOT" \
      -type f \( -name "build.sh" -o -name "build.py" -o -name "Makefile" \) \
      -not -path "*/.git/*" -print0 2>/dev/null
  )
}

# ─────────────────────────────────────────────────────────────────────────────
# Generate Report
# ─────────────────────────────────────────────────────────────────────────────
generate_report() {
  log_section "Docker Branding Validation Report"

  echo "Violations found  : $VIOLATIONS"
  echo "Transformations   : $TRANSFORMATIONS"

  if [[ "$VIOLATIONS" -eq 0 ]]; then
    log_ok "✓ All Docker branding checks passed!"
    return 0
  else
    log_fail "✗ Docker branding validation failed with $VIOLATIONS violation(s)"
    return 1
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
main() {
  log_section "Docker Branding Validation"
  log_info "Repository: $REPO_ROOT"
  log_info "Fix mode: $FIX"

  validate_dockerfiles
  validate_docker_compose
  validate_github_actions
  validate_dockerignore
  validate_registry_config
  validate_build_scripts

  generate_report
}

main
