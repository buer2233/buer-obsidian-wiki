# Pi 的 AI 设计经验

> 来源一：`D:\AI\pi\AGENTS.md`（Pi 项目官方开发规则，供 AI 协作时遵循）
> 来源二：`D:\AI\pi` 仓库源码精读（按《Pi 源码精读顺序清单》逐层读取：README / package.json / 各包 README / `packages/evals` 评测框架 / 安全护栏 Extension 示例 / `test.sh` / `SECURITY.md`）
> 提取范围：AI 编程经验 + Agent 设计经验 + Harness 测试经验
> 整理方式：按主题重组、简体中文翻译，关键英文术语保留原文对照，并补充「设计意图」「测试视角」解读
> 整理日期：2026-08-28

---

## 导读：这份文档为什么值得学

`AGENTS.md` 是 Pi 项目（Armin Ronacher 主导的极简 coding harness）写给在自己仓库里协作的 AI 看的「行为规范」。它本质上是一份**被精心设计的、约束 AI 行为的提示词工程成果**，也是理解「如何让 AI 稳定、安全、可靠地工作」的一手教材。

对测试开发工程师（SDET）来说，它有双重价值：

1. **作为「被约束对象」**：看 Pi 团队如何用规则约束 AI 的行为边界（不出错、不越权、不踩坑）。
2. **作为「约束手段」**：这些规则本身可以直接复用——你之后给自己的 AI 自动化项目写 `AGENTS.md` / `CLAUDE.md` 时，这些就是现成的、经过实战验证的条款。

---

## 第一部分：AI 编程经验

### 1.1 对话风格（Conversational Style）

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Keep answers short and concise | 回答保持简短、精炼 | 降低 token 消耗、减少噪音，让 AI 只说有用的话 |
| No emojis in commits/issues/PR/code | 提交、issue、PR 评论、代码中一律不用 emoji | 保证交付物专业、可被工具解析 |
| No fluff or cheerful filler text | 不用客套话或欢快的填充词（写 "Thanks @user" 而非 "Thanks so much @user!"） | 去掉无信息量的文字 |
| Technical prose only, be direct | 只写技术性文字，直接了当 | 提高信息密度 |
| Define unavoidable jargon before using it | 使用无法回避的行话前，先下定义 | 避免术语歧义，降低误读 |
| Explain as: problem → concrete example/trace → solution | 解释非平凡设计用「问题 → 具体例子/简短 trace → 解决方案」结构 | 强制逻辑闭环，杜绝空洞描述 |
| State why the solution is necessary, distinguish from optional complexity | 说明方案为何「必要」，并把它与「可选的复杂度」区分开 | 防止 AI 过度设计、堆砌不必要的复杂度 |
| Prefer concrete behavior over abstract summary | 偏好具体行为和小的示例，而非抽象总结 | 可验证、可复现 |
| Answer the question first, then edit | 用户提问时，先回答问题，再做编辑或执行命令 | 先对齐意图，再动手，避免跑偏 |
| Explicitly agree/disagree before saying what changed | 回应用户反馈时，先明确「同意/不同意」，再说改了什么 | 让 AI 先表态，避免无声地顺从或偏离 |

> 💡 **测试视角**：这一组规则本质是「AI 输出的可控性」设计——每一条都在压低 AI 的「幻觉空间」和「噪音空间」。做 AI 评测时，「是否客套」「是否先回答再动手」「是否区分必要与可选复杂度」都可以转成可打分的评测指标。

