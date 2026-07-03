# WIKI.md — LLM Wiki 模式

> 如果你正在使用 claude-obsidian 插件，技能会自动处理这里的所有内容。
> 本文件是参考文档。阅读它以了解系统的工作原理。
> 基于 Andrej Karpathy 的 LLM Wiki 模式。

---

## 这是什么

你正在维护一个持久的、可复合增长的 wiki，它存在于一个 Obsidian vault 中。你不仅仅是回答问题。你构建并维护一个结构化的知识库，每添加一个来源、每提出一个问题，它都会变得更加丰富。人类负责整理来源和提出问题。你负责所有的写作、交叉引用、归档和维护。

wiki 才是产品。聊天只是界面。

与 RAG 的关键区别：wiki 是一个持久的产物。交叉引用已经存在。矛盾已被标记。综合分析已经反映了所有已读内容。知识像利息一样复合增长。

---

## 0 — 引导：首次运行设置

在任何新项目中首次运行时，按顺序执行以下步骤。跳过已完成的步骤。

### 0.1 检查 Obsidian 安装

```bash
# Linux: 先检查 flatpak，再检查 PATH
flatpak list 2>/dev/null | grep -i obsidian && echo "FOUND via flatpak" || \
which obsidian 2>/dev/null && echo "FOUND in PATH" || echo "NOT FOUND"

# macOS
ls /Applications/Obsidian.app 2>/dev/null && echo "FOUND" || echo "NOT FOUND"

# Windows (PowerShell)
Test-Path "$env:LOCALAPPDATA\Obsidian" && echo "FOUND" || echo "NOT FOUND"
```

如果未安装：

```bash
# Linux (Flatpak)
flatpak install flathub md.obsidian.Obsidian

# macOS (Homebrew)
brew install --cask obsidian

# Windows (winget)
winget install Obsidian.Obsidian

# 所有平台: https://obsidian.md/download
```

安装后：Obsidian > 管理 Vault > 打开文件夹作为 Vault > 选择 vault 目录。

如果没有可用的包管理器，告诉用户："从 https://obsidian.md 下载 Obsidian —— 安装它，创建一个 vault，然后告诉我路径。"

### 0.2 Vault 位置

询问 vault 路径或使用默认值：

```
VAULT_PATH=~/Documents/Obsidian Vault
```

验证：`ls "$VAULT_PATH/.obsidian" 2>/dev/null`

### 0.3 安装 Local REST API 插件

引导用户（你无法以编程方式完成此操作）：

1. Obsidian > 设置 > 社区插件 > 关闭受限模式
2. 浏览 > 搜索 "Local REST API" > 安装 > 启用
3. 设置 > Local REST API > 复制 API 密钥
4. 插件运行在 `https://127.0.0.1:27124`（自签名证书）

测试：`curl -sk -H "Authorization: Bearer <KEY>" https://127.0.0.1:27124/`

### 0.4 配置 MCP 服务器

**选项 A：mcp-obsidian（基于 REST API，最流行）**

```bash
claude mcp add-json obsidian-vault '{
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp-obsidian"],
  "env": {
    "OBSIDIAN_API_KEY": "<KEY>",
    "OBSIDIAN_HOST": "127.0.0.1",
    "OBSIDIAN_PORT": "27124",
    "NODE_TLS_REJECT_UNAUTHORIZED": "0"
  }
}' --scope user
```

**选项 B：MCPVault（基于文件系统，无需插件）**

```bash
claude mcp add-json obsidian-vault '{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@bitbonsai/mcpvault@latest", "<VAULT_PATH>"]
}' --scope user
```

**选项 C：通过 curl 直接调用 REST API** —— 始终有效，无需 MCP。参见第 11 节。

使用 `--scope user` 以便 vault 在所有项目中可用。

**验证：**

```bash
claude mcp list               # 确认服务器出现
claude mcp get obsidian-vault # 确认路径正确
```

在 Claude Code 会话中，输入 `/mcp` 检查连接状态。

### 0.5 推荐插件

通过 设置 > 社区插件 > 浏览 安装：

