# DocumentComments selection trigger & sizing (blogV2, 2026-08-24)

## Context
Adding a floating comment action button triggered by text selection in `DocumentComments.vue` + `useDocumentComments.ts`.

## Problem
1. When selecting text, `selectionchange` fired on every mousemove, displaying the comment icon immediately mid-drag and tracking the cursor, which was disruptive.
2. Initial button dimensions (`40px × 36px`, `MessageSquare :size="17"`) were visually oversized ("太大了") relative to text lines.

## Solution
1. **Pointer state gating**: Added `isPointerDown` flag via `pointerdown`/`pointerup` on the prose container.
2. **Debounced display**: While pointer is down, suppress the popover and clear any pending timer. On `pointerup`, trigger a 100ms timer before flipping `panel.value = 'selection'`.
3. **Compact sizing**: Reduced button to `30px × 28px` with `border-radius: 9px` and `MessageSquare :size="14"`.

```ts
// useDocumentComments.ts
let selectionTimer: ReturnType<typeof setTimeout> | null = null
let isPointerDown = false

function updateSelection() {
  if (panel.value === 'composer' || panel.value === 'detail') return
  const root = proseRoot.value
  const selection = window.getSelection()
  if (!root || !selection || selection.rangeCount === 0 || selection.isCollapsed) {
    clearSelectionTimer()
    if (panel.value === 'selection') closePanel()
    return
  }

  const range = selection.getRangeAt(0)
  if (!root.contains(range.startContainer) || !root.contains(range.endContainer)) return
  const anchor = textQuoteFromRange(root, range)
  if (!anchor) return

  pendingAnchor.value = anchor
  selectionRange = range.cloneRange()
  position.value = positionForSelectionRect(selectionAnchorRect(selectionRange))
  error.value = ''

  if (isPointerDown) {
    if (panel.value === 'selection') closePanel()
    clearSelectionTimer()
    return
  }
  if (panel.value !== 'selection') {
    clearSelectionTimer()
    selectionTimer = setTimeout(() => {
      selectionTimer = null
      if (!pendingAnchor.value || !selectionRange) return
      panel.value = 'selection'
    }, 100)
  }
}
```
