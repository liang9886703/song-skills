# 发现来源与统一安装

此文件合并公开发现、企业推荐和旧内网目录的用法。安装与同步由主入口的统一流程执行；本文件中的搜索命令不会替用户选择或安装技能。

## 来源关系与核验边界

- `find-skills` 原本使用 Vercel 的 `npx skills find`。官方源码通过 `https://skills.sh/api/search` 取得技能索引，结果含源仓库；它与 GitHub 直接搜索覆盖的技能可能相同，但检索后端不相同。
- `skillshare search` 默认走 GitHub Code Search；`--hub` 查询指定索引。Hub 可能只是同一仓库的另一条目录记录。
- `openai/skills` 官方精选与实验目录是 GitHub 的子集，按仓库和路径参与同一去重。
- 原 `oneskill-recommend-search` 使用企业 OneSkill CLI；原 `skill-recommender` 使用另一组内网 metadata / package HTTP 接口。缺少足以证明两者共享目录的证据，保留两个发现适配，不因“都返回 ZIP”就删除其中一个。
- 本次只核对接口、官方公开资料和本地 CLI 帮助，没有请求企业目录，也没有验证不同服务的实际结果交集。

## 公开搜索：skills.sh

```bash
npx skills find "react performance"
```

提供非空关键词，避免进入交互选择器。未安装的 CLI 使用 npx 时会涉及获取依赖，遵守当前环境权限。结果中的 `owner/repo@skill` 是搜索标识；先确认真实仓库内的技能子目录，不能把 `@skill` 原样当成 skillshare 的仓库路径。

只有索引结果时，不猜子目录；读取仓库确认后再安装。不要用 `npx skills add/check/update` 维护本个人库，避免建立另一套安装记录。

## 公开搜索：GitHub 与 Hub

```bash
skillshare search "code review" -g --list --json --limit 10
skillshare search "code review" -g --hub --list --json --limit 10
```

指定团队索引时，将 `--hub` 后的值替换为用户提供或已经配置的 Hub 标签、URL 或本地索引。GitHub 搜索需要可用的 GitHub 认证，缺失时报告该来源不可用，不自动改变用户认证或换成未经指定的私有源。

确定候选后只安装目标技能，例如：

```bash
skillshare install anthropics/skills -g -s pdf --dry-run
```

上面只是 CLI 选包语法示例，不表示本次需要安装该技能。实际使用选定的仓库和技能名；预览后再以相同选择执行正式安装。

## OpenAI 官方精选目录

本机系统 skill-installer 说明的官方来源为 `openai/skills`，默认目录 `skills/.curated`；实验目录 `skills/.experimental` 只在用户需要时查询。目录不存在或调整时核对实际结构，不猜迁移路径。

可用 GitHub 工具或已有 gh 查看，例如：

```bash
gh api repos/openai/skills/contents/skills/.curated --jq '.[].name'
```

按实际子目录导入 `skillshare`。系统安装辅助脚本若被用于下载，将 `--dest` 指向临时目录；其默认写入 Codex 目标的行为不用于个人库维护。不要复制或删除 `.system` 技能。

## 企业搜索：OneSkill

优先从 PATH 找 `oneskill`，再检查已有的 `$HOME/.oneskill-cli/bin/oneskill` 或项目 `.oneskill-cli/oneskill`；复用已安装 CLI。版本与能力以 `--version`、`recommend --help`、`search --help` 为准。本机核对版本为 1.0.12；搜索前不自动升级，也不下载执行安装脚本。

自然语言需求优先 recommend，明确关键词用 search：

```bash
oneskill recommend --query "生成每周工作周报" --top-n 5 --need-requery false --need-rerank true
oneskill search --keyword "周报" --type all --page 1 --page-size 20
```

保留原本地用法的默认：不扩写查询、启用 rerank。用户要求更强召回时可改 `--need-requery true`，要求更快或关闭重排时可用 `--need-rerank false`。`--score-threshold` 在 0~1，缺省或 0 使用服务端默认值；不固定服务端的数值或额外耗时估计。