| 插件 | 用途 |
|------|------|
| **Dataview** | 将 vault 作为数据库查询。驱动仪表板。 |
| **Templater** | 在创建笔记时自动填充 frontmatter。 |
| **Obsidian Git** | 每 15 分钟自动提交。防止数据丢失。 |
| **Iconize** | 可视化文件夹图标。 |
| **Minimal Theme** | 最适合密集信息展示的深色主题。 |

可选：Smart Connections（语义搜索）、QuickAdd（宏）、Folder Notes（可点击文件夹）。

还请安装 **Obsidian Web Clipper** 浏览器扩展。它可以将网页文章转换为 markdown 并一键发送到 `.raw/`。适用于 Chrome、Firefox 和 Safari。

---

## 1 — 架构

```
vault/
├── .raw/                   # 第 1 层：不可变的源文档
│   ├── articles/
│   ├── transcripts/
│   ├── screenshots/
│   ├── data/
│   └── assets/
│
├── wiki/                   # 第 2 层：LLM 生成的知识库
│   ├── index.md            # 所有 wiki 页面的主目录
│   ├── log.md              # 所有操作的时间顺序记录
│   ├── hot.md              # 热缓存：最近上下文摘要（约 500 词）
│   ├── overview.md         # 整个 wiki 的执行摘要
│   ├── sources/            # 每个原始来源一个摘要页面
│   ├── entities/           # 人物、组织、产品、仓库
│   │   └── _index.md
│   ├── concepts/           # 想法、模式、框架
│   │   └── _index.md
│   ├── domains/            # 顶层主题领域
│   │   └── _index.md
│   ├── comparisons/        # 并排分析
│   ├── questions/          # 已归档的用户查询答案
│   └── meta/               # 仪表板、lint 报告、约定
│
├── _templates/             # Templater 模板
├── _attachments/           # wiki 页面引用的图片和 PDF
│
├── WIKI.md                 # 第 3 层：本文件
└── .obsidian/              # Obsidian 配置（自动管理）
```

### 规则

- `.raw/` 是只读的。永远不要修改源文件。
- `wiki/` 是你的。自由创建、更新、重命名、删除。
- 每个 wiki 页面都有 frontmatter。没有例外。
- Wikilinks 优于路径。使用 `[[Page Name]]` 而不是 `[text](path/to/file.md)`。
- 原子笔记。每个页面一个概念。如果涉及两件事，请拆分它。
- 更新，不要重复。如果页面已存在，请更新它。

---

## 2 — 热缓存

`wiki/hot.md` 是最近上下文的约 500 词摘要。它的存在使得其他指向此 vault 的项目无需爬取整个 wiki 即可获取最近上下文。

在每次摄入后、任何重要的查询交换后以及每次会话结束时更新 hot.md。

格式：

```markdown
---
type: meta
title: "Hot Cache"
updated: 2026-04-07T14:30:00
---

# 最近上下文

## 最后更新
2026-04-07 — 摄入了 3 个新的 YouTube 转录稿

## 关键近期要点
- [最重要的近期收获]
- [第二重要的]

## 近期变更
- 创建：[[New Page 1]], [[New Page 2]]
- 更新：[[Existing Page]]（添加了关于 X 的部分）
- 标记：[[Page A]] 和 [[Page B]] 在主题 Y 上存在矛盾

## 活跃线程
- 用户正在研究 [主题]
- 开放问题：[仍在调查的事情]
```

保持在 500 词以内。它是缓存，不是日志。每次完全覆盖。

---

## 3 — Frontmatter 模式

每个 wiki 页面都以扁平 YAML frontmatter 开头。没有嵌套对象。Obsidian 的属性界面不支持它们。

### 通用字段（每个页面）：

```yaml
---
type: <source|entity|concept|domain|comparison|question|overview|meta>
title: "人类可读标题"
created: 2026-04-07
updated: 2026-04-07
tags:
  - <domain-tag>
  - <type-tag>
status: <seed|developing|mature|evergreen>
related:
  - "[[Other Page]]"
sources:
  - "[[.raw/articles/source-file.md]]"
---
```

### 类型特定附加字段：

**source**：`source_type`、`author`、`date_published`、`url`、`confidence`（high|medium|low）、`key_claims`（列表）

**entity**：`entity_type`（person|organization|product|repository|place）、`role`、`first_mentioned`

**concept**：`complexity`（basic|intermediate|advanced）、`domain`、`aliases`（列表）

