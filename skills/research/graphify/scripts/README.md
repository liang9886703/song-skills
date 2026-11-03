# Graphify 安装脚本说明

本目录包含 graphify 离线安装包的安装脚本。

## 脚本列表

### setup.sh

离线安装脚本，自动检测环境并选择最合适的安装方式。

**功能特性**:
- 自动检测 Python 和 pip 环境
- 支持多种安装方式（用户级、系统级、break-system-packages）
- 检查已安装版本并提供升级选项
- 完整的错误处理和用户友好提示
- 安装后验证

**使用方法**:
```bash
# 自动安装（首次使用 /graphify 命令时会自动调用）
cd scripts
./setup.sh

# 或者直接使用相对路径
./scripts/setup.sh
```

**安装方式优先级**:
1. 用户级安装 (`--user`) - 推荐，无需管理员权限
2. 系统级安装 - 如果有足够权限
3. Break system packages 安装 - 仅在必要时使用

## 离线安装包

**包名**: `graphifyy-0.5.0+baidu1-py3-none-any.whl`
**路径**: `../packages/graphifyy-0.5.0+baidu1-py3-none-any.whl`
**大小**: ~270 KB

此 wheel 包包含了 graphifyy 的所有核心依赖，支持完全离线安装。

## 版本信息

- **版本号**: 0.5.0+baidu1
- **Python 要求**: >=3.10, <3.14
- **平台**: 跨平台 (py3-none-any)

## 依赖说明

核心依赖（已包含在 wheel 包中）:
- networkx
- tree-sitter >= 0.23.0
- tree-sitter-* (多语言支持)

可选依赖（需要额外安装）:
- `[pdf]`: pypdf, html2text
- `[video]`: faster-whisper, yt-dlp
- `[watch]`: watchdog
- `[leiden]`: graspologic
- `[office]`: python-docx, openpyxl
- `[all]`: 所有可选依赖

## 故障排除

### 安装失败

如果自动安装失败，可以尝试手动安装：

```bash
# 方法 1: 用户级安装（推荐）
python3 -m pip install --user --no-index --find-links=../packages ../packages/graphifyy-0.5.0+baidu1-py3-none-any.whl

# 方法 2: 直接安装
python3 -m pip install --user ../packages/graphifyy-0.5.0+baidu1-py3-none-any.whl

# 方法 3: 使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install ../packages/graphifyy-0.5.0+baidu1-py3-none-any.whl
```

### 权限问题

如果遇到权限错误：
1. 优先使用 `--user` 选项进行用户级安装
2. 考虑使用 Python 虚拟环境
3. 联系系统管理员获取必要权限

### 导入错误

如果安装成功但无法导入：
1. 检查 Python 路径: `python3 -m site`
2. 重启终端或重新加载环境变量
3. 确认 `~/.local/bin` 在 PATH 中

### 版本冲突

如果已安装其他版本的 graphifyy：
```bash
# 卸载旧版本
pip uninstall graphifyy

# 重新运行安装脚本
./setup.sh
```

## 更新说明

### v0.5.0+baidu1 变更
- 升级到上游 0.5.0 版本
- 包含最新功能和性能改进
- 优化安装脚本错误处理
- 更新依赖包版本

### 从 v0.4.16+baidu1 升级
```bash
# 1. 卸载旧版本
pip uninstall graphifyy

# 2. 运行新的安装脚本
cd /path/to/new/graphify/skill
./scripts/setup.sh
```

## 技术细节

### Wheel 包结构
- 纯 Python 包 (py3-none-any)
- 包含所有必需的运行时文件
- 包含 skill 配置文件 (skill*.md)
- 预编译的 tree-sitter 语法支持

### 安装位置
- 用户级: `~/.local/lib/python3.x/site-packages/graphify`
- 系统级: `/usr/local/lib/python3.x/dist-packages/graphify`
- 可执行文件: `~/.local/bin/graphify` 或 `/usr/local/bin/graphify`

## 支持

如遇到问题，请提供以下信息：
- Python 版本 (`python3 --version`)
- pip 版本 (`pip --version`)
- 操作系统和版本
- 完整的错误信息
- 安装脚本输出
