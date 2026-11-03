# Sidebar Utility Footer 比例统一 — blogV2 (2026-08-26)

## Problem

用户反馈侧边栏底部工具行（主题切换、X、LinkedIn、GitHub 图标）与上方导航行（Home、Musings、Projects）的比例不统一，看起来不像同一套组件。

## Root Cause

`SidebarUtilityFooter.vue` 的样式与 `SidebarNavigation.vue` 的 `.module-row` 不一致：

| 属性 | 导航行 (.module-row) | 底部工具行 (.sidebar-footer) |
|------|---------------------|---------------------------|
| padding | `5px 16px` | `10px 12px` |
| gap | `10px` | `4px` |
| 按钮尺寸 | 自适应 | 固定 `28×28px` |
| 图标大小 | `16px` | `16px`（但 X 图标 `14px`） |

底部行的 `padding` 更大但 `gap` 更小，按钮是固定大小的方块，导致视觉上比上面的文字行更紧凑、更"挤"。

## Fix

将 `.sidebar-footer` 的 `padding` 和 `gap` 改成与 `.module-row` 一致：

```css
.sidebar-footer {
  display: flex;
  align-items: center;
  gap: 10px;          /* was: 4px */
  border-top: 1px solid var(--line);
  padding: 5px 16px;  /* was: 10px 12px */
}
```

同时把 X 图标从 `14px` 改成 `16px`，与其他图标保持一致：

```css
.x-icon {
  width: 16px;   /* was: 14px */
  height: 16px;  /* was: 14px */
}
```

## 教训

1. **"像一行"的核心是 padding 和 gap 一致**，而不是按钮尺寸一致。导航行是文字+图标，底部是纯图标，按钮尺寸可以不同（28px vs 自适应），但行的 padding 和元素间距必须一致。
2. **图标大小要统一**：一个 14px 图标混在 16px 图标里会立刻显得"不属于这一行"。
3. **检查比例问题时，先看 padding/gap，再看 font-size/line-height，最后看元素尺寸**。前两者决定"行感"，后者决定"元素感"。

## Files Changed

- `app/components/navigation/SidebarUtilityFooter.vue` — 统一 padding/gap/图标大小

## Verification

浏览器中对比上方导航行和底部工具行的 computed style：
- `padding` 应相同（`5px 16px`）
- `gap` 应相同（`10px`）
