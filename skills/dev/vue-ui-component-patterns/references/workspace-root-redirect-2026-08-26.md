# Workspace Root Redirect Fix — blogV2 (2026-08-26)

## Problem

After the "split blog into song/mine workspaces" refactor, clicking the "Mine" workspace in the system switcher redirected to `/song` instead of staying in `/mine`.

## Root Cause

In `app/pages/[system]/[[...path]].vue`, the module visibility check runs before any workspace-root handling:

```ts
if (!isModuleVisibleInSystem(system.value, activeModule.value.id, ARTICLE_MODULE_ID)) {
  // ... redirect to owning workspace
}
```

When `segments = []` (root path like `/mine`), `resolveModuleRoute` returns `homeModule`. But `home` is not in `mine`'s `navigationModuleIds` (`['tasks', 'bookmark', 'stars', 'tags']`). So `isModuleVisibleInSystem('mine', 'home', 'article')` returns `false`, and the code redirects to `song` (which owns `home`).

## Fix

Add a workspace-root redirect **before** the visibility check:

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

Key points:

- The `else if` is critical — without it, both `navigateTo` calls execute and the second one (to `/song`) wins.
- `navigationModuleIdsForSystem` must be imported from `~/modules/workspaces`.
- The redirect target is the first module in the workspace's `navigationModuleIds` array (for `mine`, that's `tasks`).

## Verification

1. `npm run typecheck` — passes.
2. `curl -I http://localhost:3000/mine` — should return 302 to `/mine/tasks` (not `/song`).
3. Browser: click "Mine" in system switcher → URL becomes `/mine/tasks`, sidebar shows tasks/bookmark/stars/tags.

## Files Changed

- `app/pages/[system]/[[...path]].vue` — added workspace-root redirect before module visibility check; added `navigationModuleIdsForSystem` to imports.
