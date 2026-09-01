---
name: blog-musings-authoring
description: Use when creating file-backed personal blog musings.
---

# Blog Musings Authoring

Use this skill when turning a user's personal observation or reflection into a published musing in a file-backed blog repository.

## Workflow

1. Resolve the repository and content root before writing. Do not assume the active Obsidian vault is the blog repository; inspect the configured project/workspace when the request names a site or content collection.
2. Inspect one or more neighboring documents in the target collection to learn the repository's tone, filename convention, metadata shape, and tag vocabulary.
3. Preserve the user's concrete facts and emotional stance. Edit for readability and rhythm, but do not invent names, events, motives, dates, or outcomes. Keep personal musings personal rather than turning them into generic advice.
4. Write the Markdown body without frontmatter when the repository uses separate metadata files.
5. Write the same-basename JSON metadata beside the Markdown file. At minimum include the repository schema's `schemaVersion`, stable `id`, `slug`, `title`, `summary`, `tags`, `related`, publication status, timestamps, `order`, `revision`, and module-specific `attributes.kind`.
6. Prefer existing tags whose meaning materially fits. Do not create new tag files merely to describe one article unless the user's workflow explicitly asks for tag vocabulary changes.
7. Verify the pair after writing: both files exist, basenames match, JSON parses, slug matches the basename, and the metadata kind points to the intended module.

## Content style

For a short life musing, use a lightly edited first-person narrative: concrete event first, a small amount of reflection, then a natural closing image or line. Avoid over-explaining, motivational conclusions, and fabricated detail. Preserve the user's humor and specific phrasing when it carries personality.

## Repository rules

- Follow the target repository's local content contract over generic Obsidian conventions.
- If the project separates body and metadata, never add YAML frontmatter to the Markdown body.
- Treat data directories outside the code repository as runtime content; avoid unrelated cleanup or formatting changes.

## References

- See `references/paired-content-records.md` for the reusable Markdown/JSON contract and verification checklist.
