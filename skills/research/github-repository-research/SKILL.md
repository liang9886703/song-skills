---
name: github-repository-research
description: "Research and compare GitHub repositories: popularity, activity, positioning, README summaries, and market/category fit."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, research, repositories, comparison, popularity, activity]
    related_skills: [github-repo-management, github-auth]
---

# GitHub Repository Research

Use this skill when the user asks to compare GitHub repositories, judge which is more popular/active, summarize what projects do, or find external articles describing/benchmarking repos.

## Core workflow

1. **Collect canonical repo metadata first** using GitHub API, not search snippets:
   - stars: `stargazers_count`
   - forks: `forks_count`
   - watchers/subscribers: `subscribers_count`
   - open issues: `open_issues_count`
   - creation/update/push timestamps
   - default branch, language, topics, homepage, description
2. **Measure activity with time windows**:
   - commits in last 30 days
   - commits in last 90 days
   - issues/PRs updated in last 30 days
   - latest release date
   - approximate contributor count
3. **Read README excerpts** for positioning:
   - repo description is often too short; README usually contains the product/category claim.
   - Strip badges/images and extract the first meaningful headings/paragraphs.
4. **Separate popularity from activity**:
   - popularity: stars, forks, watchers, org reputation, age.
   - activity: pushed_at, recent commits, issue/PR updates, release cadence.
   - do not collapse these into one score unless the user asks.
5. **When searching external articles**, use targeted exact-name queries and expect noisy results for generic names like `warp`, `ax`, `best`, or `agent`.
   - Prefer exact quoted combinations: `"Multica" "Ruflo"`, `"OpenAgents" "Multica"`, `"google/ax" "Agent Executor"`.
   - If search engines return irrelevant matches, report that the exact article was not found yet rather than inventing it.

## Reliable `gh api` patterns

Authenticated `gh` avoids unauthenticated GitHub API rate limits:

```bash
gh auth status
```

Repo metadata:

```bash
gh api /repos/OWNER/REPO
```

Search endpoints must be forced to GET when using `-f`; otherwise `gh api` may send POST and GitHub returns 404:

```bash
gh api --method GET /search/repositories -f 'q=repo:OWNER/REPO' -f per_page=1

gh api --method GET \
  -H 'Accept: application/vnd.github.cloak-preview+json' \
  /search/commits \
  -f 'q=repo:OWNER/REPO committer-date:>=YYYY-MM-DD' \
  -f per_page=1

gh api --method GET /search/issues \
  -f 'q=repo:OWNER/REPO updated:>=YYYY-MM-DD' \
  -f per_page=1
```

Approximate contributor count via `Link` header:

```bash
gh api -i '/repos/OWNER/REPO/contributors?per_page=1&anon=1'
# parse page=N from rel="last" in the Link header
```

README extraction:

```bash
gh api /repos/OWNER/REPO/readme --jq .content | python3 -c 'import sys,base64; print(base64.b64decode(sys.stdin.read()).decode("utf-8","ignore"))'
```

## Deep source architecture tracing

When the user asks to "pull the repo and explain its principle/原理", shift from metadata research to source-grounded architecture tracing. See `references/source-architecture-tracing.md` for the reusable workflow.

Key additions to the core workflow:

1. Clone/update the repo and report path, branch, short commit, latest commit, and clean/dirty state.
2. Read README/package manifests for positioning, then trace actual entrypoints and construction paths.
3. For agent/tooling repos, inspect both the **tool registry** and the **core execution loop**; the registry shows capabilities, the loop shows how they are exercised.
4. Map advertised differentiators to concrete source paths and call chains before summarizing.
5. Final explanations should answer "why it can do X" as mechanisms, not marketing claims.

## Reporting format

For quick comparisons, produce:

1. **One-sentence conclusion**: highest popularity and highest activity.
2. **Table** with stars, forks, recent commits, updated issues/PRs, pushed_at, latest release.
3. **Per-repo role summary**: what it is, who it is for, and the category it belongs to.
4. **Caveats**: e.g. older repos have star accumulation advantage; search results for external articles may be noisy.

For deep source architecture reviews, produce:

1. **Repo metadata**: local path, branch, commit, clean/dirty status.
2. **One-sentence mechanism summary**.
3. **Layered architecture**: entrypoint → SDK/session/config → core loop → tools/subsystems.
4. **Capability chains** for the user's focus areas, with source paths.
5. **Engineering judgment**: what is genuinely distinctive, what is ordinary, and what to borrow.

## Pitfalls

- Do not treat `updated_at` alone as activity; it can change from stars/issues and not only code changes.
- Do not use unauthenticated GitHub API if `gh` is logged in; rate limits can block metadata collection.
- Do not state that an external article exists unless you have the URL/title/snippet or page content.
- Generic repo names (`warp`, `ax`) require disambiguating with owner/name or official product title.
