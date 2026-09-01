---
name: project-context-discovery
description: Use when local project source files have an unclear path.
---

# Project Context Discovery

Use this skill before implementing a project whose target data, references, fixtures, or requirements are described as local files but whose exact path is unknown.

## Goals

- Resolve the real source path before making architecture or implementation claims.
- Distinguish a missing user-level precondition from an execution-level search problem.
- Never silently substitute the current workspace or `~/Documents` for an ambiguously described directory.
- Return a concrete path and a small inventory, or state exactly what path information remains missing.

## Workflow

1. **Normalize the description**
   - Extract likely path components, expected directory depth, case sensitivity, and file types.
   - Treat names such as “文档”, “资料”, and “computer” as clues, not guaranteed literal paths.
   - Preserve constraints such as “a `computer` folder inside a second-level folder”.

2. **Search likely roots first**
   - Check the current project root, home directory, `Documents`, `Desktop`, `Downloads`, cloud-drive roots, and explicitly named mounted volumes.
   - On macOS, use Spotlight (`mdfind`) for indexed searches, then a case-insensitive wildcard query if exact matching returns nothing.
   - Use a bounded recursive directory scan as fallback for unindexed locations. Exclude system and dependency trees unless explicitly requested.

3. **Validate candidates**
   - Confirm the candidate is a directory, not an application/resource path or similarly named source-code folder.
   - Check its parent and grandparent against the user's described layout.
   - Inventory representative files and extensions; do not claim to use the corpus until the path is verified.
   - Prefer a compact sample/count over dumping a large directory listing.

4. **Handle no-result searches correctly**
   - Retry with case-insensitive and wildcard matching.
   - Search for the parent folder name and likely alternate spellings.
   - Consider iCloud, mounted disks, messaging-app storage, and locations not indexed by Spotlight.
   - Do not conclude the data does not exist based on one root or one search mechanism.
   - Ask for the absolute path only after internal search paths are exhausted.

5. **Record implementation preconditions**
   - Before building ingestion/indexing, document the resolved corpus path, supported file types, nested-folder behavior, and whether files change over time.
   - If unresolved, stop corpus-dependent implementation and report the missing precondition plainly; never present fabricated sample data as the user's documents.

## Project handoff

Once verified, hand the implementation agent:

- absolute corpus path;
- parent/grandparent layout;
- file extension inventory and approximate counts;
- parsing and encoding concerns;
- whether to copy, watch in place, or import into the application database.

For a Vue 3 + TypeScript + Convex application, keep local discovery/import separate from the runtime UI. A local importer or one-time ingestion script should parse the corpus and write normalized records to Convex; the Vue client should query normalized records rather than directly traversing the filesystem.

## Pitfalls

- Do not assume `~/Documents` is the folder meant by “文档”.
- Do not treat a failed browser or Spotlight lookup as proof that the corpus is absent.
- Do not search only the workspace when the user refers to a user-level document collection.
- Do not report “not found” without naming the roots and search methods actually tried.
- Do not design the document schema from an unverified corpus.

## References

- `references/macos-local-corpus-search.md` — bounded macOS search and candidate-validation recipe.
