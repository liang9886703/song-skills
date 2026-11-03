---
name: batch-subagent-delegation
description: Use when fan-out delegating many parallel subagent tasks.
---

# 批量子 Agent 委派（Batch Subagent Delegation）

当用户要求"给 N 个项目/目标各起一个子 agent 分别完成同类任务（调研、写文档、审计、扫描）"时使用。核心目标：避免整批失败、避免会话被同步阻塞卡住、避免把"已派发"误报为"已完成"。

## 触发信号

- 用户一句话里给出 N ≥ 3 个同类目标 + "每个起子 agent / 并行跑 / 分别产出文档"
- 用户指定了单个子 agent 的超时时长（如"每个 20 分钟"）
- 任务本身机械重复，但单个子任务需要读代码/读文档/写报告（即不是纯 terminal 循环能干的）

## 派发前检查清单（按顺序做，不要跳）

1. **核对超时配置**
   - `delegate_task` 子 agent 超时由 Hermes `config.yaml` 的 `delegation.child_timeout_seconds` 控制，默认通常 600s。
   - 用户要求的时长若超过默认值，先用 `hermes config set delegation.child_timeout_seconds <秒>` 提升，再派发。
   - **该配置是安全敏感文件**：`patch` / `write_file` 直接改会被拒写，必须走 `hermes config set` CLI。

2. **核对并发上限**
   - `delegation.max_concurrent_children` 决定后台并发数。
   - 单批 tasks 数量超过上限时，**整批会降级为同步阻塞执行**，卡住当前会话直到跑完——这会瞬间烧掉你的迭代预算。
   - 需要 N 个并发时，先 `hermes config set delegation.max_concurrent_children N` 再派发；或者把任务拆成 ≤ 上限的多个批次串行派发。

3. **验证 provider 连通性**
   - 批量委派会放大 provider 抖动：单个连接失败 × N 个子 agent = 整批白跑。
   - 派发前用一次轻量调用（如 `curl -s -o /dev/null -w '%{http_code}' <provider 健康端点>` 或一次最小 LLM 调用）确认当前 model/provider 可用。
   - 401/403 不代表"挂"——那只是鉴权，说明网络通；**Connection error / timeout 才是真的挂**。

4. **确认产物路径与命名**
   - 所有子 agent 写入的目录必须预先存在（或在 goal 里让子 agent 自己 `mkdir -p`）。
   - 文件名规则在 goal 里写死（`<项目名>.md`），不要让子 agent 自由发挥。

## 失败识别与兜底

- **整批 `API call failed after 3 retries: Connection error`** = provider 层问题，不是任务问题。继续用同一 provider 重试只会重复烧超时预算。两条路：
  a. 换 provider/model 重跑（改 `delegation.provider` / `delegation.model` 或主 model）；
  b. 降级为父 agent 自己直接执行（牺牲并行度换完成度）。
- **部分超时 + 部分连接失败混合**：通常是 provider 抖动 + 超时过短叠加。先提超时，再换/重试 provider。
- **兜底交付原则**：批量委派失败时，向用户明确报告"实际产出 X/N"，列出可选替代路径（父 agent 自己写 / 换模型重跑 / 缩小范围先跑核心子集），**不要把"已派发 N 个"汇报成"已完成 N 个"**。

## 完成后核对（必做）

- 批量结束后，父 agent 必须 `ls` 目标目录核对实际文件数，再向用户汇报。
- 子 agent 自述"已写入"不算数——它可能在写文件前一轮 API 调用就断连了。
- 缺失的产物单独补跑（小批量重试）或父 agent 自己写，不要再次整批重发。

## 反模式（不要这么做）

- ❌ 不看 `child_timeout_seconds` 就按用户要求的"每个 20 分钟"直接派发
- ❌ 一批塞超过 `max_concurrent_children` 的 tasks，让批次退化成同步阻塞
- ❌ 看到 Connection error 还用同一 provider 反复重发同一批
- ❌ 仅凭子 agent summary 就汇报"全部完成"，不核对文件系统
- ❌ 试图用 patch 工具直接改 `~/.hermes/**/config.yaml`（会被拒写）

## 相关

- `software-development/subagent-driven-development` — 单计划驱动的 2-stage 子 agent 开发流程
- `devops/kanban-orchestrator` — Kanban 场景的拆解与反模式
- `research/taste-project` — 项目调研报告的内容约束（配合本 skill 的派发模式使用）
