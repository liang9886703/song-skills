# Native macOS setup reference

## Verified pattern

- Host: macOS arm64 with Homebrew.
- Install: `brew install code-server`.
- Workspace path must be checked exactly; `Document` and `Documents` are different paths.
- Start private local service with:

```bash
code-server \
  --bind-addr 127.0.0.1:8099 \
  --disable-update-check \
  /absolute/path/to/workspace
```

- Verify with `lsof -nP -iTCP:8099 -sTCP:LISTEN` and `curl -I http://127.0.0.1:8099/`.
- Expected unauthenticated response: `HTTP/1.1 302 Found` with `Location: ./login`.

## Extension selection for a Vue 3 migration

For a current React/TypeScript intermediate project that will be merged into a Vue 3 project, install the future stack rather than React-specific tooling:

- `Vue.volar` — Vue 3 language service.
- `dbaeumer.vscode-eslint` — ESLint.
- `esbenp.prettier-vscode` — formatting.
- `bradlc.vscode-tailwindcss` — Tailwind CSS IntelliSense when Tailwind is present or planned.
- TypeScript/JavaScript language support is built in.

Do not combine `--disable-extensions` with the final command after installing these extensions. code-server uses Open VSX rather than Microsoft's Marketplace, so extension availability can differ; verify with `code-server --list-extensions` and handle VSIX installation only if needed.

## Native versus Docker decision

When the user is the sole local user and explicitly says there is no security/isolation requirement, native code-server is the simpler choice. Docker remains useful for reproducible deployment, filesystem isolation, or hard container memory limits, but it is not required just to expose a local directory. Use loopback binding for local-only access; use `0.0.0.0` only when LAN access is intentional.
