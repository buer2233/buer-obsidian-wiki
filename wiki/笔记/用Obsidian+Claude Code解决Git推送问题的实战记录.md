# 用 Obsidian + Claude Code 解决 Git 推送问题的实战记录

来源：.raw/笔记/
日期：2026-07-03

> 一次真实的经历：AI 遇到问题 → 从知识库检索方案 → 30秒解决问题。这就是 Obsidian 作为 AI 第二大脑的价值。

---

## 背景

2026年7月3日晚上，我正在用 Claude Code 处理几件事：

1. 新任务开发
2. 任务开发完成后配置每晚11:30的定时任务
3. 执行git（git add → commit → push）

前两步都很顺利，直到执行 `git push` 时，报错了：

```
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```

---

## 问题排查过程

### 第一次尝试：检查 SSH 连接

```bash
ssh -T git@github.com
```

结果：**连接成功**，显示 `Hi buer2233! You've successfully authenticated`。

这就奇怪了——SSH 明明是通的，为什么 `git push` 不行？

### 第二次尝试：切换 HTTPS

```bash
git remote set-url origin https://github.com/buer2233/learn-everyday-loop.git
git push
```

结果：网络连接被重置，HTTPS 也不行。

### 第三次尝试：查看详细 SSH 日志

```bash
ssh -vT git@github.com 2>&1 | head -30
```

关键发现：

```
debug1: identity file /mnt/c/Users/admin/.ssh/id_rsa type -1
debug1: identity file /mnt/c/Users/admin/.ssh/id_ed25519 type -1
```

所有密钥文件都显示 `type -1`，意味着 **SSH 没有找到任何密钥**。但 `ssh -T` 却能成功？这说明 `ssh` 命令和 `git` 内部使用的 SSH 客户端**不是同一个**。

---

## 关键转折：从 Obsidian 知识库找到答案

这时我想起了一件事——之前遇到过类似的问题，并且把解决方案记录在了 Obsidian 知识库里。

我让 Claude Code 搜索 Obsidian：

```
从obsidian中查找Git推送失败的解决方案
```

Claude 通过 MCP 工具 `obsidian_simple_search` 搜索了整个知识库，找到了一篇文档：

**`wiki/Codex/工程经验/Git SSH Windows路径解析错误规避.md`**

---

## 文档中的解决方案

这篇文档详细记录了问题的根本原因和解决方案：

### 根本原因

`GIT_SSH_COMMAND` 不是单纯由 PowerShell 解析后执行，而是会被 Git for Windows / MSYS 运行时转交给 Git 内部的 SSH 调用链解析。

在这个解析链里，Windows 路径中的反斜杠 `\` 容易被当成转义字符：

```powershell
# ❌ 错误写法（反斜杠被吞掉）
$env:GIT_SSH_COMMAND = 'C:\Windows\System32\OpenSSH\ssh.exe -i C:\Users\admin\.ssh\id_ed25519 -o IdentitiesOnly=yes'

# Git 执行时会解析成：
# C:WindowsSystem32OpenSSHssh.exe → command not found
```

### 正确做法

**使用正斜杠路径**：

```powershell
# ✅ 正确写法
$env:GIT_SSH_COMMAND = 'C:/Windows/System32/OpenSSH/ssh.exe -i C:/Users/admin/.ssh/id_ed25519 -o IdentitiesOnly=yes'
git push
```

### 长期方案

在 `~/.ssh/config` 中配置：

```sshconfig
Host github.com
    HostName github.com
    User git
    IdentityFile C:/Users/admin/.ssh/id_ed25519
    IdentitiesOnly yes
```

---

## 实际执行结果

按照文档中的方案，我执行了：

```bash
GIT_SSH_COMMAND='C:/Windows/System32/OpenSSH/ssh.exe -i C:/Users/admin/.ssh/id_ed25519 -o IdentitiesOnly=yes' git push
```

结果：

```
To github.com:buer2233/learn-everyday-loop.git
   a2aed75..0ca9a60  master -> master
