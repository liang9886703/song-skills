#!/bin/bash

# Graphify 离线安装脚本 v0.5.0+baidu1
# 支持多种安装方式，自动选择最合适的方法

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PACKAGES_DIR="$SKILL_DIR/packages"
WHEEL_FILE="$PACKAGES_DIR/graphifyy-0.5.0+baidu1-py3-none-any.whl"

echo "======================================"
echo "Graphify 离线安装脚本"
echo "版本: 0.5.0+baidu1"
echo "======================================"
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3 命令"
    echo "请确保 Python 3.10+ 已安装"
    exit 1
fi

PYTHON=$(command -v python3)
echo "✓ Python 环境: $PYTHON"
$PYTHON --version

# 检查 pip
if ! $PYTHON -m pip --version &> /dev/null; then
    echo "❌ 错误: pip 不可用"
    echo "请安装 pip: python3 -m ensurepip"
    exit 1
fi

echo "✓ pip 可用"

# 检查 wheel 文件
if [ ! -f "$WHEEL_FILE" ]; then
    echo "❌ 错误: 未找到 wheel 文件"
    echo "预期路径: $WHEEL_FILE"
    exit 1
fi

echo "✓ 找到 wheel 文件: $(basename "$WHEEL_FILE")"
echo "  大小: $(du -h "$WHEEL_FILE" | cut -f1)"
echo ""

# 检查是否已安装
if $PYTHON -c "import graphify" 2>/dev/null; then
    INSTALLED_VERSION=$($PYTHON -c "import graphify; print(graphify.__version__)" 2>/dev/null || echo "unknown")
    echo "ℹ️  graphifyy 已安装 (版本: $INSTALLED_VERSION)"
    echo "   如需重新安装，请先卸载: pip uninstall graphifyy"
    echo ""
    read -p "是否继续重新安装? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "取消安装"
        exit 0
    fi
    echo "正在卸载旧版本..."
    $PYTHON -m pip uninstall -y graphifyy || true
fi

echo "开始安装 graphifyy v0.5.0+baidu1..."
echo ""

# 尝试多种安装方式
INSTALL_SUCCESS=false

# 方法 1: 用户级安装（推荐）
echo "尝试方法 1: 用户级安装 (--user)..."
if $PYTHON -m pip install --user --no-index --find-links="$PACKAGES_DIR" "$WHEEL_FILE" 2>/dev/null; then
    echo "✓ 安装成功（--user）"
    INSTALL_SUCCESS=true
elif $PYTHON -m pip install --no-index --find-links="$PACKAGES_DIR" "$WHEEL_FILE" 2>/dev/null; then
    echo "✓ 安装成功"
    INSTALL_SUCCESS=true
elif $PYTHON -m pip install --user --no-index --find-links="$PACKAGES_DIR" "$WHEEL_FILE" --break-system-packages 2>/dev/null; then
    echo "✓ 安装成功（--break-system-packages）"
    echo "⚠️  警告: 使用了 --break-system-packages 选项"
    INSTALL_SUCCESS=true
fi

if [ "$INSTALL_SUCCESS" = true ]; then
    echo ""
    echo "======================================"
    echo "✅ 安装成功！"
    echo "======================================"
    echo ""

    # 验证安装
    if $PYTHON -c "import graphify; print(f'Graphify 版本: {graphify.__version__}')" 2>/dev/null; then
        echo "✓ 验证通过"
        echo ""
        echo "使用方法:"
        echo "  graphify install              # 为当前目录生成知识图谱"
        echo "  graphify install <path>       # 为指定目录生成知识图谱"
        echo "  graphify analyze              # 分析知识图谱"
        echo "  graphify --help               # 查看完整帮助"
        echo ""
    else
        echo "⚠️  警告: 安装完成但无法导入 graphify 模块"
        echo "   可能需要重启终端或重新加载 PATH"
    fi
else
    echo ""
    echo "======================================"
    echo "❌ 安装失败"
    echo "======================================"
    echo ""
    echo "所有安装方式都失败了，可能的原因:"
    echo "1. Python 环境权限限制"
    echo "2. pip 版本过旧"
    echo "3. 系统依赖缺失"
    echo ""
    echo "请尝试手动安装:"
    echo "  python3 -m pip install --user $WHEEL_FILE"
    echo ""
    exit 1
fi
