#!/usr/bin/env bash
# NasTech Agent Branding Transformation Script (High-End v3)
# Applies branding rules to transform Hermes → NasTech
# Handles: Content replacement, Filename renaming, Directory renaming, Import paths
#
# Usage:
#   ./rebrand.sh [REPO_ROOT] [DRY_RUN]
#   REPO_ROOT  – path to the repository root (default: .)
#   DRY_RUN    – "true" to preview changes without writing (default: false)

set -euo pipefail

REPO_ROOT="${1:-.}"
DRY_RUN="${2:-false}"

# ── Color helpers ─────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }
log_section() { echo -e "\n${BLUE}════════════════════════════════════════${NC}"; \
                echo -e "${CYAN}  $*${NC}"; \
                echo -e "${BLUE}════════════════════════════════════════${NC}"; }

# ── Guard: must be a git repository ──────────────────────────────────────────
if [[ ! -d "$REPO_ROOT/.git" ]]; then
  log_error "Not a git repository: $REPO_ROOT"
  exit 1
fi

log_info "Repository root : $REPO_ROOT"
log_info "Dry run         : $DRY_RUN"

# ── Branding rules (ORDERED – longest / most-specific first) ─────────────────
# Format: "OLD_TEXT|NEW_TEXT"
# Order matters: more specific patterns must precede their substrings.
REBRAND_RULES=(
  # Repository URLs (most specific – must come first)
  "github.com/NousResearch/Hermes-Agent|github.com/nastechai/nastech-agent"
  "github.com/NousResearch/hermes-agent|github.com/nastechai/nastech-agent"

  # Full product names
  "Hermes Agent|NasTech Agent"
  "hermes-agent|nastech-agent"

  # Organisation names (full forms before substrings)
  "Nous Research|NasTech"
  "NousResearch|nastechai"
  "nousresearch|nastechairesearch"

  # npm scope
  "@nous-research|@nastech-research"

  # Environment variables and paths
  "HERMES_|NASTECH_"
  "/opt/hermes|/opt/nastech"
  "~/.hermes|~/.nastech"

  # Generic brand names (last – broadest match)
  "Hermes|NasTech"
  "hermes|nastech"
)

# ── File patterns to process ──────────────────────────────────────────────────
INCLUDE_PATTERNS=(
  "*.json" "*.js" "*.ts" "*.tsx" "*.jsx"
  "*.py" "*.yml" "*.yaml" "*.md" "*.sh"
  "*.dockerfile" "Dockerfile" ".env*"
  "*.txt" "*.config" "*.conf" "*.toml"
)

# ── Directories / paths to exclude ───────────────────────────────────────────
EXCLUDE_DIRS=(
  ".git" "node_modules" ".venv" "dist" "build" ".next"
  ".github/workflows"
)

# ── Statistics ────────────────────────────────────────────────────────────────
TOTAL_FILES=0
MODIFIED_FILES=0
TOTAL_REPLACEMENTS=0
RENAMED_ITEMS=0

# ── Helper: escape a string for use as a sed LHS / RHS ───────────────────────
# Escapes: \ / | & (characters that have special meaning in sed s|...|...|)
sed_escape_lhs() { printf '%s' "$1" | sed 's/[\\|&]/\\&/g'; }
sed_escape_rhs() { printf '%s' "$1" | sed 's/[\\|&]/\\&/g'; }

# ── Helper: build the find -prune expression from EXCLUDE_DIRS ───────────────
build_find_prune() {
  local root="$1"; shift
  local args=("find" "$root" "(")
  local first=true
  for d in "${EXCLUDE_DIRS[@]}"; do
    $first || args+=("-o")
    args+=("-path" "*/$d" "-o" "-path" "*/$d/*")
    first=false
  done
  args+=(")" "-prune" "-o")
  printf '%q ' "${args[@]}"
}

# ============================================================================
# Phase 1: CONTENT REPLACEMENT
# ============================================================================
log_section "Phase 1: Content Replacement"

# Collect unique files matching include patterns, excluding pruned paths
declare -A SEEN_FILES
FILES_TO_PROCESS=()

for pattern in "${INCLUDE_PATTERNS[@]}"; do
  while IFS= read -r -d '' file; do
    [[ -z "$file" ]] && continue
    # Skip if already queued (deduplication)
    if [[ -z "${SEEN_FILES[$file]+_}" ]]; then
      SEEN_FILES[$file]=1
      FILES_TO_PROCESS+=("$file")
    fi
  done < <(
    find "$REPO_ROOT" \
      \( $(
          first=true
          for d in "${EXCLUDE_DIRS[@]}"; do
            $first || printf ' -o '
            printf -- '-path %q -o -path %q' "*/$d" "*/$d/*"
            first=false
          done
        ) \) -prune \
      -o -type f -name "$pattern" -print0 2>/dev/null
  )
done

log_info "Unique files to process: ${#FILES_TO_PROCESS[@]}"

