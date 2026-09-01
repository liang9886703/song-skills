---
name: vue-ui-component-patterns
description: Use when debugging Vue/Nuxt hover cards or panel collapse.
---

# Vue UI Component Patterns

Recurring pitfalls when editing Vue/Nuxt UI components — especially shell layouts (topbar / sidebar / chat rail) and floating hover UI (outlines, popovers, preview cards).

## Pattern 1 — Hover card on a tiny trigger: never bind open/close to the trigger alone

**Symptom:** a tiny trigger (a 6–8px indicator line, dot, icon) should reveal an offset floating card on hover. Implementation with per-item `@mouseenter` to set `hoveredId` and `@mouseleave` to clear it appears to "not work" — the card flickers or never appears.

**Root cause:** the floating card is absolutely positioned `right: calc(100% + Npx)` away from the trigger. The cursor must cross a dead gap between trigger and card. The instant it leaves the trigger, `mouseleave` fires, `v-if` tears the card down, and the transition never gets a frame to render. Keyboard `focus`/`blur` has the same flaw.

**Fix — two levels, prefer the simpler one:**

**Level 1 (preferred): pure-CSS hover morph, zero JS state.** When the revealed content is a *shared* panel (same content regardless of which trigger line is hovered — e.g. a full TOC list), don't keep any hover state in Vue at all. Render both states inside one wrapper and cross-fade with CSS:
```vue
<div class="outline-rail">
  <ul class="outline-rules">…dashes…</ul>
  <div class="outline-card">…shared list…</div>
</div>
```
```css
.outline-card { opacity: 0; visibility: hidden; pointer-events: none;
                transition: opacity .16s, visibility .16s; }
.outline-rail:hover .outline-rules { opacity: 0; pointer-events: none; }
.outline-rail:hover .outline-card  { opacity: 1; visibility: visible; pointer-events: auto; }
```
CSS `:hover` on the shared parent keeps the card alive while the cursor is anywhere inside the wrapper — no timers, no races, no flicker. This was the only version the user accepted after two JS iterations failed in their browser.

**Level 2 (only when content is per-trigger): hoverscope the wrapper, debounce the close.**
1. Wrap the trigger list AND the preview card in one positioned container (e.g. `.outline-rules-zone`).
2. Bind `@mouseenter="openCard"` / `@mouseleave="scheduleClose"` on the wrapper, not per item.
3. `scheduleClose` uses a ~150–200ms timeout so brief excursions outside the wrapper don't kill the card.
4. Keep per-item `aria-current`/`:hover` styling driven by a single boolean (`isCardOpen`), not a per-id `hoveredId`.

**Anti-pattern that signals you're on the wrong path:** if you find yourself writing `v-show` + scoped `display:none` + an attribute selector like `.card[style*="display: block"]` to fight Vue's inline-style toggle — stop. That's CSS/JS fighting each other; delete the JS state and go pure CSS instead of patching further.

**User's design taste for hover reveals (explicit correction):**
- The revealed element **replaces/morphs the trigger in place** — not an adjacent floating card offset to the side. ("不是横线旁边多一个卡片，而是浮现的卡片代替这个横线")
- Active/current item in revealed lists: **bold + ink color only**. No trailing dot/marker — "加粗就已经能表示当前所在层级了".
- Keep the card minimal: no title bar ("本文目录" header was rejected), no heavy shadow, compact rows with subtle hover background.
- **Width is content-adaptive, not fixed.** Use `width: max-content` with `min-width` / `max-width` guards, not a fixed `width: NNNpx`. Fixed widths produced "大片空白" / wide empty trailing space. Final shape:
  ```css
  .outline-card {
    min-width: 140px;
    max-width: 220px;
    width: max-content;
    padding: 6px;            /* tight inner padding */
  }
  .outline-card-list { gap: 2px !important; }
  .outline-card__link { padding: 6px 10px; border-radius: 6px; font-size: 13px; }
  ```
- **Visual restraint over decoration.** When the user says "有点丑", the diagnosis is almost always over-decoration: too much shadow, too much border, too much spacing, too loud a title bar, a useless trailing dot. Strip back to: subtle border, modest shadow, generous line-height, ink-soft for inactive / ink+bold for active.

## Pattern 4 — Design-variant first for vague "不够好看" feedback

**Symptom:** user says "不够好看" / "有点丑" / "需要重构" about a UI element, but doesn't specify what "好看" means. Jumping straight to a single "improved" implementation risks another rejection loop.

**Root cause:** "好看" is a subjective composite of spacing, color, weight, motion, and density. Without constraints, the agent often over-corrects toward their own aesthetic (usually heavier, more decorated) rather than the user's established taste.

**Fix — present 2–3 named variants before touching code:**
1. **Extract the current shape** from the live page (screenshot + computed styles) so the user sees you understand the baseline.
2. **Name each variant** with a one-line philosophy (e.g. "A: 精致卡片式", "B: 侧边栏融合式", "C: 极简增强式") and state what changes vs. what stays.
3. **Map each variant to the user's prior corrections** in this skill (Pattern 1). If they previously rejected heavy shadow, title bars, fixed widths, and trailing dots, your variants should *all* respect those constraints; the differences should be in layout position, information density, and motion style — not in decoration level.
4. **Let the user pick** before writing the final CSS. This converts an aesthetic guessing game into a constrained choice.

**User's established taste constraints (from Pattern 1 + this session):**
- Active/current item: **bold + ink color only**, no dots, no bars, no extra icons.
- Card width: `max-content` with min/max guards, never fixed.
- No title bar on hover cards.
- Subtle border, modest shadow, compact rows.
- In-place morph over adjacent popup.
- **Position matters as much as styling.** A card that overlaps Share buttons or正文 text is automatically "不好看" regardless of internal polish.

## Pattern 5 — Collapsing a Vue child panel: `width: 0 !important` is not enough

**Symptom:** parent shell toggles `chatOpen`/`sidebarOpen` and applies `.shell-panel--closed { width: 0 !important; flex-basis: 0 !important; opacity: 0; visibility: hidden }` to the child component root. The panel stays visible / the close button "does nothing".

**Root cause:** the child component's own scoped CSS sets `flex: 0 0 var(--chat-width)` (a `flex` shorthand) and a `border-left`. `flex-basis: 0 !important` alone does not reliably defeat the `flex` shorthand, and residual borders / min-width / padding keep the rail visually present.

**Fix — the closed class must defeat every sizing axis the child can set:**
```css
.shell-panel--closed {
  width: 0 !important;
  min-width: 0 !important;
  flex: 0 0 0 !important;      /* beats child `flex: 0 0 var(--chat-width)` */
  flex-basis: 0 !important;
  opacity: 0;
  visibility: hidden;
  border-left-width: 0 !important;
  border-right-width: 0 !important;
  padding: 0 !important;
  pointer-events: none !important;
  transition-delay: 0s, 0s, 0s, var(--shell-motion-duration);
}
```
Keep it in a shared stylesheet (e.g. `assets/css/motion.css`) so both sidebar and chat rail reuse the same collapse semantics. `flex: 0 0 0 !important` is the load-bearing line — don't rely on `flex-basis` alone.

## Pattern 6 — Text-selection action button: defer until pointer is up

