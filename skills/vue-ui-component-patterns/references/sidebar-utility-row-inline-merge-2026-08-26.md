# Sidebar Utility Footer → Inline Utility Row (blogV2, 2026-08-26)

## Session context

User rejected the separate bottom utility footer (theme toggle + X + LinkedIn + GitHub in a distinct `<footer>` component) and asked to move it into the sidebar navigation as a 4th row, visually identical to Home / Musings / Projects.

User's exact words: "把这一坨移到上面吧，和之前上面那部分一样" (with screenshot of the 3-row nav).

## What changed

### Before (rejected)
- `SidebarUtilityFooter.vue` — separate `<footer>` component with `border-top`, its own padding/gap, horizontal icon-only row.
- `ProjectSidebar.vue` rendered `<SidebarUtilityFooter />` below `<SidebarNavigation />`.
- Result: footer looked like a separate component, not part of the sidebar list.

### After (accepted)
- `SidebarUtilityFooter.vue` deleted; logic merged into `SidebarNavigation.vue`.
- `SidebarNavigation.vue` now renders a 4th `<li>` in the same `<ul class="module-items">`.
- The utility row uses the exact same CSS classes as navigation rows: `.module-row` (padding `5px 16px`, gap `10px`, font variables).
- Inside the row: theme button (Sun/Moon + label text) → divider (`1px × 16px`) → 3 social links (28×28px each).
- The utility row is a `<div class="module-row utility-row">`, not a `<button>` — because it contains nested interactive elements (social `<a>` links). The theme toggle is a nested `<button class="utility-theme-button">`.

## Key structural detail

```vue
<li>
  <div class="module-row utility-row">
    <button class="utility-theme-button" @click="toggleTheme">
      <Sun v-if="dark" :size="16" class="module-icon" />
      <Moon v-else :size="16" class="module-icon" />
      <span class="truncate">{{ dark ? '浅色' : '深色' }}</span>
    </button>
    <span class="utility-divider" aria-hidden="true" />
    <a v-for="item in socialLinks" class="utility-social" :href="item.href" target="_blank">
      <component :is="item.icon" :size="16" />
    </a>
  </div>
</li>
```

## Why this works

- Same `<ul>` container → same list semantics, same DOM depth.
- `.module-row` on the wrapper → identical padding, gap, font-size, line-height as nav rows.
- `.utility-theme-button` has `border: 0; background: transparent; padding: 0;` so it doesn't fight the row metrics.
- `.utility-social` links are `28×28px` with `border-radius: 6px` and hover background — compact but clickable.
- Divider is `width: 1px; height: 16px; margin: 0 2px; background: var(--line);` — subtle vertical separator.

## User taste notes

- "一行放 4 个" — the utility row must remain horizontal, not vertical stack.
- "把每个图标当成一个文字来看待" — icons should feel like characters in a line of text.
- "和之前上面那部分一样" — visual parity with navigation rows is the goal; the utility row should not stand out as a different component.
- The divider between theme toggle and social links is expected ("皮肤旁边那个横线应该有的").

## Files touched

- `app/components/navigation/SidebarNavigation.vue` — added theme state, utility row template + styles.
- `app/components/navigation/ProjectSidebar.vue` — removed `<SidebarUtilityFooter />` import and usage.
- `app/components/navigation/SidebarUtilityFooter.vue` — deleted (logic absorbed into SidebarNavigation).

## Verification

- `npm run typecheck` → 0 errors.
- Browser console confirmed: `totalRows: 4`, `hasUtilityRow: true`, `hasThemeButton: true`, `hasDivider: true`, `socialCount: 3`.
