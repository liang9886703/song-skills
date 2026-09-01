# Tool-positioning comparison pattern

This session compared Figma, Magic Patterns, v0, Lovable, Codex, and 百度「秒哒」.

## Positioning ladder

```text
Figma            → design source / collaboration
Magic Patterns   → AI visual and interactive prototype exploration
v0               → AI frontend/full-stack web implementation
Lovable/秒哒      → AI application builder for an end-to-end MVP
Codex            → repository coding agent for real engineering work
```

## Useful distinctions

- “Can generate a page” does not mean “can maintain a product.”
- A hosted app builder starts from a prompt and owns much of the project workflow; a coding agent starts from a repository and works within its stack, tests, git history, and architecture.
- Lovable and 秒哒 are broadly the same product class, but they differ by ecosystem, language, deployment, service integrations, and portability. Verify export, database ownership, self-hosting, and custom backend support before calling them substitutes.
- For an existing Vue3 project, use Magic Patterns for design exploration and Codex for implementation; use Lovable/秒哒 mainly for disposable MVPs or independent product experiments.

## Response shape that worked

Start with a direct category sentence, then give a compact table with `定位 / 主要产物 / 控制力 / 适合场景`, then end with a concrete recommendation for the user's project. Mention uncertainty only where a current product feature must be verified.

## Source-checking note

For current product positioning, check official landing pages or docs first. The Magic Patterns page described itself as an AI design tool for product teams that turns prompts into production-ready UI, supports design-system context, and enables interactive prototyping/collaboration. Avoid hard claims about pricing, code export, framework support, or deployment unless verified from current documentation.
