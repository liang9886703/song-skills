# LiteLLM Agent Control Plane 仓库快照（2026-09-01 调研）

来源：`$HOME/github/litellm-agent-control-plane/`（本地已有完整克隆，非浅克隆）。本文件记录已核实的事实，供下次调研该仓库直接引用；同因预算耗尽未交付正式报告（详见 SKILL.md「失控信号与急救规则」第三次复现记录）。

## 仓库元信息

- GitHub: `LiteLLM-Labs/litellm-agent-control-plane`（https://github.com/LiteLLM-Labs/litellm-agent-control-plane）
- 描述："1 place to call all your agents - OpenCode, Hermes, Claude Managed Agents, Cursor Agents API, DeepAgents."
- star 1263 / fork 142；创建于 2026-05-07；最近推送 2026-06-20；主语言 Rust；默认分支 main
- topics: agent-builder, agent-platform, ai-gateway, claude-code, codex, litellm, sandbox 等
- crate 名 `litellm-rust`，二进制名 `lite`（`src/main.rs`），MIT license

## 一句话定位

infra 控制面（Agent 产品分类约定中属「工具/内容/归档」）：一个 Rust 单体服务 + 内嵌 Next.js UI + Postgres，坐在各种 agent runtime 之上，提供统一 API 来创建/运行 agent、会话管理、CRON 定时、记忆、多渠道（UI/API/Slack/Teams/Google Chat/webhook）触达。

## 运行方式与包含的服务

Docker Compose 一键起（`docker compose --profile opencode up`），包含：

- `postgres`（postgres:16-alpine，库 `litellm_agents`）
- `lap`（Rust 服务本体，端口 4000，master key 默认 `sk-local`）
- 模板 runtime profiles：`opencode` / `deepagents` / `hermes` / `openclaw`（各自 + `register-*` sidecar，通过 `POST /api/runtime-harnesses` 把自己注册成 `local-<name>`）
- `templates/<name>/` 每个都是自包含 server，把对应 agent runtime 包装成 Anthropic Managed Agents API spec，LAP 通过 `api_base`/`api_key` 驱动，无需改 LAP 代码。`templates/manifest.json` 列出全部可安装模板（含 pydantic-deepagents）。

## 技术栈与依赖

- 后端 Rust 2021：axum 0.8 + tokio + sqlx(postgres) + reqwest(rustls) + serde + clap；错误统一 `GatewayError`（`src/errors.rs`）
- 前端 `src/ui/`：Next.js 16 + React 19（静态导出后由 Rust 服务托管，Dockerfile 三阶段构建：node 构建 UI → rust 构建 lite → debian slim 运行时）
- 数据库必需：无 `DATABASE_URL` 时 sessions/agents/credentials 路由返回 503
- 沙箱：`src/agents/sandboxes/` 支持 e2b（默认 provider）和 local；harness 目前只有 `claude_code`（`src/agents/harnesses/`，拼 shell 命令在沙箱里 `npm install @anthropic-ai/claude-agent-sdk` 后跑 node 脚本）
- Runtime 适配层：`src/sdk/providers/` 下 anthropic / cursor / elastic / gemini 四个 RuntimeAdapter（`src/sdk/providers/base/runtime.rs` 定义 trait），`src/sdk/agents/` 是 `Lap` 客户端 + 归一化事件类型。AgentRuntime 枚举：ClaudeManagedAgents / Cursor / GeminiAntigravity / ElasticAgentBuilder

## 源码结构（主线相关）

- `src/main.rs` — 入口，构建 provider registry + router，`spawn` routine scheduler（60s 轮询，`src/http/managed_agents/routines/scheduler.rs`，cron 字段存 Postgres RoutineRow）
- `src/http/routes.rs` — 全部路由表（约 50 条，单文件聚合，读一遍即知 API 面）：`/v1/messages`、`/v1/responses`、`/v1/models`、`/v1/sessions/{id}/events/stream`、静态 UI fallback
- `src/http/managed_agents/routes.rs` — 管理面路由：`/api/agents`（CRUD/pause/resume/files/memory/run/runs/logs）、`/api/agents/import/{provider}`、`/api/rules`、`/api/routines`（+trigger）、`/api/skills`、`/api/inbox`、`/api/approvals`、slack/teams/google_chat/webhook 渠道回调
- `src/http/sessions.rs` + `sessions/` 子模块 — 会话核心：`create_runtime_session` → `runtime_provision.rs`（在 provider 侧创建 agent+environment+session）→ `execute_runtime_prompt`（SDK `send_with_model` + 流式 drain）。无 runtime 的会话走 `execution.rs`：build_harness_run → sandbox.create → stream output → persist
- `src/http/runtime_resolution.rs` — 按 alias 从静态 registry 或 DB harnesses 表解析 runtime + 凭据
- `src/proxy/` — config.yaml 解析、master-key 鉴权、凭据加解密（credential_crypto）、AppState
- `src/callbacks/` — 观测性扩展点：StandardLoggingPayload → CallbackManager（litellm_db、standard_logging）
- `src/db/managed_agents/` — sqlx 仓库层：registry/runs/routines/memory/skills/rules/inbox/sessions/messages/runtime_refs/migrations 等
- `src/mcp/` — MCP server registry + streamable HTTP 路由
- `src/cli/` — `litellm-rust claude` 向导，把 Claude Code 指向本 gateway

## 九项骨架覆盖度（下次直接复用）

背景/问题/名词/场景（compose profiles + channels）/用户故事（readme 的 Create an Agent 三步 + Slack 连接流）/如何跑起来（Docker Compose，Dockerfile 也可托管部署如 Render）/整体链路（UI/API/channel → routes → session 或 managed_agents → runtime_resolution → Lap SDK → provider，或 → harness + e2b/local sandbox）/结构/依赖/技术栈/元信息 —— 全部已核实，见上。
