---
name: ai-morning-digest
description: >-
  跑 AI 信息晨报/日报：读《优秀 AI 信息源》（跳过 AIHOT），按各源「最近一天」抓取，按信息源分组，去重近三天，白名单与条数上限，三栏
  HTML（左文件树/中单篇/右当前篇大纲）输出到 <STORAGE>/daily/YYYY-MM-DD/ 并对话通知。定时任务触发时也用。
metadata:
  storageRoot: 由部署方配置，默认 /home/box/data/ai-digest
  provenanceFile: SOURCE.md
  layout: source-file-tree
  updatedAt: 2026-11-04T05:20:00.000Z
---
# AI 晨报（信息源日报）

## 文件

本 skill 自包含，不依赖其他 skill。

| 路径 | 作用 |
| --- | --- |
| `reference/article-summary.md` | 每篇 md 怎么写：导读 + 命中框架的正文，保留主干、标题优先原文、不联网补背景 |
| `reference/repo-analysis.md` | 仓库类条目怎么深入分析；`report_dir` 指向当日 `intermediate/repos/<owner-repo>/`，配套 `reference/repo-analysis/` 下的约束文档 |
| `templates/report.html` + `templates/FILL.md` + `templates/check_report.py` | 固定三栏 HTML 壳（左文件树 / 中单篇 / 右当前篇大纲）、填法、填完自检 |
| `whitelist.md`、`blacklist.md` | Trending / HF 的收录名单 |
| `examples/` | 一份真成品 HTML、候选清单、fill-notes |
| `SOURCE.md` | 来源与打包改动记录 |

`bro`（去 AI 味）是可选的通用能力，环境里有就用，没有不影响本 skill 成立；用了只做最后一遍语感。

## 何时使用

用户要求跑 AI 信息晨报/日报，或定时 routine 触发。每次重读 Google Doc《优秀 AI 信息源》`https://docs.google.com/document/d/1cbzQ5e92UxDC75cdemcvUs1Q7SpOZ97htfLb5s0mTSU/edit`，**跳过 AIHOT**。

## 存储

时区 **Asia/Shanghai**。`<STORAGE>` 由部署方配置，默认 `/home/box/data/ai-digest`；换机器只改这一个根，其余都是相对路径。交接、部署与已知脆弱点见 `HANDOFF.md`，定时定义见 `routine.md`。

```
<STORAGE>/daily/YYYY-MM-DD/
├── report.html              成品，单文件，内联全部 CSS/JS/正文
├── seen.json                近三天去重：{date, timezone, items[{url, source, title, date}]}
├── articles/<源>/<篇名>.md   单篇源文件，HTML 正文的来源
└── intermediate/
    ├── candidates.json      低档产出、高档输入（唯一交接物）
    ├── items.json           最终收录清单，填 HTML 时按它生成文件树
    ├── sources/<源>/        抓下来的原始列表页 / 正文
    ├── repos/<owner-repo>/  仓库深入报告
    ├── lenny/               当日 Lenny 邮件正文
    └── fill-notes/notes.md  收了什么、省了谁、哪路失败
```

## 「最近一天」

该源最新已发布内容的发布日；今日无则取昨天等。约一个月无更新则**整源省略**。GitHub Trending：Daily、不限语言（当日快照）。

## 上限

| 对象 | 规则 |
| --- | --- |
| 博客 + 仓库合计 | ≤ 20；白名单优先，再按与 Agent runtime / 会话编排 / 沙箱 / 权限 / 评测 / 模型服务相关度 |
| HF Papers | 白名单；最多 10；只简写；降权纯层训练细节 |
| Trending | 见 `whitelist.md` / `blacklist.md`；名单外按相关度极简必收、不深入 |

## 组织（按信息源）

报告按**信息源**分组，不分资讯/技术/思考。

左栏文件树：源文件夹 → 每篇文章一个 `.md` 节点（另有根级 `今日.md` 索引）。点文件只打开那一篇。

一篇文章一个节点，简略与深入**同一篇**，不拆两个文件。右栏只放当前篇的大纲。

## 成本路由（按任务分档）

| 环节 | 档 | 为什么 |
| --- | --- | --- |
| 读清单、抓取、列表解析、去重、选条、写 `seen.json` | 低 | 判定标准已写死，机械活 |
| 填 `report.html`（替换占位符、生成文件树与大纲） | 低 | 模板已定，只做替换 |
| 导读 + 正文（`reference/article-summary.md`） | 高 | 全报告唯一的质量来源，需要读懂主干、判断取舍 |
| 仓库深入（`reference/repo-analysis.md`） | 高 | 要读代码、下结论 |

分派要求：

1. **一次执行只做一类事**。抓取阶段一个低档执行，产出 `intermediate/candidates.json`（源、标题、链接、发布时间、原文正文）；写作阶段一个高档执行，输入只有这份候选清单 + 原文，**不要让它重新抓取**。
2. 高档执行只写正文（每篇 md 的正文内容），不碰 HTML、不去重、不写 seen。
3. 抓取失败或列表偏薄的源，在候选清单里标 `fail: <原因>`，不占用高档执行的时间。

## 写作

每篇按 `reference/article-summary.md` 写，动笔前读一遍。三条最容易破的：

- 导读说清这篇在谈什么话题，读者据此判断值不值得细看。
- 只写文章里实际有的东西，没有背景就不写背景，不联网补，不替作者补他没写的代价。
- 保留主干略去细节：例子写它在证明什么，不逐个复述。

不合格的典型：「本文介绍了…」开头、通篇名词要点、凑齐框架而写了原文没有的章节。

正文用中文；`bro` 有就用，只做最后一遍语感。**不要**「今日必看一页纸」。

## 去重与 Lenny

近三天 `seen.json` 去重（URL 或 `源+标题+日`）。同源事件合并。**必查当日 Lenny 邮件**（发件人含 Lenny's Newsletter）。

## 填 HTML

1. 按 `templates/FILL.md` 填 `templates/report.html` 的四个占位（`TITLE` / `LEFT_TREE` / `DOCS` / `OUTLINES`），不改 CSS 与脚本。
2. 落到当日 `report.html`，跑 `python3 templates/check_report.py <report.html>` 自检（占位符、文件树/大纲对齐、死锚点）。
3. 自检通过后再写 `seen.json`。

## 会踩的坑

- **`openai.com/news` 直连 403**：curl 拿不到就换 WebFetch，或直接抓文章页，别当成源挂了。
- **列表页可能是 gzip 块或 JS 空壳**：先看字节数；薄的列表走搜索定位当日文章，再抓正文。
- **「最近一天」不是「今天」**：取该源最新已发布条目的发布日；约一个月没更新就整源省略，不抓旧文凑数。
- **Trending 是当日快照**：漏了当天补不回来，抓取段必须当天跑。
- **去重按近三天**：只比 URL 会漏同源改标题的重复，加 `源+标题+日` 一起判。
- **HF Papers 最多 10 条且只简写**：写结论和它怎么验证的，不展开方法细节。
- **空报告也要出**：全部源都没更新时，生成带索引的空壳并说明原因；静默跳过等于任务失败。

## 交付

对话通知用户；附上当日报告（`file://<STORAGE>/daily/YYYY-MM-DD/report.html`）与条数、省略的源、失败的源。

## 流程

读清单 → 建目录 → 读 seen →【低档】抓取 + Lenny + 裁剪 + 去重 → `candidates.json` →【高档】导读+正文（仓：`reference/repo-analysis.md` + `report_dir`）→【低档】填 HTML + 写 seen → 通知。