for file in "${FILES_TO_PROCESS[@]}"; do
  [[ -f "$file" ]] || continue

  # Skip binary files using grep's built-in binary detection (-I flag)
  if ! grep -qI '' "$file" 2>/dev/null; then
    continue
  fi

  TOTAL_FILES=$((TOTAL_FILES + 1))
  FILE_CHANGED=0
  FILE_REPLACEMENTS=0

  for rule in "${REBRAND_RULES[@]}"; do
    old_text="${rule%%|*}"
    new_text="${rule##*|}"

    # Count matches safely (grep returns 1 on no match; we handle it explicitly)
    count=0
    count=$(grep -cF -- "$old_text" "$file" 2>/dev/null) || count=0

    if [[ "$count" -gt 0 ]]; then
      FILE_REPLACEMENTS=$((FILE_REPLACEMENTS + count))
      FILE_CHANGED=1

      if [[ "$DRY_RUN" == "true" ]]; then
        log_info "  [DRY] $file : '$old_text' → '$new_text' (×${count})"
      else
        escaped_old=$(sed_escape_lhs "$old_text")
        escaped_new=$(sed_escape_rhs "$new_text")
        sed -i "s|${escaped_old}|${escaped_new}|g" "$file"
      fi
    fi
  done

  if [[ "$FILE_CHANGED" -eq 1 ]]; then
    MODIFIED_FILES=$((MODIFIED_FILES + 1))
    TOTAL_REPLACEMENTS=$((TOTAL_REPLACEMENTS + FILE_REPLACEMENTS))
    log_info "  Modified: $file (${FILE_REPLACEMENTS} replacement(s))"
  fi
done

log_info "Files scanned: $TOTAL_FILES | Modified: $MODIFIED_FILES | Replacements: $TOTAL_REPLACEMENTS"

# ============================================================================
# Phase 2: RENAMING FILES
# ============================================================================
log_section "Phase 2: Renaming Files"

# Sort in reverse so deeper paths are renamed before their parents
while IFS= read -r -d '' file; do
  [[ -z "$file" ]] && continue

  dir=$(dirname "$file")
  base=$(basename "$file")
  new_base=$(printf '%s' "$base" | sed 's/hermes/nastech/g; s/Hermes/NasTech/g')

  if [[ "$base" != "$new_base" ]]; then
    if [[ "$DRY_RUN" == "true" ]]; then
      log_info "  [DRY] Rename file: $base → $new_base"
    else
      mv -- "$file" "$dir/$new_base"
      log_info "  Renamed file: $base → $new_base"
    fi
    RENAMED_ITEMS=$((RENAMED_ITEMS + 1))
  fi
done < <(
  find "$REPO_ROOT" -type f \( -name "*hermes*" -o -name "*Hermes*" \) \
    -not -path "*/.git/*" -print0 2>/dev/null \
  | sort -rz
)

# ============================================================================
# Phase 3: RENAMING DIRECTORIES
# ============================================================================
log_section "Phase 3: Renaming Directories"

# Deepest directories first to avoid broken paths
while IFS= read -r dir; do
  [[ -z "$dir" ]] && continue

  parent=$(dirname "$dir")
  base=$(basename "$dir")
  new_base=$(printf '%s' "$base" | sed 's/hermes/nastech/g; s/Hermes/NasTech/g')

  if [[ "$base" != "$new_base" ]]; then
    if [[ "$DRY_RUN" == "true" ]]; then
      log_info "  [DRY] Rename dir: $base → $new_base"
    else
      mv -- "$dir" "$parent/$new_base"
      log_info "  Renamed dir: $base → $new_base"
    fi
    RENAMED_ITEMS=$((RENAMED_ITEMS + 1))
  fi
done < <(
  find "$REPO_ROOT" -type d \( -name "*hermes*" -o -name "*Hermes*" \) \
    -not -path "*/.git/*" 2>/dev/null \
  | awk '{ print length, $0 }' | sort -rn | cut -d' ' -f2-
)

# ============================================================================
# Phase 4: VERIFY REMAINING REFERENCES
# ============================================================================
log_section "Phase 4: Verifying Remaining References"

REMAINING=0
REMAINING=$(
  find "$REPO_ROOT" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" \) \
    -not -path "*/.git/*" -not -path "*/node_modules/*" \
    -exec grep -lIF "hermes" {} \; 2>/dev/null | wc -l
) || REMAINING=0

if [[ "$REMAINING" -gt 0 ]]; then
  log_warn "Found $REMAINING code file(s) with residual 'hermes' references:"
  find "$REPO_ROOT" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" \) \
    -not -path "*/.git/*" -not -path "*/node_modules/*" \
    -exec grep -lIF "hermes" {} \; 2>/dev/null | head -10
else
  log_info "✓ No residual 'hermes' references in code files"
fi

# ============================================================================
# Phase 5: GIT DIFF SUMMARY
# ============================================================================
log_section "Phase 5: Git Diff Summary"

if [[ "$DRY_RUN" != "true" ]]; then
  cd "$REPO_ROOT"
  if git diff --quiet 2>/dev/null; then
    log_info "No staged or unstaged changes detected (repo may already be clean)"
  else
    log_info "Changed files:"
    git diff --stat 2>/dev/null || true
  fi
fi

# ============================================================================
# SUMMARY
# ============================================================================
log_section "Transformation Summary"

log_info "Total files scanned  : $TOTAL_FILES"
log_info "Files modified       : $MODIFIED_FILES"
log_info "Total replacements   : $TOTAL_REPLACEMENTS"
log_info "Items renamed        : $RENAMED_ITEMS"

if [[ "$DRY_RUN" == "true" ]]; then
  log_warn "Dry run complete — no changes were written to disk."
  exit 0
fi

log_info "✓ All transformations applied successfully."
exit 0
