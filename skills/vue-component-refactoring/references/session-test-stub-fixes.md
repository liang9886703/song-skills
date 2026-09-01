# Session: Test Stub and Assertion Fixes

## Context

After creating the side panel components (`SidePanelHeader.vue`, `OutlinePanel.vue`, `CommentsPanel.vue`) and updating `AppShell.vue` to use `onUnmounted`, two unit test failures appeared that were not directly caused by the new component logic but by test infrastructure gaps.

## Failure 1: Missing `onUnmounted` stub

**Error:**
```
ReferenceError: onUnmounted is not defined
 ❯ setup app/components/shell/AppShell.vue:117:1
```

**Root cause:** The test file `app-shell-module-controls.test.ts` stubbed `onMounted` but not `onUnmounted`. When `AppShell.vue` gained an `onUnmounted` call for cleanup, the shallow-mount environment no longer had that global available.

**Fix:**
```typescript
import { computed, onMounted, onUnmounted, shallowRef, useTemplateRef } from 'vue'
// ...
vi.stubGlobal('onUnmounted', onUnmounted)
```

## Failure 2: Missing child component stubs

**Error:**
```
[Vue warn]: Failed to resolve component: OutlinePanel
[Vue warn]: Failed to resolve component: CommentsPanel
```

**Root cause:** `AppShell.vue` now conditionally renders `OutlinePanel` and `CommentsPanel`, but the test stub map only included `ChatPanel`, `FloatingOutline`, `NavigationProjectSidebar`, and `NavigationTopBar`.

**Fix:** Add the new components to the `stubs` object:
```typescript
stubs: {
  ChatPanel: true,
  CommentsPanel: true,
  FloatingOutline: true,
  NavigationProjectSidebar: true,
  NavigationTopBar: TopBarStub,
  OutlinePanel: true,
},
```

## Failure 3: Brittle file-content assertion

**Error:**
```
AssertionError: expected '...' to contain '### 4.1 表 `app.workspaces`\n\n#### 职责'
```

**Root cause:** The test `article-reader-layout.test.ts` asserted on exact section numbers and heading text in `docs/storage/database-storage-plan.md`. That documentation file was rewritten by another session, changing section numbers and removing the expected headings.

**Fix:** Update assertions to match the current file content, and prefer stable markers (e.g. `CREATE TABLE app.workspaces`) over heading text that may change during documentation edits.

## Lesson

When adding new lifecycle hooks or child components to a Vue component, always check every test file that shallow-mounts it. The test environment is not auto-imported; it is manually stubbed, so any new global dependency must be explicitly declared.
