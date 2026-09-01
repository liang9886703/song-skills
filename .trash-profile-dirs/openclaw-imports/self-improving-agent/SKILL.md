---
name: self-improvement
description: "Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks."
metadata:
  openclaw:
    requires:
      env:
        - CLAUDE_TOOL_OUTPUT
---

# Self-Improvement Skill

将经验与错误记录到 Markdown 文件中，用于持续改进。后续编码代理可以把这些记录转化为修复动作，高价值经验再提升到项目记忆中。

## 快速参考

| 场景         | 动作                                                                                  |
| ---------- | ----------------------------------------------------------------------------------- |
| 命令/操作失败    | 记录到 `.learnings/ERRORS.md`                                                          |
| 用户纠正你      | 记录到 `.learnings/LEARNINGS.md`，分类为 `correction`                                      |
| 用户需要缺失能力   | 记录到 `.learnings/FEATURE_REQUESTS.md`                                                |
| API/外部工具失败 | 记录到 `.learnings/ERRORS.md`，附上集成细节                                                   |
| 知识过时       | 记录到 `.learnings/LEARNINGS.md`，分类为 `knowledge_gap`                                   |
| 发现更优方案     | 记录到 `.learnings/LEARNINGS.md`，分类为 `best_practice`                                   |
| 简化/加固的重复模式 | 在 `.learnings/LEARNINGS.md` 记录或更新，带 `Source: simplify-and-harden` 和稳定 `Pattern-Key` |
| 与已有条目相似    | 使用 `**See Also**` 建立关联，并考虑提高优先级                                                     |
| 广泛适用的经验    | 提升到 `CLAUDE.md`、`AGENTS.md` 和/或 `.github/copilot-instructions.md`                   |
| 工作流改进      | 提升到 `AGENTS.md`（OpenClaw 工作区）                                                       |
| 工具注意事项     | 提升到 `TOOLS.md`（OpenClaw 工作区）                                                        |
| 行为模式       | 提升到 `SOUL.md`（OpenClaw 工作区）                                                         |

## OpenClaw 配置（推荐）

OpenClaw 是此 skill 的主要运行平台。它使用基于工作区的提示注入和自动 skill 加载。

### 安装

**通过 ClawdHub（推荐）：**
```bash
clawdhub install self-improving-agent
```

**手动安装：**
```bash
git clone https://github.com/peterskoett/self-improving-agent.git ~/.openclaw/skills/self-improving-agent
```

该版本为适配 OpenClaw 的重制版，源自仓库：
https://github.com/pskoett/pskoett-ai-skills
https://github.com/pskoett/pskoett-ai-skills/tree/main/skills/self-improvement

### 工作区结构

OpenClaw 会在每个会话中注入以下文件：

```
~/.openclaw/workspace/
├── AGENTS.md          # 多代理工作流、委派模式
├── SOUL.md            # 行为准则、人格、原则
├── TOOLS.md           # 工具能力、集成注意事项
├── MEMORY.md          # 长期记忆（仅主会话）
├── memory/            # 每日记忆文件
│   └── YYYY-MM-DD.md
└── .learnings/        # 本 skill 的日志文件
    ├── LEARNINGS.md
    ├── ERRORS.md
    └── FEATURE_REQUESTS.md
```

### 创建学习日志文件

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

然后创建日志文件（或从 `assets/` 拷贝）：
- `LEARNINGS.md`：纠正、知识缺口、最佳实践
- `ERRORS.md`：命令失败、异常
- `FEATURE_REQUESTS.md`：用户请求的新能力

### 提升目标

当经验被证明具有普适性时，将其提升到工作区文件：

| 经验类型 | 提升到 | 示例 |
|---------------|------------|---------|
| 行为模式 | `SOUL.md` | "保持简洁，避免免责声明" |
| 工作流改进 | `AGENTS.md` | "长任务拆分为子代理" |
| 工具注意事项 | `TOOLS.md` | "Git push 前需先配置鉴权" |

### 跨会话通信

OpenClaw 提供以下工具，在不同会话间共享经验：

- **sessions_list**：查看活跃/近期会话
- **sessions_history**：读取其他会话的对话记录
- **sessions_send**：把经验发送给其他会话
- **sessions_spawn**：启动子代理做后台工作

### 可选：启用 Hook

用于会话开始时自动提醒：

```bash
# 复制 hook 到 OpenClaw hooks 目录
cp -r hooks/openclaw ~/.openclaw/hooks/self-improvement

# 启用
openclaw hooks enable self-improvement
```

完整细节见 `references/openclaw-integration.md`。

---

## 通用配置（其他代理）

对于 Claude Code、Codex、Copilot 或其他代理，在项目中创建 `.learnings/`：

