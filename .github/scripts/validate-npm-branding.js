#!/usr/bin/env node
/**
 * NasTech npm Branding Validator (v3.0)
 * 
 * Validates and transforms branding in:
 * - package.json (name, description, keywords, repository, bugs, homepage)
 * - package-lock.json (dependencies)
 * - .npmrc (registry, scope configuration)
 * - Monorepo workspaces
 * 
 * Usage:
 *   node validate-npm-branding.js [--repo ROOT] [--fix] [--report]
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ─────────────────────────────────────────────────────────────────────────────
// Colors
// ─────────────────────────────────────────────────────────────────────────────
const Colors = {
  OK: '\x1b[92m',
  WARN: '\x1b[93m',
  FAIL: '\x1b[91m',
  INFO: '\x1b[94m',
  CYAN: '\x1b[96m',
  RESET: '\x1b[0m',
  BOLD: '\x1b[1m',
};

const log = {
  ok: (msg) => console.log(`${Colors.OK}[✓]${Colors.RESET} ${msg}`),
  warn: (msg) => console.warn(`${Colors.WARN}[⚠]${Colors.RESET} ${msg}`),
  fail: (msg) => console.error(`${Colors.FAIL}[✗]${Colors.RESET} ${msg}`),
  info: (msg) => console.log(`${Colors.INFO}[•]${Colors.RESET} ${msg}`),
  section: (title) => {
    console.log(`\n${Colors.CYAN}${'='.repeat(60)}${Colors.RESET}`);
    console.log(`${Colors.CYAN}${Colors.BOLD}  ${title}${Colors.RESET}`);
    console.log(`${Colors.CYAN}${'='.repeat(60)}${Colors.RESET}`);
  },
};

// ─────────────────────────────────────────────────────────────────────────────
// Branding Rules
// ─────────────────────────────────────────────────────────────────────────────
const BRANDING_RULES = [
  { old: 'hermes-agent', new: 'nastech-agent', priority: 100 },
  { old: 'Hermes Agent', new: 'NasTech Agent', priority: 95 },
  { old: '@nous-research', new: '@nastech-research', priority: 90 },
  { old: 'nousresearch', new: 'nastechairesearch', priority: 85 },
  { old: 'NousResearch', new: 'nastechai', priority: 85 },
  { old: 'Nous Research', new: 'NasTech', priority: 80 },
  { old: 'hermes', new: 'nastech', priority: 75 },
  { old: 'Hermes', new: 'NasTech', priority: 75 },
];

const RULES_SORTED = BRANDING_RULES.sort((a, b) => b.priority - a.priority);

// ─────────────────────────────────────────────────────────────────────────────
// Utilities
// ─────────────────────────────────────────────────────────────────────────────
function applyBrandingRules(text) {
  let result = text;
  let replacements = 0;

  for (const rule of RULES_SORTED) {
    const regex = new RegExp(rule.old, 'g');
    const matches = (result.match(regex) || []).length;
    if (matches > 0) {
      result = result.replace(regex, rule.new);
      replacements += matches;
    }
  }

  return { result, replacements };
}

function transformObject(obj) {
  let replacements = 0;

  if (typeof obj === 'string') {
    const { result, replacements: count } = applyBrandingRules(obj);
    return { result, replacements: count };
  }

  if (Array.isArray(obj)) {
    for (let i = 0; i < obj.length; i++) {
      if (typeof obj[i] === 'string') {
        const { result, replacements: count } = applyBrandingRules(obj[i]);
        obj[i] = result;
        replacements += count;
      } else if (typeof obj[i] === 'object' && obj[i] !== null) {
        const { replacements: count } = transformObject(obj[i]);
        replacements += count;
      }
    }
    return { result: obj, replacements };
  }

  if (typeof obj === 'object' && obj !== null) {
    for (const key in obj) {
      if (typeof obj[key] === 'string') {
        const { result, replacements: count } = applyBrandingRules(obj[key]);
        obj[key] = result;
        replacements += count;
      } else if (typeof obj[key] === 'object' && obj[key] !== null) {
        const { replacements: count } = transformObject(obj[key]);
        replacements += count;
      }
    }
  }

  return { result: obj, replacements };
}

// ─────────────────────────────────────────────────────────────────────────────
// Validators
// ─────────────────────────────────────────────────────────────────────────────
class NpmBrandingValidator {
  constructor(repoRoot, options = {}) {
    this.repoRoot = repoRoot;
    this.fix = options.fix || false;
    this.violations = [];
    this.transformations = [];
  }

  validatePackageJson(filepath) {
    if (!fs.existsSync(filepath)) return;

    try {
      const content = fs.readFileSync(filepath, 'utf-8');
      const data = JSON.parse(content);

      // Check name
      if (data.name && data.name.includes('hermes')) {
        this.violations.push({
          file: filepath,
          type: 'package-name',
          value: data.name,
          message: `Package name contains 'hermes': ${data.name}`,
        });
      }

      // Check for @nous-research scope
      if (data.dependencies) {
        for (const dep in data.dependencies) {
          if (dep.includes('@nous-research')) {
            this.violations.push({
              file: filepath,
              type: 'npm-scope',
              value: dep,
              message: `Dependency uses @nous-research scope: ${dep}`,
            });
          }
        }
      }

      if (data.devDependencies) {
        for (const dep in data.devDependencies) {
          if (dep.includes('@nous-research')) {
            this.violations.push({
              file: filepath,
              type: 'npm-scope',
              value: dep,
              message: `Dev dependency uses @nous-research scope: ${dep}`,
            });
          }
        }
      }

      // Fix if requested
      if (this.fix) {
        const { replacements } = transformObject(data);
        if (replacements > 0) {
          fs.writeFileSync(filepath, JSON.stringify(data, null, 2) + '\n');
          this.transformations.push({
            file: filepath,
            replacements,
          });
        }
      }
    } catch (err) {
      log.warn(`Failed to parse ${filepath}: ${err.message}`);
    }
  }

  validatePackageLock(filepath) {
    if (!fs.existsSync(filepath)) return;

    try {
      const content = fs.readFileSync(filepath, 'utf-8');
      const data = JSON.parse(content);

      // Check packages
      if (data.packages) {
        for (const pkgPath in data.packages) {
          const pkg = data.packages[pkgPath];
          if (pkg.name && pkg.name.includes('hermes')) {
            this.violations.push({
              file: filepath,
              type: 'lock-package-name',
              value: pkg.name,
              message: `Locked package name contains 'hermes': ${pkg.name}`,
            });
          }
        }
      }

      // Fix if requested
      if (this.fix) {
        const { replacements } = transformObject(data);
        if (replacements > 0) {
          fs.writeFileSync(filepath, JSON.stringify(data, null, 2) + '\n');
          this.transformations.push({
            file: filepath,
            replacements,
          });
        }
      }
    } catch (err) {
      log.warn(`Failed to parse ${filepath}: ${err.message}`);
    }
  }

  validateNpmrc(filepath) {
    if (!fs.existsSync(filepath)) return;

    try {
      const content = fs.readFileSync(filepath, 'utf-8');

      if (content.includes('@nous-research')) {
        this.violations.push({
          file: filepath,
          type: 'npmrc-scope',
          message: '.npmrc contains @nous-research configuration',
        });

        if (this.fix) {
          const fixed = content.replace(/@nous-research/g, '@nastech-research');
          fs.writeFileSync(filepath, fixed);
          this.transformations.push({
            file: filepath,
            replacements: 1,
          });
        }
      }
    } catch (err) {
      log.warn(`Failed to read ${filepath}: ${err.message}`);
    }
  }

  validateYarnLock(filepath) {
    if (!fs.existsSync(filepath)) return;

    try {
      const content = fs.readFileSync(filepath, 'utf-8');

      if (content.includes('hermes') || content.includes('@nous-research')) {
        this.violations.push({
          file: filepath,
          type: 'yarn-lock',
          message: 'yarn.lock contains branding references (manual review recommended)',
        });
      }
    } catch (err) {
      log.warn(`Failed to read ${filepath}: ${err.message}`);
    }
  }

  validateAll() {
    log.section('npm Branding Validation');

    // Find all package.json files
    try {
      const packageJsonFiles = execSync(
        `find "${this.repoRoot}" -name "package.json" -not -path "*/node_modules/*" -not -path "*/.git/*"`,
        { encoding: 'utf-8' }
      ).split('\n').filter(Boolean);

      for (const file of packageJsonFiles) {
        this.validatePackageJson(file);
      }
    } catch (err) {
      log.warn(`Failed to find package.json files: ${err.message}`);
    }

    // Find package-lock.json
    try {
      const lockFiles = execSync(
        `find "${this.repoRoot}" -name "package-lock.json" -not -path "*/node_modules/*" -not -path "*/.git/*"`,
        { encoding: 'utf-8' }
      ).split('\n').filter(Boolean);

      for (const file of lockFiles) {
        this.validatePackageLock(file);
      }
    } catch (err) {
      log.warn(`Failed to find package-lock.json files: ${err.message}`);
    }

    // Find .npmrc
    try {
      const npmrcFiles = execSync(
        `find "${this.repoRoot}" -name ".npmrc" -not -path "*/.git/*"`,
        { encoding: 'utf-8' }
      ).split('\n').filter(Boolean);

      for (const file of npmrcFiles) {
        this.validateNpmrc(file);
      }
    } catch (err) {
      log.warn(`Failed to find .npmrc files: ${err.message}`);
    }

    // Find yarn.lock
    try {
      const yarnLockFiles = execSync(
        `find "${this.repoRoot}" -name "yarn.lock" -not -path "*/.git/*"`,
        { encoding: 'utf-8' }
      ).split('\n').filter(Boolean);

      for (const file of yarnLockFiles) {
        this.validateYarnLock(file);
      }
    } catch (err) {
      log.warn(`Failed to find yarn.lock files: ${err.message}`);
    }

    return {
      violations: this.violations,
      transformations: this.transformations,
      passed: this.violations.length === 0,
    };
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────────────────────────────────────
function main() {
  const args = process.argv.slice(2);
  let repoRoot = '.';
  let fix = false;
  let report = false;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--repo') {
      repoRoot = args[++i];
    } else if (args[i] === '--fix') {
      fix = true;
    } else if (args[i] === '--report') {
      report = true;
    }
  }

  const validator = new NpmBrandingValidator(repoRoot, { fix });
  const results = validator.validateAll();

  log.ok(`Violations found: ${results.violations.length}`);
  log.ok(`Transformations applied: ${results.transformations.length}`);

  if (results.violations.length > 0) {
    console.log('\nViolations:');
    for (const v of results.violations) {
      console.log(`  - ${v.file}: ${v.message}`);
    }
  }

  if (results.transformations.length > 0) {
    console.log('\nTransformations:');
    for (const t of results.transformations) {
      console.log(`  - ${t.file}: ${t.replacements} replacement(s)`);
    }
  }

  if (results.passed) {
    log.ok('✓ All npm branding checks passed!');
    process.exit(0);
  } else {
    log.fail('✗ npm branding validation failed');
    process.exit(1);
  }
}

main();
