---
type: reference
title: "OMP（Oh My Pi）使用手册"
source: ".raw/AI相关学习资料/OMP使用手册.md"
created: 2026-09-10
updated: 2026-09-10
tags:
  - AI编码Agent
  - OMP
  - 使用手册
  - 工具参考
  - 测试开发
status: live
related:
  - "[[wiki/AI相关学习资料/OMP的设计经验]]"
  - "[[wiki/AI相关学习资料/AI编码Agent五工具对比分析报告]]"
  - "[[wiki/AI相关学习资料/测试开发如何使用DSH]]"
  - "[[wiki/AI相关学习资料/Pi的AI设计经验]]"
---

# OMP（Oh My Pi）使用手册

> 基于 GitHub 开源项目 [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) 整理（v18.x）｜官网 https://omp.sh ｜ 许可证 MIT ｜ TypeScript + Rust 核心（~80k 行）

**OMP（命令名 `omp`）**是一个**把 IDE 能力内置进来的编码智能体**，口号 *"A coding agent with the IDE wired in"*。它基于 Mario Zechner 的 Pi 项目 fork 演化，定位为「编码优先、开箱即用、**Windows 原生（无需 WSL）**」的 Agent 终端。

## 核心数据一览

| 指标 | 数值 |
|---|---|
| 支持的模型提供商 | **60+**（Anthropic、OpenAI、Gemini、DeepSeek、Kimi、智谱、Ollama 等） |
| 内置工具 | **31 个** |
| LSP 操作 | 14 个（代码跳转/重命名/诊断） |
| 调试器（DAP）操作 | 28 个（lldb/dlv/debugpy） |
| Rust 原生核心 | ~80k 行（嵌入式 bash、ripgrep、AST 引擎等） |

**与同类工具的关系**：Claude Code / Codex CLI 是厂商绑定的终端 Agent；OMP 是**多提供商中立 Agent**，**可直接继承** Claude Code/Codex/Cursor/CLine/Copilot 等 8 种工具的已有配置，迁移成本低；支持 ACP 协议，可作为 Zed 的 Agent 后端运行。

## 一、安装

| 平台 | 命令 |
|---|---|
| macOS / Linux（脚本） | `curl -fsSL https://omp.sh/install \| sh` |
| **Windows（PowerShell）** | `irm https://omp.sh/install.ps1 \| iex` |
| macOS / Linux（Homebrew） | `brew install can1357/tap/omp` |
| Bun 全局安装（推荐） | `bun install -g @oh-my-pi/pi-coding-agent` |
| Nix 免安装运行 | `nix run github:can1357/oh-my-pi` |
| mise 版本锁定 | `mise use -g github:can1357/oh-my-pi` |

**环境要求**：Bun 安装方式需 bun ≥ 1.3.14；Alpine/musl 用户需先 `apk add libstdc++ libgcc`。

> 💡 Windows 用户注意：OMP 是 **Windows 原生**实现（进程内 ripgrep/glob/bash），**不需要 WSL**。

**Shell 补全**：`eval "$(omp completions bash)"`（或 zsh / fish）
**更新**：`omp update`（`--canary` 切 canary 频道，`--stable` 切回）

## 二、快速上手（5 分钟）

```bash
# Windows PowerShell
irm https://omp.sh/install.ps1 | iex
omp                       # 启动交互式 TUI
```

**第 2 步：登录模型提供商**（按提供商隔离，登录 anthropic 不会自动登录 openai）
```
/login              # 打开 OAuth/Key 选择器
/login anthropic    # 直接登录 Anthropic（OAuth）
```
或直接用环境变量：`export ANTHROPIC_API_KEY=sk-ant-...`

**常用操作**：`Ctrl+P` 循环切换模型 ｜ `/model` 打开选择器 ｜ `omp models` 查看已登录模型 ｜ `omp usage` 查看用量/限额 ｜ `omp --continue` / `-c` 继续上次会话

## 三、四大运行入口

| 入口 | 命令 | 用途 |
|---|---|---|
| **交互式 TUI** | `omp` / `omp "修复这个构建错误"` / `omp @需求文档.md "按文档实现"` | 日常使用；`@` 前缀附加文件/图片 |
| **一次性提问（Headless）** | `omp -p "总结最近一次 commit 的改动"` | 脚本自动化；`--mode json` 输出机器可读 JSON 事件流；`echo "review this diff" \| omp -p` 走 stdin |
| **RPC 模式** | `omp --mode rpc` / `--mode rpc-ui` | stdio JSON-RPC（NDJSON），供外部程序驱动 |
| **ACP 模式** | `omp acp` | Agent Client Protocol，可在 **Zed** 等编辑器作为 Agent 后端运行 |
| **Node SDK** | `bun install @oh-my-pi/pi-coding-agent` | 二次开发嵌入（`createAgentSession` / `ModelRegistry`） |