```bash
mkdir -p .learnings
```

从 `assets/` 复制模板，或手动创建带表头的文件。

### 在代理指令文件中添加引用

在 `AGENTS.md`、`CLAUDE.md` 或 `.github/copilot-instructions.md` 中加入提醒，提示自己记录经验（这是 hook 提醒以外的替代方案）。

#### 自我改进工作流

当出现错误或被纠正时：
1. 记录到 `.learnings/ERRORS.md`、`LEARNINGS.md` 或 `FEATURE_REQUESTS.md`
2. 复查并把广泛适用的经验提升到：
   - `CLAUDE.md`：项目事实与约定
   - `AGENTS.md`：工作流与自动化规则
   - `.github/copilot-instructions.md`：Copilot 上下文

## 记录格式

### Learning 条目

追加到 `.learnings/LEARNINGS.md`：

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话描述学到的内容

### Details
完整上下文：发生了什么、哪里错了、正确做法是什么

### Suggested Action
具体可执行的修复或改进动作

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001（若与已有条目相关）
- Pattern-Key: simplify.dead_code | harden.input_validation（可选，用于重复模式追踪）
- Recurrence-Count: 1（可选）
- First-Seen: 2025-01-15（可选）
- Last-Seen: 2025-01-15（可选）

---
```

### Error 条目

追加到 `.learnings/ERRORS.md`：

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
失败现象的简要描述

### Error
```
实际错误信息或输出
```

### Context
- 尝试执行的命令/操作
- 使用的输入或参数
- 如有必要，补充环境细节

### Suggested Fix
若可判断，给出可能的修复方向

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001（若为重复问题）

---
```

### Feature Request 条目

追加到 `.learnings/FEATURE_REQUESTS.md`：

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
用户想要实现的能力

### User Context
用户为什么需要它、在解决什么问题

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
如何实现、可能扩展哪些现有能力

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## ID 生成规则

格式：`TYPE-YYYYMMDD-XXX`
- TYPE：`LRN`（learning）、`ERR`（error）、`FEAT`（feature）
- YYYYMMDD：当前日期
- XXX：递增编号或随机 3 位字符（例如 `001`、`A7B`）

示例：`LRN-20250115-001`、`ERR-20250115-A3F`、`FEAT-20250115-002`

## 条目关闭

问题修复后，更新对应条目：

