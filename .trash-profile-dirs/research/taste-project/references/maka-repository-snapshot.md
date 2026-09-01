# maka 仓库速查（2026-09-01 调研）

> 本次调研因工具调用预算耗尽未能交付正式报告，此处保留已验证的元信息与核心发现，供后续补写或复用。

## 元信息

- GitHub: `apache/maka`（Apache Incubator 孵化中）
- Stars: 4368 | Forks: 406 | Open issues: 385
- Created: 2026-05-27 | Pushed: 2026-09-01（高度活跃）
- Language: TypeScript
- License: Apache-2.0
- Topics: agent-runtime, ai-agent, electron, local-first, event-sourcing, llm, tool-use

## 一句话定位

Local-first Agent workspace：在本地机器上通过统一的 Runtime Host 运行 agent，把模型消息、工具调用、工具结果、权限决策、终止事件全部记录为 append-only Runtime Event Log。

## 运行形态（Surfaces）

| 入口 | 用途 |
|---|---|
| Desktop | Electron + React，日常交互、文件/Artifact 工作流、模型与权限设置 |
| TUI / CLI | `maka` / `maka run`，与 Desktop 共享 workspace 和模型连接 |
| Eval | `maka eval run <spec> --out <dir>`，可复现的 benchmark 实验 |

## 核心架构

```
Desktop / TUI / CLI / Bot / Eval → Runtime Host → SessionManager → AgentRun + RuntimeKernel
                                                        ↓
                                          Model + Tool Runtime → Runtime Event Log
                                                        ↓
                                    Context / Session / UI / Recovery projections
```

- Runtime Host 是唯一执行权威，所有客户端不拥有自己的 Runtime。
- Runtime Event Log 是语义事实源；State(t) = Project(RuntimeEvents[0..t])。
- Agent Graph 用 child Session 作为 operator 容器、AgentRun 作为 activation，复用同一 Runtime 而非第二运行时。

## 仓库结构（主线相关）

```
maka/
├── apps/desktop/              # Electron main/preload/renderer + React UI
├── packages/
│   ├── core/                  # Session/AgentRun/RuntimeEvent/Permission 纯契约
│   ├── storage/               # SQLite 存储、Artifact、Usage、Credential、Telemetry
│   ├── runtime/               # SessionManager、AgentRun、模型适配、工具、沙箱、恢复、Graph
│   ├── runtime-host/          # 唯一托管执行权威、公开协议、Host Kernel/Composition/Domain Module
│   ├── eval/                  # Experiment → Cell → Attempt → Result，Harbor/Pier 执行器适配
│   ├── cli/                   # TUI 与 maka / maka eval 入口
│   ├── computer-use/          # Computer Use 后端与协议
│   ├── mcp/                   # MCP 工具发现、OAuth、凭据协调
│   └── ui/                    # 共享 React 组件
├── native/
│   ├── gitoxide-helper/       # Rust Git 辅助
│   └── runtime-host-peer/     # Rust cdylib，Host 本地 peer
└── docs/architecture/         # 架构草案（Runtime Core、Runtime Host、Agent Graph、Recovery、Compaction 等）
```

## 技术栈

- 语言：TypeScript（主）、Rust（native 辅助）
- 桌面：Electron 43 + React 19
- 模型层：Vercel AI SDK（`ai` 7.0.70），适配 Anthropic / OpenAI / OpenAI-Compatible / Google / Cohere / Open Responses
- 协议/通信：ws（WebSocket）、zod 4
- 存储：SQLite（通过 storage 包封装）
- CLI 发布：npm 包 `maka-agent@next`（公网 beta）

## 依赖

- 必须联网调用第三方模型 API（Anthropic/OpenAI/Google/Cohere 或兼容网关）。
- 可选本地模型连接。
- 内置工具 Read/Write/Edit/Glob/Grep/Bash；Grep 依赖系统 `ripgrep`。
- 可选 Computer Use、Catalog Skills、MCP 工具、IM Bot（Telegram/Slack/Discord/QQ/微信/企业微信/钉钉/飞书）。
- Eval 可对接外部 Harbor/Pier 执行器，但 Maka subject 必须走 Runtime Host。

## 关键约束（写报告时可直接引用）

- 本地优先：数据默认留在本地 `runtime.sqlite` + `credential-vault.json`。
- 沙箱边界：越出沙箱的工具必须用户批准；`request_sandbox_boundary` 可请求最小扩张。
- 崩溃恢复：Runtime Event Log 支持 crash recovery；Safe resume 默认关闭，需 `MAKA_RUNTIME_SAFE_BOUNDARY_RESUME=1`。
- 上下文压缩：compaction 只改变 provider input projection，不删除历史。
- Eval 边界：Maka subject 必须通过 Runtime Host 执行；external subject 用 generic adapter；result kernel 只含 score/usage/cost/duration/status/artifacts。

## 教训

本次任务失败原因：在 packages/runtime/src 目录里用 `ls | grep` 反复扫描同义词变体（artifact/usage/pricing/telemetry/graph/recovery 等），30+ 次调用边际递减，报告未写。正确做法：README + ARCHITECTURE.md + package.json + `gh api` 4 个调用后应立即开始写报告。
