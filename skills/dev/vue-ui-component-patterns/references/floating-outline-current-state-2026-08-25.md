# Session detail: FloatingOutline current state + "不够好看" feedback (blogV2, 2026-08-25)

Repo: `/Users/songkuakua/Documents/code/Codex-Blog-AI-Chat/blogV2`
File: `app/components/content/FloatingOutline.vue`

## Current implementation (as of 2026-08-25)

The FloatingOutline component has two display modes driven by a container query (`@container reader (max-width: 1039px)`):

### Wide view (≥1040px)
- Shows `.outline-labels`: a vertical text list of section titles, right-aligned.
- Each item is a `<button>` with `max-width: 220px`, `font-size: 12.5px`, `color: var(--ink-faint)`.
- Active item: `color: var(--ink); background: var(--active); font-weight: 600`.
- **Problem:** the wide view is essentially invisible in the current layout because the article container is 736px wide, so the container query always resolves to "narrow".

### Narrow view (<1040px)
- Shows `.outline-rail`: a vertical stack of short horizontal dashes (22px wide column, 13px/22px line lengths).
- Active dash: longer (22px), darker (`var(--ink)`).
- On `.outline:hover`, the labels list appears as an absolutely positioned card:
  ```css
  position: absolute;
  top: 50%;
  right: 4px;
  transform: translateY(-50%);
  width: max-content;
  max-width: min(252px, calc(100vw - 40px));
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 6px;
  background: var(--card-bg);
  box-shadow: var(--shadow-popover);
  backdrop-filter: blur(10px);
  ```
- **Problem identified by user:** the hover card overlaps the Share button and article text. Position is the main complaint, not internal styling.

## User feedback pattern observed

User said: "博客项目里，现在正文的目录里，目录卡片等功能不够好看"

This is a **vague aesthetic complaint** without specific constraints. The agent's response pattern that worked:
1. Reproduce the current state in browser (took screenshots, checked computed styles).
2. Identify the concrete issues: (a) card overlaps Share button, (b) wide view never shows text labels due to container width, (c) overall visual is "too plain".
3. Offer **3 named variants** before writing code:
   - A: 精致卡片式 — wide view shows a polished floating card with title and better typography
   - B: 侧边栏融合式 — integrate TOC into the right margin like Notion, text right-aligned with left active indicator
   - C: 极简增强式 — keep dashes but improve hover card position and add micro-interactions

## Key layout measurements

- Article container width: 736px (always triggers "narrow" mode)
- Viewport width during test: 1280px
- Outline rail width: 38px
- Outline position: `absolute; right: 20px; top: 50%; transform: translateY(-50%)`
- The `.outline` is positioned relative to the article reader container, not the viewport.

## What the user has NOT yet chosen

The user had not selected a variant when the session was compacted. Next step on resumption: present the 3 variants and let them pick.

## Related session detail

Earlier iterations on this same component (Aug 24, 2026) are in `references/floating-outline-hover-card.md`. The user's established taste constraints from that session still apply:
- No title bar on hover cards
- Active item = bold + ink only, no dots/bars
- Width = max-content with min/max guards
- Subtle border, modest shadow
- In-place morph over adjacent popup
