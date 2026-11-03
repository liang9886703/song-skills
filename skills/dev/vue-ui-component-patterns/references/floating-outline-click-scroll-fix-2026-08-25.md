# Session detail: FloatingOutline click-target + scroll-passthrough fix (blogV2, 2026-08-25)

Repo: `/Users/songkuakua/Documents/code/Codex-Blog-AI-Chat/blogV2`
File: `app/components/content/FloatingOutline.vue`

## User feedback

> "不要只在有文字的地方才能点击，应该是那一行都能点击，而且再卡片里面的时候，滚轮依然可以滚动正文的"

Two concrete interaction defects in the narrow-view hover card:
1. Row hit area was text-only (`width: max-content` on the `<button>`).
2. Wheel events inside the card were trapped (`overscroll-behavior: contain`).

## Fix applied

```diff
 /* hover card buttons */
 .outline:hover ul.outline-labels button {
-  width: max-content;
+  display: flex;
+  width: 100%;
   max-width: 100%;
   min-height: 16px;
   padding: 2.5px 6px;
   ...
+  cursor: pointer;
 }

 /* hover card container */
 .outline:hover ul.outline-labels {
   overflow-y: auto;
-  overscroll-behavior: contain;
+  overscroll-behavior: auto;
   scrollbar-width: thin;
   ...
 }
```

## Verification

- `npm run typecheck` passed.
- Browser verification was blocked by Nuxt dev-server restart (`.nuxt/dist` removed and rebuilt); user to confirm on next page load.

## Environment pitfall: Nuxt dev-server restart loop

During this session, the Nuxt dev server entered a restart loop after `.nuxt/dist` was removed (possibly by a file watcher or cache invalidation). Symptoms:

- Browser shows `.nuxt/dist directory has been removed. Restarting Nuxt...` for an extended period.
- `curl` to the dev server returns `503` or connection refused.
- Background `npm run dev` process shows repeated `[vue-tsc] Found 0 errors. Watching for file changes.` but the HTTP server never becomes ready.

**Fix:** kill the stale background process (`process kill`) and restart `npm run dev` fresh. Do not wait for auto-recovery — it may stay stuck for minutes. After restart, verify with `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000` before attempting browser automation.

**Lesson for UI verification workflow:** when the user says "没生效", first check if the dev server is actually serving requests (HTTP 200), not just whether the process is running. A stuck Nuxt restart makes hot-reload appear broken even when the code change is correct.

## Design principle captured

Transient hover cards should feel like **part of the page**, not modal overlays:
- Full-row click targets (not just text).
- Scroll chaining allowed (`overscroll-behavior: auto`), so the user can keep scrolling the article while the card is open.
- No `wheel` event blocking.
