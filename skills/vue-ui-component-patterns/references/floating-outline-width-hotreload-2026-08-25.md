# Session detail: FloatingOutline card width + Nuxt hot-reload failure (blogV2, 2026-08-25)

Repo: `/Users/songkuakua/Documents/code/Codex-Blog-AI-Chat/blogV2`
File: `app/components/content/FloatingOutline.vue`

## User feedback

> "卡片是文字的最大长度，而且有上限"

After previous fixes (full-row click, scroll passthrough, text alignment), the hover card width was still `max-content` — it only expanded to fit the longest text item, not a consistent `220px` as intended. The card looked ragged and unpredictable.

## Root cause

The `ul.outline-labels` element had `width: max-content` inside the `@container reader (max-width: 1039px)` hover state. Even though `width: 220px` was added in a later edit, the **Nuxt dev server was serving stale CSS** — the browser kept rendering the old `max-content` rule.

## The Nuxt hot-reload failure

This session exposed a severe Nuxt 4 + Vite hot-reload reliability issue:

1. **Source file was correct** — `git diff` confirmed `width: 220px` and `justify-content: flex-end` were in the source.
2. **Type check passed** — `npm run typecheck` returned 0 errors.
3. **Nuxt restart showed no errors** — dev server compiled successfully.
4. **Browser still rendered old styles** — `data-v-f5c3bc79` hash never changed, computed styles showed `width: 176.875px` (content width) instead of `220px`.

### Debugging steps taken

- Verified compiled CSS in browser stylesheets: new properties were present in the `@container` rule.
- Cleared `.nuxt`, `node_modules/.cache`, `node_modules/.vite` — no effect.
- Killed and restarted `npm run dev` multiple times — no effect.
- Hard-refreshed browser (Ctrl+Shift+R) — no effect.
- Checked for Service Worker / browser cache — none found.

### Likely cause

Vite's dependency pre-bundling or Nuxt's component virtual module cache became corrupted after multiple `.nuxt/dist` removals and rebuilds. The component's scoped CSS hash (`data-v-f5c3bc79`) was generated from an older version of the file and was never invalidated, even though the file content changed.

### Workaround (not yet confirmed)

A full **cold start** is required:
1. Kill the dev server.
2. Delete `.nuxt`, `node_modules/.cache`, `node_modules/.vite`.
3. Clear browser cache / open in incognito.
4. Restart dev server.

If that fails, the nuclear option is to delete `node_modules` and `package-lock.json` and reinstall.

## Design principle captured

**Never trust hot-reload for scoped CSS changes in Nuxt 4.** Always verify with `window.getComputedStyle()` in the browser console before telling the user a change is live. If the computed style doesn't match the source, restart the dev server — don't assume the user "didn't refresh hard enough."

## Related patterns

- Pattern 7 — Hover card click target + scroll passthrough
- Pattern 8 — Flex button text alignment (`text-align` ignored in flex contexts)
- Pattern 9 — Nuxt hot-reload verification habit
