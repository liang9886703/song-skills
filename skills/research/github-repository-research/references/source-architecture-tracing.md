# Source architecture tracing for GitHub repos

Use this reference when a user asks to pull a GitHub repo and explain its implementation principle / architecture, especially for agent frameworks, CLIs, SDKs, or tool-heavy systems.

## Goal

Produce a source-grounded explanation, not a README paraphrase. Connect the advertised capabilities to actual files, call paths, registries, and runtime loops.

## Efficient tracing sequence

1. **Clone/update and capture immutable metadata**
   - Local path, branch, short commit, latest commit subject.
   - Verify clean status before reporting.
2. **Read product positioning first**
   - README, root `package.json`/manifest, package manifests in monorepos.
   - Extract the project's own claim, but do not stop there.
3. **Find entry points**
   - CLI binaries, SDK exports, server startup, app bootstrap, package `bin`/`exports`/scripts.
   - For TypeScript monorepos, inspect the package that matches the product name plus any lower-level core package.
4. **Trace construction/wiring**
   - How config/auth/settings/session are built.
   - Where tools/plugins/providers are registered.
   - Where the main object/session/loop is instantiated.
5. **Trace the core loop**
   - For agent repos: model call → streaming → tool call extraction → tool execution → append tool results → repeat/stop.
   - Capture loop file/function names and the reason continuation stops.
6. **Map advertised differentiators to source**
   - Editing: patch format, resolver, preflight, commit, diff rendering, no-op guards.
   - LSP/IDE: read-only ops, write ops, writethrough/format/diagnostics/saved notifications.
   - Runtime/eval: persistent kernels, language backends, bridge back into tools.
   - Browser/shell/MCP/custom tools: registry and settings gates.
   - Subagents: task tool, agent definitions, recursion/budget/lifecycle, output/yield schema.
7. **Synthesize around mechanisms**
   - Explain "why it can do X" as a chain from user/model intent to concrete runtime path.
   - Prefer diagrams and file-backed bullets over long file-by-file narration.

## Reporting template

- Repo metadata: path, branch, commit, clean/dirty status.
- One-sentence architecture summary.
- Layered architecture: entrypoint, session/SDK, core loop, tools, feature-specific subsystems.
- Capability chains: e.g. "precise edits" = edit tool → patch parser → resolver → LSP writethrough → diagnostics.
- Noteworthy engineering choices and pitfalls.
- If no build/tests were run, say so; for read-only architecture reviews, source inspection can be sufficient.

## Pitfalls

- Do not claim a feature works only from README marketing; tie it to source paths.
- Do not over-index on file counts/LOC when the user asked for principles.
- Do not stop after cloning; trace at least entrypoint, core loop, and one advertised differentiator.
- For tool-call agents, inspect the registry and the loop separately: registry shows available powers, loop shows how powers are exercised.
- Preserve exact source paths in the final answer so future follow-up work can jump directly into code.
