---
name: repo-evolution-audit
description: Trace code paths, data flow, JSON or event formats, and recent git evolution for a feature or protocol. Use when the user wants repository archaeology, compatibility assessment, file mapping, format summaries, or a concise breakdown of logic changes vs field changes.
---

# Repo Evolution Audit

## Overview

Use this skill when the user wants to understand how a feature works today, which files own it, how data moves through the code, what the current input or output format looks like, and how that contract changed over time.

Default to a compatibility-review mindset: separate logic changes from schema or protocol changes, call out real structure changes, and avoid drowning the user in per-commit detail unless they ask.

## Workflow

1. Narrow the scope first.
Ask: what exact surface is under review?
- Event stream or protocol output
- Persisted JSON import or export
- CLI rendering vs transport layer
- Local file format vs network or share API

If the user's wording is ambiguous, infer the narrowest useful scope from context and state it.

2. Map the current code path before reading history.
Find:
- Format definition files
- Producer files
- Transport or persistence files
- Consumer or renderer files

Summarize the flow as:
`producer -> storage/bus -> transport -> consumer`
or
`DB -> serializer -> JSON`

3. Describe the current format in plain language.
Distinguish clearly between:
- Event wrapper format
- Event payload shape
- Persisted JSON shape
- CLI display format

If multiple layers exist, do not collapse them into one.

4. Inspect git history only for the files that actually own the contract.
Prefer the smallest file set that explains the format:
- Producer
- Schema or type definition
- Serializer or importer/exporter

Use history to answer:
- How active is this area
- Which changes were logic-only
- Which changes added fields
- Which changes changed or removed fields
- Which changes altered nesting or event boundaries

5. Classify changes by compatibility impact.
Use these buckets:
- Logic changes: timing, retries, ordering, compaction, status handling, persistence path, error recovery
- Added fields or added event types: usually backward compatible
- Changed or removed fields: key rename, semantics change, removal, requiredness change
- Structure changes: nesting changes, flat-to-nested or nested-to-flat changes, one event split into two, two events merged into one
- Other useful changes: auth, performance, tests, tooling, docs drift

6. Answer at the right granularity.
If the user asks for a summary, prefer grouped conclusions and tables.
If the user asks for every commit, list commits but still annotate which ones actually matter.

## Review Rules

- Keep “current behavior” and “historical changes” separate.
- Keep “local JSON contract” and “network/share contract” separate.
- Keep “event transport” and “terminal/UI rendering” separate.
- Treat added optional fields as lower risk than changed structure.
- Do not overstate churn. If many commits are unrelated list, test, refactor, or formatting changes, say so.
- If a field existed briefly and was reverted, mention it as an experiment, not as a stable migration.
- If there is no meaningful rename or deletion, say that explicitly.

## Output Pattern

Start with a short scope line in prose. Then use one or more tables like these.

### Summary table

| Category | Count | Main changes | Compatibility impact | Notes |
|---|---:|---|---|---|
| Logic changes | 0 | ... | ... | ... |
| Added fields or events | 0 | ... | ... | ... |
| Changed or removed fields | 0 | ... | ... | ... |
| Structure changes | 0 | ... | ... | ... |
| Other | 0 | ... | ... | ... |

### Field-focused table

| Area | Added fields | Changed fields | Removed fields | Structure changes | Notes |
|---|---|---|---|---|---|
| Event payload | ... | ... | ... | ... | ... |
| Session JSON | ... | ... | ... | ... | ... |
| Message or part JSON | ... | ... | ... | ... | ... |

### Stability table

| Surface | Stability | Why |
|---|---|---|
| Event wrapper | High | ... |
| Event payload | Medium | ... |
| Local export JSON | High | ... |
| Share import API | Low | ... |

## What Good Answers Should Emphasize

- Which files are the true sources of the format
- Whether the shape is mostly stable with additive growth
- Whether any old keys were actually renamed or removed
- Whether any nesting changed in a way that can break consumers
- Whether recent git activity is real protocol churn or mostly implementation churn

## Useful Phrasing

Use direct conclusions like:
- “The outer shape stayed stable; most changes were additive.”
- “The main compatibility risk is event splitting, not field rename.”
- “Local export JSON stayed stable; churn is mostly in share import.”
- “Recent commits are active, but most are logic or infra rather than schema changes.”

## Tooling Hints

- Prefer `rg` to find ownership quickly.
- Use `git log -- <file>` to count and bound history.
- Use `git show <commit> -- <file>` to verify whether a commit changed logic, fields, or structure.
- When multiple files are involved, inspect them in parallel.
