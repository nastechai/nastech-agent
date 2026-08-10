#!/usr/bin/env python3
"""
NasTech Configuration Branding Validator (v3.0)

Validates and transforms branding in:
- YAML files (.yml, .yaml)
- TOML files (.toml)
- INI files (.ini, .conf, .config)
- Environment files (.env, .env.*)
- JSON files (.json)
- Markdown documentation

Usage:
  python3 validate-config-branding.py [--repo ROOT] [--fix] [--report]
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    import tomllib
    HAS_TOML = True
except ImportError:
    try:
        import tomli as tomllib
        HAS_TOML = True
    except ImportError:
        HAS_TOML = False

# ─────────────────────────────────────────────────────────────────────────────
# Colors
# ─────────────────────────────────────────────────────────────────────────────
class Colors:
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    INFO = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def log_ok(msg):
    print(f"{Colors.OK}[✓]{Colors.RESET} {msg}")

def log_warn(msg):
    print(f"{Colors.WARN}[⚠]{Colors.RESET} {msg}", file=sys.stderr)

def log_fail(msg):
    print(f"{Colors.FAIL}[✗]{Colors.RESET} {msg}", file=sys.stderr)

def log_info(msg):
    print(f"{Colors.INFO}[•]{Colors.RESET} {msg}")

def log_section(title):
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}  {title}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")

# ─────────────────────────────────────────────────────────────────────────────
# Branding Rules
# ─────────────────────────────────────────────────────────────────────────────
BRANDING_RULES = [
    ('github.com/NousResearch/hermes-agent', 'github.com/nastechai/nastech-agent', 100),
    ('github.com/NousResearch/Hermes-Agent', 'github.com/nastechai/nastech-agent', 100),
    ('nousresearch/hermes', 'nastechairesearch/nastech', 95),
    ('Hermes Agent', 'NasTech Agent', 90),
    ('hermes-agent', 'nastech-agent', 90),
    ('@nous-research', '@nastech-research', 85),
    ('Nous Research', 'NasTech', 80),
    ('NousResearch', 'nastechai', 80),
    ('nousresearch', 'nastechairesearch', 80),
    ('HERMES_', 'NASTECH_', 75),
    ('/opt/hermes', '/opt/nastech', 75),
    ('~/.hermes', '~/.nastech', 75),
    ('Hermes', 'NasTech', 50),
    ('hermes', 'nastech', 50),
]

RULES_SORTED = sorted(BRANDING_RULES, key=lambda x: x[2], reverse=True)

# ─────────────────────────────────────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────────────────────────────────────
def apply_branding_rules(text: str) -> Tuple[str, int]:
    """Apply all branding rules to text."""
    result = text
    replacements = 0

    for old, new, _ in RULES_SORTED:
        count = result.count(old)
        if count > 0:
            result = result.replace(old, new)
            replacements += count

    return result, replacements

def transform_dict_recursive(obj) -> int:
    """Recursively transform dictionary values."""
    replacements = 0

    if isinstance(obj, dict):
        for key in list(obj.keys()):
            # Transform key
            new_key = key
            for old, new, _ in RULES_SORTED:
                new_key = new_key.replace(old, new)
            
            if new_key != key:
                obj[new_key] = obj.pop(key)
                replacements += 1
                key = new_key
            
            # Transform value recursively
            replacements += transform_dict_recursive(obj[key])
    
    elif isinstance(obj, list):
        for item in obj:
            replacements += transform_dict_recursive(item)
    
    elif isinstance(obj, str):
        for old, new, _ in RULES_SORTED:
            count = obj.count(old)
            if count > 0:
                replacements += count
    
    return replacements

# ─────────────────────────────────────────────────────────────────────────────
# File Validators
# ─────────────────────────────────────────────────────────────────────────────
class ConfigBrandingValidator:
    def __init__(self, repo_root: str, fix: bool = False):
        self.repo_root = Path(repo_root)
        self.fix = fix
        self.violations = []
        self.transformations = []

    def validate_yaml_files(self):
        """Validate YAML configuration files."""
        log_section("YAML Configuration Files")

        for filepath in self.repo_root.rglob('*.yml'):
            if self._should_skip(filepath):
                continue
            self._validate_yaml(filepath)

        for filepath in self.repo_root.rglob('*.yaml'):
            if self._should_skip(filepath):
                continue
            self._validate_yaml(filepath)

    def _validate_yaml(self, filepath: Path):
        """Validate a single YAML file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for branding violations
            violations = 0
            for old, new, _ in RULES_SORTED:
                count = content.count(old)
                if count > 0:
                    violations += count

            if violations > 0:
                log_warn(f"  {filepath}: {violations} violation(s)")
                self.violations.append((filepath, violations))

                if self.fix:
                    new_content, replacements = apply_branding_rules(content)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    log_ok(f"    Fixed: {replacements} replacement(s)")
                    self.transformations.append((filepath, replacements))
            else:
                log_ok(f"  {filepath}")

        except Exception as e:
            log_warn(f"  {filepath}: {e}")

    def validate_toml_files(self):
        """Validate TOML configuration files."""
        if not HAS_TOML:
            log_warn("toml library not available, skipping TOML validation")
            return

        log_section("TOML Configuration Files")

        for filepath in self.repo_root.rglob('*.toml'):
            if self._should_skip(filepath):
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                violations = 0
                for old, new, _ in RULES_SORTED:
                    count = content.count(old)
                    if count > 0:
                        violations += count

                if violations > 0:
                    log_warn(f"  {filepath}: {violations} violation(s)")
                    self.violations.append((filepath, violations))

                    if self.fix:
                        new_content, replacements = apply_branding_rules(content)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        log_ok(f"    Fixed: {replacements} replacement(s)")
                        self.transformations.append((filepath, replacements))
                else:
                    log_ok(f"  {filepath}")

            except Exception as e:
                log_warn(f"  {filepath}: {e}")

    def validate_env_files(self):
        """Validate environment files."""
        log_section("Environment Files")

        patterns = ['.env', '.env.*']
        for pattern in patterns:
            for filepath in self.repo_root.glob(pattern):
                if self._should_skip(filepath):
                    continue

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    violations = 0
                    for old, new, _ in RULES_SORTED:
                        count = content.count(old)
                        if count > 0:
                            violations += count

                    if violations > 0:
                        log_warn(f"  {filepath}: {violations} violation(s)")
                        self.violations.append((filepath, violations))

                        if self.fix:
                            new_content, replacements = apply_branding_rules(content)
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            log_ok(f"    Fixed: {replacements} replacement(s)")
                            self.transformations.append((filepath, replacements))
                    else:
                        log_ok(f"  {filepath}")

                except Exception as e:
                    log_warn(f"  {filepath}: {e}")

    def validate_json_files(self):
        """Validate JSON configuration files."""
        log_section("JSON Configuration Files")

        for filepath in self.repo_root.rglob('*.json'):
            if self._should_skip(filepath) or 'node_modules' in filepath.parts:
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                violations = 0
                for old, new, _ in RULES_SORTED:
                    count = content.count(old)
                    if count > 0:
                        violations += count

                if violations > 0:
                    log_warn(f"  {filepath}: {violations} violation(s)")
                    self.violations.append((filepath, violations))

                    if self.fix:
                        try:
                            data = json.loads(content)
                            transform_dict_recursive(data)
                            new_content = json.dumps(data, indent=2) + '\n'
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            log_ok(f"    Fixed: {violations} replacement(s)")
                            self.transformations.append((filepath, violations))
                        except json.JSONDecodeError:
                            # Fall back to text replacement
                            new_content, replacements = apply_branding_rules(content)
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            log_ok(f"    Fixed: {replacements} replacement(s)")
                            self.transformations.append((filepath, replacements))
                else:
                    log_ok(f"  {filepath}")

            except Exception as e:
                log_warn(f"  {filepath}: {e}")

    def validate_markdown_files(self):
        """Validate Markdown documentation files."""
        log_section("Markdown Documentation")

        for filepath in self.repo_root.rglob('*.md'):
            if self._should_skip(filepath):
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                violations = 0
                for old, new, _ in RULES_SORTED:
                    count = content.count(old)
                    if count > 0:
                        violations += count

                if violations > 0:
                    log_warn(f"  {filepath}: {violations} violation(s)")
                    self.violations.append((filepath, violations))

                    if self.fix:
                        new_content, replacements = apply_branding_rules(content)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        log_ok(f"    Fixed: {replacements} replacement(s)")
                        self.transformations.append((filepath, replacements))
                else:
                    log_ok(f"  {filepath}")

            except Exception as e:
                log_warn(f"  {filepath}: {e}")

    def validate_all(self):
        """Run all validators."""
        self.validate_yaml_files()
        self.validate_toml_files()
        self.validate_env_files()
        self.validate_json_files()
        self.validate_markdown_files()

        log_section("Configuration Branding Report")
        log_ok(f"Violations found: {len(self.violations)}")
        log_ok(f"Transformations applied: {len(self.transformations)}")

        if len(self.violations) == 0:
            log_ok("✓ All configuration branding checks passed!")
            return True
        else:
            log_fail("✗ Configuration branding validation failed")
            return False

    def _should_skip(self, filepath: Path) -> bool:
        """Check if file should be skipped."""
        skip_dirs = {'.git', 'node_modules', '.venv', 'dist', 'build', '.next'}
        return any(skip in filepath.parts for skip in skip_dirs)

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description='NasTech Configuration Branding Validator'
    )
    parser.add_argument('--repo', default='.', help='Repository root path')
    parser.add_argument('--fix', action='store_true', help='Apply fixes')
    parser.add_argument('--report', action='store_true', help='Generate report')

    args = parser.parse_args()

    validator = ConfigBrandingValidator(args.repo, fix=args.fix)
    validator.validate_all()

if __name__ == '__main__':
    main()