RPC 通信格式（NDJSON）示例：
```json
> {"id":"r1","type":"prompt","message":"list .ts files"}
< {"id":"r1","type":"response", ...}
> {"id":"r2","type":"set_model","provider":"anthropic","modelId":"sonnet-4.5"}
```

## 四、常用 CLI 参数速查

### 4.1 会话与工作区

| 参数 | 说明 |
|---|---|
| `--cwd <dir>` | 指定启动目录 |
| `--add-dir <dir>` | 追加额外工作区目录（可重复） |
| `--continue` / `-c` | 继续上一个会话 |
| `--resume [id]` / `-r` | 恢复指定会话（不带 id 打开选择器） |
| `--fork <session>` | Fork 一个已保存会话为新会话 |
| `--from-claude` / `--from-codex` | **导入 Claude Code / Codex 的历史会话** |
| `--export <session>` | 导出会话为 HTML |
| `--profile <name>` | 使用隔离的配置档案 |

### 4.2 模型选择

| 参数 | 说明 |
|---|---|
| `--model <id-or-role>` | 指定模型或角色（支持模糊匹配，如 `opus`、`openai/gpt-5.2`） |
| `--smol` / `--slow` / `--plan <id>` | 轻量快速模型 / 深度推理模型 / 架构规划模型 |
| `--models <a,b,c>` | 定义 `Ctrl+P` 循环切换的模型列表 |
| `--api-key <key>` | 运行时 API key（优先级最高，不持久化） |

### 4.3 思考与审批

| 参数 | 说明 |
|---|---|
| `--thinking <level>` | `off`/`minimal`/`low`/`medium`/`high`/`xhigh`/`max`/`auto` |
| `--tools read,edit,bash` | 只启用指定工具 |
| `--approval-mode <mode>` | `always-ask` / `write` / `yolo` |
| `--auto-approve` / `--yolo` | 自动批准所有工具调用（**慎用**） |
| `--advisor` | 启用第二模型顾问（每轮被动审查并注入笔记） |
| `--max-time <duration>` | 会话限时（如 `600`、`10m`、`1h`） |

### 4.4 扩展、技能与规则

| 参数 | 说明 |
|---|---|
| `-e <path>` / `--extension <path>` | 加载扩展（可重复） |
| `--skills <globs>` | 过滤技能（如 `git-*,docker`） |
| `--no-skills` / `--no-rules` / `--no-lsp` | 禁用技能/规则发现/LSP |
| `--system-prompt` / `--append-system-prompt <text\|file>` | 替换 / 追加系统提示词 |

## 五、模型与提供商配置

### 5.1 认证方式与优先级

| 方式 | 操作 | 优先级 |
|---|---|---|
| CLI 运行时覆盖 | `--api-key` | 1（最高，不持久化） |
| models.yml 固定 key | `~/.omp/agent/models.yml` | 2 |
| OAuth 登录 | TUI 中 `/login <provider>` | 3（自动刷新，多账号轮换） |
| `/login` 保存的 API Key | TUI 交互式输入 | 4 |
| 环境变量 / `.env` 文件 | 见下表 | 5 |

**凭据存储位置**：`~/.omp/agent/agent.db`

**常用环境变量**：`ANTHROPIC_API_KEY`、`OPENAI_API_KEY`、`GEMINI_API_KEY`、`DEEPSEEK_API_KEY`、`MOONSHOT_API_KEY`、`OPENROUTER_API_KEY`、`ZHIPU_API_KEY`、`COPILOT_GITHUB_TOKEN`；Ollama 默认 `http://127.0.0.1:11434`（无需 key）

### 5.2 `.env` 自动加载优先级

```
进程已导出的环境变量 > <当前目录>/.env > ~/.omp/agent/.env > ~/.omp/.env > ~/.env
```

### 5.3 自定义提供商（接入任意 OpenAI 兼容网关）⭐

> **重要：providers 必须是列表形式**（`providers: [{name, baseUrl, ...}, ...]`），每个 provider 用 `name` 字段指定名字。

