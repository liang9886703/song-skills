# Knowledge-vault refactor pattern

Use this pattern when an existing reference-driven Vue site must be turned into a real personal knowledge workspace.

## Source discovery

1. Locate the existing project before scaffolding. A prior prototype may live outside the current workspace, for example under `~/work/`.
2. Confirm the user-provided data root and inspect it recursively.
3. Exclude hidden/auxiliary directories such as `.history`, `.git`, `.obsidian`, and generated caches from the user-facing index.
4. Generate a typed content index from real Markdown files: stable relative ID/path, title, category, body preview, and size/metadata.

## UI mapping

- Preserve the previously established three-pane layout: collapsible source tree, source-of-truth article, context-aware agent panel.
- Bind the active document to both the article and agent context card.
- Add search over title, path, and body preview before introducing remote search.
- Keep local content usable without Convex credentials; install/prepare the Convex boundary without making local preview depend on a deployment.

## Style continuity

For the songkuakua visual baseline, retain the documented Futura/Together font cues, `#f3d2c1` body background, `#fef6e4` main surface, `#8bd3dd` cyan block, `#f582ae` pink accent, `#172c66` ink, and saturated blur/glass surfaces. The result should remain text-first and editorial rather than turning into a generic SaaS dashboard.

## Verification

Run the project build, verify HTTP 200, then use native Playwright with a system Chrome fallback if bundled Chromium is unavailable. Capture a real screenshot and report the absolute path, page title, key DOM counts, and any platform-specific media delivery fallback.
