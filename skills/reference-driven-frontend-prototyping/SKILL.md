---
name: reference-driven-frontend-prototyping
description: Build frontend-only prototypes from multiple website references, where one reference supplies layout/interaction structure and another supplies visual tone/style tokens. Use for Vue/React/static frontend MVPs that must be real, runnable artifacts rather than design-only commentary.
---

# Reference-Driven Frontend Prototyping

Use this skill when the user wants to build a new frontend from website references, especially phrasing like:

- “主体布局像 A，整体元素风格像 B”
- “用 Vue3/React 实现前端，只做前端部分”
- “我想做一套自己的站/产品原型，参考这两个网站”
- “复刻这个结构，但不要照搬内容/品牌”

This is **not** pure pixel-perfect cloning. The references are design inputs; the deliverable is an original runnable prototype in the requested stack.

## Core mode

1. **Separate reference roles**
   - Layout reference: page topology, columns, scrolling model, pane behavior, information architecture.
   - Style reference: typography, density, borders, radii, color posture, motion restraint, interaction tone.
   - If roles are not explicit, infer only when obvious; otherwise ask one concise question.

2. **Honor the requested stack and scope**
   - If the user says “Vue3” or “frontend only,” build Vue3 frontend only.
   - Do not add backend, auth, persistence, database, live agent gateway, or deployment unless requested.
   - Use local mock data for chat, docs, tools, and sandbox status.

3. **Build a real artifact**
   - Create files under the user’s preferred work location (default `work/` when no path is given).
   - Use the actual stack build tooling (e.g. Vite + Vue3) instead of a one-off description.
   - Keep content realistic enough to evaluate layout, but mark strategic copy as draft/mock when it is not final.

4. **Verify with real output**
   - Install dependencies if needed.
   - Run the production build (`npm run build`, `pnpm build`, etc.).
   - Start a dev server only if useful, then verify it responds over HTTP.
   - If browser screenshot tooling is unavailable, do not claim visual verification; report build + HTTP verification and the exact limitation.

## Screenshot-led implementation corrections

When the user provides a screenshot of the target product surface, treat it as the primary specification for the **embedded product UI**, not merely as a loose inspiration. Extract and reproduce concrete geometry: pane ratios, toolbar height, scroll ownership, document column width, typography scale, component dimensions, border radius, padding, and card placement. Keep the user's previously established visual system (fonts, palette, blur, or effects) unless the user explicitly asks to replace it; combine screenshot geometry with those style tokens rather than switching wholesale to the screenshot's colors or fonts. If a prior prototype already exists, locate and modify that project instead of scaffolding a replacement.

### Preserve-and-tune visual systems

If the user asks for multiple visual references or skins, implement them as explicit, reversible theme classes/configurations with a visible toggle. Do not flatten one skin into grayscale when the requested change is only tonal cleanup. For color corrections, preserve hue families and assign one stable surface color per major region (sidebar, document, assistant); reduce gradients, opacity stacking, and blur before removing color. Keep existing fonts unless the user explicitly asks to change typography. Validate both skins after every style change, not only the default one.

When a user says one side of a split view is correct and the other is dirty, scope the correction to the named pane. Match the good pane's tonal family and use solid surfaces if the user rejects glassmorphism; do not redesign the whole page or replace the established palette.

## Extraction pattern without over-cloning

When using reference sites:

- Fetch and inspect static HTML/CSS when browser automation is unavailable.
- Extract broad cues: text hierarchy, colors, fonts, page topology, layout ratios, interaction intent.
- Avoid copying proprietary content, assets, or exact branded UI unless the user has rights.
- Transform the references into an original design system for the user’s product.

Useful cues to capture:

- Layout: number of panes, sticky/fixed behavior, scroll ownership, responsive collapse order.
- Typography: system vs custom fonts, headline weight, letter spacing, line-height.
- Surfaces: plain paper, cards, split panes, border strength, shadow usage.
- Interaction: hover subtlety, toggles, selected state, chat/composer behavior.

## Recommended implementation shape for knowledge + agent sites

For a three-pane “docs + article + agent” personal site:

- **Left:** collapsible document tree / table of contents / source graph.
- **Center:** readable article/document surface; this remains the source of truth.
- **Right:** agent conversation body with context card, message stream, composer, and future tool/sandbox hooks.
- **Responsive:** collapse left navigation first; on small screens, place chat after content or convert it into a drawer.
- **Visual posture:** quiet, text-first, low decoration, clear borders, subtle hover, no generic SaaS hero unless the surface is actually marketing.

## Existing-project and user-reference discipline

- Before scaffolding anything, inspect the current conversation/session context and search the expected workspace paths for an existing Vue project. If the user says “refactor,” modify that project rather than creating a parallel replacement.
- When the user identifies a local knowledge/data directory, use that directory as the source of truth. Inspect its actual structure and generate/import an index from real files; do not invent mock content or infer a folder name from an earlier ambiguous description.
- If a user’s own website is the visual reference, preserve the previously established layout while reusing its documented style cues (self-hosted fonts, palette, blur/glass surfaces). Treat the site-style reference as a design system input, not a reason to replace the existing information architecture.
- For screenshot requests, run both production/build verification and native browser verification. Return the concrete screenshot path using `MEDIA:` plus the artifact path, dev URL, DOM checks, and any visibility fallback; never claim a screenshot was delivered without a real file.

## Pitfalls

- Do not answer with only an architecture plan when the user asks to implement.
- Do not force pixel-perfect cloning when the user wants “layout from A + style from B.”
- Do not ignore a stack clarification; if the user says Vue3, switch to Vue3 immediately.
- Do not invent backend complexity for a frontend-only request.
- Do not claim browser/visual QA if browser automation timed out or was unavailable.
- Do not store the prototype at the repository root unless the user asked; default to `work/` for new artifacts.

## Completion report

Keep the final response compact and include:

- Artifact path.
- Dev URL if a server is running.
- What was implemented.
- Exact verification command and result.
- Any verification limitation.

- `references/vibecape-shloked-vue3-personal-site.md` — concrete session pattern for a three-pane Vue3 personal site.
- `references/knowledge-vault-refactor.md` — existing-project discovery, Markdown vault indexing, style continuity, and screenshot verification pattern.
- `references/songkuakua-personal-site-style.md` — user's own personal-site style tokens: embedded fonts, color palette, and glassmorphism/blur cues.
