---
name: game-info-search
description: 通过经过实测的公开网页、RSS 与 Steam API 搜索游戏发售和定档、玩家评价、媒体评测、攻略及开发幕后；适用于按游戏名、AppID 或时间范围搜索，以及筛选值得关注的新游。
---

# 游戏信息搜索

先识别游戏（中英文名、代数、开发商、版本），用发行商官网或官方商店确认发售日期、平台和版本。找“最新”时，限定用户要求的窗口；未指定时先看近 7 天，不足则说明后再放宽。按原文的发布日期或评论时间排序，不用搜索抓取时间。没发布的游戏只有预告、媒体预览或测试体验，不能写成正式版玩家评价。

## 按问题选入口

| 问题 | 优先路线 |
|---|---|
| 新游戏、发售计划、平台、开发幕后 | 发行商官网/公告、Steam 商店和公告、主机官方商品页；开发幕后优先找开发者博客和原始采访。Steam 搜不到确切游戏时，不用相似游戏、上一代或 DLC 的 AppID 代替。 |
| 玩家如何评价 | 有正确 Steam AppID 用新版评测 API；主机游戏先看 PlayStation Store 等发行平台上可见的玩家评分或文字评价，再看游戏专版、其乐、电玩帮等第一人称体验。商店评分与社区样本分别报告。 |
| 中文评测、攻略、具体玩法 | 机核、篝火营地查编辑长文；其乐、电玩帮查玩家攻略与硬件/玩法经验；Reddit 游戏专版补细节。先读原文，辨别是媒体试玩、玩家自述、转载还是攻略；有结局内容标注剧透。 |

## 已验证的访问方式

- **Steam**：先按游戏名在[商店](https://store.steampowered.com/)核对开发商与对应 AppID，用 [IUserReviewsService.GetAppReviews](https://partner.steamgames.com/doc/webapi/IUserReviewsService#GetAppReviews) 和 [ISteamNews.GetNewsForApp](https://partner.steamgames.com/doc/webapi/ISteamNews#GetNewsForApp)。评测 API 匿名可用但限流较低；遇到 429 就降低频率、按服务器提示退避，不反复重试。新闻接口是公告或新闻，不是玩家评论。公开讨论与指南可尝试 `https://steamcommunity.com/app/<AppID>/discussions/` 和 `https://steamcommunity.com/app/<AppID>/guides/`，只引用完整可读条目。旧的 `store.steampowered.com/appreviews` 已弃用，实测跳商店首页。
- **PlayStation Store**：用公开搜索找与游戏版本、地区匹配的商品页，读 “Ratings and reviews”。只写该页面当时可见的评分、数量和文字评价，不把其数值当全平台口碑。Xbox 等商品页用于核实发行信息；只有实际读到评分或评论时才引用。
- **Reddit**：以中英文名和版本名做外部网页搜索，如 `site:reddit.com GTA VI (impressions OR hours OR performance)`。优先游戏专版或对应主机社区，直接读普通帖子网页和可见评论。匿名 `.json` 在搜索缓存里可能有结果，但在云浏览器直连曾被明确 403；不作生产依赖。官方 RSS 已停止支持，不把旧公共 API 当新项目的默认入口。
- **机核 GCORES**：以 [RSS 原地址](https://www.gcores.com/rss)做发现，交给 XML/RSS 读取器；普通网页提取器可能报不支持 XML。对已有主题另用 `site:gcores.com` 搜索，文章页可读图文。区分编辑评测、普通玩家投稿和节目简介；有 AI 生成标记注明，不能将节目简介当完整访谈。
- **篝火营地**：从[官网](https://gouhuo.qq.com/)或[评测栏目](https://gouhuo.qq.com/evaluate)按中文名发现，点进 `/content/detail/…`。搜索索引和简单网页提取曾漏掉普通浏览器能匿名打开的[评测正文](https://gouhuo.qq.com/content/detail/0_20261117180854_mVSHCFzbB)。若出现缓存未命中或空壳，可换支持渲染的公开页面读取方式一次。默认是媒体资料，不当玩家评论源。
- **其乐 Keylol**：用 `site:keylol.com` 加游戏名、平台及“体验/通关/攻略”，也可由论坛版面发现。公开[主题页](https://keylol.com/forum.php?mod=viewthread&tid=1056089)可读主楼，附件和部分楼层可能受限。新闻汇总优先追原出处，别把转帖和原帖算成两份反馈。
- **电玩帮**：用 `site:vgover.com` 加游戏名及体验关键词，直读[公开帖子](https://www.vgover.com/news/247450)。自述时长或设备仅作上下文，不当身份或事实认证。
- **补充入口**：贴吧只用已经公开可读的[热议聚合页](https://tieba.baidu.com/hottopic/browse/hottopic?topic_id=28370067)发现话题，截断片段不算读到原帖；知乎只用可直读的公开专栏。NGA 抽查的访客受限原帖、微信/小黑盒等国内 App 不纳入。没有真实读取结果的第三方抓取服务不列为已验证方案。

### Steam 接口对照

用已知 Steam 游戏 AppID 对照网络与解析问题。两个接口均曾用 AppID 440（TF2）匿名返回 JSON；下例仅用于连通性检查；`filter:1`（Recent）按发表时间倒序，不限制日期。正式查近 7 天（或用户指定窗口）时，在同一个 `input_json` 里同时传 `date_range_start` 和 `date_range_end`（Unix 秒，含首尾）；缺一会忽略范围。按结果的 `timestamp_created` 核对，不用更新时间替代。取多页用响应 `cursor`。空的或未传 `languages` 默认英语；查所有语言显式传 `["all"]`，或指定所需语言。不要用 `day_range` 限制 Recent；它只用于 Helpful，且没结果时该模式可能扩大范围。优点和缺点都取样，不仅看最有帮助的热帖。

```sh
curl -fsS --max-time 15 -G \
  'https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/' \
  --data-urlencode 'input_json={"appid":440,"filter":1,"num_per_page":5}'
curl -fsS --max-time 15 \
  'https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=440&count=3'
```

若执行环境不能出网，使用可拿到公开响应的读取入口，不把超时当站点拒绝。确认返回的是相应 AppID 的内容和正确格式，不把跳转后的主页当成功。

## 证据与交付

- 记录原文链接、日期、平台和证据类型：官方公告、商店聚合评分、媒体实测、玩家自述、转载或索引线索。作者没有说自己玩过、只复述他人或只看过预告的内容不计作实玩样本。按原始 URL 或帖子 ID 去重；没读到原文时明确标成线索，不据此概括口碑。
- 读取器不支持格式、缓存未命中和网络超时可换合适的解析入口；站点明确要求验证或拒绝时停止，不登录、不绕过。只读公开素材，不采集私人信息，不按小样本算全体好评率。
- 成品先写结论，再给日期/平台、具体好评和争议、附原文。想介绍新游时优先说明玩法和亮点，有合适的官方截图或主视觉可注明来源；开发幕后区分开发者原话和媒体推测。来源不足就写清只验证到什么，不凑数。
