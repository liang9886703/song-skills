# Core Code Rules

普通 TypeScript 代码、函数、类、模块、异步和错误处理任务读取本文件。

## 命名

| 构造 | 约定 | 示例 |
| --- | --- | --- |
| 变量 / 函数 | `camelCase` | `getUserName`, `isActive` |
| 布尔变量 | 带语义前缀的 `camelCase` | `isLoading`, `hasAccess`, `canEdit` |
| 模块级常量 | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| 局部常量 | `camelCase` | `defaultTimeout` |
| 类 | `PascalCase` | `UserService` |
| 文件名 | `kebab-case.ts` | `user-service.ts` |
| 私有字段 | `camelCase`，不加 `_` | `private count: number` |

- 不要给接口加 `I` 前缀。
- 不要给类型或接口加 `Type` / `Interface` 后缀。
- 除循环索引和泛型参数外，避免单字母变量。
- 2 个字符缩写保持全大写（`ID`、`IO`）；3 个及以上用 PascalCase（`Http`、`Api`）。

## 变量与常量

- 默认使用 `const`；只有需要重新赋值时使用 `let`。
- 不使用 `var`。
- 变量声明靠近第一次使用处。
- 每条语句只声明一个变量。
- 提取对象属性时优先使用解构。
- 对不可变字面量对象或数组使用 `as const`。

## 函数

- 导出函数和公共函数必须显式标注返回类型。
- 顶层具名函数优先使用函数声明。
- 回调和短内联逻辑优先使用箭头函数。
- 位置参数最多 3 个；更多参数用 options object。
- 不使用 `arguments`，改用 rest 参数。
- 不使用 `Function` 类型，写具体函数签名。
- 函数应只做一件事，逻辑最好不超过 30 行。
- 优先提前返回，减少嵌套。

```typescript
interface CreateUserOptions {
  readonly name: string;
  readonly email: string;
  readonly role?: Role;
}

export function createUser(options: CreateUserOptions): User {
  const { name, email, role = Role.Viewer } = options;
  return { name, email, role };
}
```

## 类

- 优先组合而不是继承。
- 构造后不应变化的属性使用 `readonly`。
- 成员排序：静态字段、实例字段、构造函数、静态方法、公共方法、受保护方法、私有方法。
- 成员使用显式访问修饰符：`public`、`protected`、`private`。
- 不给私有成员加 `_` 前缀。
- 需要运行时私有性时使用 `#` 私有字段。
- 简单构造赋值可使用参数属性。
- 避免只有静态方法的类；改用模块内普通函数。

## 模块与导入

- 优先使用命名导出。
- React 组件只有在项目约定要求时才使用默认导出。
- 类型导入 / 导出使用 `import type` / `export type`。
- 导入分组顺序：Node 内置、外部包、内部别名、父级相对路径、同级相对路径。
- 每组导入之间留一个空行。
- 避免 `import * as`，除非需要模块命名空间。
- `index.ts` barrel 文件保持轻量，不放业务逻辑。

## 异步与 Promise

- 优先使用 `async` / `await`，避免长 `.then()` 链。
- 异步函数返回类型标注为 `Promise<T>`。
- 独立并发任务使用 `Promise.all()`。
- 单个失败不应中断其他任务时使用 `Promise.allSettled()`。
- 避免不必要的 `new Promise()`。
- 顺序异步迭代使用 `for...of` + `await`，不要用 `forEach`。

## 错误处理

- 不要写空 `catch`，不要静默吞错。
- 领域错误使用继承自 `Error` 的自定义错误类。
- `catch` 变量按 `unknown` 处理，使用前先收窄。
- 库中的预期失败可使用 `Result` / `Either` 模式。
- 资源清理放在 `finally` 或显式释放流程中。
- 日志至少包含操作名、关键输入摘要和错误堆栈。

```typescript
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };
```

## 注释与格式

- 公共 API、导出函数、类、接口和类型使用 TSDoc。
- 只解释非显而易见的设计意图、约束或副作用。
- 不保留注释掉的废弃代码。
- 无项目格式配置时使用：2 空格、分号、单引号、多行尾逗号。
- 所有控制结构都使用大括号。
- 软行宽 100，硬行宽 120。
