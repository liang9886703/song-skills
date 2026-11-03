# Multi-view side panel implementation (blogV2, Aug 30 2026)

## What was built

Expanded the single-purpose chat side panel into a multi-view panel with three switchable views:
- **Chat** (original): AI conversation panel
- **Outline**: document table of contents (reuses FloatingOutline logic)
- **Comments**: list of all document comments with scroll-to-comment navigation

## Files created

| File | Purpose |
|------|---------|
| `app/components/navigation/SidePanelHeader.vue` | Icon bar header with 3 buttons (Bot, List, MessageSquare) |
| `app/components/content/OutlinePanel.vue` | Full-height outline panel with active heading tracking |
| `app/components/content/CommentsPanel.vue` | Comment list panel with click-to-scroll |

## Files modified

| File | Change |
|------|--------|
| `app/components/shell/AppShell.vue` | Replaced `chatOpen` with `sidePanelOpen` + `sidePanelView`; added `toggleSidePanel` and `updateSidePanelView` |
| `app/components/navigation/TopBar.vue` | Replaced `ChatPanelHeader` with `SidePanelHeader`; added `sidePanelOpen`/`sidePanelView` props |
| `app/components/chat/ChatPanel.vue` | Root element changed from `<aside>` to `<div>`; removed independent width/border styles |
| `tests/unit/top-bar.test.ts` | Updated props and event names |
| `tests/unit/app-shell-module-controls.test.ts` | Added `onUnmounted` stub, `contentKey` prop, and new component stubs |
| `tests/e2e/blog.spec.ts` | Updated DOM selectors and assertions |

## Key design decisions

1. **Icon bar in topbar, not in panel**: The `SidePanelHeader` lives in `.topbar-end`, so the icons remain visible and clickable even when the panel is closed (width: 0). This follows Pattern 27.

2. **Panel container stays, content switches**: The `.side-panel` wrapper is always in the DOM with its width transition. Only the inner component changes via `v-if="sidePanelView === 'chat'"` etc.

3. **Default open with view memory**: `sidePanelOpen` defaults to `true` (preserving previous chat behavior). `sidePanelView` remembers the last active view. Clicking the active icon closes the panel; clicking a different icon switches content while keeping it open.

4. **Padding compensation**: When the panel closes, `.topbar-center` needs `padding-right: 116px` to reserve space for the 3-icon bar. Without this, the icons overlap the view-switch toolbar buttons.

## The overlap bug (user-reported)

**Symptom**: "机器人图标关上特边栏装后，会出现和工具栏重叠的情况" — after closing the side panel, the bot icon overlaps the toolbar buttons.

**Root cause**: `.topbar-center` had `padding-right: 56px` when the panel was closed, but the 3-icon bar (32px × 3 + gaps ≈ 100px) remained visible. The `view-switch` buttons expanded into the icon bar's space.

**Fix**: Increased `.topbar-center` default `padding-right` from `56px` to `116px`.

**Verification**: `browser_console` measurement showed `viewSwitch.right = 1160` and `icons[0].left = 1172` — a 12px gap.

## Cross-directory file loss incident

During the session, the agent accidentally wrote new files to `~/.openclaw/workspace-chouno_hina/app/components/` instead of the project directory. The files were "lost" until a `find` command located them. This is captured in Pattern 29 of the skill.

## Test results

- `npm run build` — passes
- `npm test` — 265/265 tests pass (1 pre-existing failure in `opencode-provider.test.ts` unrelated to this change)
- `npm run typecheck` — passes
- `npm run lint` — no new errors in modified files