**comparison**：`subjects`（wikilinks 列表）、`dimensions`（列表）、`verdict`（一行）

**question**：`question`（原始查询）、`answer_quality`（draft|solid|definitive）

---

## 4 — 操作

### 4.1 SCAFFOLD — 首次运行结构

触发条件：用户描述 vault 的用途。

1. 确定 wiki 模式（参见下方模式表和第 4.1a 节中的完整模式详情）。
2. 问一个问题："这个 vault 是做什么用的？"
3. 在 `wiki/` 下创建完整文件夹结构。
4. 为每个领域创建领域页面 + `_index.md` 子索引。
5. 创建 `wiki/overview.md`、`wiki/index.md`、`wiki/log.md`、`wiki/hot.md`。
6. 创建 `_templates/` 并为每种笔记类型准备模板。
7. 应用视觉自定义（第 7 节）。创建 `.obsidian/snippets/vault-colors.css`。
8. 创建 vault CLAUDE.md（模板见第 4.1b 节）。
9. 初始化 git（第 8 节）。
10. 展示结构并询问："在我们开始之前想调整什么吗？"

**模式选择：**

| 用户说 | 最佳模式 |
|--------|----------|
| "我的网站"、"站点地图"、"内容审计" | A：网站 |
| "我的仓库"、"代码库地图"、"架构 wiki" | B：GitHub |
| "我的业务"、"项目 wiki"、"竞争情报" | C：业务 |
| "第二大脑"、"目标"、"日记"、"我的生活" | D：个人 |
| "研究主题"、"论文"、"深入研究" | E：研究 |
| "我正在读的书"、"课程笔记"、"章节追踪" | F：书籍/课程 |

你可以组合模式。"GitHub 仓库 + 对 AI 方法的研究"使用模式 B 文件夹加上模式 E 的 papers/ 文件夹。

### 4.1a — 六种 Wiki 模式

**模式 A：网站 / 站点地图**

```
vault/
├── .raw/              # 爬虫导出、分析数据、GSC 数据
├── wiki/
│   ├── pages/         # 每个 URL 一个笔记
│   ├── structure/     # 站点架构、导航层级
│   ├── audits/        # 内容缺口、重定向需求
│   ├── keywords/      # 关键词集群、目标页面分配
│   └── entities/      # 品牌、作者、主题中心
```

pages/ 的 frontmatter：`url`、`status`（live|redirect|404|stub|no-index）、`h1`、`meta_description`、`word_count`、`has_schema`、`indexed`、`canonical`、`internal_links_in`、`internal_links_out`、`last_crawled`

关键页面：`[[Site Overview]]`、`[[Navigation Structure]]`、`[[Content Gaps]]`、`[[Redirect Map]]`、`[[Keyword Clusters]]`

---

**模式 B：GitHub / 仓库**

```
vault/
├── .raw/              # README、git 日志导出、代码转储
├── wiki/
│   ├── modules/       # 每个模块/包/服务一个笔记
│   ├── components/    # 可复用组件
│   ├── decisions/     # 架构决策记录
│   ├── dependencies/  # 外部依赖、版本、风险
│   └── flows/         # 数据流、请求路径、认证流程
```

modules/ 的 frontmatter：`path`、`status`（active|deprecated|experimental|planned）、`language`、`purpose`、`maintainer`、`depends_on`、`used_by`、`linked_issues`

关键页面：`[[Architecture Overview]]`、`[[Data Flow]]`、`[[Tech Stack]]`、`[[Dependency Graph]]`、`[[Key Decisions]]`

---

**模式 C：业务 / 项目**

```
vault/
├── .raw/              # 会议转录稿、Slack 导出、文档
├── wiki/
│   ├── stakeholders/  # 人物、公司、决策者
│   ├── decisions/     # 带有理由和日期的关键决策
│   ├── deliverables/  # 里程碑、产出、状态
│   ├── intel/         # 竞争对手分析、市场研究
│   └── comms/         # 综合会议笔记
```

decisions/ 的 frontmatter：`status`（active|pending|done|blocked|superseded）、`priority`（1-5）、`date`、`owner`、`due_date`、`context`

