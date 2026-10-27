# Type System Rules

类型建模、泛型、枚举、null/undefined、断言和类型守卫任务读取本文件。

## 类型与接口

- 对象形状优先使用 `interface`。
- 联合类型、交叉类型、映射类型、条件类型、元组和原始类型别名使用 `type`。
- 函数签名优先使用 `type`。
- 公共 API 的返回类型必须显式标注。
- 局部变量类型明显时让 TypeScript 推断。
- 避免空接口；确实需要时写注释解释意图。
- 使用 `Record<K, V>`，不要写 `{ [key: string]: V }`。
- 使用 `Partial`、`Pick`、`Omit`、`Required` 等工具类型派生类型，避免重复定义。

```typescript
interface User {
  readonly id: string;
  name: string;
  email: string;
}

type Status = 'active' | 'inactive' | 'suspended';
type Comparator<T> = (a: T, b: T) => number;
```

## `any` 与 `unknown`

- 避免新增 `any`；每个 `any` 都应视为技术债。
- 外部输入、反序列化结果和不可信数据优先用 `unknown`。
- 使用类型守卫、schema 校验或显式收窄后再访问属性。
- 如果因第三方库限制必须使用 `any`，将范围压到最小，并加说明。

## 枚举与字面量联合

- 小集合且不需要命名空间能力时，优先使用字符串字面量联合类型。
- 需要枚举时优先字符串枚举。
- 不使用没有显式值的数字枚举。
- 不在同一个 enum 中混用字符串成员和数字成员。
- `const enum` 只在确认构建链支持且确实需要零运行时成本时使用。

```typescript
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
```

## 泛型

- 简单泛型使用 `T`、`U`、`K`、`V`。
- 多个类型参数或语义不明显时使用 `TKey`、`TValue`、`TResult` 等描述性名称。
- 能添加约束时添加约束：`<T extends SomeType>`。
- 类型参数只使用一次时，通常说明泛型不必要。
- 不要为了“看起来通用”引入泛型。

```typescript
export function getProperty<T, K extends keyof T>(value: T, key: K): T[K] {
  return value[key];
}
```

## Null 与 Undefined

- 启用并尊重 `strictNullChecks`。
- 默认用 `undefined` 表示缺失值；对接外部 API 时按 API 的 `null` 语义处理。
- 优先使用可选链 `?.` 和空值合并 `??`。
- 不使用非空断言 `!`，除非能证明值一定存在，并写注释说明。
- 使用 `satisfies` 校验类型而不是扩大或强行断言类型。

```typescript
const displayName = user.nickname ?? user.name ?? 'Anonymous';
```

## 类型断言与类型守卫

- 优先使用类型守卫，不优先使用 `as`。
- 使用 `as const` 做字面量收窄。
- 状态机和结果类型使用带 `kind` 或 `type` 字段的可辨识联合。
- 避免 `as unknown as T` 双重断言。
- 必须断言时，加短注释说明为什么编译器无法推断但运行时安全。

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
}
```
