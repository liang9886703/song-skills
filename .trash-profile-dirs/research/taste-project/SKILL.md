---
name: taste-project
description: 阅读代码仓库并按约束产出分析报告。用户丢来仓库链接或目录时使用。
---

# 阅读项目仓库

本 skill 用来阅读代码仓库，并根据用户的需要读取对应的约束文件，再按约束产出分析报告。

## 如何选择约束

先判断用户的需要，再读对应的约束文件：

- **初步了解整个项目仓库** → 读 `references/first-understand-project-repository.md`
- **了解仓库里的一个子能力** → 读 `references/one-ability-analyze.md`
- **用户只丢了一个链接（没说具体要什么）** → 默认按初步了解处理，读 `references/first-understand-project-repository.md`

## 默认目录约定

### 代码仓库

- 默认代码根目录是 `$HOME/github/`，不要把用户目录硬编码成某个具体用户名。
- 用户给出本地代码目录时，直接读取该目录。
- 用户只给出 GitHub 仓库链接时，把仓库克隆到 `$HOME/github/<仓库名>/`，之后从这里读取代码；不要下载到临时目录、`$HOME/code/` 或当前工作区。
- 用户只给出项目名、没有给路径时，先到 `$HOME/github/` 下查找对应仓库。
- 目标仓库目录已存在时，先核对它是否对应同一个远程仓库，再复用已有目录，不要另建重复副本。
- 私有仓库优先复用现有 `gh` 登录或 SSH 凭据，不要要求用户重复提供 token。
- 克隆出现超时、`unexpected disconnect` 或长时间无进展时，不要原样重试：先检查系统代理是否没有传递给 Git；如用户正在使用本地代理，将有效的 HTTP/HTTPS 代理显式传给 Git 后重试。
- 仓库历史过大且任务只需要阅读当前代码时，可以改用 `--depth 1 --single-branch --filter=blob:none` 获取默认分支当前版本，但完成后必须明确说明这是浅克隆；需要研究历史时再对对应仓库补全历史。
- 克隆完成后必须逐个验证远程地址、当前分支、`HEAD` 可解析且工作区干净，不能只根据克隆命令退出状态判断成功。

### 调研文档

- 默认只产出 Markdown（`.md`）文档，并写入用户指定的路径；用户未指定路径时，才按下面的默认目录约定确定路径。
- 除非用户当次明确要求，否则不要生成 PDF、HTML、DOCX、图片或其他导出版本，也不要因为历史偏好、其他 skill 或常见交付习惯而额外生成这些产物。
- 默认文档根目录是 `$HOME/code/`。
- 所有调研文档都必须放进 `$HOME/code/` 下的一个语义明确的子文件夹，禁止把 Markdown、PDF、图片或其他调研产物直接写在 `$HOME/code/` 根目录。
- 按能力或主题调研时，文件夹使用能力或主题名，例如 `$HOME/code/coding-agent-记忆能力/`。
- 按项目调研时，文件夹使用项目名，例如 `$HOME/code/hermes-agent/`。
- 同一项调研产生的主文档、分项目文档、图片和导出文件统一放在这个文件夹内。跨多个项目研究同一能力时，优先使用能力或主题名作为文件夹名，并把各项目文档与汇总文档放在同一文件夹中。
- 目标文件夹不存在时先创建，再写入文档。

## Coding Agent 项目分类约定

判断标准是「**本质上是产品驱动**」——是不是有用户拿来就用的产品形态（自己的 UX、入口、编排面、协作面），而不是「是否自研 agent 内核」。一个项目即使自己实现了 agent loop，只要它同时封装/编排别家 agent 或以产品形态交付，就算 Agent 产品；反过来，只提供 CLI/SDK 被调用的，就算 Coding Agent 内核。

当用户使用下面这些集合称呼时，默认按对应项目展开，不必再次询问范围：

- **Agent 产品**（产品驱动，有自己的 UX + 编排面，可能自研也可能封装其他 agent）：
  - 通用 / 终端 / 编排面：`hermes-agent`、`openclaw`、`open-design`、`warp`、`openagents`、`ruflo`
  - 围绕某个 coding agent 的增强 / 编排层：`oh-my-claudecode`、`oh-my-codex`、`oh-my-openagent`、`oh-my-pi`、`superpowers`、`claw-code`
  - 编辑器 / 笔记嵌入形态：`claudian`、`claude-obsidian`、`obsidian-claude-sidebar`
- **Coding Agent 内核**（agent 本体，CLI/SDK 形态，被上层产品调用）：`codex`、`opencode`、`pi`、`deepseek-harness`、`kimi-code`、`qwen-code`、`goose`、`maka`、`grok-build`、`cline`、`kilocode`、`SWE-agent`、`ax`
- **工具 / 内容 / 归档**（不算产品也不算内核）：`mycc`（Claude Code 泄露存档）、`codex-security`（安全工具）、`agentlab`（情报站）、`SkillSpector`（skill 扫描）、`litellm-agent-control-plane`（infra 控制面）、`NemoClaw`、`OpenShell`

