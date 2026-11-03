# Tooling And Config Rules

初始化或调整 TypeScript 项目、`tsconfig`、ESLint、Prettier 时读取本文件。

## tsconfig 基线

没有项目现有配置时，可从以下基线开始，再按运行环境调整：

```jsonc
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

## Prettier 基线

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always"
}
```

## ESLint 建议

| 规则 | 设置 |
| --- | --- |
| `@typescript-eslint/no-explicit-any` | `error` |
| `@typescript-eslint/explicit-function-return-type` | `warn`，重点关注导出函数 |
| `@typescript-eslint/no-unused-vars` | `error` |
| `@typescript-eslint/consistent-type-imports` | `error` |
| `@typescript-eslint/no-non-null-assertion` | `warn` |
| `@typescript-eslint/prefer-nullish-coalescing` | `error` |
| `@typescript-eslint/prefer-optional-chain` | `error` |
| `@typescript-eslint/strict-boolean-expressions` | `warn` |
| `@typescript-eslint/naming-convention` | `error`，按项目约定配置 |

## 配置调整原则

- 不盲目覆盖现有配置，先理解项目运行环境。
- Node 项目优先考虑 `NodeNext`；前端构建项目按 bundler 约定处理。
- 库项目通常需要 `declaration` 和 `declarationMap`。
- 应用项目未必需要生成声明文件。
- 新增严格选项时评估现有代码修复成本。
