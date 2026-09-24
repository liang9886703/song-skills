# Skills 能力总览

> 共 88 个 skill，按功能分类整理。自动生成于 2026-09-10。


## Agent 系统与配置（23）

| Skill | 说明 |
|-------|------|
| `agent-model-configuration` | Use when changing an agent model or reasoning strength. |
| `batch-subagent-delegation` | Use when fan-out delegating many parallel subagent tasks. |
| `codex-desktop-network-debugging` | Use when Codex WebSockets fail behind Clash. |
| `debugging-hermes-tui-commands` | Debug Hermes TUI slash commands: Python, gateway, Ink UI. |
| `find-skills` | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a … |
| `handoff` | Compact the current conversation into a handoff document for another agent to pick up. |
| `hermes-agent` | Use, configure, theme, extend, and orchestrate Hermes Agent. |
| `hermes-gateway-debugging` | Debug Hermes Gateway platform adapters and messaging delivery paths. |
| `hermes-update-recovery` | Recover and verify git-installed Hermes Agent updates, especially when `hermes update` is interrupte… |
| `huashu-md-html` | 花叔的「md/html/docx 多向流水线」skill，四个能力 + 两种模式：(1) 用Microsoft markitdown把任意文件（PDF/DOCX/PPTX/XLSX/HTML/图片/音… |
| `hv-analysis` | 横纵分析法（Horizontal-Vertical Analysis）深度研究Skill。由数字生命卡兹克提出，融合了索绪尔的历时-共时分析、社会科学的纵向-横截面研究设计、商学院案例研究法与竞争战略… |
| `khazix-writer` | 数字生命卡兹克（Khazix）的公众号长文写作skill。当用户需要撰写公众号文章、写稿子、续写文章、根据素材产出长文时使用。触发词包括但不限于：写文章、写稿子、帮我写、续写、扩写、公众号文章、长文、… |
| `macos-computer-use` | Drive the macOS desktop in the background — screenshots, mouse, keyboard, scroll, drag — without ste… |
| `native-mcp` | MCP client: connect servers, register tools (stdio/HTTP). |
| `ontology` | Typed knowledge graph for structured agent memory and composable skills. Use when creating/querying … |
| `plan` | Write a markdown plan to .hermes/plans/; no execution. |
| `project-context-discovery` | Use when local project source files have an unclear path. |
| `prompt-log` | Extract conversation transcripts from AI coding session logs (Clawdbot, Claude Code, Codex). Use whe… |
| `self-improving-agent` | A universal self-improving agent that learns from ALL skill experiences. Uses multi-memory architect… |
| `skillshare-skill-management` | Use when assembling or syncing agent skills with skillshare. |
| `subagent-driven-development` | Execute plans via delegate_task subagents (2-stage review). |
| `taste-project` | 阅读代码仓库并按约束产出分析报告。用户想初步了解一个项目仓库、或想深入了解仓库里的某一个子能力时使用；用户只丢来一个仓库链接或目录、没说具体要什么时也用本 skill。 |
| `xurl` | A curl-like CLI tool for making authenticated requests to the X (Twitter) API. Use this skill when y… |

## 开发工具与代码（39）

