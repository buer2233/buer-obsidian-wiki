---
type: reference
title: "Pi 源码精读顺序清单"
source: ".raw/AI相关学习资料/Pi源码精读顺序清单.html"
created: 2026-09-10
updated: 2026-09-10
tags:
  - AI编码Agent
  - Pi
  - 源码精读
  - evals框架
  - 学习路线
status: live
related:
  - "[[wiki/AI相关学习资料/Pi的AI设计经验]]"
  - "[[wiki/AI相关学习资料/AI编码Agent五工具对比分析报告]]"
  - "[[wiki/AI相关学习资料/OMP的设计经验]]"
---

# Pi 源码精读顺序清单

面向 SDET 的 Pi 仓库阅读路线——clone 之后按这个顺序读，少走弯路。**由浅入深 10 层（L0-L9）+ 动手产出**。

> ⚠️ **说明 ①：真实目录已重构。** 官网 README 早期提到的 5 包（pi-telemetry / pi-ai / pi-agent-core / pi-coding-agent / pi-tui）**已过时**。当前 `packages/` 下实际是 **9 个包**：`agent`、`ai`、`client`、`coding-agent`、`evals`、`protocol`、`server`、`session-backends/sqlite-node`、`tui`。
>
> ⭐ **说明 ②：SDET 必读的重头戏是 `packages/evals`。** 这是 Pi 官方的**行为评测框架**（基于 `vitest-evals`），教你怎么把 Agent 当被测对象、怎么写评测 harness、怎么做 baseline vs candidate 的对比评测（含 pass-rate 提升、token/延迟/成本增量）。**这是市面上最难得的「官方 Agent 测试」活教材**，建议单独花 2 小时精读。

## L0 · 准备：先跑起来（约 15 分钟）

```bash
git clone https://github.com/earendil-works/pi.git
cd pi
npm install --ignore-scripts   # 装依赖，跳过生命周期脚本
npm run build                  # 构建所有包（首次较久）
./pi-test.sh                   # 从源码直接运行 pi，无需全局安装
```

> 先跑通一次交互，建立「它到底怎么工作」的直觉，再开始读代码。（Windows 用 `pi-test.ps1` 或 `pi-test.bat`）

## L1 · 入口层：先看全局（约 30 分钟）

| # | 文件 | 为什么读 | 产出 |
|---|---|---|---|
| 1 | `README.md` | 项目定位「minimal terminal coding harness」、四种运行模式、设计哲学 | 能一句话说清 Pi 是什么 |
| 2 | ⭐ `AGENTS.md` | **SDET 视角的宝藏**：看他们**怎么给 AI 写项目约束**——活生生的「prompt/约定工程」范例 | 理解「给 Agent 写约定」到底写什么 |
| 3 | `package.json` | workspaces 列表（9 个包）、scripts（`build` / `check` / `eval`） | 知道有哪些命令、9 个包分别叫什么 |

## L2 · 架构总览：9 包分工（约 1 小时）

| 包 | 定位（测试视角） | 优先级 |
|---|---|---|
| `agent` | Agent 运行时：工具调用 + 状态管理 —— **被测对象核心** | ⭐⭐⭐ |
| `evals` | 官方评测框架（行为评测 + 对比评测） | ⭐⭐⭐ |
| `coding-agent` | 交互式 CLI 主包（用户入口） | ⭐⭐⭐ |
| `protocol` | 事件 / 协议类型定义（telemetry 契约的演化） | ⭐⭐ |
| `server` | RPC / 进程集成服务端 | ⭐⭐ |
| `ai` | 统一多提供商 LLM API 适配层 | ⭐⭐ |
| `tui` | 终端 UI（差分渲染） | ⭐ |
| `client` | 客户端 / 连接层 | ⭐ |
| `session-backends/sqlite-node` | 会话存储后端（SQLite） | ⭐ |

**第 4 步**：读 `tsconfig.base.json` + `vitest.base.ts` —— 整个 monorepo 的工程基础配置，看懂它就懂这套工程的「骨架」。

## L3 · 运行时：Agent 怎么跑（约 1.5 小时）

| # | 目标 | 为什么读 | 产出 |
|---|---|---|---|
| 5 | `packages/agent/src/` | Agent Loop 核心实现：怎么读上下文、调度工具调用、管理状态。**这是「被测对象」本体** | 画出 Agent Loop 的流程图 |
| 6 | `packages/protocol/` | 事件类型、会话格式、工具调用 schemas。**可观测性的源头** | 列出「可断言的关键事件类型」清单 |
| 7 | `packages/server/` | RPC 服务端，第三方进程如何通过 stdin/stdout JSONL 驱动 Pi | 理解「进程级测试驱动」的原理 |

## L4 · 交互与扩展：怎么写 Extension（约 1.5 小时）

| # | 目标 | 为什么读 |
|---|---|---|
| 8 | `packages/coding-agent/README.md` | CLI 完整参考：命令、快捷键、模式、Providers——官方文档的「源码版」 |
| 9 | ⭐ `packages/coding-agent/examples/` | 官方示例：`extensions/` 下有 `summarize.ts`、`snake.ts` 等可运行实现。**照着抄一遍，胜过读十篇教程** → 产出：把 `summarize.ts` 改成自己的「测试守护」Extension |
| 10 | `packages/coding-agent/docs/` | 文档源：containerization、extensions 等主题，比网页版更全更细 |