关键页面：`[[Project Overview]]`、`[[Stakeholder Map]]`、`[[Decision Log]]`、`[[Competitor Landscape]]`

---

**模式 D：个人 / 第二大脑**

```
vault/
├── .raw/              # 日记条目、文章、语音转录稿
├── wiki/
│   ├── goals/         # 个人和职业目标
│   ├── learning/      # 正在掌握的概念
│   ├── people/        # 人际关系、共享上下文
│   ├── areas/         # 生活领域：健康、财务、职业
│   └── resources/     # 书籍、课程、工具
├── _meta/
│   └── hot-cache.md   # 约 500 词的活跃上下文
```

goals/ 的 frontmatter：`area`（health|career|finance|creative|relationships|growth）、`priority`、`target_date`、`progress`（0-100）

关键页面：`[[North Star]]`、`[[Weekly Review Template]]`、`[[Annual Goals]]`

---

**模式 E：研究**

```
vault/
├── .raw/              # PDF、网页剪藏、原始笔记
├── wiki/
│   ├── papers/        # 论文摘要及关键主张
│   ├── concepts/      # 提取的概念、模型、框架
│   ├── entities/      # 人物、组织、数据集
│   ├── thesis/        # 不断演进的综合分析
│   └── gaps/          # 开放问题、矛盾
```

papers/ 的 frontmatter：`year`、`authors`、`venue`、`key_claim`、`methodology`、`contradicts`、`supports`

关键页面：`[[Research Overview]]`、`[[Key Claims Map]]`、`[[Open Questions]]`、`[[Methodology Comparison]]`

---

**模式 F：书籍 / 课程**

```
vault/
├── .raw/              # 章节笔记、高亮、练习
├── wiki/
│   ├── characters/    # 角色、人物、专家
│   ├── themes/        # 主要主题及证据
│   ├── concepts/      # 领域特定术语
│   ├── timeline/      # 结构、顺序、章节地图
│   └── synthesis/     # 你自己的收获和应用
```

concepts/ 的 frontmatter：`source_chapters`、`first_appearance`

关键页面：`[[Book Overview]]`、`[[Theme Map]]`、`[[Character / Expert Index]]`、`[[My Takeaways]]`

### 4.1b — Vault CLAUDE.md 模板

在搭建新项目 vault 时在 vault 根目录创建此文件：

```markdown
# [WIKI NAME] — LLM Wiki

模式: [MODE A/B/C/D/E/F]
用途: [一句话]
所有者: [NAME]
创建日期: YYYY-MM-DD

## 结构

[粘贴所选模式的文件夹地图]

## 约定

- 所有笔记使用 YAML frontmatter：type、status、created、updated、tags（最低要求）
- Wikilinks 使用 [[Note Name]] 格式 —— 文件名唯一，无需路径
- .raw/ 包含源文档 —— 永远不要修改它们
- wiki/index.md 是主目录 —— 每次摄入时更新
- wiki/log.md 是仅追加的 —— 新条目放在顶部，永远不要编辑过去的条目

## 操作

- 摄入：将来源放入 .raw/，说 "ingest [filename]"
- 查询：提出任何问题 —— Claude 先读索引，然后深入
- Lint：说 "lint the wiki" 运行健康检查
```

### 4.2 INGEST — 单个来源

触发条件：用户将文件放入 `.raw/` 或粘贴内容。

1. 完整阅读来源。
2. 与用户讨论关键要点。如果用户说 "just ingest it" 则跳过。
3. 在 `wiki/sources/` 中创建来源摘要。
4. 为提到的每个人物/组织/产品/仓库创建或更新实体页面。
5. 为重要想法创建或更新概念页面。
6. 更新相关领域页面及其 `_index.md` 子索引。
7. 如果整体情况发生变化，更新 `wiki/overview.md`。
8. 更新 `wiki/index.md`。为所有新页面添加条目。
9. 用本次摄入的上下文更新 `wiki/hot.md`。
10. 追加到 `wiki/log.md`（新条目放在顶部）：
    ```markdown
    ## [2026-04-07] ingest | Source Title
    - 来源: `.raw/articles/filename.md`
    - 摘要: [[Source Title]]
    - 创建的页面: [[Page 1]], [[Page 2]]
    - 更新的页面: [[Page 3]], [[Page 4]]
    - 关键洞察：关于新内容的一句话总结。
    ```
