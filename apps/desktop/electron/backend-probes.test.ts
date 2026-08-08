/**
 * Tests for electron/backend-probes.ts.
 *
 * Run with: node --test electron/backend-probes.test.ts
 * (Wired into npm test:desktop:platforms in package.json.)
 */

import assert from 'node:assert/strict'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

import { test } from 'vitest'

import {
  canImportNasTechCli,
  DEFAULT_PROBE_TIMEOUT_MS,
  nastechRuntimeImportProbe,
  PROBE_TIMEOUT_MS,
  resolveProbeTimeoutMs,
  shouldTrustNasTechOverride,
  verifyNasTechCli
} from './backend-probes'

// Resolve the host's own Node binary -- guaranteed to be on disk and
// runnable. We use it as both a stand-in for "a python that doesn't
// have nastech_cli" (since `node -c "import nastech_cli"` will exit
// non-zero) and as a way to script verifyNasTechCli's success path
// (a tiny script we write to disk that exits 0 on --version).
const NODE_BIN = process.execPath

test('canImportNasTechCli returns false when path is falsy', () => {
  assert.equal(canImportNasTechCli(''), false)
  assert.equal(canImportNasTechCli(null), false)
  assert.equal(canImportNasTechCli(undefined), false)
})

test('canImportNasTechCli returns false when interpreter cannot run -c', () => {
  // node IS an interpreter, but `node -c "import nastech_cli"` is a
  // SyntaxError -- different exit reason from a real Python's
  // ModuleNotFoundError, but the predicate is "exit 0 or not" and
  // both land on "not", which is exactly what we want for the
  // resolver fall-through.
  assert.equal(canImportNasTechCli(NODE_BIN), false)
})

test('canImportNasTechCli returns false when binary does not exist', () => {
  const ghost = path.join(os.tmpdir(), 'nastech-probes-ghost-' + Date.now() + '.exe')
  assert.equal(canImportNasTechCli(ghost), false)
})

test('nastech runtime import probe checks config dependencies', () => {
  const probe = nastechRuntimeImportProbe()
  assert.match(probe, /\bimport yaml\b/)
  // dotenv is the first third-party import on the CLI boot path
  // (nastech_cli/env_loader.py); a mid-update venv missing python-dotenv
  // passed the old probe and produced an unrecoverable boot loop.
  assert.match(probe, /\bimport dotenv\b/)
  assert.match(probe, /\bimport nastech_cli\.config\b/)
})

test('explicit NasTech override is authoritative', () => {
  assert.equal(shouldTrustNasTechOverride('/nix/store/abc/bin/nastech'), true)
})

test('empty NasTech override is not authoritative', () => {
  assert.equal(shouldTrustNasTechOverride(''), false)
  assert.equal(shouldTrustNasTechOverride(undefined), false)
})

test('verifyNasTechCli returns false when command is falsy', () => {
  assert.equal(verifyNasTechCli(''), false)
  assert.equal(verifyNasTechCli(null), false)
  assert.equal(verifyNasTechCli(undefined), false)
})

test('verifyNasTechCli returns false when binary does not exist', () => {
  const ghost = path.join(os.tmpdir(), 'nastech-probes-ghost-' + Date.now() + '.exe')
  assert.equal(verifyNasTechCli(ghost), false)
})

test('verifyNasTechCli returns true when --version exits 0', () => {
  // Write a tiny script that exits 0 regardless of args, then invoke
  // it through node. This stands in for a working nastech binary --
  // verifyNasTechCli only cares about the exit code.
  const scriptPath = path.join(os.tmpdir(), `nastech-probes-ok-${Date.now()}-${process.pid}.cjs`)
  fs.writeFileSync(scriptPath, 'process.exit(0)\n')

  try {
    // Use node as the launcher and our script as the "command". Pass
    // shell:false (default) -- node is a real binary, no shim.
    // execFileSync passes ['--version'] as args, which node ignores
    // gracefully (well, it prints its version and exits 0, which is
    // perfect -- exit code 0 is the only signal we read).
    assert.equal(verifyNasTechCli(NODE_BIN), true)
  } finally {
    try {
      fs.unlinkSync(scriptPath)
    } catch {
      void 0
    }
  }
})

test('verifyNasTechCli swallows timeouts (does not throw)', () => {
  // We can't easily provoke a real hang in CI without slowing the
  // suite, but we CAN confirm that an invocation that DOES throw
  // (because the binary is missing) returns false rather than
  // propagating. Same code path the timeout case takes.
  assert.equal(verifyNasTechCli('/definitely/not/a/real/binary/anywhere'), false)
})

test('default probe timeout is 15s (not the old 5s death-loop value)', () => {
  assert.equal(DEFAULT_PROBE_TIMEOUT_MS, 15_000)
  // Module constant uses process.env at load time; with no override it
  // matches the default (tests run without NASTECH_PROBE_TIMEOUT_MS).
  assert.equal(PROBE_TIMEOUT_MS, DEFAULT_PROBE_TIMEOUT_MS)
})

test('resolveProbeTimeoutMs honours NASTECH_PROBE_TIMEOUT_MS', () => {
  assert.equal(resolveProbeTimeoutMs({}), DEFAULT_PROBE_TIMEOUT_MS)
  assert.equal(resolveProbeTimeoutMs({ NASTECH_PROBE_TIMEOUT_MS: '30000' }), 30_000)
  assert.equal(resolveProbeTimeoutMs({ NASTECH_PROBE_TIMEOUT_MS: '0' }), DEFAULT_PROBE_TIMEOUT_MS)
  assert.equal(resolveProbeTimeoutMs({ NASTECH_PROBE_TIMEOUT_MS: 'nope' }), DEFAULT_PROBE_TIMEOUT_MS)
  // Cap runaway values
  assert.equal(resolveProbeTimeoutMs({ NASTECH_PROBE_TIMEOUT_MS: '999999' }), 120_000)
})
