# Sidebar Layout Order Swap (blogV2, 2026-08-26)

## Session context

User had accepted the utility row (theme + social icons) being placed at the top of the article navigation area (see `sidebar-utility-row-inline-merge-2026-08-26.md`). But after seeing it live, they realized the **order was wrong**: the navigation (Home / Musings / Projects) was at the bottom and the utility row was at the top. They wanted the reverse.

User's exact words: "反了，上面的在下面，下面的在上面" (with screenshot showing utility row on top and nav on bottom).

## What changed

### Before (rejected)
- `ProjectSidebar.vue` rendered: `<SidebarNavigation />` (bottom) → `<div class="sidebar-scroll-wrap">` with `<ArticleNavigation />` inside (top, containing utility row).
- Visual order: utility row → article tree → navigation.
- The utility row was inside `ArticleNavigation.vue`, which is inside the scrollable area.

### After (accepted)
- `ProjectSidebar.vue` renders: `<SidebarNavigation />` (top) → `<div class="sidebar-scroll-wrap">` with `<ArticleNavigation />` inside (bottom, still containing utility row at its top).
- Visual order: navigation → utility row → article tree.
- The border between navigation and article area changed from `border-top` to `border-bottom` on `.sidebar-navigation`.

## Key structural detail

```vue
<template>
  <nav class="project-sidebar" aria-label="Projects">
    <SidebarNavigation
      :modules="props.navigationModules"
      :active-module-id="props.activeModuleId"
    />
    <div class="sidebar-scroll-wrap">
      <div class="sidebar-scroll codex-scroll">
        <ArticleNavigation ... />
      </div>
    </div>
  </nav>
</template>
```

```css
.project-sidebar > :deep(.sidebar-navigation) {
  flex-shrink: 0;
  border-bottom: 1px solid var(--line);  /* was border-top */
  padding-top: 8px;
  padding-bottom: 8px;
}
```

## Why this works

- `ProjectSidebar` is a flex column (`display: flex; flex-direction: column`). The first child is at the top.
- Moving `<SidebarNavigation />` above the scroll wrapper puts it at the top of the sidebar.
- The utility row remains at the top of `ArticleNavigation` (inside the scroll area), so it appears right below the navigation.
- `border-bottom` on `.sidebar-navigation` creates the separator line between nav and article area.

## User taste notes

- "反了，上面的在下面，下面的在上面" — the user has a clear mental model of the sidebar's visual hierarchy: primary navigation first, then utility, then content tree.
- When a layout feels "wrong" after a merge, the fix is often just reordering siblings in the parent component, not redesigning the merged component.
- The utility row's position is tied to the article tree (it's the "toolbar" for the article section), not to the navigation.

## Files touched

- `app/components/navigation/ProjectSidebar.vue` — reordered `<SidebarNavigation />` and `<div class="sidebar-scroll-wrap">`; changed `border-top` to `border-bottom` on `.sidebar-navigation`.

## Verification

- `npm run typecheck` → 0 errors.
- Browser snapshot confirmed: navigation (Home/Musings/Projects) appears before article region in the DOM order.