recommend 返回字段按实际结果读取：`skill_id`、`skill_name`、`skill_description`、`skill_capability`，可用包地址在 `business_info.package_url`。search 按自身返回字段处理，不能假定它一定有同样的 package_url。只展示实际返回值，缺包地址时先核对该技能详情，不编造下载链接。

未登录或服务不可达时报告此来源未完成；不打印 token，不把令牌插入命令示例。用户要安装且已给出授权时，下载选定包并按主入口导入；不再写入旧规则指定的 `~/.claude/skills`。

## 旧内网目录：可选读取适配

已迁移 metadata 和 package 的读接口至 `scripts/internal_catalog.py`。它只读取目录或包地址，没有安装、覆盖或删除功能。

脚本先读环境变量 `SKILL_INTERNAL_CATALOG_URL`，否则读 `${XDG_CONFIG_HOME:-$HOME/.config}/skillshare/discovery.json` 的 `internal_catalog_base_url`。机器地址保存在私有配置，不写入公开技能正文；合并时已将旧脚本的地址迁入本机配置。其他机器未配置此来源时返回 `provider_not_configured`，继续使用其他适用来源。

从当前技能目录运行，或使用其真实绝对路径：

```bash
python3 scripts/internal_catalog.py list
python3 scripts/internal_catalog.py url "<实际 skill identifier>"
```

`list` 请求 `/api/v1/skills/metadata`，`url` 请求 `/api/v1/skills/package?skillIdentifier=...`，服务原协议为 `code=200` 且下载地址为 `data.bosUrl`。输出统一含 `provider`、`success`、`data` 或 `error`。请求超时为 10 秒；失败不自动重试，保留该来源未完成的状态，不能以此宣称“没有相关技能”。

目录含名称和描述，可按用户需求筛选；这是旧平台的目录读取和本地语义筛选，不等同于平台提供了服务端推荐排序。

## 候选去重与安装交付

优先使用规范仓库 URL + 技能子目录作身份；保留实际分支/提交/版本。GitHub SSH / HTTPS 可归一，路径大小写与不同版本不盲目抹平。平台 ID 按提供方命名空间区分；跨平台相同 ID 或相同名字都不能证明是同一技能。

重复结果合并来源标签、简介和链接，不叠加重复推荐。版本或发布者不同且无法确认同源时分别说明。平台包如包含可核验的 GitHub 来源，将该来源加入对应记录，避免从两个平台安装两次。

推荐时给出名称、用途、来源、已安装状态和必要依赖。用户只要搜索就停留在候选；用户明确要安装后核验选定包并导入。ZIP 解包后的本地目录用 `skillshare install <实际目录> -g --name <技能名> -s <技能名>`，先 dry-run 再执行；多技能包只选择目标目录。现有目录需保留定制时先比较，不盲目加 --force。完成后登记真实出处，再预览和执行同步，读取目标结果。

## 合并来源说明

- Skillshare 搜索与安装：[runkids/skillshare](https://github.com/runkids/skillshare/tree/main/skills/skillshare)，[search 官方文档](https://skillshare.runkids.cc/docs/reference/commands/search/)。
- 公开发现方法：[vercel-labs/skills 的 find-skills](https://github.com/vercel-labs/skills/tree/main/skills/find-skills)；检索后端依据 [src/find.ts](https://github.com/vercel-labs/skills/blob/main/src/find.ts)。仅吸收搜索能力，安装改为个人库统一流程。
- OneSkill 用法来自本机安装的 `oneskill-recommend-search` 1.0.3 与 CLI 1.0.12 帮助，未发现可确认的原作者 GitHub 地址，不虚构上游。原条目及其安装规则已归档，原有推荐与搜索参数在此保留。
- 旧内网适配来自个人库原 `skill-recommender` 的两段 API 调用；其原作者/许可未提供，未另行声明作者或许可。旧的覆盖安装、整包无校验解压与直接目标目录写入不再使用。
