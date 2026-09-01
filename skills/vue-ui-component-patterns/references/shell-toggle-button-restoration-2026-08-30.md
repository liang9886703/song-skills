# Shell Toggle Button Restoration — blogV2, Aug 30 2026

## Context

After the rejected structural refactor (moving panel topbars into panels), the user reported: "这下左右两边的侧边栏关上后没有点击打开的按钮了"

## Problem

The structural refactor moved toggle buttons from the shared `TopBar` into each panel's own topbar:
- Sidebar toggle moved from `TopBar.start` into `sidebar-topbar` (inside sidebar panel)
- Chat toggle moved from `TopBar.end` into `chat-topbar` (inside chat panel)

When panels collapsed (`width: 0`), their topbars collapsed too, hiding the toggle buttons.

## Fix

Restored toggle buttons to the shared `TopBar` while keeping panel-specific content in panel topbars:

### TopBar.vue changes
- Added `sidebarOpen` and `chatOpen` props
- Added `toggle-sidebar` and `toggle-chat` emits
- Added left toggle button (PanelLeft icon) and right toggle button (Bot icon) to the shared topbar
- Buttons remain visible regardless of panel state

### AppShell.vue changes
- Removed toggle button from `sidebar-topbar` (kept SystemMenu only)
- Removed toggle button from `chat-topbar` (kept ChatPanelHeader only)
- Passed `sidebar-open` and `chat-open` props to TopBar
- Wired `@toggle-sidebar` and `@toggle-chat` events

### Result
- Toggle buttons always accessible in shared topbar
- Panel topbars show panel-specific content when open
- No structural refactor needed

## User's Layout Model

```
┌─────────────────────────────────────────────────┐
│ [◀] [sidebar toggle] [search] [tools] [chat toggle] │  ← shared topbar
├──────────┬──────────────────────────┬───────────┤
│ sidebar  │ main                     │ chat      │
│ (SystemMenu)│ (shared topbar)      │ (对话/未配置)│
├──────────┤                          ├───────────┤
│          │                          │           │
│ content  │       content            │  content  │
│          │                          │           │
└──────────┴──────────────────────────┴───────────┘
```

- Shared topbar spans full width, always visible
- Each panel has its own topbar content when open
- Toggle buttons in shared topbar control panel visibility

## Verification

- `npm run typecheck` passes
- 12/12 e2e tests pass (including `matches the Codex shell geometry` which clicks the chat toggle to reopen)
