# Bundled plugins

Drop a `<name>/plugin.{ts,tsx}` here that default-exports a `NastechPlugin` and
it registers automatically at boot (vite glob in `../contrib/plugins.ts`), with
the same inventory + live enable/disable contract as runtime plugins.

None ship in-tree today — reference/demo plugins (the counter example, the
gateway-pill 1:1 rebuild, the runtime-loader hello world) live in the companion
[`nastech-example-plugins`](https://github.com/nastechai/nastech-example-plugins)
repo so the shipped app stays uncluttered.

User- and agent-authored plugins load at runtime from
`$NASTECH_HOME/desktop-plugins/<name>/plugin.js` (the disk door) — see the
`nastech-desktop-plugins` skill.
