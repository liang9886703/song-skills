# AI 信息晨报 · 交接说明

一句话：把一批 AI 信息源按「最近一天」抓下来，按成本分三段（低档抓取 / 高档写作 / 低档填模板）产出一份三栏 HTML 日报，工作日早上 8 点推送。

规则在 [`SKILL.md`](SKILL.md)，定时定义在 [`routine.md`](routine.md)。本文只讲为什么这么设计、哪些地方会出问题、怎么接手，不重复规则本身。

## 为什么放在 `scheduler/` 而不是 `skills/`

`scheduler/` 是交接包，不是本机在用的技能：它不参与 skillshare 同步，也不该被分发到各个 agent 的技能目录。放进 `skills/<场景>/` 会被当成常规技能同步出去，所以单独放一层。真正要用的地方，把 `ai-morning-digest/` 拷过去再按技能加载。

## 为什么是一个 skill

原先「单篇写法」和「仓库深入分析」是两个独立 skill，被晨报引用。合成一个 skill 的理由：

- 它们只有这一条使用主线，独立分发要维护两处版本，而且换环境时三个 `SKILL.md` 要同时装对才跑得起来。
- 引用改成同一目录内的相对路径后，装一个目录就够，`reference/` 里是文档不是 skill，不需要被技能系统识别。

代价是这两个能力不再能单独被别的 skill 调用。要拆回去也简单：`reference/` 里两份文档各自补一个 frontmatter 就是原来的 skill。

## 为什么分三段

一个 agent 从头跑到尾时，抓下来的大量原始文本会污染写作阶段的判断，而且慢。拆开之后中间只过一个 `candidates.json`：

| 段 | 档 | 输入 | 产出 |
| --- | --- | --- | --- |
| 抓取 | 低 | 源清单、近三天 `seen.json` | `candidates.json`（含原文正文）、`fill-notes` |
| 写作 | 高 | 只有 `candidates.json` | `articles/<源>/<篇名>.md` |
| 填装 | 低 | `articles/`、`items.json` | `report.html`、`seen.json` |

判据很硬：**判定的活给低档，判断的活给高档**。别让高档去数条数、拼文件树；也别让低档决定一篇文章的主干是什么。

高档执行明确不许：重新抓取、碰 HTML、去重、写 `seen.json`。抓取失败或列表偏薄的源在候选清单里标 `fail: <原因>`，不占用高档时间。

## 交付物形态

成品是**单个** HTML 文件，内联全部 CSS/JS/正文，可以直接 `file://` 打开或当附件发。三栏、抽屉、大纲都靠这份文件自带的脚本，不依赖网络资源。

改内容时只填四个占位（`TITLE` / `LEFT_TREE` / `DOCS` / `OUTLINES`），不动 CSS 与脚本；填法见 `templates/FILL.md`，填完跑 `check_report.py` 自检。

模板的约束只有三条，其余都是样式细节：一篇文章一个节点（深入是同一篇里的 `h2`，不拆两个文件）；`data-doc` 在文件树、doc、大纲三处必须一致；锚点用 `#doc-<id>`，小节用 `<id>-<小节>`。

## 接手步骤

1. 把本目录（`scheduler/ai-morning-digest/`）整个放进目标 agent 能加载的 skill 目录；确认 `SKILL.md` 的 name 是 `ai-morning-digest`，`reference/`、`templates/` 跟着一起过去。
2. 定 `<STORAGE>`，改 `SKILL.md` 的「存储」一节，建好 `daily/`。
3. 按 `routine.md` 建定时任务，prompt 里的 `<STORAGE>` 换成上一步的路径。
4. 先只跑第一段，检查 `candidates.json` 条数和来源分布是否正常；再跑第二、三段。
5. 用 `check_report.py` 过一遍，再打开 `report.html` 看三栏、抽屉、大纲。
6. 对照 `examples/` 里那份真成品比版式，确认 `seen.json` 落盘后再交给定时。

## 已知的脆弱点

- **依赖外部源清单**：源在 Google Doc 里，每次跑都重读。文档改了结构或权限变了，抓取段会整段空转，所以要先看 `candidates.json` 是否非空再往下跑。
- **抓取能力是硬依赖**：网页抓不动、邮件读不到，就直接缺那一路。失败要写进 `fill-notes`，不能让报告看起来像那天真的没有新闻。
- **模型分档靠调用方自觉**：skill 只说哪段该用低档、哪段该用高档，没有强制机制。接手的 agent 若只有一档模型，第二段的质量会明显下降，这点要提前说清。
- **`bro` 与「保留主干」有张力**：`bro` 会把句子往口语改，改多了会把技术判断磨平成大白话。以 `reference/article-summary.md` 为准，`bro` 只做最后一遍语感。

## 来源

各文件出处见 `sources.md`。合并上游时注意两处本地补丁：`reference/repo-analysis.md` 的 `report_dir` 必传，以及 `reference/article-summary.md` 的「不补背景、不替作者评价」。
