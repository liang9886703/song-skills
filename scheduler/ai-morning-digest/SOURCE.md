# Skill source

| 字段 | 值 |
| --- | --- |
| skill id | `ai-morning-digest` |
| kind | 用户自建（nazuna） |
| source list doc | https://docs.google.com/document/d/1cbzQ5e92UxDC75cdemcvUs1Q7SpOZ97htfLb5s0mTSU/edit |
| storage root | 部署方配置，默认 `/home/box/data/ai-digest/` |
| created at | 2026-11-03T22:45:00+08:00 |
| bundled at | 2026-11-04 |

本 skill 无单一上游仓库拷贝；规则以对话约定为准。更新源清单只改 Google Doc。各文件出处见 `sources.md`。

## 打包时的改动

原先「单篇写法」和「仓库深入分析」是两个独立 skill，现在合并进本 skill 的 `reference/`：

| 原 | 现 |
| --- | --- |
| `article-summary/SKILL.md` | `reference/article-summary.md` |
| `taste-project/SKILL.md` + `reference/` | `reference/repo-analysis.md` + `reference/repo-analysis/` |

同时做的去环境化：

- 原 `sand-workflow:` 形式的 skill 链接改为包内相对路径，换 agent 也能点开。
- 存储根从写死的 `/home/box/data/ai-digest` 改为 `<STORAGE>`，默认值保留在「存储」一节，换机器只改一处。
- 新增 `templates/check_report.py`：填完 HTML 自检占位符、文件树/大纲对齐、死锚点。

这些改动不涉及运行规则；同步回技能库时，链接可换回原写法，`check_report.py` 与 `<STORAGE>` 建议保留。
