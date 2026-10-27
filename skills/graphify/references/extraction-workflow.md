# Graphify 提取工作流

本文档描述如何使用 graphify 从各种内容源提取知识并构建知识图谱。

## 快速开始

### 基本命令

```bash
# 为代码库生成知识图谱
graphify install /path/to/repo

# 分析知识图谱
graphify analyze

# 生成报告
graphify report

# 导出知识图谱
graphify export --format json
```

## 支持的内容类型

### 1. 代码库

**支持的语言**:
- Python, JavaScript, TypeScript
- Go, Rust, Java, C, C++
- Ruby, C#, Kotlin, Scala
- PHP, Swift, Lua, Zig
- PowerShell, Elixir, Objective-C
- Julia, Verilog

**提取的知识**:
- 函数和类定义
- 模块依赖关系
- 函数调用关系
- 文档字符串

**示例**:
```bash
# 分析整个代码库
graphify install ~/projects/myapp

# 只分析特定文件类型
graphify install ~/projects/myapp --include "*.py"

# 排除某些目录
graphify install ~/projects/myapp --exclude "*/tests/*"
```

### 2. Markdown 文档

**提取的知识**:
- 标题层级结构
- 链接关系
- 代码块
- 列表和表格

**示例**:
```bash
# 分析文档目录
graphify install ~/docs

# 指定 Markdown 文件
graphify install ~/docs --include "*.md"
```

### 3. PDF 文档

**前置条件**:
```bash
pip install graphifyy[pdf]
```

**提取的知识**:
- 文本内容
- 段落结构
- 链接关系

**示例**:
```bash
graphify install ~/papers --include "*.pdf"
```

### 4. Office 文档

**前置条件**:
```bash
pip install graphifyy[office]
```

**支持格式**:
- DOCX (Word 文档)
- XLSX (Excel 表格)

**示例**:
```bash
graphify install ~/documents --include "*.docx,*.xlsx"
```

### 5. 视频内容

**前置条件**:
```bash
pip install graphifyy[video]
```

**功能**:
- 视频转录
- YouTube 视频下载和分析

**示例**:
```bash
# 分析本地视频
graphify install ~/videos --include "*.mp4"

# 分析 YouTube 视频
graphify install --youtube https://www.youtube.com/watch?v=xxxxx
```

## 知识图谱操作

### 查询和分析

```bash
# 查看图谱统计信息
graphify analyze

# 查看关键节点
graphify report --top 20

# 搜索特定节点
graphify search "function_name"

# 查看节点的邻居
graphify neighbors "module_name"
```

### 社区检测

```bash
# 使用 Leiden 算法进行社区检测
graphify cluster --algorithm leiden

# 查看社区信息
graphify analyze --communities

# 导出社区结构
graphify export --format json --communities
```

### 导出知识图谱

```bash
# JSON 格式（完整图谱）
graphify export --format json --output graph.json

# CSV 格式（节点和边）
graphify export --format csv --output nodes.csv

# SVG 可视化
graphify export --format svg --output graph.svg

# Neo4j 导入格式
graphify export --format neo4j --output neo4j/
```

## 高级工作流

### 1. 增量更新

实时监控代码变化并更新知识图谱：

```bash
# 监控当前目录
graphify watch

# 监控指定目录
graphify watch /path/to/project

# 指定更新间隔（秒）
graphify watch /path/to/project --interval 5
```

### 2. 批量处理

处理多个项目：

```bash
#!/bin/bash
for project in ~/projects/*; do
    echo "Processing $project..."
    graphify install "$project" --output "~/graphs/$(basename $project)"
done
```

### 3. 集成到 CI/CD

在持续集成流程中使用：

```yaml
# .github/workflows/knowledge-graph.yml
name: Update Knowledge Graph

on:
  push:
    branches: [main]

jobs:
  update-graph:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install graphify
        run: pip install graphifyy
      - name: Generate graph
        run: graphify install . --output graph.json
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: knowledge-graph
          path: graph.json
```

### 4. 与其他工具集成

**与 Neo4j 集成**:
```bash
# 导出到 Neo4j 格式
graphify export --format neo4j --output neo4j_import/

# 导入到 Neo4j
neo4j-admin import \
  --nodes=neo4j_import/nodes.csv \
  --relationships=neo4j_import/edges.csv
```

**与 Obsidian 集成**:
```bash
# 导出为 Obsidian Markdown
graphify export --format obsidian --output ~/ObsidianVault/
```

## 性能优化

### 缓存管理

```bash
# 查看缓存统计
graphify cache --stats

# 清空缓存
graphify cache --clear

# 指定缓存位置
graphify install ~/project --cache-dir /tmp/graphify_cache
```

### 并行处理

```bash
# 使用多个工作进程
graphify install ~/large_project --workers 4

# 批量处理大文件
graphify install ~/large_project --batch-size 100
```

## 常见模式

### 1. 代码库分析

```bash
# 完整分析流程
cd /path/to/repo
graphify install .
graphify analyze
graphify cluster --algorithm leiden
graphify report --top 30
graphify export --format json --output repo_graph.json
```

### 2. 文档知识提取

```bash
# 文档分析流程
cd /path/to/docs
graphify install . --include "*.md,*.pdf"
graphify analyze
graphify export --format obsidian --output ~/ObsidianVault/
```

### 3. 多模态内容分析

```bash
# 混合内容分析
cd /path/to/project
graphify install . \
  --include "*.py,*.md,*.pdf,*.docx" \
  --exclude "*/node_modules/*,*/venv/*"
graphify analyze --detail
graphify report
```

## 故障排除

### 常见问题

**问题**: 解析失败
```bash
# 查看详细错误信息
graphify install ~/project --verbose

# 跳过错误文件
graphify install ~/project --skip-errors
```

**问题**: 内存不足
```bash
# 减少批量大小
graphify install ~/large_project --batch-size 50

# 使用流式处理
graphify install ~/large_project --streaming
```

**问题**: 处理速度慢
```bash
# 增加工作进程
graphify install ~/project --workers 8

# 启用缓存
graphify install ~/project --cache-dir /tmp/cache
```

## 最佳实践

1. **定期更新**: 使用 `graphify watch` 保持图谱实时更新
2. **版本控制**: 将生成的图谱文件纳入版本控制
3. **增量构建**: 对大型项目使用增量更新而非完全重建
4. **合理过滤**: 使用 `--include` 和 `--exclude` 减少不必要的处理
5. **性能监控**: 定期查看 `graphify cache --stats` 优化缓存使用

## 更多资源

- 官方文档: https://github.com/safishamsi/graphify
- API 参考: 运行 `graphify --help` 查看完整命令列表
- 社区讨论: GitHub Issues
