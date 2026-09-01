---
name: content-driven-nuxt-refactor
description: Use for Nuxt 4/Vue 3 local Markdown content refactors.
---

# Content-driven Nuxt refactoring

Use this class-level skill when an existing blog, knowledge-base, document reader, or agent/content UI must be refactored into Nuxt 4 + Vue 3 while preserving the existing visual language and making content data-driven.

## Core operating model

1. **Inspect before redesigning**
   - Read the target repository manifest, entrypoints, data modules, layout components, style tokens, and tests.
   - If the current repo is React/Vite but a companion project is the intended future Vue source, inspect both manifests and representative source files before choosing dependencies.
   - Treat an explicit user correction about the target stack as authoritative. Do not preserve React tooling merely because the intermediate prototype uses React.
   - Refactor the existing project path; do not create a parallel replacement unless explicitly requested.

2. **Preserve the product surface**
   - Keep the current layout geometry, pane topology, typography posture, spacing, colors, and interaction intent unless the user asks for a visual redesign.
   - Separate migration work from visual changes. First reproduce the existing UI in Nuxt/Vue, then move data and behavior behind stable interfaces.
   - Organize UI by responsibility: app shell, top bar, primary sidebar, document navigation, reader, outline, secondary/chat panel, and reusable primitives.
   - Extract palette, typography, spacing, borders, radii, and motion into configurable theme tokens rather than scattering values through components.

3. **Model documents as data**
   - Use a repository/provider boundary so the UI never directly traverses the filesystem.
   - Start with a local Markdown implementation; leave a compatible Supabase implementation seam for later.
   - Prefer an explicit interface such as `DocumentRepository` with methods for listing documents, reading one document, searching, filtering by tag, resolving related documents, and subscribing to changes.
   - Keep parsing, indexing, and rendering separate: filesystem adapter → Markdown/front-matter parser → normalized document index → Nuxt server/API → Vue composables/components.

## Default four-level content model

Unless the user specifies another mapping, use:

```text
content-root/
└── system/
    └── project/
        └── collection/
            └── document.md
```

Semantic levels:

- **System** — broad domain or knowledge space.
- **Project** — a concrete project or long-running subject.
- **Collection** — a blog series, topic group, or bounded set.
- **File** — the actual Markdown document and source of truth.

Do not invent a corpus path. Verify the absolute root and sample the actual extensions/structure before implementing ingestion. If the path is not known, ask for it instead of creating fake content.

## Markdown contract

Use YAML front matter for normalized metadata. A practical baseline is:

```md
---
title: RAG 架构设计
slug: rag-architecture
tags:
  - RAG
  - Agent
summary: 从原型到生产的 RAG 架构实践
createdAt: 2026-08-03
updatedAt: 2026-08-03
draft: false
related:
  - context-window
---

正文内容。
```

Rules:

- `title` falls back to the filename when absent.
- `slug` falls back to a stable path-derived identifier.
- `tags` are normalized for case-insensitive filtering while preserving display labels.
- File modification time can supplement or override `updatedAt` according to an explicit policy.
- Support relative Markdown links and explicit `related` IDs; resolve both to internal routes.
- Keep raw Markdown available for source/debug views while rendering sanitized HTML or Vue content safely.

## Local hot reload

For local development and local production-like operation:

1. Watch the verified content root on the server side.
2. On file add/change/delete, reparse the affected file and update the normalized index.
3. Notify the browser through Nuxt HMR or a lightweight server event mechanism.
4. Refresh the active document, tag results, sidebar tree, and search index without a full manual restart.
5. Start with a reliable full reindex fallback if incremental parsing fails; optimize only after measuring corpus size.
6. If using `chokidar@4`, watch the root directory and filter file types in `ignored`; do not rely on the removed v3 glob-pattern behavior.

Do not assume browser-side code can read arbitrary local files. Filesystem access belongs in Nuxt server routes/server utilities or a separately designed import process.

For large or moderately sized corpora, separate list and detail payloads: list/search endpoints should return metadata, while raw Markdown and rendered HTML should be fetched by document path. Otherwise SSR serializes the entire corpus into the initial page.

## Supabase seam

For the local-first release:

- Keep `LocalMarkdownRepository` as the active implementation.
- Define types and repository methods that a future `SupabaseDocumentRepository` can satisfy.
- Add a small Supabase client/config boundary only when requested; do not force online persistence into the first local-file release.
- Make the source of truth explicit to avoid silent conflicts between local files and Supabase rows.
- Reserve write APIs for document metadata, tags, collections, and future publishing workflows, but do not add authentication, multi-user behavior, comments, or likes unless requested.

## Basic blog capabilities for the first release

Prioritize:

- Home/recent document listing.
- Hierarchical sidebar navigation.
- Markdown rendering with code highlighting.
- Document detail route.
- Tags and tag filtering.
- Full-text search over title, summary, tags, and body.
- Related-document navigation.
- Draft/visibility metadata if useful for local content.
- File-change refresh.

Defer:

- Login and authorization.
- Multi-user collaboration.
- Comments, likes, follows, and social features.
- Complex CMS editing screens.
- Mandatory Supabase synchronization.
- AI chat integration unless it is already part of the preserved surface and can remain a non-blocking placeholder.

## Questions that materially change implementation

Resolve only these before coding if they are not inferable:

- Exact local content-root path.
- Whether the four-level directory shape is strict or allows shallower files.
- Front matter field names and date/draft policy.
- Relative-link syntax and whether `related` metadata is also required.
- Whether hot reload is development-only or must work in a local production process.
- Whether Supabase is only an interface seam or should be configured with a real schema/client now.
- Whether the existing chat panel remains a visual placeholder.

Use sensible defaults for everything else and record assumptions in the implementation plan.

## Verification

At minimum:

- Install dependencies and run the Nuxt typecheck/build.
- Exercise the local repository against real Markdown fixtures or the verified content root.
- Verify add/change/delete file events update the index.
- Verify tag search, full-text search, relative links, related documents, and four-level navigation.
- Verify the existing visual layout with a native browser check or screenshot.
- Confirm Supabase is not accidentally required when local mode is selected.

## Pitfalls

- Do not design the document schema from invented mock data or an unverified path.
- Do not treat a React prototype's hard-coded posts as the long-term domain model.
- Do not install React-specific tooling when the stated destination is Vue 3/Nuxt 4.
- Do not put filesystem traversal in Vue components or browser code.
- Do not collapse the four semantic levels into one flat `posts` array.
- Do not introduce authentication or social features merely because a typical blog has them.
- Do not claim hot reload after only proving that the initial page renders; test an actual file mutation.
- Do not assume `~/shared` points at the repository root in Nuxt 4; use the correct root alias (`~~`) or place shared code under `app/` deliberately.
- Do not leave the legacy Vite `tsconfig`, Vitest auto-discovery, or Tailwind/PostCSS references active after removing their dependencies; they can make Nuxt migration checks fail before new code is evaluated.
- Do not use a `**/*.md` watcher pattern with chokidar 4; watch the root and filter events.
- If the verified corpus is shallower than the target taxonomy, add an explicit compatibility mapping instead of silently relocating or fabricating documents.
- Keep list and document-detail payloads separate so SSR does not embed every article's source and rendered HTML.

## Reference

See `references/session-decisions.md` for the concrete project context, confirmed decisions, migration pitfalls, and verification recipe from the originating refactor discussion.
