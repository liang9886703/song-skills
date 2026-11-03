# 运行说明

上游：https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge

固定版本：`05b24cbbb0fe409c5e23c9791f0342f07524ffdc`。`assets/upstream/` 保存本流程使用的原始源码及 MIT 许可证，包装器不修改上游文件。

## 本地代码库

将技能目录替换为当前 `SKILL.md` 所在目录。参数使用绝对路径，`--output` 是基础目录，最终教程位于其中的项目名称子目录：

```bash
python3 /技能目录/scripts/run.py \
  --dir /源码目录 \
  --output /教程输出目录 \
  --work-dir /临时工作目录 \
  --name 项目名称 \
  --language Chinese
```

也支持 `--repo https://github.com/组织/仓库`。本地仓库不需要 GitHub 凭据。`--include`、`--exclude`、`--max-size`、`--max-abstractions` 沿用上游含义；显式提供 include/exclude 会替换对应默认集合。其他参数见 `--help`。

默认运行环境：`~/.local/share/codebase-to-tutorial/venv/bin/python`，可用 `CODEBASE_TUTORIAL_PYTHON` 指定兼容环境。依赖见 `requirements-host.txt`。若环境丢失，在该位置重新创建虚拟环境并安装此依赖文件；不要依赖历史 `/tmp` 路径。

## 处理请求

退出码 **75** 表示等待智能体提供响应。工作目录包含：

- `pending.json`：请求的 `prompt`、`response`、调用序号和字符数。
- `model-exchange/*.prompt.txt`：上游真实提示词。
- `model-exchange/*.response.txt`：智能体写入的响应。
- `crawl-manifest.json`：文件索引、路径、字符数和内容哈希。
- `crawl-files.json`：当前读取的完整文件快照，可按索引提取内容。

前三类响应按提示词使用 YAML 代码块：抽象列表、关系及项目说明、章节顺序。后续响应为各章 Markdown。继续运行时按提示词哈希复用响应，原生节点负责格式和索引校验。源码变化导致提示词变化时生成新请求。不同参数使用不同工作目录。

章节提示词包含之前的章节，可能很长；按实际预算选择合理的文件范围和章节数量。不能把未读的上下文说成已审阅。最终 **0** 才代表完成，`completed.json` 记录交付入口。脚本仅修正上游固定英文标题、署名及本地仓库链接，其他正文直接生成中文。生成的 `run-report.md` 记录抓取范围与适配方式，实际补读和校验结果由智能体追加。

## 原生外部模型方式

`assets/upstream/main.py` 和 `utils/call_llm.py` 保持原版。需要此方式时，在独立环境安装 `assets/upstream/requirements.txt`，按上游配置模型提供方。使用已有环境配置，不要求用户发送密钥原文。默认宿主适配模式不调用此模型实现，也不向第三方模型发送源码。