```yaml
# ~/.omp/agent/models.yml
providers:
  - name: spark                            # 自定义 provider 名（用 name 字段）
    baseUrl: http://192.168.10.223:8000/v1
    api: openai-completions                # 或 anthropic-messages / bedrock-converse-stream
    apiKey: MY_GATEWAY_API_KEY             # 环境变量名或字面量；前缀 ! 表示 shell 命令
    models:
      - id: minimax-m3
        name: MiniMax M3
        contextWindow: 100000
        maxTokens: 32000
  - name: local-ollama
    baseUrl: http://127.0.0.1:11434/v1
    api: openai-completions
    auth: none                             # 免密本地服务用 auth: none
    models:
      - id: qwen2.5-coder:14b
        contextWindow: 32768
        maxTokens: 8192
```

验证与启用：`omp models spark`（验证加载）｜ `omp setup` 或在 TUI 用 `/model` 分配角色

### 5.4 模型角色（9 种）

OMP 把不同任务路由到不同模型，角色定义在 `~/.omp/agent/config.yml`：

| 角色 | 用途 |
|---|---|
| `default` | 默认主力模型 |
| `smol` | 轻量任务（索引、简单问答） |
| `slow` | 深度推理 |
| `plan` | 架构规划 |
| `commit` | 生成 commit 消息 |
| `vision` | 图像理解 |
| `task` | 子代理任务 |
| `advisor` | 顾问（第二模型审查） |
| `tiny` | 极小任务（会话标题、记忆，可用 `omp tiny-models` 下载本地小模型） |

```yaml
modelRoles:
  default: spark/minimax-m3
  slow: anthropic/claude-opus-4-6
```

**高级路由四旋钮**：① Fallback 链（`retry.fallbackChains`，遇 429 限流自动切换）② Path-scoped 模型（`enabledModels` 加 `path:` 前缀按仓库锁模型）③ Round-robin 凭证（同一提供商堆叠多个 key 运行时轮转）④ 自定义 API 类型

## 六、31 个内置工具概览

| 类别 | 工具 | 说明 |
|---|---|---|
| 文件与搜索 | `read` `write` `edit` `ast_edit` `ast_grep` `grep` `glob` | 读写编辑、AST 级精准修改、进程内原生搜索 |
| 运行时 | `bash` `eval` | 内嵌 bash（46 个 coreutils）；**持久 Python/JS worker** |
| 代码智能 | `lsp` `debug` `security_scan` | LSP 14 种操作；**真实调试器附加**；安全扫描 |
| 协调 | `task` `hub` `todo` `ask` | 子代理扇出；任务列表；向用户提问 |
| 桌面与 Web | `browser` `computer` `web_search` `github` `generate_image` `tts` | 真实浏览器驱动；桌面控制；23 家搜索供应商 |
| 记忆与技能 | `checkpoint` `rewind` `retain` `recall` `reflect` `memory_edit` `learn` `manage_skill` | 记忆管理（后端可选 local/Hindsight/Mnemopi） |

**默认关闭的工具**（需在设置中开启）：`github`、`security_scan`、`generate_image`、`tts`、`checkpoint`、`rewind`、记忆类工具。

**两个杀手锏特性**：
1. **Hashline 编辑**：`edit` 工具按**内容哈希锚点**定位编辑点而非行号——省 token 且防止编辑错位/文件损坏
2. **时间旅行流规则（TTSR）**：流式输出中用正则匹配到危险内容时，中止当前流、注入规则、自动重试，且**不占用上下文窗口**

## 七、核心特性详解

