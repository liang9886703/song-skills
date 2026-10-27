# Testing Rules

编写、修改或审查 TypeScript 测试时读取本文件。

## 文件与命名

- 测试文件与代码同目录，或放在 `__tests__` 目录。
- 文件命名使用 `*.test.ts`、`*.spec.ts`、`*.test.tsx` 或 `*.spec.tsx`。
- 测试名称应读起来像一句行为描述。

## 测试结构

- 遵循 Arrange → Act → Assert。
- 每个测试验证一个断言概念；多个 `expect` 可以服务于同一概念。
- 优先测试公开行为，不测试实现细节。
- 业务逻辑追求较高覆盖率；不要为了样板代码追求 100%。

```typescript
describe('UserService', () => {
  describe('findById', () => {
    it('should return the user when the id exists', async () => {
      const user = await service.findById('user-1');
      expect(user).toEqual(expect.objectContaining({ id: 'user-1' }));
    });
  });
});
```

## Mock 与依赖

- mock 外部依赖，不 mock 被测模块本身。
- 优先通过依赖注入提升可测试性。
- mock 和 spy 要有类型。
- 异步测试必须 `await` 结果或返回 Promise。

```typescript
const mockFetch = jest.fn<Promise<User>, [string]>();
```

## 审查测试时重点

- 是否真的覆盖失败路径、边界条件和异步错误。
- 是否存在 flaky 行为，例如真实时间、真实网络、未隔离全局状态。
- 是否过度依赖内部实现，导致重构时测试无意义失败。
