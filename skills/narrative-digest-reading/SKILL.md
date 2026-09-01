---
name: narrative-digest-reading
description: Compress long narrative texts into plot/event digests for skip-reading. Use for novels, serial fiction, biographies, oral histories, long reportage, transcripts, or any long article where the user wants “what happened” rather than argument/idea summarization.
---

# Narrative Digest Reading

Use this skill when the user says things like:

- “小说太长了不想看”
- “这几章讲了啥”
- “只讲故事情节”
- “把几章浓缩成一段文本”
- “长文章分块阅读”
- “叙事类文章帮我跳读”
- “按章节/段落压缩剧情”

The core task is **narrative compression**, not generic summarization.

## Difference from ordinary summarization

Generic summaries often abstract into themes, viewpoints, and arguments. For narrative reading, preserve:

- who did what
- where/when it happened
- cause → action → consequence
- relationship changes
- reveals, twists, clues, foreshadowing
- what the reader needs to remember for later

Avoid over-abstracting into “the author discusses…” unless the text is actually argumentative.

## Input handling

1. Accept text, Markdown, chapters, URLs, PDF/epub/docx converted to text, or user-pasted excerpts.
2. If the source is copyrighted and the user asks to find pirated/full text online, refuse that path and offer:
   - official reading links/search terms;
   - digesting user-provided text or lawful excerpts;
   - per-chapter summaries from content the user supplies.
3. Split long sources by natural boundaries first: chapter, heading, scene break, timestamp. If none exist, chunk by length while avoiding cutting mid-scene when possible.

## Digest levels

Offer or choose an appropriate level:

### Micro
One sentence per chapter/chunk.

### Standard
One paragraph per 3–5 chapters/chunks, focusing on plot movement.

### Arc
One section per 10–20 chapters/chunks, summarizing the major conflict, reversals, and current state.

### State tracker
Maintain across chunks:

- characters and current goals
- factions/organizations
- relationship changes
- timeline
- mysteries/foreshadowing
- key objects/settings
- unresolved questions

## Default output format

For each block:

```md
## 第 X-Y 章 / Chunk X-Y

### 剧情浓缩
一段话讲清这几章发生了什么，按因果顺序写。

### 关键事件
- ...
- ...

### 人物/关系变化
- A：...
- B：...

### 伏笔/设定/未解问题
- ...

### 跳读建议
- 必看：...
- 可略读：...
```

If the user asks for extreme compression, return only the “剧情浓缩” paragraph.

## Style for this user

- Prefer concise Chinese.
- Do not write literary criticism unless asked.
- Do not moralize about reading shortcuts.
- When the user wants “几章浓缩成一段”， obey the compression target and avoid tables/lists unless helpful.
- Keep names and causal links accurate; if uncertain, mark uncertainty instead of inventing.

## Workflow

1. Identify whether the text is narrative or argumentative.
2. Determine chunk boundaries.
3. For each chunk, extract events in chronological/causal order.
4. Compress events into a readable plot paragraph.
5. Update state tracker only with facts that will matter later.
6. Periodically merge several chunk digests into an arc summary.

## Pitfalls

- Do not turn plot into vague themes.
- Do not omit names; readers need entity continuity.
- Do not summarize every scene equally; privilege turning points.
- Do not quote large copyrighted passages back; digest in your own words.
- Do not use pirated “全文免费/无弹窗/精校版” sites as the source path when the user asks to find a novel online.
