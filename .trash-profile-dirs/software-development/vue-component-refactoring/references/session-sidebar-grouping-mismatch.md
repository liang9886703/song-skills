# Session: sidebar grouping/filter mismatch bug

## Problem

User reported: sidebar "Library" tree showed a `SKILLS` top-level book collection that was visible but could not be expanded/clicked.

## Root cause

Two functions in `app/utils/sidebar.ts` had mismatched exclusion logic:

- `groupArticleProjects` — grouped documents into top-level projects, did **not** exclude `skills` collection
- `groupArticleDocuments` — built folder trees inside a project, **did** exclude `skills` collection

Result: `SKILLS` appeared as a project node but had zero folders/documents underneath, making it appear "stuck" or unclickable.

## Fix

Applied the same exclusion filter to `groupArticleProjects`:

```ts
if (document.collection === 'skills' || document.collection.endsWith('--skills')) continue
```

## Verification

After the patch, the sidebar no longer renders a `SKILLS` project row. The dev server was already running with hot reload, so the change took effect immediately.

## Files touched

- `app/utils/sidebar.ts` — added `skills` exclusion to `groupArticleProjects`

## Related components

- `app/components/navigation/ArticleNavigation.vue` — consumes `groupArticleProjects`
- `app/components/navigation/ArticleFolderTree.vue` — consumes `groupArticleDocuments`

## Lesson

When multiple utility functions shape the same hierarchical UI data, any category exclusion must be applied consistently across all of them. A partial filter creates phantom nodes that confuse users.
