# 2026-07 Hermes update recovery case

## Symptoms

- `hermes update` started from a gateway session.
- Initial update stashed local changes, found new commits, then failed during reset/fetch with Git partial-clone network errors:
  - `RPC failed; curl 92 HTTP/2 stream ... CANCEL`
  - `fatal: early EOF`
  - `fatal: fetch-pack: invalid index-pack output`
  - `fatal: could not fetch ... from promisor remote`
- The working tree showed many deleted files and later import failure:
  - `ModuleNotFoundError: No module named 'hermes_cli.subcommands.postinstall'`
- A later update restored upstream but attempted to re-apply updater stashes, producing many rename/delete conflicts.
- `hermes --version` then printed: previous update was interrupted, finishing dependency installation, and hung while installing managed uv.

## Recovery that worked

From `~/.hermes/hermes-agent`:

```bash
# Clear the conflict state created by the updater's stash replay.
git restore --source=HEAD --staged --worktree .

# Seed managed uv from the existing system uv so Hermes does not hang on installer download.
mkdir -p ~/.hermes/bin
cp "$(command -v uv)" ~/.hermes/bin/uv
~/.hermes/bin/uv --version

# Verify Hermes can start.
hermes --version
```

If version output still showed branch metadata like `ahead 11, behind 1` after the updater had successfully fetched `origin/main`, this aligned the local branch ref:

```bash
git update-ref refs/heads/main origin/main
git restore --source=HEAD --staged --worktree .
```

Final verification showed:

```text
git status --short --branch
## main...origin/main

hermes --version
Hermes Agent v0.19.0 (2026.7.20) · upstream 4da7b9ee
```

## Gateway note

Running `hermes gateway restart` from inside the gateway session is blocked by design. Tell the user to run it from a separate terminal after disk update completes.