### 1.2 代码质量（Code Quality）

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Read files in full before wide-ranging changes | 做大范围改动、编辑未完整检查的文件、或做调查/审计前，必须完整读取文件；不要依赖搜索片段 | 防止 AI 基于片段误判上下文，是「可信改动」的前提 |
| No `any` unless absolutely necessary | 除非绝对必要，禁止使用 `any` | 保住类型安全，TypeScript 项目的底线 |
| Inline single-line helpers with one call site | 只有一个调用点的单行辅助函数直接内联 | 避免无意义的抽象 |
| Check node_modules for external API types | 查询 node_modules 里的外部 API 类型，不要靠猜 | 写调用代码必须核对真实类型签名 |
| No inline imports; top-level imports only | 禁止内联导入（`await import()`、`import("pkg").Type` 等动态导入），只用顶层导入 | 规避运行时模块加载的不确定性 |
| Never downgrade code to fix type errors; upgrade the dep | 修复过时依赖导致的类型错误时，绝不降级/删减代码，而是升级依赖 | 保持代码向前演进，不向旧依赖妥协 |
| Use only erasable TypeScript syntax | 只用可擦除的 TS 语法（Node strip-only 模式），不用 parameter properties、`enum`、`namespace`、`import =` 等需要 JS 发射的语法 | 简化构建链路，减少运行时差异 |
| Always ask before removing intentional code | 删除看似「有意的」功能/代码前，必须先询问 | 核心安全护栏：防止 AI 误删有意图的实现 |
| Do not preserve backward compatibility unless asked | 除非用户要求，不保留向后兼容 | 不做无谓的历史包袱 |
| Never hardcode key checks; add to DEFAULT configs | 不硬编码按键判断（如 `matchesKey(keyData, "ctrl+x")`），要加到 `DEFAULT_EDITOR_KEYBINDINGS` / `DEFAULT_APP_KEYBINDINGS` 让它可配置 | 把「魔法值」变成「可配置项」，这是可测试性设计 |
| Never modify generated files; update generator then regenerate | 不直接改 `models.generated.ts` 这类生成文件，改生成脚本后重新生成 | 保证生成物与生成器一致，避免手工修改被覆盖 |

> 💡 **测试视角**：「删除故意代码前先询问」「不硬编码而走配置」这两条，是**安全测试与可配置性测试**的直接体现——前者防止越权破坏，后者让行为可通过配置注入、可被自动化遍历。

### 1.3 命令执行规范（Commands）

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| After code changes: `npm run check`, fix all errors/warnings/infos | 代码改动后运行 `npm run check`（完整输出、不截断），提交前修完所有错误/警告/信息 | 质量门禁：不留任何 lint/type 残留 |
| Never run build/test unless requested | 未经用户要求，不运行 `npm run build` / `npm test` | 省钱省时，避免无关的耗时操作 |
| Never run full vitest directly (contains e2e) | 绝不直接跑完整 vitest 套件（含需要 endpoint/auth 环境变量才会激活的 e2e）；非 e2e 用 `./test.sh` | **测试分层**：长/外部依赖的测试必须与普通测试隔离 |
| If you create/modify a test file, run it and iterate until passing | 新建/修改测试文件后，必须跑它，并迭代直到通过 | 测试代码也要自证可用 |
| Put regressions under `.../regressions/` named `<issue>-<slug>.test.ts` | 针对具体 issue 的回归测试放到 `regressions/` 目录，命名 `<issue号>-<简短slug>.test.ts` | 回归用例可追溯，与 issue 一一对应 |
| Write ad-hoc scripts to temp files; don't embed in bash | 临时脚本写到临时文件（如 `/tmp`），跑完删除；不要把多行脚本塞进 bash 命令里 | 保持命令干净、可审查 |
| Never commit unless the user asks | 未经用户要求，绝不提交 | 提交权始终在用户手中 |

> 💡 **测试视角**：「完整 vitest 含 e2e、普通测试走 `./test.sh`」是**测试环境隔离**的经典做法——有外部依赖/凭证的用例必须显式隔离，否则 CI 跑出「环境相关」的假失败，这是 test flakiness 治理的第一课。

---

## 第二部分：Agent 设计经验

### 2.1 多 Agent 并行协作的 Git 护栏（最精华的一段）

