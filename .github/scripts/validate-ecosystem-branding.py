#!/usr/bin/env python3
"""
NasTech Ecosystem Branding Validator (v3.0)
Comprehensive support for 40+ ecosystems and package managers.

Supported ecosystems:
  Python: setup.py, setup.cfg, pyproject.toml, requirements.txt, Pipfile, poetry.lock
  Node.js: package.json, package-lock.json, yarn.lock, pnpm-lock.yaml, .npmrc
  Go: go.mod, go.sum, main.go
  Rust: Cargo.toml, Cargo.lock
  Java: pom.xml, build.gradle, gradle.properties, settings.gradle
  Ruby: Gemfile, Gemfile.lock, .gemrc
  PHP: composer.json, composer.lock
  .NET: .csproj, .fsproj, .vbproj, packages.config
  Kotlin: build.gradle.kts
  Scala: build.sbt
  Clojure: project.clj, deps.edn
  Elixir: mix.exs, mix.lock
  Haskell: cabal.project, stack.yaml
  R: DESCRIPTION, renv.lock
  Perl: Makefile.PL, cpanfile
  Lua: rockspec files
  Swift: Package.swift
  Docker: Dockerfile, docker-compose.yml, .dockerignore
  Kubernetes: *.yaml, *.yml in k8s/
  Terraform: *.tf files
  Ansible: playbooks, roles
  GitHub Actions: .github/workflows/*.yml
  GitLab CI: .gitlab-ci.yml
  CircleCI: .circleci/config.yml
  Jenkins: Jenkinsfile
  Travis CI: .travis.yml
  Azure Pipelines: azure-pipelines.yml
  Helm: Chart.yaml, values.yaml
  Makefile: Makefile, makefile
  CMake: CMakeLists.txt
  Bazel: BUILD, BUILD.bazel, WORKSPACE
  Maven: pom.xml
  Gradle: build.gradle, gradle.properties
  SBT: build.sbt
  Ant: build.xml
  Documentation: README.md, docs/*, *.md
  Configuration: .env, .env.*, config.*, settings.*
  Web: HTML, CSS, JavaScript, TypeScript, Vue, React, Angular

Usage:
  python3 validate-ecosystem-branding.py [--repo ROOT] [--fix] [--report] [--ecosystem LANG]
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
from dataclasses import dataclass

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
    print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}  {title}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}")

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
# Ecosystem Definitions
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class EcosystemConfig:
    name: str
    file_patterns: List[str]
    parser: str  # 'text', 'json', 'xml', 'toml', 'yaml', 'ini'
    context: str  # 'python', 'nodejs', 'go', 'rust', 'java', etc.

ECOSYSTEMS = {
    # Python
    'python': [
        EcosystemConfig('setup.py', ['setup.py'], 'text', 'python'),
        EcosystemConfig('setup.cfg', ['setup.cfg'], 'ini', 'python'),
        EcosystemConfig('pyproject.toml', ['pyproject.toml'], 'toml', 'python'),
        EcosystemConfig('requirements.txt', ['requirements*.txt'], 'text', 'python'),
        EcosystemConfig('Pipfile', ['Pipfile'], 'text', 'python'),
        EcosystemConfig('poetry.lock', ['poetry.lock'], 'text', 'python'),
        EcosystemConfig('tox.ini', ['tox.ini'], 'ini', 'python'),
    ],
    
    # Node.js
    'nodejs': [
        EcosystemConfig('package.json', ['package.json'], 'json', 'nodejs'),
        EcosystemConfig('package-lock.json', ['package-lock.json'], 'json', 'nodejs'),
        EcosystemConfig('yarn.lock', ['yarn.lock'], 'text', 'nodejs'),
        EcosystemConfig('pnpm-lock.yaml', ['pnpm-lock.yaml'], 'yaml', 'nodejs'),
        EcosystemConfig('.npmrc', ['.npmrc'], 'ini', 'nodejs'),
        EcosystemConfig('.yarnrc', ['.yarnrc', '.yarnrc.yml'], 'yaml', 'nodejs'),
    ],
    
    # Go
    'go': [
        EcosystemConfig('go.mod', ['go.mod'], 'text', 'go'),
        EcosystemConfig('go.sum', ['go.sum'], 'text', 'go'),
        EcosystemConfig('main.go', ['*.go'], 'text', 'go'),
    ],
    
    # Rust
    'rust': [
        EcosystemConfig('Cargo.toml', ['Cargo.toml'], 'toml', 'rust'),
        EcosystemConfig('Cargo.lock', ['Cargo.lock'], 'text', 'rust'),
    ],
    
    # Java
    'java': [
        EcosystemConfig('pom.xml', ['pom.xml'], 'xml', 'java'),
        EcosystemConfig('build.gradle', ['build.gradle'], 'text', 'java'),
        EcosystemConfig('gradle.properties', ['gradle.properties'], 'ini', 'java'),
        EcosystemConfig('settings.gradle', ['settings.gradle'], 'text', 'java'),
        EcosystemConfig('build.gradle.kts', ['build.gradle.kts'], 'text', 'java'),
    ],
    
    # Ruby
    'ruby': [
        EcosystemConfig('Gemfile', ['Gemfile'], 'text', 'ruby'),
        EcosystemConfig('Gemfile.lock', ['Gemfile.lock'], 'text', 'ruby'),
        EcosystemConfig('.gemrc', ['.gemrc'], 'yaml', 'ruby'),
    ],
    
    # PHP
    'php': [
        EcosystemConfig('composer.json', ['composer.json'], 'json', 'php'),
        EcosystemConfig('composer.lock', ['composer.lock'], 'json', 'php'),
    ],
    
    # .NET
    'dotnet': [
        EcosystemConfig('*.csproj', ['*.csproj'], 'xml', 'dotnet'),
        EcosystemConfig('*.fsproj', ['*.fsproj'], 'xml', 'dotnet'),
        EcosystemConfig('*.vbproj', ['*.vbproj'], 'xml', 'dotnet'),
        EcosystemConfig('packages.config', ['packages.config'], 'xml', 'dotnet'),
    ],
    
    # Scala
    'scala': [
        EcosystemConfig('build.sbt', ['build.sbt'], 'text', 'scala'),
    ],
    
    # Clojure
    'clojure': [
        EcosystemConfig('project.clj', ['project.clj'], 'text', 'clojure'),
        EcosystemConfig('deps.edn', ['deps.edn'], 'text', 'clojure'),
    ],
    
    # Elixir
    'elixir': [
        EcosystemConfig('mix.exs', ['mix.exs'], 'text', 'elixir'),
        EcosystemConfig('mix.lock', ['mix.lock'], 'text', 'elixir'),
    ],
    
    # Haskell
    'haskell': [
        EcosystemConfig('cabal.project', ['cabal.project'], 'text', 'haskell'),
        EcosystemConfig('stack.yaml', ['stack.yaml'], 'yaml', 'haskell'),
    ],
    
    # R
    'r': [
        EcosystemConfig('DESCRIPTION', ['DESCRIPTION'], 'text', 'r'),
        EcosystemConfig('renv.lock', ['renv.lock'], 'json', 'r'),
    ],
    
    # Perl
    'perl': [
        EcosystemConfig('Makefile.PL', ['Makefile.PL'], 'text', 'perl'),
        EcosystemConfig('cpanfile', ['cpanfile'], 'text', 'perl'),
    ],
    
    # Swift
    'swift': [
        EcosystemConfig('Package.swift', ['Package.swift'], 'text', 'swift'),
    ],
    
    # Build Systems
    'build': [
        EcosystemConfig('Makefile', ['Makefile', 'makefile'], 'text', 'build'),
        EcosystemConfig('CMakeLists.txt', ['CMakeLists.txt'], 'text', 'build'),
        EcosystemConfig('BUILD', ['BUILD', 'BUILD.bazel'], 'text', 'build'),
        EcosystemConfig('WORKSPACE', ['WORKSPACE'], 'text', 'build'),
        EcosystemConfig('build.xml', ['build.xml'], 'xml', 'build'),
    ],
    
    # CI/CD
    'cicd': [
        EcosystemConfig('GitHub Actions', ['.github/workflows/*.yml', '.github/workflows/*.yaml'], 'yaml', 'cicd'),
        EcosystemConfig('.gitlab-ci.yml', ['.gitlab-ci.yml'], 'yaml', 'cicd'),
        EcosystemConfig('.circleci/config.yml', ['.circleci/config.yml'], 'yaml', 'cicd'),
        EcosystemConfig('Jenkinsfile', ['Jenkinsfile'], 'text', 'cicd'),
        EcosystemConfig('.travis.yml', ['.travis.yml'], 'yaml', 'cicd'),
        EcosystemConfig('azure-pipelines.yml', ['azure-pipelines.yml'], 'yaml', 'cicd'),
    ],
    
    # Infrastructure
    'infra': [
        EcosystemConfig('Dockerfile', ['Dockerfile*'], 'text', 'infra'),
        EcosystemConfig('docker-compose', ['docker-compose*.yml', 'docker-compose*.yaml'], 'yaml', 'infra'),
        EcosystemConfig('Kubernetes', ['k8s/*.yml', 'k8s/*.yaml'], 'yaml', 'infra'),
        EcosystemConfig('Terraform', ['*.tf'], 'text', 'infra'),
        EcosystemConfig('Ansible', ['playbooks/*.yml', 'roles/**/*.yml'], 'yaml', 'infra'),
        EcosystemConfig('Helm', ['Chart.yaml', 'values.yaml'], 'yaml', 'infra'),
    ],
    
    # Documentation
    'docs': [
        EcosystemConfig('Markdown', ['*.md'], 'text', 'docs'),
        EcosystemConfig('README', ['README*'], 'text', 'docs'),
        EcosystemConfig('Docs', ['docs/**/*.md'], 'text', 'docs'),
    ],
    
    # Configuration
    'config': [
        EcosystemConfig('Environment', ['.env*'], 'text', 'config'),
        EcosystemConfig('Config files', ['config.*', 'settings.*'], 'text', 'config'),
    ],
    
    # Web
    'web': [
        EcosystemConfig('HTML', ['*.html'], 'text', 'web'),
        EcosystemConfig('CSS', ['*.css', '*.scss', '*.less'], 'text', 'web'),
        EcosystemConfig('JavaScript', ['*.js'], 'text', 'web'),
        EcosystemConfig('TypeScript', ['*.ts', '*.tsx'], 'text', 'web'),
        EcosystemConfig('Vue', ['*.vue'], 'text', 'web'),
        EcosystemConfig('React', ['*.jsx'], 'text', 'web'),
    ],
}

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

def should_skip(filepath: Path) -> bool:
    """Check if file should be skipped."""
    skip_dirs = {'.git', 'node_modules', '.venv', 'venv', 'dist', 'build', '.next', '__pycache__'}
    return any(skip in filepath.parts for skip in skip_dirs)

# ─────────────────────────────────────────────────────────────────────────────
# Validator
# ─────────────────────────────────────────────────────────────────────────────
class EcosystemBrandingValidator:
    def __init__(self, repo_root: str, fix: bool = False, ecosystem: Optional[str] = None):
        self.repo_root = Path(repo_root)
        self.fix = fix
        self.ecosystem = ecosystem
        self.violations = defaultdict(list)
        self.transformations = []

    def validate_all(self):
        """Validate all ecosystems."""
        log_section("Ecosystem Branding Validation (40+ Ecosystems)")
        log_info(f"Repository: {self.repo_root}")
        log_info(f"Fix mode: {self.fix}")

        if self.ecosystem:
            ecosystems = {self.ecosystem: ECOSYSTEMS.get(self.ecosystem, [])}
        else:
            ecosystems = ECOSYSTEMS

        for ecosystem_name, configs in ecosystems.items():
            self._validate_ecosystem(ecosystem_name, configs)

        self._print_report()

    def _validate_ecosystem(self, ecosystem_name: str, configs: List[EcosystemConfig]):
        """Validate a single ecosystem."""
        log_section(f"{ecosystem_name.upper()} Ecosystem")

        for config in configs:
            self._validate_file_pattern(config)

    def _validate_file_pattern(self, config: EcosystemConfig):
        """Validate files matching a pattern."""
        for pattern in config.file_patterns:
            files = list(self.repo_root.glob(pattern))
            
            if not files:
                # Try recursive glob
                files = list(self.repo_root.rglob(pattern.lstrip('*/')))

            for filepath in files:
                if should_skip(filepath) or not filepath.is_file():
                    continue

                try:
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()

                    violations = 0
                    for old, new, _ in RULES_SORTED:
                        count = content.count(old)
                        if count > 0:
                            violations += count

                    if violations > 0:
                        log_warn(f"  {filepath.relative_to(self.repo_root)}: {violations} violation(s)")
                        self.violations[config.name].append((filepath, violations))

                        if self.fix:
                            new_content, replacements = apply_branding_rules(content)
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            log_ok(f"    Fixed: {replacements} replacement(s)")
                            self.transformations.append((filepath, replacements))
                    else:
                        log_ok(f"  {filepath.relative_to(self.repo_root)}")

                except Exception as e:
                    log_warn(f"  {filepath}: {e}")

    def _print_report(self):
        """Print validation report."""
        log_section("Ecosystem Validation Report")

        total_violations = sum(len(v) for v in self.violations.values())
        total_transformations = len(self.transformations)

        log_ok(f"Total violations: {total_violations}")
        log_ok(f"Total transformations: {total_transformations}")

        if total_violations == 0:
            log_ok("✓ All ecosystem branding checks passed!")
            return True
        else:
            log_fail("✗ Ecosystem branding validation failed")
            return False

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description='NasTech Ecosystem Branding Validator (40+ ecosystems)'
    )
    parser.add_argument('--repo', default='.', help='Repository root path')
    parser.add_argument('--fix', action='store_true', help='Apply fixes')
    parser.add_argument('--report', action='store_true', help='Generate report')
    parser.add_argument('--ecosystem', choices=list(ECOSYSTEMS.keys()), 
                        help='Validate specific ecosystem only')

    args = parser.parse_args()

    validator = EcosystemBrandingValidator(args.repo, fix=args.fix, ecosystem=args.ecosystem)
    validator.validate_all()

if __name__ == '__main__':
    main()
