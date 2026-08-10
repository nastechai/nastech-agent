#!/bin/bash
# NasTech Agent Branding Transformation Script (Enhanced v2)
# Applies branding rules to transform NasTech to NasTech
# Handles: Content replacement, Filename renaming, Folder renaming, Code imports

set -euo pipefail

REPO_ROOT="${1:-.}"
DRY_RUN="${2:-false}"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
  echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $*"
}

log_section() {
  echo -e "\n${BLUE}=== $* ===${NC}"
}

# Verify we're in a git repository
if [ ! -d "$REPO_ROOT/.git" ]; then
  log_error "Not a git repository: $REPO_ROOT"
  exit 1
fi

log_info "Starting branding transformation in $REPO_ROOT"
log_info "Dry run: $DRY_RUN"

# Define branding rules (order matters - longest first to avoid partial replacements)
declare -A REBRAND_RULES=(
  # Full product names
  ["NasTech Agent"]="NasTech Agent"
  ["nastech-agent"]="nastech-agent"
  ["NasTech"]="NasTech"
  ["nastech"]="nastech"
  
  # Organization names
  ["NasTech"]="NasTech"
  ["nastechai"]="nastechai"
  ["nastechairesearch"]="nastechairesearch"
  
  # npm scopes
  ["@nastech-research"]="@nastech-research"
  
  # Environment variables and paths
  ["NASTECH_"]="NASTECH_"
  ["/opt/nastech"]="/opt/nastech"
  ["~/.nastech"]="~/.nastech"
  
  # Repository URLs
  ["github.com/nastechai/nastech-agent"]="github.com/nastechai/nastech-agent"
  ["github.com/nastechai/nastech-agent"]="github.com/nastechai/nastech-agent"
)

# File patterns to process
INCLUDE_PATTERNS=(
  "*.json" "*.js" "*.ts" "*.tsx" "*.jsx" "*.py" "*.yml" "*.yaml" "*.md" "*.sh" "*.dockerfile" "Dockerfile" ".env*" "*.txt" "*.config" "*.conf"
)

# Exclude patterns
EXCLUDE_PATTERNS=(
  ".git" "node_modules" ".venv" "dist" "build" ".next" "*.lock" "*.lockfile" ".DS_Store" ".github/workflows"
)

# Track statistics
TOTAL_FILES=0
MODIFIED_FILES=0
TOTAL_REPLACEMENTS=0
RENAMED_ITEMS=0

# ============================================================================
# Phase 1: CONTENT REPLACEMENT
# ============================================================================
log_section "Phase 1: Content Replacement"

FIND_CMD="find $REPO_ROOT -type f"
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
  FIND_CMD="$FIND_CMD -not -path '*/$pattern/*' -not -path '*/$pattern'"
done

FILES_TO_PROCESS=()
for pattern in "${INCLUDE_PATTERNS[@]}"; do
  while IFS= read -r file; do
    [ -n "$file" ] && FILES_TO_PROCESS+=("$file")
  done < <(eval "$FIND_CMD -name '$pattern'" 2>/dev/null || true)
done

log_info "Found ${#FILES_TO_PROCESS[@]} files to process"

for file in "${FILES_TO_PROCESS[@]}"; do
  if [ ! -f "$file" ]; then continue; fi
  if file "$file" 2>/dev/null | grep -q "binary"; then continue; fi
  
  TOTAL_FILES=$((TOTAL_FILES + 1))
  FILE_CHANGED=0
  FILE_REPLACEMENTS=0
  
  # Apply each branding rule
  for old_text in "${!REBRAND_RULES[@]}"; do
    new_text="${REBRAND_RULES[$old_text]}"
    
    # Count occurrences
    count=$(grep -c "$old_text" "$file" 2>/dev/null || echo 0)
    
    if [ "$count" -gt 0 ]; then
      FILE_REPLACEMENTS=$((FILE_REPLACEMENTS + count))
      FILE_CHANGED=1
      
      if [ "$DRY_RUN" = "true" ]; then
        log_info "  [$file] Would replace '$old_text' → '$new_text' ($count times)"
      else
        sed -i "s|$old_text|$new_text|g" "$file"
      fi
    fi
  done
  
  if [ "$FILE_CHANGED" -eq 1 ]; then
    MODIFIED_FILES=$((MODIFIED_FILES + 1))
    TOTAL_REPLACEMENTS=$((TOTAL_REPLACEMENTS + FILE_REPLACEMENTS))
  fi
