# claude-obsidian 

个人的obsidian-wiki
> Claude + Obsidian 自组织 AI 第二大脑。基于 [Andrej Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

---

## 环境要求

| 组件 | 版本 | 下载地址 |
|------|------|---------|
| Obsidian | v1.9.10+ | https://obsidian.md |
| Claude Code | 最新版 | https://claude.ai/claude-code |
| Git | 任意 | https://git-scm.com |

---

## 搭建步骤

### 第一步：创建 Obsidian 专属知识库

1. 安装并打开 Obsidian
2. 点击 **创建新库**，自定义名称，选个位置存放

> ⚠️ **必须单独建一个干净的库**，不要混进已有的笔记库或建成子文件夹，否则 AI 会读错地方。

---

### 第二步：安装 Obsidian 插件，获取连接密钥

1. Obsidian → 左下角 **设置** → **第三方插件** → **关闭安全模式**
2. 点击 **社区插件市场 → 浏览**，搜索 **`Local REST API`**，安装并启用
3. 进入插件设置，复制 **API Key**（只复制 `Bearer` 后面那串，不要带 "Bearer"）

> ⚠️ Key 是每个库独立的，复制前确认当前打开的是 `Second-Brain` 库。

---

### 第三步：在 Claude Code 中建立连接

在终端中粘贴以下命令，**替换 `你的API密钥`**：

```bash
claude mcp add-json obsidian-vault '{
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp-obsidian"],
  "env": {
    "OBSIDIAN_API_KEY": "你的API密钥",
    "OBSIDIAN_HOST": "127.0.0.1",
    "OBSIDIAN_PORT": "27124",
    "NODE_TLS_REJECT_UNAUTHORIZED": "0"
  }
}' --scope user
```

**验证连接：** 在 Claude 中说：

```
列出当前库的文件列表，然后写入一个测试文件，内容为 3.1415926
```

回 Obsidian 看到测试文件且目录正确，即连接成功。

---

### 第四步：安装 claude-obsidian 技能包

**方式一（推荐）：命令行安装**

```bash
claude plugin marketplace add AgriciDaniel/claude-obsidian
claude plugin install claude-obsidian@agricidaniel-claude-obsidian
```

**方式二：对话安装**

在 Claude Code 终端中发送：

```
请在当前 Claude Code 环境中，为我安装并配置 claude-obsidian
这个插件，安装完要保证在 Claude Code 中能正常使用。
项目地址：https://github.com/AgriciDaniel/claude-obsidian
```

验证：在 Claude Code 中输入 `/wiki`，能看到帮助信息即表示安装成功。

---

### 第五步：初始化知识库

在 Claude Code 终端中输入：

```
/wiki
```

或者直接说：

```
帮我初始化第二大脑 wiki
```

Claude 会问你：**"这个知识库是拿来干嘛的？"**，你的回答决定知识库骨架。参考：

```
长期个人第二大脑，沉淀我研究的主题，包括但不限于经验沉淀、
网页文章、文档资料、和 AI 的历史对话记录等，供我构建个人知识库，
以及和 AI 日常对话调用。
```

Claude 会自动搭建好完整的知识库结构。

---

## 核心概念

```
  你投放资料          AI 读取并整理           你提问
     │                    │                    │
     ▼                    ▼                    ▼
  .raw/ 目录    →    AI 提取实体/概念    →   AI 从 wiki 中
  (原始文件)         建立交叉引用              检索并综合回答
                       更新索引                 引用具体页面
                       更新热缓存
```

**三个关键目录：**
- `.raw/` — 放入原始资料（PDF、文章、网页等），AI 读取但不修改
- `wiki/` — AI 生成的知识库（实体、概念、来源、元数据）
- `_templates/` — Obsidian 模板，用于自动填充笔记格式

**三个核心文件：**
- `wiki/index.md` — 主目录，所有知识页面的索引
- `wiki/hot.md` — 热缓存，最近的上下文摘要（跨会话记忆）
- `wiki/log.md` — 操作日志，记录每次 ingest 和变更

---

## 常用命令速查

### 日常使用（最常用）

| 你说 | Claude 做什么 |
|------|-------------|
| `ingest 文件名` | 读取资料，创建 8-15 个 wiki 页面，更新索引 |
| `ingest all of these` | 批量处理多个资料，然后交叉引用 |
| `关于 X 你知道什么？` | 从 wiki 中检索，综合回答并引用来源 |
| `/save` | 将当前对话保存为 wiki 笔记 |
| `/save 我的笔记名` | 用指定名称保存 |

### 研究与分析

| 你说 | Claude 做什么 |
|------|-------------|
| `/autoresearch 主题` | 自主研究循环：搜索→获取→综合→归档（3轮） |
| `/think 问题描述` | 10 原则深度思考框架，用于复杂决策 |
| `lint the wiki` | 健康检查：孤儿页、死链接、缺失引用 |
| `update hot cache` | 刷新热缓存，保存最新上下文 |

### 可视化

| 你说 | Claude 做什么 |
|------|-------------|
| `/canvas` | 打开或创建可视化画布 |
| `/canvas add image 路径` | 添加图片到画布 |
| `/canvas add note 页面名` | 将 wiki 页面钉到画布上 |
| `/canvas zone 区域名` | 创建分组区域 |

---

## 知识库结构说明

```
D:\AI\Hermes\claude-obsidian\
├── .raw/                    ← 放入原始资料（AI 读取，不修改）
├── wiki/                    ← AI 生成的知识库
│   ├── index.md             ← 主目录索引
│   ├── hot.md               ← 热缓存（最近上下文）
│   ├── log.md               ← 操作日志
│   ├── overview.md          ← 概览摘要
│   ├── concepts/            ← 概念页面
│   ├── entities/            ← 实体页面（人物、组织、工具）
│   ├── sources/             ← 来源页面（你导入的资料）
│   ├── questions/           ← 问答页面
│   ├── references/          ← 参考资料
│   ├── meta/                ← 元数据和仪表盘
│   │   ├── dashboard.base   ← Obsidian Bases 仪表盘
│   │   └── dashboard.md     ← Dataview 仪表盘（备用）
│   └── canvases/            ← 可视化画布
├── _templates/              ← Obsidian 模板
├── scripts/                 ← 辅助脚本（锁、检索、传输）
├── docs/                    ← 文档和审计记录
├── .obsidian/               ← Obsidian 配置和插件
├── CLAUDE.md                ← Claude Code 项目指令
└── README.md                ← 本文件
```

---

## 知识组织方法（4种模式）

首次运行 `/wiki` 时，Claude 会让你选择组织方法。可以用 `bash bin/setup-mode.sh` 切换。

| 模式 | 理念 | 适合场景 |
|------|------|---------|
| **Generic**（默认） | 不强制规则，v1.7 原始行为 | 通用知识库 |
| **LYT**（Linking Your Thinking） | 笔记靠链接连接，不靠文件夹 | 个人知识管理、创意工作 |
| **PARA**（Tiago Forte） | 按可操作性组织（项目/领域/资源/归档） | 项目管理、商业分析 |
| **Zettelkasten**（Luhmann 卡片盒） | 原子笔记、时间戳 ID、密集双向链接 | 学术研究、深度学习 |

> 💡 切换模式不会自动迁移已有文件。建议在项目初期就选定。

---

## 使用场景

| 场景 | 说明 |
|------|------|
| **A: 网站** | 站点地图、内容审计、SEO 知识库 |
| **B: GitHub** | 代码库地图、架构文档 |
| **C: 商业** | 项目 wiki、竞品分析 |
| **D: 个人** | 第二大脑、目标管理、日记综合 |
| **E: 研究** | 论文、概念、课题追踪 |
| **F: 书籍/课程** | 章节追踪、课程笔记 |

场景可以组合使用，例如「商业 + 研究」配合 PARA 模式。

---

## MCP 配置（可选）

MCP 让 Claude 直接读写 Obsidian 笔记，无需复制粘贴。

### 方式 A：基于 REST API（需要 Obsidian 插件）

1. 在 Obsidian 中安装「Local REST API」插件
2. 复制 API Key
3. 运行：
```bash
claude mcp add-json obsidian-vault '{
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp-obsidian"],
  "env": {
    "OBSIDIAN_API_KEY": "你的API密钥",
    "OBSIDIAN_HOST": "127.0.0.1",
    "OBSIDIAN_PORT": "27124",
    "NODE_TLS_REJECT_UNAUTHORIZED": "0"
  }
}' --scope user
```

### 方式 B：基于文件系统（无需额外插件）

```bash
claude mcp add-json obsidian-vault '{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@bitbonsai/mcpvault@latest", "D:/AI/Hermes/claude-obsidian"]
}' --scope user
```

---

## Obsidian 插件说明

### 已预装（开箱即用）

| 插件 | 功能 |
|------|------|
| **Calendar** | 右侧栏日历，显示字数统计和任务标记 |
| **Thino** | 快速备忘录面板 |
| **Excalidraw** | 手绘白板，可标注图片 |
| **Banners** | Notion 风格的笔记头部横幅图片 |

### 建议额外安装（在 Obsidian 设置 → 社区插件中搜索）

| 插件 | 功能 |
|------|------|
| **Templater** | 自动从 `_templates/` 填充笔记模板 |
| **Obsidian Git** | 每 15 分钟自动提交 vault 备份 |
| **Dataview**（可选） | 仅在使用旧版仪表盘时需要 |

### Obsidian Web Clipper

安装浏览器扩展 [Obsidian Web Clipper](https://obsidian.md/clipper)，一键将网页保存到 `.raw/` 目录。

---

## 跨项目引用知识库

在其他 Claude Code 项目的 `CLAUDE.md` 中添加：

```markdown
## Wiki 知识库
路径: D:/AI/Hermes/claude-obsidian

当需要本项目之外的上下文时：
1. 先读 wiki/hot.md（最近上下文缓存）
2. 不够的话读 wiki/index.md
3. 需要领域细节时读对应的子索引
4. 最后才读具体的 wiki 页面

对于与当前领域无关的通用编码问题，不要读取 wiki。
```

这样你的所有项目都能共享同一个知识库。

---

## FAQ

**会把笔记发到 Anthropic 吗？** 不会。所有处理默认在本地完成。

**多设备同步？** 配合 Obsidian Sync、Obsidian Git 或 Syncthing 等工具即可。

**能用其他 AI 工具吗？** 实验性支持 Cursor、Windsurf、Gemini CLI，目前仅在 Claude Code 上验证。

**Excalidraw 插件下载失败怎么办？** 手动下载 `main.js`：
```bash
curl -L "https://github.com/zsviczian/obsidian-excalidraw-plugin/releases/latest/download/main.js" \
  -o .obsidian/plugins/obsidian-excalidraw-plugin/main.js
```
如果 GitHub 被墙，使用镜像：
```bash
curl -L "https://ghfast.top/https://github.com/zsviczian/obsidian-excalidraw-plugin/releases/latest/download/main.js" \
  -o .obsidian/plugins/obsidian-excalidraw-plugin/main.js
```

**图谱视图颜色重置了怎么办？** 打开 Obsidian 图谱设置 → 颜色分组 → 重新添加一次即可永久保留。

**如何切换知识组织模式？**
```bash
bash bin/setup-mode.sh
```
选择新模式后，新创建的页面会按新模式组织，已有文件不迁移。

**多人同时写入会冲突吗？** 不会。v1.7+ 使用 per-file advisory lock（`scripts/wiki-lock.sh`），并行写入时自动排队，不会损坏文件。

**如何启动自主研究？** 在 Claude Code 中输入：
```
/autoresearch 你想研究的主题
```
AI 会自动进行 3 轮搜索、获取、综合、归档，最终生成完整的研究 wiki。

**wiki 内容太多了怎么办？** 运行健康检查：
```
lint the wiki
```
Claude 会找出孤儿页面、死链接、缺失引用和过时内容。

---

## 卸载

```bash
# 插件方式
claude plugin uninstall claude-obsidian@agricidaniel-claude-obsidian
claude plugin marketplace remove AgriciDaniel/claude-obsidian

# 克隆方式：直接删除文件夹
rm -rf /path/to/claude-obsidian
```

知识库内容（`wiki/` 下的 Markdown 文件）卸载后仍保留。

---

## 学习资源

- 📖 [官方博客深度解析](https://agricidaniel.com/blog/claude-obsidian-ai-second-brain)
- 🎥 [YouTube 演示视频](https://www.youtube.com/watch?v=a2hgayvr-H4)
- 📚 [Compound Vault 指南](docs/compound-vault-guide.md)
- 📚 [知识组织模式指南](docs/methodology-modes-guide.md)
- 📚 [DragonScale 记忆扩展](docs/dragonscale-guide.md)
- 💬 [AI Marketing Hub 社区](https://www.skool.com/ai-marketing-hub-pro)
- 🔗 [GitHub 仓库](https://github.com/AgriciDaniel/claude-obsidian)
