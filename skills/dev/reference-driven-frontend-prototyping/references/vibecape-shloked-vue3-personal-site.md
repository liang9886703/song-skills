# Vibecape + Shloked → Vue3 personal agent site pattern

Session pattern captured from a frontend-only prototype request.

## User goal

- Reference A: `https://vibecape.com` supplies the main layout.
- Reference B: `https://www.shloked.com` supplies overall element/style tone.
- Build a personal website frontend with:
  - left collapsible document directory / full-page content index
  - center article body
  - right intelligent conversation body
- User clarified: use **Vue3** and **frontend only**.

## Reference extraction summary

### Vibecape cues

- Three-pane product workspace: tree on the left, page in the middle, conversation on the right.
- Quiet local-first workspace tone.
- Light warm background (`#f7f7f5`-like), thin borders, low contrast surfaces.
- Right agent pane is a collaborator/margin assistant, not a floating customer-service chat bubble.

### Shloked cues

- Personal-site restraint: black/white/gray, text-first, minimal decoration.
- Low-noise links and lists, system sans / Geist-like typography.
- Strong editorial hierarchy without generic SaaS cards or gradients.

## Implementation choices that worked

- Vite + Vue3 app under `work/personal-agent-site`.
- `src/App.vue` holds the layout state and mock content.
- `src/style.css` implements the full visual system with CSS Grid and CSS variables.
- Layout:
  - `grid-template-columns: 288px minmax(0, 1fr) 380px`
  - collapsed left state: `76px minmax(0, 1fr) 380px`
  - left/right panes are `height: 100vh; position: sticky; top: 0`
  - center article pane owns the main scroll
- Mock interactions:
  - toggle sidebar open/closed
  - select document item
  - send a mock chat message
- Responsive behavior:
  - collapse left directory at medium widths
  - single-column flow on small screens, chat after content

## Verification pattern

Run:

```bash
npm install
npm run build
npm run dev
```

Then verify the dev server responds:

```bash
python3 - <<'PY'
import urllib.request
print(len(urllib.request.urlopen('http://127.0.0.1:5173', timeout=2).read()))
PY
```

If browser automation is unavailable, report that limitation explicitly instead of claiming visual screenshot QA.

## Durable lesson

For reference-driven site building, the critical move is to separate **layout reference** from **style reference** and then build an original product surface in the requested frontend stack. Treat installed clone/pixel-perfect skills as extraction aids, not as a mandate to clone exactly.
