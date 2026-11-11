# Skills 能力总览

> 本项目技能按应用场景分为四大体系：**电脑运维 (`ops`)**、**程序开发 (`dev`)**、**生活管理相关 (`lifestyle`)**、**调研报告类 (`research`)**。每个技能以其目录下的 `SKILL.md` 为统一入口。

> 注：部分企业内部私有技能受 `.gitignore` 保护，仅在本地使用，不在公开仓库中展示。

---

## 目录导航

- [电脑运维 (ops)（20）](#ops)
- [程序开发 (dev)（46）](#dev)
- [生活管理相关 (lifestyle)（3）](#lifestyle)
- [调研报告类 (research)（9）](#research)

---

<a id="ops"></a>
## 电脑运维 (ops)

| Skill | 说明 |
|-------|------|
| [`agent-model-configuration`](ops/agent-model-configuration/SKILL.md) | Use when changing an agent model or reasoning strength. |
| [`baidu-bls-log-py`](ops/baidu-bls-log-py/SKILL.md) | 使用 Python 查询、搜索和统计百度云 BLS 日志，查看日志组、日志集及索引。适用于 BLS 日志检索、错误排查和日志分析，无需 Go 环境。 |
| [`baidu-cloud-bos`](ops/baidu-cloud-bos/SKILL.md) | 百度智能云对象存储（BOS）集成技能。当用户需要上传、下载、删除或复制 BOS 文件， 列出文件列表或 Bucket，获取签名 URL，处理图片（亮度、对比度、模糊、旋转、裁剪、水印等）， 或递归同步本地目录与  |
| [`baidu-enterprise-search`](ops/baidu-enterprise-search/SKILL.md) | 百度企业内部六类关键词搜索（内搜/通讯录/会议/知识库/OKR/周报）。搜人搜群、找文档、检索任意人会议/周报/OKR 时使用。需深度分析OKR→用 fetch-okr-content；汇总下属周报→用 fetch |
| [`baidu-get-ugate-token`](ops/baidu-get-ugate-token/SKILL.md) | 获取并缓存 ugate token，供其他 skill 依赖使用进行API调用（多用户版本，永久有效） |
| [`baidu-infoflow-message-group`](ops/baidu-infoflow-message-group/SKILL.md) | 通过如流机器人发送、撤回或置顶消息，以及管理群聊、成员、权限、公告和群配置。用户要求如流消息操作或群管理时使用。 |
| [`baidu-ku-doc-2-md`](ops/baidu-ku-doc-2-md/SKILL.md) | 百度知识库文档转本地Markdown。从知识库URL读取文档内容，下载图片到本地，生成带图片的完整Markdown文件。触发词:知识库转md/ku转markdown/文档下载/知识库导出/导出md/保存知识库文档。 |
| [`baidu-ku-doc-manage`](ops/baidu-ku-doc-manage/SKILL.md) | 百度知识库(ku.baidu-int.com)文档管理。触发词:知识库URL/文档/知识库/库/ku文档/创建文档/查询文档/复制文档/移动文档/编辑文档/文档权限/文档列表/文档评论/文档内容/浏览记录/流程图导 |
| [`batch-subagent-delegation`](ops/batch-subagent-delegation/SKILL.md) | 当用户要求"给 N 个项目/目标各起一个子 agent 分别完成同类任务（调研、写文档、审计、扫描）"时使用。核心目标：避免整批失败、避免会话被同步阻塞卡住、避免把"已派发"误报为"已完成"。 |
| [`debugging-hermes-tui-commands`](ops/debugging-hermes-tui-commands/SKILL.md) | Debug Hermes TUI slash commands: Python, gateway, Ink UI. |
| [`find-skills`](ops/find-skills/SKILL.md) | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express int |
| [`github-auth`](ops/github-auth/SKILL.md) | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. |
| [`google-workspace`](ops/google-workspace/SKILL.md) | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. |
| [`hermes-agent`](ops/hermes-agent/SKILL.md) | Use, configure, theme, extend, and orchestrate Hermes Agent. |
| [`hermes-gateway-debugging`](ops/hermes-gateway-debugging/SKILL.md) | Debug Hermes Gateway platform adapters and messaging delivery paths. |
| [`hermes-update-recovery`](ops/hermes-update-recovery/SKILL.md) | Recover and verify git-installed Hermes Agent updates, especially when `hermes update` is interrupted, leaves local stashes/conflicts, or the CLI cannot start a |
| [`native-mcp`](ops/native-mcp/SKILL.md) | MCP client: connect servers, register tools (stdio/HTTP). |
| [`skill-quality-checker`](ops/skill-quality-checker/SKILL.md) | Skill 质量校验官（生产级）。对其他 Skill 进行结构化质量检查，覆盖6大维度21项核心指标。触发词/场景：校验Skill、检查Skill质量、质量检验、skill质检、review skill、技能审查、 |
| [`skillshare`](ops/skillshare/SKILL.md) | 统一发现、推荐、安装与维护个人技能：结合意图分析从远端/平台推荐 Top 3 技能并预览确认，支持搜索 skills.sh、GitHub、Hub、OneSkill 与内网源，安装到 song-skills 并分发。 |
| [`skillshare-skill-management`](ops/skillshare-skill-management/SKILL.md) | 管理个人 song-skills：登记出处、按各技能 GitHub 上游更新，再同步仓库和工具目录。 |

<a id="dev"></a>
## 程序开发 (dev)

| Skill | 说明 |
|-------|------|
| [`Ontology`](dev/Ontology/SKILL.md) | Typed knowledge graph for structured agent memory and composable skills. Use when creating/querying entities (Person, Project, Task, Event, Document), linking r |
| [`ai-drawio`](dev/ai-drawio/SKILL.md) | Generate draw.io diagrams from natural language and render in browser |
| [`aj-geddes-architecture-diagrams`](dev/aj-geddes-architecture-diagrams/SKILL.md) | Create system architecture diagrams using Mermaid, PlantUML, C4 model, |
| [`api-design-principles`](dev/api-design-principles/SKILL.md) | Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers. Use when designing new APIs, reviewin |
| [`archify`](dev/archify/SKILL.md) | Create interactive architecture, workflow, sequence, data-flow, and state diagrams as standalone HTML/SVG with image or video export. Use for technical diagrams |
| [`architecture-diagram`](dev/architecture-diagram/SKILL.md) | Dark-themed SVG architecture/cloud/infra diagrams as HTML. |
| [`architecture-diagram-builder`](dev/architecture-diagram-builder/SKILL.md) | - 画架构图、系统图、模块图、组件图、部署图、拓扑图、链路图、时序图、迁移图或可靠性/路由图。 |
| [`ascii-art`](dev/ascii-art/SKILL.md) | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. |
| [`ascii-art-diagrams`](dev/ascii-art-diagrams/SKILL.md) | Create aligned ASCII art and text diagrams in Markdown. Load before drawing; follow the PLAN, DRAW, VERIFY workflow. |
| [`backend-patterns`](dev/backend-patterns/SKILL.md) | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. |
| [`claude-design`](dev/claude-design/SKILL.md) | Design one-off HTML artifacts (landing, deck, prototype). |
| [`clone-website`](dev/clone-website/SKILL.md) | Reverse-engineer and clone one or more websites in one shot — extracts assets, CSS, and content section-by-section and proactively dispatches parallel builder a |
| [`content-driven-nuxt-refactor`](dev/content-driven-nuxt-refactor/SKILL.md) | Use for Nuxt 4/Vue 3 local Markdown content refactors. |
| [`design-md`](dev/design-md/SKILL.md) | Author/validate/export Google's DESIGN.md token spec files. |
| [`doc-publish`](dev/doc-publish/SKILL.md) | Use when explicitly asked to use 文档发布 skill. |
| [`documentation`](dev/documentation/SKILL.md) | Write and maintain technical documentation. Trigger with "write docs for", "document this", "create a README", "write a runbook", "onboarding guide", or when th |
| [`excalidraw`](dev/excalidraw/SKILL.md) | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). |
| [`fastify-best-practices`](dev/fastify-best-practices/SKILL.md) | Guides development of Fastify Node.js backend servers and REST APIs using TypeScript or JavaScript. Use when building, configuring, or debugging a Fastify appli |
| [`github-code-review`](dev/github-code-review/SKILL.md) | Review PRs: diffs, inline comments via gh or REST. |
| [`github-issues`](dev/github-issues/SKILL.md) | Create, triage, label, assign GitHub issues via gh or REST. |
| [`github-pr-workflow`](dev/github-pr-workflow/SKILL.md) | GitHub PR lifecycle: branch, commit, open, CI, merge. |
| [`github-repo-management`](dev/github-repo-management/SKILL.md) | Clone/create/fork repos; manage remotes, releases. |
| [`golang-context`](dev/golang-context/SKILL.md) | Idiomatic context.Context usage in Golang — propagation through API boundaries, cancellation, timeouts and deadlines, request-scoped values, context.WithoutCanc |
| [`golang-pro`](dev/golang-pro/SKILL.md) | Master Go 1.21+ with modern patterns, advanced concurrency, performance optimization, and production-ready microservices. |
| [`handoff`](dev/handoff/SKILL.md) | Compact the current conversation into a handoff document for another agent to pick up. |
| [`neat-freak`](dev/neat-freak/SKILL.md) | Knowledge and governance closeout: reconcile project docs, rule files (CLAUDE.md/AGENTS.md), authorized ag |
| [`nuxt`](dev/nuxt/SKILL.md) | Nuxt full-stack Vue framework with SSR, auto-imports, and file-based routing. Use when working with Nuxt apps, server routes, useFetch, middleware, or hybrid re |
| [`plan`](dev/plan/SKILL.md) | Write a markdown plan to .hermes/plans/; no execution. |
| [`popular-web-designs`](dev/popular-web-designs/SKILL.md) | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. |
| [`project-context-discovery`](dev/project-context-discovery/SKILL.md) | - Treat names such as “文档”, “资料”, and “computer” as clues, not guaranteed literal paths. |
| [`prompt-log`](dev/prompt-log/SKILL.md) | Extract conversation transcripts from AI coding session logs (Clawdbot, Claude Code, Codex). Use when asked to export prompt history, session logs, or transcrip |
| [`reference-driven-frontend-prototyping`](dev/reference-driven-frontend-prototyping/SKILL.md) | - “主体布局像 A，整体元素风格像 B” |
| [`requesting-code-review`](dev/requesting-code-review/SKILL.md) | Pre-commit review: security scan, quality gates, auto-fix. |
| [`self-improving-agent`](dev/self-improving-agent/SKILL.md) | A universal self-improving agent that learns from ALL skill experiences. Uses multi-memory architecture (semantic + episodic + working) to continuously evolve t |
| [`simplify-code`](dev/simplify-code/SKILL.md) | Parallel 4-agent cleanup of recent code changes. |
| [`sketch`](dev/sketch/SKILL.md) | Throwaway HTML mockups: 2-3 design variants to compare. |
| [`subagent-driven-development`](dev/subagent-driven-development/SKILL.md) | Execute plans via delegate_task subagents (2-stage review). |
| [`systematic-debugging`](dev/systematic-debugging/SKILL.md) | 4-phase root cause debugging: understand bugs before fixing. |
| [`test-driven-development`](dev/test-driven-development/SKILL.md) | TDD: enforce RED-GREEN-REFACTOR, tests before code. |
| [`test-script-standards`](dev/test-script-standards/SKILL.md) | Treat rules marked **必须** as hard requirements. Apply **推荐** rules unless the repository |
| [`typescript`](dev/typescript/SKILL.md) | TypeScript 编码规范、代码生成、代码审查、JavaScript 转 TypeScript、React TSX、 |
| [`ui-ux-pro-max`](dev/ui-ux-pro-max/SKILL.md) | UI/UX design intelligence for web and mobile. Searchable local database with 84 styles, 192 color palettes, 74 font pairings, 192 product types, 98 UX guideline |
| [`vue-best-practices`](dev/vue-best-practices/SKILL.md) | MUST be used for Vue.js tasks. Strongly recommends Composition API with script setup and TypeScript as the standard approach. Covers Vue 3, SSR, Volar, vue-tsc. |
| [`vue-component-refactoring`](dev/vue-component-refactoring/SKILL.md) | Use when refactoring Vue/Nuxt components or UI panels. |
| [`vue-ui-component-patterns`](dev/vue-ui-component-patterns/SKILL.md) | Use when debugging Vue/Nuxt hover cards or panel collapse. |
| [`writing-plans`](dev/writing-plans/SKILL.md) | Write implementation plans: bite-sized tasks, paths, code. |

<a id="lifestyle"></a>
## 生活管理相关 (lifestyle)

| Skill | 说明 |
|-------|------|
| [`cat-care`](lifestyle/cat-care/SKILL.md) | - Playing with curtains: exploration/hunting/climbing impulse; prioritize physical prevention (tie/clip curtains up, sec |
| [`daily-report-writer`](lifestyle/daily-report-writer/SKILL.md) | Write or update a Chinese daily work report from ~/daily/YYYY/MM/DD.md and coding-agent conversations. Use  |
| [`gamer-news`](lifestyle/gamer-news/SKILL.md) | Fetch and summarize the latest video game news from major gaming outlets (IGN, Kotaku, GameSpot, Polygon, Eurogamer, Rock Paper Shotgun, VG247, Gematsu, PlaySta |

<a id="research"></a>
## 调研报告类 (research)

| Skill | 说明 |
|-------|------|
| [`codebase-to-tutorial`](research/codebase-to-tutorial/SKILL.md) | 把本地代码库或 GitHub 仓库整理成面向人的中文阅读教程，解释核心概念、关键流程和源码阅读顺序。用户要求“代码库转教程”“为新人讲解项目”“生成代码阅读教程”或提到 Codebase to Tutorial 时 |
| [`github-repository-research`](research/github-repository-research/SKILL.md) | Research and compare GitHub repositories: popularity, activity, positioning, README summaries, and market/category fit. |
| [`huashu-md-html`](research/huashu-md-html/SKILL.md) | 花叔的「md/html/docx 多向流水线」skill，四个能力 + 两种模式：(1) 用Microsoft markitdown把任意文件（PDF/DOCX/PPTX/XLSX/HTML/图片/音… |
| [`humanizer-zh`](research/humanizer-zh/SKILL.md) | 去除文本中的 AI 生成痕迹。适用于编辑或审阅文本，使其听起来更自然、更像人类书写。 |
| [`hv-analysis`](research/hv-analysis/SKILL.md) | 横纵分析法（Horizontal-Vertical Analysis）深度研究Skill。由数字生命卡兹克提出，融合了索绪尔的历时-共时分析、社会科学的纵向-横截面研究设计、商学院案例研究法与竞争战略… |
| [`khazix-writer`](research/khazix-writer/SKILL.md) | 数字生命卡兹克（Khazix）的公众号长文写作skill。当用户需要撰写公众号文章、写稿子、续写文章、根据素材产出长文时使用。触发词包括但不限于：写文章、写稿子、帮我写、续写、扩写、公众号文章、长文、… |
| [`my-repo-story`](research/my-repo-story/SKILL.md) | 多代码仓库自动化安全拉取、24小时变更分析与技术演进故事复盘技能。提供核心约束、位置规范与叙事要求，由高级模型自主完成多仓库状态排查、冲突防护、提交考古与演进复盘。 |
| [`repo-story-time`](research/repo-story-time/SKILL.md) | Generate a comprehensive repository summary and narrative story from commit history |
| [`taste-project`](research/taste-project/SKILL.md) | 阅读代码仓库并按约束产出分析报告。用户想初步了解一个项目仓库、或想深入了解仓库里的某一个子能力时使用；用户只丢来一个仓库链接或目录、没说具体要什么时也用本 skill。 |

