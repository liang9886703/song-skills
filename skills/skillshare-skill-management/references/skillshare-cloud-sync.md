# Skillshare cloud sync layer (git remote, pull, --track)

Skillshare's local source→target sync is only half the tool. The cloud layer makes a Git
repo the source of truth and the local `~/.config/skillshare/` a cache. This file covers
the cloud model and how to diagnose when it is unwired.

## The intended three-layer model

```
Git repo (GitHub/GitLab/any git host)   ← cloud source of truth
        │  skillshare pull / push
        ▼
~/.config/skillshare/skills/            ← local cache (a git repo with a remote)
        │  skillshare sync (symlink or copy)
        ▼
targets: ~/.hermes/skills, claude, cursor, codex, ... (60+)
```

Key commands (verified against v0.20.x):

- `skillshare pull` — pull from git remote AND sync to targets in one step.
- `skillshare push -m "msg"` — commit and push the source directory to the remote.
- `skillshare commit -m "msg"` — local checkpoint without pushing.
- `skillshare install github.com/owner/repo --track` — install tracked; tracked skills
  are updated in bulk by `skillshare update --all`.
- `skillshare update --all` — pull updates for every tracked/remote-installed skill.
  Skills shown as `local` in `skillshare list` are NOT touched by this.

## Diagnosing "cloud capability not wired"

A user can have skillshare fully working as a local symlink distributor while the entire
cloud chain is inert. Check three things:

1. `cd ~/.config/skillshare && git remote -v` — if "not a git repository" or no remote,
   `pull`/`push` have nothing to talk to. The source dir must be a git repo with a
   remote (typically a private GitHub repo).
2. `skillshare list` — skills marked `local` were never installed from a remote;
   `update --all` is a no-op for them. Reinstall from their upstream GitHub source
   with `--track` to make them updatable.
3. No scheduler — skillshare has no built-in daemon. "Auto pull" must come from a cron
   job running `skillshare pull && skillshare update --all`.

## Wiring it up from scratch

```bash
cd ~/.config/skillshare
git init && git add -A && git commit -m "init skills"
git remote add origin git@github.com:<user>/<private-skills-repo>.git
git push -u origin main
# then on any machine: skillshare pull  (pulls + syncs to all targets)
```

Creating the GitHub repo is a side effect on the user's account — confirm with the user
(or use `gh repo create` only after explicit approval) before doing this autonomously.

## Notes

- There is no `skillshare remote` or `skillshare repo` subcommand; remote management is
  plain git inside the source directory. The git-related subcommands are `commit`,
  `push`, `pull` (listed under "GIT REMOTE" in `skillshare --help`).
- `skillshare hub <subcommand>` is a separate feature (hub management) — do not confuse
  it with the git remote flow.