11. 检查矛盾。在两个页面上用 `> [!contradiction]` 标注框标记。

单个来源通常涉及 8-15 个 wiki 页面。

### 4.3 INGEST — 批量模式

触发条件：用户放入多个文件或说 "ingest all of these"。

1. 列出所有要处理的文件。与用户确认。
2. 按照单个摄入流程处理每个来源。推迟交叉引用。
3. 所有来源处理完后：进行交叉引用。寻找新来源之间的联系。
4. 最后一次性更新索引、热缓存和日志，而不是每个来源都更新。
5. 报告："处理了 N 个来源。创建了 X 个页面，更新了 Y 个页面。关键联系：..."

批量摄入交互性较低。对于 30 个以上的来源，每 10 个检查一次。

### 4.4 QUERY — 回答问题

1. 先读 `wiki/hot.md`。它可能已有答案。
2. 读 `wiki/index.md` 找到相关页面。
3. 读这些页面（通常 3-5 个，10 个以上太多了）。
4. 在聊天中综合答案。用 wikilinks 引用。
5. 提议将答案归档为 `wiki/questions/` 中的 wiki 页面。
6. 如果问题揭示了缺口："我对 X 了解不够。想找一个来源吗？"

### 4.5 LINT — 健康检查

触发条件：用户说 "lint" 或每 10-20 次摄入。

检查：孤立页面、死链接、过时的主张、提到的概念缺少页面、缺少交叉引用、frontmatter 缺口、空章节。

输出：`wiki/meta/lint-report-YYYY-MM-DD.md`。自动修复前先询问。

---

## 5 — 索引和子索引

### wiki/index.md（主索引）

```markdown
---
type: meta
title: "Wiki Index"
updated: 2026-04-07
---
# Wiki 索引

## 领域
- [[Domain Name]] — 描述（N 个来源）

## 实体
- [[Entity Name]] — 角色（首次出现：[[Source]]）

## 概念
- [[Concept Name]] — 定义（状态：developing）

## 来源
- [[Source Title]] — 作者、日期、类型

## 问题
- [[Question Title]] — 答案摘要
```

### 领域子索引

每个领域文件夹都有一个 `_index.md`，其中包含该领域页面的目录。

```markdown
---
type: meta
title: "Entities Index"
updated: 2026-04-07
---
# 实体

## 人物
- [[Person Name]] — 角色、组织

## 组织
- [[Org Name]] — 他们做什么
```

### wiki/log.md

仅追加。新条目放在顶部。每个条目：`## [YYYY-MM-DD] operation | title`

解析最近条目：
```bash
grep "^## \[" wiki/log.md | head -10
```

---

## 6 — 跨项目引用

任何 Claude Code 项目都可以读取你的 wiki 而无需复制上下文。

在另一个项目的 CLAUDE.md 中添加：

```markdown
## Wiki 知识库
路径: ~/Documents/Obsidian Vault

当你需要此项目中尚未包含的上下文时：
1. 先读 wiki/hot.md（最近上下文，约 500 词）
2. 如果不够，读 wiki/index.md（完整目录）
3. 如果需要领域特定内容，读 wiki/<domain>/_index.md
4. 只有这样才读单个 wiki 页面

不要为一般性编码问题、已在此项目上下文中的内容或与 [你的领域] 无关的任务读取 wiki。
```

这可以保持低 token 使用量。热缓存约 500 tokens。索引约 1000 tokens。单个页面每个 100-300 tokens。

---

## 7 — 视觉自定义

在搭建时应用。创建 `.obsidian/snippets/vault-colors.css`：

