# Session detail: Chat panel遮挡工具栏问题 (blogV2, 2026-08-30)

## User report

User shared a screenshot showing:
- Path bar fully visible but compressed: `/ article / default / codex-blog-ai-chat--blogv2--docs--storage`
- "对话 / ● 未配置" appearing in the top toolbar right zone
- Eye/pencil icons NOT visible (covered by the chat header copy)
- Window width approximately 978px

## Root cause

The resize-listener fix (Pattern 25) was applied, but the user's screenshot showed the issue persisting. Investigation revealed:

1. The user had manually toggled chat at some point, setting `chatManuallySet = true`
2. This prevented the resize listener from auto-closing chat when the window was dragged to ~978px
3. With `chatOpen=true` at 978px viewport, the 320px chat rail forced the layout to compress
4. The chat header copy ("对话/未配置") overflowed into the center zone, covering the eye/pencil icons

## The deeper issue

The `chatManuallySet` flag was too aggressive — once set, it permanently disabled auto-close on resize. But the user's intent was "don't close chat when I accidentally nudge the window", not "never close chat even when the window is too narrow".

## Fix needed

The resize listener should still auto-close chat when the viewport is critically narrow (e.g. < 1120px), even if the user manually opened it. The `chatManuallySet` flag should only prevent auto-close within a "safe" range, not override it entirely.

Alternatively: reset `chatManuallySet` when the window is widened back above the threshold, so the auto-close behavior resumes for the next resize cycle.

## User's layout model (confirmed)

- Chat open: "机器人图标所在的方框延长，把工具栏顶出右侧栏的范围"
- The topbar right zone and chat panel topbar are the same visual element
- Search bar should shrink to make room, not be overlapped
- When viewport is too narrow, chat should auto-close to preserve usable center space

## Related patterns

- Pattern 25: Chat header copy overflow — resize listener vs CSS clipping
- Pattern 27: Panel toggle buttons must remain accessible