Pi 官方明确说明：**同一个工作目录下可能同时跑着多个 pi 会话，各自改不同的文件**。为此制定了一套 Git 协作护栏，保证多个 AI 不互相踩踏。

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Only commit files YOU changed in THIS session | 只提交「你在本次会话中」改过的文件 | 明确所有权边界 |
| Stage explicit paths, never `git add -A` / `git add .` | 用显式路径 `git add <path1> <path2>` 暂存，绝不 `git add -A` / `.` | 防止把别的会话改动卷进来 |
| Run `git status` and verify before committing | 提交前跑 `git status`，确认只暂存了自己的文件 | 提交前自查 |
| Never run `git reset --hard` / `git checkout .` / `git clean -fd` / `git stash` / `git commit --no-verify` | 严禁 reset --hard、checkout .、clean -fd、stash、`commit --no-verify` | 这些会销毁其他 Agent 的工作或绕过检查 |
| Rebase 冲突：只解决自己改过的文件；冲突在未改文件里则中止并询问用户 | 只处理自己的冲突，别碰别人的 | 冲突处理不越界 |
| Never force push | 绝不强推 | 保护远程历史 |

> 💡 **核心洞察**：这是「多 Agent 共享状态」场景下最实用的护栏设计。本质是**给每个 AI 划清「可写边界」**：只动自己的文件、显式暂存、禁止破坏性命令。当你日后做「多个 AI Agent 协同测试」或多 worker 自动化时，这套规则可以直接套用到你的并发测试框架里，防止竞态和相互覆盖。

### 2.2 安全与授权边界

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Treat dep/lockfile changes as reviewed code | 把依赖和 lockfile 的改动当作「需审查的代码」 | 供应链安全：依赖变更不是小事 |
| Direct external deps pinned to exact versions | 直接外部依赖锁定精确版本 | 可复现构建，防依赖漂移 |
| Hydrate with `npm install --ignore-scripts`; clean with `npm ci --ignore-scripts` | 本地用 `--ignore-scripts` 安装；CI 式用 `npm ci --ignore-scripts`；非用户要求不跑生命周期脚本 | 阻断依赖 install 脚本的潜在执行风险 |
| New deps with lifecycle scripts need review + explicit allowlist | 带生命周期脚本的新依赖需审查，并在脚本里显式加入 allowlist；绝不静默添加 | 供应链攻击面控制 |
| Pre-commit blocks lockfile commits unless `PI_ALLOW_LOCKFILE_CHANGE=1` | pre-commit 阻止 lockfile 提交，除非显式设置环境变量放行 | 用钩子强制把关 |

> 💡 **核心洞察**：这是「最小权限 + 显式放行」的安全设计。对 AI 代理尤其重要——AI 可能自动引入依赖、自动跑 install，必须用「默认拒绝、显式 allowlist」的环境变量和 hook 把风险关进笼子。

---

## 第三部分：Harness 测试经验

### 3.1 用 faux provider 做隔离测试（最值的技巧）

原文核心要求：测试 `packages/coding-agent/test/suite/` 时，**使用 `test/suite/harness.ts` + faux provider（仿制的模型提供商），绝不碰真实 provider API、密钥或付费 token**。

| 要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Use harness.ts + faux provider | 用 harness 脚手架 + 仿制 provider 做测试 | 把 LLM 替换为确定性的假实现，测试不依赖网络/费用/模型 |
| No real provider APIs, keys, or paid tokens | 不用真实接口、密钥、付费 token | 降低成本 + 消除外部依赖导致的 flaky |

> 💡 **核心洞察**：这是测试 LLM 应用的**黄金手法**——「fake provider / mock model」模式。测 Agent 逻辑（工具调用、状态流转、会话管理）时，把一个**行为可预测的假模型**注入进去，就能把「模型不确定性」从测试里剥离，只专注验证 harness 自身逻辑。这与你测接口时用 mock server 是同一个道理。

### 3.2 用 tmux 测交互式 TUI

原文给了一套在受控终端里驱动 TUI 的标准流程：

```bash
tmux new-session -d -s pi-test -x 80 -y 24   # 建一个 80x24 的受控终端
tmux send-keys -t pi-test "./pi-test.sh" Enter
sleep 3 && tmux capture-pane -t pi-test -p    # 启动后截图
tmux send-keys -t pi-test "你的提示词" Enter
tmux send-keys -t pi-test Escape              # 特殊键（C-o 表示 ctrl+o 等）
tmux kill-session -t pi-test
```

