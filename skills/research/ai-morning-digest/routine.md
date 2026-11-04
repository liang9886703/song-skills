# 定时任务定义（可直接粘贴到别的 agent）

## 触发

| 字段 | 值 |
| --- | --- |
| 名称 | AI 信息晨报 |
| 类型 | 定时（cron） |
| cron | `CRON_TZ=Asia/Shanghai 0 8 * * 1-5` |
| 时间 | 工作日 8:00 Asia/Shanghai |
| 容差 | flexible，早 30 分 / 晚 30 分（实际常在 7:40 起跑） |
| 投递 | 回到发起它的对话 |

## prompt

```
跑 AI 信息晨报。完整按 ai-morning-digest skill 执行：重读《优秀 AI 信息源》清单（跳过 AIHOT），按各源「最近一天」抓取，按信息源分组，近三天 seen 去重，套白名单与条数上限，必查当日 Lenny 邮件。

按成本路由分三段跑：抓取 / 去重 / 选条 / 填 HTML / 写 seen 用低档；导读与正文用高档，阶段之间只用 candidates.json 交接。填完 HTML 用 templates/check_report.py 自检。每篇按 reference/article-summary.md 写：导读说清在谈什么话题，正文只命中文章实际有的框架，标题优先用原文的，不联网补背景。

用 skill 内固定三栏 HTML 模板（左文件树 / 中单篇 / 右当前篇大纲）写到 <STORAGE>/daily/当日/，仓库深入按 skill 内 reference/repo-analysis.md 做，report_dir 指到当日 intermediate/repos/<owner-repo>/。

结果交给本对话里的用户：发简短通知，附上当日 report.html；说明条数、省略的源、失败的源。若当日各源都无「最近一天」可收内容且 Lenny 也无，仍生成带索引的空壳报告并说明原因，不要沉默跳过。
```

`<STORAGE>` 换成目标机器上的存储根目录（本仓库默认约定 `/home/box/data/ai-digest`，见 HANDOFF.md「环境变量」一节）。
