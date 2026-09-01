---
name: ai-product-tool-evaluation
description: Use when comparing AI product tools.
---

# AI Product Tool Evaluation

Use this skill when a user asks whether AI product tools are “the same kind of thing,” or asks to compare tools such as Figma, Magic Patterns, v0, Lovable, Codex, Bolt, Replit, or domestic equivalents.

## Core rule

Do not compare tools by feature-count or marketing labels. Compare the job they take over and the artifact they produce:

1. **Design source** — visual specification, components, Design System, collaboration.
2. **Prototype** — high-fidelity, interactive product exploration.
3. **Frontend code** — runnable UI components and page implementation.
4. **Full application** — frontend plus data, auth, backend workflows, preview, and deployment.
5. **Repository engineering** — changes inside an existing codebase, tests, CI, git history, and architecture constraints.

A useful one-line framing is: “X is a ___; Y is a ___.” Avoid saying two products are equivalent merely because both accept natural-language prompts.

## Evaluation dimensions

For each product, assess:

- Primary user: designer, product manager, developer, or non-technical builder.
- Input surface: canvas, prompt, screenshot, repository, terminal, or hosted project.
- Primary output: design file, prototype, source code, deployed app, or repository change.
- Stack and architecture control.
- Data/auth/backend ownership.
- Export and portability: source code, git integration, database access, independent deployment.
- Iteration loop: visual editing, prompt refinement, code review, or test-driven changes.
- Best-fit project stage: exploration, prototype, MVP, or production maintenance.
- Lock-in and migration cost.
- Fit with the user's existing stack and repository.

## Comparison procedure

1. Identify the user's actual goal: explore UI, validate a product, generate frontend code, ship an MVP, or modify an existing project.
2. Verify current official positioning when the products may have changed. Prefer official pages/docs; if access is unavailable, state that the comparison is based on general positioning and avoid brittle feature claims.
3. Put tools on the same axis before comparing. A compact table should include “定位 / 产物 / 控制力 / 适合场景.”
4. Distinguish platform-generated applications from agents that operate inside an existing repository.
5. Give a recommendation for the user's concrete project instead of ending with an undifferentiated list.
6. Mention the decisive unknowns that require a trial: code export, database portability, custom backend integration, self-hosting, and generated-code quality.

## Practical positioning map

- Figma: design source and collaboration.
- Magic Patterns: AI-assisted visual/product exploration and interactive prototypes.
- v0: prompt-to-frontend/full-stack web implementation, generally strongest around UI code.
- Lovable and similar “AI app builders”: prompt-to-MVP application platforms with backend/deployment abstractions.
- Codex and repository coding agents: engineering agents that inspect and modify a real codebase, run commands/tests, and preserve project architecture.

Treat these as broad categories, not permanent feature boundaries; products increasingly overlap.

## Recommendation heuristic

- Existing repository + explicit stack + architecture constraints → prefer a repository coding agent.
- Unclear UI direction → use an AI prototyping/design tool first.
- Need a disposable or fast MVP → use an AI app builder, then evaluate portability before committing.
- Need a durable design language and team review → use a design collaboration tool.
- Need domestic deployment or service ecosystem → evaluate the domestic app builder's export, hosting, and data-control path rather than assuming it matches Lovable.

## Pitfalls

- Do not equate “can generate a page” with “can build and maintain a product.”
- Do not call a coding agent a design tool; its output is repository changes, not necessarily polished visual exploration.
- Do not recommend replacing an existing Vue/React project with a hosted app builder without discussing migration and lock-in.
- Do not make detailed claims about pricing, framework support, export, or integrations without checking current official documentation.
- Do not bury the conclusion under a feature inventory; state the category and recommendation first.

## Reference

See `references/tool-positioning-session.md` for a condensed comparison pattern covering Figma, Magic Patterns, v0, Lovable, Codex, and domestic AI app builders.