| 特性 | 说明 |
|---|---|
| **LSP 接入每一次写入** | 每次 `write`/`edit` 后自动走 LSP：诊断错误、格式化，错误作为工具结果喂回 Agent 上下文当场自愈；重命名走 `workspace/willRenameFiles`，**自动更新所有 re-exports 和 barrel files** |
| **驱动真实调试器（DAP）** | 附加 **lldb（C/C++/Rust）/ dlv（Go）/ debugpy（Python）**，28 种操作：断点、单步、查变量、调用栈 |
| **一等子代理（task）与 Agent Hub** | 扇出隔离的 git worktree 子代理，各自独立上下文，返回 **schema 验证过的结构化对象**（不是自由文本） |
| **Vibe 模式（导演模式）** ⭐ | `/vibe` 把当前会话变成导演：自己不编辑代码，只保留 `read` 和 5 个 worker 控制工具，指挥常驻后台 worker |
| **顾问（Advisor）** | `--advisor` 启用后第二个模型在独立上下文中**被动审查每一轮**，发现问题注入笔记 |
| **协作（Collab）** | `/collab` 生成中继链接 + 二维码，他人以读写或只读方式加入同一会话 |
| **GitHub 即文件系统** | `read` 可直接读 GitHub 内部 URI：`pr://`、`issue://`、`agent://`、`skill://`、`ssh://` 等 16 种 scheme |
| **冲突解决** | 冲突文件以 `conflict://N` 暴露，可写 `@theirs`/`@ours`/`@base` 三方内容，语义化解决合并冲突 |
| **omp commit** | 自动分析改动 → **原子化拆分**成多个逻辑提交 → 依赖排序 → 生成并验证 commit 消息 → 更新 changelog |
| **/review** | 生成带 **P0-P3 优先级**和 verdict 结论的审查报告 |
| **代理管理记忆** | `retain` / `learn` / `recall` 自主管理长期记忆 |
| **桌面与浏览器控制** | `eval` 里 `browser.open()` 返回真实 tab handle 驱动你的 Chrome（配合 `omp browser-relay` 本地 CDP 中继）；`computer` 工具控制窗口、截图、原生输入、读无障碍树 |

**Vibe 模式两级 worker**：

| 层级 | 内置代理 | 默认模型 | 用途 |
|---|---|---|---|
| `fast` | sonic | `@smol` | 机械执行、草稿、大批量任务 |
| `good` | task | `@task` | 设计、判断、审查 fast 的产出 |

控制工具：`vibe_spawn`（派生）、`vibe_send`（追加指令）、`vibe_wait`（等待）、`vibe_kill`（终止）、`vibe_list`（列出）
典型玩法：需求拆成多个独立工作流 → 每流 spawn 常驻 worker → 并行跑 fast/good 混合梯队 → 导演用 `read` 验证产出 → `vibe_send` 纠偏

## 八、斜杠命令与魔法关键字

**常用斜杠命令**：`/model`｜`/login [provider]`｜`/logout`｜`/vibe`｜`/fresh`（重置流状态保留会话）｜`/review`｜`/collab`｜`/join`｜`/share`｜`/debug`

**魔法关键字**（在普通提示词中包含即可触发）：`ultrathink`（最大深度思考）｜`orchestrate`（编排子代理/工作流）｜`workflowz`（工作流模式）

**快捷键**：`Ctrl+P` 循环切换模型

## 九、配置文件体系

```
~/.omp/
├── agent/
│   ├── agent.db          # 凭据存储（OAuth/API key）
│   ├── config.yml        # 主配置（modelRoles、retry 等）
│   ├── models.yml        # 自定义提供商
│   ├── .env              # 环境变量
│   └── wt/               # agent 管理的 git worktrees
└── ...
```

**配置读取优先**：进程环境变量 > CLI 参数覆盖 > `~/.omp/agent/config.yml` > `--config` 附加 overlay

**继承其他工具配置**：可直接读取 Cursor、CLine、Codex、Copilot、Claude Code 等 **8 种工具**的已有配置文件

**配置管理命令**：`omp config`（管理配置项）｜`omp models`（列出/刷新模型）｜`omp setup`（引导式初始化）

## 十、典型使用场景

| 场景 | 做法 |
|---|---|
| **日常编码** | `omp "给 utils/date.ts 里的 formatDate 函数补上单元测试"` → grep 定位 → read → 写测试 → LSP 诊断 → 运行验证 |
| **无头脚本（CI）** | `omp -p "总结最近一次 commit，输出 markdown" > changelog.md`；`omp -p --mode json "检查未使用导出" \| jq ...` |
| **原子化提交** | `git add -A && omp commit` |
| **并行重构大任务** | `/vibe 把这个 monorepo 从 jest 迁移到 vitest` |
| **接入公司内部模型网关** | 配 `models.yml` → `omp models company-gw` 验证 → `omp --model qwen3-coder` 使用 |
| **在 Zed 编辑器中使用** | `omp acp` 作为 ACP 服务器，Zed 设置里选 OMP 作 Agent 后端 |

## 十一、SDET 视角：测试工程师如何用 OMP