```css
:root {
  --wiki-1: #4fc1ff;  --wiki-2: #c586c0;  --wiki-3: #dcdcaa;
  --wiki-4: #ce9178;  --wiki-5: #6a9955;  --wiki-6: #d16969;
  --wiki-7: #569cd6;
}

.nav-folder-title[data-path^="wiki/domains"]     { color: var(--wiki-1); }
.nav-folder-title[data-path^="wiki/entities"]    { color: var(--wiki-2); }
.nav-folder-title[data-path^="wiki/concepts"]    { color: var(--wiki-3); }
.nav-folder-title[data-path^="wiki/sources"]     { color: var(--wiki-4); }
.nav-folder-title[data-path^="wiki/questions"]   { color: var(--wiki-5); }
.nav-folder-title[data-path^="wiki/comparisons"] { color: var(--wiki-6); }
.nav-folder-title[data-path^="wiki/meta"]        { color: var(--wiki-7); }
.nav-folder-title[data-path=".raw"]              { color: #808080; opacity: 0.6; }

.callout[data-callout='contradiction'] { --callout-color: 209, 105, 105; --callout-icon: lucide-alert-triangle; }
.callout[data-callout='gap']           { --callout-color: 220, 220, 170; --callout-icon: lucide-help-circle; }
.callout[data-callout='key-insight']   { --callout-color: 79, 193, 255;  --callout-icon: lucide-lightbulb; }
.callout[data-callout='stale']         { --callout-color: 128, 128, 128; --callout-icon: lucide-clock; }
```

启用：设置 > 外观 > CSS 代码片段 > 刷新 > 开启。

### 图谱视图分组

在图谱视图设置中设置：

| 查询 | 颜色 |
|------|------|
| `path:wiki/domains` | 蓝色 |
| `path:wiki/entities` | 紫色 |
| `path:wiki/concepts` | 黄色 |
| `path:wiki/sources` | 橙色 |
| `path:wiki/questions` | 绿色 |
| `path:.raw` | 灰色（暗淡） |

---

## 8 — Git 设置

```bash
cd "$VAULT_PATH"
git init
cat > .gitignore << 'EOF'
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.smart-connections/
.obsidian-git-data
.trash/
.DS_Store
node_modules/
EOF
git add -A && git commit -m "Initial vault scaffold"
```

启用 Obsidian Git：设置 > Obsidian Git > 自动备份间隔 > 15 分钟。

---

## 9 — Dataview 仪表板

在搭建后创建 `wiki/meta/dashboard.md`：

````markdown
---
type: meta
title: "Dashboard"
---
# Wiki 仪表板

## 最近活动
```dataview
TABLE type, status, updated FROM "wiki" SORT updated DESC LIMIT 15
```

## 种子页面（需要开发）
```dataview
LIST FROM "wiki" WHERE status = "seed" SORT updated ASC
```

## 缺少来源的实体
```dataview
LIST FROM "wiki/entities" WHERE !sources OR length(sources) = 0
```
````

---

## 10 — 上下文窗口管理

只读取最少需要的内容：

- 先读 `hot.md`。它可能已有你需要的内容。
- 再读 `index.md`。找到相关页面，不要扫描所有内容。
- 读领域子索引进行有针对性的查找。
- 每次查询只读 3-5 个页面。10 个以上太多了。
- 使用搜索进行关键词查找。不要扫描整个页面来找一个词。
- 使用 PATCH 进行精确编辑。永远不要为了改一个字段而重新读取和重写整个文件。
- 保持 wiki 页面简短。最多 100-300 行。拆分长页面。
- 除非用户要求，否则不要将 wiki 内容粘贴到聊天中。通过 wikilink 引用。

---

## 11 — REST API 快速参考

在运行任何命令之前设置这些：

```bash
API="https://127.0.0.1:27124"
KEY="your-api-key-here"
```

**读取文件：**
```bash
curl -sk -H "Authorization: Bearer $KEY" "$API/vault/wiki/index.md"
```

**创建或替换文件：**
```bash
curl -sk -X PUT \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: text/markdown" \
  --data-binary @file.md \
  "$API/vault/wiki/entities/Name.md"
```

**追加到文件：**
```bash
curl -sk -X POST \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: text/markdown" \
  --data "- New item" \
  "$API/vault/wiki/log.md"
```

**修补 frontmatter 字段：**
```bash
curl -sk -X PATCH \
  -H "Authorization: Bearer $KEY" \
  -H "Operation: replace" -H "Target-Type: frontmatter" \
  -H "Target: status" -H "Content-Type: application/json" \
  --data '"mature"' \
  "$API/vault/wiki/concepts/Name.md"
```