这些分类用于确定默认调研范围，不代表互斥的技术定义；同一项目可能同时具备产品面和内核面（例如 warp 自带 agent 也接入别家 CLI agent）。用户明确点名、增删项目或另行限定范围时，以当次要求为准。

## 流程

1. 判断用户属于上面哪种需要。
2. 读取对应的约束文件。
3. 按默认目录约定确定或准备代码仓库位置与调研文档文件夹。
4. 按约束文件探索仓库并产出报告。
5. 完成前检查：GitHub 链接下载的代码位于 `$HOME/github/`，所有调研产物位于 `$HOME/code/<能力、主题或项目名>/`，且没有文件直接落在 `$HOME/code/` 根目录。

## 执行要点

- **预算分配（核心教训）**：调研报告的交付物是 Markdown 文件，不是源码阅读笔记。工具调用预算大部分必须留给「写文件」和「补漏」，读源码最多占 1/3。读的时候要有明确的「停止信号」：一旦收集到「背景/问题/名词/场景/链路/结构/依赖/技术栈/元信息」这九项的骨架，立刻停止深入，开始写报告；写的过程中发现缺什么再针对性补读。
- **失控信号与急救规则（2026-09-01 claudian 调研再次复现；同日 litellm-agent-control-plane 第三次复现）**：如果在任何时刻发现「已用调用次数 ≥ 总预算一半，但报告文件一个字都还没写」，立即停止一切探索调用，下一次调用必须是 `write_file` 把当前脑中的全部信息写成报告草稿（哪怕每个章节只有两三行、带 TODO 占位）。宁可交一份标注了「未覆盖部分」的完整结构报告，也不能继续读源码赌还有预算。这个 skill 里已有本规则的前身，但三次任务（codex、claudian、litellm-agent-control-plane）都在「读 AGENTS.md / 契约文件 / routes.rs 很有意思」的循环里烧光预算——**对带 AGENTS.md/CLAUDE.md 分层文档或单文件聚合路由表（如 axum routes.rs）的仓库尤其危险**，这些文档读起来获得感强但边际信息递减极快，读完根级 AGENTS.md + 1 个分层文档（或 routes.rs 全文一遍）就必须停。litellm-agent-control-plane 的具体失控形态：已拿到 readme、compose.yaml、src/README.md、routes.rs 全部路由表后（九项骨架已齐），又花 30+ 次调用逐个追 runtime.rs / runtime_provision.rs / scheduler.rs 的函数实现——全部属于「链路图不需要的实现细节」。
- **禁止逐文件顺序遍历**：不要按 `lib.rs → mod.rs → handlers/mod.rs → config/mod.rs` 这种顺序把每个目录都翻一遍。正确顺序是：README → Cargo.toml / package.json → 顶层目录列表 → `gh api` 元信息 → 挑 2-3 个核心文件（入口 + 主循环 + 协议定义）各读 100-200 行 → 直接开写。大文件用 `search_files` 定位关键符号后只读那一小段，不要从第 1 行开始顺序读。
- **禁止同义词变体扫目录（2026-09-01 maka 调研复现）**：`ls src | grep -E "usage|pricing|stats"`、`ls src | grep -E "artifact"`、`ls src | grep -E "telemetry"` 这种「同一目录换关键词反复 ls」是逐文件遍历的变种，每次调用信息量接近零。想知道某领域有没有对应模块，一次 `search_files(target='files', pattern='*usage*')` 或直接读一个聚合文件（如 README 的能力清单、ARCHITECTURE.md 的模块表）就够了；同一目录最多列一次，后续必须用「已知文件名直接读」而不是「再列一遍确认」。
- **架构文档齐全的仓库是最危险的时间黑洞（2026-09-01 maka 调研）**：当 repo 自带 `ARCHITECTURE.md` / `docs/architecture/*.md` 时，README + ARCHITECTURE.md + package.json + `gh api` 这 4 个调用通常已经覆盖报告 9 项里的 8 项（背景/问题/场景/链路/结构/依赖/技术栈/元信息）。此时名词表直接抄架构文档的 "Parts in plain language" 表，链路图直接改写架构文档的 mermaid，**第 5-6 次调用就必须开始 `write_file`**。maka 调研中我把 ARCHITECTURE.md 的模块表读完后又花了 30+ 次调用去 packages/runtime/src 里逐个核实文件名——全部属于边际递减信息，报告一行没写。
- **工具调用预算硬上限兜底**：如果运行环境有调用次数上限（如 50 次），第 25 次调用时必须已经把报告骨架（含全部章节标题 + 已知内容 + TODO 占位）`write_file` 落盘。被截断时没有文件落盘 = 任务完全失败；有骨架落盘 = 用户至少拿到半成品。这条优先级高于上面所有「再补读一点」的冲动。
- **写报告优先用模板填空**：按 `references/first-understand-project-repository.md` 的章节顺序，每收集到一类信息就立刻在草稿里填一节，不要等全部读完再组织语言。20 分钟限时任务，前 10 分钟必须已经写出带占位符的完整骨架。
- 用户只丢来 GitHub 链接时，先 `gh api /repos/OWNER/REPO` 取元信息（star、fork、创建时间、最近推送、语言、topics），再克隆仓库。
- 克隆用浅克隆：`git clone --depth 1 --single-branch --filter=blob:none <url> $HOME/github/<repo>`，速度快、省磁盘；报告中必须注明这是浅克隆。
- 克隆后必须验证：远程地址、当前分支、`HEAD` 可解析、工作区干净。
- 仓库结构探索时，macOS 默认没有 `tree`，用 `find . -maxdepth N -not -path './.git*'` 或 `ls` 代替。
- 读大文件用 `read_file` 分批（`offset`/`limit`），不要用 `cat` 或 `head` 刷 context。
- 如果用户只说「taste project」或「读一下这个项目」，默认按 `references/first-understand-project-repository.md` 处理，不要退化成只给 star 数和 README 摘要。

