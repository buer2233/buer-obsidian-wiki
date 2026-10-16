---
type: source
title: "LLM Wiki 模式"
created: 2026-09-23
updated: 2026-09-23
source_type: idea-file
author: "Andrej Karpathy"
date_published: 2026-04-04
url: "https://gist.github.com/karpathy"
confidence: high
tags:
  - 来源
  - LLM
  - 知识库
  - Obsidian
status: live
key_claims:
  - "多数文档类 LLM 系统仍是 chunk-first RAG，知识不累积"
  - "LLM Wiki 以持久化的 markdown 知识库替代每次查询重检索"
  - "三层架构：不可变原始来源 / LLM 维护的 wiki / schema 约定文件"
  - "三个操作：ingest、query、lint"
related:
  - "[[wiki/概念/wiki一词与Wiki知识库]]"
  - "[[wiki/来源/_index]]"
sources:
  - ".raw/claude-obsidian-ecosystem-research.md"
  - ".raw/笔记/2026-09-23_wiki一词与Wiki知识库.md"
---

# LLM Wiki 模式

## 来源信息

| 项目 | 内容 |
|---|---|
| 作者 | Andrej Karpathy |
| 发布形式 | GitHub gist（他称之为 **「idea file」**：只分享设计，由读者自己的 agent 定制实现） |
| 发布日期 | 2026-04-04 |
| 影响 | 单文件 gist 获 5,000+ stars / 5,000+ forks，被视为 2026 年最具影响力的 agent memory 文档之一 |
| 本地落地 | 本 vault 的 `WIKI.md` 明确声明「基于 Andrej Karpathy 的 LLM Wiki 模式」 |

## 核心主张

Karpathy 指出的问题是：多数基于文档的 LLM 系统仍是 **chunk-first RAG**——保存原始文档、查询时检索片段、每次都让模型从零综合答案。具体痛点：

- 跨 5 份文档的综合问题，每次都要重新寻找并拼接片段
- **交叉引用不是预先建好的**
- **矛盾不会被预先标记**
- **综合不累积**——问同一个问题两次，就做两遍功

LLM Wiki 把**维护工作交给 LLM**：新增来源时由 AI 整合（更新实体页、修订摘要、标注矛盾）；查询时交叉引用已经存在；wiki 随每个来源、每个好答案变得更丰富。

**Karpathy 的比喻**：

> **Obsidian 是 IDE，LLM 是程序员，wiki 是代码库。**（人看图谱视图，AI 在另一侧编辑）

## 三层架构

| 层 | 内容 | 本地映射 |
|---|---|---|
| **原始来源**（不可变） | 文章、论文、图片、数据、会议转录、代码导出。LLM 只读不改，是真源 | `.raw/`（126 文件） |
| **Wiki**（LLM 拥有） | 来源摘要页、实体页（人物/公司/概念）、主题综合页、对比分析、`overview.md` | `wiki/`（135+ md） |
| **Schema**（steering 文件） | 目录结构约定、页面格式与命名、ingest/query/lint 工作流 | `WIKI.md` |

## 三个操作

| 操作 | 流程 |
|---|---|
| **Ingest** | 读源 → 抽取持久事实/实体/概念/矛盾 → 写或更新互链页面 → 更新索引与日志。**一次摄入通常触碰 10–15 个页面**，而非只存一份摘要 |
| **Query** | 先读 `hot.md`（可能已有答案）→ 读 `index.md` 定位相关页 → 读 3–5 个页面 → 综合作答并引用 wikilink → **把好答案归档回 wiki** |
| **Lint** | 健康检查：孤立页面、死链、过时主张、缺失概念页、缺交叉引用、frontmatter 缺口、空章节。输出到 `wiki/meta/lint-report-YYYY-MM-DD.md` |

## 两个特殊文件

| 文件 | 作用 |
|---|---|
| `index.md` | 面向内容的全量目录（页面链接、摘要、分类、新鲜度） |
| `log.md` | **仅追加**的时间顺序记录，新条目置顶，形如 `## [YYYY-MM-DD] operation \| title` |

## 分工原则

- **人的工作**：整理来源、提出好问题、思考其意义
- **LLM 的工作**：摘要、交叉引用、归档、记账（bookkeeping）

> **wiki 才是产品。聊天只是界面。**

## 与 RAG 的取舍

| 场景 | 更优选择 |
|---|---|
| 个人知识库 / 小团队共享研究上下文（约 50K–100K tokens 以内） | **LLM Wiki**（换取查询加速与持久综合） |
| 百万级 tokens、语料每小时变化的大规模检索 | **RAG** |

**代价**：摄入更重、schema 须持续维护、lint 若漏掉矛盾会累积。

## 生态衍生

- **Open Knowledge Format（OKF）**：gist 走红数日后由 Google 形式化的厂商中立版本
- **OpenKnowledge（Inkeep，2026-06）**：产品化实现，含所见即所得编辑器与 agent 接线（`ok init`）

## 对本项目/学习的价值

- 本 vault 即该模式的完整落地，其三层结构与 `ingest`/`query`/`lint` 流程可直接作为**企业级知识管理**的参考设计。
- 概念层拆解见 [[wiki/概念/wiki一词与Wiki知识库|wiki 一词与 Wiki 知识库]]。
- **AI 测试迁移点**：模式中「检索结果 vs 维护后的知识产物」这一区分，可映射为 AI 产品评测的指标设计问题。

## 🔗 关联

- [[wiki/概念/wiki一词与Wiki知识库]] — 概念详解
- [[wiki/index]] — 本 vault 主索引

**本 vault 的 schema 层文件**：`WIKI.md`（vault 根目录）