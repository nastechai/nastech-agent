#!/usr/bin/env bash
# NasTech Branding Orchestrator (v3.0)
# Master script that coordinates all branding validators and transformers
# across 40+ ecosystems, file types, and package managers.
#
# This is the single entry point for complete branding transformation.
#
# Usage:
#   ./branding-orchestrator.sh [--repo ROOT] [--mode transform|validate|report] [--dry-run] [--parallel]

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
REPO_ROOT="${1:-.}"
MODE="${2:-transform}"
DRY_RUN="${3:-false}"
PARALLEL="${4:-false}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG_FILE="/tmp/branding-orchestrator-${TIMESTAMP}.log"

# ─────────────────────────────────────────────────────────────────────────────
# Colors
# ─────────────────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'

log_ok()      { echo -e "${GREEN}[✓]${NC} $*" | tee -a "$LOG_FILE"; }
log_warn()    { echo -e "${YELLOW}[⚠]${NC} $*" | tee -a "$LOG_FILE" >&2; }
log_fail()    { echo -e "${RED}[✗]${NC} $*" | tee -a "$LOG_FILE" >&2; }
log_info()    { echo -e "${BLUE}[•]${NC} $*" | tee -a "$LOG_FILE"; }
log_section() { echo -e "\n${CYAN}${BOLD}════════════════════════════════════════════════════════════════${NC}" | tee -a "$LOG_FILE"; \
                echo -e "${CYAN}${BOLD}  $*${NC}" | tee -a "$LOG_FILE"; \
                echo -e "${CYAN}${BOLD}════════════════════════════════════════════════════════════════${NC}" | tee -a "$LOG_FILE"; }

# ─────────────────────────────────────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────────────────────────────────────
validate_repo() {
  if [[ ! -d "$REPO_ROOT/.git" ]]; then
    log_fail "Not a git repository: $REPO_ROOT"
    exit 1
  fi
  log_ok "Repository verified: $REPO_ROOT"
}

