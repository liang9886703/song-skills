# Codex 仓库调研速查（2026-09-01 会话）

## 元信息
- `openai/codex`，Apache-2.0，Rust，约 120k stars / 18k forks
- 创建于 2025-04-13，活跃度极高
- 描述：Lightweight coding agent that runs in your terminal

## 顶层结构
- `codex-rs/`：核心 Rust workspace（90+ crate，Bazel）
- `codex-cli/`：npm 发布壳（Node 包装，分发 Rust 二进制）
- `sdk/`：python、python-runtime、typescript
- `docs/`：用户向文档

## codex-rs 关键 crate 分组
- 入口：`cli`（clap MultitoolCli，子命令 exec/review/login/mcp/mcp-server/app-server/app/sandbox/apply/resume/queue/doctor）
- TUI：`tui`（ratatui 终端 UI）
- 富客户端接口：`app-server`（JSON-RPC 2.0 over stdio/websocket/unix socket，驱动 VS Code 扩展）
- 内核：`core`（ThreadManager / CodexThread / Session / TurnContext / ModelClient）
- 协议：`protocol`（Submission{op: Op} SQ/EQ；Op 含 Interrupt/TurnInput/ExecApproval/PatchApproval/Compact/Review/Shutdown；EventMsg 约 90 变体；TurnItem 含 UserMessage/AgentMessage/Reasoning/Plan/CommandExecution/FileChange/McpToolCall/WebSearch/ContextCompaction）
- 模型/API：`codex-api`、`backend-client`、`model-provider`、`models-manager`；`client.rs` 中 ModelClient 管会话级 auth/provider，ModelClientSession 管 turn 级 WebSocket 复用 + sticky routing
- 工具：`core/src/tools/`（router/registry/orchestrator/handlers），handlers 含 unified_exec、apply_patch、plan、mcp、view_image、request_user_input、request_permissions、multi_agents_v2、code_mode、tool_search
- 沙箱：`sandboxing`、`linux-sandbox`（bubblewrap + Landlock）、`windows-sandbox-rs`（restricted token）、macOS Seatbelt（`/usr/bin/sandbox-exec`）
- 持久化：`rollout`（JSONL session 文件）、`thread-store`、`state`（SQLite via codex-state）
- MCP：`mcp-server`（暴露 Codex 为 MCP server）、`rmcp-client`（作为 MCP client 调外部 server，含 OAuth）、`codex-mcp`
- 扩展：`plugin`、`connectors`、`skills`、`hooks`、`core-plugins`、`ext`
- 其他：`exec`（非交互模式）、`exec-server`（环境抽象）、`login`（ChatGPT OAuth + API key）、`chatgpt`、`cloud-tasks`、`cloud-config`、`agent-identity`、`agent-roles`、`memories`、`ollama`、`lmstudio`、`responses-api-proxy`、`rollout-trace`、`otel`、`analytics`

## 核心请求链路（run_turn）
1. UI/app-server 把用户输入包装为 `Submission{ op: Op::TurnInput }` 推入 SQ
2. ThreadManager/CodexThread 拉到 Session，派生 RegularTask，发 TurnStarted
3. run_turn：async hooks → pre-sampling compact（token 满或模型切换）→ 解析 skills/plugins/MCP mentions → capture_step_context 拿到 StepContext（含 ToolRouter、模型设置、环境快照）→ 写历史
4. 主循环：构造 Prompt{input, tools, base_instructions} → ModelClientSession.stream() 通过 Responses API（SSE 或 WebSocket）调模型
5. 流式处理 ResponseEvent：OutputItemDone（function call → ToolCallRuntime 执行 → 结果回写历史，可能触发审批）、OutputTextDelta/ReasoningSummaryDelta（实时转成 AgentMessageContentDelta 等 EventMsg 推给 UI）、Completed（记录 token，可能进入 auto-compact 或结束 turn）
6. 模型只回 assistant message 且无后续工具调用 → 退出循环，发 TurnComplete

## 贡献的场景（产品形态）
- `codex`（默认 TUI 交互终端）
- `codex exec` / `codex review`（非交互一次性执行）
- `codex app-server`（驱动 VS Code 扩展等富客户端）
- `codex mcp-server`（把 Codex 作为 MCP 服务）
- `codex app`（macOS/Windows 桌面应用启动器）
- `codex cloud-tasks`（云端任务）
- SDK：Python / TypeScript
- 模型侧：默认 OpenAI Responses API，同时内置 ollama、lmstudio 等本地 provider

## 教训
- 本次会话把工具预算全部耗在源码阅读上，没有进入写文件阶段。以后必须：收集到九项骨架立刻停止深入，先写带占位符的完整报告，再补漏。
