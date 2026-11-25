# bot

只绑定单个 Bot 的技能放在这里。布局上与 [`scheduler/`](../scheduler/README.md) 同级，但这里不是定时任务，也不参与 `skills/` 的 skillshare 同步。

把文件放进本仓库不会安装技能，不会写入常驻指令，也不会创建监听。

## last30days 话题归档

只给所有者的 last30days Bot（`41abf589-9a81-42df-a156-af345dd36299`）使用。不给 main，也不给其他 Bot。

- 流程：[last30days-ticket-archive/SKILL.md](last30days-ticket-archive/SKILL.md)
- 实例配置：[reference/instance.yaml](last30days-ticket-archive/reference/instance.yaml)
- 目的地说明：[reference/destination.md](last30days-ticket-archive/reference/destination.md)

启用步骤、常驻指令和“必须真的发出后台任务”都写在技能的启用一节。本目录当前只是仓库里的副本。
