# song-skills

个人技能主仓库：<https://github.com/liang9886703/song-skills>。

所有技能统一放在 `skills/<技能名>/`。编辑、提交和推送均以本仓库为准；旧的 `liang9886703/skills` 仓库仅保留为迁移备份，不再作为本机 skillshare 的源目录。

## 本机 skillshare 配置

在当前机器的 `~/.config/skillshare/config.yaml` 中，将 `sources.skills` 设为本仓库 `skills/` 的绝对路径，保留当前机器已有的 agents、targets 和其他设置，然后执行 `skillshare sync -g --dry-run` 核对，再执行 `skillshare sync -g`。

根目录的 `config.yaml` 是历史机器配置，包含另一台机器的路径和目标，仅供参考，不应直接覆盖当前机器的配置。

## 本地技能与提交范围

- 所有以 `baidu` 开头的技能目录仅保留在本地，已由 `.gitignore` 的 `/skills/baidu*/` 排除，不提交到 GitHub。
- 百度工作技能统一使用 `baidu-` 前缀，包括 BLS、BOS、企业搜索、如流消息、知识库管理与导出、ugate 认证。
- 本地配置、认证信息和缓存随本地技能保留，不发布；其他机器需要自行配置这些技能。
- 中文去 AI 写作痕迹技能使用 `humanizer-zh`；已移除的英文 `humanizer` 保持移除。
- 同名技能以本仓库原有版本为准；迁入技能保留其支持脚本和资源，统一目录与入口名称。

## 提交与同步

在本仓库检查 `git status` 和待提交差异后，使用 Git 提交并推送。skillshare 的同步源是当前配置的 `sources.skills`；不要仅凭默认目录推断应该提交哪个 Git 仓库。

首次迁移完成后，核对各目标工具的技能链接是否指向本仓库。旧源目录暂时保留，以便核对迁移内容。