## L5 · UI 层（约 40 分钟 / 可选）

**第 11 步**：`packages/tui/` + 根目录 `tui-plan.md`（约 36KB 设计文档）——差分渲染终端 UI 怎么设计的。若非 UI 方向可略读，重点理解「UI 与逻辑解耦」。

## L6 · AI 适配层（约 1 小时）

| # | 目标 | 为什么读 |
|---|---|---|
| 12 | `packages/ai/` | 统一多提供商 LLM API：OpenAI/Anthropic/Google 如何被抽象成统一接口。**「模型中立」的实现原理在这** |
| 13 | `packages/client/` | 连接/客户端层 |

## L7 · ⭐ 评测层（SDET 金矿，约 2-3 小时，重点）

> **这是全仓库对测试工程师价值最高的部分**：Pi 官方把「怎么评测一个 Agent」写成了可运行的代码。

| # | 目标 | 为什么读 |
|---|---|---|
| 14 | `packages/evals/README.md` | 评测框架总纲：行为评测（behavioral）、隔离临时目录运行、自动附上原生 session 产物。`npm run eval -- --provider openai --model ...` → 产出：理解「Agent 评测 harness」长什么样 |
| 15 | ⭐ `packages/evals/src/pi-harness.ts` | `createPiCodingAgentHarness(...)`：把真实 `AgentSession` 包装成可评测对象，支持 `noTools`、`transformSystemPrompt`、`output` 转换、多步 prompt/reload 序列。**这就是「被测对象适配器」的标准写法** |
| 16 | `packages/evals/src/*.eval.ts` | 真实评测用例，例如用 `describeEval("Pi smoke", { harness }, ...)` 写断言 |
| 17 | ⭐ `packages/evals/src/vitest-evals/harness-table.ts` | **对比评测**：`evalHarnessTable(baseline vs candidate)`，跑重复次数（repetitions），用 judge 打分，算 **pass-rate 提升、token/延迟/成本增量**。这是做「A/B 评测」的现成方法论 |
| 18 | `packages/evals/test/` | 评测框架自己的测试，看它怎么验证「评测代码」本身 |

**关键概念对照（面试会考）**：`harness`（被测对象适配器）、`judge`（打分器）、`judgeThreshold`（阈值）、`describeEval`（评测套件）、`repetitions`（重复次数）、`pass-rate lift`（通过率提升）、`paired deltas`（token/延迟/成本成对增量）。

> 详细机制解读见 → [[wiki/AI相关学习资料/Pi的AI设计经验|Pi 的 AI 设计经验]] §4.5

## L8 · 测试工程：他们怎么测自己（约 1.5 小时）

| # | 目标 | 为什么读 |
|---|---|---|
| 19 | 各包的 `test/` 目录 | 逐个看 `agent/test/`、`coding-agent/test/`、`evals/test/`……**读别人怎么测一个 Agent runtime，是最实在的测试能力积累** |
| 20 | `vitest.config.ts` / `vitest.test.config.ts` / `test.sh` | 测试编排入口：`./test.sh` 跑全量（**无 API Key 时自动跳过依赖 LLM 的用例**） |

## L9 · 供应链与工程化（约 40 分钟）

| # | 目标 | 为什么读 |
|---|---|---|
| 21 | `.npmrc`、`npm-shrinkwrap.json`、`scripts/build-binaries.sh` | 供应链安全加固（`save-exact`、`min-release-age`、shrinkwrap 锁传递依赖）——学习「工程化 + 安全」 |
| 22 | `.github/workflows/`、`.husky/`、`biome.json`、`SECURITY.md` | CI 流程、git hooks、lint/format、漏洞上报规范。**看一个开源项目怎么管质量门禁** |

## 动手产出（把知识变成简历项目）

- ✅ 手写一个 Extension（如 `run_tests`），用 `pi -e ./my-ext.ts` 验证
- ✅ 用 `npm run eval` 跑通一个官方评测，读懂输出里的 `runs.jsonl` + `sessions/`
- ✅ 基于 `evalHarnessTable` 写一个自己的对比评测（baseline vs candidate）
- ✅ 写一篇「Pi 评测机制源码分析」笔记，沉淀到知识库

> 💡 **面试加分项**：能说出「**我读过 Pi 的 `packages/evals` 源码，它用 `vitest-evals` 把 AgentSession 包装成 harness，用 judge + baseline/candidate 做行为对比评测**」——这句话足以证明你的 AI 测试能力不是背的，是拆过源码的。

## 🔗 关联文档

- [[wiki/AI相关学习资料/Pi的AI设计经验|Pi 的 AI 设计经验]] — 源码精读提炼的设计经验（faux provider、evals 框架、安全护栏）
- [[wiki/AI相关学习资料/AI编码Agent五工具对比分析报告|AI 编码 Agent 五工具对比]] — 选型与二次开发建议
- [[wiki/AI相关学习资料/OMP的设计经验|OMP 的设计经验]] — 另一个可精读的架构范本
- [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点-进阶版|eval 体系工程化落地]]

## 源文件

- `.raw/AI相关学习资料/Pi源码精读顺序清单.html`

> 注：以上目录结构为 2026-08-27 检索时点快照，仓库迭代快，若路径略有出入以 `git pull` 后的实际为准；`client`/`server` 的精确职责建议以各自包内 README 为准。仓库地址：github.com/earendil-works/pi
