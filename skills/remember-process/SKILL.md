---
name: remember:process
description: Process unprocessed Claude Code sessions into your Second Brain
---

# /remember:process — Process Sessions into Second Brain

Reads unprocessed Claude Code transcripts and routes valuable content into your Second Brain using a knowledge-aware pipeline.

Only use Bash for running Node.js scripts. Use Read/Write/Edit/Glob/Grep for all file operations.

---

## Core Principles

1. **Chronology:** `session_date < file_last_modified` → OLD SESSION (append only, no replace, no frontmatter update). Otherwise → normal update.
2. **Knowledge Index:** Built in Step 1. Use throughout to resolve entities, link with `[[wikilinks]]`, prevent duplicates.
3. **REMEMBER.md overrides:** User instructions take precedence over default routing.

---

## Step 1: Build Knowledge Index

1. Read `$REMEMBER_BRAIN_PATH` env var (fallback `~/remember`). Call this `{brain}`.
2. If missing → tell user to run `/remember:init` and stop.
3. Run: `node ${CLAUDE_PLUGIN_ROOT}/scripts/build-index.js`
4. Read output — this is your map of everything that exists.

## Step 1b: Load User Instructions

Read REMEMBER.md (cascading): `{brain}/REMEMBER.md` (global) + `{project_root}/REMEMBER.md` (project, if exists). These override default routing, capture rules, templates, and custom types.

## Step 1c: Batch Chronology Map

Run once to get last-modified dates for all brain files:
```bash
cd {brain} && git log --format="%ai" --name-only --diff-filter=ACMR HEAD | paste - - | sort -k2 -u
```

Parse into a lookup map: `file_path → last_modified_date`. Use this in Step 4c instead of per-file git log calls.

## Step 2: Find Unprocessed Sessions

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/extract.js --unprocessed
```

Optional filters: `--project <name>`, `--source openclaw|claude-code`.

Show the list. Ask user which to process: **All**, **specific sessions by number**, or **Skip**.

## Step 3: Extract Each Session

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/extract.js <file_path>
```

Use the `**Session date (use for journal/tasks):**` line as SESSION_DATE for everything. Never use today's date.

## Step 4: Process Each Session

Read `@reference.md` for routing tables, templates, and classification rules.

### 4a. Build Resolution Map

Resolve every name, project, topic against the knowledge index. Fuzzy match: "John", "john smith", "John S." → `People/john-smith.md`.

### 4b. Classify Content

Apply REMEMBER.md rules first (Always/Never/Routing overrides/Custom Types), then fall through to default classification in `reference.md`. Skip: routine code generation, debugging noise, tool call chatter.

### 4c. Update Existing Files (Edit Tool)

Use `Edit` for surgical updates. Do NOT rewrite whole files.

**Chronology check:** Look up the file in the batch chronology map (Step 1c).
- `session_date < file_last_modified` → **OLD SESSION:** append only, insert chronologically in logs, don't replace sections, don't update frontmatter
- Otherwise → **NEW SESSION:** normal Edit, update frontmatter `updated:` field

See `reference.md` for per-type update patterns and chronology examples.

**When in doubt:** Append. Duplicate context is better than lost information.

### 4d. Create New Files (Write Tool)

Check REMEMBER.md `## Templates` first, then fall back to `reference.md` templates. Use `[[wikilinks]]` everywhere.

### 4e. Update Persona.md

Analyze session for: user corrections, stated preferences, repeated workflows, communication style, decision criteria, code style. Read current Persona.md first. Add evidence with `[{SESSION_DATE}]` prefix. Skip if no clear patterns.

## Step 5: Maintain Derived Index Files

After writing brain content, also maintain lightweight derived files so the brain remains readable even when the semantic index is stale.

### 5a. Update `knowledge-index.md`

Refresh `{brain}/knowledge-index.md` so it stays aligned with the current brain state.
At minimum, keep these sections current:
- `## Identity`
- `## Projects`
- `## Notes`
- `## Tasks`
- `## Recent Journal`
- `## Recent Changes`

Requirements:
- Include newly created or newly relevant project/note files.
- Advance the frontmatter `updated:` date.
- Keep the file concise; this is a human-readable map, not a full dump.

### 5b. Maintain project-level routing/index files when touched

If a processed session adds or changes important structure for an existing project file (for example a project gains new routing rules, write contracts, memory-layer definitions, or key implementation status), update that project file in the same run instead of only writing the daily journal.

Example:
- Knowledge-base design changes affecting `Projects/knowledge-base-setup/knowledge-base-setup.md` should update that file directly.
- General OpenClaw project progress should continue to update `Projects/openclaw/openclaw.md`.

## Step 6: Mark Processed, Snapshot, and Report

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/extract.js --source <source> --mark-processed <session_id>
```

After all content updates and processed-marking are done, create a daily git snapshot for the entire brain:

1. `cd {brain}`
2. `git add -A`
3. `git commit -m "YYYY-MM-DD"`

Rules:
- Run this after all other remember-processing rules are complete.
- Use the current run date in `Asia/Shanghai` as the commit message, formatted exactly as `YYYY-MM-DD`.
- If there are no staged changes, do not fail the workflow; just note that no daily snapshot commit was needed.
- This snapshot is for the whole brain state after processing, not per-file commits.

Report: list created files, updated files (note if append-only), skipped files, session dates, remaining unprocessed count. Also mention whether the daily git snapshot commit was created or skipped. See `reference.md` for report template.

## Error Handling

- Script fails → show error, skip session, continue
- File write fails → warn, continue
- No unprocessed → tell user, suggest "remember this:"
- web_fetch fails → minimal resource note, flag for review
