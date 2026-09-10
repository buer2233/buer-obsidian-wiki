# OMP 的 AI 设计经验

> 来源一：GitHub 仓库 [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) 的 `README.md`（项目定位与 21 项特性设计说明）
> 来源二：同仓库根目录 `AGENTS.md`（Development Rules，写给在本仓库协作的 AI 的行为规范）
> 来源三：本机实战安装与配置过程（v18.1.9，Windows 原生，LSP 配置实战经验）
> 提取范围：AI 编程经验 + Agent 架构设计经验 + 测试/质量工程经验
> 整理方式：按主题重组、简体中文翻译，关键英文术语保留原文对照，并补充「设计意图」「测试视角」解读
> 整理日期：2026-09-05

---

## 导读：这份文档为什么值得学

OMP（Oh My Pi）是 Mario Zechner 的 Pi 项目的「重装 fork」——Pi 走极简路线，OMP 的口号是 **"The Pi you love, with batteries included"**（你所爱的 Pi，但开箱即用）。它有两份截然不同的学习素材：

1. **README**：一份罕见的「设计决策说明书」。绝大多数开源项目的 README 只讲功能，OMP 的 README 在讲**为什么这样设计**——为什么用 Rust、为什么消灭 fork/exec、为什么按内容哈希做编辑。每一条都是可复用的 Agent 设计经验。
2. **`AGENTS.md`**：与 Pi 的 `AGENTS.md` 一脉相承的「AI 协作行为规范」，但 OMP 的版本在**测试规范**上走得更远——它用整整一章定义「什么是好测试、什么是坏测试」，几乎是一份可直接引用的测试代码评审清单。

对测试开发工程师（SDET）来说，它有双重价值：

1. **作为「被约束对象」**：看 OMP 团队如何用规则约束 AI 的行为边界（不硬编码、不手改生成文件、不写假测试）。
2. **作为「架构范本」**：OMP 是目前把「IDE 能力内置进 Agent」做得最彻底的开源实现——LSP 接入每次写入、DAP 驱动真实调试器、子代理返回 schema 验证的结构化结果，这些设计直接回答了「如何让 Agent 的产出可信」这个测试工程师最关心的问题。

---

## 第一部分：AI 编程经验（来自 AGENTS.md）

### 1.1 对话与上下文规范

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Default focus is `packages/coding-agent/` | 除非特别指定，所有工作默认聚焦 `coding-agent` 包 | 消除「改错包」的歧义，给 AI 一个默认作用域 |
| "agent" means the CLI implementation, not the current assistant session | 用户说 "agent" 时指 CLI 工具的实现，不是当前助手会话 | 术语消歧：防止 AI 把「讨论对象」和「自己」搞混 |
| Never comment on GitHub / never create issues unless told | 除非用户明确告知，绝不在 GitHub 上评论、绝不创建 issue | 外部副作用最小化：AI 的「写外部世界」权限默认关闭 |
| Code imports catalog values from `@oh-my-pi/pi-catalog/<module>`, never from `pi-ai` | catalog 值只许从 `pi-catalog` 导入，`pi-ai` 只允许类型导入 | 用导入路径强制分层，防止依赖方向腐化 |

> 💡 **测试视角**：「默认作用域 + 术语消歧 + 外部写权限默认关闭」是 AI 行为可控性的三条基线。评测一个 Agent 时，「是否越界评论外部系统」「是否混淆讨论对象与自己」都可以转成可打分的评测指标。