> 💡 **核心洞察**：交互式 TUI / CLI 的自动化测试，标准套路就是 **tmux 建会话 → send-keys 模拟输入 → capture-pane 截图断言 → 销毁会话**。这与你做终端 UI 测试（比如测某个 CLI 工具的交互）完全通用。

### 3.3 回归测试的落位规范

| 要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Put issue-specific regressions under `regressions/` | 按 issue 的回归测试统一放 `packages/coding-agent/test/suite/regressions/` | 集中管理，一类问题一个文件 |
| Name them `<issue-number>-<short-slug>.test.ts` | 命名 `<issue号>-<简短slug>.test.ts` | 文件名即溯源信息 |

> 💡 **核心洞察**：让回归用例与缺陷号强绑定，是最朴素的「缺陷闭环」工程实践——看到测试文件名就知道它防的是哪个 bug。

### 3.4 发布前的 smoke test（构建产物验证）

原文要求发布前在 **仓库外部** 构建未发布版本并做冒烟测试，防止解析到 workspace 内的文件：

```bash
npm run release:local -- --out /tmp/pi-local-release --force
cd /tmp
/tmp/pi-local-release/node/pi --help
/tmp/pi-local-release/node/pi --version
/tmp/pi-local-release/node/pi --list-models
/tmp/pi-local-release/node/pi -p "Say exactly: ok"
/tmp/pi-local-release/node/pi          # 交互模式（在 tmux 里跑，等模型回复）
```

| 要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Build & smoke test from OUTSIDE the repo | 在仓库外构建和冒烟测试（`cd /tmp`） | 确保测的是「真实发布产物」，而非 workspace 内源码的直接解析 |
| Verify Node AND Bun startup, model/account listing, interactive startup, real prompt | 同时验证 Node 和 Bun 两个运行时、模型/账号列表、交互式启动、至少一次真实 prompt | 覆盖多运行时 + 关键路径 |
| Failures are release blockers unless user accepts risk | 失败即阻断发布，除非用户显式接受风险 | 质量门禁不可绕过 |

> 💡 **核心洞察**：「在仓库外测产物」是**环境隔离测试**的进阶——避免「workspace 内的 path 解析 / 软链」掩盖真实的部署问题。两个运行时的双验证，则体现了「跨运行时兼容性测试」的意识。

---

## 第四部分：源码精读——从架构学到「Agent 如何被测」

> 这一部分来自对 `D:\AI\pi` 仓库的逐层精读（按《Pi 源码精读顺序清单》的 L0-L9）。与前三部分「AGENTS.md 规则」不同，这里提炼的是**代码层面真正落地了的设计经验**——尤其是对测试工程师极其珍贵的「官方 Agent 评测框架」和「安全护栏示例」。

### 4.1 架构总览：分层如此干净，是为了「各层可独立测」

Pi 的 monorepo 用 npm workspaces 拆成 10 个包，职责边界极清晰：

| 层 | 包名 | 一句话定位 | 测试视角 |
|----|------|-----------|---------|
| 协议层 | `protocol` | 运行时中立的 schema / CBOR 编码 / 字节流分帧 | 事件契约，可观测性源头 |
| 模型层 | `ai` | 统一多提供商 LLM API + 认证 + token/成本追踪 | 模型适配，可做跨模型对比 |
| 运行时层 | `agent` | 有状态 Agent，工具执行 + 事件流 | **被测对象核心** |
| 服务端 | `server` | 会话服务 + 传输监听器（RPC） | 进程级驱动 |
| 客户端 | `client` | 传输中立的远程会话客户端 | 远程/多进程场景 |
| 交互层 | `coding-agent` | 交互式 CLI 主包（用户入口） | 端到端入口 |
| 评测层 | `evals` | 官方行为评测框架 | **SDET 金矿** |
| UI 层 | `tui` | 差分渲染终端 UI | UI 层 |
| 遥测 | `telemetry` | 供应商中立遥测契约 | 可观测性 |
| 存储 | `session-backends/sqlite-node` | SQLite 会话存储 | 会话持久化 |

