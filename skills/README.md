# Skills 能力总览

> 共 131 个 skill，按功能分类整理。自动生成于 2026-09-10。


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

## 社交媒体与消息（6）

| Skill | 说明 |
|-------|------|
| `channel-ownership-and-proxy-diagnostics` | Use when channels fail across runtimes or proxy/TUN paths. |
| `himalaya` | Himalaya CLI: IMAP/SMTP email from terminal. |
| `imessage` | Send and receive iMessages/SMS via the imsg CLI on macOS. |
| `messaging-network-diagnostics` | Use when messaging channels fail. |
| `messaging-runtime-ownership` | Use when channel ownership is unclear across runtimes. |
| `yuanbao` | Yuanbao (元宝) groups: @mention users, query info/members. |

## 音视频与媒体（4）

| Skill | 说明 |
|-------|------|
| `humanizer` | Humanize text: strip AI-isms and add real voice. |
| `songsee` | Audio spectrograms/features (mel, chroma, MFCC) via CLI. |
| `songwriting-and-ai-music` | Songwriting craft and Suno AI music prompts. |
| `voice-chat-mode` | 在用户明确要求中文语音聊天或中文语音模式时激活。 |

## 系统运维与网络（4）

| Skill | 说明 |
|-------|------|
| `findmy` | Track Apple devices/AirTags via FindMy.app on macOS. |
| `minecraft-modpack-server` | Host modded Minecraft servers (CurseForge, Modrinth). |
| `openhue` | Control Philips Hue lights, scenes, rooms via OpenHue CLI. |
| `vpn-proxy-diagnostics` | Use when a VPN/proxy cannot reach a domain. |

## AI/ML 工具链（14）

| Skill | 说明 |
|-------|------|
| `audiocraft-audio-generation` | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. |
| `comfyui` | Generate images, video, and audio via diffusion workflows. |
| `dspy` | DSPy: declarative LM programs, auto-optimize prompts, RAG. |
| `evaluating-llms-harness` | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). |
| `godmode` | Jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN. |
| `heartmula` | HeartMuLa: Suno-like song generation from lyrics + tags. |
| `huggingface-hub` | HuggingFace hf CLI: search/download/upload models, datasets. |
| `llama-cpp` | llama.cpp local GGUF inference + HF Hub model discovery. |
| `nano-banana-pro` | Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image). Use for image create/modify requests… |
| `obliteratus` | OBLITERATUS: abliterate LLM refusals (diff-in-means). |
| `polymarket` | Query Polymarket: markets, prices, orderbooks, history. |
| `segment-anything-model` | SAM: zero-shot image segmentation via points, boxes, masks. |
| `serving-llms-vllm` | vLLM: high-throughput LLM serving, OpenAI API, quantization. |
| `weights-and-biases` | W&B: log ML experiments, sweeps, model registry, dashboards. |

## 思维模型与人物视角（15）

| Skill | 说明 |
|-------|------|
| `andrej-karpathy-perspective` | Andrej Karpathy的思维框架与表达方式。基于20+篇博文、16段深度访谈、100+条X帖子的系统蒸馏， 提炼6个核心心智模型、8条决策启发式、完整的中文输出适配和经典句式速查。 用途：作为… |
| `elon-musk-perspective` | 马斯克的思维操作系统。基于传记、播客、推文、法庭证词、决策记录和外部批评的深度调研， 提炼5个核心心智模型、8条决策启发式和完整的表达DNA。 用途：作为思维顾问，用马斯克的视角分析问题、审视决策、拆… |
| `feynman-perspective` | 理查德·费曼的思维框架与表达方式。基于40+个一手来源的深度调研， 提炼5个核心心智模型、8条决策启发式和完整的表达DNA。 用途：作为思维顾问，用费曼的视角分析问题、审视决策、提供反馈。 当用户提到… |
| `ilya-sutskever-perspective` | Ilya Sutskever的思维框架与表达方式。基于12段一手对话、9篇学术论文、10小时宣誓证词、 27篇推荐阅读清单和14个权威二手来源的深度调研， 提炼6个核心心智模型、8条决策启发式和完整的… |
| `llm-wiki` | Karpathy's LLM Wiki: build/query interlinked markdown KB. |
| `mrbeast-perspective` | MrBeast（Jimmy Donaldson）的内容创造操作系统。基于泄露的36页内部培训手册、 6个深度播客、决策记录和外部批评的深度调研，提炼6个核心心智模型、8条决策启发式、 完整的标题/缩略… |
| `munger-perspective` | 查理·芒格的思维框架与表达方式。基于《穷查理宝典》、伯克希尔/Daily Journal股东会、 USC/哈佛演讲、访谈记录、外部批评等50+来源的深度调研， 提炼5个核心心智模型、8条决策启发式和完… |
| `naval-perspective` | Naval Ravikant的思维操作系统。基于著作、播客、推文、决策记录和外部批评的深度调研， 提炼5个核心心智模型、8条决策启发式和完整的表达DNA。 激活后沉浸式扮演Naval，直接以「我」的视… |
| `paul-graham-perspective` | Paul Graham的思维框架与表达方式。基于200+篇essays、12个播客/访谈、 Twitter/X分析、7位核心批评者视角和完整人生时间线的深度调研， 提炼5个核心心智模型、8条决策启发式… |
| `steve-jobs-perspective` | 史蒂夫·乔布斯(Steve Jobs)的思维框架与表达方式。基于Isaacson授权传记、Stanford演讲、 Lost Interview、D Conference系列、Make Somethin… |
| `sun-yuchen-perspective` | 孙宇晨（Justin Sun / 孙割）的思维框架与行为逻辑。基于6个维度（著作、深度采访、表达DNA、 他者视角、决策记录、时间线）共1500+行调研素材的深度蒸馏， 提炼6个核心心智模型、8条决策… |
| `taleb-perspective` | 塔勒布(Nassim Nicholas Taleb)的思维框架与表达方式。基于40+个来源的深度调研， 提炼6个核心心智模型、9条决策启发式和完整的表达DNA。 用途：作为思维顾问，用塔勒布的视角分析… |
| `trump-perspective` | 唐纳德·特朗普（Donald Trump）的思维框架与行为逻辑。基于著作、长访谈、辩论、 心理分析、前幕僚回忆录、重大决策记录共6个维度的深度调研（320KB+原始资料）， 提炼6个核心心智模型、8条… |
| `zhang-yiming-perspective` | 张一鸣（字节跳动/TikTok创始人）的思维框架与表达方式。基于6个维度（著作、深度访谈、 表达DNA、他者视角、决策记录、时间线）的调研，涵盖32个访谈片段、12个重大决策案例， 提炼5个核心心智模… |
| `zhangxuefeng-perspective` | 张雪峰的思维框架与表达方式。基于5本著作、15+篇权威媒体深度采访、 30+条一手语录、11个关键决策记录和完整人生时间线的深度调研， 提炼5个核心心智模型、8条决策启发式和完整的表达DNA。 用途：… |

## 生活与其他（3）

| Skill | 说明 |
|-------|------|
| `pokemon-player` | Play Pokemon via headless emulator + RAM reads. |
| `pp-steam-web` | Every Steam Web API endpoint, plus a local SQLite store that turns friend playtimes, achievement pro… |
| `x-mastery-mentor` | $10K/hr级X/Twitter运营导师。基于Nicolas Cole、Dickie Bush、Sahil Bloom、Justin Welsh、 Dan Koe、Alex Hormozi六位顶级创… |
