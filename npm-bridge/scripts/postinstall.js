#!/usr/bin/env node

const { spawnSync } = require("node:child_process");
const path = require("node:path");
const packageJson = require("../package.json");
const { getRelatedPackageNames } = require("../lib/package-metadata");
const { findPython, getPythonPackageSpec } = require("../lib/python-launcher");

const candidate = findPython();
const packageSpec = getPythonPackageSpec();
const packageName = packageJson.name;

function warnIfRelatedPackageInstalled() {
  const relatedPackages = getRelatedPackageNames(packageName);

  if (relatedPackages.length === 0) {
    return;
  }

  const npmRootCommand = process.env.npm_execpath
    ? { command: process.execPath, args: [process.env.npm_execpath, "root", "-g"] }
    : { command: process.platform === "win32" ? "npm.cmd" : "npm", args: ["root", "-g"] };

  const rootResult = spawnSync(npmRootCommand.command, npmRootCommand.args, {
    encoding: "utf8",
    windowsHide: true
  });

  if (rootResult.status !== 0) {
    return;
  }

  const globalRoot = rootResult.stdout.trim();

  for (const relatedPackage of relatedPackages) {
    const relatedPackageJson = path.join(globalRoot, relatedPackage, "package.json");

    try {
      if (require("node:fs").existsSync(relatedPackageJson)) {
        console.warn(
          `${relatedPackage} is already installed globally. ` +
            `${packageName} is an alias package for the same Nastech Agent runtime; ` +
            "you do not need to install both."
        );
      }
    } catch {
      return;
    }
  }
}

warnIfRelatedPackageInstalled();

if (!candidate) {
  console.error("Nastech Agent requires Python 3.11 or newer.");
  console.error(`Install Python, then run: python -m pip install --upgrade ${packageSpec}`);
  process.exit(1);
}

function runPip(extraArgs) {
  return spawnSync(
    candidate.command,
    [...candidate.args, "-m", "pip", "install", "--upgrade", ...extraArgs, packageSpec],
    { stdio: "inherit", windowsHide: true }
  );
}

let result = runPip([]);

if (result.status !== 0) {
  console.warn("Global pip install failed; retrying with --user.");
  result = runPip(["--user"]);
}

if (result.status !== 0) {
  console.error(`Failed to install ${packageSpec}.`);
  process.exit(result.status || 1);
}
