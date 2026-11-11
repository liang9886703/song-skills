---
name: project-pool
description: 个人项目池与技术知识库管理。支持检索、查看或追加开源项目、Agent 论文、AI 信息源、技术笔记与需求画像数据。触发词：记一下、记录项目、收藏项目、收藏论文、添加信息源、查项目池、项目池、project-pool、查论文收藏、需求画像。
---

# 个人项目池与知识库 (Project Pool)

本 Skill 用于统一维护和查询个人的开源项目、前沿论文、信息源与技术洞察。所有结构化数据作为本 Skill 内部资产，集中存储于本 Skill 目录下的 `data/` 文件夹中。

## 数据文件概览与结构

数据文件均位于本 Skill 的 `data/` 目录：

| 文件 | 描述 | 主要结构 / 字段 |
| :--- | :--- | :--- |
| `data/projects.yaml` | 精选开源项目与工具库 | `name`, `url`, `tags`, `desc`, `created_at` |
| `data/papers.yaml` | Agent 核心前沿论文与文章 | `title`, `url`, `category`, `purpose`, `core_content` |
| `data/sources.yaml` | 优质技术博客、资讯平台与一手源 | `name`, `url`, `type`, `tags`, `desc` |
| `data/insights.yaml` | 启发性观点与行业洞察 | `source_url`, `insight`, `tags`, `date` |
| `data/notes.yaml` | 技术调研、问答探测与架构记录 | `title`, `source`, `date`, `qa` (`q`, `a`) |
| `data/profiles.yaml` | 用户画像与话题/偏好边界 | `title`, `updated_at`, `strict_boundaries` |
| `data/tasks.yaml` | 个人规划与任务清单 | `title`, `updated_at`, `weekly_plan` |

## 触发与操作规则

### 1. 记录 / 收藏新项目（“记一下”、“收藏这个项目”）
当用户提供项目链接或名字并要求记录时：
1. 读取 `data/projects.yaml` 检查是否已收录（避免重复添加）。
2. 提取或向用户确认关键信息（名称、Canonical URL、Tags、简洁准确的 `desc`）。
3. 追加到 `data/projects.yaml` 末尾，保持 YAML 缩进与格式正确。

### 2. 收藏论文 / 文章（“收藏这篇论文”）
追加到 `data/papers.yaml`，包含：
- `title`: 论文或文章标题
- `url`: 官方链接或 arXiv 原文
- `category`: 分类（如任务执行优化、训练任务生成等）
- `purpose`: 解决了什么核心痛点/目的
- `core_content`: 核心方法或创新机制

### 3. 记录信息源或观点
追加到 `data/sources.yaml` 或 `data/insights.yaml`。

### 4. 查询与检索（“查一下我收藏了什么项目/论文”、“我的需求画像是什么”）
直接读取 `data/` 下对应 YAML 文件，按用户意图进行过滤、总结或格式化展示。
