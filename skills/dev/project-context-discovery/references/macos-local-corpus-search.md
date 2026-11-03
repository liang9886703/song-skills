# macOS Local Corpus Search

A compact recipe for locating a user-described local document corpus without assuming the project workspace is the source.

## Search order

1. Exact indexed directory query:

```bash
mdfind 'kMDItemContentType == "public.folder" && kMDItemFSName == "computer"cd'
```

2. Case-insensitive wildcard query:

```bash
mdfind 'kMDItemFSName == "*computer*"cd'
```

3. Bounded recursive scan of likely roots (`Documents`, `Desktop`, `Downloads`, cloud roots). Only scan the whole home directory as a last resort; skip `Library`, dependency directories, and system paths where possible.

## Candidate validation

- Confirm `is_dir` and print the absolute path.
- Inspect parent and grandparent names to verify the described nesting.
- Count/sample files by extension rather than reading all content immediately.
- Separate actual corpus folders from source-code directories, app bundles, and system resources with similar names.

## Reporting a miss

State the exact roots and methods searched, then ask for an absolute path or the parent folder name. A no-result Spotlight lookup is not proof that the files are absent: removable volumes, iCloud placeholders, and unindexed locations can be invisible to it.

## Project implication

Do not make the Vue/TypeScript/Convex schema depend on an unverified corpus. Once found, treat filesystem traversal and parsing as a local importer/ingestion step; persist normalized document metadata and content in Convex, then have the Vue client query that normalized model.
