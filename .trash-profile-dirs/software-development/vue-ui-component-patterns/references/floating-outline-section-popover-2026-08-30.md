# FloatingOutline per-section popover rewrite (blogV2, Aug 30 2026)

## Context

The side panel gained an outline view (Pattern 28). The FloatingOutline's role changed: the full TOC now lives in the side panel, so the floating rail no longer needs to expand into the full list. Instead, each dash shows a popover with that section's details on hover.

## User corrections during the session

1. **"由于侧边栏装目录了，现在目录栏弹卡片就没必要了"** — initial reading: remove the floating card. Agent first rewrote to in-place morph (Pattern 30), which was wrong.
2. **"理解不对，不管右侧目录栏有没有打开都要有那些横线，而且鼠标移到横线上，应该有我发你图片的那种这一章节的详细信息"** — the real spec: rail always visible (regardless of side panel state), hover shows per-section popover.
3. **"横线离右侧有点远了"** — rail `right: 20px → 8px`; popover `right: 42px → 30px`.

## Reference image failure

The user's reference screenshot (`image.png` from Discord CDN) failed vision analysis twice — returned a description of an unrelated dark AI-chat screenshot. Agent guessed the design twice and was corrected. Lesson captured in Pattern 33: ask for a verbal description after one failed analysis.

## Final implementation shape

`app/components/content/FloatingOutline.vue` (rewritten):

- Script: `hoveredRuleId: shallowRef<string | null>`, `popoverLink = computed(() => outlineLinks.find(l => l.id === hoveredRuleId))`, `getChildren(link)` returns `link.children ?? []`.
- Template: `.outline-rail` with `.outline-rules` (one `<li>` per depth-2 link; `@mouseenter`/`@mouseleave` on the li). Rule `<button>` keeps the distance-based width/color gradient. Popover in `<Transition name="popover">` with `v-if="popoverLink"`.
- Popover content: `h3.outline-popover__title` + `ul.outline-popover__list` of children as `<button class="outline-popover__item">` (active state via `child.id === activeId`), or `<p class="outline-popover__empty">暂无子章节</p>`.
- Click behaviors: rule click → `scrollTo(link)`; popover item click → `scrollTo(child)` + clears hover.

`app/components/shell/AppShell.vue`:

- Removed `&& sidePanelView !== 'outline'` from the FloatingOutline `v-if` — rail renders regardless of side panel view.

## CSS

```css
.outline { position: absolute; top: 50%; right: 8px; transform: translateY(-50%); }
.outline-popover {
  position: absolute; top: 50%; right: 30px; transform: translateY(-50%);
  width: max-content; min-width: 180px; max-width: 280px;
  max-height: calc(100vh - 120px); overflow-y: auto;
  border: 1px solid color-mix(in srgb, var(--line) 72%, transparent);
  border-radius: 10px; padding: 12px 14px;
  background: var(--canvas);
  box-shadow: 0 8px 24px rgb(31 35 40 / 12%), 0 2px 6px rgb(31 35 40 / 6%);
}
.outline-popover__title { margin: 0 0 8px; font-size: 13px; font-weight: 600; color: var(--ink); }
.outline-popover__item { width: 100%; padding: 4px 6px; font-size: 12px; color: var(--ink-faint); text-align: left; }
.outline-popover__item.active { color: var(--ink); background: var(--active); font-weight: 500; }
.popover-enter-from, .popover-leave-to { opacity: 0; transform: translateY(-50%) translateX(4px); }
```

## Tests rewritten

`tests/unit/floating-outline.test.ts` — all 12 old tests (full-list/compact-open model) replaced with 8 new ones: rail rule count, popover show/hide on hover, rule click navigation, popover item click navigation + close, active rule from scroll, transition-marker density, wheel forwarding. Full suite: 263/263 passed.

## Test rewrite caution

The old test file had a 40+-assertion "keeps the hover target active" test that hardcoded CSS strings from the old implementation (backdrop-filter, gradient, etc.). When rewriting a component's interaction model, rewrite its tests in the same commit — stale CSS-string assertions are the first thing that breaks and they encode the old design, not a contract.
