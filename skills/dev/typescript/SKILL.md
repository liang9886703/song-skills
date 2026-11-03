---
name: typescript
description: >
  TypeScript 编码规范、代码生成、代码审查、JavaScript 转 TypeScript、React TSX、
  测试与 tsconfig/ESLint/Prettier 配置指导。用户提到 TypeScript、TS、tsx、
  tsconfig、类型错误、类型重构、React TypeScript、TypeScript 测试或 TypeScript
  项目初始化时使用。
---

# TypeScript Skill

这个入口文件只负责路由和全局规则。详细规则按任务类型放在 `references/` 中，只有在任务需要时才读取。

## 全局优先级

1. 优先遵循当前仓库已有约定、lint 配置、formatter 配置和测试框架。
2. 用户明确要求高于本 skill 默认规则。
3. 没有本地约定时，使用本 skill 的默认 TypeScript 规范。
4. 修改现有代码时保持改动范围小，不做无关重构。

## 默认底线

- 开启并尊重严格类型检查，避免新增隐式 `any`。
- 能不用 `any` 就不用；外部未知输入优先用 `unknown` 并收窄。
- 优先使用 `const`、`readonly` 和明确的数据边界。
- 导出函数、公共 API、React 组件和异步函数需要显式返回类型。
- 优先使用命名导出；仅当项目约定要求时使用默认导出。
- 错误不能静默吞掉；异步代码优先使用 `async` / `await`。
- 使用项目现有格式化工具；无配置时按 2 空格、分号、单引号、尾逗号处理。

## 按问题类型加载规则

根据用户问题选择最小必要集合读取，不要一次性加载全部文件。

| 用户问题 / 任务类型 | 需要读取 |
| --- | --- |
| 写普通 TypeScript 函数、模块、业务逻辑 | `references/core-code.md`、`references/type-system.md` |
| 审查或重构 TypeScript 代码 | `references/review-refactor.md`，必要时再读相关专项文件 |
| 处理类型建模、泛型、枚举、null、类型断言 | `references/type-system.md` |
| 处理函数、类、模块组织、导入导出、异步和错误 | `references/core-code.md` |
| 编写或修改 React / JSX / TSX 组件 | `references/react-tsx.md`，必要时再读 `references/type-system.md` |
| 编写或修改测试 | `references/testing.md` |
| 新建项目、调整 `tsconfig`、ESLint、Prettier | `references/tooling-config.md` |
| 用户要求解释某条 TypeScript 规范 | 只读取包含该规则的对应文件 |

## 资源说明

- `references/`：按需加载的具体规则文档。
- `scripts/`：仅用于未来可执行自动化脚本，不放 Markdown 规则文本。

## 输出要求

- 生成代码时直接给出可用实现，不要复述整套规范。
- 审查代码时优先指出会导致 bug、类型漏洞、运行时风险或维护成本的问题。
- 如果本 skill 规则和项目现有规则冲突，说明冲突并按项目规则执行。