### 1.2 代码质量（比 Pi 更严格的类型与结构纪律）

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| No `any` / no `ReturnType<>` | 禁止 `any`，禁止 `ReturnType<>`，必须写真类型名 | 类型即文档，`ReturnType<>` 隐藏了真实契约 |
| No inline imports, top-level only | 禁止动态导入，只用顶层导入 | 消除运行时模块加载的不确定性 |
| ES `#private` fields; no `private`/`protected` keywords | 类私有字段用 ES 原生 `#private`，禁用 TS 访问修饰符 | 运行时真实私有（TS 修饰符编译后形同虚设） |
| `Promise.withResolvers()` over `new Promise(...)` | 用标准 API 替代手写 Promise 包装 | 减少样板代码和回调错误 |
| **Never construct prompts in code** | **绝不在代码里构建 prompt**（禁内联字符串/模板拼接）；prompt 必须放静态 `.md` 文件，用 Handlebars 注入动态内容，`import content from "./prompt.md" with { type: "text" }` 导入 | **这是最具远见的一条**：prompt 即资产，独立于代码可审查、可 diff、可版本化 |
| Check central utils before writing helpers; grep first | 写 helper 前先查中央工具库、先 grep；「两个都能用的实现本身就是 bug」 | 杜绝重复实现，单一事实来源 |
| Extend, don't fork central helpers | 缺能力时扩展中央 helper，不在本地 fork 逻辑 | 防止逻辑碎片化，修复只改一处 |
| `utils/git.ts` is the ONLY legal way to run git | git/jj 只能走中央封装，绝不手搓 `` $` `` 或 `Bun.spawn` | 唯一执行通道：审计、注入防护、跨平台兼容只需管一个点 |

> 💡 **测试视角**：「prompt 不进代码」这条对测试人极其重要——它意味着 **prompt 变更可以像接口变更一样被追踪和回归**。你的 AI 接口自动化 SKILL 体系如果也把 prompt 抽成独立文件，就能做「prompt diff 触发的评测回归」。「唯一执行通道」则是可测性设计的经典手法：所有 git 调用过一个收口函数，测试时只需 mock 这一个点。

### 1.3 模型/提供商策略：禁止硬编码（KDL 强制）

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Never hardcode model/provider conditional logic in TypeScript | 绝不在 TS 里硬编码模型条件策略（禁 `id.includes("claude")`、禁模型名正则、禁 per-model 查找表） | 模型策略散落代码里必然腐化，每加一个模型都是地雷 |
| All rules live in `packages/catalog/src/compat/rules/` KDL tree, compiled to `rules.json` | 策略全部放 KDL 规则树，构建期编译成 `rules.json` | 声明式规则 + 构建期固化：可审查、可测试、运行期零解析成本 |
| TS may only branch on structured facts from `classifyModel()` | TS 只允许基于 `classifyModel()` 返回的结构化事实（class/family/revision）分支 | 把「模型是什么」收敛为一个分类器，其余代码只见事实不见字符串 |
| Ambiguous overlap → fix with KDL `priority=` | 规则重叠报 `AmbiguousOverlapError`，用 KDL 优先级解决 | 冲突在构建期暴露，而不是运行期行为漂移 |

> 💡 **核心洞察**：60+ 提供商、几百个模型的兼容性适配，OMP 的选择是**把策略数据化（KDL）+ 构建期编译 + 结构化分类**。这与你管理大量接口测试用例的思路完全同构：用例数据（KDL/JSON）与执行引擎（TS）分离，新增模型/接口不动引擎。这也直接回答了「你们的框架怎么适配新模型？」这个面试高频题。

### 1.4 生成文件纪律

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Never edit `models.json` / `rules.json` directly | 绝不手改生成文件 | 手工修改会被下次生成覆盖，且源与产物不一致 |
| Change the source (KDL tree / CATALOG_PROVIDERS / mappers), regenerate, commit both | 改源 → 重新生成（`bun run gen:compat`）→ 一起提交 | 源与产物同 commit，保证可回溯 |
| Regression tests target rules/descriptors/mappers, not the JSON | 回归测试针对规则与映射器，不测生成的 JSON 本体 | 测「生成逻辑」而非「生成结果」——结果由逻辑保证 |

> 💡 **测试视角**：「测生成器不测生成物」是测试设计的重要原则——和「测 schema 不测逐条数据」「测模板不测渲染结果」是同一个思想。

### 1.5 命令执行规范（Bun 优先 + 运行时纪律）

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Never spawn a shell when a proper API exists | 有正规 API 就绝不 spawn shell（如用 `mkdirSync` 而非 `` $`mkdir -p` ``） | 少一层进程 = 少一层注入面、少一份跨平台差异 |
| NEVER commit unless the user asks | 未经用户要求，绝不提交 | 提交权始终在用户手中 |
| Never use `tsc`/`npx tsc`; always `bun check` | 禁用裸 tsc，统一走 `bun check` | 检查入口唯一，避免「本地过了 CI 挂了」的双标 |
| Never run `cargo test` directly; use `bun run test:rs` | Rust 测试统一走 `bun run test:rs`（nextest + doc test） | 同上：测试入口唯一 |
| Async code: no `existsSync`/`readFileSync`; no existence-check-then-read | async 代码禁同步文件 API；禁「先判存在再读」，用 try-catch `isEnoent` | 「检查再读」是经典的 TOCTOU 竞态，直接捕获异常既快又对 |

> 💡 **测试视角**：「先判存在再读」被列为禁令，本质是**竞态条件（race condition）防御**——这与你在接口测试中「不要用状态查询结果决定下一步断言，要用最终一致性等待」是同一类工程直觉。

---

## 第二部分：Agent 架构设计经验（来自 README 设计决策）

### 2.1 顶层定位：一个你不会「用腻」的 harness

README 的三条 Key Ideas：

| 原文 | 中文 | 设计意图 |
|------|------|---------|
| Keep interactive terminal-first UX for real coding work | 保持「终端优先」的交互体验，面向真实编码工作 | 不做 Web 套壳，CLI 是开发者的主场 |
| Include practical built-ins (tools, sessions, branching, subagents, extensibility) | 内置实用能力：工具、会话、分支、子代理、可扩展性 | 开箱即用（batteries included），不让用户自己拼积木 |
| Make advanced behavior configurable rather than hidden | 高级行为做成可配置，而不是藏起来 | 能力可见、可调，拒绝「黑盒魔法」 |

> 💡 **核心洞察**："A harness worth keeping is one you don't outgrow"（值得留的 harness 是你不会长大的那个）——这句话点出了 OMP 与 Pi 的分野：Pi 极简到需要自己搭扩展，OMP 把 80% 人需要的能力内置、20% 做成配置项。**做测试平台时同理：高频路径内置，长尾需求配置化，而不是全塞进 UI 或全甩给用户写脚本。**

### 2.2 Rust 原生核心：消灭热路径上的 fork/exec

这是 OMP 最硬核的架构决策，约 **80,000 行 Rust** 组成 6 个 crate，以 N-API 插件形式嵌入 Node 进程：

| Crate | 职责 | 规模 |
|-------|------|------|
| `pi-shell` | 内嵌 bash 引擎 + 持久会话 + 进程内 coreutils | ~38k LoC |
| `pi-natives` | N-API 接口层 | ~25k LoC |
| `pi-walker` | 并行、ignore 感知的目录遍历 | ~5.2k LoC |
| `pi-iso` | 工作区隔离（apfs/btrfs/zfs/reflink） | ~3.3k LoC |
| `pi-ast` | tree-sitter + ast-grep 匹配 | ~2.9k LoC |
| `pi-voice` | 音频采集/播放、Opus、WebRTC | ~1k LoC |

**为什么这样做（README 原文论证）：**

> "Other agents shell out to rg, grep, find, and bash. On many machines those binaries don't exist, and on the ones where they do, every call costs a fork-exec round-trip. omp links the real implementations into the process."
> （其他 Agent 靠调用 rg、grep、find、bash 这些外部二进制。很多机器上根本没有这些程序；有的机器上，每次调用都要付出一次 fork-exec 的往返开销。omp 把真实实现链接进了进程。）

> "No fork/exec on the hot path."（热路径上零 fork/exec。）

> "Unapologetically native. Even on Windows."（毫不妥协的原生化，包括 Windows。）

**设计意图**：

1. **性能**：Agent 一次任务可能调几十次 grep/glob，进程内调用把每次 fork-exec 的毫秒级开销归零；
2. **可移植性**：不假设目标机器有 ripgrep/bash——这正是它敢承诺 **Windows 原生（无需 WSL）** 的底气；
3. **行为一致性**：所有平台的搜索/shell 行为由同一份代码保证，不存在「这台机器的 grep 版本不同导致结果不同」。

> 💡 **测试视角**：这条经验直接适用于你的自动化框架设计——**框架对外部二进制的依赖越少，环境差异导致的 flaky 越少**。你本机实测也验证了这一点：OMP 安装后是 155MB 的单文件 `omp.exe`，Python/pytest/LSP 环境全在进程内或显式配置，没有隐式依赖。另外「同一行为一份代码」让跨平台测试矩阵可以大幅缩水。

### 2.3 "IDE wired in"：让 Agent 拥有 IDE 的代码感知

OMP 的核心口号，由三个落地机制支撑：

**① LSP 接入每一次写入（LSP wired into every write）**

> "Everything your IDE knows, the agent knows."（你的 IDE 知道的一切，Agent 都知道。）

- 每次 `write`/`edit` 后自动走 LSP：诊断错误、格式化，错误作为工具结果**喂回 Agent 上下文**，Agent 当场自愈；
- 重命名文件走 `workspace/willRenameFiles`：re-exports、barrel files、别名导入**在文件移动前**就已更新；
- LSP 服务器不内置下载，采用「检测 PATH + 项目根标记（rootMarkers）」的自动发现机制，可用 `lsp.json` 按服务器覆盖配置。

**② 驱动真实调试器（Drives a real debugger）**

> "A C binary segfaults: the agent attaches lldb, steps to the bad pointer, reads the frame. ... Most agents are still sprinkling print statements."
> （C 程序段错误：Agent 附加 lldb，单步到坏指针，读栈帧。……而大多数 Agent 还在撒 print 语句。）

- 通过 DAP（Debug Adapter Protocol）支持 lldb / dlv / debugpy，28 种调试操作：断点、单步、查变量、调用栈。

**③ 编辑器可驱动（ACP: editor-drivable agent）**

- 通过 Agent Client Protocol 在 Zed 等编辑器里运行：读你正在看的 buffer、走编辑器的保存路径写文件、在编辑器终端起 shell。

> 💡 **测试视角**：LSP 回路把 Agent 从「盲写代码」变成「带编译器反馈的闭环」——**每次编辑即时拿到类型错误并自愈**。对测试人来说，DAP 能力更具杀伤力：`pytest` 挂了，Agent 附加 debugpy 真实打断点查变量，而不是靠日志猜测。这是「缺陷定位」场景的降维打击，你本机已装好 pyright/typescript/vue/jdtls 四个服务器，可以直接用。

### 2.4 Hashline 编辑：按内容哈希锚点定位，而不是行号

> "Perfect edits, fewer tokens. The model points at anchors instead of retyping the lines it wants to change, so whitespace battles and string-not-found loops just stop happening."
> （完美的编辑，更少的 token。模型指向锚点，而不是重打它想改的行——空白符大战和"找不到字符串"死循环就此消失。）

> "Edit a stale file and the anchors diverge — we reject the patch before it corrupts anything."
> （编辑一个已过期的文件，锚点会对不上——我们在补丁损坏任何东西之前拒绝它。）

**设计意图**：

| 问题 | 传统做法 | Hashline 做法 |
|------|---------|--------------|
| 编辑定位 | 模型重打整行/整段做字符串匹配 | 指向内容哈希锚点 |
| 常见失败 | 空白符差异 → `string not found` → 重试循环 | 锚点精确匹配，无歧义 |
| 并发/过期 | 文件被外部改动后编辑错位，损坏文件 | 锚点失配 → **拒绝补丁**， fail-fast |
| Token 成本 | 重打上下文浪费输出 token | 实测 Grok 4 Fast 输出 token **降低 61%** |

> 💡 **测试视角**：「锚点失配即拒绝」是 **乐观锁思想** 在编辑场景的落地——带版本号（哈希）的更新，过期即拒，绝不带病写入。这和你在接口并发测试中用的「条件更新/CAS」是同一个模式。同时「fail-fast 优于带病执行」也是测试设计的第一原则。

### 2.5 TTSR（时间旅行流规则）：纠错不占上下文税

> "Your rules sit dormant until the model goes off-script. A regex match aborts the stream mid-token, injects the rule as a system reminder, and retries from the same point."
> （规则平时休眠，直到模型跑题。正则命中时在 token 流中途中止，把规则作为系统提醒注入，从同一点重试。）

> "You get course-correction without paying context tax on every turn. Injections survive compaction, so the fix sticks."
> （你得到了纠偏，却不用在每一轮都支付上下文税。注入在压缩后仍然存活，修复效果持久。）

**设计意图**：传统做法是把所有规则塞进系统提示词——每轮都占上下文（context tax）。TTSR 反其道而行：**规则挂起为流式输出的正则守卫，命中才注入**，注入以 system reminder 形式存在所以压缩后仍在。

> 💡 **测试视角**：这是「按需注入」的上下文工程范本。你做 AI 测试 prompt 设计时可借鉴：长规则不要全塞系统提示，把「禁止事项」做成输出守卫（流式检测 → 中止 → 注入 → 重试），既省 token 又不漏约束。评测时，「规则触发率」本身可作为一个指标——触发越少说明模型对齐越好。

### 2.6 一等子代理：返回 schema 验证的结构化结果

- `task` 工具扇出隔离的 git worktree 子代理，各自独立上下文；
- 子代理返回 **schema 验证过的结构化对象**，不是自由文本；
- Vibe 模式（`/vibe`）把主会话变成「导演」：自己不写代码，指挥 `fast`（机械执行）/ `good`（判断审查）两级常驻 worker 并行干活；
- Advisor（`--advisor`）：第二个模型在独立上下文中**被动审查每一轮**，发现问题注入笔记。

> 💡 **测试视角**：「子代理返回结构化对象而非自由文本」是 Agent 可测性的关键设计——**自由文本只能人肉判断，结构化结果可以断言**。你在设计自己的多 Agent 测试框架时，worker 的产出契约就该定义为 JSON schema。「导演 + 两级 worker」则是经典的「生成者-审查者分离」：fast 产草稿、good 做审查，与「开发写代码、测试做验证」的组织分工同构。

### 2.7 生态兼容：继承而不是重建

> "Inherits what your other tools already wrote."（继承你其他工具已经写好的东西。）

- 直接读取 Claude Code、Codex、Cursor、CLine、Copilot 等 8 种工具的已有配置；
- `--from-claude` / `--from-codex` 导入历史会话；
- 9 种模型角色（default/smol/slow/plan/commit/vision/task/advisor/tiny）+ fallback 链 + 按路径锁模型 + 多 key 轮转。

> 💡 **核心洞察**：「不逼用户迁移，而是兼容存量」是工具推广的最优策略。对你的测试平台设计的启示：**新平台先兼容 pytest 已有用例和报告格式，再谈新能力**——降低迁移成本比功能强大更重要。

### 2.8 Token 与成本工程

| 手段 | 机制 | 效果 |
|------|------|------|
| Hashline 编辑 | 锚点代替重打 | 输出 token −61%（Grok 4 Fast 实测） |
| TTSR | 规则休眠，命中才注入 | 省每轮的系统提示上下文税 |
| `read` 摘要 | 读文件返回摘要片段而非全文 | 默认就省输入 token |
| 模型角色 | 简单任务路由到 smol/tiny | 小任务不烧大模型 |
| `tiny` 本地模型 | 会话标题/记忆用本地小模型 | 边角任务零 API 成本 |
| `snapcompact` | 位图帧光栅化 + PNG 编码压缩上下文 | 长会话压缩 |
| Fallback 链 | 429 限流自动切换模型 | 提高可用性，减少人工重试 |

> 💡 **测试视角**：「成本可观测、成本可路由」是 Agent 工程化的必修课。`omp usage` 提供按账号的用量监控——你给自己的 AI 自动化 SKILL 做成本评估时，也该把「每用例生成成本」「每轮对话 token」做成一等指标。

---

## 第三部分：测试与质量工程经验（AGENTS.md 的 Testing Guidance，全仓库最精华）

OMP 的 `AGENTS.md` 用整整一章定义测试哲学，其密度和可操作性远超一般开源项目，**几乎可以直接当作团队测试代码的评审 checklist**。

### 3.1 总纲：契约导向测试（Contract-oriented testing）

> 原文核心：**测试系统暴露的契约（行为、输出形状、状态转换、错误映射、解析边界）；无法命名失败模式，就不加测试。**

一句话：**每个测试都必须能回答「它防的是哪种具体的失败」**，答不上来的测试不写。

### 3.2 好测试清单（值得加测试的六类）

| 类别 | 说明 | 举例 |
|------|------|------|
| 命名失败模式 | 消费者会观察到什么错误 | 「解析器遇到非法 UTF-8 必须报 X 错误」 |
| 变换 | fixture 证明 parse/render/resolve 正确 | 输入 A → 输出 B 的转换对 |
| 分支/边界 | 空、畸形、路由、状态转换产生不同结果 | 空列表、超限额、非法枚举 |
| 外部契约 | provider/parser 读取的精确字节/形状 | API 响应的精确字段结构 |
| 优先级/否定契约 | 显式 `false`、override-wins 防泄漏 | 配置覆盖链的优先级 |
| 回归 | 复现历史失败路径并断言修正结果 | 与 issue 绑定的复现用例 |

### 3.3 坏测试清单（明确禁止的四类）

| 禁令 | 说明 | 为什么坏 |
|------|------|---------|
| **静态回声**（static echo） | 测「构造函数把 fixture 拷进字段」 | 没有行为契约，重构即碎 |
| **成功透传** | `fn(x) === x`（x 本来就合法） | 没测任何东西，假覆盖率 |
| **措辞/默认值** | 测 prompt 样板、默认字面量、非空、长度增长 | 无消费者契约，脆且噪音大 |
| **重复行** | 参数化同一代码路径 | 数量幻觉，不增加信息 |

### 3.4 测试工程纪律（执行层面）

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| No placeholders/tautologies (`expect(true).toBe(true)`) | 禁占位断言、禁同义反复 | 「代码跑了」不是断言 |
| Full-suite safe: no long-lived file/env mutations | 禁文件级/env 长效 mutation，用 `vi.spyOn` + `vi.restoreAllMocks()` | 测试间串扰是 flaky 的头号来源 |
| **No `mock.module()`**（Bun 全局泄漏），用 spyOn | 禁模块级 mock（全局污染），用对象级 spyOn | mock 泄漏 = 测试顺序依赖 |
| Trigger real failure paths, don't instantiate error classes | 触发真实失败路径，不直接 new 错误类 | 直 new 错误类测的是 catch 块，不是真实链路 |
| **Never source-grep tests** | **绝不允许读 `.ts`/`.rs` 源码文本做断言**（`expect(src).toContain(...)`）；结构约束用 type test / oxlint 强制 | 测实现而非契约，重构即假失败 |
| Assert exact bytes only when a consumer depends on them | 只有下游依赖精确字节时才断言精确字符串 | 过强断言 = 脆弱测试 |
| No tests for trivial low-risk changes | 微小低风险变更不强制加测试 | 测试有维护成本，ROI 优先 |
| Termination assertions must check bounded output, not bare `not.toThrow()` | 终止性断言要查有界输出/错误，裸 `not.toThrow()` 不算数 | 「不抛异常」是最弱断言 |

> 💡 **测试视角**：这一章值得你整章背诵——它把「测试反模式」从经验直觉变成了明文禁令。其中三条对你日常最有杀伤力：**① 禁 source-grep**（很多团队用「文件里有没有这段代码」当测试，这是假测试）；**② 禁 mock.module 用 spyOn**（Python 里对应：优先 `mocker.patch.object` 而非全局 patch）；**③ 每个测试必须能命名失败模式**（写用例标题时就要回答「防什么」）。面试被问「你怎么保证测试质量」时，这套清单就是满分答案。

### 3.5 Worker 脚本的冒烟验证

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Workers re-enter the CLI entry, never a separate entry module | worker 重新进入 CLI 主入口，绝不生成独立 worker 入口模块 | 单入口 = 单一启动路径，历史 issue #1011/#1027 都是双入口导致的二进制崩溃 |
| New workers verified via `omp --smoke-test` (runs in CI) | 新 worker 必须过 `--smoke-test`（CI 中运行） | 启动路径本身是回归对象 |
| Smoke tests only when they catch a narrow failure mode | 冒烟测试只在能抓窄失败模式时存在，「包能启动」不算 | 宽冒烟 = 假安全感 |

> 💡 **测试视角**：「冒烟测试必须抓窄失败模式」纠正了一个普遍误解——很多人以为冒烟就是「能起来就行」，OMP 的标准是「能精确抓住某一类启动回归」。你做接口冒烟时同理：冒烟用例应对准「部署后最容易坏的那几个点」（登录、核心链路、配置加载），而不是泛泛的「返回 200」。

---

## 第四部分：工程质量经验

### 4.1 日志与输出净化（容易被忽视的安全细节）

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| MUST NOT use `console.log/error/warn` in TUI/RPC/SDK/workers | TUI/RPC/SDK/worker 活跃时禁用 console 输出，必须走中心 logger（自动轮转落盘 `~/.omp/logs/`） | console 输出会破坏 TUI 渲染和 JSON-RPC 协议帧 |
| All tool renderer text must be sanitized | 所有工具渲染文本必须净化 | 防三类问题：tab 撑破布局、超长溢出、**home 目录路径泄露** |
| Tabs→spaces; truncate with helpers; `shortenPath()` replaces home with `~`; preview limits via `PREVIEW_LIMITS` | 制表符转空格、统一截断函数、路径家目录替换为 `~`、预览长度走常量表 | 净化逻辑集中且一致，连错误消息里的文件内容也要处理 |

> 💡 **测试视角**：「错误消息里的文件内容也要 replaceTabs」这个细节说明净化是**全路径覆盖**的——成功输出、错误输出、diff、流预览一个不漏。你做日志安全测试时，「错误路径是否泄露敏感信息（绝对路径、堆栈、密钥）」正是最容易被漏测的面。会话分享/导出场景（`/share`、`--export`）下路径脱敏更是硬性合规要求。

### 4.2 Changelog 与发布纪律

| 原文要点 | 中文翻译 | 设计意图 |
|---------|---------|---------|
| Entries only under `## [Unreleased]`, never modify released sections | 新条目只进 Unreleased 区，**绝不改已发布段落** | 已发布历史是不可变事实 |
| One line, user-facing; root cause belongs in commit/PR | 一行、面向用户；根因分析留给 commit/PR | changelog 是给用户的，不是给开发者的 |
| `bun run release` handles bump, finalize, commit, tag, publish | 发布全流程一个脚本：版本号、定稿、提交、打 tag、发布 | 发布动作原子化、去人工化 |

