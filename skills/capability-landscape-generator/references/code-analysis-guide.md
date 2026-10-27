# 代码分析方法指南

本文档描述如何从项目代码中提取信息以填充 capability-landscape.md 模板。

---

## 一、识别项目类型

### 后端服务项目

**特征文件**:
- `go.mod` / `go.sum` (Go)
- `pom.xml` / `build.gradle` (Java)
- `requirements.txt` / `setup.py` / `pyproject.toml` (Python)
- `package.json` (Node.js 后端)

**重点提取**:
- API 路由定义
- 数据模型/实体
- 数据库表结构
- 中间件/认证逻辑

### 前端项目

**特征文件**:
- `package.json` (含 React/Vue/Angular 依赖)
- `tsconfig.json` / `jsconfig.json`
- `vite.config.*` / `webpack.config.*`

**重点提取**:
- 页面/路由结构
- 组件层级
- API 调用接口
- 状态管理模型

### 全栈项目

**特征文件**: 同时包含前后端特征

**重点提取**: 整合前后端模型，梳理完整数据流

---

## 二、信息提取方法

### 2.1 实体提取

**数据库实体**:
- Go: `type XxEntity struct` / GORM model
- Java: `@Entity` / `@Table` 注解的类
- Python: `models.py` / SQLAlchemy / Django models
- SQL: `CREATE TABLE` 语句

**提取内容**:
```yaml
- 实体名称
- 表名
- 主键
- 外键关系
- 字段列表 (名称、类型、约束)
- 索引/唯一键
```

**示例识别**:
```
搜索模式:
- "struct" + "db:" tag (Go)
- "@Entity" 或 "@Table" (Java)
- "class.*Model" 或 "class.*Entity" (Python)
- "CREATE TABLE" (SQL migration files)
```

### 2.2 API 端点提取

**路由定义文件**:
- Go: `router.go` / `route.go` / `main.go` (http.HandleFunc)
- Java: `@RestController` / `@Controller` / `@RequestMapping`
- Python: `views.py` / `urls.py` / `routes.py`
- Node.js: `routes/*.js` / `app.use()`

**提取内容**:
```yaml
- HTTP 方法 (GET/POST/PUT/DELETE)
- 路径
- 认证方式 (从中间件推断)
- 请求参数 (从 handler 函数参数推断)
- 响应结构 (从返回类型推断)
```

**认证模式识别**:
```
- 无认证: 公开接口
- BDUSS/Session: 用户登录接口
- Token/JWT: API 认证接口
- 白名单: 内部服务调用
```

### 2.3 业务模块提取

**模块识别**:
- 目录结构: `modules/` / `services/` / `controllers/`
- 包名/命名空间
- 依赖注入配置

**提取内容**:
```yaml
- 模块名称
- 核心文件路径
- 输入/输出数据结构
- 核心逻辑 (从函数名推断)
- 依赖的其他模块
```

### 2.4 业务流程提取

**流程识别**:
- 入口函数 (handler/controller 方法)
- 调用链追踪
- 状态变更点

**提取方法**:
```
1. 找到入口 API 端点
2. 追踪 handler -> service -> repository 调用链
3. 识别关键决策点 (if/switch)
4. 记录外部调用 (DB/Cache/MQ/第三方API)
5. 标记异步操作
```

---

## 三、文档生成策略

### 3.1 分层生成顺序

1. **基础设施层** → 从配置文件、依赖项提取
2. **实体模型** → 从数据库代码提取
3. **核心能力层** → 从 service 层代码提取
4. **API 层** → 从路由定义提取
5. **业务流程** → 从调用链分析得出

### 3.2 信息补充来源

当代码无法提供完整信息时，检查:

- `README.md` / `readme.md`
- `docs/` 目录
- `api/` / `swagger/` 文档
- `config/` 配置文件
- 数据库 schema 文件
- 注释 (特别是 docstring / godoc / javadoc)

### 3.3 不确定信息处理

当无法确定信息时:

1. 标记为 `<待补充>` 或 `<TBD>`
2. 在文档末尾添加 "待确认事项" 章节
3. 不要猜测或编造信息

---

## 四、质量检查

生成后需检查:

- [ ] 所有实体都有 primary_key
- [ ] 所有 API 端点都有 auth 字段
- [ ] 流程步骤有明确的 id
- [ ] YAML 格式正确 (可用 yamllint 验证)
- [ ] 表格格式对齐
- [ ] 无 `undefined` / `null` 占位符
