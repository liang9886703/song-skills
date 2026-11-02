# song-skills

个人技能主仓库：<https://github.com/liang9886703/song-skills>。

所有技能统一放在 `skills/<技能名>/`，每个技能以 `SKILL.md` 为入口，脚本、参考资料和资源保存在对应技能目录中。

## 本机 skillshare 配置

在当前机器的 `~/.config/skillshare/config.yaml` 中，将 `sources.skills` 设为本仓库 `skills/` 的绝对路径，保留当前机器已有的 agents、targets 和其他设置，然后执行 `skillshare sync -g --dry-run` 核对，再执行 `skillshare sync -g`。

## 个人技能管理约定

个人编写的技能使用中文，包括入口描述、正文和配套说明；目录名、命令和代码标识保留必要的英文。第三方技能保留原文、署名和已有中文适配。

用户说“更新一下 skills”或“更新技能库”时，按各技能的出处获取并合并上游更新，保留本地定制，再提交、推送到 song-skills，并同步到本机配置的工具目录。只拉取 song-skills 或只执行 `skillshare sync` 不代表完成上游更新。具体流程由 [`skillshare`](skills/skillshare/SKILL.md) 维护。

## 技能出处

以下列出有明确依据的技能出处；未列出的技能来源待确认。安装或更新技能时同步维护来源链接、改编关系和更新注意事项，采用的上游版本记录在对应技能的来源文件中。

| 技能 | 来源 | 关系与更新注意事项 |
|------|------|------------------|
| `humanizer-zh` | [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 中文版本的直接来源；原说明另署名 blader/humanizer 与 hardikpandya/stop-slop，更新时保留中文版本。 |
| `gamer-news` | [byeolbit/gamer-news-skill](https://github.com/byeolbit/gamer-news-skill) | 入口 homepage 声明的来源。 |
| `skillshare` | [runkids/skillshare 的官方技能](https://github.com/runkids/skillshare/tree/main/skills/skillshare) | 官方 CLI 配套资料与个人管理规则合并；同时统一公开与企业技能发现，安装和分发由本入口维护。 |
| `skillshare` 的公开发现模块 | [vercel-labs/skills 的 find-skills](https://github.com/vercel-labs/skills/tree/main/skills/find-skills) | 合并搜索方法，保留 skills.sh 索引；OneSkill 与旧内网来源见技能内参考说明，不虚构 GitHub 出处。 |
| `architecture-diagram` | [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) | 入口声明基于该项目，移植到 Hermes；按改编关系合并。 |
| `codebase-to-tutorial` | [The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge](https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge) | 个人技能封装的上游程序，不是官方 skill；内置源码版本见 `assets/upstream/source.json`，保留本地模型调用封装。 |
| `my-repo-story` | 个人编写 | 多代码仓库自动化安全拉取、24小时变更分析与技术演进复盘技能；支持本地冲突保护与 macOS launchd 定时调度。 |
