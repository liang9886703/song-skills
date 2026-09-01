# claudian 仓库速查快照（2026-09-01 调研）

YishenTu/claudian — Obsidian 插件，把 coding agent（Claude Code / Codex / Grok / OpenCode / Pi）嵌入笔记 vault。本文件是会话中逐文件验证过的信息快照，供写报告或二次调研直接引用，避免重读源码。注意：当时因工具预算耗尽，正式报告未交付——本文件本身是「先写草稿」规则的产物。

## 元信息（gh api 实测）

- stars 15,091 / forks 992 / open issues 68
- 创建于 2025-12-05，最近 push 2026-09-01，878 commits，tag 2.2.5
- 语言 TypeScript，topics: claude-code, codex, ide, obsidian, obsidian-plugin, productivity
- manifest id 为 `realclaudian`（社区插件名），desktop only，minAppVersion 1.13.0
- 源码规模：788 个 ts 文件 / ~205k 行 / src 9.3MB

## 一句话定位

Obsidian 社区插件：vault 即 agent 工作目录，侧边栏聊天 + 内联编辑（word-level diff）+ 多 tab 会话 + 实验性 Collab 模式（LAN/Cloud 协作，基于 Git + 独立协议包 `@claudian-collab/protocol`）。**自己不做 agent 内核**，全部通过子进程适配各家 CLI/SDK：claude 用 `@anthropic-ai/claude-agent-sdk`，codex 用 `codex app-server`（stdio JSON-RPC 2.0），grok 用 `grok agent --no-leader stdio`（ACP），opencode 用 `opencode acp`（ACP），pi 用 `pi --mode rpc`。

## 分层架构（依赖方向严格）

```
main.ts (组合根) → app/ (会话仓储、设置、Collab 子系统、agent-runtime HTTP)
                 → features/ (chat / inline-edit / collab / settings UI)
                 → providers/ (claude/codex/grok/opencode/pi 适配 + acp 共享传输)
                 → core/ (provider 中立契约：execution/providers/collab/storage)
```

- `core/execution/`：`ProviderExecutionBackend`（廉价注册入口）→ `createSession()` → `ProviderExecutionSession.execute(request)` 返回 `ProviderExecutionRun { events: AsyncIterable, cancel() }`。事件统一为 `ProviderExecutionEvent`：turn_started / text_delta / thinking_delta / tool_started/output/completed / usage_updated / turn_completed / cancelled / execution_error，事件 scope 分 requested/background/session 三类。
- `core/providers/`：`ProviderRegistry` + `ProviderWorkspaceRegistry` 静态注册表；`ProviderCapabilities`（planMode/rewind/fork/commands/images/instructionMode/turnSteer/reasoningControl）声明各 provider 差异，禁止假设 provider parity。
- 5 个 provider 目录内部结构同构：`execution/`（会话绑定）、`runtime/`（进程/协议）、`history/`（原生 transcript 只读回放：claude 读 `~/.claude/projects/`，codex 读 `~/.codex/sessions/` JSONL，opencode 读 SQLite，pi 读 JSONL）、`app|commands|agents/`（workspace 目录发现）、`storage/`（provider 自有配置）。
- `features/chat/`：TabManager/TabSession/TabLifecycle（provisional→cold→warm→closing）+ ChatExecutionCoordinator（每 tab 一个执行绑定）+ WarmExecutionPool（应用级 LRU，默认 5、上限 10 个 warm agent 进程）。
- `app/agent-runtime/`：`LocalAgentRuntimeHttpServer`（127.0.0.1，`/v1/rpc`，64KB body 上限）暴露 Collab 操作给主 agent——系统提示注入 RPC endpoint，agent 用 `runtime.operations.list/get` 自发现操作，再走 `collab.*` 方法读写 Collab 状态。这是「agent 操作 Collab」的桥。
- Collab：`src/app/collab/` 极重（authority-transfer、host-transfer、join、lan、git、review、conflicts、publish 等 30+ 子目录），共享 wire 契约在独立 npm 包 `@claudian-collab/protocol`（精确版本依赖，3.3.1），LAN 走 mDNS(bonjour-service) + HTTPS + Smart HTTP Git，Cloud binding 由协议包定义。

## 持久化位置

- `.claudian/claudian-settings.json`（vault 内设置）
- `.claudian/sessions/`（会话元数据 + input ledger，设备分 namespace，legacy `.claude/sessions` 会迁移）
- 各 provider 原生 transcript 一律只读，Claudian 不改不删。

## 构建/技术栈

- TypeScript + esbuild（`scripts/build.mjs`）+ Jest 30，Node 24，obsidian API 1.13
- 运行时依赖：claude-agent-sdk、@claudian-collab/protocol、@modelcontextprotocol/sdk、CodeMirror 6（内联编辑 diff）、@pierre/diffs、sql.js（opencode 历史）、ws、bonjour-service、node-forge
- 10 个 i18n locale；stylelint + eslint（obsidianmd 插件）

## 写作时可直接用的判断

- 分类：按 taste-project 的分类约定属于「Agent 产品 — 编辑器/笔记嵌入形态」。
- 解决的问题：coding agent 原本活在终端，与笔记/知识库割裂；用户要在 Obsidian 里写文档时让 agent 直接读写 vault 文件，不用切窗口、不用手动复制路径。
- 用户故事主线：装插件 → 装任一 CLI → 侧边栏开聊 → agent 读写 vault；选中文本热键内联编辑；@提及文件/subagent；/斜杠命令与 skills；Shift+Tab Plan Mode；Collab 模式多人共享项目。
