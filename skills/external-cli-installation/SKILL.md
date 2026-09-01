---
name: external-cli-installation
description: "Use when installing external CLIs or skill managers."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [cli, installation, npm, homebrew, github-releases, skill-managers, macos, verification]
---

# External CLI Installation

Use this skill when a user asks to install a third-party CLI, agent skill manager, or repository-provided command-line tool.

The goal is a working, verifiable installation—not merely an attempted command. Prefer the upstream-supported distribution method over a guessed package-manager command.

## Workflow

1. **Identify the source and requested scope**
   - Resolve the exact repository, package name, or release URL.
   - Distinguish between installing the CLI itself and installing resources managed by that CLI.
   - Clarify the target scope only when it changes the action: system-wide `/usr/local/bin`, user-level `~/.local/bin`, or a tool-specific source directory.

2. **Inspect the distribution method before installing**
   - Check the repository README and root metadata for `package.json`, `go.mod`, release archives, Homebrew instructions, or installer scripts.
   - Do not infer that a GitHub repository is npm-installable.
   - Run an npm registry/package lookup only when npm is actually indicated. A missing npm package is evidence to switch methods, not to invent a package name.
   - For remote shell installers, fetch and inspect the script before execution.

3. **Choose the least surprising supported method**
   - Prefer, in order: package manager explicitly documented upstream, versioned release binary, then a reviewed installer script.
   - If the project is a standalone binary (for example, a Go release), use its release archive or Homebrew rather than `npm install`.
   - Avoid piping unreviewed remote content to a shell. If the user explicitly approves the reviewed upstream script, it may be used subject to runtime approval controls.

4. **Handle privilege and non-interactive environments**
   - Try the requested system-wide install only when the user has authorized it.
   - If `sudo` needs an interactive password and the current execution channel cannot provide one, do not fabricate success and do not repeatedly retry the same command.
   - Fall back to a user-level executable directory such as `~/.local/bin` when it preserves the requested functionality and does not require admin access. Create the directory, install the binary with executable permissions, and report the exact path.
   - Do not confuse a user-level binary install with the tool's own configuration/source directory.

5. **Verify the artifact**
   - Run the installed binary's version/help command.
   - Resolve it with `command -v` or an absolute path.
   - If the directory is not on `PATH`, report that explicitly and give the minimal shell configuration needed; do not claim the command is globally available when only the absolute path works.
   - For skill managers, verify the CLI first; initialize or sync its skill store only if the user also requested that step.

## Important distinctions

- **Package manager scope**: npm installs JavaScript packages; Homebrew may install standalone binaries; a GitHub release may provide a compiled executable.
- **Binary scope**: where the command is installed (`/usr/local/bin`, `~/.local/bin`).
- **Skill-store scope**: where the manager keeps its source skills (for example, a tool-specific config directory).
- **Agent runtime scope**: where Hermes or another agent loads skills. These are separate locations and should be named explicitly in the result.

## Common pitfalls

- Saying a repository supports npm merely because the user asks for npm.
- Treating a 404 from `npm view` as a transient error when the project documents a non-npm distribution model.
- Running a `curl | sh` installer without inspecting it first.
- Retrying a sudo command after a non-interactive password failure without changing the installation strategy.
- Reporting “global” without stating whether that means system-wide binary, user-level binary, skill manager source, or agent runtime skills.
- Initializing a skill manager when the user asked only to install its executable.

## Reusable verification pattern

For a versioned macOS release binary:

```bash
set -e
version=<version>
os=darwin
arch=arm64
bin_dir="$HOME/.local/bin"
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT
mkdir -p "$bin_dir"
curl -fsSL "https://github.com/<owner>/<repo>/releases/download/v${version}/<binary>_${version}_${os}_${arch}.tar.gz" -o "$tmp_dir/tool.tar.gz"
tar -xzf "$tmp_dir/tool.tar.gz" -C "$tmp_dir"
install -m 755 "$tmp_dir/<binary>" "$bin_dir/<binary>"
"$bin_dir/<binary>" version
command -v <binary> || true
```

## Session-specific reference

For the verified `runkids/skillshare` installation path, release naming, and the sudo fallback, see `references/skillshare-install.md`.
