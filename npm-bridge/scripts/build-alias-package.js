#!/usr/bin/env node

/**
 * Builds an alias package manifest for `nastechagent` (no hyphen).
 * The alias package installs and launches the same Nastech Agent runtime
 * as the canonical `nastech-agent` package.
 *
 * Output: dist/nastechagent/package.json (and supporting files)
 *
 * Usage:
 *   npm run build:alias
 *   npm pack --dry-run ./dist/nastechagent
 */

const fs = require("node:fs");
const path = require("node:path");

const { ALIAS_PACKAGE_NAME, getPackageBinNames } = require("../lib/package-metadata");

const rootDir = path.resolve(__dirname, "..");
const distDir = path.resolve(rootDir, "dist", ALIAS_PACKAGE_NAME);

const canonicalPkg = JSON.parse(fs.readFileSync(path.join(rootDir, "package.json"), "utf8"));

const binNames = getPackageBinNames(ALIAS_PACKAGE_NAME);
const binEntries = {};
for (const name of binNames) {
  binEntries[name] = "bin/nastech-agent.js";
}

const aliasPkg = {
  name: ALIAS_PACKAGE_NAME,
  version: canonicalPkg.version,
  description: `Alias for nastech-agent — ${canonicalPkg.description}`,
  license: canonicalPkg.license,
  type: canonicalPkg.type,
  bin: binEntries,
  scripts: {
    postinstall: "node scripts/postinstall.js"
  },
  repository: canonicalPkg.repository,
  bugs: canonicalPkg.bugs,
  homepage: canonicalPkg.homepage,
  engines: canonicalPkg.engines,
  files: canonicalPkg.files,
  nastechAgent: canonicalPkg.nastechAgent
};

fs.mkdirSync(path.join(distDir, "bin"), { recursive: true });
fs.mkdirSync(path.join(distDir, "lib"), { recursive: true });
fs.mkdirSync(path.join(distDir, "scripts"), { recursive: true });

fs.writeFileSync(
  path.join(distDir, "package.json"),
  JSON.stringify(aliasPkg, null, 2) + "\n"
);

for (const file of ["bin/nastech.js", "bin/nastech-agent.js", "lib/python-launcher.js",
  "lib/package-metadata.js", "scripts/postinstall.js",
  "DISCLAIMER.md", "LICENSE", "NOTICE", "PRIVACY.md", "README.md", "SECURITY.md"]) {
  const src = path.join(rootDir, file);
  const dest = path.join(distDir, file);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, dest);
  }
}

console.log(`Built alias package: ${distDir}`);
console.log(`  name:    ${aliasPkg.name}`);
console.log(`  version: ${aliasPkg.version}`);
