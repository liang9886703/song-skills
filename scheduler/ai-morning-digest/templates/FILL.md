# 填装晨报阅读室

采用 2026-11-11 最新阅读器，不再使用四个旧占位或 11/05 的紫色操作区。以 `reader-shell.html` 为内联模板，或复制 `reader.css`、`structure.html`、`reader.js`、`reader-utils.js`、`build_reader.py` 到当日 Site 源码目录进行组装。

## 内容与数据

- `articles.json`：当日对象，包含 `date`（北京时间 YYYY-MM-DD）、`title`、准确 `site_url`、`articles`、可选 `project_library_url`，以及可选 `coverage`、`limitations`。
- 每篇使用稳定且当期唯一的 `id`，保留 `title`、`source`、原文发表 `date`、`lead`、`sections`、`links`、准确的 `original_url`、可选 `terms`。项目保留 `repo_url`。`sections` 可用 `title`、`level`、`paragraphs` 或已安全渲染的 `html`。完整 Markdown 可放 `full_markdown` / `bodyMarkdown`，复制与页面必须一致。
- `history.json`：此前已核实发布的日报对象数组，不含当日本身。不要只存标题或短摘录；保留完整正文、引用和原图。仅在有实际日报数据时给日历日期加标记；缺失日期显示未收录，未来日期显示尚未发布。
- 模板内数据标记是 `/*DATA*/{}` 和 `/*HISTORY*/[]`，各替换一次为 JSON。嵌入 script 前将 JSON 中 `</` 转义为 `<\/`，防止正文意外结束 script。`build_reader.py` 执行这一组装，输出 `dist/index.html` 和可检查的 `check.js`。
- 历史旧 HTML 可使用 `rendered_body` 加 `content_format`；原 HTML 的操作条、脚本和事件属性不得带入。`overview_html` 只保留当期内容说明，不恢复旧界面。
- 历史图存于 `dist/history-assets/YYYY-MM-DD/`，相应正文使用 `/history-assets/YYYY-MM-DD/...`。不得把仅有本地文件的路径或未校验资源当成线上图。

## 外观和交互

浅灰外壳、白色阅读区、珊瑚色线性图标、玫红色加粗与亮粉色行内代码、标题旁短斜杠。桌面左右两栏均可拖动，支持键盘调宽并保持设置。最左功能列为今日阅读、跨期搜索、中央日历；左下两个图标切换明暗主题并保持选择。默认按北京时间打开今天，未收录今天时清楚提示并提供最近一期，不把历史稿冒充今天。

标题下平铺一个原文/官方项目入口、一个复制按钮和一个直接打开 Codex 的图标，不恢复卡片、菜单或说明小字。项目的同一 Codex 预填请求包含准确仓库及 taste-project 约束；只打开并预填，不执行。复制失败才展开可手动选取的正文。

日期文章锚点为 `#day-YYYY-MM-DD/doc-ID`，具体标题为 `#day-YYYY-MM-DD/doc-ID/heading-ID`，旧 `#doc-ID` 在当期仍可读。历史大纲必须带文章 ID，不能因旧标题 ID 没有文章前缀就跳回总览。

900px 及以下用单篇正文与文件/大纲抽屉；320–440px 保持 16px 正文、主要按钮 44px、局部表格滚动和无整页横向溢出。保留术语原位浮窗、引用、深链接与手动复制。

## 历史归档与恢复

当前共享归档为 `<STORAGE>/archive/editions.json` 和 `archive/history-assets/`。新一期先加载已核实归档，排除当日日期；发布成功后按日期去重追加或替换当期，保存完整 articles、Site URL 和图片。

本地目录丢失时，从 Sites 中最近一期已成功发布的源码恢复 `articles.json`、`history.json`、阅读器源码及 `dist/history-assets/`。恢复项目与链接从本地部署配置及已验证发布记录读取，以最新成功发布日版为准。不能仅恢复 GitHub 的旧模板后丢掉新界面或历史数据。

每天仍新建独立、仅本人可访问的当日 Site，同日重试复用。每期是发布时的历史快照：包含当时已收录日期，不自动发现以后新建的日报；后续新一期继续带上既有归档，不改其他日期站点。

## 内容规范与检查

文章继续读取 `../reference/article-summary.md` 的基础和适用专用规范，保留导读和原文主干。项目直接使用 `../../../skills/research/taste-project/SKILL.md` 路由，不自造轻量版。不要以布局优化为由删改文章、引用、图表或来源许可。

发布前检查 JSON 日期和当期 ID 唯一、script 转义、正文与复制一致、全部资源、历史缺失日期、跨月日历、跨期搜索、双栏拖动、刷新后主题与宽度、文章及大纲锚点、手机抽屉和横向溢出、术语关闭、复制成功与失败、Codex 编码。静态 `node --check check.js` 与受支持的浏览器测试互相补充；旧 `check_report.py` 的四占位/旧 DOM 假设不适用于本模板，不把其结果冒充新阅读器检查。区分浏览器验证、真实 iPhone 和用户本机 Codex 验证。

## 排版细节（2026-11-11 近景参考）

不要只对齐外壳。正文普通文字为深暖灰；加粗使用玫红 #dd2c38，行内代码使用亮粉 #dd1499，不合并成一种强调色。选中态是浅粉底 #fee4e2，保留文字本来的语义色；链接为蓝色 #1875d9 并显示细下划线。斜体用温暖深橙。

引用为细珊瑚竖线和轻微点纹底，表格使用淡粉细网格、点纹表头和紧凑但清楚的单元格间距。标题按 H1–H6 建立字号、间距和短斜线色阶，不用粗重色块；各级标题本身保持正文深色。代码块、列表、分隔线、图注、上下标、键帽、删除线、标记与脚注也有对应样式。

暗色主题使用专门的前景、选中底、表格边线和点纹色，不仅反转背景；确保文字仍清晰。窄屏长表格/代码只在自身区域滚动，正文不横向溢出。不要给测试样张添入日报，也不因重新排版改动正文或归档。样式测试片段保存在 Site 源码 tests/typography-fixture.html，发布目录不能包含临时 QA 页面。


## 项目分析库
左侧项目分析按钮链接固定私有项目库，不随日报日期新建。执行 PROJECT_LIBRARY.md 的完整发布约定。reader.js 新增 /*PROJECTS*/ 数据标记；独立日报不必携带项目数据，但必须保留固定入口。项目库更新时保留本站的日报历史正文，只合并 projects.json 并重建发布。

## 部署配置边界

复制 `deployment.example.json` 为未入库的 `deployment.local.json`，填入本地运行资料。生成当期数据时仅把已授权在私有站点显示的 `project_library_url` 写入 `articles.json`；不得把完整部署配置、信息源文档地址、存储路径或凭证注入网页。未配置项目入口时按钮隐藏。源码模板不携带日报正文或历史归档；部署时从自己的授权来源恢复。