> 💡 **核心洞察**：把一个 Agent 拆成「协议 / 模型 / 运行时 / UI / 存储」五个正交层，是**为了各层能独立测试**——协议层测编码解码、模型层可用假模型、运行时层可注入 mock 工具、UI 层可 tmux 驱动。这正是「可测性设计（design for testability）」在大型 TS 项目里的范本。你搭自己的测试框架时，也可以用同样的分层思路。

**工程基础配置的两个细节**（来自 `tsconfig.base.json` / `vitest.base.ts`）：

1. `erasableSyntaxOnly: true` —— 强制只用「可擦除 TS 语法」（不用 `enum`、`namespace`、`import=` 等需要 JS 发射的语法），让源码直接用 Node strip-only 模式运行，构建链路里少了「类型代码转 JS」这一步，运行时行为与源码完全一致，调试更可信。
2. `vitest.base.ts` 用 **alias 把包名映射到源码**（`@earendil-works/pi-agent-core → packages/agent/src/index.ts`），使测试直接跑源码而非编译产物，迭代更快。

### 4.2 运行时层（agent 包）：Agent Loop 的事件化设计

`packages/agent/README.md` 把 Agent 的一次运行拆成一串**事件流**，这是理解「如何测一个 Agent」的关键：

```
prompt("Hello")
├─ agent_start
├─ turn_start                              ← 一轮 = 一次 LLM 调用 + 若干工具执行
├─ message_start/end  { userMessage }
├─ message_start      { assistantMessage }  ← LLM 开始回复
├─ message_update × N                       ← 流式增量
├─ message_end
├─ tool_execution_start  { toolCallId, toolName, args }   ← 工具被调用
├─ tool_execution_update { partialResult }                ← 工具流式进度（可选）
├─ tool_execution_end    { toolCallId, result }
├─ message_start/end  { toolResultMessage }
├─ turn_end           { message, toolResults }
│
├─ turn_start                               ← 下一轮（LLM 消化工具结果后继续）
│  ...
└─ agent_end           { messages: [...] }
```

**三个对测试工程师最有价值的细节：**

1. **`AgentMessage` 与 LLM Message 分层**：Agent 内部用一个更灵活的 `AgentMessage`（可含 UI-only、自定义类型），真正喂给 LLM 前经过两道转换 `transformContext()`（裁剪/注入上下文）→ `convertToLlm()`（过滤 UI 消息、转换自定义类型）。**这给你一个天然的「测试注入点」**——想测「上下文裁剪是否正确」，只需断言 `convertToLlm` 的输出。

2. **并行 vs 顺序工具执行**：`toolExecution` 可设 `parallel`（默认，preflight 后并发执行）或 `sequential`（逐个执行）。单工具还能用 `executionMode` 覆盖全局设置；只要批次里有一个 `sequential` 工具，整批回退为顺序执行。**这是「受控并发」测试的好素材**——可以测同一批工具在两种模式下的完成顺序与竞态。

3. **`beforeToolCall` / `afterToolCall` 钩子 + `terminate` 语义**：`beforeToolCall` 在参数校验后执行，可 `block`（拦截并附原因）；任何工具结果返回 `terminate: true` 可提示「跳过后续自动 LLM 调用」。**这直接就是「工具调用断言/拦截」的原生支持**，写安全测试时无需额外 mock 框架。

> 💡 **核心洞察**：Pi 把一个「黑盒 Agent」做成了「全事件可见 + 可挂钩子」的白盒。你在测自己的 AI 自动化 Agent 时，最该仿照的就是这两点——**暴露事件流（可观测）+ 留出钩子点（可控制）**。

### 4.3 协议层（protocol 包）：从「事件流」到「可断言协议」

`protocol` 包定义了运行时中立的 wire 协议，几个利于测试的设计：