### 4.3 Rust 构建 profile 的「已驳回方案」清单

AGENTS.md 专门记录了被驳回的方案（sccache、mold、dev 上 `panic="abort"`）及驳回原因。

> 💡 **核心洞察**：把「已驳回方案 + 原因」写进规范，是防止 AI（和新成员）反复重提旧方案的记忆机制。这与你的错题集机制完全同构——**把失败决策显性化，避免重复踩坑**。你的团队技术文档也该有一节「我们不这样做，因为……」。

---

## 总结：OMP 留给我们最该带走的六条经验

1. **策略数据化，代码只管执行**：模型兼容性策略放 KDL 规则树构建期编译，代码只基于结构化分类分支——映射到测试领域：用例数据与执行引擎分离，新增接口/模型不动引擎。
2. **把确定性基础设施做进进程**：8 万行 Rust 消灭热路径 fork/exec，换来性能、可移植性与行为一致——映射到测试框架：外部二进制依赖越少，环境差异 flaky 越少。
3. **给 Agent 接上「编译器反馈闭环」**：LSP 接入每次写入、DAP 驱动真实调试器——Agent 从盲写变成自愈，这是「生成代码可信」的工程前提。
4. **编辑要有乐观锁**：Hashline 锚点失配即拒绝补丁——fail-fast 优于带病写入，并发场景的通用原则。
5. **测试必须能命名失败模式**：契约导向测试 + 好/坏测试清单 + 禁 source-grep/mock.module——可直接作为团队测试评审 checklist。
6. **上下文税要精打细算**：TTSR 规则休眠、read 默认摘要、模型角色路由——prompt 工程的尽头是成本工程。

如果再加一条属于 SDET 的「行动项」：

7. **把你已装好的环境用起来**：本机 OMP v18.1.9 + 4 个 LSP 服务器（pyright/ts/vue/jdtls）已就绪——下一步挑一个真实 pytest 项目，体验「LSP 自愈回路」和 `debug` 工具附加 debugpy 定位失败用例，把本文的设计经验变成手感。

> 注：本文基于 oh-my-pi 仓库 2026-09 的 README 与 AGENTS.md 整理（v18.x），项目迭代极快，规则细节以官方仓库最新版为准。与 Pi 原始设计经验的对比学习，见同目录《Pi的AI设计经验.md》。
