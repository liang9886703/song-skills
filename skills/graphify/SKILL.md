---
name: graphify
description: 将代码库、文档、论文、图片等多模态内容转换成知识图谱，大幅减少 token 消耗（最高 71.5x）。离线定制版 v0.5.0，包含离线安装包。
---

# Graphify - 知识图谱构建工具（离线版）

将代码库、文档、论文、图片等多模态内容转换成知识图谱，大幅减少 token 消耗（最高 71.5x）。

## 版本说明

- **版本号**: 0.5.0+offline1
- **特性**: 离线定制版，包含离线安装包
- **更新内容**:
  - 升级到上游 0.5.0 版本
  - 包含最新功能和性能优化
  - 支持完全离线安装，无需连接 PyPI

## 快速开始

### 安装

本 skill 已包含完整的 graphifyy 离线安装包，首次使用时会自动安装：

```bash
# 自动安装（首次使用时触发）
/graphify --help

# 手动安装（可选）
cd scripts && ./setup.sh
```

### 基础用法

1. **为代码库生成知识图谱**

```bash
# 为当前目录生成知识图谱
/graphify install

# 为指定目录生成知识图谱
/graphify install /path/to/your/project

# 指定输出目录
/graphify install --output ~/Documents/graphs/myproject
```

2. **查询知识图谱**

```bash
# 查看统计信息
/graphify analyze

# 查看关键节点
/graphify report

# 导出为多种格式
/graphify export --format json
/graphify export --format csv
```

3. **实时监控代码变化**

```bash
# 监控当前目录
/graphify watch

# 监控指定目录
/graphify watch /path/to/project
```

## 支持的内容类型

- **代码**: Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, Ruby, C#, Kotlin, Scala, PHP, Swift, Lua, Zig, PowerShell, Elixir, Objective-C, Julia, Verilog
- **文档**: Markdown, PDF, DOCX, XLSX
- **多媒体**: 视频转录（需要额外安装 `[video]` 依赖）
- **其他**: Wiki 文档、知识库内容

## 高级功能

### 社区检测

使用 Leiden 算法进行社区检测：

```bash
/graphify cluster --algorithm leiden
```

### 导出知识图谱

```bash
# JSON 格式
/graphify export --format json --output graph.json

# CSV 格式（节点和边分别导出）
/graphify export --format csv --output nodes.csv

# SVG 可视化
/graphify export --format svg --output graph.svg
```

### 缓存管理

```bash
# 查看缓存大小
/graphify cache --stats

# 清空缓存
/graphify cache --clear
```

## 性能优化

Graphify 通过知识图谱显著减少 LLM 的 token 消耗：

- **平均减少**: 10-20x
- **最高可达**: 71.5x
- **适用场景**:
  - 大型代码库理解
  - 技术文档分析
  - 跨项目知识管理
  - RAG 应用构建

## 技术细节

### 离线安装说明

本 skill 包含预构建的 `graphifyy-0.5.0+offline1-py3-none-any.whl` 包，支持以下安装方式：

1. 用户级安装（推荐）
2. 系统级安装
3. 带 `--break-system-packages` 的安装（仅限必要情况）

安装脚本会自动选择最合适的方式，无需手动干预。

### 版本管理

- **版本号格式**: `x.y.z+offline1`
- **版本号 +offline1 标识**: 表示这是离线定制版本
- **兼容性**: 与上游版本 API 完全兼容

## 故障排除

### 安装问题

如果自动安装失败，可以手动运行安装脚本：

```bash
cd "<本机 graphify 技能目录>/scripts"
./setup.sh
```

### 权限问题

如遇到权限错误，安装脚本会自动尝试其他安装方式。如果所有方式都失败，请检查：

1. Python 环境是否正常
2. pip 是否可用
3. 是否有必要的文件系统权限

### 依赖问题

基础功能只需要核心依赖（已包含在 wheel 包中）。如需使用高级功能：

```bash
# PDF 支持
pip install graphifyy[pdf]

# 视频转录
pip install graphifyy[video]

# 完整功能
pip install graphifyy[all]
```

## 更新日志

### v0.5.0+offline1 (2026-04-27)
- 升级到上游 0.5.0 版本
- 包含最新功能和性能改进
- 优化离线安装流程
- 更新依赖包版本

### v0.4.16+offline1 (2026-04-22)
- 初始离线定制版本
- 支持离线安装
- 无需连接 PyPI

## 参考资源

- 原始项目: https://github.com/safishamsi/graphify
- 详细使用文档: 参见 `references/extraction-workflow.md`

## 适用场景

1. **代码库理解**: 快速了解新项目结构和依赖关系
2. **技术文档分析**: 自动提取文档中的知识结构
3. **研发知识管理**: 构建团队知识库的图谱化表示
4. **RAG 应用**: 为检索增强生成提供高效的知识检索

## 注意事项

- 本版本为离线定制版，版本号带有 `+offline1` 标识
- 已包含完整的离线安装包，首次使用会自动安装
- 如需更新，请重新下载最新的 skill 包
- 不建议通过 PyPI 更新，以保持版本一致性
