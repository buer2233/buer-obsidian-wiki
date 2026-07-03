# claude-obsidian：智能体指令

本仓库既是个人使用Claude Code构建 的 Obsidian 知识库，使用 Andrej Karpathy 的 LLM Wiki 模式构建持久化、可累积增长的知识库。它支持**任何**遵循 Agent Skills 标准的 AI 编码智能体，包括 Codex CLI、OpenCode 等。

最初为 Claude Code 构建，技能遵循跨平台的 Agent Skills 规范。较新的技能（`wiki-fold`、`wiki-ingest`、`wiki-lint`）仅使用 `name` 和 `description` frontmatter（kepano 约定）。部分较早的技能仍保留可选的 `allowed-tools` 字段以兼容 Claude Code；不识别该字段的跨平台智能体应忽略它。

## 技能发现

所有技能位于全局插件路径 `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/<name>/SKILL.md`。Codex / OpenCode / 其他兼容 Agent Skills 的智能体在你创建符号链接后会自动发现它们：

```bash
# Codex CLI
ln -s ~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills ~/.codex/skills/claude-obsidian

# OpenCode
ln -s ~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills ~/.opencode/skills/claude-obsidian
```

或运行内置安装脚本：

```bash
bash bin/setup-multi-agent.sh
```

## 可用技能

| 技能 | 触发短语 |
|---|---|
| `wiki` | `/wiki`、set up wiki、scaffold vault |
| `wiki-ingest` | ingest、ingest this url、ingest this image、batch ingest |
| `wiki-query` | query、what do you know about、query quick:、query deep: |
| `wiki-lint` | lint the wiki、health check、find orphans |
| `wiki-fold` | fold the log、run a fold、log rollup（DragonScale 机制 1，可选启用） |
| `save` | /save、file this conversation |
| `autoresearch` | autoresearch、autonomous research loop |
| `canvas` | /canvas、add to canvas、create canvas |
| `defuddle` | clean this url、defuddle |
| `obsidian-markdown` | obsidian syntax、wikilink、callout |
| `obsidian-bases` | obsidian bases、.base file、dynamic table |

## 关键约定

- **知识库根目录**：包含 `wiki/` 和 `.raw/` 的目录
- **热缓存**：`wiki/hot.md`（会话开始时读取，会话结束时更新）
- **源文档**：`.raw/`（不可变：智能体永不修改这些文件）
- **生成的知识**：`wiki/`（智能体拥有，通过 wikilinks 链接到源文档）
- **清单文件**：`.raw/.manifest.json` 跟踪已摄取的源文档（增量追踪）

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

## 引导流程

当用户首次打开此项目时：

1. 阅读本文件（`AGENTS.md`）和项目 `CLAUDE.md` 以获取完整上下文
2. 阅读全局插件中的 `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/wiki/SKILL.md` 了解编排模式
3. 如果 `wiki/hot.md` 存在，静默读取它以恢复最近的上下文
4. 如果用户输入 `/wiki`（或"set up wiki"），按照 wiki 技能的脚手架工作流执行

## 参考资料

- 插件主页（公开规范版）：https://github.com/AgriciDaniel/claude-obsidian
- 社区抢先体验镜像（Pro）：https://github.com/AI-Marketing-Hub
- 模式来源：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- 交叉参考：https://github.com/kepano/obsidian-skills（权威的 Obsidian 专用技能）
