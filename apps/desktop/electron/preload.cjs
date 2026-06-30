const { contextBridge, ipcRenderer, webUtils } = require('electron')

contextBridge.exposeInMainWorld('nastechDesktop', {
  getConnection: profile => ipcRenderer.invoke('nastech:connection', profile),
  revalidateConnection: () => ipcRenderer.invoke('nastech:connection:revalidate'),
  touchBackend: profile => ipcRenderer.invoke('nastech:backend:touch', profile),
  getGatewayWsUrl: profile => ipcRenderer.invoke('nastech:gateway:ws-url', profile),
  openSessionWindow: (sessionId, opts) => ipcRenderer.invoke('nastech:window:openSession', sessionId, opts),
  openNewSessionWindow: () => ipcRenderer.invoke('nastech:window:openNewSession'),
  petOverlay: {
    // Main renderer → main process: window lifecycle + drag. `request` is
    // `{ bounds, screen }`; resolves with the screen bounds it actually used.
    open: request => ipcRenderer.invoke('nastech:pet-overlay:open', request),
    close: () => ipcRenderer.invoke('nastech:pet-overlay:close'),
    setBounds: bounds => ipcRenderer.send('nastech:pet-overlay:set-bounds', bounds),
    setIgnoreMouse: ignore => ipcRenderer.send('nastech:pet-overlay:ignore-mouse', ignore),
    // Flip the overlay focusable (and focus it) while the composer needs keys.
    setFocusable: focusable => ipcRenderer.send('nastech:pet-overlay:set-focusable', focusable),
    // Main renderer → overlay (forwarded by main): push the latest pet state.
    pushState: payload => ipcRenderer.send('nastech:pet-overlay:state', payload),
    // Overlay → main renderer (forwarded by main): pop back in / composer submit.
    control: payload => ipcRenderer.send('nastech:pet-overlay:control', payload),
    // Overlay subscribes to state pushes.
    onState: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('nastech:pet-overlay:state', listener)
      return () => ipcRenderer.removeListener('nastech:pet-overlay:state', listener)
    },
    // Main renderer subscribes to overlay control messages.
    onControl: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('nastech:pet-overlay:control', listener)
      return () => ipcRenderer.removeListener('nastech:pet-overlay:control', listener)
    }
  },
  getBootProgress: () => ipcRenderer.invoke('nastech:boot-progress:get'),
  getConnectionConfig: profile => ipcRenderer.invoke('nastech:connection-config:get', profile),
  saveConnectionConfig: payload => ipcRenderer.invoke('nastech:connection-config:save', payload),
  applyConnectionConfig: payload => ipcRenderer.invoke('nastech:connection-config:apply', payload),
  testConnectionConfig: payload => ipcRenderer.invoke('nastech:connection-config:test', payload),
  probeConnectionConfig: remoteUrl => ipcRenderer.invoke('nastech:connection-config:probe', remoteUrl),
  oauthLoginConnectionConfig: remoteUrl => ipcRenderer.invoke('nastech:connection-config:oauth-login', remoteUrl),
  oauthLogoutConnectionConfig: remoteUrl => ipcRenderer.invoke('nastech:connection-config:oauth-logout', remoteUrl),
  profile: {
    get: () => ipcRenderer.invoke('nastech:profile:get'),
    set: name => ipcRenderer.invoke('nastech:profile:set', name)
  },
  api: request => ipcRenderer.invoke('nastech:api', request),
  notify: payload => ipcRenderer.invoke('nastech:notify', payload),
  requestMicrophoneAccess: () => ipcRenderer.invoke('nastech:requestMicrophoneAccess'),
  readFileDataUrl: filePath => ipcRenderer.invoke('nastech:readFileDataUrl', filePath),
  readFileText: filePath => ipcRenderer.invoke('nastech:readFileText', filePath),
  selectPaths: options => ipcRenderer.invoke('nastech:selectPaths', options),
  writeClipboard: text => ipcRenderer.invoke('nastech:writeClipboard', text),
  saveImageFromUrl: url => ipcRenderer.invoke('nastech:saveImageFromUrl', url),
  saveImageBuffer: (data, ext) => ipcRenderer.invoke('nastech:saveImageBuffer', { data, ext }),
  saveClipboardImage: () => ipcRenderer.invoke('nastech:saveClipboardImage'),
  getPathForFile: file => {
    try {
      return webUtils.getPathForFile(file) || ''
    } catch {
      return ''
    }
  },
  normalizePreviewTarget: (target, baseDir) => ipcRenderer.invoke('nastech:normalizePreviewTarget', target, baseDir),
  watchPreviewFile: url => ipcRenderer.invoke('nastech:watchPreviewFile', url),
  stopPreviewFileWatch: id => ipcRenderer.invoke('nastech:stopPreviewFileWatch', id),
  setTitleBarTheme: payload => ipcRenderer.send('nastech:titlebar-theme', payload),
  setNativeTheme: mode => ipcRenderer.send('nastech:native-theme', mode),
  setTranslucency: payload => ipcRenderer.send('nastech:translucency', payload),
  setPreviewShortcutActive: active => ipcRenderer.send('nastech:previewShortcutActive', Boolean(active)),
  openExternal: url => ipcRenderer.invoke('nastech:openExternal', url),
  openPreviewInBrowser: url => ipcRenderer.invoke('nastech:openPreviewInBrowser', url),
  fetchLinkTitle: url => ipcRenderer.invoke('nastech:fetchLinkTitle', url),
  sanitizeWorkspaceCwd: cwd => ipcRenderer.invoke('nastech:workspace:sanitize', cwd),
  settings: {
    getDefaultProjectDir: () => ipcRenderer.invoke('nastech:setting:defaultProjectDir:get'),
    setDefaultProjectDir: dir => ipcRenderer.invoke('nastech:setting:defaultProjectDir:set', dir),
    pickDefaultProjectDir: () => ipcRenderer.invoke('nastech:setting:defaultProjectDir:pick')
  },
  revealLogs: () => ipcRenderer.invoke('nastech:logs:reveal'),
  getRecentLogs: () => ipcRenderer.invoke('nastech:logs:recent'),
  readDir: dirPath => ipcRenderer.invoke('nastech:fs:readDir', dirPath),
  gitRoot: startPath => ipcRenderer.invoke('nastech:fs:gitRoot', startPath),
  revealPath: targetPath => ipcRenderer.invoke('nastech:fs:reveal', targetPath),
  renamePath: (targetPath, newName) => ipcRenderer.invoke('nastech:fs:rename', targetPath, newName),
  writeTextFile: (filePath, content) => ipcRenderer.invoke('nastech:fs:writeText', filePath, content),
  trashPath: targetPath => ipcRenderer.invoke('nastech:fs:trash', targetPath),
  git: {
    worktreeList: repoPath => ipcRenderer.invoke('nastech:git:worktreeList', repoPath),
    worktreeAdd: (repoPath, options) => ipcRenderer.invoke('nastech:git:worktreeAdd', repoPath, options),
    worktreeRemove: (repoPath, worktreePath, options) =>
      ipcRenderer.invoke('nastech:git:worktreeRemove', repoPath, worktreePath, options),
    branchSwitch: (repoPath, branch) => ipcRenderer.invoke('nastech:git:branchSwitch', repoPath, branch),
    branchList: repoPath => ipcRenderer.invoke('nastech:git:branchList', repoPath),
    repoStatus: repoPath => ipcRenderer.invoke('nastech:git:repoStatus', repoPath),
    fileDiff: (repoPath, filePath) => ipcRenderer.invoke('nastech:git:fileDiff', repoPath, filePath),
    scanRepos: (roots, options) => ipcRenderer.invoke('nastech:git:scanRepos', roots, options),
    review: {
      list: (repoPath, scope, baseRef) => ipcRenderer.invoke('nastech:git:review:list', repoPath, scope, baseRef),
      diff: (repoPath, filePath, scope, baseRef, staged) =>
        ipcRenderer.invoke('nastech:git:review:diff', repoPath, filePath, scope, baseRef, staged),
      stage: (repoPath, filePath) => ipcRenderer.invoke('nastech:git:review:stage', repoPath, filePath),
      unstage: (repoPath, filePath) => ipcRenderer.invoke('nastech:git:review:unstage', repoPath, filePath),
      revert: (repoPath, filePath) => ipcRenderer.invoke('nastech:git:review:revert', repoPath, filePath),
      revParse: (repoPath, ref) => ipcRenderer.invoke('nastech:git:review:revParse', repoPath, ref),
      commit: (repoPath, message, push) => ipcRenderer.invoke('nastech:git:review:commit', repoPath, message, push),
      commitContext: repoPath => ipcRenderer.invoke('nastech:git:review:commitContext', repoPath),
      push: repoPath => ipcRenderer.invoke('nastech:git:review:push', repoPath),
      shipInfo: repoPath => ipcRenderer.invoke('nastech:git:review:shipInfo', repoPath),
      createPr: repoPath => ipcRenderer.invoke('nastech:git:review:createPr', repoPath)
    }
  },
  terminal: {
    dispose: id => ipcRenderer.invoke('nastech:terminal:dispose', id),
    resize: (id, size) => ipcRenderer.invoke('nastech:terminal:resize', id, size),
    start: options => ipcRenderer.invoke('nastech:terminal:start', options),
    write: (id, data) => ipcRenderer.invoke('nastech:terminal:write', id, data),
    onData: (id, callback) => {
      const channel = `nastech:terminal:${id}:data`
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on(channel, listener)
      return () => ipcRenderer.removeListener(channel, listener)
    },
    onExit: (id, callback) => {
      const channel = `nastech:terminal:${id}:exit`
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on(channel, listener)
      return () => ipcRenderer.removeListener(channel, listener)
    }
  },
  onClosePreviewRequested: callback => {
    const listener = () => callback()
    ipcRenderer.on('nastech:close-preview-requested', listener)
    return () => ipcRenderer.removeListener('nastech:close-preview-requested', listener)
  },
  onOpenUpdatesRequested: callback => {
    const listener = () => callback()
    ipcRenderer.on('nastech:open-updates', listener)
    return () => ipcRenderer.removeListener('nastech:open-updates', listener)
  },
  onDeepLink: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('nastech:deep-link', listener)
    return () => ipcRenderer.removeListener('nastech:deep-link', listener)
  },
  signalDeepLinkReady: () => ipcRenderer.invoke('nastech:deep-link-ready'),
  onWindowStateChanged: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('nastech:window-state-changed', listener)
    return () => ipcRenderer.removeListener('nastech:window-state-changed', listener)
  },
  onFocusSession: callback => {
    const listener = (_event, sessionId) => callback(sessionId)
    ipcRenderer.on('nastech:focus-session', listener)
    return () => ipcRenderer.removeListener('nastech:focus-session', listener)
  },
  onNotificationAction: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('nastech:notification-action', listener)
    return () => ipcRenderer.removeListener('nastech:notification-action', listener)
  },
  onPreviewFileChanged: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('nastech:preview-file-changed', listener)
    return () => ipcRenderer.removeListener('nastech:preview-file-changed', listener)
  },
  onBackendExit: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('nastech:backend-exit', listener)
    return () => ipcRenderer.removeListener('nastech:backend-exit', listener)
  },
  onPowerResume: callback => {
    const listener = () => callback()
    ipcRenderer.on('nastech:power-resume', listener)
    return () => ipcRenderer.removeListener('nastech:power-resume', listener)
  },
  onBootProgress: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('nastech:boot-progress', listener)
    return () => ipcRenderer.removeListener('nastech:boot-progress', listener)
  },
  // First-launch bootstrap progress -- emitted by the install.ps1 stage
  // runner in main.cjs (apps/desktop/electron/bootstrap-runner.cjs).
  // Renderer's install overlay subscribes to live events and queries the
  // current snapshot via getBootstrapState() to recover after a devtools
  // reload mid-bootstrap.
  getBootstrapState: () => ipcRenderer.invoke('nastech:bootstrap:get'),
  resetBootstrap: () => ipcRenderer.invoke('nastech:bootstrap:reset'),
  repairBootstrap: () => ipcRenderer.invoke('nastech:bootstrap:repair'),
  cancelBootstrap: () => ipcRenderer.invoke('nastech:bootstrap:cancel'),
  onBootstrapEvent: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('nastech:bootstrap:event', listener)
    return () => ipcRenderer.removeListener('nastech:bootstrap:event', listener)
  },
  getVersion: () => ipcRenderer.invoke('nastech:version'),
  getRemoteDisplayReason: () => ipcRenderer.invoke('nastech:get-remote-display-reason'),
  uninstall: {
    summary: () => ipcRenderer.invoke('nastech:uninstall:summary'),
    run: mode => ipcRenderer.invoke('nastech:uninstall:run', { mode })
  },
  updates: {
    check: () => ipcRenderer.invoke('nastech:updates:check'),
    apply: opts => ipcRenderer.invoke('nastech:updates:apply', opts),
    getBranch: () => ipcRenderer.invoke('nastech:updates:branch:get'),
    setBranch: name => ipcRenderer.invoke('nastech:updates:branch:set', name),
    onProgress: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('nastech:updates:progress', listener)
      return () => ipcRenderer.removeListener('nastech:updates:progress', listener)
    }
  },
  themes: {
    fetchMarketplace: id => ipcRenderer.invoke('nastech:vscode-theme:fetch', id),
    searchMarketplace: query => ipcRenderer.invoke('nastech:vscode-theme:search', query)
  }
})
