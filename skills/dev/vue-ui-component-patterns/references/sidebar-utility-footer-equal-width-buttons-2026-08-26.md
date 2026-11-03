# Sidebar Utility Footer 等宽图标按钮 — blogV2 (2026-08-26)

## Problem

用户反馈底部工具行（主题切换、X、LinkedIn、GitHub 图标）虽然 padding/gap 已和导航行统一，但视觉上仍然"差点意思"。用户要求"把每个图标当成一个文字来看待，再和上面对齐"。

## Root Cause

之前的修复只统一了 `.sidebar-footer` 的 `padding` 和 `gap`，但按钮仍然是固定 `28×28px` 的小方块，在整行宽度中显得局促。用户希望每个图标像导航行中的"文字"一样，占据相等的空间，形成统一的节奏感。

## Fix

把 `.footer-icon-button` 从固定宽度改为 `flex: 1`，让每个按钮等分剩余空间：

```css
.footer-icon-button {
  display: flex;
  flex: 1;              /* was: width: 28px */
  height: 28px;
  align-items: center;
  justify-content: center;
  border: 0;
  border-radius: 6px;
  padding: 0;
  color: var(--ink-soft);
  background: transparent;
  text-decoration: none;
  transition: color 150ms ease, background-color 150ms ease;
}
```

## 关键教训

1. **"把图标当成文字"意味着等宽分配**：每个图标按钮占据相同的水平空间，就像文字在段落中占据相同的字距一样。
2. **用户明确拒绝了垂直堆叠**："别啊，样式还是得我之前那样，一行放 4 个"。底部必须保持单行横向排列，即使要和上方的垂直导航列表统一。
3. **统一感的层次**：先统一 padding/gap（行级），再统一元素尺寸（图标大小），最后统一空间分配（flex: 1）。

## Files Changed

- `app/components/navigation/SidebarUtilityFooter.vue` — 按钮改为 `flex: 1` 等宽

## Verification

浏览器中检查 computed style：
- `.sidebar-footer` 的 `padding` 应为 `5px 16px`
- `.sidebar-footer` 的 `gap` 应为 `10px`
- `.footer-icon-button` 的 `flex` 应为 `1 1 0%`
- 每个按钮的 `width` 应自动计算为等分后的值
