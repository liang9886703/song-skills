# scheduler

**AI 信息晨报**定时任务的交接包，给别的 agent 接手用。

这里的 `ai-morning-digest/` 是一个完整可用的 skill（自包含，内部 `reference/` 带齐了写作和仓库分析的约束），但它放在 `scheduler/` 而不是 `skills/`：这是交接物，不该参与 skillshare 同步，也不该被自动分发到各个 agent。用的时候把 `ai-morning-digest/` 整个拷到目标 agent 能加载的位置即可。

| 路径 | 作用 |
| --- | --- |
| [`ai-morning-digest/SKILL.md`](ai-morning-digest/SKILL.md) | skill 本体：流程、上限、组织方式、成本路由 |
| [`ai-morning-digest/HANDOFF.md`](ai-morning-digest/HANDOFF.md) | 为什么这么设计、已知脆弱点、接手步骤 |
| [`ai-morning-digest/routine.md`](ai-morning-digest/routine.md) | 定时定义（cron / 时区 / 容差）与可直接粘贴的 prompt |
| `ai-morning-digest/reference/` | 单篇写法、仓库分析约束 |
| `ai-morning-digest/templates/` | 三栏 HTML 壳、填法、填完自检脚本 |
| `ai-morning-digest/examples/` | 一份真成品 HTML、候选清单、fill-notes |

产物长什么样，直接打开 [`ai-morning-digest/examples/2026-11-04-report.html`](ai-morning-digest/examples/2026-11-04-report.html)。
