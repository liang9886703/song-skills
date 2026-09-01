# Codex skill install fallback for large repositories

Use this only after the normal installer command is blocked by repeated hangs/timeouts on a large repository.

## Situation

The user provides commands like:

```bash
npx skills add <owner>/<repo> --skill <skill-name> --agent codex
```

For large repos, `npx skills add` may spend most of its time cloning the entire repository and can exceed practical tool timeouts.

## Fallback procedure

1. Try the official command first with a bounded timeout and non-interactive flags when appropriate:

```bash
npx skills add <owner>/<repo> --skill <skill-name> --agent codex -g -y
```

2. If it stalls repeatedly, inspect whether any install process is still running before retrying.

3. Fetch only the requested skill directory from GitHub into:

```bash
~/.agents/skills/<skill-name>/
```

The minimum valid structure is:

```txt
~/.agents/skills/<skill-name>/SKILL.md
~/.agents/skills/<skill-name>/agents/openai.yaml   # when present upstream
```

Copy any `references/`, `templates/`, `scripts/`, or assets shipped with that skill.

4. Update `~/.agents/.skill-lock.json` consistently so the skills CLI can recognize the install. Preserve existing entries and include enough source metadata to identify the upstream repo/skill.

5. Verify from the CLI, not by eyeballing files:

```bash
npx skills list -g -a codex --json
```

Check that every requested skill appears and is associated with Codex.

## Reporting

Report:

- which skills installed via official command;
- which skills used the fallback;
- final verification command and result;
- install path, usually `~/.agents/skills/`.

Do not call the fallback a success until `skills list` recognizes the skills.
