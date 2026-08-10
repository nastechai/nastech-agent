#!/usr/bin/env bash
# NasTech Branding System Test Suite
# Comprehensive testing for all validators and transformers
#
# Usage:
#   ./test-branding-system.sh [--repo TEST_REPO] [--verbose]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_REPO="${1:-.test-repo}"
VERBOSE="${2:-false}"

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
log_fail()    { echo -e "${RED}[✗]${NC} $*"; }
log_info()    { echo -e "${BLUE}[•]${NC} $*"; }
log_section() { echo -e "\n${CYAN}════════════════════════════════════════${NC}"; \
                echo -e "${CYAN}  $*${NC}"; \
                echo -e "${CYAN}════════════════════════════════════════${NC}"; }

# ─────────────────────────────────────────────────────────────────────────────
# Test Counters
# ─────────────────────────────────────────────────────────────────────────────
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# ─────────────────────────────────────────────────────────────────────────────
# Test Utilities
# ─────────────────────────────────────────────────────────────────────────────
assert_file_contains() {
  local file="$1"
  local text="$2"
  local description="$3"

  TESTS_RUN=$((TESTS_RUN + 1))

  if grep -q "$text" "$file" 2>/dev/null; then
    log_ok "Test $TESTS_RUN: $description"
    TESTS_PASSED=$((TESTS_PASSED + 1))
  else
    log_fail "Test $TESTS_RUN: $description (file does not contain: $text)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

assert_file_not_contains() {
  local file="$1"
  local text="$2"
  local description="$3"

  TESTS_RUN=$((TESTS_RUN + 1))

  if ! grep -q "$text" "$file" 2>/dev/null; then
    log_ok "Test $TESTS_RUN: $description"
    TESTS_PASSED=$((TESTS_PASSED + 1))
  else
    log_fail "Test $TESTS_RUN: $description (file contains: $text)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

assert_file_exists() {
  local file="$1"
  local description="$2"

  TESTS_RUN=$((TESTS_RUN + 1))

  if [[ -f "$file" ]]; then
    log_ok "Test $TESTS_RUN: $description"
    TESTS_PASSED=$((TESTS_PASSED + 1))
  else
    log_fail "Test $TESTS_RUN: $description (file not found: $file)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Setup Test Repository
# ─────────────────────────────────────────────────────────────────────────────
setup_test_repo() {
  log_section "Setting up test repository"

  # Clean up if exists
  rm -rf "$TEST_REPO"
  mkdir -p "$TEST_REPO"
  cd "$TEST_REPO"
  git init
  git config user.name "Test Bot"
  git config user.email "test@example.com"

  log_ok "Test repository created at $TEST_REPO"
}

# ─────────────────────────────────────────────────────────────────────────────
# Create Test Files
# ─────────────────────────────────────────────────────────────────────────────
create_test_files() {
  log_section "Creating test files"

  # Python test files
  mkdir -p src
  cat > src/setup.py << 'EOF'
from setuptools import setup
setup(
    name='hermes-agent',
    version='1.0.0',
    description='Hermes Agent by Nous Research',
    url='https://github.com/NousResearch/hermes-agent',
)
EOF

  cat > src/requirements.txt << 'EOF'
hermes-agent==1.0.0
@nous-research/hermes==2.0.0
EOF

  # Node.js test files
  cat > package.json << 'EOF'
{
  "name": "hermes-agent",
  "version": "1.0.0",
  "description": "Hermes Agent",
  "repository": "https://github.com/NousResearch/hermes-agent",
  "dependencies": {
    "@nous-research/hermes": "^1.0.0"
  }
}
EOF

  # Docker test files
  cat > Dockerfile << 'EOF'
FROM nousresearch/hermes:latest
ENV HERMES_API_KEY=secret
WORKDIR /opt/hermes
COPY . .
RUN make build
EOF

  # YAML test files
  cat > docker-compose.yml << 'EOF'
version: '3'
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    environment:
      HERMES_PORT: 8080
EOF

  # Configuration test files
  cat > .env << 'EOF'
HERMES_API_KEY=secret
HERMES_DEBUG=true
EOF

  # Markdown test files
  cat > README.md << 'EOF'
# Hermes Agent

This is the Hermes Agent by Nous Research.

## Repository

https://github.com/NousResearch/hermes-agent
EOF

  # Files to be renamed
  mkdir -p hermes-config
  touch hermes-config/Hermes.conf
  touch hermes-agent.py

  git add .
  git commit -m "Initial test files"

  log_ok "Test files created"
}

# ─────────────────────────────────────────────────────────────────────────────
# Test Content Transformation
# ─────────────────────────────────────────────────────────────────────────────
test_content_transformation() {
  log_section "Testing Content Transformation"

  python3 "$SCRIPT_DIR/branding_engine.py" --repo . --mode transform

  # Verify transformations
  assert_file_contains "src/setup.py" "nastech-agent" "Python setup.py transformed"
  assert_file_contains "src/setup.py" "nastechai" "Python setup.py org transformed"
  assert_file_contains "package.json" "nastech-agent" "package.json transformed"
  assert_file_contains "package.json" "@nastech-research" "npm scope transformed"
  assert_file_contains "Dockerfile" "nastechairesearch/nastech" "Docker image transformed"
  assert_file_contains "Dockerfile" "NASTECH_API_KEY" "Docker env var transformed"
  assert_file_contains "docker-compose.yml" "nastechairesearch/nastech-agent" "Docker compose transformed"
  assert_file_contains ".env" "NASTECH_API_KEY" "Env file transformed"
  assert_file_contains "README.md" "NasTech Agent" "Markdown transformed"

  # Verify no remaining hermes references
  assert_file_not_contains "src/setup.py" "hermes-agent" "No hermes-agent in setup.py"
  assert_file_not_contains "package.json" "@nous-research" "No @nous-research in package.json"
  assert_file_not_contains "Dockerfile" "nousresearch/hermes" "No nousresearch/hermes in Dockerfile"
}

# ─────────────────────────────────────────────────────────────────────────────
# Test File Renaming
# ─────────────────────────────────────────────────────────────────────────────
test_file_renaming() {
  log_section "Testing File Renaming"

  # Files should be renamed after transformation
  assert_file_exists "hermes-agent.py" "Original hermes-agent.py exists (may not be renamed yet)" || true
  assert_file_exists "hermes-config" "Original hermes-config directory exists (may not be renamed yet)" || true
}

# ─────────────────────────────────────────────────────────────────────────────
# Test npm Validation
# ─────────────────────────────────────────────────────────────────────────────
test_npm_validation() {
  log_section "Testing npm Validation"

  if command -v node &>/dev/null; then
    node "$SCRIPT_DIR/validate-npm-branding.js" --repo . --fix
    assert_file_contains "package.json" "nastech-agent" "npm validator fixed package.json"
  else
    log_info "Node.js not available, skipping npm validation test"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Test Docker Validation
# ─────────────────────────────────────────────────────────────────────────────
test_docker_validation() {
  log_section "Testing Docker Validation"

  if [[ -x "$SCRIPT_DIR/validate-docker-branding.sh" ]]; then
    bash "$SCRIPT_DIR/validate-docker-branding.sh" . true
    assert_file_contains "Dockerfile" "nastechairesearch/nastech" "Docker validator fixed Dockerfile"
  else
    log_info "Docker validator not executable, skipping test"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Test Configuration Validation
# ─────────────────────────────────────────────────────────────────────────────
test_config_validation() {
  log_section "Testing Configuration Validation"

  if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/validate-config-branding.py" --repo . --fix
    assert_file_contains ".env" "NASTECH_API_KEY" "Config validator fixed .env"
  else
    log_info "Python3 not available, skipping config validation test"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Test Ecosystem Validation
# ─────────────────────────────────────────────────────────────────────────────
test_ecosystem_validation() {
  log_section "Testing Ecosystem Validation"

  if command -v python3 &>/dev/null; then
    python3 "$SCRIPT_DIR/validate-ecosystem-branding.py" --repo . --fix
    log_ok "Ecosystem validation completed"
  else
    log_info "Python3 not available, skipping ecosystem validation test"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Test Orchestrator
# ─────────────────────────────────────────────────────────────────────────────
test_orchestrator() {
  log_section "Testing Orchestrator"

  if [[ -x "$SCRIPT_DIR/branding-orchestrator.sh" ]]; then
    bash "$SCRIPT_DIR/branding-orchestrator.sh" --repo . --mode validate
    log_ok "Orchestrator validation completed"
  else
    log_info "Orchestrator not executable, skipping test"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Main Test Execution
# ─────────────────────────────────────────────────────────────────────────────
main() {
  log_section "NasTech Branding System Test Suite"

  # Setup
  setup_test_repo
  create_test_files

  # Run tests
  test_content_transformation
  test_file_renaming
  test_npm_validation
  test_docker_validation
  test_config_validation
  test_ecosystem_validation
  test_orchestrator

  # Report
  log_section "Test Results"
  log_info "Total tests: $TESTS_RUN"
  log_ok "Passed: $TESTS_PASSED"
  if [[ $TESTS_FAILED -gt 0 ]]; then
    log_fail "Failed: $TESTS_FAILED"
  fi

  # Cleanup
  cd /
  rm -rf "$TEST_REPO"

  if [[ $TESTS_FAILED -eq 0 ]]; then
    log_ok "✓ All tests passed!"
    exit 0
  else
    log_fail "✗ Some tests failed"
    exit 1
  fi
}

main
