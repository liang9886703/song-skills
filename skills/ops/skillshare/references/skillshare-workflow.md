# 技能组装与本机同步

## 确认源目录

读取当前生效的 skillshare 配置。`sources.skills` 指向本机真实源目录，不使用历史机器的路径覆盖当前配置。本机主仓库为 `/Users/zisongliang/code/song-skills`，技能源在其中的 `skills/`。

分多次提供的内容应先组装完整：入口放在 `<源目录>/<技能名>/SKILL.md`，参考文件、脚本与资源保留用户要求的相对路径。自编说明使用中文。外部技能同时在主仓库 README 登记来源及本地适配。

## 检查并同步

在已配置的机器上执行：

```bash
skillshare target list --json -g
skillshare sync -g --dry-run
skillshare sync -g
```

若尚未初始化，先查阅当前 `skillshare init --help` 再初始化，核对实际导入内容。只有需要配置缺失目标时，才使用当前 CLI 支持的目标管理命令。目标路径以用户实际使用的工具为准；Hermes 的默认目录和 profile 专属目录可能不同，不自动把 Hermes 加到每台机器。

读取同步摘要，并核对目标中的入口和关键支持文件。符号链接模式应确认链接指向当前源目录；复制模式应比较内容。写入源目录只是完成编辑，有至少一个目标且同步成功后才算完成分发。

## CLI 安装注意

`skillshare` 来自 `runkids/skillshare`，是 Go 单文件 CLI，不是 npm 同名包。需要安装时按项目说明选择官方安装器、Homebrew 或对应平台的发行二进制。下载脚本先阅读再执行；无法交互输入 sudo 密码时可安装到用户可写的可执行目录，并用 `skillshare version` 验证。

用户要求“更新 skills”时，先执行主技能中的上游更新流程，再执行这里的分发步骤；不能仅运行同步命令就声称已更新。