**Symptom:** an action button (e.g. \"add comment\" speech-bubble) appears *while the user is still dragging to select* text, flickering and chasing the cursor.

**Root cause:** listening only to `selectionchange` or `mouseup`/`keyup`. The `selectionchange` event fires continuously as the drag expands, so the button appears mid-drag and tracks the cursor — visually noisy and distracting.

**Fix — gate on pointer state, delay the reveal:**
```ts
let selectionTimer: ReturnType<typeof setTimeout> | null = null
let isPointerDown = false

function updateSelection() {
  // … compute anchor, position as before …
  if (isPointerDown) {
    clearSelectionTimer()
    if (panel.value === 'selection') closePanel()  // suppress while dragging
    return
  }
  if (panel.value !== 'selection') {
    clearSelectionTimer()
    selectionTimer = setTimeout(() => {
      selectionTimer = null
      if (pendingAnchor.value && selectionRange) panel.value = 'selection'
    }, 100)  // 100ms after pointerup
  }
}

function onRootPointerDown() {
  isPointerDown = true
  clearSelectionTimer()
  if (panel.value === 'selection') closePanel()
}
function onRootPointerUp() {
  isPointerDown = false
  updateSelection()
}
```
Bind `pointerdown`/`pointerup` on the prose root, keep `selectionchange` as the canonical watcher for keyboard selection, and always clear the timer on `closePanel()`.

**User sizing preference for action chips:**
- The floating action button should be **compact**, not the same size as composer/detail cards. Final shape for the blogV2 comment chip: `width: 30px; height: 28px; border-radius: 9px; icon: 14px`. An earlier `40px × 36px` + `17px` icon was called \"太大了\".
- Speech-bubble / popover icons at 14px in a 28–30px chip reads as balanced; going to 17px+ in a 36px+ chip dominates the text selection.

## Pattern 7 — Hover card click target + scroll passthrough

**Symptom:** a hover-revealed card (TOC, outline, quick-nav) has two interaction defects: (a) only the text inside each row is clickable, not the full row; (b) when the cursor is inside the card, the mouse wheel is trapped and cannot scroll the underlying page.

**Root cause:** (a) the row `<button>` uses `width: max-content` so its hit area hugs the text; (b) the card container sets `overscroll-behavior: contain` (or the card has `overflow-y: auto` with a scrollbar), which blocks wheel events from propagating to the page scroll container.

**Fix — two one-line CSS changes:**
```css
/* (a) Full-row click target */
.my-card button {
  display: flex;
  width: 100%;          /* was: max-content */
  max-width: 100%;
}

/* (b) Let wheel events pass through to the page */
.my-card {
  overflow-y: auto;
  overscroll-behavior: auto;  /* was: contain */
}
```

**Why this works:**
- `width: 100%` on a flex button stretches the hit area to the card's inner width; the text stays right-aligned via `text-align: right` or `justify-content: flex-end`.
- `overscroll-behavior: auto` removes the scroll-chain block. When the card has no scrollbar (short list), wheel events fall through to the page immediately. When the card is scrollable, the user scrolls the card first, then the page takes over at the boundary — the standard "scroll chaining" behavior users expect.

**Anti-pattern:** don't add `@wheel.stop` or `e.preventDefault()` on the card to "keep it stable" — that breaks the user's mental model of scrolling past a transient overlay.

## Pattern 8 — Flex button text alignment: `text-align` is ignored, use `justify-content`

**Symptom:** a `<button>` styled with `display: flex` and `text-align: right` still shows text left-aligned. The user reports "文字没右对齐" even though `text-align: right` is clearly in the CSS.

**Root cause:** `text-align` applies to **inline-level content** inside a block container. When the button is `display: flex`, its children become flex items, and `text-align` on the flex container does **not** affect the alignment of flex items. The text node inside the button is treated as an anonymous flex item, and its alignment is controlled by the flex container's `justify-content` (main axis) and `align-items` (cross axis), not by `text-align`.

**Fix — pair `text-align` with `justify-content` for flex buttons:**
```css
.my-card button {
  display: flex;
  width: 100%;
  text-align: right;        /* fallback for non-flex contexts */
  justify-content: flex-end; /* actual alignment for flex layout */
}
```

**Why this works:** `justify-content: flex-end` packs flex items toward the right edge of the button, which achieves the visual right-alignment the user expects. `text-align: right` is kept as a defensive fallback in case the button ever loses `display: flex`.

**When this bites you:** any time you convert a text-aligned `<button>` or `<a>` to `display: flex` for full-row click targets (Pattern 7). The two properties must be updated together — `text-align` alone is silently ignored in flex contexts.

## Pattern 9 — Nuxt hot-reload may not apply scoped CSS changes: verify with computed styles, not just source

**Symptom:** you edit a Vue SFC's `<style scoped>` block, the dev server shows "0 errors", but the browser still renders the old styles. The user says "没生效" and you suspect a cache issue.

**Root cause:** Nuxt 4 + Vite's hot-reload for scoped styles can be unreliable when the component's style block changes in specific ways (e.g. adding new selectors inside `@container` queries, or modifying nested hover states). The `.nuxt` dev cache may serve stale CSS even though the source file is correct. This is especially common after `.nuxt/dist` is removed and rebuilt, or when the dev server has been running for a long time across multiple edits.

**Fix — three-step verification:**
1. **Check the served CSS** in browser dev tools: find the component's `data-v-*` attribute in the rendered DOM, then search the active stylesheets for that attribute selector. Confirm the new property values are actually present.
2. **Check computed styles** on the target element: `window.getComputedStyle(el)` should reflect the new values. If it doesn't, the CSS isn't being applied — not just overridden.
3. **Hard-restart the dev server** if the served CSS is stale: `kill` the background `npm run dev` process and restart it. Do not rely on hot-reload for scoped style changes that involve `@container` or complex nesting.

**Lesson:** when the user reports a CSS change "没生效", don't immediately re-edit the source. Verify the served CSS first — the bug may be in the build pipeline, not your code.

## Pattern 10 — Card width: `max-content` vs fixed width — when to use which

**Symptom:** a hover card's width is unpredictable — sometimes too narrow, sometimes too wide — because it uses `width: max-content` and the content length varies. The user says "卡片是文字的最大长度，而且有上限" and wants a consistent width.

**Root cause:** `max-content` sizes the card to the longest single item. Short lists produce a narrow card; long lists produce a wide card. The `max-width` guard (e.g. `min(252px, calc(100vw - 40px))`) only kicks in when content exceeds it, but doesn't establish a baseline width.

**Fix — choose based on content type, but prefer content-adaptive for nav/TOC:**
- **Content-adaptive width (preferred for TOC/nav):** use `width: max-content` with `min-width` to prevent collapse (e.g. `min-width: 140px`). Fixed widths like `220px` often produce "太宽了" / "左边空了一大块" feedback because the longest item rarely fills the fixed width. The user explicitly rejected `width: 220px` in favor of `max-content` after seeing it live.
- **Fixed width (only when the user explicitly asks for consistency):** if the user complains about width jumping between items, use a fixed `width` with `max-width` as a safety guard. But be prepared to revert to `max-content` if they say it feels too wide.

**Anti-pattern:** don't mix the two. If you set `width: 220px` but the browser still renders `max-content`, the CSS isn't being applied — check Pattern 9 (Nuxt hot-reload failure) before assuming the user is wrong.

The workspace-root redirect fix for split song/mine workspaces (blogV2, Aug 26 2026) is in `references/workspace-root-redirect-2026-08-26.md`.
The Nuxt dev server crash and port drift issue (blogV2, Aug 26 2026) is in `references/nuxt-dev-server-crash-port-drift-2026-08-26.md`.
The card width revert from fixed 220px back to max-content after user feedback "太宽了" (blogV2, Aug 26 2026) is in `references/floating-outline-width-maxcontent-revert-2026-08-26.md`.

## Pattern 11 — Workspace root path redirect: empty path defaults to home, which may belong to another workspace

**Symptom:** after splitting a blog into multiple workspaces (e.g. `song` / `mine`), clicking a workspace in the system switcher redirects to the wrong workspace. For example, `/mine` redirects to `/song` instead of showing the `mine` workspace content.

**Root cause:** when `segments = []` (root path like `/mine`), `resolveModuleRoute` returns `homeModule`. But `home` may not be in the target workspace's `navigationModuleIds`. The module visibility check then redirects to the workspace that owns `home` — which is the wrong target.

**Fix — add a workspace-root redirect before the visibility check:**

```ts
// When landing on a workspace root with no path, redirect to the first
// available module for that workspace instead of showing the home module
// (which may belong to a different workspace).
if (segments.value.length === 0 && activeModule.value.id === 'home') {
  const firstModuleId = navigationModuleIdsForSystem(system.value)[0]
  if (firstModuleId && firstModuleId !== 'home') {
    await navigateTo(`/${system.value}/${firstModuleId}`, { replace: true })
  }
} else if (!isModuleVisibleInSystem(system.value, activeModule.value.id, ARTICLE_MODULE_ID)) {
  // ... existing redirect logic
}
```

**Key points:**
- The `else if` is critical — without it, both `navigateTo` calls execute and the second one wins.
- Import `navigationModuleIdsForSystem` from `~/modules/workspaces`.
- The redirect target is the first module in the workspace's `navigationModuleIds` array.

**Verification:** `curl -I http://localhost:3000/mine` should return 302 to `/mine/tasks` (not `/song`).

The workspace-root redirect fix for split song/mine workspaces (blogV2, Aug 26 2026) is in `references/workspace-root-redirect-2026-08-26.md`.
The sidebar utility footer proportion unification (blogV2, Aug 26 2026) is in `references/sidebar-utility-footer-proportion-fix-2026-08-26.md`.

## Pattern 12 — Sidebar utility footer: unify row metrics with navigation rows

**Symptom:** the bottom utility footer (theme toggle, social icons) looks visually "off" compared to the navigation rows above it — different height, different spacing, not "like a row".

**Root cause:** the footer was designed independently with its own padding (`10px 12px`), gap (`4px`), and fixed-size icon buttons (`28×28px`). The navigation rows use `padding: 5px 16px` and `gap: 10px`. The mismatch in row metrics makes the footer feel like a separate component rather than a continuation of the sidebar list.

**Fix — copy the row metrics from `.module-row`:**

```css
.sidebar-footer {
  display: flex;
  align-items: center;
  gap: 10px;          /* match .module-row */
  border-top: 1px solid var(--line);
  padding: 5px 16px;  /* match .module-row */
}
```

Also unify icon sizes within the footer (e.g. X icon was `14px` while others were `16px` — bump to `16px`).

**Key lesson:** "looks like a row" is determined by **padding and gap**, not by button size. Navigation rows are text+icon (auto width), footer rows are icon-only (fixed 28px). The buttons can differ in size as long as the row metrics (padding, gap) are identical.

**Layout variant — equal-width icon buttons (user preference):** when the user wants the footer icons to feel like "text characters" in a row, use `flex: 1` on each button so they share the row width equally. This creates a balanced, typographic rhythm where each icon occupies the same visual "space" as a word would:

```css
.footer-icon-button {
  display: flex;
  flex: 1;              /* equal width, like characters in a justified line */
  height: 28px;
  align-items: center;
  justify-content: center;
  /* ... rest same ... */
}
```

**User taste:** the user explicitly rejected a vertical stack (`flex-direction: column`) for the footer — "别啊，样式还是得我之前那样，一行放 4 个". The footer must remain a single horizontal row, even when unifying metrics with the vertical nav list above it.

## Verification habit

**"Currently looks fine" is not a resolution.** When a user reports a UI bug with a screenshot and your live check shows the page rendering correctly, do NOT reply "it's a transient state, refresh and tell me if it recurs" and stop. The user's screenshot is proof a real broken state exists — your job is to find the boundary condition that produces it and fix that, even if the default path currently renders fine. The user pushed back on exactly this: "去修他 / 你直接操作浏览器不行？" — drive the browser yourself, reproduce the broken state deterministically (see the `browser_console` force-reflow recipe in Pattern 23), apply the fix, and verify the broken state can no longer occur. Closing with "can't reproduce" is a failed outcome for this user even when it's technically true.

**Symptom:** user says "your changes were overwritten by another thread" or "the file got reverted", but `git diff` shows the modifications are still present. The browser renders old styles, making it look like the file was rolled back.

**Root cause:** in a multi-agent environment (Hermes + Codex + other threads), it's easy to assume a file was overwritten when the browser shows stale rendering. But the actual cause is almost always **Vite/Nuxt hot-reload cache**, not file loss. The file on disk has the new code; the browser just hasn't loaded it.

**Fix — verify before assuming:**
1. `git diff <file>` — confirms uncommitted changes are present.
2. `grep -n "key-string" <file>` — confirms the specific edit is in the source.
3. `ls -la <file>` — check modification time (should be recent).
4. `git log --oneline -3` — check if another thread committed a revert.

If all show the changes are present, the issue is **browser/build cache**, not file loss. Follow Pattern 9 (Nuxt hot-reload verification) instead of re-editing the file.

**Multi-thread file race (inverse case):** the same `patch` tool that defends you with `_warning: file modified since last read` is also your early-warning that another thread touched the file. When you see that warning, **stop and re-read the whole file** — don't blindly retry the patch. In this session another thread had converted `SkillsDetail.vue` from a `document` prop to a `skill: SkillInfo` prop with a `parsedBody` computed; I nearly shipped a "fix" that restored `:body="document.body"`, which would have broken their refactor and introduced a `TS2339`. The correct move was to re-read, discover the new `SkillInfo` type, and align with their design (or leave their code alone entirely). Treat any externally-modified file as "not yours to redesign" until you understand the new shape.

The workspace-root redirect fix for split song/mine workspaces (blogV2, Aug 26 2026) is in `references/workspace-root-redirect-2026-08-26.md`.
The Nuxt dev server crash and port drift issue (blogV2, Aug 26 2026) is in `references/nuxt-dev-server-crash-port-drift-2026-08-26.md`.
The card width revert from fixed 220px back to max-content after user feedback "太宽了" (blogV2, Aug 26 2026) is in `references/floating-outline-width-maxcontent-revert-2026-08-26.md`.
The sidebar utility footer proportion unification (blogV2, Aug 26 2026) is in `references/sidebar-utility-footer-proportion-fix-2026-08-26.md`.
The sidebar utility footer equal-width icon buttons (blogV2, Aug 26 2026) is in `references/sidebar-utility-footer-equal-width-buttons-2026-08-26.md`.
The sidebar utility row inline merge — moving theme toggle + social links from a separate footer into a 4th navigation row (blogV2, Aug 26 2026) — is in `references/sidebar-utility-row-inline-merge-2026-08-26.md`.
The sidebar layout order swap — navigation above article area, utility row stays at top of article area (blogV2, Aug 26 2026) — is in `references/sidebar-layout-order-swap-2026-08-26.md`.
The search bar path-segment badges + pre-refactor color restoration via `git show` (blogV2, Aug 26 2026) is in `references/search-bar-path-badges-color-restore-2026-08-26.md`.

## Pattern 15 — Reference-image badges: bind to dynamic data, not literal strings

**Symptom:** user shares a reference screenshot of a UI element (e.g. a search bar) and asks to restyle the local component "in that style". The screenshot shows small badge-like elements whose meaning is ambiguous (could be keyboard shortcuts, path segments, active filters, etc.). Agent picks the most literal interpretation and hardcodes it; user corrects with the actual semantic meaning.

**Fix — when the badge content is ambiguous, prefer dynamic data:**
1. List the plausible interpretations (keyboard hint? current path? active workspace? filter state?).
2. If the component already receives a relevant prop (e.g. `currentPath`, `system`, `activeModule`), bind the badges to that prop — dynamic data is the more common real-world meaning.
3. Render each segment/chip with the same visual treatment as the reference (small border, mono font, 4px radius) but with content derived from props.
4. If truly static, confirm with the user before hardcoding literal strings.

**Anti-pattern:** screenshot shows `/` `Tab` badges → agent renders literal `<kbd>/</kbd><kbd>Tab</kbd>`. User actually meant "this is where the current path goes". One round-trip wasted.

## Pattern 16 — "颜色不一样了" after a CSS-vars refactor: restore exact previous literals via git

**Symptom:** a theming refactor converts hardcoded colors to CSS variables. User reports a subtle visual regression — "颜色好像和之前不一样了", "看着不太对". Nothing in the diff looks wrong, but the rendered color/border/shadow is off.

**Fix — don't re-derive from the screenshot; recover the exact previous value from git:**
```bash
git log --oneline -5 -- <file>
git show <prev-sha>:<file> | grep -A2 '<selector>'
```
Paste the literal pre-refactor values back (or verify the var actually resolves to the same color under the active theme). CSS vars like `--line-strong` vs `#d5d9df`, or `--card-bg` vs `white`, often differ in subtle ways (alpha, theme-dependent resolution) that only show up in side-by-side rendering.

**Lesson:** "var rename" refactorings are not always value-preserving. When the user's eye says the color changed, trust it and check git — don't argue that "the var should be equivalent".

## Pattern 13 — Workspace root path redirect: empty path defaults to home, which may belong to another workspace

**Symptom:** after splitting a blog into multiple workspaces (e.g. `song` / `mine`), clicking a workspace in the system switcher redirects to the wrong workspace. For example, `/mine` redirects to `/song` instead of showing the `mine` workspace content.

**Root cause:** when `segments = []` (root path like `/mine`), `resolveModuleRoute` returns `homeModule`. But `home` may not be in the target workspace's `navigationModuleIds`. The module visibility check then redirects to the workspace that owns `home` — which is the wrong target.

**Fix — add a workspace-root redirect before the visibility check:**

```ts
// When landing on a workspace root with no path, redirect to the first
// available module for that workspace instead of showing the home module
// (which may belong to a different workspace).
if (segments.value.length === 0 && activeModule.value.id === 'home') {
  const firstModuleId = navigationModuleIdsForSystem(system.value)[0]
  if (firstModuleId && firstModuleId !== 'home') {
    await navigateTo(`/${system.value}/${firstModuleId}`, { replace: true })
  }
} else if (!isModuleVisibleInSystem(system.value, activeModule.value.id, ARTICLE_MODULE_ID)) {
  // ... existing redirect logic
}
```

**Key points:**
- The `else if` is critical — without it, both `navigateTo` calls execute and the second one wins.
- Import `navigationModuleIdsForSystem` from `~/modules/workspaces`.
- The redirect target is the first module in the workspace's `navigationModuleIds` array.

**Verification:** `curl -I http://localhost:3000/mine` should return 302 to `/mine/tasks` (not `/song`).

## Pattern 14 — Sidebar layout order: navigation above content, utility row stays with content

**Symptom:** after merging a utility row (theme toggle + social links) into a sidebar section, the visual order feels wrong — navigation items end up at the bottom and utility/content at the top, or vice versa.

**Root cause:** the parent component's flex column order determines visual stacking. When `<SidebarNavigation />` is placed after the scrollable content wrapper, it renders below it. The user expects a fixed hierarchy: primary navigation first, then utility, then content tree.

**Fix — reorder siblings in the parent, don't redesign the child:**

```vue
<template>
  <nav class="project-sidebar">
    <!-- 1. Primary navigation at top -->
    <SidebarNavigation ... />
    <!-- 2. Scrollable content area below -->
    <div class="sidebar-scroll-wrap">
      <div class="sidebar-scroll">
        <ArticleNavigation ... />  <!-- utility row lives at top of this -->
      </div>
    </div>
  </nav>
</template>
```

Also flip the border direction to match the new order:
```css
.project-sidebar > :deep(.sidebar-navigation) {
  border-bottom: 1px solid var(--line);  /* was border-top when nav was at bottom */
}
```

**Key lesson:** the utility row belongs to the content section (it's the "toolbar" for the article tree), not to the navigation. Keep it inside `ArticleNavigation`, but ensure `ArticleNavigation` renders below `SidebarNavigation` in the parent. When a layout feels "wrong" after a merge, the fix is often just reordering siblings in the parent component.
The search bar path-segment badges + pre-refactor color restoration via `git show` (blogV2, Aug 26 2026) is in `references/search-bar-path-badges-color-restore-2026-08-26.md`.
The search bar path badges hide/show on typing with Transition animation (blogV2, Aug 26 2026) is in `references/search-bar-path-badges-hide-show-animation-2026-08-26.md`.
The dev server port drift and stale process cleanup (blogV2, Aug 26 2026) is in `references/dev-server-port-drift-stale-process-cleanup-2026-08-26.md`.
The sidebar layout order swap — navigation above article area, utility row stays at top of article area (blogV2, Aug 26 2026) — is in `references/sidebar-layout-order-swap-2026-08-26.md`.

## Pattern 17 — Conditional show/hide of inline UI elements: use Vue Transition, not CSS classes

**Symptom:** an inline element (e.g. path badges in a search bar) should disappear when the user starts typing and reappear when the input is cleared. A plain `v-if` toggle works but feels abrupt — no animation.

**Fix — wrap in `<Transition>` with a named transition:**

```vue
<Transition name="search-path">
  <div v-if="!query" class="search-path">...</div>
</Transition>
```

```css
.search-path-enter-active, .search-path-leave-active { transition: opacity 120ms ease, transform 120ms ease; }
.search-path-enter-from, .search-path-leave-to { opacity: 0; transform: translateX(4px); }
.search-path-enter-to, .search-path-leave-from { opacity: 1; transform: translateX(0); }
```

**Key points:**
- The `name` on `<Transition>` becomes the CSS class prefix (`search-path-enter-*`, `search-path-leave-*`).
- Keep the animation fast (`120ms`) — this is a micro-interaction, not a page transition.
- `translateX(4px)` gives a subtle directional cue without being distracting.
- Don't add `transition` to the base class (`.search-path`) — only the enter/leave classes need it.

**Anti-pattern:** don't use `v-show` + manual CSS class toggles for this. Vue's `<Transition>` handles the mount/unmount timing automatically, including the brief window where the element is leaving but still needs to be rendered for the leave animation to play.

## Pattern 18 — Dev server port drift: kill stale processes before restarting

**Symptom:** `npm run dev` starts but binds to an unexpected port (e.g. 3001 instead of 8080). The user expects the app at a specific port (e.g. 8080) but gets a "port not available" fallback.

**Root cause:** a previous dev server process (or another Node process) is still holding the target port. Nuxt's `get-port` finds the port occupied and auto-increments to the next available one.

**Fix — check and kill stale processes before restarting:**

```bash
# Check what's on the target port
lsof -nP -iTCP:8080 -sTCP:LISTEN

# Kill the stale process(es)
kill <PID>

# Also check common fallback ports if the app was restarted multiple times
lsof -nP -iTCP:3000 -sTCP:LISTEN
lsof -nP -iTCP:3001 -sTCP:LISTEN
kill <PID>
```

**Key lesson:** "port already in use" is not always obvious — the process may be a zombie from a previous `npm run dev` that wasn't cleanly killed. Always `lsof` before assuming the port is free. If the user says "部署到 8080 了吗，重启一下呢", check 8080, 3000, and 3001 — Nuxt's port fallback chain often leaves multiple stale processes.

**User expectation:** the project AGENTS.md should document the expected port (e.g. 8080) so agents don't have to guess. When the actual port drifts, the user notices immediately.

## Pattern 19 — Component moved between parents: check sibling order, not just the moved component

**Symptom:** after moving a utility component (e.g. sidebar footer with theme toggle + social links) from one parent to another, the visual order is "反了" — the moved component and the remaining content are in the wrong stacking order.

**Root cause:** Vue renders components in the order they appear in the parent's `<template>`. Moving a component from below a scrollable content area to above it (or vice versa) changes the visual hierarchy. The child component itself is correct; the parent's sibling order is wrong.

**Fix — reorder siblings in the parent template, not the child:**

```vue
<!-- Wrong: navigation below article content -->
<nav class="sidebar">
  <div class="scroll-wrap">
    <ArticleNavigation />  <!-- contains utility row at top -->
  </div>
  <SidebarNavigation />    <!-- renders at bottom -->
</nav>

<!-- Correct: navigation above article content -->
<nav class="sidebar">
  <SidebarNavigation />    <!-- renders at top -->
  <div class="scroll-wrap">
    <ArticleNavigation />  <!-- contains utility row at top -->
  </div>
</nav>
```

Also update the border direction to match the new order:
```css
.sidebar > :deep(.sidebar-navigation) {
  border-bottom: 1px solid var(--line);  /* was border-top when at bottom */
}
```

**Key lesson:** when a merged component looks "wrong", the fix is often just swapping the order of two sibling elements in the parent template. Don't redesign the child component — check the parent's layout first.

## Pattern 20 — Search bar inline badges: bind to dynamic data, not literal strings

**Symptom:** user shares a reference screenshot of a search bar with small badge-like elements and asks to restyle the local component "in that style". The screenshot shows ambiguous chips (could be keyboard shortcuts, path segments, active filters, etc.). Agent picks the most literal interpretation and hardcodes it; user corrects with the actual semantic meaning.

**Fix — when badge content is ambiguous, prefer dynamic data:**

1. List plausible interpretations (keyboard hint? current path? active workspace? filter state?).
2. If the component already receives a relevant prop (e.g. `currentPath`, `system`, `activeModule`), bind the badges to that prop — dynamic data is the more common real-world meaning.
3. Render each segment/chip with the same visual treatment as the reference (small border, mono font, 4px radius) but with content derived from props.
4. If truly static, confirm with the user before hardcoding literal strings.

**Anti-pattern:** screenshot shows `/` `Tab` badges → agent renders literal `<kbd>/</kbd><kbd>Tab</kbd>`. User actually meant "this is where the current path goes". One round-trip wasted.

**User correction example (blogV2, Aug 2026):** user showed a reference with badge chips and said "搜索栏里面用这个样式，现在的路径是显示在里面的文字的，改成他这种感觉". Agent initially rendered literal `/` and `Tab` keyboard shortcut badges; user corrected with "这个表示的是当前页面所在的路径". The fix was to render `currentPath` split by `/` into small mono-font chips with `/` separators.

## Pattern 21 — Hide inline UI on user input: use Vue Transition, not CSS classes

**Symptom:** an inline element (e.g. path badges in a search bar) should disappear when the user starts typing and reappear when the input is cleared. A plain `v-if` toggle works but feels abrupt — no animation.

**Fix — wrap in `<Transition>` with a named transition:**

```vue
<Transition name="search-path">
  <div v-if="!query" class="search-path">...</div>
</Transition>
```

```css
.search-path-enter-active, .search-path-leave-active { transition: opacity 120ms ease, transform 120ms ease; }
.search-path-enter-from, .search-path-leave-to { opacity: 0; transform: translateX(4px); }
.search-path-enter-to, .search-path-leave-from { opacity: 1; transform: translateX(0); }
```

**Key points:**
- The `name` on `<Transition>` becomes the CSS class prefix (`search-path-enter-*`, `search-path-leave-*`).
- Keep the animation fast (`120ms`) — this is a micro-interaction, not a page transition.
- `translateX(4px)` gives a subtle directional cue without being distracting.
- Don't add `transition` to the base class (`.search-path`) — only the enter/leave classes need it.

**Anti-pattern:** don't use `v-show` + manual CSS class toggles for this. Vue's `<Transition>` handles the mount/unmount timing automatically, including the brief window where the element is leaving but still needs to be rendered for the leave animation to play.

## Pattern 22 — "颜色不一样了" after a CSS-vars refactor: restore exact previous literals via git

**Symptom:** a theming refactor converts hardcoded colors to CSS variables. User reports a subtle visual regression — "颜色好像和之前不一样了", "看着不太对". Nothing in the diff looks wrong, but the rendered color/border/shadow is off.

**Fix — don't re-derive from the screenshot; recover the exact previous value from git:**

```bash
git log --oneline -5 -- <file>
git show <prev-sha>:<file> | grep -A2 '<selector>'
```

Paste the literal pre-refactor values back (or verify the var actually resolves to the same color under the active theme). CSS vars like `--line-strong` vs `#d5d9df`, or `--card-bg` vs `white`, often differ in subtle ways (alpha, theme-dependent resolution) that only show up in side-by-side rendering.

**Lesson:** "var rename" refactorings are not always value-preserving. When the user's eye says the color changed, trust it and check git — don't argue that "the var should be equivalent".

## Verification habit

After either fix, run the project's own check (`npm run typecheck` for Nuxt). When the user reports "didn't work", reproduce the pointer path yourself before re-patching: mental-trace `mouseenter → gap → mouseleave` for hover UI, and inspect the `flex`/`width` cascade across scoped styles for collapse UI.

**Dev-server sanity check before browser verification:** if the user says "没生效" after a CSS-only change, first confirm the dev server is actually serving (HTTP 200), not just that the process is running. A stuck Nuxt restart (e.g. after `.nuxt/dist` is removed) makes hot-reload appear broken even when the code change is correct. Kill and restart the dev server if the browser shows a restart loop.

**Hover-state verification:** when verifying CSS changes inside `:hover` or `@container` blocks, always simulate the hover state before reading computed styles. Reading computed styles without triggering hover will show default (non-hover) values, which can be mistaken for "the change didn't apply." Use `document.querySelector('.parent').classList.add('debug-hover')` with injected CSS, or simply hover the element manually before checking.

## Pattern 23 — Shell topbar overflow: zero-width flex children with `overflow: visible` can leak into siblings

**Symptom:** a shell topbar has three flex zones (start / center / end). The end zone contains a component (e.g. chat header) that shows/hides content based on a boolean prop. When the prop is true, the end zone's content overflows into the center zone, compressing breadcrumbs and pushing action buttons out of place.

**Root cause:** the end zone uses `width: 0; flex: 0 0 0; overflow: visible` as its collapsed state. The child component inside sets `flex: 1; width: 100%; overflow: visible`. When the child's `v-if` content is shown, the zero-width parent cannot constrain it — the content renders at its intrinsic width and spills into the center zone's space.

**Fix — constrain the child, not just the parent:**

1. **Parent (topbar-end):** keep `overflow: visible` for the toggle button, but add `position: relative` so absolutely-positioned children anchor correctly.
2. **Child (chat-panel-header):** remove `flex: 1` and `width: 100%` from the root. Use `position: absolute; right: 0; top: 0; bottom: 0` to pin the content to the end zone's right edge, with `width: var(--chat-width)` when open.
3. **Alternative (simpler, verified in blogV2 Aug 30 2026):** flip `overflow: visible → hidden` on **both** the parent zone (`.topbar-end`) and the child root (`.chat-panel-header`). Two one-line changes, no repositioning needed.

**Why the simple version works (verified against live page + e2e):**
- `.topbar-end { overflow: hidden }` clips anything that escapes the zero-width collapsed state, so `topbar-center` can never be overlapped.
- `.chat-panel-header { overflow: hidden }` clips the copy ("对话 / 未配置") when the header is squeezed.
- **The absolutely-positioned toggle button survives** because of a subtle flex behavior: the header has `min-width: 0` but its content (the 36px `position: absolute; right: 8px` bot toggle) gives it an intrinsic min-content width of ~70px, so the header never actually collapses to 0 — the toggle stays fully inside the header's box and is not clipped. Verify this with `getBoundingClientRect()` on both header and toggle before assuming the toggle is safe; if your toggle is a normal flow child (not absolute), it WILL be clipped and you need option 2 instead.

**Key lesson:** `width: 0` + `overflow: visible` on a flex parent is a loaded gun. Any child with `flex: 1` or intrinsic width will overflow. Either clip the child (`overflow: hidden` on parent) or pin the child (`position: absolute` with explicit width).

**Reproduction recipe (browser_console, no manual window-dragging needed):**
```js
const end = document.querySelector('.topbar-end');
end.style.transition = 'none';   // kill the width transition
end.style.width = '0';           // force the broken collapsed state
end.style.flexBasis = '0';
void end.offsetWidth;            // force reflow BEFORE measuring
// now measure header/copy rects vs .search-wrap rect to confirm overlap
```
Then restore (`end.style.transition = ''; end.style.width = ''; ...`). This simulates the mid-transition / missing-rail-class transient state deterministically — much faster than trying to catch it by resizing the window.

**Verification checklist after the fix:**
1. Force the zero-width state again → copy must report `visible: false` / zero visible width, and must not overlap `.search-wrap`'s right edge.
2. Toggle button (`chat-panel-header__bot-toggle`) must still report `visible: true` and be clickable — `overflow: hidden` must not have clipped it.
3. Run the existing e2e topbar/chat specs (blogV2 has 3: unconfigured chat contract, chat panel visual density, unconfigured sections render) — all must pass.

## Pattern 24 — Conditional flex panel: `v-if` vs `v-show` vs CSS `visibility` — when to use which

**Symptom:** a side panel (chat, sidebar, outline) toggles open/closed. Using `v-if` causes layout shift; using `v-show` keeps the element in the DOM but it still takes up space; using CSS `visibility: hidden` hides it but preserves layout.

**Fix — choose based on the panel's role:**

- **`v-if`:** use when the panel is expensive to render (heavy component, many DOM nodes) AND the layout shift is acceptable (e.g. mobile drawer that slides in from off-screen).
- **`v-show`:** use when the panel is cheap to render AND you need to preserve its state (e.g. chat input draft, scroll position) BUT you handle the width/visibility separately via CSS.
- **CSS `visibility` + `width: 0`:** use when the panel must animate smoothly (width transition) and you want to avoid Vue re-rendering. This is the blogV2 shell pattern: the element stays in the DOM, `width` transitions from `var(--chat-width)` to `0`, and `visibility` flips after the transition.

**Anti-pattern:** don't use `v-if` for a panel that transitions width — Vue will destroy/recreate the element on every toggle, killing the CSS transition. Don't use `v-show` alone for a zero-width panel — `display: none` removes it from the flex layout entirely, causing siblings to shift.

**blogV2 shell pattern (verified):**
```css
.shell-panel {
  width: var(--chat-width);
  flex: 0 0 var(--chat-width);
  transition: width var(--shell-motion-duration) var(--ease-shell),
              flex-basis var(--shell-motion-duration) var(--ease-shell),
              opacity var(--shell-motion-duration) var(--ease-shell);
}
.shell-panel--closed {
  width: 0 !important;
  min-width: 0 !important;
  flex: 0 0 0 !important;
  flex-basis: 0 !important;
  opacity: 0;
  visibility: hidden;
  border-left-width: 0 !important;
  border-right-width: 0 !important;
  padding: 0 !important;
  pointer-events: none !important;
  transition-delay: 0s, 0s, 0s, var(--shell-motion-duration);
}
```

**Key lesson:** the closed state must defeat every sizing axis the child can set (width, min-width, flex, flex-basis, borders, padding). See Pattern 5 for the full explanation.

## Pattern 25 — Chat header copy overflow: resize listener vs CSS clipping

**Symptom:** user reports "对话 / 未配置" appearing in the middle of the topbar, overlapping breadcrumbs, with path compressed to `.../...age`. Screenshot shows the chat header copy (title + status) intruding into `topbar-center` instead of staying inside `topbar-end`.

**First fix attempt (CSS clipping) — failed e2e:** changing `.topbar-end { overflow: visible → hidden }` and `.chat-panel-header { overflow: visible → hidden }` clips the overflowing copy, but also clips the absolutely-positioned bot toggle button (36px, `right: 8px`) when the parent has zero width. The toggle becomes unclickable, breaking the "chat closed → click bot to reopen" flow. Playwright test `matches the Codex shell geometry` fails with `chatBotToggle.click()` timeout.

**Root cause (deeper):** the overflow only happens when `chatOpen=true` but the viewport is too narrow to accommodate the 320px chat rail. `AppShell.vue` only checks `window.innerWidth` in `onMounted` — it does NOT listen to `resize`. So if the user loads at 1280px (chat auto-opens), then drags the window to 800px, `chatOpen` stays `true`, the 320px rail is forced into the layout, and the header copy overflows into the compressed center zone.

**Fix — resize listener, not CSS clipping (verified in blogV2 Aug 30 2026):**

```ts
let chatManuallySet = false

const syncPanelWithViewport = () => {
  if (window.innerWidth < 760) {
    sidebarOpen.value = false
    if (!chatManuallySet) chatOpen.value = false
  } else if (window.innerWidth < 1120) {
    if (!chatManuallySet) chatOpen.value = false
  }
}

const toggleChat = () => {
  chatOpen.value = !chatOpen.value
  chatManuallySet = true
}

onMounted(() => {
  syncPanelWithViewport()
  window.addEventListener('resize', syncPanelWithViewport)
})

onUnmounted(() => {
  window.removeEventListener('resize', syncPanelWithViewport)
})
```

And in the template: `@toggle-chat="toggleChat"` instead of `@toggle-chat="chatOpen = !chatOpen"`.

**Key points:**
- **Do NOT use `overflow: hidden` on `.topbar-end` or `.chat-panel-header`** — it clips the bot toggle. The toggle must remain visible and clickable when chat is closed.
- **`chatManuallySet` flag:** once the user manually toggles chat, stop auto-syncing on resize. Otherwise the user's explicit open gets overridden by a resize event.
- **Thresholds:** `< 760px` closes both sidebar and chat; `< 1120px` closes only chat. These match blogV2's existing breakpoints.
- **Verification:** `npm run typecheck` + `npx playwright test tests/e2e/blog.spec.ts` must pass. The test `matches the Codex shell geometry` is the canary — it clicks the bot toggle to reopen chat, which fails if the toggle is clipped.

**Anti-pattern:** don't try to fix this with CSS alone (`overflow: hidden`, `max-width`, `text-overflow: ellipsis`). The root cause is a state-management gap (no resize listener), not a styling issue. CSS clipping treats the symptom and breaks the toggle.

**Workflow lesson (same as Pattern 23):** "currently renders fine on my machine" is not a resolution. The user's screenshot showed a real broken state at ~800px viewport. The fix is to make the layout resilient to that viewport, not to say "it looks fine at 1280px."

**User's structural preference (blogV2, Aug 30 2026):** when the resize-listener fix was followed by a structural refactor (moving panel topbars into the panels themselves), the user explicitly rejected it: "换个思路，还是用之前的那种顶部栏和正文上下两部分，正文分为左中右三部分". The user prefers the original single-topbar structure. Do NOT refactor the shell layout — fix the state management (resize listener) instead.

## Pattern 26 — Shell layout: structural refactor was rejected — prefer minimal state fixes over DOM restructuring

**Symptom:** a three-column shell (sidebar / main / chat) has a single topbar with three zones (start / center / end). The end zone contains chat header content that overflows into the center zone when the layout is compressed or state gets out of sync.

**Root cause (initial diagnosis):** the topbar's left/right zones are independent elements with their own width calculations, separate from the panels below. When states diverge, content overflows.

**Structural refactor attempt (rejected by user, blogV2 Aug 30 2026):** moved each panel's topbar into the panel itself (sidebar-topbar, chat-topbar), stripping TopBar to center-only. This eliminated the sync issue structurally but introduced new problems:
- When both panels closed, no toggle buttons remained visible to reopen them
- User explicitly rejected: "换个思路，还是用之前的那种顶部栏和正文上下两部分，正文分为左中右三部分"
- E2E tests broke because they referenced the old DOM structure

**User's preferred model:** single topbar spanning full width, with left/center/right zones. Left zone = sidebar toggle (when sidebar closed, button is in topbar; when open, button is "wrapped" inside sidebar). Right zone = chat toggle (when chat closed, button is in topbar; when open, chat panel "pushes" the topbar's right zone out of its space).

**Correct fix (Pattern 25, verified):** keep the original single-topbar structure. Add a `resize` event listener to auto-close panels when viewport is too narrow. Do NOT restructure the DOM.

**Key lesson:** when the user reports a layout bug, the first instinct should be to check if it's a **state management issue** (missing resize listener, stale boolean) before attempting a **structural refactor**. The user prefers minimal, targeted fixes that preserve the existing DOM structure and interaction patterns. Structural changes that alter the visual hierarchy or remove familiar toggle buttons will be rejected even if they "fix" the root cause.

**Anti-pattern:** don't refactor the shell layout to "solve" a sync issue. The user has a clear mental model of how the layout should work (single topbar, panels below). Respect that model and fix the state management instead.

The full structural refactor attempt + rejection detail (blogV2, Aug 30 2026) is in `references/shell-topbar-structural-refactor-2026-08-30.md`.

## Pattern 27 — Panel toggle buttons must remain accessible when panels are closed

**Symptom:** after moving panel toggle buttons from a shared topbar into the panels themselves (as part of a structural refactor), closing a panel also hides its toggle button — leaving no way to reopen it.

**User report (blogV2, Aug 30 2026):** "这下左右两边的侧边栏关上后没有点击打开的按钮了"

**Root cause:** the toggle button was moved inside the panel's own topbar (e.g. `sidebar-topbar`, `chat-topbar`). When the panel collapses (`width: 0`), its topbar collapses too, taking the toggle button with it.

**Fix — keep toggle buttons in the shared topbar, not inside the panels:**

The shared topbar (`.topbar`) should always contain:
- Left side: sidebar toggle button (PanelLeft icon)
- Center: breadcrumbs, search, tools
- Right side: chat toggle button (Bot icon)

When a panel is open, its own topbar (inside the panel) can show panel-specific content (e.g. "对话 / 未配置" for chat). But the **toggle button to open/close the panel must always be in the shared topbar**, accessible regardless of panel state.

**Layout model (user's explicit preference):**
```
┌─────────────────────────────────────────────────┐
│ [◀] [sidebar toggle] [search] [tools] [chat toggle] │  ← shared topbar, always visible
├──────────┬──────────────────────────┬───────────┤
│ sidebar  │ main                     │ chat      │
│ (own     │ (own topbar              │ (own      │
│  topbar) │  = shared topbar)        │  topbar)  │
└──────────┴──────────────────────────┴───────────┘
```

- When sidebar is closed: sidebar toggle button is visible in the shared topbar (left side)
- When sidebar is open: sidebar panel appears, and the toggle button is "wrapped" inside it (or remains in the shared topbar — user accepted both)
- When chat is closed: chat toggle button is visible in the shared topbar (right side)
- When chat is open: chat panel appears, and the shared topbar's right zone is "pushed out" of the chat panel's space

**User's precise description of the chat-open behavior (blogV2, Aug 30 2026):** "机器人图标所在的方框延长，把工具栏顶出右侧栏的范围" — the bot icon's container extends rightward into the chat panel's space, pushing the topbar's right zone (with "对话/未配置") out to become the chat panel's own topbar. The shared topbar's right zone and the chat panel's topbar are the same visual element — they must align perfectly (same width, same background, same left border) so the transition is seamless. The search bar in the center zone should shrink to make room, not be overlapped.

**Anti-pattern:** don't move toggle buttons into the panels themselves. A toggle button must always be reachable, even when the panel it controls is hidden.

**E2E canary:** the test `matches the Codex shell geometry` clicks the chat bot toggle to reopen chat after closing it. If the toggle is hidden inside a collapsed panel, this test fails with a timeout.

The toggle-button restoration detail (blogV2, Aug 30 2026) is in `references/shell-toggle-button-restoration-2026-08-30.md`.
The chat panel遮挡工具栏 issue + `chatManuallySet` refinement needed (blogV2, Aug 30 2026) is in `references/chat-panel-topbar-overlap-2026-08-30.md`.

## Pattern 28 — Multi-view side panel: icon bar + content switching

**Symptom:** a single-purpose side panel (e.g. chat) needs to expand into a multi-view panel (chat / outline / comments) with an icon bar for switching, similar to VS Code's Activity Bar.

**Design decisions (verified in blogV2, Aug 30 2026):**

1. **Keep the shared topbar structure** — the icon bar lives in the topbar's right zone (`.topbar-end`), not inside the panel itself. This preserves the existing shell topology the user prefers (see Pattern 26).
2. **Panel content switches, panel container stays** — the `.side-panel` wrapper remains in the DOM with its width transition; only the inner content component changes (`v-if="sidePanelView === 'chat'"` etc.). This avoids layout shift and preserves the collapse animation.
3. **Default open with view memory** — `sidePanelOpen` defaults to `true` (preserving previous chat default), and `sidePanelView` remembers the last active view. Clicking the active icon closes the panel; clicking a different icon switches content while keeping it open.
4. **Padding compensation for closed state** — when the panel closes, `.topbar-center` must reserve enough `padding-right` for the icon bar (~116px for 3×32px icons + gaps), otherwise the icons overlap the view-switch toolbar buttons.

**Component structure:**
```vue
<!-- TopBar.vue: icon bar in topbar-end -->
<div class="topbar-end" :class="{ 'topbar-end--rail': sidePanelOpen }">
  <SidePanelHeader :open="sidePanelOpen" :active-view="sidePanelView"
    @toggle="toggleSidePanel" @update:active-view="sidePanelView = $event" />
</div>

<!-- AppShell.vue: panel content switches -->
<aside class="shell-panel side-panel" :class="{ 'shell-panel--closed': !sidePanelOpen }">
  <ChatPanel v-if="sidePanelView === 'chat'" ... />
  <OutlinePanel v-else-if="sidePanelView === 'outline'" ... />
  <CommentsPanel v-else-if="sidePanelView === 'comments'" ... />
</aside>
```

**Key CSS:**
```css
.topbar-center { padding: 0 116px 0 228px; }  /* reserve space for icon bar when closed */
.topbar-center--side-panel-open { padding-right: 12px; }
```

**Pitfalls:**
- Don't move the icon bar into the panel itself — when the panel closes (`width: 0`), the icons disappear with it (see Pattern 27).
- Don't forget to reserve `padding-right` on `.topbar-center` for the closed state — the icons remain visible even when the panel is collapsed, and they will overlap center content if padding is insufficient.
- Keep the floating outline (FloatingOutline) visible when the side panel shows chat or comments, but hide it when the side panel shows outline — otherwise two outlines compete for the same screen edge.

**Verification:** use `browser_console` to measure `getBoundingClientRect()` on `.view-switch` and `.side-panel-header__icon` — the first icon's `left` must be greater than `viewSwitch`'s `right` when the panel is closed.

The multi-view side panel implementation (blogV2, Aug 30 2026) is in `references/side-panel-multi-view-2026-08-30.md`.
The FloatingOutline per-section popover rewrite — rail always visible, hover shows per-section detail card (blogV2, Aug 30 2026) — is in `references/floating-outline-section-popover-2026-08-30.md`.

## Pattern 30 — In-place morph CSS: hide the trigger, show the replacement at the same anchor

**Symptom:** after adding a proper panel for content (e.g. TOC moved into a side panel), the small hover indicator (dash rail) should expand *in place* into the full list instead of popping an adjacent floating card. First attempt edits the CSS but the user reports "没生效" — the old popup card still appears.

**Root causes (two compounding):**
1. **Leftover conflicting rule.** The old floating-card CSS included a rule like `.parent:is(:hover, .open) .trigger { z-index: 1; pointer-events: none; }` which is compatible with the floating-card model (trigger stays rendered under the card). After switching to in-place morph, this rule conflicts with the new `.trigger { display: none }` — CSS specificity may keep the trigger visible, or the trigger's hit area blocks the expanded content.
2. **Absolute positioning residue.** The old card used `position: absolute; top: 50%; right: 4px; transform: translateY(-50%)` to float next to the trigger. The new expanded content must use `position: relative` so it occupies the trigger's own slot in the layout — otherwise it still floats beside the (now-hidden) trigger and looks identical to the old popup.

**Fix — three coordinated edits:**
```css
/* 1. Hide the trigger when expanded */
.parent:is(:hover, .open) .trigger { display: none; }

/* 2. Show the expanded content in normal flow at the same anchor */
.parent:is(:hover, .open) .expanded-content {
  display: flex;
  position: relative;         /* was: absolute + transform */
  /* remove: top/right/transform — let it sit where the trigger was */
}

/* 3. DELETE any leftover trigger-styling rules from the floating-card era */
/* e.g. remove: .parent:is(:hover, .open) .trigger { z-index: 1; pointer-events: none; } */
```

**Also strip the heavy popup styling** — the old floating card often has `backdrop-filter: blur(20px)`, `box-shadow: 0 16px 36px ...`, gradient backgrounds. In-place morph should look like part of the page, not a modal: `background: var(--canvas)`, `box-shadow: 0 4px 12px rgb(... / 8%)`, no backdrop-filter.

**Verification habit:** after the patch, `curl` the dev server's compiled CSS for the component (find the `data-v-*` hash from the served HTML, then fetch the `/_nuxt-dev/components/.../Foo.vue?vue&type=style&...` URL) and `grep` for both the new rules AND the absence of the old conflicting selectors. Source-only verification is not enough — Nuxt's hot-reload can leave stale rules in the served CSS (see Pattern 9).

**Session example (blogV2, Aug 30 2026):** FloatingOutline hover was converted from a floating card beside the dash rail to an in-place expansion replacing the rail. Initial patch missed the leftover `.outline-rail { z-index: 1; pointer-events: none; }` rule; user reported "没生效" until the rule was deleted. The served CSS check confirmed the new rules were present but were being overridden by the leftover.

## Pattern 31 — Nuxt dev cache corruption: restart the server, do NOT delete `.nuxt` or `.data`

**Symptom:** dev server log shows `Restarting Nuxt due to error: SqliteError: UNIQUE constraint failed: _development_cache.__hash__` and the user reports the site is broken or behaving strangely. Tempting fix: `rm -rf .nuxt .data .output` to "clear the cache."

**Root cause of the follow-up failure:** deleting `.nuxt/` while a fix-up restart is needed produces a worse error — `worker entry not found in ".../.nuxt/dev/index.mjs"` with HTTP 500 on every route. The Nitro dev server needs its build artifacts regenerated in the correct order, and a partially-deleted `.nuxt` tree breaks the worker bootstrap. The SqliteError itself is a Nuxt Content dev-cache uniqueness violation that resolves on a clean process restart — the cache file is recreated on boot.

**Fix — restart only, never delete:**
```bash
# 1. Kill the running dev server (via process tool or kill PID)
# 2. Restart: npm run dev (background, watch for "Local:")
# 3. Verify: curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:<port>/<route>
```

If you already deleted `.nuxt` or `.data` and are now getting `worker entry not found` 500s: restore from a backup if you made one (`mv .data.bak .data; mv .nuxt/content.bak .nuxt/content`), then kill + restart. If no backup, a full `rm -rf .nuxt && npm run dev` will eventually regenerate everything, but expect a slow first boot and possible type regeneration.

**Anti-pattern:** do not treat Nuxt dev-cache errors like node_modules corruption. `.nuxt` is not disposable mid-session the way `node_modules/.cache` is — the dev server holds open handles and expects specific files to exist across HMR restarts.

**Key lesson:** when the dev server logs a SqliteError but `curl` still returns 200, the user-visible symptom is often just a stale hot-reload state, not a broken server. Restart first; delete caches only as a last resort and never while the server is running.

## Pattern 29 — Cross-directory file operations: verify target path before writing

**Symptom:** after creating or modifying files, `ls` shows the directory is empty or files are missing, but `write_file` reported success. The project builds fine, but the files seem to "disappear" on subsequent checks.

**Root cause:** the agent's current working directory (cwd) differs from the project root. `write_file` resolves relative paths against the agent's cwd, not the project directory. When the agent later runs `ls` or `git status` from the project directory, the files are "missing" because they were written to a different location entirely.

**Fix — always verify the target path before writing:**
1. `pwd` — confirm the current working directory.
2. If the target is a project file, use an absolute path or `cd` to the project root first.
3. After `write_file`, immediately verify with `ls -la <absolute-path>`.

**Anti-pattern:** don't assume `write_file` with a relative path like `./app/components/...` will land in the project directory. The agent's cwd may be a workspace, home directory, or another project entirely.

**Session example (blogV2, Aug 30 2026):** agent created SidePanelHeader.vue, OutlinePanel.vue, CommentsPanel.vue, and AppShell.vue in `~/.openclaw/workspace-chouno_hina/app/components/` instead of `/Users/songkuakua/Documents/code/Codex-Blog-AI-Chat/blogV2/app/components/`. The files were "lost" until a `find` command located them. The fix was to copy them to the correct project directory with `cp`.

**Key lesson:** when `write_file` succeeds but `ls` shows nothing, the first check should be `find / -name "<filename>" 2>/dev/null | head -5` — not "the file was deleted by another thread."

## Pattern 32 — Per-item hover popover: each trigger reveals its own content card

**Symptom:** a rail of small indicators (dash per section) should show a popover with *that specific item's* details on hover (title + sub-items), not a shared full list. This is the "Level 2" case from Pattern 1.

**Implementation (verified in blogV2 FloatingOutline rewrite, Aug 30 2026):**

1. Track `hoveredRuleId` (per-item), not a single boolean.
2. Bind `@mouseenter="hoveredRuleId = link.id"` on each `<li>` wrapper (NOT on the tiny `<button>` rule itself — the li is the larger hit area), and `@mouseleave="hoveredRuleId = null"` on both the li and the outer `<nav>`.
3. Render the popover with `v-if="popoverLink"` inside a `<Transition name="popover">`, positioned `absolute; top: 50%; right: <rail-width + gap>px; transform: translateY(-50%)` relative to the `.outline` nav.
4. Popover content: section title (`h3`, 13px/600) + list of children as clickable items. Clicking a child scrolls to it AND clears `hoveredRuleId` so the popover closes.
5. Keep the rail visible at all times — do NOT hide it when a separate side panel shows the same content (user correction: "不管右侧目录栏有没有打开都要有那些横线"). Remove conditions like `v-if="sidePanelView !== 'outline'"` from the parent.

**Key CSS:**
```css
.outline-popover {
  position: absolute;
  top: 50%;
  right: 30px;             /* rail width + small gap — user said 42px felt "离右侧有点远" */
  transform: translateY(-50%);
  width: max-content;
  min-width: 180px;
  max-width: 280px;
  background: var(--canvas);
  box-shadow: 0 8px 24px rgb(31 35 40 / 12%), 0 2px 6px rgb(31 35 40 / 6%);
}
.popover-enter-from, .popover-leave-to { opacity: 0; transform: translateY(-50%) translateX(4px); }
```

**Proximity preference (user feedback):** the rail itself sits `right: 8px` from the content edge (was 20px — "横线离右侧有点远了"), and the popover gap from the rail should be small (~4-12px, not 20px+). Hover UI should feel attached to its trigger, not floating far away.

**Interaction evolution note:** this supersedes the "in-place morph of the full list" approach from Pattern 1 Level 1 for cases where per-item detail is wanted. The user moved to per-item popovers once the full TOC moved into the side panel — the rail's job changed from "expand to full list" to "preview one section". Both patterns are valid; pick based on whether the revealed content is shared (→ pure CSS morph) or per-trigger (→ JS hoveredId + Transition).

## Pattern 33 — When a reference image fails to analyze, ask for a description instead of guessing

**Symptom:** user sends a reference screenshot for a UI style, but `vision_analyze` returns an unrelated description (wrong image content) or errors. Agent proceeds to implement based on a guess; user replies "理解不对" — two wasted iterations.

**Fix — stop and ask after ONE failed analysis:**
1. If the first `vision_analyze` result clearly doesn't match the user's description (e.g. user says "目录卡片样式" but analysis describes an AI chat log), don't retry the same call hoping for a better result, and don't implement from imagination.
2. Tell the user the image didn't come through clearly and ask 2-3 targeted questions: "卡片显示的是当前章节标题+子章节列表，还是完整目录？" / "卡片在横线左边弹出，还是原地展开？"
3. Only implement after the user confirms the interaction model in words.

**Anti-pattern:** analyzing the same broken image twice, then guessing the design from the user's one-line description. The user's mental model ("类似这样" + image) is in the image — if you can't see it, you don't have the spec.

**Related lesson — "没生效" ambiguity:** when the user reports a change "没生效", before re-editing, check whether the component is even rendered in the current state (e.g. a parent `v-if` hides FloatingOutline when the side panel is open). Ask "是在侧边栏关闭时看到的，还是打开时？" if the visibility depends on app state. In the Aug 30 session, the floating outline was intentionally hidden while the outline side panel was open — the user's "没生效" was actually about a state where the component never mounted.

The topbar chat header overflow investigation (blogV2, Aug 30 2026) is in `references/topbar-chat-header-overflow-2026-08-30.md`.
The resize-listener fix for the same issue (blogV2, Aug 30 2026) is in `references/topbar-chat-header-overflow-resize-fix-2026-08-30.md`.
The structural refactor attempt + rejection detail (blogV2, Aug 30 2026) is in `references/shell-topbar-structural-refactor-2026-08-30.md`.
The toggle-button restoration after the rejected refactor (blogV2, Aug 30 2026) is in `references/shell-toggle-button-restoration-2026-08-30.md`.

The exact FloatingOutline.vue + AppShell/motion.css fix (blogV2, Aug 2026) is captured in `references/floating-outline-hover-card.md`.
The DocumentComments selection-trigger popover pattern + sizing preferences (same session) is in `references/selection-action-popover.md`.
The current FloatingOutline implementation state + "不够好看" feedback analysis (blogV2, Aug 25 2026) is in `references/floating-outline-current-state-2026-08-25.md`.
The click-target + scroll-passthrough fix for the same component (blogV2, Aug 25 2026) is in `references/floating-outline-click-scroll-fix-2026-08-25.md`.
The flex-button text-alignment pitfall (`justify-content: flex-end`) discovered during the same session is in `references/floating-outline-flex-alignment-fix-2026-08-25.md`.
The Nuxt hot-reload failure + card width issue (stale `data-v-*` hash) from the same session is in `references/floating-outline-width-hotreload-2026-08-25.md`.
The multi-thread conflict false alarm + hover-state verification lesson (blogV2, Aug 26 2026) is in `references/floating-outline-multithread-verification-2026-08-26.md`.
The workspace-root redirect fix for split song/mine workspaces (blogV2, Aug 26 2026) is in `references/workspace-root-redirect-2026-08-26.md`.
The sidebar utility footer proportion unification (blogV2, Aug 26 2026) is in `references/sidebar-utility-footer-proportion-fix-2026-08-26.md`.
The sidebar utility footer equal-width icon buttons (blogV2, Aug 26 2026) is in `references/sidebar-utility-footer-equal-width-buttons-2026-08-26.md`.
The sidebar utility row inline merge — moving theme toggle + social links from a separate footer into a 4th navigation row (blogV2, Aug 26 2026) — is in `references/sidebar-utility-row-inline-merge-2026-08-26.md`.
The sidebar layout order swap — navigation above article area, utility row stays at top of article area (blogV2, Aug 26 2026) — is in `references/sidebar-layout-order-swap-2026-08-26.md`.
The search bar path-segment badges + pre-refactor color restoration via `git show` (blogV2, Aug 26 2026) is in `references/search-bar-path-badges-color-restore-2026-08-26.md`.
The search bar path badges hide/show on typing with Transition animation (blogV2, Aug 26 2026) is in `references/search-bar-path-badges-hide-show-animation-2026-08-26.md`.