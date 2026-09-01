# Search Bar Path Badges + Color Restoration (blogV2, 2026-08-26)

## Context
User showed a screenshot of a bookmark-search input with two kbd-style badges on the right (`/` and `Tab`) and asked to restyle TopSearch.vue "in that style". After shipping literal kbd badges, user corrected: the badges in the reference actually represent the **current page path segments**, not keyboard shortcuts. User also noted the search bar's color "好像和之前不一样了" after a CSS-vars refactor.

## Correction 1 — Reference-image badges are path segments, not keyboard hints
**Symptom:** Agent interpreted the two right-side badges in the reference screenshot as literal keyboard shortcut hints (`/` and `Tab`) and rendered them as static `<kbd>` elements. User: "这个表示的是当前页面所在的路径".

**Fix — derive badges from `currentPath` prop:**
```vue
const pathSegments = computed(() =>
  props.currentPath ? props.currentPath.split('/').filter(Boolean) : []
)
```
```html
<div class="search-path" aria-hidden="true">
  <span v-for="(seg, i) in pathSegments" :key="i" class="path-segment">
    <span v-if="i > 0" class="path-sep">/</span>
    <span class="path-text">{{ seg }}</span>
  </span>
</div>
```
```css
.search-path { display: flex; align-items: center; gap: 2px; margin-left: auto; flex-shrink: 0;
               font-family: var(--font-mono); font-size: 11px; color: var(--ink-faint); }
.path-text { padding: 2px 6px; border: 1px solid var(--line); border-radius: 4px; background: var(--card-bg); }
```

**Lesson:** when a reference screenshot shows small kbd/badge-like elements in a UI, don't assume literal content — ask what they *represent* before hardcoding. Dynamic context (current path, active filters, workspace) is a more common meaning for such badges than static shortcut hints. If ambiguous, the first implementation should bind to dynamic data, not literal strings.

## Correction 2 — "Color is different": check git log for pre-refactor hardcoded values
**Symptom:** user says "这个搜索框的颜色好像和之前不一样了" after a theming refactor converted hardcoded colors to CSS vars.

**Fix — `git log` the file and restore the original literal values:**
```bash
git log --oneline -5 -- app/components/navigation/TopSearch.vue
git show <prev-sha>:app/components/navigation/TopSearch.vue | grep -A2 'search-wrap'
```
Found the pre-refactor values were hardcoded (not vars):
```css
.search-wrap { border: 1px solid #d5d9df; background: white; }
.search-wrap:hover, .search-wrap.focused { border-color: #b9c0c9; box-shadow: 0 1px 2px rgb(16 24 40 / 4%); }
```
vs the post-refactor:
```css
.search-wrap { border: 1px solid var(--line-strong); background: var(--card-bg); }
.search-wrap:hover, .search-wrap.focused { border-color: var(--ink-soft); box-shadow: var(--shadow-sm); }
```

**Lesson:** when user reports a subtle visual regression ("颜色不一样了", "看着不太一样"), don't guess new values — `git show <prev-sha>:<file>` to recover the exact previous literals. CSS-var refactorings often change effective values even when they claim to be pure renames (e.g. `--line-strong` ≠ `#d5d9df`, `--card-bg` ≠ `white` under certain themes). Restoring the exact previous value is faster than re-deriving it from a screenshot.
