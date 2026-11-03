# Session detail: FloatingOutline hover card + ChatPanel collapse (blogV2, 2026-08-24)

Repo: `/Users/songkuakua/Documents/code/Codex-Blog-AI-Chat/blogV2`

## Iteration log & failure modes on FloatingOutline.vue

### Attempt 1: per-item hover + adjacent preview popup (Broken)
- Code: `@mouseenter/@mouseleave` on each `<button>` to set `hoveredId = link.id`; card absolutely positioned `right: calc(100% + 14px)`.
- Failure: cursor leaves button to reach card → `mouseleave` fires in the gap → Vue destroys card immediately. Net UX: "卡片出不来".

### Attempt 2: wrapper hover + 180ms debounce timer (Broken in practice)
- Code: `@mouseenter="openCard"` / `@mouseleave="scheduleClose"` on `.outline-rules-zone` wrapper, single `isCardOpen` boolean, transition on card.
- User feedback: "样式太丑了，不是横线旁边多一个卡片，而是浮现的卡片代替这个横线；不需要那个点，加粗就已经能表示当前所在层级了".
- Design flaw: popped up as a secondary box next to the dashes with a title header, heavy shadow, and a trailing dot indicator on the active link.

### Attempt 3: v-show + scoped display:none fight (Broken)
- Code: tried `v-show="isCardOpen"` with scoped `.outline-card { display: none }` and `.outline-card[style*="display: block"] { display: flex }` to force inline styles to work with flex.
- User feedback: "又坏了，用不了" — CSS specificity fight and JS state getting out of sync with real cursor position.

### Attempt 4: pure CSS hover morph, initial fixed width (Partial)
- Replaced JS hover with pure CSS `:hover` on `.outline-rail`.
- User feedback:
  - "卡片里面点不了，另外卡片的样式不太好看，比例不太对，有点密" → Added padding to `.outline-rail` so the hover hotspot surrounds the card, increased gap to 4px, button padding to 7px 10px.
  - "卡片有点宽啊，大片的空白" → Fixed `230px` had empty trailing space on short section titles. Switched to `width: max-content` with `min-width: 140px; max-width: 220px`.
  - "有点丑啊" → Stripped all leftover decoration: no title bar, no trailing dot, subtle 1px border, reduced padding, active item = bold only.

### Attempt 5 (Final, accepted): content-adaptive pure-CSS morph
- Code in `app/components/content/FloatingOutline.vue`:
```vue
<div class="outline-rail">
  <ul class="outline-rules" aria-hidden="true">
    <li v-for="link in outlineLinks" :key="link.id">
      <span class="rule" :class="{ active: link.id === activeId }" />
    </li>
  </ul>

  <div class="outline-card" role="navigation" aria-label="浮动目录">
    <ul class="outline-card-list">
      <li v-for="item in outlineLinks" :key="item.id">
        <button
          type="button"
          class="outline-card__link"
          :class="{ active: item.id === activeId }"
          :aria-current="item.id === activeId ? 'true' : undefined"
          @click.stop="scrollTo(item)"
        >
          <span class="outline-card__link-text">{{ item.text }}</span>
        </button>
      </li>
    </ul>
  </div>
</div>
```
- Scoped CSS:
```css
.outline-rail {
  display: none;
  position: relative;
  pointer-events: auto;
  min-width: 32px;
  min-height: 48px;
  padding: 12px 6px;
  align-items: center;
  justify-content: flex-end;
}
.outline-rules {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  pointer-events: none;
  transition: opacity .15s ease-out;
}
.rule {
  display: block;
  width: 7px;
  height: 2px;
  border-radius: 999px;
  background: #cfd4da;
  transition: width .2s ease-out, background-color .2s ease-out;
}
.rule.active { width: 11px; height: 2.5px; background: var(--ink); }

.outline-card {
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  min-width: 140px;
  max-width: 220px;
  width: max-content;
  max-height: 380px;
  overflow-y: auto;
  border: 1px solid var(--line, #e4e7eb);
  border-radius: 12px;
  padding: 6px;
  background: var(--canvas, #ffffff);
  box-shadow: 0 8px 24px rgb(0 0 0 / 8%), 0 2px 6px rgb(0 0 0 / 4%);
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transition: opacity .18s ease-out, visibility .18s ease-out, transform .18s ease-out;
}
.outline-card-list {
  display: flex;
  margin: 0;
  padding: 0;
  flex-direction: column;
  align-items: stretch !important;
  gap: 2px !important;
  list-style: none;
}
.outline-card__link {
  display: flex;
  width: 100%;
  padding: 6px 10px;
  border-radius: 6px;
  color: var(--ink-soft, #57606a);
  text-align: left;
  font-size: 13px;
  line-height: 1.4;
  transition: color .15s ease-out, background-color .15s ease-out;
  cursor: pointer;
}
.outline-card__link.active {
  color: var(--ink, #1f2328);
  font-weight: 600;
}
.outline-rail:hover .outline-rules { opacity: 0; }
.outline-rail:hover .outline-card  { opacity: 1; visibility: visible; pointer-events: auto; }

@container reader (max-width: 1039px) {
  .outline ul.outline-labels { display: none; }
  .outline .outline-rail { display: flex; }
}
```

## Bug B — ChatPanel collapse

**Bug:** `.shell-panel--closed { width: 0 !important; flex-basis: 0 !important; opacity: 0; visibility: hidden }` in `app/assets/css/motion.css` failed because `app/components/chat/ChatPanel.vue` set scoped `flex: 0 0 var(--chat-width)` and `border-left: 1px solid var(--line)`.

**Fix:**
```css
.shell-panel--closed {
  width: 0 !important;
  min-width: 0 !important;
  flex: 0 0 0 !important;
  flex-basis: 0 !important;
  opacity: 0;
  visibility: hidden;
  border-left-width: 0 !important;
  border-right-width: 0 !important;
  padding: 0 !important;
  pointer-events: none !important;
  transition-delay: 0s, 0s, 0s, var(--shell-motion-duration);
}
```

## Verification

`npm run typecheck` passes after both edits.
