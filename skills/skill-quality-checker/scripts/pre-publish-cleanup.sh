#!/bin/bash
# pre-publish-cleanup.sh
# 清理 SKILL 目录下的平台自动生成的隐藏/缓存文件
#
# 用法：
#   bash scripts/pre-publish-cleanup.sh              # 清理当前技能目录
#
# 执行时机：
#   1. oneskill create/update 之前（避免隐藏文件被打包）
#   2. oneskill create/update 之后（oneskill 会重新生成 .dodo_managed.json）
#
# 清理内容：
#   - .dodo_managed.json  — OneTool 平台自动生成的元数据缓存文件
#   - .DS_Store           — macOS 系统文件

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "🔍 清理目标: ${SKILL_DIR}"
echo ""

# 清理 .dodo_managed.json（OneTool CLI 发布时自动生成）
if [[ -f "${SKILL_DIR}/.dodo_managed.json" ]]; then
  rm -f "${SKILL_DIR}/.dodo_managed.json"
  echo "  🗑  已删除: .dodo_managed.json"
else
  echo "  ✅ 无需清理: .dodo_managed.json（不存在）"
fi

# 清理 .DS_Store
while IFS= read -r -d '' f; do
  rm -f "$f"
  echo "  🗑  已删除: ${f#${SKILL_DIR}/}"
done < <(find "${SKILL_DIR}" -name '.DS_Store' -print0 2>/dev/null)

echo ""
echo "✅ 清理完成"