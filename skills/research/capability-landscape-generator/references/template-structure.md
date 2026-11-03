# Capability Landscape 文档模板结构

本文档定义 capability-landscape.md 的标准结构和生成规则。

---

## 文档层级结构

```
1. 文档元数据 (Document Metadata)
2. 系统定位与核心理念
3. 核心概念模型 (Entity Relationship Model)
4. 能力全景分层 (Capability Layers)
5. 业务流程全链路 (Business Process Flows)
6. 约束与SLA (Constraints and SLAs)
7. 常见问题 (FAQ)
8. 附录 (Appendix)
9. AI解析指南
```

---

## 一、文档元数据

```yaml
document_metadata:
  domain: <project_domain>           # 项目域名标识
  document_type: capability-landscape
  version: v1.0
  last_updated: <YYYY-MM-DD>
  maintainer: <team_email>
  target_reader:
    - human
    - ai_assistant
  change_log:
    - version: v1.0
      date: <YYYY-MM-DD>
      author: <author>
      changes: [initial_version]
```

---

## 二、系统定位与核心理念

### 2.1 系统定位

```yaml
system:
  name: <system_name>
  category: <system_category>        # 如：消息中台 / 数据平台 / 业务系统
  value_proposition: <一句话描述核心价值>
  domain:
    - <业务领域1>
    - <业务领域2>
```

### 2.2 核心问题-解决方案映射表

| 问题ID | 问题描述 | 解决方案 | 能力ID |
|-------|---------|---------|--------|
| PROBLEM_001 | <问题描述> | <解决方案描述> | <CAP_XXX> |
| PROBLEM_002 | ... | ... | ... |

---

## 三、核心概念模型

### 3.1 实体定义

```yaml
entities:
  <EntityName>:
    type: AGGREGATE_ROOT | ENTITY | VALUE_OBJECT
    description: <实体描述>
    table: <数据库表名>
    primary_key: <主键字段>
    foreign_key: [<外键引用>]
    unique_key: [<唯一键组合>]
    properties:
      - name: <字段名>
        type: <数据类型>
        constraint: <约束条件>        # 可选
        pattern: <正则模式>           # 可选
        examples: [<示例值>]          # 可选
        nullable: true/false          # 可选
        default: <默认值>             # 可选
```

### 3.2 实体关系邻接表

| 源实体 | 目标实体 | 关系类型 | 基数 | 约束 | 描述 |
|---------|----------|----------|:-----:|------|------|
| <EntityA> | <EntityB> | AGGREGATION/COMPOSITION/ASSOCIATION | 1:N/N:N | CASCADE_DELETE/INDEPENDENT | <关系描述> |

### 3.3 配置键命名规范（如有）

```yaml
config_key_spec:
  pattern: "<prefix>:<type>:<sub_ident>"
  description: <命名规范描述>
  segments:
    prefix:
      value: <固定前缀>
      constraint: FIXED
    type:
      enum: [<类型枚举>]
      required: true
    sub_ident:
      type: string
      pattern: <正则模式>
```

---

## 四、能力全景分层

### 4.1 对外能力层 (API)

```yaml
api_endpoints:
  prefix: <api_prefix>
  authentication_modes:
    NONE: []
    <AUTH_TYPE>: [<middleware_list>]

  group_by_auth:
    <auth_group_name>:
      description: <认证组描述>
      endpoints:
        - path: <HTTP_METHOD> <path>
          auth: <auth_type>
          request_schema: {<请求参数>}
          response_schema: {<响应结构>}
          constraints:
            - <约束条件1>
            - <约束条件2>
```

### 4.2 核心能力层

```yaml
internal_modules:
  <module_name>:
    id: CAP_<MODULE_ID>
    description: <模块描述>
    key_file: <核心代码文件路径>
    input: <输入数据结构>
    output: <输出数据结构>
    # 根据模块类型添加特定字段
```

### 4.3 基础设施层

```yaml
infrastructure:
  <component_name>:
    storage: [<存储类型>]
    # 组件特定配置
```

---

## 五、业务流程全链路

```yaml
flow: <FLOW_NAME>
  steps:
    - id: STEP_XXX_001
      name: <步骤名称>
      actor: <执行者>
      endpoint: <API端点>            # 可选
      module: <处理模块>             # 可选
      precondition: <前置条件>       # 可选
      action: <执行动作描述>
      constraint: <约束条件>         # 可选

  error_handling:
    - <STEP_XXX> fails: <处理方式>

  sla:
    - <性能指标描述>
```

---

## 六、约束与SLA

### 6.1 性能指标

```yaml
performance_sla:
  <metric_name>:
    metric: <指标类型>              # QPS / P99 latency / etc.
    target: <目标值>
    scope: <作用范围>
```

### 6.2 安全约束

```yaml
security_constraints:
  <constraint_name>:
    applies_to: [<API路径>]
    enforcement: <执行方式>
    rule: <约束规则>
```

### 6.3 容错与降级

```yaml
fault_tolerance:
  <failure_scenario>:
    impact: <影响程度>
    action: <处理动作>
    fallback: <降级方案>            # 可选
```

---

## 七、常见问题 (FAQ)

```yaml
faq:
  - question: <问题内容>
    answer: |
      <回答内容，支持多行>
```

---

## 八、附录

### 8.1 错误码体系

```yaml
error_codes:
  <error_category>:
    range: <错误码范围>
    examples:
      - code: <错误码>
        message: <错误消息>
        action: <处理建议>
```

### 8.2 监控与观测

```yaml
monitoring:
  <component>:
    url: <监控地址>
    metrics:
      - name: <指标名>
        type: Counter/Gauge/Histogram
        labels: [<标签>]
```

---

## 九、AI解析指南

固定内容，指导 AI 如何解析文档：

1. 元数据提取: 解析顶部 YAML 块
2. 实体提取: 解析 entities 段落
3. API端点解析: 解析 api_endpoints 段落
4. 流程解析: 解析 flow 段落
5. 约束解析: 解析 *_sla、*_constraints 段落
6. FAQ解析: 解析 faq 段落

**解析优先级**: YAML结构化数据 > Markdown表格 > 纯文本描述