| 要点 | 说明 | 测试价值 |
|------|------|---------|
| 帧格式固定 | `[4字节大端长度][CBOR payload]`，进程间传输可任意分包/合并 | 解码器必须抗分包，是标准的协议健壮性测试点 |
| 校验严格 | 未知字段一律拒绝、顶层 undefined/稀疏数组/不安全数字/嵌套过深都报 `ProtocolValidationError` | 非法输入是被明确拒绝的，容易写边界用例 |
| 显式限额 | frame 默认 16MiB、数组/映射 100 万元素、嵌套 64 层，可配置 | 限额本身就是「DoS 防护」测试点 |
| **权威快照 vs 瞬时事件** | 进程事件是瞬时的 UI 提示，**不得**归约为权威状态；只有 server snapshot 才算数 | **这是分布式/异步系统的金科玉律**：区分「事实」与「提示」，避免用临时事件推断最终状态 |

> 💡 **核心洞察**：`progress events are transient ... must not be reduced into authoritative state` 这一条，翻译成测试语言就是——**别用中间态断言最终结果，只信快照**。这与你测异步任务时「等待稳定状态再断言」是同一个道理，Pi 把它写进了协议规范。

### 4.4 模型层（ai 包）：faux provider 是「去模型化测试」的官方实现

前三部分提到「用假的模型做测试」，`ai` 包给出了**完整的官方实现**：

```typescript
const faux = fauxProvider({ tokensPerSecond: 50 });   // 可指定出字速度
faux.setResponses([
  fauxAssistantMessage([
    fauxThinking("Need to inspect package metadata first."),
    fauxToolCall("echo", { text: "package.json" }),
  ], { stopReason: "toolUse" }),
]);
// ... 然后 models.stream(model, context) 拿到确定性的脚本化响应
```

**关键能力**：

- **脚本化响应队列**：`faux.setResponses([...])` 替换队列、`faux.appendResponses([...])` 追加。响应按请求顺序出队。
- **队列耗尽自动报错**：`errorMessage: "No more faux responses queued"`——这样测试不会「默默拿到空响应」而假通过。
- **可观测状态**：`faux.state.callCount`、`faux.getPendingResponseCount()`，可直接断言「模型被调用了几次」。
- **多模型切换**：一个 faux provider 可建多个带 `reasoning` 标记的假模型，测模型切换逻辑。
- **自动模拟 token 与缓存**：约 1 token / 4 字符估算，带 `sessionId` 时自动模拟 prompt cache 读写。

> 💡 **核心洞察**：faux provider 就是「mock model」的教科书级实现。它做到了三件事：**确定性**（脚本化）、**可观测**（callCount/pendingCount）、**防假通过**（队列耗尽即报错）。你测任何「依赖 LLM 输出的代码」时，照这个模式写一个 fake model 即可，完全不必为每次测试付真金白银、也不必担心模型输出的随机性导致 flaky。

**附：跨 provider 切换的兼容性设计** ——同一会话从 Claude 切到 GPT 再到 Gemini 时，库会自动把「别家的 thinking 块」转成 `<thinking>` 标签文本、保留 tool call 与常规文本。这既是「模型中立」的实现原理，也是**「跨模型消息兼容性」测试**的重点对象。

### 4.5 评测层（evals 包）：官方把「如何评测一个 Agent」写成代码

这是全仓库对测试工程师**价值最高**的部分，把上一版清单里的「金矿」落到实处：

**① 核心：`createPiCodingAgentHarness`（被测对象适配器）**

`packages/evals/src/pi-harness.ts` 做了一件关键的事——**把一个真实的 `AgentSession` 包装成 `vitest-evals` 的 `Harness`**，并在「隔离临时目录」里运行：

- 用 `mkdtemp` 造独立的 `workspace/` 和 `agent/` 目录，跑完自动 `rm` 清理。
- 隔离会话**默认不带任何 Extension**（启动时断言 `extensionPaths.length === 0`），保证评测环境干净可控。
- 支持 `noTools`（禁工具）、`transformSystemPrompt`（改写系统提示）、`output`（把最终响应 + session 转成 JSON-safe 的结果，暴露 `getActiveToolNames()`、`extensionErrors` 等）。
- 输入支持「单条 prompt」或「多步序列」`[{type:"prompt"}, {type:"reload"}, ...]`。
- 自动收集 `usage`：input/output/total tokens、toolCalls、cache read/write、estimatedCostUsd、耗时。

