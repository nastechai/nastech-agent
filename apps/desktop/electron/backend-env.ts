import path from 'node:path'

// Match the POSIX fallback surface used by the Python terminal environment.
// macOS apps launched from Finder/Dock often inherit only /usr/bin:/bin:/usr/sbin:/sbin,
// which misses Apple Silicon Homebrew and user-installed CLI tools such as codex.
const POSIX_SANE_PATH_ENTRIES = Object.freeze([
  '/opt/homebrew/bin',
  '/opt/homebrew/sbin',
  '/usr/local/sbin',
  '/usr/local/bin',
  '/usr/sbin',
  '/usr/bin',
  '/sbin',
  '/bin'
])

function delimiterForPlatform(platform = process.platform) {
  return platform === 'win32' ? ';' : ':'
}

function pathModuleForPlatform(platform = process.platform) {
  return platform === 'win32' ? path.win32 : path.posix
}

function pathEnvKey(env = process.env, platform = process.platform) {
  if (platform !== 'win32') {
    return 'PATH'
  }

  return Object.keys(env || {}).find(key => key.toUpperCase() === 'PATH') || 'PATH'
}

function currentPathValue(env = process.env, platform = process.platform) {
  const key = pathEnvKey(env, platform)

  return env?.[key] || ''
}

function appendUniquePathEntries(entries, { delimiter = path.delimiter } = {}) {
  const seen = new Set()
  const ordered = []

  for (const entry of entries) {
    if (!entry) {
      continue
    }

    const parts = Array.isArray(entry) ? entry : String(entry).split(delimiter)

    for (const part of parts) {
      if (!part || seen.has(part)) {
        continue
      }

      seen.add(part)
      ordered.push(part)
    }
  }

  return ordered.join(delimiter)
}

/**
 * NasTech-managed Node.js directories, in preferred lookup order.
 *
 * There are two on-disk layouts. `scripts/install.ps1` unpacks portable Node
 * straight into `%LOCALAPPDATA%\nastech\node` (node.exe at the root, no `bin\`);
 * `scripts/install.sh` and the node-bootstrap helper use the POSIX
 * `$NASTECH_HOME/node/bin`. Emit BOTH on every platform so mixed and migrated
 * installs resolve, leading with the layout native to the current platform.
 *
 * This is the single source of truth for the ordering rule on the Node side —
 * `main.ts` imports it rather than keeping its own copy. Mirrors
 * `iter_nastech_node_dirs()` in nastech_constants.py, which the Electron main
 * process cannot import.
 */
function nastechManagedNodePathEntries(
  nastechHome,
  { platform = process.platform, pathModule = pathModuleForPlatform(platform) }: any = {}
) {
  if (!nastechHome) {
    return []
  }

  const root = pathModule.join(nastechHome, 'node')
  const bin = pathModule.join(root, 'bin')

  return platform === 'win32' ? [root, bin] : [bin, root]
}

function buildDesktopBackendPath({
  nastechHome,
  venvRoot,
  currentPath = '',
  platform = process.platform,
  pathModule = pathModuleForPlatform(platform)
}: any = {}) {
  const delimiter = delimiterForPlatform(platform)
  const nastechNodeDirs = nastechManagedNodePathEntries(nastechHome, { platform, pathModule })
  const venvBin = venvRoot ? pathModule.join(venvRoot, platform === 'win32' ? 'Scripts' : 'bin') : null
  const saneEntries = platform === 'win32' ? [] : POSIX_SANE_PATH_ENTRIES

  return appendUniquePathEntries([nastechNodeDirs, venvBin, currentPath, saneEntries], { delimiter })
}

function normalizeNasTechHomeRoot(nastechHome, { pathModule = pathModuleForPlatform(process.platform) }: any = {}) {
  if (!nastechHome) {
    return nastechHome
  }

  const resolved = pathModule.resolve(String(nastechHome))
  const parent = pathModule.dirname(resolved)

  if (pathModule.basename(parent).toLowerCase() === 'profiles') {
    return pathModule.dirname(parent)
  }

  return resolved
}

function buildDesktopBackendEnv({
  nastechHome,
  pythonPathEntries = [],
  venvRoot,
  currentEnv = process.env,
  platform = process.platform,
  pathModule = pathModuleForPlatform(platform)
}: any = {}) {
  const delimiter = delimiterForPlatform(platform)
  const currentPythonPath = currentEnv?.PYTHONPATH || ''
  const key = pathEnvKey(currentEnv, platform)

  return {
    PYTHONPATH: appendUniquePathEntries([...pythonPathEntries, currentPythonPath], { delimiter }),
    // Force PEP 540 UTF-8 mode in the spawned Python backend so its stdio and
    // subprocess defaults are UTF-8 even on non-UTF-8 Windows locales (GBK,
    // cp1252, ...). nastech_bootstrap sets this inside the child too, but only
    // after import — anything emitted earlier (interpreter startup errors,
    // pre-bootstrap tracebacks) still decodes with the locale default without
    // this. User's explicit setting wins. Re-port of PR #56499 (echoriver89).
    PYTHONUTF8: currentEnv?.PYTHONUTF8 ?? '1',
    [key]: buildDesktopBackendPath({
      nastechHome,
      venvRoot,
      currentPath: currentPathValue(currentEnv, platform),
      platform,
      pathModule
    })
  }
}

export {
  appendUniquePathEntries,
  buildDesktopBackendEnv,
  buildDesktopBackendPath,
  delimiterForPlatform,
  nastechManagedNodePathEntries,
  normalizeNasTechHomeRoot,
  pathEnvKey,
  POSIX_SANE_PATH_ENTRIES
}
