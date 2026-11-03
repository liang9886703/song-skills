# 版本历史

## v1.0.0（2025-06-14）

- 初始版本发布
- 覆盖 6 大维度 21 项核心检查指标
- 支持生产级 Skill 的全面质量校验
- 输出标准化质量报告（含综合评分、问题清单、修复优先级）

## v1.0.1（2025-06-15）

- 优化 SKILL.md 结构，新增「错误处理」和「使用示例」标准章节
- 将详细检查标准和输出模板下沉到 references/ 目录，精简主文档篇幅
- 修复 D02 检查项中字面量 "待办" 被平台扫描器误检的问题
- 清除 `.dodo_managed.json` 等隐藏文件，满足平台发布规范

## v1.0.2（2026-06-15）

- 将「触发场景」章节升级为「触发条件」Markdown 表格格式，通过平台触发条件表格化检查
- 技能标识改为英文 `skill-quality-checker`，满足 OneTool 平台发布要求
- 发布到 OneTool 平台（skillId: 7589，隐藏空间）

## v1.0.3（2026-06-15）

- 新增 `scripts/pre-publish-cleanup.sh` 发布前清理脚本，自动删除 `.dodo_managed.json` 等隐藏文件
- 新增「发布前检查」章节，指引用户发布前执行清理

## v1.0.4（2026-06-15）

- 重新发布到 OneTool 平台（skillId: 7593，隐藏空间）

## v1.0.5（2026-06-15）

- 重新发布到 OneTool 平台（skillId: 7599，隐藏空间）

## v1.0.6（2026-06-15）

- 修复 `.dodo_managed.json` 反复再生问题：oneskill CLI 发布后会重新生成该文件，更新「发布后清理」章节强调发布后也必须执行清理
- 优化 `pre-publish-cleanup.sh` 脚本，输出更清晰的清理结果

## v1.0.7（2026-06-15）

- 重新发布到 OneTool 平台（skillId: 7600，隐藏空间）
- 发布后自动执行 cleanup，清除 `.dodo_managed.json` 残留

## v1.0.8（2026-06-15）

- 完善「发布后清理」章节：明确清理必须作为最后一步，任何平台 CLI 操作后都需要补充清理
- 根因分析：`.dodo_managed.json` 由 `dodo_cli prepare` 自动生成，oneskill / dodo_cli extension publish 均会触发重建