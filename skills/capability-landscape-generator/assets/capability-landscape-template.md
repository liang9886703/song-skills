# <项目名称> - 能力全景图

> **文档格式**：本文档采用结构化语义格式，同时支持人工阅读和AI自动解析。AI解析器请参考顶部的 `document_metadata` 段落提取元数据。

---

## 文档元数据 (Document Metadata)

```yaml
document_metadata:
  domain: <项目域名标识>
  document_type: capability-landscape
  version: v1.0
  last_updated: <YYYY-MM-DD>
  maintainer: <维护团队邮箱>
  target_reader:
    - human
    - ai_assistant
  change_log:
    - version: v1.0
      date: <YYYY-MM-DD>
      author: <作者>
      changes: [initial_version]
```

---

## 一、系统定位与核心理念

### 1.1 系统定位

```yaml
system:
  name: <系统名称>
  category: <系统分类>
  value_proposition: <核心价值主张>
  domain:
    - <领域1>
    - <领域2>
```

### 1.2 核心问题-解决方案映射表

| 问题ID | 问题描述 | 解决方案 | 能力ID |
|-------|---------|---------|--------|
| PROBLEM_001 | <描述系统解决的核心问题> | <对应的解决方案> | <CAP_XXX> |

---

## 二、核心概念模型 (Entity Relationship Model)

### 2.1 实体定义 (Entity Definitions)

```yaml
entities:
  <EntityName>:
    type: AGGREGATE_ROOT | ENTITY | VALUE_OBJECT
    description: <实体描述>
    table: <数据库表名>
    primary_key: <主键字段>
    foreign_key: [<外键引用>]
    properties:
      - name: <字段名>
        type: <数据类型>
```

### 2.2 实体关系邻接表 (Relationship Adjacency Table)

| 源实体 | 目标实体 | 关系类型 | 基数 | 约束 | 描述 |
|---------|----------|----------|:-----:|------|------|
| <EntityA> | <EntityB> | <RELATION_TYPE> | 1:N | <CONSTRAINT> | <描述> |

---

## 三、能力全景分层 (Capability Layers)

### 3.1 对外能力层 (External Capabilities - API)

```yaml
api_endpoints:
  prefix: <API前缀>
  authentication_modes:
    NONE: []

  group_by_auth:
    public:
      description: 公开接口
      endpoints:
        - path: GET /example
          auth: NONE
```

### 3.2 核心能力层 (Internal Capabilities)

```yaml
internal_modules:
  <module_name>:
    id: CAP_<MODULE_ID>
    description: <模块描述>
    key_file: <核心文件路径>
```

### 3.3 基础设施层 (Infrastructure)

```yaml
infrastructure:
  <component>:
    storage: []
```

---

## 四、业务流程全链路 (Business Process Flows)

### 4.1 主流程 (Main Flow)

```yaml
flow: MAIN_FLOW
  steps:
    - id: STEP_001
      name: <步骤名称>
      actor: <执行者>
      action: <执行动作>
```

---

## 五、约束与SLA (Constraints and SLAs)

### 5.1 性能指标 (Performance Metrics)

```yaml
performance_sla:
  <metric_name>:
    metric: <指标类型>
    target: <目标值>
```

### 5.2 安全约束 (Security Constraints)

```yaml
security_constraints:
  <constraint_name>:
    applies_to: []
    rule: <约束规则>
```

---

## 六、常见问题 (FAQ)

```yaml
faq:
  - question: <问题>
    answer: |
      <回答>
```

---

## 七、附录 (Appendix)

### 7.1 错误码体系 (Error Code System)

```yaml
error_codes:
  parameter_errors:
    range: 14001-14999
    examples: []
```

---

## AI解析指南 (AI Parsing Guide)

如果使用AI系统自动解析本文档，请遵循以下规则：

1. **元数据提取**: 解析顶部 `document_metadata` YAML块
2. **实体提取**: 解析 `entities` 段落
3. **API端点解析**: 解析 `api_endpoints` 段落
4. **流程解析**: 解析 `flow` 段落
5. **约束解析**: 解析 `*_sla`、`*_constraints` 段落
6. **FAQ解析**: 解析 `faq` 段落

**解析优先级**: YAML结构化数据 > Markdown表格 > 纯文本描述
