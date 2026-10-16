# OMP（Oh My Pi）使用手册

> 基于 GitHub 开源项目 [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) 整理（2026-09 最新版，v18.x）
> 官网：https://omp.sh ｜ 许可证：MIT ｜ 语言：TypeScript + Rust 核心（~80k 行）

---

## 目录

1. [OMP 是什么](#一omp-是什么)
2. [安装](#二安装)
3. [快速上手（5 分钟）](#三快速上手5-分钟)
4. [四大运行入口](#四四大运行入口)
5. [常用 CLI 参数速查](#五常用-cli-参数速查)
6. [模型与提供商（Provider）配置](#六模型与提供商provider配置)
7. [31 个内置工具概览](#七31-个内置工具概览)
8. [核心特性详解](#八核心特性详解)
9. [斜杠命令与魔法关键字](#九斜杠命令与魔法关键字)
10. [配置文件体系](#十配置文件体系)
11. [典型使用场景实战](#十一典型使用场景实战)
12. [SDET 视角：测试工程师如何用 OMP](#十二sdet-视角测试工程师如何用-omp)
13. [常见问题与故障排查](#十三常见问题与故障排查)

---

## 一、OMP 是什么

**Oh My Pi（命令名 `omp`）** 是一个**把 IDE 能力内置进来的编码智能体（coding agent）**，口号是 *"A coding agent with the IDE wired in"*。

它基于 Mario Zechner 的 [Pi](https://github.com/badlogic/pi-mono) 项目 fork 演化而来，定位为「编码优先、开箱即用、Windows 原生（无需 WSL）」的 Agent 终端。

### 核心数据一览

| 指标 | 数值 |
|------|------|
| 支持的模型提供商 | 60+（Anthropic、OpenAI、Gemini、DeepSeek、Kimi、智谱、Ollama 等） |
| 内置工具 | 31 个 |
| LSP 操作 | 14 个（代码跳转/重命名/诊断） |
| 调试器（DAP）操作 | 28 个（lldb/dlv/debugpy） |
| Rust 原生核心 | ~80k 行（嵌入式 bash、ripgrep、AST 引擎等） |

### 与同类工具的关系

| 工具 | 定位 |
|------|------|
| Claude Code / Codex CLI | 厂商绑定的终端 Agent |
| **OMP** | 多提供商中立 Agent，**可直接继承** Claude Code/Codex/Cursor/CLine/Copilot 等 8 种工具的已有配置，迁移成本低 |
| Zed 内置 Agent | OMP 支持 ACP 协议，可作为 Zed 的 Agent 后端运行 |

---

## 二、安装

### 2.1 各平台安装命令

| 平台 | 命令 |
|------|------|
| macOS / Linux（脚本） | `curl -fsSL https://omp.sh/install \| sh` |
| **Windows（PowerShell）** | `irm https://omp.sh/install.ps1 \| iex` |
| macOS / Linux（Homebrew） | `brew install can1357/tap/omp` |
| Bun 全局安装（推荐） | `bun install -g @oh-my-pi/pi-coding-agent` |
| Nix 免安装运行 | `nix run github:can1357/oh-my-pi` |
| mise 版本锁定 | `mise use -g github:can1357/oh-my-pi` |

**环境要求**：macOS / Linux / Windows 均可；Bun 安装方式需 bun ≥ 1.3.14。Alpine/musl 用户需先执行 `apk add libstdc++ libgcc`。

> 💡 Windows 用户注意：OMP 是 **Windows 原生**实现（进程内 ripgrep/glob/bash），不需要 WSL。

### 2.2 Shell 补全（可选）

```bash
# zsh —— 加入 ~/.zshrc
eval "$(omp completions zsh)"

# bash —— 加入 ~/.bashrc
eval "$(omp completions bash)"

# fish
omp completions fish > ~/.config/fish/completions/omp.fish
```

### 2.3 更新

```bash
omp update                # 更新到最新稳定版
omp update --canary       # 切换到 canary 频道
omp update --stable       # 切回 stable 频道
```

---

## 三、快速上手（5 分钟）

### 第 1 步：安装并启动

```bash
# Windows PowerShell
irm https://omp.sh/install.ps1 | iex

# 启动交互式 TUI
omp
```

### 第 2 步：登录模型提供商

进入 TUI 后执行斜杠命令登录（按提供商隔离，登录 anthropic 不会自动登录 openai）：

```
/login              # 打开 OAuth/Key 选择器
/login anthropic    # 直接登录 Anthropic（OAuth）
/login openai       # 直接登录 OpenAI
```

或者直接用环境变量（在进入 omp 前设置）：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export DEEPSEEK_API_KEY=sk-...
```

### 第 3 步：开始对话

```
帮我把 src/ 下所有用到旧 API 的地方列出来，并给出重构建议
```

工具调用会渲染成**卡片**：编辑操作先出预览、确认后才落盘；有歧义时通过 `ask` 工具向你提问。

### 第 4 步：常用操作

| 操作 | 方式 |
|------|------|
| 切换模型 | `Ctrl+P` 循环切换，或 `/model` 打开选择器 |
| 查看已登录的模型 | 退出 TUI 后执行 `omp models` |
| 查看用量/限额 | `omp usage` |
| 继续上次会话 | `omp --continue` 或 `omp -c` |

---

## 四、四大运行入口

### 4.1 交互式 TUI（默认，日常使用）

```bash
omp                          # 空会话启动
omp "修复这个构建错误"        # 带初始提示词启动
omp @需求文档.md "按文档实现"  # @ 前缀附加文件/图片
```

### 4.2 一次性提问（Headless / Print 模式，脚本自动化）

```bash
# 处理完 prompt 直接退出，结果输出到 stdout
omp -p "总结最近一次 commit 的改动"

# 机器可读的 JSON 事件流（适合管道）
omp -p --mode json "列出 src/ 下所有 TODO" > todos.json

# 通过 stdin 管道输入
echo "review this diff" | omp -p

# 包含思考过程
omp -p --print-thoughts "解释这次重构的理由"
```

### 4.3 RPC 模式（stdio JSON-RPC，供外部程序驱动）

```bash
omp --mode rpc            # 纯 RPC
omp --mode rpc-ui         # RPC + UI 扩展事件
```

通信格式为 NDJSON：

```json
> {"id":"r1","type":"prompt","message":"list .ts files"}
< {"id":"r1","type":"response", ...}
> {"id":"r2","type":"set_model","provider":"anthropic","modelId":"sonnet-4.5"}
> {"id":"r3","type":"abort"}
```

### 4.4 ACP 模式（Agent Client Protocol，编辑器集成）

```bash
omp acp
```

基于 JSON-RPC 的 [Agent Client Protocol](https://github.com/zed-industries/agent-client-protocol)，可在 **Zed** 等编辑器中把 OMP 作为 Agent 后端，读写都经由编辑器完成。

### 4.5 Node SDK 嵌入（二次开发）

```bash
bun install @oh-my-pi/pi-coding-agent
```

```typescript
import {
  ModelRegistry,
  SessionManager,
  createAgentSession,
  discoverAuthStorage,
} from "@oh-my-pi/pi-coding-agent";

const auth = await discoverAuthStorage();
const models = new ModelRegistry(auth);
await models.refresh();

const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
  authStorage: auth,
  modelRegistry: models,
});
await session.prompt("list .ts files");
```

---

## 五、常用 CLI 参数速查

> 完整参考见 `docs/cli-reference.md`，或 `omp --help` / `omp <command> --help`。

### 5.1 会话与工作区

| 参数 | 说明 |
|------|------|
| `--cwd <dir>` | 指定启动目录 |
| `--add-dir <dir>` | 追加额外工作区目录（可重复） |
| `--continue` / `-c` | 继续上一个会话 |
| `--resume [id]` / `-r` | 恢复指定会话（不带 id 则打开选择器） |
| `--fork <session>` | Fork 一个已保存会话为新会话 |
| `--from-claude` / `--from-codex` | 导入 Claude Code / Codex 的历史会话 |
| `--export <session>` | 导出会话为 HTML |
| `--no-session` | 不保存会话（一次性） |
| `--profile <name>` | 使用隔离的配置档案 |

### 5.2 模型选择

| 参数 | 说明 |
|------|------|
| `--model <id-or-role>` | 指定模型或角色（支持模糊匹配，如 `opus`、`openai/gpt-5.2`） |
| `--smol <id>` | 轻量快速模型（简单任务） |
| `--slow <id>` | 深度推理模型（复杂分析） |
| `--plan <id>` | 架构规划模型 |
| `--models <a,b,c>` | 定义 `Ctrl+P` 循环切换的模型列表 |
| `--api-key <key>` | 运行时 API key（优先级最高，不持久化） |

### 5.3 思考与推理

| 参数 | 说明 |
|------|------|
| `--thinking <level>` | 思考强度：`off` / `minimal` / `low` / `medium` / `high` / `xhigh` / `max` / `auto` |
| `--hide-thinking` | TUI 中隐藏思考块（仅显示，不禁用） |

### 5.4 工具与审批

| 参数 | 说明 |
|------|------|
| `--tools read,edit,bash` | 只启用指定工具 |
| `--no-tools` | 禁用全部内置工具 |
| `--no-lsp` | 禁用 LSP 工具/格式化/诊断 |
| `--approval-mode <mode>` | 审批模式：`always-ask` / `write` / `yolo` |
| `--auto-approve` / `--yolo` | 自动批准所有工具调用（慎用） |
| `--advisor` | 启用第二模型顾问（每轮被动审查并注入笔记） |
| `--max-time <duration>` | 会话限时（如 `600`、`10m`、`1h`） |

### 5.5 扩展、技能与规则

| 参数 | 说明 |
|------|------|
| `-e <path>` / `--extension <path>` | 加载扩展（可重复） |
| `--skills <globs>` | 过滤技能（如 `git-*,docker`） |
| `--no-skills` / `--no-rules` | 禁用技能/规则发现 |
| `--system-prompt <text\|file>` | 替换系统提示词 |
| `--append-system-prompt <text\|file>` | 追加系统提示词 |

---

## 六、模型与提供商（Provider）配置

### 6.1 三种认证方式

| 方式 | 操作 | 优先级 |
|------|------|--------|
| CLI 运行时覆盖 | `--api-key` | 1（最高，不持久化） |
| models.yml 固定 key | `~/.omp/agent/models.yml` | 2 |
| OAuth 登录 | TUI 中 `/login <provider>` | 3（自动刷新，多账号轮换） |
| `/login` 保存的 API Key | TUI 交互式输入 | 4 |
| 环境变量 / `.env` 文件 | 见下表 | 5 |

**凭据存储位置**：`~/.omp/agent/agent.db`。

### 6.2 常用提供商环境变量

| Provider | 环境变量 |
|----------|---------|
| Anthropic | `ANTHROPIC_API_KEY`（OAuth 用 `/login anthropic`） |
| OpenAI | `OPENAI_API_KEY` |
| Google Gemini | `GEMINI_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| Moonshot/Kimi | `MOONSHOT_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Groq | `GROQ_API_KEY` |
| xAI | `XAI_API_KEY` |
| GitHub Copilot | `COPILOT_GITHUB_TOKEN`（或 `/login github-copilot`） |
| Cursor | `CURSOR_ACCESS_TOKEN` |
| 智谱 Coding Plan | `ZHIPU_API_KEY`（或 `/login zhipu-coding-plan`） |
| Ollama（本地） | 默认 `http://127.0.0.1:11434`，无需 key |
| LM Studio（本地） | 默认 `http://127.0.0.1:1234/v1`，无需 key |
| vLLM（本地） | `VLLM_API_KEY`（本地无认证可省略） |

### 6.3 `.env` 文件自动加载

OMP 启动时按以下优先级读取 `.env`（先到先得）：

```
进程已导出的环境变量 > <当前目录>/.env > ~/.omp/agent/.env > ~/.omp/.env > ~/.env
```

项目本地 `.env` 示例：

```dotenv
OPENROUTER_API_KEY=sk-or-...
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

### 6.4 自定义提供商（接入任意 OpenAI 兼容网关）

**重要：providers 必须是列表形式**（`providers: [{name, baseUrl, ...}, ...]`），每个 provider 用 `name` 字段指定名字。

编辑 `~/.omp/agent/models.yml`：

```yaml
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
  - name: local-ollama                     # 同一文件可配多个 provider
    baseUrl: http://127.0.0.1:11434/v1
    api: openai-completions
    auth: none                             # 免密本地服务用 auth: none
    models:
      - id: qwen2.5-coder:14b
        name: Qwen2.5 Coder 14B
        contextWindow: 32768
        maxTokens: 8192
```

验证与启用：

```bash
omp models spark     # 验证自定义 provider 是否加载成功
omp setup            # 或在 TUI 里用 /model 分配角色
```

### 6.5 模型角色（Model Roles，9 种）

OMP 把不同任务路由到不同模型，角色定义在 `~/.omp/agent/config.yml`：

| 角色 | 用途 |
|------|------|
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
# ~/.omp/agent/config.yml —— 设置默认模型
modelRoles:
  default: spark/minimax-m3
  slow: anthropic/claude-opus-4-6
```

### 6.6 高级路由（四旋钮）

1. **Fallback 链**：`retry.fallbackChains` 按角色配置模型链，遇到 429 限流自动切换；
2. **Path-scoped 模型**：`enabledModels` 加 `path:` 前缀，按仓库锁定可用模型；
3. **Round-robin 凭证**：同一提供商堆叠多个 API key，运行时轮转分摊限流；
4. **自定义 API 类型**：`openai-completions` / `anthropic-messages` / `bedrock-converse-stream` 等。

---

## 七、31 个内置工具概览

| 类别 | 工具 | 说明 |
|------|------|------|
| 文件与搜索 | `read` `write` `edit` `ast_edit` `ast_grep` `grep` `glob` | 读写编辑、AST 级精准修改、进程内原生搜索 |
| 运行时 | `bash` `eval` | 内嵌 bash（46 个 coreutils）；持久 Python/JS worker |
| 代码智能 | `lsp` `debug` `security_scan` | LSP 14 种操作；真实调试器附加；安全扫描 |
| 协调 | `task` `hub` `todo` `ask` | 子代理扇出；任务列表；向用户提问 |
| 桌面与 Web | `browser` `computer` `web_search` `github` `generate_image` `tts` | 真实浏览器驱动；桌面控制；23 家搜索供应商 |
| 记忆与技能 | `checkpoint` `rewind` `retain` `recall` `reflect` `memory_edit` `learn` `manage_skill` | 记忆管理（可选后端 local/Hindsight/Mnemopi） |

**默认关闭的工具**（需在设置中开启）：`github`、`security_scan`、`generate_image`、`tts`、`checkpoint`、`rewind`、记忆类工具（需配置 `memory.backend`）。

**两个杀手锏特性：**

1. **Hashline 编辑**：`edit` 工具按**内容哈希锚点**定位编辑点，而不是行号——省 token 且防止编辑错位/文件损坏。
2. **时间旅行流规则（TTSR）**：流式输出中用正则匹配到危险/错误内容时，中止当前流、注入规则、自动重试，且**不占用上下文窗口**。

---

## 八、核心特性详解

### 8.1 LSP 接入每一次写入

每次 `write`/`edit` 后自动走 LSP：诊断错误、格式化；重命名文件时走 `workspace/willRenameFiles`，**自动更新所有 re-exports 和 barrel files**。这是"IDE wired in"的核心体现。

LSP 配置见 `docs/lsp-config.md`；`--no-lsp` 可关闭。

### 8.2 驱动真实调试器（DAP）

通过 `debug` 工具附加 **lldb（C/C++/Rust）/ dlv（Go）/ debugpy（Python）**，支持 28 种调试操作：断点、单步、查看变量、调用栈等。Agent 可以真的"调试"而不只是打印日志。

### 8.3 一等子代理（task）与 Agent Hub

`task` 工具可扇出隔离的 git worktree 子代理，各自独立上下文，返回 **schema 验证过的结构化对象**（不是自由文本）。Agent Hub（`docs/agent-hub.md`）统一管理这些子代理。

### 8.4 Vibe 模式（导演模式）⭐

`/vibe` 把当前会话变成**导演（director）**：自己不编辑代码，只保留 `read` 和 5 个 worker 控制工具，指挥一组**常驻后台 worker** 干活：

```
/vibe                              # 进入
/vibe 修复 packages/tui 里的 flaky 测试   # 进入并下达第一个指令
/vibe                              # 退出（杀死所有 worker）
```

两级 worker：

| 层级 | 内置代理 | 默认模型 | 用途 |
|------|---------|---------|------|
| `fast` | sonic | `@smol` | 机械执行、草稿、大批量任务 |
| `good` | task | `@task` | 设计、判断、审查 fast 的产出 |

控制工具：`vibe_spawn`（派生）、`vibe_send`（追加指令）、`vibe_wait`（等待）、`vibe_kill`（终止）、`vibe_list`（列出）。

**典型玩法**：把需求拆成多个独立工作流 → 每个流 spawn 一个常驻 worker → 并行跑 fast/good 混合梯队 → 导演用 `read` 验证产出 → `vibe_send` 纠偏。

### 8.5 顾问（Advisor）

`--advisor` 启用后，**第二个模型在独立上下文中被动审查每一轮**，发现问题时注入笔记——相当于自带 code review 副驾驶。

### 8.6 协作（Collab）

```
/collab    # 生成中继链接 + 二维码
```

其他人（或你自己的另一台设备）通过链接以**读写或只读**方式加入同一会话，跨设备协作调试。

### 8.7 GitHub 即文件系统

`read` 工具可直接读 GitHub 内部 URI：`pr://`（Pull Request）、`issue://`、`agent://`、`skill://`、`ssh://` 等 16 种 scheme。例如让 Agent 读某个 PR 的 diff 并做审查，无需 clone。

### 8.8 冲突解决

冲突文件以 `conflict://N` 路径暴露，编辑时可写 `@theirs` / `@ours` / `@base` 三方内容，Agent 可以语义化解决合并冲突。

### 8.9 omp commit（原子提交）

```bash
omp commit
```

自动分析改动 → **原子化拆分**成多个逻辑提交 → 依赖排序 → 生成并验证 commit 消息 → 更新 changelog。

### 8.10 /review（代码审查）

```
/review
```

生成带 **P0-P3 优先级**和 verdict 结论的审查报告。

### 8.11 代理管理记忆

`retain` / `learn` / `recall` 三个工具让 Agent 自主管理长期记忆；后端可选 local / Hindsight / Mnemopi（`docs/memory.md`）。

### 8.12 桌面与浏览器控制

- `eval` 里的 `browser.open()` 返回真实 tab handle，驱动你的 Chrome（配合 `omp browser-relay` 本地 CDP 中继）；
- `computer` 工具控制窗口、截图、原生输入、读取无障碍（AX）树。

---

## 九、斜杠命令与魔法关键字

### 9.1 常用斜杠命令（TUI 内）

| 命令 | 作用 |
|------|------|
| `/model` | 打开模型选择器 |
| `/login [provider]` | 登录提供商 |
| `/logout` | 登出 |
| `/vibe` | 进入/退出导演模式 |
| `/fresh` | 重置流状态（保留会话） |
| `/review` | 代码审查（P0-P3 报告） |
| `/collab` | 生成协作链接 |
| `/join` | 加入协作会话 |
| `/share` | 加密链接分享会话 |
| `/debug` | 打开调试工具 |

### 9.2 魔法关键字（Prompt 控制词）

在**普通提示词**（prose）中包含以下词即可触发对应行为（匹配规则见 `docs/magic-keywords.md`）：

| 关键字 | 作用 |
|--------|------|
| `ultrathink` | 最大深度思考 |
| `orchestrate` | 编排子代理/工作流 |
| `workflowz` | 工作流模式 |

### 9.3 快捷键

| 按键 | 作用 |
|------|------|
| `Ctrl+P` | 循环切换模型（`--models` 定义的列表） |

完整键位见 `docs/keybindings.md`。

---

## 十、配置文件体系

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

**配置读取优先**：进程环境变量 > CLI 参数覆盖 > `~/.omp/agent/config.yml` > `--config` 附加 overlay。

**继承其他工具配置**：OMP 可直接读取 Cursor、CLine、Codex、Copilot、Claude Code 等 8 种工具的已有配置文件，切换工具时无需重新配置。

**配置管理命令**：

```bash
omp config          # 管理配置项
omp models          # 列出/刷新可用模型
omp setup           # 引导式初始化 / 安装可选功能依赖
```

---

## 十一、典型使用场景实战

### 场景 1：日常编码（TUI）

```bash
cd my-project
omp "给 utils/date.ts 里的 formatDate 函数补上单元测试"
```

Agent 会：grep 定位 → read 读取 → 写测试文件 → LSP 诊断确认无错 → 运行测试验证。

### 场景 2：无头脚本（CI / 自动化）

```bash
# CI 里生成变更摘要
omp -p "总结最近一次 commit 的改动，输出为 markdown" > changelog.md

# JSON 事件流供下游程序消费
omp -p --mode json "检查 src/ 是否有未使用的导出" | jq '.[] | select(.type=="response")'
```

### 场景 3：原子化提交

```bash
git add -A
omp commit    # 自动拆分成多个逻辑提交并生成消息
```

### 场景 4：并行重构大任务（Vibe 模式）

```
/vibe 把这个 monorepo 从 jest 迁移到 vitest
```

导演自动拆分工作流：fast worker 批量改配置文件，good worker 处理 mock 策略等判断性工作，并行推进。

### 场景 5：接入公司内部模型网关

```yaml
# ~/.omp/agent/models.yml
providers:
  company-gw:
    baseUrl: http://10.0.0.5:8000/v1
    api: openai-completions
    apiKey: COMPANY_GW_KEY
    models:
      - id: qwen3-coder
        name: Qwen3 Coder
        contextWindow: 131072
        maxTokens: 32768
```

```bash
omp models company-gw     # 验证
omp --model qwen3-coder   # 使用
```

### 场景 6：在 Zed 编辑器中使用

```bash
omp acp   # 作为 ACP 服务器
```

Zed 设置中选择 OMP 作为 Agent 后端，读写直接经编辑器完成。

---

## 十二、SDET 视角：测试工程师如何用 OMP

结合测试开发（SDET）的日常工作，OMP 的这些能力特别有价值：

| 测试场景 | OMP 能力 | 做法 |
|---------|---------|------|
| 生成/维护接口测试用例 | `read` + `eval`（持久 Python） | 让 Agent 读源码/抓包文件，直接在持久 Python worker 里调 requests + pytest 生成并试跑用例 |
| 调试测试失败 | `debug` 工具（debugpy/DAP） | pytest 挂了让 Agent 附加真实调试器查变量、调用栈，而非人肉 print |
| 批量重构测试代码 | `/vibe` 导演模式 | fast worker 批量迁移断言风格，good worker 审查边界情况 |
| 代码审查/提测前自检 | `/review` | 生成 P0-P3 优先级问题清单，当作提测门禁 |
| UI 自动化探索 | `browser.open()` | Agent 驱动真实 Chrome 验证选择器是否有效，再固化到 Playwright 用例 |
| 语义化解决合并冲突 | `conflict://N` | 测试脚本多人协作冲突时用 @theirs/@ours 语义解决 |
| CI 里的智能检查 | `omp -p --mode json` | 无头模式嵌入流水线，输出结构化结果供下游解析 |
| 从 Claude Code 迁移 | `--from-claude` | 直接导入历史会话；继承原有配置，零成本切换 |

**与「AI 接口自动化 SKILL」思路的对照**：OMP 的 `manage_skill` 工具 + skills 发现机制（`--skills git-*,docker` 过滤）与 WorkBuddy/Claude Code 的 SKILL 体系理念相通——把领域工作流沉淀成可复用技能，Agent 按需加载。

---

## 十三、常见问题与故障排查

**Q1：模型列表里看不到某个模型？**
检查三件事：① provider 是否已登录（`/login`）或设置了环境变量；② 是否被 `disabledProviders` 禁用（禁用检查优先于凭据）；③ 自定义 provider 的 YAML 是否有语法错误（`omp models` 验证）。

**Q2：`.env` 里的 key 没生效？**
优先级是：已导出的进程环境变量 > `<cwd>/.env` > `~/.omp/agent/.env` > `~/.omp/.env` > `~/.env`。先检查 shell 里是否导出过旧 key。

**Q3：Windows 上需要 WSL 吗？**
不需要。OMP 是 Windows 原生实现，bash/grep/glob 都在进程内以 Rust 完成。

**Q4：怎么限制 Agent 别乱改文件？**
`--approval-mode write`（写操作需确认）或 `always-ask`；最保守可 `--tools read,grep` 只给只读工具。反向放开则用 `--yolo`。

**Q5：会话存在哪？怎么恢复？**
`~/.omp/agent/` 下；`omp -r` 打开会话选择器，`omp -c` 继续最近会话，`--fork` 可复制分支探索。

**Q6：如何控制成本？**
- 用模型角色把简单任务路由到 `smol`/`tiny`；
- `omp tiny-models` 下载本地小模型跑会话标题和记忆；
- `omp usage` 监控各账号用量与限额。

---

## 附录：关键文档索引

| 文档 | 内容 |
|------|------|
| [README](https://github.com/can1357/oh-my-pi) | 项目总览 |
| `docs/cli-reference.md` | CLI 完整参考 |
| `docs/providers.md` | 提供商认证大全 |
| `docs/models.md` | 模型解析与角色 |
| `docs/vibe-mode.md` | 导演模式详解 |
| `docs/approval-mode.md` | 审批模式 |
| `docs/skills.md` / `docs/extensions.md` | 技能与扩展 |
| `docs/mcp-config.md` | MCP 配置 |
| `docs/memory.md` | 记忆系统 |
| `docs/collab.md` | 协作会话 |
| `docs/session-operations-export-share-fork-resume.md` | 会话操作 |
| `docs/sdk.md` | Node SDK |
| `docs/rpc.md` | RPC 协议 |

> 📌 提示：OMP 迭代很快（当前 v18.x，2026-09），以官方仓库 README 与 docs/ 为最终准绳。