**在标题下追加：**
```bash
curl -sk -X PATCH \
  -H "Authorization: Bearer $KEY" \
  -H "Operation: append" -H "Target-Type: heading" \
  -H "Target: Connections" -H "Content-Type: text/markdown" \
  --data "- [[New Page]]" \
  "$API/vault/wiki/entities/Name.md"
```

**搜索：**
```bash
curl -sk -X POST \
  -H "Authorization: Bearer $KEY" \
  "$API/search/simple/?query=machine+learning"
```

**Dataview 查询：**
```bash
curl -sk -X POST \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/vnd.olrapi.dataview.dql+txt" \
  --data 'TABLE status FROM "wiki" WHERE status = "seed"' \
  "$API/search/"
```

---

## 12 — Vault CLAUDE.md 模板

为新项目创建 wiki 时（不是此插件），在 vault 根目录创建 CLAUDE.md：

```markdown
# [WIKI NAME] — LLM Wiki

模式: [MODE A/B/C/D/E/F]
用途: [一句话]
所有者: [NAME]
创建日期: YYYY-MM-DD

## 结构

[粘贴所选模式的文件夹地图]

## 约定

- 所有笔记使用 YAML frontmatter：type、status、created、updated、tags（最低要求）
- Wikilinks 使用 [[Note Name]] 格式
- .raw/ 包含源文档 —— 永远不要修改它们
- wiki/index.md 是主目录 —— 每次摄入时更新
- wiki/log.md 是仅追加的 —— 新条目放在顶部

## 操作

- 摄入：将来源放入 .raw/，说 "ingest [filename]"
- 查询：提出任何问题
- Lint：说 "lint the wiki"
```

---

## 13 — 约定

### 命名

- **文件名**：标题大小加空格（`Machine Learning.md`）
- **文件夹**：小写加连字符（`wiki/data-models/`）
- **标签**：小写，层级式（`#domain/architecture`）
- **唯一文件名**，这样 wikilinks 无需路径即可工作

### 写作风格

- 陈述式，现在时。"X uses Y" 而不是 "X basically does Y."
- 大量链接。每次提到 wiki 页面都使用 wikilink。
- 引用来源：`(Source: [[Page]])`。
- 标记不确定性：`> [!gap] 这需要更多证据。`
- 标记矛盾：`> [!contradiction] [[Page A]] 声称 X，但 [[Page B]] 说 Y。`

### 交叉引用

更新 Page A 以提到 Page B 时，检查 Page B 是否应该链接回来。双向链接使图谱视图更有用。

---

## 14 — Canvas 地图

创建 `.canvas` 文件用于可视化概览：

```json
{
  "nodes": [
    {"id": "1", "type": "file", "file": "wiki/domains/Architecture.md",
     "x": 0, "y": 0, "width": 250, "height": 120, "color": "4"},
    {"id": "2", "type": "file", "file": "wiki/domains/APIs.md",
     "x": 300, "y": 0, "width": 250, "height": 120, "color": "5"}
  ],
  "edges": [
    {"id": "e1", "fromNode": "1", "fromSide": "right",
     "toNode": "2", "toSide": "left", "toEnd": "arrow"}
  ]
}
```

Canvas 节点颜色（Obsidian canvas 颜色代码）：1=红色，2=橙色，3=黄色，4=绿色，5=青色，6=紫色。
注意：这些与 wiki 图谱 CSS 颜色方案不同。完整的 canvas 颜色表参见全局插件中的 `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/canvas/references/canvas-spec.md`。

在搭建时创建领域关系 canvas。随着 wiki 的增长更新。

---

## 总结

作为 LLM，你的工作：
1. 设置 vault（一次性）
2. 根据用户的领域描述搭建 wiki 结构
3. 摄入来源：阅读、总结、交叉引用、归档
4. 每次操作后维护热缓存
5. 使用索引 > 相关页面 > 综合来回答问题
6. 将好的答案归档回 wiki
7. 定期 lint：发现并修复健康问题
8. 永远不要修改 .raw/ 来源
9. 始终更新索引、子索引、日志和热缓存
10. 始终使用 frontmatter 和 wikilinks

人类的工作：整理来源、提出好问题、思考其意义。其他一切都是你的。

---

*基于 Andrej Karpathy 的 LLM Wiki 模式。插件：claude-obsidian，由 AgriciDaniel / AI Marketing Hub 开发。*
