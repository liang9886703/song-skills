# Search Bar Path Badges Hide/Show Animation (blogV2, 2026-08-26)

## Context
After adding path-segment badges to the search bar (showing current page path like `/article/skills/backend-patterns`), the user requested two refinements:
1. **Hide badges while typing** — "打字的时候，消失他们" (when typing, make them disappear)
2. **Add a quick fade animation** — "消失和现实有个快速的浮现动画" (disappear and reappear with a quick fade animation)

## Implementation

### Hide on typing
Simple `v-if` bound to the query state:

```vue
<div v-if="!query" class="search-path" aria-hidden="true">
  <span v-for="(seg, i) in pathSegments" :key="i" class="path-segment">
    <span class="path-sep">/</span>
    <span class="path-text">{{ seg }}</span>
  </span>
</div>
```

### Add Transition animation
Wrap in Vue `<Transition>` with a named transition for CSS class scoping:

```vue
<Transition name="search-path">
  <div v-if="!query" class="search-path" aria-hidden="true">
    <span v-for="(seg, i) in pathSegments" :key="i" class="path-segment">
      <span class="path-sep">/</span>
      <span class="path-text">{{ seg }}</span>
    </span>
  </div>
</Transition>
```

```css
.search-path-enter-active, .search-path-leave-active {
  transition: opacity 120ms ease, transform 120ms ease;
}
.search-path-enter-from, .search-path-leave-to {
  opacity: 0;
  transform: translateX(4px);
}
.search-path-enter-to, .search-path-leave-from {
  opacity: 1;
  transform: translateX(0);
}
```

## Key decisions

1. **120ms duration** — fast enough to feel responsive, slow enough to be perceptible. This is a micro-interaction, not a page transition.

2. **`translateX(4px)`** — subtle directional cue. The badges slide slightly right when disappearing and slide in from the right when appearing. Keeps the animation feeling connected to the input field's right edge.

3. **No `transition` on base class** — the `.search-path` class itself has no `transition` property. Only the Vue Transition classes (`search-path-enter-*`, `search-path-leave-*`) have transitions. This prevents conflicts and ensures the animation only plays during mount/unmount.

4. **Vue `<Transition>` over manual CSS** — `v-show` + manual class toggles would require tracking enter/leave states manually. Vue's `<Transition>` handles the brief window where the element is leaving but still needs to be rendered for the leave animation to play.

## Anti-pattern avoided

Don't put `transition` on the base `.search-path` class:

```css
/* ❌ Wrong — causes transition to fire on any property change */
.search-path {
  transition: opacity 120ms ease, transform 120ms ease;
}
```

This would make the badges animate on hover, focus, or any other state change, not just on mount/unmount. The Vue Transition classes are the correct scope.
