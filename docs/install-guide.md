# claude-obsidian：安装指南

**Claude + Obsidian 知识伴侣**
版本 1.9.2 · 公开权威仓库：[github.com/AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) · 社区抢先体验镜像（Pro）：[AI Marketing Hub org](https://github.com/AI-Marketing-Hub)

> ℹ️ 以下安装命令使用**公开开源** URL（`AgriciDaniel/claude-obsidian`），推荐所有人使用，无需任何会员资格。[AI Marketing Hub Pro](https://www.skool.com/ai-marketing-hub-pro) 会员如需抢先体验开发中的功能，可将所有 `AgriciDaniel/claude-obsidian` 替换为 `AI-Marketing-Hub/claude-obsidian`，将插件 slug `claude-obsidian@agricidaniel-claude-obsidian` 替换为 `claude-obsidian@ai-marketing-hub-claude-obsidian`。

> **可选：DragonScale Memory 扩展。** 如果你需要扁平的提取式日志折叠、确定性页面地址、语义平铺检查和边界优先的自动研究主题选择，在基础安装完成后运行 `bash bin/setup-dragonscale.sh`。基础安装之外的额外前置条件：`flock`（Linux 标准自带；macOS 上通过 `util-linux` 获取）和 `python3`（用于平铺和边界辅助工具）。可选：如果你需要语义平铺检查（仅机制 3），安装 `ollama` 并拉取 `nomic-embed-text`；当 ollama 或模型不可用时会优雅跳过。边界优先评分器（机制 4）只需要 `python3`，无需 ollama。参见 [`docs/dragonscale-guide.md`](./dragonscale-guide.md) 了解面向用户的指南，`wiki/concepts/DragonScale Memory.md` 了解完整规范，`CHANGELOG.md` 了解 1.6.0 中发布的内容。

---

## 什么是 claude-obsidian？

claude-obsidian 是一个 Claude Code 插件 + Obsidian 知识库，用于构建和维护一个持久的、复利型的知识库。你添加的每个源文件都会被处理成交叉引用的 wiki 页面。你提出的每个问题都会从所有已读取的内容中提取答案。知识像利息一样复利增长。

基于 Andrej Karpathy 的 LLM Wiki 模式构建。

---

## 前置条件

| 工具 | 获取方式 | 备注 |
|------|---------|------|
| **Claude Code** | `npm install -g @anthropic-ai/claude-code` | 有免费套餐 |
| **Obsidian** | [obsidian.md](https://obsidian.md) | 免费 |
| **Git** | 大多数系统预装 | 选项 1 需要 |

---

## 安装

### 选项 1：克隆为知识库（推荐）

完整设置不超过 2 分钟。

```bash
git clone https://github.com/AgriciDaniel/claude-obsidian
cd claude-obsidian
bash bin/setup-vault.sh
```

然后在 Obsidian 中：**管理知识库 → 打开文件夹作为知识库 → 选择 `claude-obsidian/`**

在同一文件夹中打开 Claude Code 并输入 `/wiki`。

### 选项 2：安装为 Claude Code 插件

在 Claude Code 中安装插件是一个两步过程。首先添加市场目录，然后从中安装插件。

```bash
# 步骤 1：添加市场
claude plugin marketplace add AgriciDaniel/claude-obsidian

# 步骤 2：安装插件
claude plugin install claude-obsidian@agricidaniel-claude-obsidian
```

验证安装：
```bash
claude plugin list
```

在任何 Claude Code 会话中：输入 `/wiki`，Claude 会引导你完成知识库设置。

### 选项 3：添加到现有知识库

将此仓库中的 `WIKI.md` 复制到你的知识库根目录。然后在 Claude 中粘贴：

```
Read WIKI.md in this project. Then:
1. Check if Obsidian is installed. If not, install it.
2. Check if the Local REST API plugin is running on port 27124.
3. Configure the MCP server.
4. Ask me ONE question: "What is this vault for?"
Then scaffold the full wiki structure.
```

---

## 入门步骤

### 1. 搭建知识库框架

在 Claude Code 中输入 `/wiki`。Claude 将会：
- 检测你的知识库模式（网站、GitHub、企业、个人、研究或书籍/课程）
- 创建文件夹结构和核心 wiki 页面
- 设置 `wiki/index.md`、`wiki/hot.md`、`wiki/log.md` 和 `wiki/overview.md`

### 2. 放入你的第一个源文件

将任何文档放入 `.raw/`：
- PDF、markdown 文件、转录稿、文章、URL

告诉 Claude：`ingest [filename]`

Claude 读取源文件并创建 8-15 个交叉引用的 wiki 页面。

### 3. 提问

```
what do you know about [topic]?
```

Claude 读取热缓存、扫描索引、深入相关页面，然后给出综合答案，引用具体的 wiki 页面而非训练数据。

---

## 命令参考

| 命令 | Claude 执行的操作 |
|------|-----------------|
| `/wiki` | 设置检查、搭建框架，或继续上次的工作 |
| `ingest [file]` | 读取源文件，创建 8-15 个 wiki 页面，更新索引和日志 |
| `ingest all of these` | 批量处理多个源文件，然后进行交叉引用 |
| `what do you know about X?` | 读取索引 → 相关页面 → 综合答案 |
| `/save` | 将当前对话保存为 wiki 笔记 |
| `/save [name]` | 以指定标题保存 |
| `/autoresearch [topic]` | 自主研究循环：搜索、获取、综合、归档 |
| `/canvas` | 打开或创建可视化画布 |
| `/canvas add image [path]` | 向画布添加图片 |
| `/canvas add text [content]` | 添加 markdown 文本卡片 |
| `/canvas add pdf [path]` | 添加 PDF 文档 |
| `/canvas add note [page]` | 将 wiki 页面固定为链接卡片 |
| `lint the wiki` | 健康检查：孤立页面、死链接、知识空白 |
| `update hot cache` | 用最新的上下文摘要刷新 `hot.md` |

---

## 插件（预装）

在 **设置 → 社区插件** 中启用：

| 插件 | 用途 |
|------|------|
| **Calendar** | 右侧栏日历，带字数统计和任务标记点 |
| **Thino** | 快速备忘录捕获面板 |
| **Excalidraw** | 手绘、图片标注 |
| **Banners** | 通过 `banner:` frontmatter 设置头图 |

还需要从社区插件安装：

| 插件 | 用途 |
|------|------|
| **Dataview** | 驱动仪表盘查询 |
| **Templater** | 从模板自动填充 frontmatter |
| **Obsidian Git** | 每 15 分钟自动提交知识库 |

---

## CSS 代码片段

三个代码片段由 `setup-vault.sh` 自动启用：

| 代码片段 | 效果 |
|---------|------|
| `vault-colors` | 在文件资源管理器中为 wiki 文件夹着色 |
| `ITS-Dataview-Cards` | 将 Dataview 查询转换为可视化卡片网格 |
| `ITS-Image-Adjustments` | 精细图片尺寸控制；在嵌入后追加 `\|100` |

---

## 六种 Wiki 模式

| 模式 | 适用场景 |
|------|---------|
| **A：网站** | 站点地图、内容审计、SEO wiki |
| **B：GitHub** | 代码库地图、架构 wiki |
| **C：企业** | 项目 wiki、竞争情报 |
| **D：个人** | 第二大脑、目标、日志综合 |
| **E：研究** | 论文、概念、学位论文 |
| **F：书籍/课程** | 章节追踪器、课程笔记 |

模式可以组合使用。

---

## MCP 设置（可选）

MCP 让 Claude 无需复制粘贴即可直接读写知识库笔记。

**选项 A：REST API**

1. 在 Obsidian 中安装 **Local REST API** 插件
2. 复制你的 API 密钥
3. 运行：

```bash
claude mcp add-json obsidian-vault '{
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp-obsidian"],
  "env": {
    "OBSIDIAN_API_KEY": "your-key",
    "OBSIDIAN_HOST": "127.0.0.1",
    "OBSIDIAN_PORT": "27124",
    "NODE_TLS_REJECT_UNAUTHORIZED": "0"
  }
}' --scope user
```

**选项 B：文件系统（无需插件）**

```bash
claude mcp add-json obsidian-vault '{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@bitbonsai/mcpvault@latest", "/path/to/your/vault"]
}' --scope user
```

---

## 故障排除

| 问题 | 解决方法 |
|------|---------|
| `/wiki` 显示 "not found" | 确保 `claude-obsidian` 插件已启用：`claude plugin list` |
| 关闭 Obsidian 后图谱颜色重置 | 打开图谱视图 → 齿轮 → 颜色分组 → 重新添加一次。之后永久生效。 |
| Excalidraw 无法加载 | 运行 `bash bin/setup-vault.sh` 下载 `main.js`（8MB，不在 git 中） |
| 仪表盘没有显示结果 | 从社区插件安装 **Dataview** 插件 |
| 会话启动时热缓存未加载 | 检查 hooks：`claude hooks list`；应存在 SessionStart hook |

---

## 跨项目高级用法

让任何 Claude Code 项目指向此知识库。在该项目的 `CLAUDE.md` 中添加：

```markdown
## Wiki Knowledge Base
Path: ~/path/to/claude-obsidian

When you need context not in this project:
1. Read wiki/hot.md first (recent context cache)
2. If not enough, read wiki/index.md
3. If you need domain details, read the relevant wiki page

Do NOT read the wiki for general coding questions.
```

你的行政助理、编码项目和内容工作流都从同一个知识库中提取信息。

---

## 支持

- **GitHub（公开权威仓库）**：[github.com/AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)
- **问题反馈**：[github.com/AgriciDaniel/claude-obsidian/issues](https://github.com/AgriciDaniel/claude-obsidian/issues)
- **社区抢先体验（Pro）**：[AI Marketing Hub org](https://github.com/AI-Marketing-Hub) · [Skool 社区](https://www.skool.com/ai-marketing-hub-pro)

---

*由 [AgriciDaniel](https://github.com/AgriciDaniel) / AI Marketing Hub 构建*
*基于 Andrej Karpathy 的 LLM Wiki 模式*