## 大批量子 Agent 调研的坑（父 agent 侧）

一次性为多个仓库各起一个子 agent（如「每个产品单独出一份文档」）时，除上面的预算纪律外，父 agent 还必须注意：

- **「completed」≠ 文件已写**：子 agent 状态为 completed 也可能只返回了失败摘要（如 `API call failed: Connection error`、`max_iterations`）而没写文件。收尾时必须 `ls` 目标目录核对实际产物数量，不能只看 batch 回执里的 status；缺哪些就补哪些，不要整批重跑。
- **provider 持续不稳定时立刻降级**：子 agent 模型若反复 `Connection error`，不要原地重试整批（重试也大概率死在同一点）。降级路径：(a) 换稳定 provider 后重跑缺失项；(b) 父 agent 自己直接产文档（牺牲部分源码细节换完成度）；(c) 从 live transcript（`cache/delegation/live/<delegation_id>/task-N.log`）提取子 agent 已收集到的事实接力写报告——很多时候信息已足够，只是没走到写文件那步。
- **超时和并发要在派发前调**：`delegation.child_timeout_seconds` 默认 600s，完整仓库调研通常不够；用 `hermes config set delegation.child_timeout_seconds 1200` 调整（`patch`/`write_file` 工具会拒绝改 config.yaml，必须走 `hermes config set` CLI）。`max_concurrent_children` 上限之外的批次会退化为同步执行、阻塞父会话，应分批派发且每批 ≤ 上限。
- **规模失控预警（2026-09-01，35 仓库批量调研 0/35 产出事故）**：一次 fan-out 超过 ~10 个仓库调研子 agent 时，任何一个平台性问题（provider 抖动、超时过短）都会让整个批次归零。大批量任务应先跑 2-3 个试点确认端到端能产出文件，再放全量；并在派发 prompt 里重申上面「预算分配」和「骨架先落盘」两条——子 agent 不会自动继承父 agent 读过的 skill 内容。

## 参考资料索引

- `references/first-understand-project-repository.md` — 初步了解整个仓库的约束
- `references/openshell-multi-agent-payload-mechanism.md` — 案例：定位「某能力的封装/扩展机制」类问题的 grep 路径与写法（注册表、trait 边界、声明式配置 vs 代码插件、平台 API vs 仓库内部工具链的区分）
- `references/codex-repository-snapshot.md` — 案例：openai/codex 仓库的元信息、结构、核心链路速查（2026-09-01 调研），以及「预算耗尽未交付」的教训
- `references/claudian-repository-snapshot.md` — 案例：YishenTu/claudian（Obsidian 插件封装 5 家 coding agent）的元信息、provider 分层架构、事件契约、Collab/agent-runtime 设计速查（2026-09-01 调研）；同因预算耗尽未交付正式报告
- `references/litellm-agent-control-plane-snapshot.md` — 案例：LiteLLM-Labs/litellm-agent-control-plane（Rust agent 控制面：统一 API + 会话 + CRON + 记忆 + 多渠道）的元信息、compose 服务构成、runtime 适配层与路由面速查（2026-09-01 调研）；同因预算耗尽未交付正式报告
- `references/maka-repository-snapshot.md` — 案例：apache/maka（local-first agent workspace，Runtime Host + Event Log 架构）的元信息、三种运行形态、仓库结构、技术栈与依赖速查（2026-09-01 调研）；因「同义词变体扫目录」耗尽预算未交付正式报告