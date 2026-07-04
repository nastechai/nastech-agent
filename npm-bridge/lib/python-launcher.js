const { spawn, spawnSync } = require("node:child_process");
const path = require("node:path");

const packageJson = require("../package.json");

function getPythonCandidates(platform = process.platform) {
  if (platform === "win32") {
    return [
      { command: "py", args: ["-3"] },
      { command: "python", args: [] },
      { command: "python3", args: [] }
    ];
  }

  return [
    { command: "python3", args: [] },
    { command: "python", args: [] }
  ];
}

function findPython(candidates = getPythonCandidates()) {
  for (const candidate of candidates) {
    const result = spawnSync(
      candidate.command,
      [...candidate.args, "-c", "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)"],
      { encoding: "utf8", windowsHide: true }
    );

    if (result.status === 0) {
      return candidate;
    }
  }

  return null;
}

function normalizeBinName(binName) {
  const baseName = path.basename(binName || "nastech-agent").toLowerCase();
  return baseName.replace(/(\.cmd|\.exe)$/i, "");
}

function getPythonEntryPoint(binName) {
  return normalizeBinName(binName) === "nastech" ? "nastech_cli.main" : "run_agent";
}

function getPythonCode(binName) {
  const moduleName = getPythonEntryPoint(binName);
  return `from ${moduleName} import main; raise SystemExit(main())`;
}

function buildPythonInvocation(candidate, binName, userArgs) {
  return {
    command: candidate.command,
    args: [...candidate.args, "-c", getPythonCode(binName), ...userArgs]
  };
}

function getPythonPackageSpec() {
  const version = packageJson.nastechAgent?.pythonPackageVersion || packageJson.version;
  return `nastech-agent==${version}`;
}

function runNastech(binName, userArgs, stdio = "inherit") {
  const candidate = findPython();

  if (!candidate) {
    console.error("Nastech Agent requires Python 3.11 or newer.");
    console.error("Install Python, then run: python -m pip install --upgrade " + getPythonPackageSpec());
    return 1;
  }

  const invocation = buildPythonInvocation(candidate, binName, userArgs);
  const child = spawn(invocation.command, invocation.args, { stdio, windowsHide: false });

  child.on("exit", (code, signal) => {
    if (signal) {
      process.kill(process.pid, signal);
      return;
    }

    process.exit(code ?? 1);
  });

  child.on("error", (error) => {
    console.error(error.message);
    process.exit(1);
  });

  return 0;
}

module.exports = {
  buildPythonInvocation,
  findPython,
  getPythonCandidates,
  getPythonEntryPoint,
  getPythonPackageSpec,
  runNastech
};
