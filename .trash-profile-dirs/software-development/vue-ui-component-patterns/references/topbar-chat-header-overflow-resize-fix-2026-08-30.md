# Session detail: Topbar chat header overflow — resize listener fix (blogV2, 2026-08-30)

Repo: `/Users/songkuakua/Documents/code/Codex-Blog-AI-Chat/blogV2`

## User report (second occurrence)

User shared another screenshot showing the same symptom:
- Breadcrumb/path bar compressed to `… / …orage`
- "对话" and "● 未配置" appearing in the top toolbar, not in a separate chat sidebar
- No visible chat sidebar panel
- Window width approximately 800px

## Root cause (deeper than first fix)

First fix attempt (earlier same day): changed `.topbar-end` and `.chat-panel-header` to `overflow: hidden`. This clipped the overflowing copy but **also clipped the bot toggle button** (36px, `position: absolute; right: 8px`), making it unclickable. Playwright test `matches the Codex shell geometry` failed with `chatBotToggle.click()` timeout.

**Real root cause:** `AppShell.vue` only checks `window.innerWidth` in `onMounted`:

```ts
onMounted(() => {
  if (window.innerWidth < 760) {
    sidebarOpen.value = false
    chatOpen.value = false
  } else if (window.innerWidth < 1120) {
    chatOpen.value = false
  }
})
```

No `resize` listener. So:
1. User loads at 1280px → `chatOpen = true` (chat opens)
2. User drags window to ~800px → `chatOpen` stays `true`
3. `topbar-end--rail` forces 320px width, but viewport can't fit sidebar + center + 320px
4. Header copy ("对话 / 未配置") overflows into compressed `topbar-center`
5. Path bar gets squeezed to `.../...age`

## Fix applied

**File:** `app/components/shell/AppShell.vue`

```ts
let chatManuallySet = false

const syncPanelWithViewport = () => {
  if (window.innerWidth < 760) {
    sidebarOpen.value = false
    if (!chatManuallySet) chatOpen.value = false
  } else if (window.innerWidth < 1120) {
    if (!chatManuallySet) chatOpen.value = false
  }
}

const toggleChat = () => {
  chatOpen.value = !chatOpen.value
  chatManuallySet = true
}

onMounted(() => {
  syncPanelWithViewport()
  window.addEventListener('resize', syncPanelWithViewport)
})

onUnmounted(() => {
  window.removeEventListener('resize', syncPanelWithViewport)
})
```

Template change: `@toggle-chat="toggleChat"` (was `@toggle-chat="chatOpen = !chatOpen"`)

## Why not CSS clipping

`overflow: hidden` on `.topbar-end` or `.chat-panel-header` treats the symptom (copy overflow) but breaks the bot toggle:

- `.topbar-end` width: 0 (chat closed)
- `.chat-panel-header` has intrinsic min-content width ~70px (from the 36px absolute toggle + padding)
- Toggle lands inside that 70px box, which extends leftward from the 0-width parent
- `overflow: hidden` on the 0-width parent clips the toggle

**Verified:** `botWouldBeClipped: true` when forcing zero-width state with `overflow: hidden`.

## Verification

- `npm run typecheck` ✅
- `npx playwright test tests/e2e/blog.spec.ts` → 11 passed, 1 failed (the 1 failure was pre-existing, unrelated)
- `matches the Codex shell geometry` now passes (bot toggle clickable)

## Related patterns

- Pattern 23: Shell topbar overflow — zero-width flex children with `overflow: visible`
- Pattern 25: Chat header copy overflow — resize listener vs CSS clipping (this fix)
