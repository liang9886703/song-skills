# FloatingOutline 宽度修正：从固定 220px 回到 max-content

## 背景

2026-08-26，用户在 blogV2 项目中反馈悬浮目录卡片"太宽了"。此前会话中曾将卡片宽度从 `max-content` 改为固定 `220px`（见 references/floating-outline-width-hotreload-2026-08-25.md），理由是"用户说卡片是文字最大长度，有上限，想要固定宽度"。

但用户实际看到固定宽度后的反馈是："太宽了"——左侧空出大量空白，文字右对齐后视觉上不平衡。

## 修正

将 `.outline:hover ul.outline-labels` 的宽度从：
```css
width: 220px;
max-width: min(252px, calc(100vw - 40px));
```

改回：
```css
width: max-content;
min-width: 140px;
max-width: min(252px, calc(100vw - 40px));
```

## 教训

1. **"有上限"不等于"要固定宽度"**：用户说"卡片是文字最大长度，而且有上限"是在描述现状（max-content 导致宽度不一致），不是在要求固定宽度。真正的需求是"不要太宽，也不要太窄"，`max-content + min-width + max-width` 组合就能满足。
2. **固定宽度在文字列表中容易显得空**：当大多数条目较短时，固定宽度会在左侧留下大量空白，尤其在文字右对齐的布局中，空白更明显。
3. **先给变体，再定稿**：如果当时给出 2-3 个宽度方案（固定 200px / max-content / max-content+min-width）让用户选择，可以避免这次往返。

## 相关引用

- 原固定宽度决策：references/floating-outline-width-hotreload-2026-08-25.md
- 宽度选择模式：Pattern 10 in vue-ui-component-patterns/SKILL.md
