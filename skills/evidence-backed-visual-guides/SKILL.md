---
name: evidence-backed-visual-guides
description: Use when turning researched constraints into a visual guide.
---

# Evidence-Backed Visual Guides

Use this skill when a user wants a researched guide turned into a readable HTML artifact, especially when the request combines preferences, rankings, logistics, images, and a route or schedule.

## Core workflow

1. **Extract constraints before researching**
   - Capture origin, dates/season, group size, budget posture, duration flexibility, interests, exclusions, and required output format.
   - Resolve ambiguities that materially change the route. If dates are unavailable, state the planning assumption in the artifact.

2. **Lock the information architecture**
   - Preserve the user's requested order. A reliable default is: places/experiences ranked by priority; food ranked by priority; route with day numbers; then time, transport, accommodation, meals, budget, and booking notes.
   - Use P0/P1/P2 or Must/Should/Optional, and explicitly list what to cut when time is short.

3. **Research and qualify claims**
   - Prefer official tourism, transport, venue, and booking sources for current logistics.
   - Separate real-world locations from fictional settings, adaptations, or visual inspirations.
   - Do not turn thematic resemblance into a claim of exact one-to-one correspondence.
   - Mark prices, timetables, and holiday assumptions as approximate and date-sensitive.

4. **Design for use, not density**
   - Build around the user's actual interest rather than generic completeness.
   - Do not fill a nominal seven-day trip just to reach seven days.
   - Minimize backtracking; keep optional items removable.
   - For image-rich HTML, use meaningful photos with alt text, readable contrast, responsive layout, and links to maps or official sources.

5. **Deliver a real artifact**
   - Write HTML to an explicit output path, normally under `work/` when no path is supplied.
   - Prefer a single HTML file for easy sharing; if remote images are used, say that the page needs internet access.
   - Include a short source note and key assumptions inside the page.

6. **Verify before reporting success**
   - Open the generated page in a browser or local server.
   - Check title, section order, text presence, links, responsive layout at a narrow viewport, and image loading.
   - Replace broken remote assets instead of handing over silent image failures.
   - Report the exact artifact path and remaining external dependencies.

## Travel-specific application

For game- or film-inspired travel, map fictional districts to real neighborhoods as an experience route, not as a scavenger hunt for exact buildings. Keep the route compact: select the strongest city anchors, choose one or two signature foods per city, and make transit days explicit. If an open-jaw itinerary avoids substantial backtracking, recommend it directly and show the round-trip fallback.

## Quality gates

- [ ] User exclusions are visible in the final plan.
- [ ] Place list and food list precede the route when requested.
- [ ] Every day has a base area, time shape, transport, meal, and lodging logic.
- [ ] Optional items are labeled and removable.
- [ ] Current facts and uncertain estimates are qualified.
- [ ] HTML has been opened and images/links checked.

## Supporting notes

See `references/guide-production-checklist.md` for a compact reusable checklist and verification notes. See `references/yakuza-japan-case-study.md` for a game-inspired travel example covering ranked places/food, anti-overstuffing, open-jaw routing, and remote-image verification.