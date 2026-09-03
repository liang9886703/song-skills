---
name: taste-project
description: 阅读代码仓库并按约束产出分析报告。用户想初步了解一个项目仓库、或想深入了解仓库里的某一个子能力时使用；用户只丢来一个仓库链接或目录、没说具体要什么时也用本 skill。
---

# 阅读项目仓库

本 skill 用来阅读代码仓库，并根据用户的需要读取对应的约束文件，再按约束产出分析报告。

## 如何选择约束

先判断用户的需要，再读对应的约束文件：

- **初步了解整个项目仓库** → 读 `reference/first-understand-project-repository.md`
- **了解仓库里的一个子能力** → 读 `reference/one-ability-analyze.md`
- **用户只丢了一个链接（没说具体要什么）** → 默认按初步了解处理，读 `reference/first-understand-project-repository.md`

## 默认目录约定

### 代码仓库

- 默认代码根目录是 `$HOME/github/`，不要把用户目录硬编码成某个具体用户名。
- 用户给出本地代码目录时，直接读取该目录。
- 用户只给出 GitHub 仓库链接时，把仓库克隆到 `$HOME/github/<仓库名>/`，之后从这里读取代码；不要下载到临时目录、`$HOME/code/` 或当前工作区。
- 用户只给出项目名、没有给路径时，先到 `$HOME/github/` 下查找对应仓库。
- 目标仓库目录已存在时，先核对它是否对应同一个远程仓库，再复用已有目录，不要另建重复副本。
- 私有仓库优先复用现有 `gh` 登录或 SSH 凭据，不要要求用户重复提供 token。
- 克隆出现超时、`unexpected disconnect` 或长时间无进展时，不要原样重试：先检查系统代理是否没有传递给 Git；如用户正在使用本地代理，将有效的 HTTP/HTTPS 代理显式传给 Git 后重试。
- 仓库历史过大且任务只需要阅读当前代码时，可以改用 `--depth 1 --single-branch --filter=blob:none` 获取默认分支当前版本，但完成后必须明确说明这是浅克隆；需要研究历史时再对对应仓库补全历史。
- 克隆完成后必须逐个验证远程地址、当前分支、`HEAD` 可解析且工作区干净，不能只根据克隆命令退出状态判断成功。

### 调研文档

- 默认只产出 Markdown（`.md`）文档，并写入用户指定的路径；用户未指定路径时，才按下面的默认目录约定确定路径。
- 除非用户当次明确要求，否则不要生成 PDF、HTML、DOCX、图片或其他导出版本，也不要因为历史偏好、其他 skill 或常见交付习惯而额外生成这些产物。
- 默认文档根目录是 `$HOME/github/blogV2/data/content/`。
- 所有调研文档都必须放进 `$HOME/github/blogV2/data/content/` 下的一个语义明确的子文件夹，禁止把 Markdown、PDF、图片或其他调研产物直接写在 `$HOME/github/blogV2/data/content/` 根目录。
- 按能力或主题调研时，文件夹使用能力或主题名，例如 `$HOME/github/blogV2/data/content/coding-agent-记忆能力/`。
- 按项目调研时，文件夹使用项目名，例如 `$HOME/github/blogV2/data/content/hermes-agent/`。
- 同一项调研产生的主文档、分项目文档、图片和导出文件统一放在这个文件夹内。跨多个项目研究同一能力时，优先使用能力或主题名作为文件夹名，并把各项目文档与汇总文档放在同一文件夹中。
- 目标文件夹不存在时先创建，再写入文档。

## Coding Agent 项目分类约定

当用户使用下面这些集合称呼时，默认按对应项目展开，不必再次询问范围：

- **Coding Agent**：`codex`、`opencode`、`pi`、`claw-code`、`mycc`、`deepseek-harness`、`kimi-code`、`qwen-code`、`goose`、`maka`、`grok-build`、`cline`、`kilocode`
- **Agent 产品**：`hermes-agent`、`openclaw`、`open-design`、`openagents`、`multica`、`warp`
- **Agent 基础设施**：`ruflo`、`ax`、`litellm-agent-control-plane`、`OpenShell`
- **Agent 增强**：`oh-my-claudecode`、`oh-my-codex`、`oh-my-openagent`、`oh-my-pi`、`superpowers`

这些分类用于确定默认调研范围，不代表互斥的技术定义。用户明确点名、增删项目或另行限定范围时，以当次要求为准。

## 报告中的项目地址

- 每个项目产出的报告都必须在正文开头明确写出该项目的 GitHub 地址，统一使用格式：`项目地址：<GitHub URL>`。
- 地址必须根据用户提供的链接或仓库的 Git remote 核验，不得凭项目名猜测；SSH remote 应转换为便于读者访问的 `https://github.com/<owner>/<repo>` 形式。
- 一次分析多个项目时，每个分项目报告都要写对应地址；汇总报告还必须提供“项目 / GitHub 地址”对照表。
- 若仓库确实没有可核验的 GitHub 地址，应明确写成 `项目地址：未发现可核验的 GitHub 地址`，不得省略这一项或伪造链接。

## 流程

1. 判断用户属于上面哪种需要。
2. 读取对应的约束文件。
3. 按默认目录约定确定或准备代码仓库位置与调研文档文件夹。
4. 核验每个项目的 GitHub 地址。
5. 按约束文件探索仓库并产出报告。
6. 完成前检查：每份项目报告均已写明对应的 GitHub 地址；GitHub 链接下载的代码位于 `$HOME/github/`；所有调研产物位于 `$HOME/github/blogV2/data/content/<能力、主题或项目名>/`，且没有文件直接落在 `$HOME/github/blogV2/data/content/` 根目录。
