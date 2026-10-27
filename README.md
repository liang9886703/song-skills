# song-skills

个人技能主仓库：<https://github.com/liang9886703/song-skills>。

所有技能统一放在 `skills/<技能名>/`，每个技能以 `SKILL.md` 为入口，脚本、参考资料和资源保存在对应技能目录中。

## 本机 skillshare 配置

在当前机器的 `~/.config/skillshare/config.yaml` 中，将 `sources.skills` 设为本仓库 `skills/` 的绝对路径，保留当前机器已有的 agents、targets 和其他设置，然后执行 `skillshare sync -g --dry-run` 核对，再执行 `skillshare sync -g`。

## 个人技能管理约定

个人编写的技能使用中文，包括入口描述、正文和配套说明；目录名、命令和代码标识保留必要的英文。第三方技能保留原文、署名和已有中文适配。

用户说“更新一下 skills”或“更新技能库”时，按各技能的出处获取并合并上游更新，保留本地定制，再提交、推送到 song-skills，并同步到本机配置的工具目录。只拉取 song-skills 或只执行 `skillshare sync` 不代表完成上游更新。具体流程由 [`skillshare-skill-management`](skills/skillshare-skill-management/SKILL.md) 维护。

## 技能出处

以下列出有明确依据的技能出处；未列出的技能来源待确认。安装或更新技能时同步维护来源链接、改编关系和更新注意事项，采用的上游版本记录在对应技能的来源文件中。

| 技能 | 来源 | 关系与更新注意事项 |
|------|------|------------------|
| `baoyu-article-illustrator` | [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-article-illustrator) | 宝玉原作，当前为 Hermes 适配；合并上游时保留适配。 |
| `baoyu-comic` | [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-comic) | 宝玉原作，当前为 Hermes 适配。 |
| `baoyu-infographic` | [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills/tree/main/skills/baoyu-infographic) | 宝玉原作，当前为 Hermes 适配。 |
| `golang-context` | [samber/cc-skills-golang](https://github.com/samber/cc-skills-golang) | 入口元数据声明来源；更新前定位仓库内对应技能目录。 |
| `humanizer-zh` | [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 中文版本的直接来源；原说明另署名 blader/humanizer 与 hardikpandya/stop-slop，更新时保留中文版本。 |
| `guizang-ppt-skill` | [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | 歸藏创建与维护，入口明确标注的规范源仓库。 |
| `gamer-news` | [byeolbit/gamer-news-skill](https://github.com/byeolbit/gamer-news-skill) | 入口 homepage 声明的来源。 |
| `graphify` | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 本地说明记录的原始地址为 safishamsi/graphify，目前迁至此处；本地是离线定制版，需合并更新。 |
| `nuxt` | [antfu/skills 的 nuxt 技能](https://github.com/antfu/skills/tree/main/skills/nuxt) | Anthony Fu 维护的技能；nuxt/nuxt 是其文档生成依据，不是直接替换此技能的目录。 |
| `skillshare` | [runkids/skillshare 的官方技能](https://github.com/runkids/skillshare/tree/main/skills/skillshare) | 官方 CLI 配套技能；保留 song-skills 的管理约定。 |
| `architecture-diagram` | [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) | 入口声明基于该项目，移植到 Hermes；按改编关系合并。 |
| `codebase-to-tutorial` | [The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge](https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge) | 个人技能封装的上游程序，不是官方 skill；内置源码版本见 `assets/upstream/source.json`，保留本地模型调用封装。 |
| `pixel-art` | [Synero/pixel-art-studio](https://github.com/Synero/pixel-art-studio) | 仅调色板和动画循环部分移植自该 MIT 项目；不能整目录替换技能。 |
| `systematic-debugging` | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) | 入口署名为 Hermes 改编版，保留本地适配。 |
| `test-driven-development` | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) | 入口署名为 Hermes 改编版。 |
| `writing-plans` | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/writing-plans) | 入口署名为 Hermes 改编版。 |
| `subagent-driven-development` | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/subagent-driven-development) | 入口署名为 Hermes 改编版。 |
| `requesting-code-review` | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/requesting-code-review) | 入口声明结合 obra/superpowers 与 MorAlekss；后者的具体仓库待确认，不覆盖本地组合流程。 |
| `plan` | [obra/superpowers](https://github.com/obra/superpowers) | 入口声明写作方法改编自该项目；本地“只写计划、不执行”的流程需保留。 |
| `spike`、`sketch` | [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | 本地说明声明改编自 GSD 对应工作流；仓库已归档，保留本地独立适配，不假定存在持续更新。 |