1. 将 `**Status**: pending` 改为 `**Status**: resolved`
2. 在 Metadata 后追加解决信息块：

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: 简述做了什么
```

其他状态值：
- `in_progress`：正在处理
- `wont_fix`：决定不处理（在 Resolution 的 notes 中写原因）
- `promoted`：已提升到 `CLAUDE.md`、`AGENTS.md` 或 `.github/copilot-instructions.md`

## 提升到项目记忆

当经验具备普适性（不是一次性修复）时，把它提升为长期项目记忆。

### 何时提升

- 经验适用于多个文件/功能
- 任何贡献者（人类或 AI）都应知道
- 能预防重复犯错
- 记录了项目特有约定

### 提升目标

| 目标 | 应放内容 |
|--------|-------------------|
| `CLAUDE.md` | 项目事实、约定、Claude 交互常见坑 |
| `AGENTS.md` | 代理工作流、工具使用模式、自动化规则 |
| `.github/copilot-instructions.md` | GitHub Copilot 的项目上下文与约定 |
| `SOUL.md` | 行为准则、沟通风格、原则（OpenClaw 工作区） |
| `TOOLS.md` | 工具能力、使用模式、集成注意事项（OpenClaw 工作区） |

### 如何提升

1. **提炼**：把经验压缩成简洁规则或事实
2. **写入**：加入目标文件对应段落（没有就创建）
3. **回写原条目**：
   - 把 `**Status**: pending` 改为 `**Status**: promoted`
   - 增加 `**Promoted**: CLAUDE.md`、`AGENTS.md` 或 `.github/copilot-instructions.md`

### 提升示例

**Learning**（详细）：
> 项目使用 pnpm workspaces。尝试 `npm install` 失败。  
> 锁文件是 `pnpm-lock.yaml`，必须使用 `pnpm install`。

**写入 CLAUDE.md**（简洁）：
```markdown
## Build & Dependencies
- 包管理器：pnpm（不是 npm）- 使用 `pnpm install`
```

**Learning**（详细）：
> 修改 API endpoint 后必须重新生成 TypeScript client。  
> 忘记执行会导致运行时类型不匹配。

**写入 AGENTS.md**（可执行）：
```markdown
## After API Changes
1. Regenerate client: `pnpm run generate:api`
2. Check for type errors: `pnpm tsc --noEmit`
```

## 重复模式检测

当要记录的内容与已有条目相似时：

1. **先搜索**：`grep -r "keyword" .learnings/`
2. **建立关联**：在 Metadata 添加 `**See Also**: ERR-20250110-001`
3. 若持续复发，**提高优先级**
4. **考虑系统性修复**：重复问题通常意味着：
   - 文档缺失（提升到 `CLAUDE.md` 或 `.github/copilot-instructions.md`）
   - 自动化缺失（写入 `AGENTS.md`）
   - 架构问题（创建技术债 ticket）

## Simplify & Harden 输入流

使用此流程摄取 `simplify-and-harden` skill 的重复模式，并转化为可持续的提示规则。

### 摄取流程

1. 从任务摘要读取 `simplify_and_harden.learning_loop.candidates`。
2. 对每个 candidate，用 `pattern_key` 作为稳定去重键。
3. 在 `.learnings/LEARNINGS.md` 检索是否已有该键：
   - `grep -n "Pattern-Key: <pattern_key>" .learnings/LEARNINGS.md`
4. 若已存在：
   - 增加 `Recurrence-Count`
   - 更新 `Last-Seen`
   - 增加相关条目/任务的 `See Also` 链接
5. 若不存在：
   - 新建 `LRN-...` 条目
   - 设置 `Source: simplify-and-harden`
   - 设置 `Pattern-Key`、`Recurrence-Count: 1`、`First-Seen`/`Last-Seen`

### 提升规则（系统提示反馈）

当以下条件全部满足时，把重复模式提升到代理上下文/系统提示文件：

- `Recurrence-Count >= 3`
- 至少出现在 2 个不同任务中
- 发生在 30 天窗口内

提升目标：
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- 适用时提升到 `SOUL.md` / `TOOLS.md`（OpenClaw 工作区级规则）

提升后的内容应写成简短“预防规则”（编码前/编码中该做什么），而不是长篇事故复盘。

## 周期性复查

在自然断点复查 `.learnings/`：

### 何时复查
- 开始新的大型任务前
- 完成功能后
- 进入曾经出过问题的区域时
- 活跃开发阶段每周一次

### 快速状态检查
```bash
# 统计待处理条目
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# 列出高优先级且待处理条目
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["

# 按 area 查找经验
grep -l "Area\*\*: backend" .learnings/*.md
```

### 复查动作
- 关闭已修复条目
- 提升可复用经验
- 关联相关条目
- 升级处理重复问题

## 触发信号

当你观察到以下信号时，自动记录：

**纠正（记录为 `correction` 分类的 learning）：**
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."
- "That's outdated..."

**功能请求（记录为 feature request）：**
- "Can you also..."
- "I wish you could..."
- "Is there a way to..."
- "Why can't you..."

**知识缺口（记录为 `knowledge_gap` 分类的 learning）：**
- 用户提供了你原本不知道的信息
- 你引用的文档已过时
- API 实际行为与你理解不一致

**错误（记录为 error）：**
- 命令返回非零退出码
- 抛出异常或堆栈
- 出现非预期输出或行为
- 超时或连接失败

## 优先级指南

| Priority | 使用场景 |
|----------|-------------|
| `critical` | 阻塞核心功能、存在数据丢失风险或安全问题 |
| `high` | 影响显著、影响常见流程、重复出现 |
| `medium` | 影响中等、存在替代方案 |
| `low` | 轻微不便、边缘场景、可选优化 |

## Area 标签

用于按代码区域过滤经验：

| Area | 范围 |
|------|-------|
| `frontend` | UI、组件、客户端代码 |
| `backend` | API、服务、服务端代码 |
| `infra` | CI/CD、部署、Docker、云资源 |
| `tests` | 测试文件、测试工具、覆盖率 |
| `docs` | 文档、注释、README |
| `config` | 配置文件、环境、设置 |

## 最佳实践

1. **立即记录**：问题刚发生时上下文最完整
2. **写清细节**：未来代理需要快速理解
3. **包含复现步骤**：尤其是错误条目
4. **关联相关文件**：便于后续修复
5. **给出具体修复建议**：不要只写“待调查”
6. **分类保持一致**：便于筛选和统计
7. **积极提升**：有价值就尽快写入 `CLAUDE.md` 或 `.github/copilot-instructions.md`
8. **定期复查**：过期经验会快速贬值

## Gitignore 选项

**仅本地保留经验**（按开发者隔离）：
```gitignore
.learnings/
```

**将经验纳入仓库**（团队共享）：
不要把 `.learnings/` 加入 `.gitignore`，经验将成为共享知识。

**混合模式**（跟踪模板，忽略条目）：
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Hook 集成

可通过代理 hooks 启用自动提醒。该功能为 **可选项**，需要你显式配置。

### 快速配置（Claude Code / Codex）

在项目中创建 `.claude/settings.json`：

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }]
  }
}
```

该配置会在每次 prompt 后注入一条“评估是否记录经验”的提醒（约增加 50-100 tokens）。

### 完整配置（含错误检测）

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/error-detector.sh"
      }]
    }]
  }
}
```

### 可用 Hook 脚本

| Script | Hook 类型 | 作用 |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | 任务后提醒评估并记录经验 |
| `scripts/error-detector.sh` | PostToolUse (Bash) | 在命令错误时触发 |

详细配置与排障见 `references/hooks-setup.md`。

## 自动抽取 Skill

当某条经验足够有价值、可以复用时，使用内置辅助工具把它抽取成独立 skill。

### Skill 抽取标准

满足任一条件即可考虑抽取：

| 条件 | 说明 |
|-----------|-------------|
| **Recurring** | 有 2 个及以上相似问题的 `See Also` 链接 |
| **Verified** | 状态为 `resolved` 且修复可用 |
| **Non-obvious** | 需要真实调试/调查才能得出 |
| **Broadly applicable** | 非项目专属，可跨代码库复用 |
| **User-flagged** | 用户明确说“把这个保存为 skill”或类似表达 |

### 抽取流程

1. **识别候选**：条目满足抽取标准
2. **运行脚本**（或手动创建）：
   ```bash
   ./skills/self-improvement/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improvement/scripts/extract-skill.sh skill-name
   ```
3. **完善 SKILL.md**：把学习内容填入模板
4. **更新 learning 条目**：状态改为 `promoted_to_skill`，并补 `Skill-Path`
5. **验证**：在新会话读取该 skill，确认其自包含

### 手动抽取

若你更倾向手工创建：

1. 创建 `skills/<skill-name>/SKILL.md`
2. 使用 `assets/SKILL-TEMPLATE.md` 模板
3. 遵循 [Agent Skills spec](https://agentskills.io/specification)：
   - YAML frontmatter 包含 `name` 与 `description`
   - 名称需与文件夹一致
   - skill 文件夹内不放 README.md

### 抽取触发信号

以下信号通常说明应将经验升级为 skill：

**在对话中：**
- "Save this as a skill"
- "I keep running into this"
- "This would be useful for other projects"
- "Remember this pattern"

**在 learning 条目中：**
- 有多个 `See Also` 关联（重复问题）
- 高优先级且已 `resolved`
- 分类为 `best_practice` 且具备广泛适用性
- 用户对方案给出正向反馈

### Skill 质量门槛

抽取前请确认：

- [ ] 方案已验证可用
- [ ] 脱离原始上下文也能读懂描述
- [ ] 代码示例自包含
- [ ] 不含项目特定硬编码值
- [ ] 符合命名规范（小写、连字符）

## 多代理支持

该 skill 支持不同 AI 编码代理，通过各自方式激活。

### Claude Code

**激活方式**：Hooks（UserPromptSubmit、PostToolUse）  
**配置方式**：在 `.claude/settings.json` 配置 hooks  
**检测方式**：通过 hook 脚本自动检测

### Codex CLI

**激活方式**：Hooks（与 Claude Code 同模式）  
**配置方式**：在 `.codex/settings.json` 配置 hooks  
**检测方式**：通过 hook 脚本自动检测

### GitHub Copilot

**激活方式**：手动（无 hook 支持）  
**配置方式**：在 `.github/copilot-instructions.md` 添加：

```markdown
## Self-Improvement

解决非显而易见的问题后，考虑记录到 `.learnings/`：
1. 使用 self-improvement skill 的格式
2. 用 See Also 关联相关条目
3. 将高价值经验提升为 skills

在聊天中提问："Should I log this as a learning?"
```

**检测方式**：会话结束时手动复查

### OpenClaw

**激活方式**：工作区注入 + 代理间消息  
**配置方式**：见上文 “OpenClaw 配置”  
**检测方式**：通过会话工具与工作区文件

### 与代理无关的通用建议

不论使用哪种代理，遇到以下情况都应启用自我改进流程：

1. **发现了非直观问题**：解法不是立刻得到
2. **纠正了自己**：初始方案有误
3. **学到项目约定**：发现未文档化规则
4. **遇到异常错误**：尤其是定位困难的问题
5. **找到更优路径**：明显优于最初做法

### Copilot Chat 集成

对 Copilot 用户，可在提示词中加入：

> After completing this task, evaluate if any learnings should be logged to `.learnings/` using the self-improvement skill format.

或使用快捷提示：
- "Log this to learnings"
- "Create a skill from this solution"
- "Check .learnings/ for related issues"