| 测试场景 | OMP 能力 | 做法 |
|---|---|---|
| 生成/维护接口测试用例 | `read` + `eval`（持久 Python） | 让 Agent 读源码/抓包文件，直接在持久 Python worker 里调 requests + pytest 生成并试跑用例 |
| **调试测试失败** | `debug` 工具（debugpy/DAP） | pytest 挂了让 Agent 附加真实调试器查变量、调用栈，**而非人肉 print** |
| 批量重构测试代码 | `/vibe` 导演模式 | fast worker 批量迁移断言风格，good worker 审查边界情况 |
| 代码审查/提测前自检 | `/review` | 生成 P0-P3 优先级问题清单，当作提测门禁 |
| UI 自动化探索 | `browser.open()` | Agent 驱动真实 Chrome 验证选择器是否有效，再固化到 Playwright 用例 |
| 语义化解决合并冲突 | `conflict://N` | 测试脚本多人协作冲突时用 @theirs/@ours 语义解决 |
| CI 里的智能检查 | `omp -p --mode json` | 无头模式嵌入流水线，输出结构化结果供下游解析 |
| 从 Claude Code 迁移 | `--from-claude` | 直接导入历史会话；继承原有配置，零成本切换 |

**与「AI 接口自动化 SKILL」思路的对照**：OMP 的 `manage_skill` 工具 + skills 发现机制（`--skills git-*,docker` 过滤）与 Claude Code 的 SKILL 体系理念相通——**把领域工作流沉淀成可复用技能，Agent 按需加载**。

## 十二、常见问题与故障排查

| Q | 排查 |
|---|---|
| **模型列表里看不到某个模型？** | ① provider 是否已登录或设了环境变量 ② 是否被 `disabledProviders` 禁用（禁用检查优先于凭据）③ 自定义 provider 的 YAML 是否有语法错误（`omp models` 验证） |
| **`.env` 里的 key 没生效？** | 优先级：已导出进程环境变量 > `<cwd>/.env` > `~/.omp/agent/.env` > `~/.omp/.env` > `~/.env`；先检查 shell 是否导出过旧 key |
| **Windows 上需要 WSL 吗？** | 不需要，OMP 是 Windows 原生实现 |
| **怎么限制 Agent 别乱改文件？** | `--approval-mode write`（写操作需确认）或 `always-ask`；最保守 `--tools read,grep` 只给只读工具；反向放开用 `--yolo` |
| **会话存在哪？怎么恢复？** | `~/.omp/agent/`；`omp -r` 打开选择器，`omp -c` 继续最近会话，`--fork` 复制分支 |
| **如何控制成本？** | ① 模型角色把简单任务路由到 `smol`/`tiny` ② `omp tiny-models` 下载本地小模型跑会话标题和记忆 ③ `omp usage` 监控用量与限额 |

## 附录：关键文档索引

| 文档 | 内容 |
|---|---|
| README | 项目总览 |
| `docs/cli-reference.md` | CLI 完整参考 |
| `docs/providers.md` / `docs/models.md` | 提供商认证大全 / 模型解析与角色 |
| `docs/vibe-mode.md` / `docs/approval-mode.md` | 导演模式 / 审批模式 |
| `docs/skills.md` / `docs/extensions.md` / `docs/mcp-config.md` | 技能、扩展、MCP 配置 |
| `docs/memory.md` / `docs/collab.md` | 记忆系统 / 协作会话 |
| `docs/sdk.md` / `docs/rpc.md` | Node SDK / RPC 协议 |

> 📌 OMP 迭代很快（当前 v18.x），以官方仓库 README 与 `docs/` 为最终准绳。

## 🔗 关联文档

- [[wiki/AI相关学习资料/OMP的设计经验|OMP 的设计经验]] — 设计决策背后的工程经验
- [[wiki/AI相关学习资料/AI编码Agent五工具对比分析报告|AI 编码 Agent 五工具对比]] — 选型矩阵
- [[wiki/AI相关学习资料/测试开发如何使用DSH|测试开发如何使用 DSH]] — 另一套可组装框架
- [[wiki/AI相关学习资料/Pi的AI设计经验|Pi 的 AI 设计经验]] — OMP 的上游项目
- [[wiki/语雀/claude-code/Claude Code学习笔记|Claude Code 学习笔记]] — 配置继承来源之一
- [[wiki/语雀/claude-code/Harness Engineering（驾驭工程）|Harness Engineering]] — Agent 设计原则

## 源文件

- `.raw/AI相关学习资料/OMP使用手册.md`
