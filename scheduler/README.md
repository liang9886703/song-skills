# scheduler

定时任务交接包，不参与 `skills/` 的普通 skillshare 同步。

## AI 信息晨报

统一入口：[ai-morning-digest/SKILL.md](ai-morning-digest/SKILL.md)。当前版本采用纯云端 Google Drive 工作流，通过 `digest-state` 管理时间指针、去重、项目库与失败回退，并按文档类型调度独立子代理。

- Google Drive 文档、表格与文件夹 ID，以及完整的分阶段执行规则，统一以 `SKILL.md` 为准。