```

**推送成功！** 从发现问题到解决，整个过程不到 2 分钟。

---

## 为什么 Obsidian 在这里发挥了关键作用

### 1. 知识沉淀，不是一次性的

如果这个问题的解决方案只是在某次对话中出现过，没有被记录，那么下次遇到同样的问题，我还得重新排查、重新搜索。

但因为之前已经把解决方案写入了 Obsidian 知识库，这次直接检索就能找到。

### 2. AI 可以直接读取和检索

通过 Obsidian 的 MCP（Model Context Protocol）集成，Claude Code 可以：

- **搜索**：`obsidian_simple_search` 全文检索所有笔记
- **读取**：`obsidian_get_file_contents` 获取完整文档内容
- **写入**：`obsidian_append_content` 追加新内容

这意味着 AI 不只是一个"对话工具"，而是一个**有记忆的助手**。

### 3. 知识库的结构化组织

Obsidian 知识库结构：

```
claude-obsidian/
├── .raw/                    ← 原始资料（AI 读取，不修改）
├── wiki/                    ← AI 生成的知识库
│   ├── index.md             ← 主目录索引
│   ├── hot.md               ← 热缓存（最近上下文）
│   ├── Codex/
│   │   └── 工程经验/
│   │       └── Git SSH Windows路径解析错误规避.md  ← 就是这篇！
│   └── ...
├── _templates/              ← Obsidian 模板
└── CLAUDE.md                ← Claude Code 项目指令
```

工程经验被归类到 `wiki/Codex/工程经验/` 下，和学习笔记、AI 知识等分开，方便检索。

---

## Obsidian + Claude Code 搭建简明教程

### 第一步：创建 Obsidian 知识库

1. 安装 [Obsidian](https://obsidian.md)
2. 点击**创建新库**，选择一个干净的文件夹

> ⚠️ **必须单独建一个干净的库**，不要混进已有的笔记库，否则 AI 会读错地方。

### 第二步：安装 Local REST API 插件

1. Obsidian → 左下角**设置** → **第三方插件** → **关闭安全模式**
2. 点击**社区插件市场 → 浏览**，搜索 **`Local REST API`**，安装并启用
3. 进入插件设置，复制 **API Key**

### 第三步：在 Claude Code 中建立连接

在终端中粘贴以下命令（替换 `你的API密钥`）：

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

### 第四步：验证连接

在 Claude Code 中说：

```
列出当前库的文件列表
```

能看到文件列表就说明连接成功。

### 第五步：开始使用

```bash
# 让 AI 读取资料并创建知识页面
ingest 我的笔记.md

# 向 AI 提问（会从知识库检索）
关于 Git SSH 你知道什么？

# 保存当前对话为笔记
/save
```

---

## 本次事件的时间线

| 时间 | 事件 |
|------|------|
| 之前某次 | 遇到 Git SSH 问题，排查后将解决方案写入 Obsidian |
| 2026-07-03 23:30 | 配置定时任务时再次遇到 `git push` 失败 |
| +30秒 | 让 Claude Code 搜索 Obsidian 知识库 |
| +1分钟 | 找到文档，按方案执行，推送成功 |
| +2分钟 | 配置好定时任务，所有工作完成 |

**如果没有 Obsidian 知识库**，这个过程可能需要：
- 10-30分钟重新排查问题
- 搜索 Google/Stack Overflow
- 尝试各种方案

**有了 Obsidian 知识库**：1分钟搞定。

---

## 核心理念：AI 的第二大脑

```
  你投放资料          AI 读取并整理           你提问
     │                    │                    │
     ▼                    ▼                    ▼
  .raw/ 目录    →    AI 提取实体/概念    →   AI 从 wiki 中
  (原始文件)         建立交叉引用              检索并综合回答
                    更新索引                  引用具体页面
                    更新热缓存
```

Obsidian 不只是笔记软件，它是 **AI 的外部记忆**：

- **`.raw/`** — 原始资料（你投放）
- **`wiki/`** — AI 整理后的知识库（结构化、可检索）
- **Claude Code** — 读取、检索、回答的桥梁

---

## 本次事件带给我的启发

1. **遇到问题，先查知识库** — 你可能已经解决过同样的问题
2. **解决方案要沉淀** — 不只是在对话中解决，还要写入 Obsidian
3. **AI + 知识库 > AI alone** — 没有知识库的 AI 只能靠训练数据，有知识库的 AI 能用你的经验
4. **工程经验特别值得记录** — 环境配置、路径问题、版本兼容性，这些"小坑"最容易重复踩

---

## 🔗 关联文档

- [[Codex/工程经验/Git SSH Windows路径解析错误规避]] — 本次事件的原始解决方案文档
- [[Docker]] — Docker使用经验
- [[Jenkins全攻略]] — Jenkins配置经验

---

## 相关资源

- 🏠 [Obsidian 官网](https://obsidian.md)
- 📦 [claude-obsidian 项目](https://github.com/AgriciDaniel/claude-obsidian)

---

*写于 2026-07-03，一次 Claude Code + Obsidian 的真实实战体验。*

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[Git SSH Windows路径解析错误规避]] — AI测试主题关联
- [[Docker]] — AI测试主题关联
- [[Jenkins全攻略]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[邓万鹏-AI自动化测试]] — AI测试主题关联
- [[UI自动化测试日常问题记录]] — AI测试主题关联
- [[安卓移动端appium环境搭建流程]] — AI测试主题关联
- [[vibecoding总结]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
