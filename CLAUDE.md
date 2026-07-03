# claude-obsidian — Claude + Obsidian Wiki 知识库

此文件夹既是 Claude Code 插件，也是 Obsidian 知识库。

**插件名称：** `claude-obsidian`（v1.7+ "Compound Vault" — 参见 [docs/compound-vault-guide.md](docs/compound-vault-guide.md)；v1.8+ 新增方法论模式 — 参见 [docs/methodology-modes-guide.md](docs/methodology-modes-guide.md)）
**Skills：** `/wiki`、`/wiki-ingest`、`/wiki-query`、`/wiki-lint`、`/wiki-cli`（v1.7）、`/wiki-retrieve`（v1.7，需手动启用）、`/wiki-mode`（v1.8）
**知识库路径：** 此目录（直接在 Obsidian 中打开）

## 核心交互规则

- 你每次回复的开头必须先叫我:主人
- 如果忘记叫我，就是失焦了
- 所有回答都需要优先使用简体中文，专用词汇除外

## 此知识库的用途

此知识库展示了 LLM Wiki 模式 — 一个为 Claude + Obsidian 打造的持久化、可累积增长的知识库。放入任何资料来源，提出任何问题，Wiki 会随着每次会话变得更加丰富。

## 知识库结构

```
.raw/           源文档 — 不可变，Claude 只读不修改
wiki/           Claude 生成的知识库
_templates/     Obsidian Templater 模板
_attachments/   Wiki 页面引用的图片和 PDF
```

## Obsidian 图谱颜色配置

在 `.obsidian/graph.json` 的 `colorGroups` 中配置。两种查询方式：

**给文件夹下所有文件设置颜色：**
```json
{
  "query": "path:wiki/yuque/云原生",
  "color": { "a": 1, "rgb": 16711808 }
}
```

**给单独文件设置颜色：**
```json
{
  "query": "path:wiki file:index",
  "color": { "a": 1, "rgb": 16777215 }
}
```

注意：`query` 字段使用 Obsidian 搜索语法，不是文件路径。添加新的 wiki 分组时，同步在 `colorGroups` 中添加对应的颜色条目。

**重要：** Obsidian 图谱视图的「恢复默认设置」会清空所有颜色配置。如被重置，运行：
```bash
bash scripts/restore-graph.sh
```
备份文件位于 `.obsidian/graph.json.bak`。

## 使用方法

将源文件放入 `.raw/`，然后告诉 Claude："ingest [文件名]"。

提出任何问题。Claude 会先读取索引，然后深入到相关页面。

运行 `/wiki` 来搭建新的知识库或检查设置状态。

每处理 10-15 次导入后，运行 "lint the wiki" 以检测孤立页面和内容缺口。

## Wiki 整理规则（重要）

**当整理新文件进 Wiki 时，必须遵守以下规则：**

1. **分析关联关系：** 在整理新文档时，必须分析该文档与已有文档之间的关联关系
2. **建立索引：** 将新文档添加到相应的分类索引页面中
3. **创建关联链接：** 在文档之间建立双向链接（使用 `[[文档名]]` 语法）
4. **更新图谱：** 确保新文档在知识图谱中正确连接

**整理流程：**
1. 读取新文档内容
2. 分析文档主题和关键概念
3. 查找已有文档中的相关内容
4. 创建或更新分类索引
5. 建立文档间的关联链接
6. 更新主索引页面

**示例：**
```markdown
## 🔗 关联文档
- [[相关文档1]] — 描述关联关系
- [[相关文档2]] — 描述关联关系
```

## 跨项目访问

要在其他 Claude Code 项目中引用此知识库，请在该项目的 CLAUDE.md 中添加：

```markdown
## Wiki Knowledge Base
Path: /path/to/this/vault

When you need context not already in this project:
1. Read wiki/hot.md first (recent context, ~500 words)
2. If not enough, read wiki/index.md
3. If you need domain specifics, read wiki/<domain>/_index.md
4. Only then read individual wiki pages

Do NOT read the wiki for general coding questions or things already in this project.
```

## 插件 Skills

