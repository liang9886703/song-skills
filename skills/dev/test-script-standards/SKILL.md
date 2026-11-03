---
name: test-script-standards
description: Write, refactor, review, or diagnose sh/bash scripts using repeatable environment setup, unified task output, fail-fast control flow, persistent evidence, safe process cleanup, and explicit script headers. Use for Shell script creation or standards work, especially test, recovery, E2E, harness, service startup/shutdown, HTTP workflow, and long-running process scripts; also use for requests involving set -eu, pipefail, trap and PID cleanup, output or log layout, quoting, secret handling, idempotency, sh -n, or bash -n.
---

# Test Script Standards

## Required reference

Before creating, changing, or reviewing a Shell script, read
[references/shell-script-standards.md](references/shell-script-standards.md) completely.
Treat rules marked **必须** as hard requirements. Apply **推荐** rules unless the repository
or runtime has a concrete conflicting constraint.

## Workflow

### 1. Establish the script contract

1. Read repository instructions and neighboring scripts.
2. Identify the intended interpreter: POSIX `sh` or Bash.
3. Identify inputs, stable configuration, environment-specific configuration, secrets,
   outputs, child processes, external services, and cleanup ownership.
4. Define observable success and failure conditions before editing.
5. Preserve existing runtime behavior unless the user requested a behavior change.

### 2. Design the structure

Organize the script in this order:

1. Header with Usage, Principle, Main flow, and Output files
2. Strict mode
3. Static configuration
4. Output paths
5. Small common helpers
6. Argument parsing and validation
7. Initialization and cleanup
8. Step functions
9. `main`
10. `main "$@"`

Keep execution out of global scope. A dispatcher script should only parse options, select
subtasks, call child scripts, and summarize results.

### 3. Implement the required behavior

- Default to `set -eu`. Add `set -o pipefail` only for Bash or a confirmed compatible shell.
- Quote variable expansions and paths. Do not use `eval` for external input.
- Keep stable configuration near the top; use environment variables only for real environment
  differences, CI overrides, or secrets.
- Validate configuration and destructive targets before starting a process or deleting output.
- Initialize a single task-level output root and keep all child artifacts underneath it.
- Capture multiline results in a variable or file before parsing; avoid long opaque pipelines.
- Persist main logs, child-process logs, requests, responses, important intermediate results,
  and failure snapshots.
- Stop on the first unexpected error. Limit any `set +e` or `|| true` to a documented,
  narrow cleanup or expected-failure check.
- Record child PIDs and install `trap` cleanup. Preserve the original exit status and clean in
  reverse startup order.
- Use bounded readiness probes instead of fixed long sleeps.
- Redact secrets from commands, logs, snapshots, and child environments that do not need them.

### 4. Validate proportionally

1. Run `sh -n <script>` for POSIX scripts or `bash -n <script>` for Bash scripts.
2. Run the repository's formatter or lint command. Use `shellcheck` and `shfmt -d` when
   available and appropriate.
3. Run the smallest test or dry-run that proves the changed behavior.
4. For initialization or cleanup changes, run twice when practical to prove repeatability.
5. Confirm that failed runs preserve evidence and do not leak processes, ports, sockets,
   temporary configuration, or secrets.

Do not weaken assertions or skip real failures merely to make the script pass.

### 5. Report the outcome

State:

- scripts changed or reviewed;
- behavior and structure added;
- validation commands and results;
- output or failure-evidence locations;
- remaining blockers, including whether they are script defects or external-system failures.

## Review-only tasks

When asked only to review or diagnose:

- do not edit the script;
- classify findings by impact;
- cite the exact file and line;
- distinguish formatting problems from behavioral or safety defects;
- state which checks were executed and which conclusions are static analysis only.

## Prohibited shortcuts

- Do not scatter one task's outputs across unrelated directories.
- Do not put service starts, requests, or test steps in global scope.
- Do not silently ignore unexpected failures.
- Do not use broad process-name kills when owned PIDs are available.
- Do not recursively delete an empty, root, home, repository-root, or unvalidated path.
- Do not print or persist credentials.
- Do not claim an E2E scenario passed when only request acceptance or a mocked failure path ran.
