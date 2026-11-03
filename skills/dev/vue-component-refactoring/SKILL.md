---
name: vue-component-refactoring
description: Use when refactoring Vue/Nuxt components or UI panels.
---

# Vue Component Refactoring

Use this skill when refactoring Vue/Nuxt components, adding new UI panels, or modifying existing component hierarchies.

## Pre-work verification

**Always verify the actual project root before editing.** A session working directory may contain symlinks, mirrors, or stale copies that look like the project but are not the real source tree.

1. Run `git status` or `git log` to confirm the directory is a git repository with expected history.
2. Use `find` or `ls` to verify key project files exist (package.json, nuxt.config.ts, etc.).
3. If the path looks like a workspace or sandbox, search for the real project with `find /Users -name "package.json" -path "*/blogV2/*"` or similar.
4. Confirm the absolute path before any `write_file` or `patch` operation.

## Component creation checklist

When creating new Vue components:

- [ ] Place in the correct directory under `app/components/` following existing conventions
- [ ] Export types from the component file if they will be imported by parents
- [ ] Use `defineProps` and `defineEmits` with TypeScript types
- [ ] Add scoped styles with CSS custom properties from the design system
- [ ] Include accessibility attributes (aria-label, aria-pressed, etc.)

## State management for panels

When adding toggleable panels (sidebar, chat, outline, comments):

- Use `shallowRef` for open/closed state
- Track manual user toggles separately from automatic responsive behavior
- Emit events upward; don't manage panel state in child components
- Consider whether the panel should default open or closed based on prior UX

## Testing updates

After modifying components:

- Update unit tests to match new props/events
- Update E2E tests to match new DOM structure and CSS classes
- Run `npm run build` to verify no import or type errors
- Run `npm test` and `npm run test:e2e` to verify behavior

### Test stub completeness

When shallow-mounting a component that uses Vue composition API lifecycle hooks, the test file must stub **all** of them, not just the ones the original component used. If you add `onUnmounted` (or any other hook) to a component, every existing test that shallow-mounts it will fail with `ReferenceError: <hook> is not defined` until you add the corresponding `vi.stubGlobal`.

Checklist for new/modified components in tests:

- [ ] `computed`, `shallowRef`, `ref` — state primitives
- [ ] `onMounted`, `onUnmounted`, `onBeforeUnmount` — lifecycle hooks actually used
- [ ] `useTemplateRef` — if the component uses template refs
- [ ] Any custom composables the component calls (e.g. `useSelectedText`)
- [ ] New child components introduced in the template must be added to `stubs`

### Test assertion maintenance

Tests that assert on file contents (e.g. `expect(file).toContain('...')`) are brittle when the target file is edited by other sessions or refactors. When such a test fails:

1. Read the current target file to see what content actually exists.
2. Update the assertion to match the current content, not the old expectation.
3. If the test is checking a documentation file that is not tracked in git, consider whether the assertion is testing something durable or just session-specific text.

## Sidebar tree / grouping consistency

When a sidebar shows grouped navigation (projects → folders → documents), verify that **every grouping/filtering function applies the same exclusion rules**. A common bug is one function filtering out a category (e.g. `skills`) while another does not, producing a visible but empty/unopenable group.

Example pattern:

```ts
// BAD: groupArticleProjects includes 'skills', groupArticleDocuments excludes it
const projects = computed(() => groupArticleProjects(documents))
const folders = computed(() => groupArticleDocuments(documents.filter(...)))

// GOOD: both exclude the same categories
const projects = computed(() => groupArticleProjects(documents.filter(d => !isExcluded(d))))
const folders = computed(() => groupArticleDocuments(documents.filter(d => !isExcluded(d))))
```

Always trace the full data path: source → grouping → foldering → rendering. If a node appears in the UI but has no children, check whether the child-generation function filters differently.

## References

- `references/session-side-panel-refactor.md` — concrete example of workspace-vs-real-project confusion and how to recover.
- `references/session-test-stub-fixes.md` — how missing `onUnmounted` stubs and brittle file-content assertions break tests after component changes.
- `references/session-sidebar-grouping-mismatch.md` — sidebar tree bug where `groupArticleProjects` and `groupArticleDocuments` had mismatched exclusion rules, producing a visible but unopenable `SKILLS` node.

## Pitfalls

- Do not assume the current working directory is the project root.
- Do not create files in a workspace mirror and forget to copy them to the real project.
- Do not change component root element types (e.g. `<aside>` to `<div>`) without checking parent layout expectations.
- Do not remove CSS width/border constraints from a component without verifying the parent provides them.
- Do not forget to add new lifecycle hooks to test stubs; a missing `vi.stubGlobal('onUnmounted', onUnmounted)` breaks every shallow-mount test for that component.
