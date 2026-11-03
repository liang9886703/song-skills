# React TSX Rules

编写或修改 React、JSX、TSX、组件 props、hook 相关代码时读取本文件。

## 组件定义

- 使用函数声明或具名函数表达式，不使用匿名组件。
- props 定义为 `interface`，不要内联在参数中。
- props 字段默认标记为 `readonly`。
- 不使用 `React.FC`。
- 返回类型标注为 `React.ReactElement` 或 `React.ReactNode`。
- 只有项目约定要求时才使用默认导出。

```tsx
interface UserCardProps {
  readonly user: User;
  readonly onSelect?: (userId: string) => void;
}

export function UserCard({ user, onSelect }: UserCardProps): React.ReactElement {
  const handleClick = useCallback(() => {
    onSelect?.(user.id);
  }, [onSelect, user.id]);

  return (
    <div className="user-card" onClick={handleClick} role="button" tabIndex={0}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}
```

## Props 与状态

- props 表达组件外部契约，状态表达组件内部变化。
- 优先受控组件，除非项目或库要求非受控。
- 事件回调类型写清楚，不用 `Function`。
- 组件状态应避免存储可从 props 或其他 state 推导出的值。
- DOM 事件类型使用 React 提供的类型，例如 `React.ChangeEvent<HTMLInputElement>`。

## Hook

- 昂贵计算使用 `useMemo`，稳定回调使用 `useCallback`。
- 不为便宜计算或无下游引用稳定性需求的函数滥用 memo。
- 依赖数组必须完整，不能为了消除 lint 报错随意删依赖。
- 多组件复用的逻辑提取为自定义 hook。
- 自定义 hook 名称以 `use` 开头，并返回清晰的对象或元组。

## 文件结构

1. 导入
2. 类型 / 接口
3. 常量
4. 组件函数
5. 模块私有辅助函数

## 可访问性

- 可点击非按钮元素必须有合适的 `role`、键盘交互和 `tabIndex`。
- 优先使用语义 HTML 元素。
- 表单控件应有关联 label。
- 图标按钮需要可访问名称，例如 `aria-label`。
