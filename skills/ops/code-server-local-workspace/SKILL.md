---
name: code-server-local-workspace
description: Use when serving a local project through native code-server.
---

# Native code-server for a local workspace

Use this skill when the user wants a local directory opened in code-server for browser-based code reading or development, especially on a personal workstation where Docker isolation is unnecessary.

## Default approach

1. Treat the requested path as a user-level precondition. Verify it exists before installing or starting anything.
2. Inspect the target project's manifest and source extensions before choosing plugins. Do not install Go/Python/Vue/React tooling merely because it is generally available.
3. If the user identifies a related project that will be merged later, inspect that project too and union the future stack requirements. A future Vue 3 migration means prioritize Vue tooling and do not add React-specific extensions just because the current intermediate project is React.
4. Prefer a native installation on a personal machine when the user explicitly says there is no security/isolation requirement. Docker is optional, not a prerequisite; it adds image/runtime overhead and complicates local paths.
5. Install code-server through the platform package manager where available. Check the installed version and capture package-manager warnings without treating them as a blocker unless they prevent execution.
6. Install a small, project-relevant extension set. TypeScript/JavaScript language support is usually built in; add Vue language support for Vue 3, plus ESLint, Prettier, and Tailwind CSS only when the project uses or is moving toward them.
7. Start with an explicit bind address and port. For a private local-only service, use `127.0.0.1:<port>`; only use `0.0.0.0` when the user actually needs LAN access.
8. Open the requested project directory as the workspace and disable update checks if lightweight, quiet startup is preferred. Do not use `--disable-extensions` after installing extensions because it disables the very tooling the user requested. The resulting `/?folder=/absolute/path/to/project` URL is normal: the query value is the real filesystem path, not a display-name alias. Bookmarking the root URL is fine, but do not promise that the folder query can be shortened to only the project name.
9. Verify both process output and the HTTP listener. A `302` redirect to `/login` is a successful unauthenticated code-server response, not a failure.

## Typical native macOS flow

```bash
brew install code-server
code-server --install-extension Vue.volar
code-server --install-extension dbaeumer.vscode-eslint
code-server --install-extension esbenp.prettier-vscode
code-server --install-extension bradlc.vscode-tailwindcss
code-server --bind-addr 127.0.0.1:8099 --disable-update-check \
  /absolute/path/to/project
```

Use `code-server --list-extensions` to verify installation. The generated password is normally in `~/.config/code-server/config.yaml`; do not print the secret into chat. code-server has built-in password authentication via `auth: password`; if the user explicitly chooses a password, update the config and restart the running process because the config is read at startup. Verify the restarted endpoint afterward.

## Resource discipline

There is no reliable code-server flag that makes the entire service consume an arbitrary fixed amount of RAM. Reduce footprint by avoiding unrelated extensions, opening a focused directory rather than a home/monorepo parent, and not starting language servers for unused stacks. A Node heap limit only limits V8 heap, not total code-server memory, and should not be presented as a complete memory cap.

## Security and access boundary

For a personal local-only use case, do not over-engineer a Docker or reverse-proxy deployment. Keep the default password authentication unless the access boundary is otherwise protected. Never expose code-server directly to an untrusted network without authentication and encryption; if the user explicitly says local-only, bind to loopback and report that choice.

## Pitfalls

- Do not silently substitute `Documents` for `Document` or vice versa; check the exact requested path and report which one was used.
- Do not infer project plugins from a generic wish list. Read `package.json`, framework files, and source extensions first.
- Do not install React tooling when the user says the project will migrate to Vue 3; install the Vue 3 toolchain instead.
- Do not leave `--disable-extensions` in the final startup command after installing language extensions.
- Do not claim the service is ready based only on a spawned process. Confirm the port and HTTP response.
- Homebrew may warn that a code-server formula is deprecated because of an upstream packaging issue; report it, but separate that warning from whether the current installation and service actually work.

## Reference

See `references/native-macos-setup.md` for the concrete verified setup pattern and extension rationale from a local macOS workspace session.