done

log_info "Modified $MODIFIED_FILES files with $TOTAL_REPLACEMENTS total replacements"

# ============================================================================
# Phase 2: RENAMING FILES
# ============================================================================
log_section "Phase 2: Renaming Files"

# Find all files with "nastech" or "NasTech" in their name
FILES_TO_RENAME=$(find "$REPO_ROOT" -type f \( -name "*nastech*" -o -name "*NasTech*" \) \
  -not -path "*/.git/*" 2>/dev/null | sort -r || true)

while IFS= read -r file; do
  [ -z "$file" ] && continue
  
  dir=$(dirname "$file")
  base=$(basename "$file")
  new_base=$(echo "$base" | sed 's/nastech/nastech/g; s/NasTech/NasTech/g')
  
  if [ "$base" != "$new_base" ]; then
    if [ "$DRY_RUN" = "true" ]; then
      log_info "  Would rename file: $base → $new_base"
    else
      mv "$file" "$dir/$new_base"
      log_info "  Renamed file: $base → $new_base"
    fi
    RENAMED_ITEMS=$((RENAMED_ITEMS + 1))
  fi
done <<< "$FILES_TO_RENAME"

# ============================================================================
# Phase 3: RENAMING DIRECTORIES
# ============================================================================
log_section "Phase 3: Renaming Directories"

# Find all directories with "nastech" or "NasTech" in their name (deepest first)
DIRS_TO_RENAME=$(find "$REPO_ROOT" -type d \( -name "*nastech*" -o -name "*NasTech*" \) \
  -not -path "*/.git/*" 2>/dev/null | awk '{ print length, $0 }' | sort -rn | cut -d" " -f2- || true)

while IFS= read -r dir; do
  [ -z "$dir" ] && continue
  
  parent=$(dirname "$dir")
  base=$(basename "$dir")
  new_base=$(echo "$base" | sed 's/nastech/nastech/g; s/NasTech/NasTech/g')
  
  if [ "$base" != "$new_base" ]; then
    if [ "$DRY_RUN" = "true" ]; then
      log_info "  Would rename directory: $base → $new_base"
    else
      mv "$dir" "$parent/$new_base"
      log_info "  Renamed directory: $base → $new_base"
    fi
    RENAMED_ITEMS=$((RENAMED_ITEMS + 1))
  fi
done <<< "$DIRS_TO_RENAME"

# ============================================================================
# Phase 4: VERIFY IMPORTS AND PATHS
# ============================================================================
log_section "Phase 4: Verifying Imports and Paths"

# Check for any remaining nastech references in code files
REMAINING_REFS=$(find "$REPO_ROOT" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" \) \
  -not -path "*/.git/*" -not -path "*/node_modules/*" \
  -exec grep -l "nastech\|NasTech" {} \; 2>/dev/null | wc -l || echo 0)

if [ "$REMAINING_REFS" -gt 0 ]; then
  log_warn "Found $REMAINING_REFS code files with remaining 'nastech' references"
  find "$REPO_ROOT" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" \) \
    -not -path "*/.git/*" -not -path "*/node_modules/*" \
    -exec grep -l "nastech\|NasTech" {} \; 2>/dev/null | head -5
else
  log_info "✓ No remaining 'nastech' references in code files"
fi

# ============================================================================
# SUMMARY
# ============================================================================
log_section "Transformation Summary"

log_info "Total files scanned: $TOTAL_FILES"
log_info "Files modified: $MODIFIED_FILES"
log_info "Total replacements: $TOTAL_REPLACEMENTS"
log_info "Items renamed: $RENAMED_ITEMS"

if [ "$DRY_RUN" = "true" ]; then
  log_warn "Dry run completed. No changes were made."
  exit 0
else
  log_info "✓ All transformations applied successfully"
  exit 0
fi
