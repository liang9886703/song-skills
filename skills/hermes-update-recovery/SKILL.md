---
name: hermes-update-recovery
description: Recover and verify git-installed Hermes Agent updates, especially when `hermes update` is interrupted, leaves local stashes/conflicts, or the CLI cannot start after a partial pull.
---

# Hermes Update Recovery

Use this skill when the user asks to update Hermes Agent and the install is a git checkout under `~/.hermes/hermes-agent`, or when an update leaves Hermes partially updated, conflicted, or unable to import modules.

## Goals

- Leave the Hermes source tree matching upstream `origin/main` unless the user explicitly asked to preserve local source edits.
- Preserve user profile/config/secrets under `~/.hermes/` and profile directories; do not print secrets.
- Verify with `hermes --version` and `git status` before reporting success.

## Standard update workflow

1. Load the Hermes guidance/docs if needed, then run:
   ```bash
   hermes --version
   hermes update
   hermes --version
   ```
2. If running from inside a gateway session, expect gateway restart to be blocked. Do not treat that as update failure; either tell the user to run `hermes gateway restart` from a separate shell, or schedule a one-shot external launchd restart when the user says to continue:
   ```bash
   mkdir -p ~/.hermes/logs
   launchctl remove ai.hermes.deferred-gateway-restart 2>/dev/null || true
   launchctl submit -l ai.hermes.deferred-gateway-restart -- /bin/bash -lc 'sleep 3; ~/.hermes/hermes-agent/venv/bin/hermes gateway start > ~/.hermes/logs/restart-after-update.log 2>&1'
   sleep 5
   hermes gateway status
   tail -80 ~/.hermes/logs/restart-after-update.log 2>/dev/null || true
   ```
   This avoids killing the child command from inside the running gateway while still refreshing launchd service definitions.
3. Verify:
   ```bash
   git -C ~/.hermes/hermes-agent status --short --branch
   hermes status --all
   ```

## Interrupted update recovery

A detailed worked case is in `references/interrupted-update-2026-07.md`.

If `hermes update` fails mid-pull/reset and the CLI later errors with missing modules or a dirty tree:

1. Inspect first:
   ```bash
   cd ~/.hermes/hermes-agent
   git status --short --branch
   git stash list -5
   hermes --version || true
   ```
2. If the tree is in merge/stash-conflict state but the intent is a normal update, discard the updater-created conflict state and keep upstream files:
   ```bash
   git restore --source=HEAD --staged --worktree .
   ```
3. If `hermes --version` says a previous update was interrupted and hangs installing managed `uv`, but a working `uv` exists elsewhere, seed Hermes' managed uv path:
   ```bash
   mkdir -p ~/.hermes/bin
   cp "$(command -v uv)" ~/.hermes/bin/uv
   ~/.hermes/bin/uv --version
   ```
   Then rerun `hermes --version`.
4. If the local branch metadata is ahead/behind because the updater reset succeeded but the local ref did not align, and `origin/main` is already fetched, align the ref without fetching again:
   ```bash
   git update-ref refs/heads/main origin/main
   git restore --source=HEAD --staged --worktree .
   ```
5. Re-verify:
   ```bash
   git status --short --branch
   hermes --version
   ```

## Network/pull pitfalls

- Git partial clone fetches can fail with HTTP/2 `stream was not closed cleanly: CANCEL` or promisor-remote early EOF. Retry with HTTP/1.1 before changing strategy:
  ```bash
  git config http.version HTTP/1.1
  git fetch --filter=blob:none origin main
  ```
- Do not repeatedly retry identical large downloads after timeouts. Change strategy: resume only if the server supports ranges, use git fetch with adjusted HTTP settings, or recover from already-fetched `origin/main`.

## Safety notes

- Do not apply updater-created stashes blindly. They may represent artificial delete/rename conflicts from a failed reset, not meaningful user edits.
- If the user has real local source edits they want preserved, stop and ask before discarding conflicts.
- Never print API keys from `.env`, `auth.json`, or status output beyond already-redacted command output.