# ─────────────────────────────────────────────────────────────────────────────
# Phase 1: Content Transformation
# ─────────────────────────────────────────────────────────────────────────────
run_content_transformation() {
  log_section "Phase 1: Content Transformation (Python Engine)"

  if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/branding_engine.py" \
      --repo "$REPO_ROOT" \
      --mode transform \
      $([ "$DRY_RUN" = "true" ] && echo "--dry-run" || true)
    log_ok "Content transformation complete"
  else
    log_warn "Python3 not available, skipping content transformation"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Phase 2: File/Directory Renaming
# ─────────────────────────────────────────────────────────────────────────────
run_file_renaming() {
  log_section "Phase 2: File/Directory Renaming"

  find "$REPO_ROOT" -type f \( -name "*hermes*" -o -name "*Hermes*" \) \
    -not -path "*/.git/*" -print0 2>/dev/null | sort -rz | while IFS= read -r -d '' file; do
    
    [[ -z "$file" ]] && continue
    
    dir=$(dirname "$file")
    base=$(basename "$file")
    new_base=$(echo "$base" | sed 's/hermes/nastech/g; s/Hermes/NasTech/g')
    
    if [[ "$base" != "$new_base" ]]; then
      if [[ "$DRY_RUN" != "true" ]]; then
        mv -- "$file" "$dir/$new_base"
        log_ok "Renamed file: $base → $new_base"
      else
        log_info "[DRY] Would rename: $base → $new_base"
      fi
    fi
  done

  find "$REPO_ROOT" -type d \( -name "*hermes*" -o -name "*Hermes*" \) \
    -not -path "*/.git/*" 2>/dev/null | awk '{ print length, $0 }' | sort -rn | cut -d' ' -f2- | while read -r dir; do
    
    [[ -z "$dir" ]] && continue
    
    parent=$(dirname "$dir")
    base=$(basename "$dir")
    new_base=$(echo "$base" | sed 's/hermes/nastech/g; s/Hermes/NasTech/g')
    
    if [[ "$base" != "$new_base" ]]; then
      if [[ "$DRY_RUN" != "true" ]]; then
        mv -- "$dir" "$parent/$new_base"
        log_ok "Renamed directory: $base → $new_base"
      else
        log_info "[DRY] Would rename: $base → $new_base"
      fi
    fi
  done

  log_ok "File/directory renaming complete"
}

# ─────────────────────────────────────────────────────────────────────────────
# Phase 3: npm Branding Validation
# ─────────────────────────────────────────────────────────────────────────────
run_npm_validation() {
  log_section "Phase 3: npm Ecosystem Validation"

  if command -v node &>/dev/null; then
    node "$SCRIPT_DIR/validate-npm-branding.js" \
      --repo "$REPO_ROOT" \
      $([ "$DRY_RUN" != "true" ] && echo "--fix" || true)
    log_ok "npm validation complete"
  else
    log_warn "Node.js not available, skipping npm validation"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Phase 4: Docker Branding Validation
# ─────────────────────────────────────────────────────────────────────────────
run_docker_validation() {
  log_section "Phase 4: Docker Ecosystem Validation"

  if [[ -x "$SCRIPT_DIR/validate-docker-branding.sh" ]]; then
    bash "$SCRIPT_DIR/validate-docker-branding.sh" "$REPO_ROOT" \
      $([ "$DRY_RUN" != "true" ] && echo "true" || echo "false")
    log_ok "Docker validation complete"
  else
    log_warn "Docker validator not executable"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Phase 5: Configuration Branding Validation
# ─────────────────────────────────────────────────────────────────────────────
run_config_validation() {
  log_section "Phase 5: Configuration Files Validation"

  if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/validate-config-branding.py" \
      --repo "$REPO_ROOT" \
      $([ "$DRY_RUN" != "true" ] && echo "--fix" || true)
    log_ok "Configuration validation complete"
  else
    log_warn "Python3 not available, skipping config validation"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Phase 6: Ecosystem Branding Validation (40+ ecosystems)
# ─────────────────────────────────────────────────────────────────────────────
run_ecosystem_validation() {
  log_section "Phase 6: Multi-Ecosystem Validation (40+ ecosystems)"

  if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/validate-ecosystem-branding.py" \
      --repo "$REPO_ROOT" \
      $([ "$DRY_RUN" != "true" ] && echo "--fix" || true)
    log_ok "Ecosystem validation complete"
  else
    log_warn "Python3 not available, skipping ecosystem validation"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Phase 7: Final Verification
# ─────────────────────────────────────────────────────────────────────────────
run_final_verification() {
  log_section "Phase 7: Final Verification"

  if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/branding_engine.py" \
      --repo "$REPO_ROOT" \
      --mode validate
    log_ok "Final verification complete"
  else
    log_warn "Python3 not available, skipping final verification"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Git Summary
# ─────────────────────────────────────────────────────────────────────────────
run_git_summary() {
  log_section "Git Changes Summary"

  cd "$REPO_ROOT"
  
  if git diff --quiet 2>/dev/null; then
    log_info "No staged or unstaged changes"
  else
    log_info "Changed files:"
    git diff --stat 2>/dev/null || true
  fi

  UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l)
  if [[ "$UNTRACKED" -gt 0 ]]; then
    log_info "Untracked files: $UNTRACKED"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Main Execution
# ─────────────────────────────────────────────────────────────────────────────
main() {
  log_section "NasTech Branding Orchestrator v3.0"
  log_info "Repository: $REPO_ROOT"
  log_info "Mode: $MODE"
  log_info "Dry run: $DRY_RUN"
  log_info "Parallel: $PARALLEL"
  log_info "Log file: $LOG_FILE"

  validate_repo

  case "$MODE" in
    transform)
      log_section "TRANSFORMATION MODE"
      
      if [[ "$PARALLEL" == "true" ]]; then
        log_info "Running validators in parallel..."
        run_content_transformation &
        PID1=$!
        run_npm_validation &
        PID2=$!
        run_docker_validation &
        PID3=$!
        run_config_validation &
        PID4=$!
        run_ecosystem_validation &
        PID5=$!
        
        wait $PID1 $PID2 $PID3 $PID4 $PID5 || true
      else
        log_info "Running validators sequentially..."
        run_content_transformation
        run_file_renaming
        run_npm_validation
        run_docker_validation
        run_config_validation
        run_ecosystem_validation
      fi

      run_final_verification
      run_git_summary
      log_ok "✓ Transformation complete"
      ;;

    validate)
      log_section "VALIDATION MODE"
      run_final_verification
      log_ok "✓ Validation complete"
      ;;

    report)
      log_section "REPORT MODE"
      if command -v python3 &>/dev/null; then
        python3 "$SCRIPT_DIR/branding_engine.py" \
          --repo "$REPO_ROOT" \
          --mode report
      fi
      log_ok "✓ Report generated"
      ;;

    *)
      log_fail "Unknown mode: $MODE"
      exit 1
      ;;
  esac

  log_section "Orchestration Complete"
  log_ok "Log file: $LOG_FILE"
}

main "$@"
