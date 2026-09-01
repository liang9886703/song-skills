# Paired content records

## Canonical shape

A musing record may be stored as two files with the same basename:

```text
<content-root>/<system>/musings/notes/<slug>.md
<content-root>/<system>/musings/notes/<slug>.json
```

The Markdown file is body-only. The JSON file owns title, summary, tags, relationships, lifecycle timestamps, ordering, revision, and module attributes.

## Metadata checklist

- `schemaVersion`: repository schema version
- `id`: stable UUID
- `slug`: exactly the Markdown/JSON basename
- `title`, `summary`: concise and readable
- `tags`: existing vocabulary where possible
- `related`: stable IDs, normally an empty array for a standalone note
- `status`: usually `published` for a direct publish request
- `createdAt`, `updatedAt`, `publishedAt`: one consistent ISO timestamp when created now
- `order`, `revision`: repository-compatible defaults
- `attributes.kind`: `musings`

## Verification

After writing, confirm both siblings exist, parse JSON, and assert:

```python
assert md.exists() and meta.exists()
assert data["slug"] == md.stem == meta.stem
assert data["attributes"]["kind"] == "musings"
```

Do not add frontmatter, tag dictionary files, cover images, or unrelated edits unless the repository contract or user request requires them.
