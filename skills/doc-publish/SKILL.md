---
name: doc-publish
description: Use when explicitly asked to use 文档发布 skill.
version: 0.1.0
platforms: [macos, linux]
---

# 发布 Markdown 文档到云博客

把用户明确指定的现有 Markdown，通过固定脚本交付到 Supabase，并在既有云博客验收。只负责文档发布，不负责调研或撰写正文。

## 触发与范围

- 只有用户明确点名 `doc-publish` 或「文档发布 skill」时才执行本流程。
- 不因其他 skill 完成、出现新报告或 Markdown 已保存而自动调用，也不主动把其他工作扩成发布任务。
- 本次只处理用户明确指定的文件；用户已明确指出“本次报告”且上下文中只有一份时可直接使用该路径。多个候选无法确定时，只澄清文件范围，不扫描发布整个目录。
- 用户要求仅预检、仅本地、草稿或不发布时，不执行 `--publish`。

## 前提

- 先用 `read_file` 读取 `$HOME/github/blogV2/scripts/research-publish/README.md`，以现有脚本契约为准。实现保留在博客仓库，不在 skill 内复制代码、另造同步器或临时拼接 SQL。
- 依赖博客项目已安装的 Node 26、npm 依赖与 Python3 标准库读取助手。数据库需要已有的 029 身份绑定更新能力；缺少时停止，不退回不安全写入。
- 默认文档根目录为 `$HOME/github/blogV2/data/content`，文件位于明确主题子目录。用户指定其他根目录时，通过已有 `--content-root` 参数显式设置；根目录及全部祖先不可含符号链接。
- 凭据只从已有私有配置文件或服务端环境读取；优先复用，不向用户索取已有密钥。不读取或展示密钥值，不把凭据放进正文、提示词、命令参数、聊天或版本库。

## 执行

1. 阅读指定正文，确认范围和内容；常见敏感模式扫描不能代替人工审查。未审核附件、本地相对链接和 raw HTML 不通过时停止，不自行全量上传资源。
2. 用 `terminal` 对每份文件分别执行预检，成功后才正式发布：

```bash
CLI="$HOME/github/blogV2/scripts/research-publish/cli.mjs"
REPORT="用户指定的 Markdown 绝对路径"
node "$CLI" --file "$REPORT"
node "$CLI" --file "$REPORT" --publish
```

3. 默认目标是 `song / contents / research`；其他位置只能按用户要求通过现有参数显式指定，不猜 owner、不创建工作区、不迁移全库。通过本入口发布的文章一律置顶：新建和更新均写入 `metadata.pinned=true`；旧文章缺少 pin 或为 false 时，同文件重复发布会安全补齐置顶，不批量扫描历史文章。
4. 保存脚本回执的 `action / id / revision / pinned / sourceSha256 / pageUrl`。只有 `status=verified` 且 `pinned=true` 才算云端交付通过；`unchanged` 表示正文相同且已置顶的幂等成功，不是漏执行。
5. 用已有授权浏览器打开 `pageUrl`，实际看到标题、正文和侧栏目录入口，必要时刷新验证修改。独立自动化浏览器遇到 Access 登录页时，先核查本机浏览器是否已有有效授权会话；可在原会话打开目标页，不导出 cookies、不修改访问控制。原生捕获若只取得标签悬浮卡片，列出窗口并指定主窗口 PID/window_id；控件定位优先使用新鲜 AX 索引，避免截图缩放导致坐标误点。目录过长时折叠无关库，确认本篇入口并点击回到报告页。浏览器会话确已失效时，通过正规登录交互恢复或明确报告网页验收未完成；不降低 Cloudflare Access 或匿名权限。

## 失败与边界

- 配置、安全检查、网络或 RPC 失败时，保留安全错误码，不能输出原始服务端错误、请求头或凭据。
- 发生 ownership、源位置、网页正文或 CAS 冲突时停止，不强制覆盖，不手工改标记绕过保护。
- 写入后回读失败或本地回执保存失败，不能声称没有写入或已经回滚；先核对云端状态，再按同一文件和位置安全重跑，不自动重试未知结果的写请求。
- `verified` 只代表云端回读，不代表网页已验收；登录页、302、HTTP 200 空壳或仅 API 成功都不算网页完成。
- 本流程只更新动态 `app.songkuakua.com` 数据，不等于独立静态站重建；不调用部署 CLI、不改变登录策略。

## 交付验收

向用户交付源 Markdown 路径、回执动作与版本、文章链接、实际完成的云端和网页验证。明确未完成的边界，不把预检或部分成功说成全流程成功。
