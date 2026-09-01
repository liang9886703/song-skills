---
name: external-article-repository-tracing
description: "Trace an article to its verified GitHub repository."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, web, github, wechat, source-verification]
    related_skills: [github-repository-research]
---

# External Article → GitHub Repository Tracing

Use when a user provides an article, blog post, newsletter, or WeChat URL and asks for the corresponding GitHub repository, source project, or code implementation.

## Evidence-first workflow

1. **Read the source article first.** Extract title, author/account, project names, explicit links, code/package names, repository owners, and distinctive quoted phrases.
2. **Use URL-aware readers in a fallback chain.** For WeChat, prefer the available Exa reader (`web_fetch_exa`); then try another browser/anti-detection reader or a general reader. Do not assume an old tool name such as `crawling_exa` is available.
3. **Search by semantic identifiers.** Query GitHub/web search with the article title, project name, author, and distinctive technical phrases. Search a short-link token only as a secondary hint; opaque short IDs can yield coincidental or unrelated matches.
4. **Validate candidates.** Require direct article evidence or at least two independent matches among: article hyperlink, author/account identity, repository README, package/module names, code snippets, project branding, or a citation/backlink.
5. **Classify the result.** Report `confirmed` only with direct/cross-validated evidence. Report `lead/unconfirmed` when evidence is merely topical. Never present a noisy search result as the corresponding repository.
6. **Handle blocked pages honestly.** If CAPTCHA or anti-bot protection prevents reading and title/text cannot be recovered from search, ask the user for the article title, opening paragraph, or screenshot. Do not fabricate a repository or overstate a candidate.

## WeChat-specific notes

- A short URL like `https://mp.weixin.qq.com/s/<opaque-id>` may not expose the title and the opaque ID is not a reliable project identifier.
- Jina may return a CAPTCHA shell instead of article content; detect this before extracting anything.
- Search-engine results for the exact URL can be noisy or map to related articles. Treat them as discovery hints, not proof.
- When reporting failure, state the concrete blocker and the minimal extra input needed from the user.

## Reporting format

For a confirmed result:

- **仓库：** canonical GitHub URL
- **依据：** where the article names/links it and what repo evidence matches
- **置信度：** confirmed

For an unconfirmed result:

- **状态：** 暂未确认
- **已检查：** readers/searches attempted
- **候选：** only if useful, clearly labeled as unconfirmed
- **需要用户补充：** title, opening text, project name, or screenshot

Keep the response concise. The user asked for identification, so lead with the repository or the concrete blocker rather than a long account of every failed attempt.

## Pitfalls

- Do not infer the repository from a generic topic, a similar project title, or a search result that merely mentions GitHub.
- Do not use a failed reader response as if it were article content.
- Do not retry the same blocked endpoint indefinitely; switch readers or ask for a discriminating excerpt.
- Do not claim “not found” solely because one search engine has no result; say “not confirmed with the available evidence.”

## Supporting material

- `references/wechat-reader-fallbacks.md` — concise provider/tool behavior and verification checks for blocked WeChat article reads.