```typescript
const harness = createPiCodingAgentHarness({ noTools: "all" });
describeEval("Pi smoke", { harness }, (it) => {
  it("answers a factual question", async ({ run }) => {
    const result = await run("What is the capital of France? Reply with only the city name.");
    expect(result.output.trim()).toBe("Paris");
    expect(result.errors).toEqual([]);
    expect(result.usage.totalTokens).toBeGreaterThan(0);
  });
});
```

**② 对比评测：`evalHarnessTable`（A/B 测试方法论）**

`harness-table.ts` + `summary.ts` 实现了一套**严谨的 baseline vs candidate 对比评测**：

- 同一输入跑多个 harness，可设 `repetitions`（重复次数）降低随机性。
- 用 `createJudge(...)` 打分（确定性规则或模型打分），`score >= 1` 记作通过。
- 汇总时算 **正确率提升（pass-rate lift，百分点）**、**token / 延迟 / 成本成对增量（paired delta）**、baseline/candidate 各自胜出次数、平局数。
- **关键工程细节**：`judgeThreshold: null` 让「低分」只是观测值而非让测试挂掉；硬断言只用于「套件不变量/基础设施契约」，不用 `expect.soft` 当评分机制。这保证了「评测失败」和「测试失败」语义分离。

> 💡 **核心洞察**：Pi 的 evals 框架回答了一个面试高频题——**「你怎么定量对比两个 Agent / 两个 prompt / 两个工具的优劣？」** 标准答案就是这套：`harness`（把被测对象包装成可跑单元）+ `judge`（打分器）+ `repetitions`（重复消随机）+ `pass-rate lift + paired deltas`（对比指标）。你能复述这套，就证明你的 AI 评测能力是「拆过源码」而非「背名词」。

**③ 一个绝佳的实战案例：Extensions 评测（`extensions.eval.ts`）**

它示范了「如何评测一个复杂工作流」——让 Agent 走「创建 Extension → reload → 使用 Extension」三段式，然后用一个 `ExtensionAuthoringJudge` 检查 6 个失败点（有没有正确 import、有没有用旧包、loader 有无报错、是否注册了 `hello` 工具、工具是否真被调用且返回正确、最终回复是否精确匹配）。**这就是把「验收标准」转成「可打分 judge」的活教材。**

### 4.6 安全护栏示例（6 个可直接二次开发的 Extension）

`packages/coding-agent/examples/extensions/` 里有几十个示例，其中这些对测试/安全方向直接相关：

| 示例 | 做了什么 | 对测试工程师的价值 |
|------|---------|-------------------|
| `permission-gate.ts` | 拦截危险 bash 命令（`rm -rf`/`sudo`/`chmod 777`），UI 确认否则 block | **命令级安全护栏**的完整实现，正则即测试点 |
| `protected-paths.ts` | 阻止对 `.env`/`.git/`/`node_modules/` 的 write/edit | **路径保护**，防误改敏感文件 |
| `confirm-destructive.ts` | 清会话/切换/fork 前二次确认，用 `before_*` 事件取消 | **事件级拦截**，`{cancel: true}` 语义清晰 |
| `dirty-repo-guard.ts` | 有未提交改动时，切换会话/fork 前强提醒 | 防止上下文切换丢失工作 |
| `git-checkpoint.ts` | 每轮 `git stash create` 存档，fork 时可回滚代码 | 状态快照 + 回滚，测「分支/回滚」逻辑的上佳素材 |
| `tool-override.ts` | **重写内置 `read` 工具**：记日志 + 拦截敏感路径 + 委托原实现 | **「工具覆盖」是测试注入的核心手段**，拦截读也能做审计 |

