# Shell Topbar Structural Refactor (REJECTED) — blogV2, Aug 30 2026

## What Was Attempted

Moved each panel's topbar into the panel itself:
- `sidebar-topbar` inside sidebar panel (SystemMenu + toggle button)
- `chat-topbar` inside chat panel (ChatPanelHeader)
- Stripped `TopBar` to center-only content

## Why It Was Rejected

User explicitly said: "换个思路，还是用之前的那种顶部栏和正文上下两部分，正文分为左中右三部分"

Problems introduced:
1. **Toggle buttons disappeared when panels closed** — "这下左右两边的侧边栏关上后没有点击打开的按钮了"
2. E2E tests broke (referenced old DOM structure)
3. User preferred the original single-topbar structure

## What Was Kept Instead

The resize-listener fix (Pattern 25) was kept:
```ts
const syncPanelWithViewport = () => {
  if (window.innerWidth < 760) {
    sidebarOpen.value = false
    if (!chatManuallySet) chatOpen.value = false
  } else if (window.innerWidth < 1120) {
    if (!chatManuallySet) chatOpen.value = false
  }
}
```

Plus toggle buttons restored to the shared TopBar (see `shell-toggle-button-restoration-2026-08-30.md`).

## Lesson

**Do not refactor shell layout structure to fix state sync issues.** The user has a clear mental model:
- Single topbar spanning full width
- Left zone = sidebar toggle (always accessible)
- Center = breadcrumbs/search/tools
- Right zone = chat toggle (always accessible)
- Panels below have their own content

Structural changes that alter this hierarchy will be rejected. Fix the state management (add resize listeners, sync booleans) instead.
