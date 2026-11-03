---
name: capability-landscape-generator
description: 根据项目代码自动生成 AI 可读的能力全景图文档 (capability-landscape.md)。使用场景：当用户需要为项目生成结构化的能力文档、需要 AI 理解项目架构、或需要制作项目能力图谱时触发。生成内容包括：实体模型、API 端点、核心能力模块、业务流程、约束与 SLA 等 YAML 结构化信息。
---

# Capability Landscape Generator

本 Skill 用于从项目代码中提取关键信息，生成标准化的能力全景图文档。

---

## 一、Skill 用途

能力全景图 (Capability Landscape) 是一种结构化文档，用于：

1. **AI 理解项目**：让 AI 快速掌握项目架构、实体关系、API 能力
2. **知识沉淀**：系统化记录项目的核心能力和业务流程
3. **自动化文档**：减少人工编写文档的工作量

生成的文档特点：

- YAML 结构化格式，便于 AI 解析
- 覆盖实体模型、API、流程、约束等完整维度
- 支持增量更新和版本管理

---

## 二、使用时机

触发本 Skill 的典型场景：

- "为这个项目生成能力全景图"
- "帮我生成 capability-landscape.md"
- "生成项目的 AI 能力文档"
- "分析代码结构，生成能力文档"
- "为 XXX 项目创建能力图谱"

---

## 三、生成流程

### 步骤 1：确认项目路径

首先确认要分析的项目路径：

```plaintext
项目路径：<用户指定的项目目录>
```

若用户未指定，询问："请提供项目代码的路径"

### 步骤 2：识别项目类型

检查项目特征文件，识别技术栈：

| 特征文件 | 项目类型 |
| --- | --- |
| `go.mod` | Go 后端服务 |
| `pom.xml` / `build.gradle` | Java 后端服务 |
| `requirements.txt` / `pyproject.toml` | Python 后端服务 |
| `package.json` (无前端框架) | Node.js 后端服务 |
| `package.json` (含 React/Vue) | 前端项目 |

根据项目类型选择相应的分析策略，详见 `references/code-analysis-guide.md`。

### 步骤 3：代码扫描与分析

按以下顺序扫描代码，提取信息：

**3.1 实体模型提取**

- 搜索数据模型定义文件
- 提取实体名称、表名、字段、关系
- 参考：`references/code-analysis-guide.md` 第二节

**3.2 API 端点提取**

- 搜索路由定义文件
- 提取 HTTP 方法、路径、认证方式
- 从 handler/controller 推断请求/响应结构

**3.3 核心模块提取**

- 扫描 `modules/`、`services/`、`controllers/` 目录
- 识别模块职责和依赖关系

**3.4 业务流程推断**

- 从入口 API 追踪调用链
- 识别关键步骤和决策点

**3.5 基础设施识别**

- 检查配置文件识别存储组件
- 识别消息队列、缓存等中间件

### 步骤 4：生成文档

使用 `assets/capability-landscape-template.md` 作为模板，填充提取的信息：

```bash
# 输出文件路径
<project_path>/capability-landscape.md
```

生成规则：

- YAML 块必须格式正确
- 表格必须对齐
- 不确定的信息标记为 `<待补充>` 或 `<TBD>`
- 在文档末尾添加 "待确认事项" 章节（如有）

### 步骤 5：质量检查

生成后检查：

- [ ] YAML 格式正确
- [ ] 所有实体有 primary_key
- [ ] 所有 API 端点有 auth 字段
- [ ] 流程步骤有明确 id
- [ ] 无 `undefined` / `null` 占位符

---

## 四、参考资源

### references/template-structure.md

定义文档的标准结构和各章节必填字段，确保生成文档的一致性。

**使用方式**：生成前读取此文件，了解每个章节应该包含什么内容。

### references/code-analysis-guide.md

定义如何从不同技术栈的代码中提取信息的具体方法。

**使用方式**：识别项目类型后，参考对应章节的提取方法。

### assets/capability-landscape-template.md

空白模板文件，包含完整的章节结构。

**使用方式**：复制此模板，填充从代码中提取的信息。

---

## 五、输出格式

生成的文档结构：

```plaintext
1. 文档元数据 (YAML)
2. 系统定位与核心理念
   - 系统定位 (YAML)
   - 问题-解决方案映射表 (Markdown 表格)
3. 核心概念模型
   - 实体定义 (YAML)
   - 实体关系邻接表 (Markdown 表格)
4. 能力全景分层
   - API 层 (YAML)
   - 核心能力层 (YAML)
   - 基础设施层 (YAML)
5. 业务流程全链路 (YAML)
6. 约束与 SLA (YAML)
7. 常见问题 FAQ (YAML)
8. 附录 (YAML)
9. AI 解析指南 (Markdown)
```

---

## 六、注意事项

1. **不要编造信息**：无法从代码确定的信息，标记为 `<待补充>`
2. **保持一致性**：实体名称、字段名与代码保持一致
3. **增量更新**：若项目已有 capability-landscape.md，先读取现有内容再更新
4. **安全考虑**：不要在文档中包含密码、密钥等敏感信息

---

## 七、示例命令

```plaintext
用户：为 /path/to/project 生成能力全景图

执行流程：
1. 识别项目类型 (Go)
2. 扫描代码：
   - models/*.go → 提取实体
   - router.go → 提取 API
   - services/*.go → 提取模块
3. 生成文档 → /path/to/project/capability-landscape.md
4. 报告完成
```