> 💡 **核心洞察**：这一组示例说明一个深刻的点——**Pi 把「权限系统」故意不内置，却把「如何用 Extension 自建权限系统」示范得清清楚楚**。对测试工程师来说，`permission-gate` 的「危险命令正则」、`protected-paths` 的「敏感路径清单」、`tool-override` 的「拦截 + 审计」都是你设计 **Agent 安全测试用例** 的直接素材，抄过来就能用。

### 4.7 隔离与安全边界的顶层设计

**`test.sh` 的隔离测试环境**（非常有启发）：

- 用 `mktemp -d` 建独立临时根，并写入 `.pi-test-owned` 标记文件；cleanup 时**只删带标记的目录**，防止误删。
- 用 `env -i` 从**空环境**启动，只白名单放行必要变量（PATH/HOME/TMPDIR/XDG 等），并强制 `LANG=C`、`TZ=UTC`、`GIT_ASKPASS=false`（禁止 git 交互提示）。
- 明确「无 API Key 时跑测试」，依赖 LLM 的用例被跳过。

> 💡 **核心洞察**：这是「测试环境隔离」的三板斧——**① 独立根目录 + 显式所有权标记（安全删除）② 空环境白名单启动（杜绝宿主环境污染）③ 确定性时区/语言/禁止交互（消除随机性）**。你搭 CI 或自动化测试环境时，这三条能直接解决「测试间串扰」和「环境依赖导致的 flaky」两大顽疾。

**`SECURITY.md` 的安全边界模型**（极具测试价值）：

- Pi **明确声明不内置沙箱**，信任边界 = 运行它的用户账户本身。
- **Out of Scope 列表值得细读**：local code execution、prompt injection、恶意模型输出、用户主动安装的恶意 extension/skill、伪造的 MITM 代理……都被明确排除在「漏洞」之外。
- 一个关键判断标准：**只有「demonstrate how Pi grants that write access / crosses privilege boundary」才算漏洞**；事先拿到本地写权限后写入 `AGENTS.md`/`models.json` 来注入提示，不算漏洞。

> 💡 **核心洞察**：`SECURITY.md` 本质上定义了一个 Agent 工具的**威胁模型（threat model）**——哪些算安全边界、哪些不算。这是安全测试的「范围说明书」范本。它带来的直接启示：**做 Agent 安全测试前，必须先明确「信任边界在哪」**；否则你会把「本来就该被信任的用户操作」误判成漏洞，测试结论就失去意义。

---

## 总结：这份文档留给我们最该带走的三条经验

1. **AI 输出要「可控」**：对话风格、代码质量、命令规范三层规则，本质都是在压 AI 的幻觉与噪音空间——这既是「约束 AI」的提示词工程，也是「评测 AI」的指标来源。
2. **多 Agent 要「划边界」**：只提交自己改的文件、显式暂存、禁用破坏性命令——并发协作的安全护栏，可复用到多 worker 自动化测试。
3. **测 Agent 要「去模型化」**：用 faux provider 注入假模型，把「模型不确定性」从测试里剥离，只验证 harness 自身逻辑——这是 AI 测试的黄金手法。

如果再加两条从源码里提炼的「升级版」经验：

4. **测 Agent 要「可观测 + 可挂钩」**：像 Pi 的 `agent` 包那样，把 Agent 做成事件流可见、工具调用可 `beforeToolCall/afterToolCall` 拦截——可观测性和可控制性决定了一个 Agent 可测性的上限。
5. **对比评测有标准方法**：`harness`（适配）+ `judge`（打分）+ `repetitions`（消随机）+ `pass-rate lift / paired deltas`（对比指标），这是 Pi 官方 `evals` 框架给出的、可复述的 AI 评测答案。

> 注：本文前四部分为对 `D:\AI\pi` 仓库（`AGENTS.md` + 源码精读）的提炼与翻译，聚焦「AI 编程 / Agent 设计 / Harness / 评测」四大主题。原文的 Changelog 维护、Issue/PR 流程、纯发布脚本等流程性内容已按主题取舍精简，完整规则请查阅原文件。