| Skill | 触发方式 |
|-------|---------|
| `/wiki` | 初始化、搭建、路由到子 skill |
| `ingest [source]` | 单个或批量导入源文档 |
| `query: [question]` | 从 wiki 内容中回答问题 |
| `lint the wiki` | 健康检查 |
| `/save` | 将当前对话保存为结构化的 wiki 笔记 |
| `/autoresearch [topic]` | 自主研究循环：搜索、抓取、综合、归档 |
| `/canvas` | 可视化层：向 Obsidian canvas 添加图片、PDF、笔记 |
| `/wiki-cli`（v1.7） | Obsidian CLI 传输封装；桌面上的默认变更路径 |
| `/wiki-retrieve`（v1.7） | 混合上下文 + BM25 + 余弦重排序检索（通过 `bash bin/setup-retrieve.sh` 手动启用） |
| `/wiki-mode`（v1.8） | 方法论模式（LYT / PARA / Zettelkasten / Generic）。通过 `bash bin/setup-mode.sh` 设置；由 wiki-ingest / save / autoresearch 调用以路由新页面 |
| `/think`（v1.9） | 10 原则思维循环（OBSERVE-OBSERVE-LISTEN-THINK-CONNECT-CONNECT-FEEL-ACCEPT-CREATE-GROW）作为可调用的工作流。适用于架构决策、审计、事后复盘、模糊的用户请求。每个其他 skill 都有一个"How to think"附录，将此框架映射到其具体工作 |

## 传输层（v1.7+）

`scripts/detect-transport.sh` 在首次运行时写入 `.vault-meta/transport.json`，并每周刷新。Skills 在修改知识库之前会查询该文件。回退链：Obsidian CLI → mcp-obsidian → mcpvault → 文件系统（始终可用的底层方案）。决策树参见：[wiki/references/transport-fallback.md](wiki/references/transport-fallback.md)。

## 并发控制（v1.7+）

`scripts/wiki-lock.sh` 提供基于文件的建议锁，用于安全的多写者导入。每次 wiki 页面写入都应通过 `wiki-lock acquire`/`release` 进行保护。默认过期时间为 60 秒；设计上允许跨进程释放。PostToolUse 钩子在持有锁期间会延迟 `git add`。这修复了 v1.6 中潜在的多写者数据损坏问题。

## 方法论模式（v1.8+）

通过 `bash bin/setup-mode.sh` 选择知识库的组织风格。提供四种模式：**generic**（v1.7 默认 — 无偏好）、**LYT**（Linking Your Thinking — MOC + 原子笔记）、**PARA**（Projects/Areas/Resources/Archives）、**Zettelkasten**（带时间戳的 ID、扁平结构、密集链接）。模式写入 `.vault-meta/mode.json`（默认被 gitignore；使用 `git add -f` 提交）。`wiki-ingest`、`save` 和 `autoresearch` 在归档新页面之前会调用 `python3 scripts/wiki-mode.py route <type> "<name>"` — 使用方的 skill 无需特殊处理。完整指南参见：[docs/methodology-modes-guide.md](docs/methodology-modes-guide.md)。这解决了 2026 年 5 月 compass 工件中的优先级缺口 5。

## 提交前验证器（v1.7.1+）

在为非平凡的工作流暂存更改之后、但在运行 `git commit` 之前，调度 `verifier` 代理（全局插件路径：`~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/agents/verifier.md`）。它读取 `git diff --cached`，应用 /best-practices 六重审查 + agent kernel，并以四个层级（BLOCKER / HIGH / MEDIUM / LOW）返回发现结果，附带 file:line 引用。该代理拥有只读工具（Read、Grep、Glob、Bash）— 只能检查不能修改，因此其输出纯粹是建议性的。这修复了 v1.7 审计中发现的问题：代码从 worker 直接到 commit，没有单独的验证器审查，BLOCKER B1（数据外泄同意缺口）就是这样溜过去的。参见 `docs/audits/v1.7.0-audit-2026-05-17.md` 第 10 节的回顾。

## MCP（可选）

如果你配置了 MCP 服务器，Claude 可以直接读写知识库笔记。
设置说明参见全局插件中的 `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/wiki/references/mcp-setup.md`。

## 发布博客文章

在发布新版本（git tag + `gh release create`）之后，运行：

```
/release-blog
```

这会在 https://agricidaniel.com/blog/ 上生成一篇博客文章，处理封面图片生成、SEO 元数据、FAQ 结构化数据、内部链接、sitemap/llms.txt 更新、Vercel 部署和 Google 索引。
