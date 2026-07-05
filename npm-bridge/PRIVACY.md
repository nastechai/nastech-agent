# Privacy

This npm bridge does not collect telemetry.

The package does not intentionally collect, store, or transmit:

- personal information
- analytics events
- npm tokens
- GitHub tokens
- SSH keys
- API keys
- repository contents
- shell history

During normal installation, npm runs `scripts/postinstall.js`. That script only
uses the local Node.js runtime, the local Python interpreter, and pip. Its
network activity is limited to pip downloading the pinned Python package and its
dependencies from the user's configured Python package index.

The package does not run a separate telemetry endpoint, background service,
scheduled task, or analytics uploader.

Users who do not want npm lifecycle scripts to run can install with:

```bash
npm install -g nastech-agent --ignore-scripts
```

Then install the upstream Python runtime manually:

```bash
python -m pip install --upgrade nastech-agent==<npm package version>
```
