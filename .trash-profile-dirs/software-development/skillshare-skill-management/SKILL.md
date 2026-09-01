---
name: skillshare-skill-management
description: Use when assembling or syncing agent skills with skillshare.
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [skills, skillshare, installation, synchronization, skill-management]
---

# Skillshare skill management

Use this skill when a user wants to install an agent skill through `skillshare`, assemble a skill from multiple pasted files, or synchronize shared skills into Hermes and other agent targets.

## Core model

- `~/.config/skillshare/skills/` is the skillshare source-of-truth directory.
- Each skill is a directory named after the skill and normally contains `SKILL.md`.
- Supporting material belongs inside the skill directory, commonly under `reference/` or `references/` as required by the skill's own layout.
- `skillshare sync` copies or links source skills into configured targets; it does not install a skill when no target is configured.
- Hermes' skillshare target may be `~/.hermes/skills/`, while a profile-specific Hermes runtime can have a separate profile path. Confirm the configured target before claiming installation.

## Workflow

1. Identify whether the user is providing a complete external skill or assembling one from multiple files.
2. For a multipart skill, preserve each part's requested relative path and write it under one source directory. Treat a file named `skills.md` as `SKILL.md` when its content has standard skill frontmatter and the user is clearly providing the main skill file.
3. Do not run synchronization until the user has finished sending the parts, unless they explicitly ask for incremental installation.
4. Initialize skillshare if needed:
   ```bash
   skillshare init
   ```
   The command may interactively copy existing skills into the source directory. Review its output rather than assuming the source is empty.
5. Add the intended target if `skillshare target list` shows no configured targets. For Hermes, use the actual target detected by `skillshare init`, usually:
   ```bash
   skillshare target add hermes ~/.hermes/skills
   ```
6. Synchronize:
   ```bash
   skillshare sync
   ```
7. Verify the result by checking the sync summary and reading the resulting `SKILL.md` plus important reference files from the target directory.

## Installation method

`skillshare` is a Go single-binary CLI, not the npm package named `skillshare`. Do not invent an npm installation command. Prefer the project's official installer, Homebrew, or a release binary. If the official installer needs `sudo` but the terminal cannot accept a password, install the matching release binary into `~/.local/bin` and verify `skillshare version`; report the user-level path clearly.

## Safety and reporting

- Inspect a remote install script before executing it, especially when it pipes downloaded content to a shell.
- Never claim a sync happened when the output says `0 targets` or when `skillshare sync` failed.
- Distinguish the skillshare source directory, target directory, and Hermes profile-specific directories in the final report.
- Report the actual version, target, and sync counts returned by the command.

## Cloud sync layer

The source directory can be backed by a git remote, making a Git repo the cloud source
of truth and the local directory a cache (`skillshare pull` pulls + syncs in one step;
`--track` installs enable `update --all`). A working local sync setup can still have the
cloud layer entirely unwired — no git remote on the source dir, all skills listed as
`local`, no scheduler for auto-pull. See `references/skillshare-cloud-sync.md` for the
model, the wiring recipe, and the three-point diagnosis.

## References

- See `references/skillshare-workflow.md` for the concrete multipart assembly and Hermes synchronization recipe learned from a real session.
- See `references/skillshare-cloud-sync.md` for the cloud source-of-truth setup (git remote, pull/push, --track) and diagnosing an unwired cloud layer.