| Skill | 说明 |
|-------|------|
| `backend-patterns` | Backend architecture patterns, API design, database optimization, and server-side best practices for… |
| `clone-website` | Reverse-engineer and clone one or more websites in one shot — extracts assets, CSS, and content sect… |
| `code-server-local-workspace` | Use when serving a local project through native code-server. |
| `codebase-inspection` | Inspect codebases w/ pygount: LOC, languages, ratios. |
| `content-driven-nuxt-refactor` | Use for Nuxt 4/Vue 3 local Markdown content refactors. |
| `create-architectural-decision-record` | Create an Architectural Decision Record (ADR) document for AI-optimized decision documentation. |
| `dogfood` | Exploratory QA of web apps: find bugs, evidence, reports. |
| `external-article-repository-tracing` | Trace an article to its verified GitHub repository. |
| `gamer-news` | Fetch and summarize the latest video game news from major gaming outlets (IGN, Kotaku, GameSpot, Pol… |
| `github-auth` | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. |
| `github-code-review` | Review PRs: diffs, inline comments via gh or REST. |
| `github-issues` | Create, triage, label, assign GitHub issues via gh or REST. |
| `github-pr-workflow` | GitHub PR lifecycle: branch, commit, open, CI, merge. |
| `github-repo-management` | Clone/create/fork repos; manage remotes, releases. |
| `github-repository-research` | Research and compare GitHub repositories: popularity, activity, positioning, README summaries, and m… |
| `golang-context` | Idiomatic context.Context usage in Golang — propagation through API boundaries, cancellation, timeou… |
| `golang-pro` | Master Go 1.21+ with modern patterns, advanced concurrency, performance optimization, and production… |
| `google-workspace` | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. |
| `jupyter-live-kernel` | Iterative Python via live Jupyter kernel (hamelnb). |
| `maps` | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. |
| `medical-report-review` | Review user-provided or previously shared medical reports, extract key values, compare against curre… |
| `narrative-digest-reading` | Compress long narrative texts into plot/event digests for skip-reading. Use for novels, serial ficti… |
| `node-inspect-debugger` | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. |
| `nuxt` | Nuxt full-stack Vue framework with SSR, auto-imports, and file-based routing. Use when working with … |
| `python-debugpy` | Debug Python: pdb REPL + debugpy remote (DAP). |
| `reference-driven-frontend-prototyping` | Build frontend-only prototypes from multiple website references, where one reference supplies layout… |
| `repo-evolution-audit` | Trace code paths, data flow, JSON or event formats, and recent git evolution for a feature or protoc… |
| `requesting-code-review` | Pre-commit review: security scan, quality gates, auto-fix. |
| `simplify-code` | Parallel 4-agent cleanup of recent code changes. |
| `spike` | Throwaway experiments to validate an idea before build. |
| `systematic-debugging` | 4-phase root cause debugging: understand bugs before fixing. |
| `test-driven-development` | TDD: enforce RED-GREEN-REFACTOR, tests before code. |
| `travel-planner` | Travel destination research and daily itinerary creation with logistics planning, budget tracking, a… |
| `ui-ux-pro-max` | UI/UX design intelligence for web and mobile. Searchable local database with 84 styles, 192 color pa… |
| `vue-best-practices` | MUST be used for Vue.js tasks. Strongly recommends Composition API with script setup and TypeScript … |
| `vue-component-refactoring` | Use when refactoring Vue/Nuxt components or UI panels. |
| `vue-ui-component-patterns` | Use when debugging Vue/Nuxt hover cards or panel collapse. |
| `webhook-subscriptions` | Webhook subscriptions: event-driven agent runs. |
| `writing-plans` | Write implementation plans: bite-sized tasks, paths, code. |

## 内容创作与写作（1）

| Skill | 说明 |
|-------|------|
| `ideation` | Generate project ideas via creative constraints. |

## 设计与视觉（21）

| Skill | 说明 |
|-------|------|
| `archify` | Create polished, validated architecture, workflow, sequence, data-flow, and lifecycle/state diagrams… |
| `architecture-diagram` | Dark-themed SVG architecture/cloud/infra diagrams as HTML. |
| `ascii-art` | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. |
| `ascii-video` | ASCII video: convert video/audio to colored ASCII MP4/GIF. |
| `baoyu-article-illustrator` | Article illustrations: type × style × palette consistency. |
| `baoyu-comic` | Knowledge comics (知识漫画): educational, biography, tutorial. |
| `baoyu-infographic` | Infographics: 21 layouts x 21 styles (信息图, 可视化). |
| `cat-care` | Practical cat-care guidance for new/adopted cats, behavior interpretation, household safety, feeding… |
| `claude-design` | Design one-off HTML artifacts (landing, deck, prototype). |
| `design-md` | Author/validate/export Google's DESIGN.md token spec files. |
| `evidence-backed-visual-guides` | Use when turning researched constraints into a visual guide. |
| `excalidraw` | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). |
| `manim-video` | Manim CE animations: 3Blue1Brown math/algo videos. |
| `p5js` | p5.js sketches: gen art, shaders, interactive, 3D. |
| `photo-abstract-editorial` | Create a clean, vertical editorial artwork that preserves an uploaded photograph as the original ima… |
| `pixel-art` | Pixel art w/ era palettes (NES, Game Boy, PICO-8). |
| `popular-web-designs` | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. |
| `pretext` | Build creative browser demos with DOM-free text layout. |
| `research-paper-writing` | Write ML papers for NeurIPS/ICML/ICLR: design→submit. |
| `sketch` | Throwaway HTML mockups: 2-3 design variants to compare. |
| `summarize` | Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). |

## 文档与办公（1）

| Skill | 说明 |
|-------|------|
| `pdf-to-markdown` | [Document Processing] Convert PDF files to Markdown with support for native text PDFs and scanned do… |

## 社交媒体与消息（1）

| Skill | 说明 |
|-------|------|
| `channel-ownership-and-proxy-diagnostics` | Use when channels fail across runtimes or proxy/TUN paths. |

## 系统运维与网络（1）

| Skill | 说明 |
|-------|------|
| `vpn-proxy-diagnostics` | Use when a VPN/proxy cannot reach a domain. |

## 生活与其他（1）

| Skill | 说明 |
|-------|------|
| `pp-steam-web` | Every Steam Web API endpoint, plus a local SQLite store that turns friend playtimes, achievement pro… |
