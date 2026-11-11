---
name: agent-skill-verification
description: 为验证 Agent 配置或技能，从现有本地代码目录创建一个共享源码的软链接目录。只需源目录路径，可指定输出路径，输出目录的 .agents 由用户自行配置。
---

# 创建 Agent 验证目录

接收一个已有的本地代码目录路径，运行 [link_workspace.py](scripts/link_workspace.py)，向用户返回脚本输出的绝对路径。未指定输出路径时，在源目录同级创建 `<源目录名>-agent-verify`。用户也可以指定一个尚不存在的输出目录。

```bash
python3 /path/to/agent-skill-verification/scripts/link_workspace.py "/path/to/source"
python3 /path/to/agent-skill-verification/scripts/link_workspace.py "/path/to/source" "/path/to/output"
```

脚本逐项链接源目录的顶层内容，包括隐藏文件。只跳过顶层 `.agents`，由用户在输出目录中自行创建和配置。通过这些链接编辑原有文件或在链接的子目录中添加文件，会影响源目录。创建后源目录新增的顶层条目需要另行链接。

如果源目录本身是 Git 工作区，在源目录运行 Git 命令。验证目录的顶层目录是软链接，Git 会按软链接识别这些条目。
