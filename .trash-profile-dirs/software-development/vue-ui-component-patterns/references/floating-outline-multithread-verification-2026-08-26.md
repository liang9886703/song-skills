# Session detail: FloatingOutline multi-thread conflict + verification (blogV2, 2026-08-26)

Repo: `/Users/songkuakua/Documents/code/Codex-Blog-AI-Chat/blogV2`
File: `app/components/content/FloatingOutline.vue`

## Incident

User reported: "你的改动被另一个线程给干没了"

## Investigation

### What actually happened

1. **File content was intact** — `git diff` and `grep` confirmed all modifications (`outlineNav`, `handleWheel`, `width: 220px`, `justify-content: flex-end`, `text-align: right`) were present in the working tree.
2. **Browser was loading stale code** — the rendered component still had old `data-v-f5c3bc79` hash and old computed styles (`width: auto`, `justifyContent: normal`).
3. **Root cause: Nuxt 4 + Vite hot-reload failure for scoped CSS** — the dev server was serving cached CSS even though the source file had been modified. This is a known reliability issue (Pattern 9).

### Why the user thought it was "干没了"

The user saw the old rendering in their browser and assumed the file had been overwritten by another agent/thread. In reality:
- The file was never overwritten.
- The browser simply hadn't loaded the new code due to Vite's stale cache.

### Verification method that worked

1. **Checked `git diff`** — confirmed modifications were present.
2. **Checked `grep` for key strings** — `outlineNav`, `handleWheel`, `width: 220px`, `justify-content: flex-end` all found in source.
3. **Checked browser `document.styleSheets`** — found the new CSS rules (`width: 220px`, `justify-content: flex-end`) were actually present in the served stylesheet, but only inside `:hover` / `@container` blocks.
4. **Realized the verification error** — previous checks were reading computed styles in **non-hover state**, where the old `max-width: 220px` rule still applied. The new `width: 220px` and `justify-content: flex-end` were inside `.outline:hover ul.outline-labels` — they only activate on hover.
5. **Simulated hover state via injected CSS** — confirmed the new styles did apply when hover was active.

## Key lesson

**When verifying CSS changes in hover-dependent components, always check the hover state explicitly.** Reading computed styles without triggering `:hover` will show the default (non-hover) values, which can be mistaken for "the change didn't apply."

## Multi-thread safety note

In a multi-agent environment (Hermes + Codex + other threads), file overwrites are possible but rare. Before assuming a file was overwritten:
1. `git diff` to see uncommitted changes.
2. `git log --oneline -3` to see recent commits.
3. `grep` for key strings in the file.
4. Check file modification time (`ls -la`).

If all show the changes are present, the issue is almost certainly **browser/build cache**, not file loss.

## Related patterns

- Pattern 7 — Hover card click target + scroll passthrough
- Pattern 8 — Flex button text alignment (`text-align` ignored in flex contexts)
- Pattern 9 — Nuxt hot-reload verification habit
- Pattern 10 — Card width: `max-content` vs fixed width
