---
name: ai-morning-digest
description: Build and deliver the daily AI morning digest in pure cloud Google Drive mode using a multi-stage sub-agent architecture. Use when the user asks to generate, run, or update the daily AI morning digest, AI news briefing, or scheduled morning report.
---
# ai-morning-digest

Produce and publish the daily AI morning digest entirely in Google Drive without relying on a local Mac, using a main orchestrator plus modular sub-agents split by document type.

## When to Use

- The user asks to produce or refresh today's AI morning digest.
- A daily scheduled task triggers the morning digest run.
- A new document type with its own writing prompt needs to be added into the digest pipeline.

## Cloud Resources

- Source list Google Doc (`优秀 AI 信息源`): `1cbzQ5e92UxDC75cdemcvUs1Q7SpOZ97htfLb5s0mTSU` (always skip `aihot.news`).
- State spreadsheet (`digest-state`): `1vwcRuszpGjQxClznuAqWPPUb6dvFp52Hlf5n26ZCtnc` (`pointer`, `seen_items`, `projects`, `outbox`).
- Drive `daily` folder: `1nNxETkBFwvlvhHDQ678dGTvaSarPeQ4m`.
- Drive `projects` folder: `1bB_VjqSzsDxPKTM51XmKBo1gc7oWiXQ7`.
- Drive `archive` folder: `1ZFpDtYjfRvwdKGzRhOVatfBZM1RZUMZs`.

## Workflow

### Stage 0: Read State and Time Window (Main Agent)

1. Read `digest-state` tabs `pointer`, `seen_items` (7-day article/paper dedup), and `projects` (30-day GitHub project dedup and catalog).
2. Define the active window `[last_analysis_time, current_analysis_time]` in `Asia/Shanghai`.

### Stage 1: Fetch and Deduplicate (1 Fetcher Sub-Agent)

Dispatch one fetcher sub-agent with the time window, `seen_items`, and `projects` snapshot:

- Read `优秀 AI 信息源` and skip `aihot.news`.
- Check all configured streaming web sources and Gmail senders (`lenny@substack.com`, `lenny+how-i-ai@substack.com`, `lenny+community-wisdom@substack.com`, `pragmaticengineer@substack.com`, `pragmaticengineer+deepdives@substack.com`, `aisupremacy+agi@substack.com`, `aisupremacy+guides@substack.com`, `aisupremacy+siphon@substack.com`, `aiblewmymind@substack.com`, `aiblewmymind@mail.beehiiv.com`), plus a fallback inbox scan in the same time window to catch sender alias changes.
- Check GitHub Trending daily board and Hugging Face Papers daily board with no whitelist or de-prioritization filtering.
- Deduplicate articles and papers against 7-day `seen_items`; select up to 4 GitHub Trending repos by daily rank after skipping repos already in 30-day `projects`.
- Return only a clean grouped candidate list (title, exact URL, source, timestamp), `selection_log` draft (`included`, `deduplicated`, `excluded`), and `limitations`.

### Stage 2: Parallel Reading and Writing (Per-Type Sub-Agents)

Dispatch writer sub-agents in parallel by document category. Keep every article, paper, and repository as an individual item without merging. Preserve exact source URLs and empirical figures. When adding a new document category with a dedicated prompt in the future, add a new parallel sub-agent here.

- **Sub-Agent A (Blogs, Columns, and Newsletters)**: Read each full source page or email body. Write an in-depth Chinese analysis of 1,200 to 3,000 Chinese characters (max 4,000), never a short preview. Cover the core problem, key arguments or technical mechanisms, real-world cases or empirical data, actionable takeaways, and boundaries. Include `lead`, `key_points`, `terms`, `analysis`, and `source_url`.
- **Sub-Agent B (Hugging Face Papers)**: Read the daily top 10 paper pages (falling back to arXiv HTML if needed). Keep the standard morning-digest paper format with `lead`, `key_points`, `terms`, `analysis`, and `source_url`.
- **Sub-Agent C (GitHub Trending Projects, on demand)**: Dispatch only when Stage 1 yields new unrecorded repos. Follow the 9-chapter repository analysis structure in plain Chinese (avoid function names and file paths outside Chapter 7 tree and Chapter 8 verification evidence):
  1. Project URL and background
  2. Problem solved and evolution history (how a lightweight student MVP would solve it vs. production-grade concerns and trade-offs)
  3. Glossary (`terms`)
  4. Use cases and user stories
  5. How to run it
  6. End-to-end architecture and workflow
  7. Repository metadata and directory tree
  8. Completeness verification
  9. Recent iteration direction (up to 10 merged PRs from the past month with real links, dates, and changes) plus Similar Competitors (first check `已调研项目` against `one_liner` and `tags` in `digest-state.projects` and write `无` with no explanation if none match; then list high-confidence well-known projects without extra search, or `无`).
  Do not include `lead` or `key_points` for GitHub projects. Always provide `one_liner`, `tags`, `category_id`, and `category_label`.

### Stage 3: Assemble, Persist in Strict Order, and Report (Main Agent)

1. Check `daily` and `projects` for existing same-name files before creating new ones. Move any existing file to `archive` with a timestamp suffix first.
2. Write `YYYY-MM-DD.json` into `daily` (containing `date`, `title`, `site_url: "./index.html"`, `project_library_url: "./projects.html"`, `coverage`, `selection_log`, `limitations`, and `articles`).
3. For each new GitHub project, write a standalone `<article_id>.json` into `projects` (containing `key`, `name`, `repo_url`, `category_id`, `category_label`, `one_liner`, `tags`, `edition_date`, `edition_url: "./index.html"`, and the full `article` object).
4. **Cloud Fallback**: If background policy denies direct Drive file creation, split each JSON into chunks of at most 45,000 characters and append them to the `outbox` tab in `digest-state` (`target_folder_id`, `filename`, `part_index`, `total_parts`, `json_chunk`, `status="PENDING"`, `result_note=""`) for the bound Apps Script (`morning_digest_cloud_sync.gs`) to assemble and archive automatically.
5. **Update State Last**: Only after JSON files are created directly or written completely to `outbox`, update `digest-state` in place: append new repos (with `one_liner` and `tags`) to `projects`, append new articles and papers to `seen_items` while removing rows older than 7 days, and finally advance `pointer` (`last_analysis_time`, `current_analysis_time`, `latest_date`). If both persistence paths fail, do not advance `pointer`.
6. Report total item count, full `selection_log` breakdown, `limitations`, and Drive links to `YYYY-MM-DD.json`, any new project JSONs, and `digest-state`.

## Gotchas

- Never advance `pointer` before JSON persistence succeeds, or missed items will be skipped on the next run.
- Always run the Gmail fallback scan in addition to known sender addresses so alias changes are never missed.
- Do not fabricate details for truncated emails or blocked pages; record them transparently in `limitations`.
