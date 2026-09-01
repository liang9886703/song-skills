# Session decisions and implementation lessons

## Source project

- Target repository: `/Users/songkuakua/Document/code/Codex-Blog-AI-Chat`
- Existing implementation: React + Vite + TypeScript.
- Existing content was hard-coded in `src/data/posts.ts`; the migrated surface keeps the three-pane layout, top bar, document sidebar, reader, and chat placeholder.
- The target is Nuxt 4 + Vue 3, not a parallel replacement project.

## Confirmed content contract

- Content root: `/Users/songkuakua/Documents/code/computer-science`.
- Semantic path: `system/project/collection/file.md`.
- `system` is the top-left selector and must include `song`, `game`, and `mine`.
- Markdown uses YAML Front Matter with title/slug/tags/summary/dates/draft and optional related fields.
- Relative Markdown links are resolved from the `computer-science` root contract, not from browser filesystem access.
- Production-like local operation must watch Markdown changes, not only Nuxt development HMR.
- Frontend queries Nuxt server APIs; it never traverses the filesystem directly.
- Local Markdown is the active provider. Supabase is a repository seam, not a required online dependency in this phase.
- Login, multi-user behavior, comments, likes, and real AI Chat are out of scope; preserve Chat as a non-blocking UI placeholder.

## Compatibility policy

The verified content root currently contains shallower legacy paths rather than strict `system/project/collection/file.md` directories. The repository therefore supports strict four-level paths and a compatibility fallback that assigns legacy documents to `song` while preserving their real relative path. Do not silently invent or move the user's corpus during migration.

## Nuxt 4 migration lessons

- In a Nuxt 4 `app/` layout, `~/assets` resolves under `app/assets`; root-shared types are imported with `~~/shared/...` rather than `~/shared/...`.
- Replace the old Vite `tsconfig.json` with a Nuxt config extending `.nuxt/tsconfig.json`, and exclude the legacy React `src/**` and old Vite config from type checking while they are retained for reference.
- Old Vite/PostCSS config can break Vitest even when Nuxt builds correctly. Use a dedicated `vitest.config.ts` with a `tests/**/*.test.ts` include, and remove stale Tailwind/PostCSS plugin references when Tailwind is no longer in the dependency graph.
- `chokidar@4` does not support the old glob-pattern workflow. Watch the content root and filter ignored directories/non-Markdown files in the `ignored` callback; verify an actual file mutation against a running production build.
- Avoid serializing every document's raw Markdown and rendered HTML in the initial SSR payload. Return compact metadata for list/search queries and fetch the selected document by `path` as a detail query. This materially reduces initial HTML for a non-trivial corpus.

## Verification recipe

1. Run `npm test`, `npm run lint`, and `npm run build`.
2. Query `/api/content` against the verified content root and confirm a real document count.
3. Use a temporary strict four-level fixture to test Front Matter, tag filtering, full-text search, and relative links without modifying the user's corpus.
4. Start the production output with `NUXT_CONTENT_ROOT` pointing to the fixture, mutate a Markdown file, and query again without restarting; confirm title/tags change.
5. Open the built page in a browser and inspect the three-pane surface, not just the HTTP status.
