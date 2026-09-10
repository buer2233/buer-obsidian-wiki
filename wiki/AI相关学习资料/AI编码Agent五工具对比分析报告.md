---
type: comparison
title: "AI 编码 Agent 五工具对比分析报告（OMP / Pi / DSH / Claude Code / Codex）"
source: ".raw/AI相关学习资料/AI编码Agent五工具对比分析报告.md"
subjects:
  - "OMP（Oh My Pi）"
  - "Pi（badlogic/pi-mono）"
  - "DSH（DeepSeek Harness）"
  - "Claude Code"
  - "Codex"
dimensions:
  - "可观测性"
  - "可控制性"
  - "可断言性"
  - "可隔离性"
  - "模型绑定"
  - "合规与成本"
verdict: "OMP 当枪（生产工具）、Pi 当书（架构教材）、DSH 当台（组装框架）、Claude Code / Codex 当镜（能力参照）。"
created: 2026-09-10
updated: 2026-09-10
tags:
  - 对比
  - AI编码Agent
  - OMP
  - Pi
  - dsh
  - Claude Code
  - Codex
  - 测试开发
status: live
related:
  - "[[wiki/AI相关学习资料/OMP使用手册]]"
  - "[[wiki/AI相关学习资料/OMP的设计经验]]"
  - "[[wiki/AI相关学习资料/Pi的AI设计经验]]"
  - "[[wiki/AI相关学习资料/Pi源码精读顺序清单]]"
  - "[[wiki/AI相关学习资料/测试开发如何使用DSH]]"
  - "[[wiki/AI相关学习资料/Pi与AI编程Agent对比分析]]"
---

# AI 编码 Agent 五工具对比分析报告

面向 SDET（目标岗位：AI 自动化测试 / AI 产品测试）的横向选型报告。

> **修订记录**：2026-09-06 修正 Claude Code / Codex 的模型绑定描述——**它们都能接第三方模型，但有协议兼容前提**，不是「模型锁死」。

## 一、五工具核心定位速览

| 维度 | **OMP** | **Pi** | **DSH** | **Claude Code** | **Codex** |
|---|---|---|---|---|---|
| 出品方 | can1357（社区） | Mario Zechner | DeepSeek（官方开源） | Anthropic（官方） | OpenAI（官方） |
| 一句话定位 | 把 IDE 能力内置进来的「重装」多模型 Agent | 极简 coding harness，AI 协作规则范本 | 微内核 + 一切皆插件的智能体框架 | 厂商全家桶式终端 Agent | 云端沙箱 + 本地 CLI 双形态 Agent |
| 模型绑定 | **60+ 提供商中立** | 多提供商（ai 包统一抽象） | 主推 DeepSeek，兼容近 40 家 | **主推 Claude + 支持任意 Anthropic Messages API 兼容网关** | **主推 OpenAI 系 + 支持任意 OpenAI 兼容端点** |
| 架构哲学 | batteries included（内置 80% 能力） | 极简核心 + 少量扩展点 | 微内核（Cordis）+ 插件生态 | 开箱即用 + SKILL/Hooks 生态 | 云端任务制 + 本地轻 CLI |
| 杀手级特性 | LSP 接入每次写入、DAP 真实调试器、TTSR、Hashline 编辑 | AGENTS.md 规则体系、faux provider、官方 evals 框架 | 一切皆插件、沙箱三级权限、**Python SDK**、会话 JSONL 审计 | Agent 质量与稳定性标杆、SKILL 生态、Hooks | 云端并行任务、GitHub 深度集成、沙箱隔离执行 |
| 许可证 | MIT | MIT | MIT | 闭源（订阅/API） | CLI 开源（Apache 2.0） |

### 三句话抓住本质

1. **Pi 是「教材」，OMP 是「产品」**：同一祖先，Pi 把扩展留给你自己写（适合研究与二次开发），OMP 把 LSP/DAP/子代理/记忆全内置（适合直接干活）。
2. **DSH 是「框架」，Claude Code / Codex 是「成品服务」**：DSH 给你微内核与插件机制去**组装**自己的 Agent 工作台；CC / Codex 给你调好的成品。
3. **模型中立程度不同**：OMP / Pi / DSH 是「**内置多协议适配**」（直接接各家模型 API）；CC / Codex 是「**协议网关路由**」（必须借一个翻译层来换模型）。两者自由度有差距，但 **CC / Codex 不是「模型锁死」**。

## 二、各工具优点与不足

### 2.1 OMP（Oh My Pi）

**优点**
- **生成代码可信度最高**：LSP 接入每次写入（写完即诊断自愈）、Hashline 锚点编辑（失配即拒，不损坏文件）、DAP 真实调试器
- **模型自由度最大**：60+ 提供商 + 自定义 `models.yml`（**公司内网网关可直接接**）+ 9 种模型角色路由 + fallback 链
- **Windows 原生**：Rust 进程内 ripgrep/bash，无需 WSL，155MB 单文件
- **零迁移成本**：直接继承 Claude Code/Codex/Cursor 等 8 种工具配置，`--from-claude` 导入历史会话
- **成本工程到位**：TTSR 省上下文税、read 默认摘要、tiny 本地小模型，实测部分模型输出 token **−61%**

**不足**
- 社区项目，迭代极快（v18.x），文档偶尔滞后于代码
- 功能密度高带来学习曲线（31 个工具、9 种角色、Vibe 模式）
- LSP/DAP 能力依赖本机语言服务器质量，环境配置有门槛
- 无官方商业支持，问题靠 GitHub issue

详见 → [[wiki/AI相关学习资料/OMP使用手册|OMP 使用手册]] ｜ [[wiki/AI相关学习资料/OMP的设计经验|OMP 的设计经验]]

### 2.2 Pi（badlogic/pi-mono）

**优点**
- **最干净的架构教材**：协议/模型/运行时/UI/存储五层正交分层，各层可独立测试——「可测性设计」范本
- **AGENTS.md 规则体系**：多 Agent Git 护栏、安全授权边界，可直接复用为团队 AI 协作规范
- **测试工程金矿**：faux provider（脚本化假模型）、官方 evals 框架、6 个安全护栏 Extension 示例
- 极简核心意味着**阅读源码成本最低**，想理解 Agent 原理从这里入手最快

**不足**
- 极简 = 大量能力要自己搭扩展，开箱体验不如 OMP / Claude Code
- 核心维护节奏看作者个人精力；生态规模小，现成插件少

详见 → [[wiki/AI相关学习资料/Pi的AI设计经验|Pi 的 AI 设计经验]] ｜ [[wiki/AI相关学习资料/Pi源码精读顺序清单|Pi 源码精读顺序清单]]

### 2.3 DSH（DeepSeek Harness）

**优点**
- **一切皆插件**（Cordis 微内核，Koishi 4 年验证）：工具、钩子、门禁、审计全部以插件注入
- **安全体系最完整**：沙箱（bwrap/Seatbelt/Windows ACL）+ 三级权限 + 瀑布式策略钩子
- **Python SDK 是一等公民**：对 Python 技术栈的 SDET 最友好，可直接嵌入 pytest 体系
- **会话 JSONL 事件日志**：全过程可追溯回放，天然的测试证据链
- Profile 分层：同一内核覆盖交互（web）与自动化（headless/SDK）

**不足**
- 开发者预览阶段（0.1.0-rc.x），官方明示「会有破坏性变更」
- 官方 SAFETY.md 明确沙箱「未经审计、不保证隔离」，不能作为唯一安全控制
- 插件生态年轻（社区目录收录 ≠ 官方背书）
- Web UI 优先的设计对纯终端用户不如 OMP / CC 顺手

详见 → [[wiki/AI相关学习资料/测试开发如何使用DSH|测试开发如何使用 DSH]]

### 2.4 Claude Code

**优点**
- **Agent 综合质量标杆**：复杂任务规划、长上下文工程、工具调用稳定性普遍被认为是业界天花板
- **生态最成熟**：SKILL 体系、Hooks、MCP 连接器、子代理、GitHub Actions 集成
- **网关路由能力强**：`ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` 可指向任意 Anthropic Messages API 兼容网关（智谱 GLM / Kimi / OpenRouter / Vercel AI Gateway / claude-code-router）；v2.1.129+ 支持网关模型自动发现（`CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`）

**不足**
- **有协议前提**：CC 自身只直接认 Anthropic Messages API 协议，换模型家族必须经兼容网关
- ⚠️ **认证变量有坑**：`ANTHROPIC_API_KEY`（X-Api-Key 头）优先级**高于** `ANTHROPIC_AUTH_TOKEN`（Bearer），shell profile 里残留的旧 key 会偷偷覆盖网关配置（`/status` 可查实际生效变量）
- 闭源，无法读源码学习内部实现；能力边界由厂商定义；订阅/API 对重度使用是持续成本

### 2.5 Codex

**优点**
- **云端沙箱任务制**：任务在 OpenAI 云端隔离环境并行执行，一次派多个任务不占本机资源
- **GitHub 深度集成**：直接读仓库、提 PR、做代码审查，适合「派单式」工作流
- **自定义 Provider 一等公民**：`~/.codex/config.toml` 的 `[model_providers.<name>]` 块定义 `base_url` + `env_key` + `wire_api`；官方明示「可与非 OpenAI 模型一起使用，只要使用 OpenAI chat completions API 兼容的 wire API」；实测可用 DeepSeek / OpenRouter / Ollama / LM Studio / Azure / LiteLLM

**不足**
- 必须用 OpenAI 兼容端点，想用原生 Anthropic 协议模型需经网关
- **保留名限制**：自定义 provider 名不能用 `openai`、`ollama`、`lmstudio`
- 🚫 **云端模式数据出境**——公司代码传到 OpenAI 云端，**合规红线**（公司场景基本不可用）
- 本地 CLI 形态能力与生态成熟度不及 Claude Code

## 三、SDET 四大高频场景对照

### 3.1 测试用例设计

| 工具 | 具体应用方式 |
|---|---|
| **OMP** | `read` 读源码/需求文档 → LSP 保证理解的代码结构准确 → 生成 pytest 用例骨架；`--from-claude` 可接着 CC 里的会话继续干 |
| **Pi** | 适合**研究**「用例生成 Agent 该怎么设计」：参考其 evals 框架给用例生成器建评测集 |
| **DSH** | 装 `dsh-test-runner` 插件，让 Agent 探测 pytest 框架、读业务代码提测试点；JSONL 日志可作为「用例设计过程」的评审材料 |
| **Claude Code** | 成熟路径：SKILL 化的用例生成流程（抓包 → 生成 → 入库） |
| **Codex** | 云端派单输出边界值测试点清单——但公司代码不建议上云 |

### 3.2 自动化测试（接口 + UI）

| 工具 | 具体应用方式 |
|---|---|
| **OMP** | ① 接口：`eval` 持久 Python worker 直接调 requests+pytest 试跑；② UI：`browser.open()` 驱动真实 Chrome 验证选择器再固化到 Playwright；③ CI：`omp -p --mode json` 无头模式嵌入流水线 |
| **Pi** | 不建议直接用于生产自动化，但其 **tmux 驱动 TUI** 的测试套路可借鉴 |
| **DSH** | **五者中最贴合 Python 技术栈**：Python SDK 内嵌 pytest（conftest fixture 化）；`dsh-playwright-browser` 语义定位（role/label，抗 UI 改版）；headless profile 接 CI |
| **Claude Code** | 日常主力：AI 接口自动化 SKILL 生态基本盘 |
| **Codex** | 适合开源/个人项目的 PR 级自动化验证，不适合公司内网 |

### 3.3 缺陷分析

| 工具 | 具体应用方式 |
|---|---|
| **OMP** | **独家能力**：`debug` 工具附加 debugpy 到挂掉的 pytest 进程，真实打断点、查变量、看调用栈——从「读日志猜」升级到「调试器实证」；`/review` 生成 P0-P3 报告当提测门禁 |
| **Pi** | 参考 `regressions/<issue号>-<slug>.test.ts` 规范，把回归用例与缺陷号强绑定 |
| **DSH** | headless 模式跑「失败用例分析」：执行 → 汇总失败 → 从堆栈定位可疑代码 → 给 diff 预览（人工审查后落盘） |
| **Claude Code** | 读失败日志 + 源码做根因分析；配合 Hooks 可在测试失败时自动触发分析 |
| **Codex** | 云端跑失败复现与修复建议输出 PR——开源可用，公司项目慎用 |

### 3.4 测试平台 / 框架二次开发

| 工具 | 具体应用方式 |
|---|---|
| **OMP** | Vibe 导演模式并行重构：fast worker 批量迁移、good worker 审查边界；LSP `willRenameFiles` 保证大重构不炸引用 |
| **Pi** | **二次开发首选底座**：RPC/SDK 可编程、架构清晰、MIT 许可 |
| **DSH** | **组装测试工作台首选**：用插件机制把能力（执行器、门禁、审计、报告）注入 Agent 运行时 |
| **Claude Code** | 不支持深度二次开发，只能用 SKILL/Hooks/MCP 在既定边界内扩展 |
| **Codex** | CLI 开源可改，但为单模型优化，做底座价值不如 Pi |

## 四、选型决策矩阵与推荐组合

| 约束 | 结论 |
|---|---|
| 公司内网/代码不出境 | ❌ Codex 云端模式 → ✅ OMP / DSH（可接内网模型网关）、✅ Claude Code（接公司内 Anthropic 兼容网关） |
| 已投资 Claude Code SKILL 生态 | ✅ 个人学习继续用 CC，产出沉淀为 SKILL；公司场景需把 CC 指到内网网关才合规 |
| Python 技术栈 + pytest 体系 | ✅ DSH（Python SDK）+ OMP（eval 持久 Python worker） |
| 需要读源码学 Agent 原理 | ✅ Pi（最干净）→ OMP（最丰富） |
| 成本敏感 | ✅ OMP（模型角色路由 + 本地 tiny 模型 + 内网网关） |

**推荐三件套**：

```
┌─────────────────────────────────────────────────────────┐
│  日常生产主力：OMP（已装好，直接产出）                      │
│  - 用例生成/维护、debugpy 缺陷定位、/review 提测门禁        │
│  - 接公司内网模型网关（models.yml），代码不出境             │
├─────────────────────────────────────────────────────────┤
│  框架研究底座：Pi + OMP 源码                               │
│  - Pi 学架构分层与 evals 方法论                             │
│  - OMP 学工程化决策（LSP 回路、Hashline、TTSR）             │
├─────────────────────────────────────────────────────────┤
│  工作台组装：DSH（需要插件化/沙箱时启用）                    │
│  - Python SDK 嵌入 pytest、权限门禁、CI headless 回归       │
└─────────────────────────────────────────────────────────┘
```

> **CC 与 Codex 的定位**：作为「能力参照系」而非主力——关注其 SKILL/Hooks/云端任务/网关路由设计，把可借鉴思路移植到可控的 OMP/DSH 环境里；面试时作为横向对比谈资。**Claude Code 通过 Anthropic 兼容网关可在公司内网合规使用**（前提：网关在你们内网），这点常被低估。

## 五、可借鉴的设计经验（面试弹药）

### 5.1 Agent 开发：五个工具教你的七件事

| # | 经验 | 来源 | 应用到工作 |
|---|---|---|---|
| 1 | **分层解耦，各层可独立测** | Pi（协议/模型/运行时/UI/存储五层） | 测试平台按「数据/引擎/执行/报告」分层，每层可单独单测 |
| 2 | **策略数据化，引擎不硬编码** | OMP（KDL 规则树 + classifyModel） | 用例数据、接口适配规则放 YAML/JSON；新增接口不动引擎 |
| 3 | **确定性基础设施内建** | OMP（80k 行 Rust 消灭 fork/exec） | 框架减少外部二进制依赖；必须依赖的（如 git）走唯一封装通道 |
| 4 | **一切皆插件 + 钩子策略层** | DSH（Cordis 微内核、`tools/pre-execute` 瀑布） | 测试平台的能力扩展做成插件 + 拦截器，核心循环一行不改 |
| 5 | **反馈闭环 > 盲写** | OMP（LSP 接入每次写入） | 用例生成器生成后必须自动试跑/语法校验，错误喂回重生成 |
| 6 | **fail-fast 与乐观锁** | OMP（Hashline 锚点失配即拒） | 并发写共享资源带版本校验，过期即拒 |
| 7 | **成本是一等指标** | OMP（模型角色路由/TTSR/read 摘要） | 给 AI 用例生成统计「每用例 token 成本」，简单任务路由小模型 |

### 5.2 Agent 测试：五个工具教你的七件事

| # | 经验 | 来源 | 应用到工作 |
|---|---|---|---|
| 1 | **去模型化测试（fake provider）** | Pi（faux provider：脚本化响应 + 队列耗尽报错 + callCount 可观测） | 测任何依赖 LLM 的代码时注入假模型剥离随机性；**AI 测试面试的黄金答案** |
| 2 | **对比评测标准方法** | Pi evals（harness + judge + repetitions + pass-rate lift + paired deltas） | 复用这套方法论对比「两个 prompt / 两个模型 / 两版 SKILL」 |
| 3 | **契约导向测试，每个用例命名失败模式** | OMP（Testing Guidance 好/坏测试清单） | 当作团队测试评审 checklist：禁静态回声、禁成功透传、禁 source-grep |
| 4 | **过程留痕即证据链** | DSH（会话 JSONL 日志可回放） | AI 辅助测试的操作过程全程落日志，缺陷分析可回放、可审计 |
| 5 | **威胁模型先行** | Pi（SECURITY.md 明确信任边界与 Out of Scope）+ DSH（SAFETY.md 不保证隔离） | 做 Agent 安全测试前先定义「信任边界在哪」；多层防御 |
| 6 | **环境隔离三板斧** | Pi（test.sh：独立临时根+所有权标记、env -i 空环境白名单、确定性时区语言） | CI 测试环境直接照搬，解决测试串扰与环境 flaky |
| 7 | **沙箱 ≠ 安全，验证边界行为** | DSH（read-only 模式下尝试写文件验证拒绝行为） | 把「权限模式的拒绝行为」本身写成合规性测试用例 |

### 5.3 面试应答框架（可直接用）

**Q：你怎么评测两个 AI 测试工具的优劣？**
> A：用 Pi evals 框架的方法论：**harness**（把被测对象包装成可跑单元，隔离临时目录运行）+ **judge**（确定性规则或模型打分）+ **repetitions**（重复消随机）+ 对比指标（**pass-rate lift 百分点 + token/延迟/成本的 paired delta**）。同时用可测性四维评估工具本身：可观测性（事件日志）、可控制性（钩子/权限）、可断言性（结构化输出/schema）、可隔离性（fake 模型/沙箱）。

**Q：AI 生成的测试代码怎么保证质量？**
> A：三层防线：① **生成侧**——参考 OMP 的 LSP 回路，生成即诊断，错误喂回自愈；② **契约侧**——Hashline 思想，落盘前校验锚点（上下文未漂移）才允许写入；③ **评审侧**——用契约导向清单过滤坏测试（静态回声、成功透传、假断言），AI 生成的用例必须能命名它防的失败模式。

**Q：多个 AI Agent 协作怎么防止互相踩踏？**
> A：参考 Pi 的多 Agent Git 护栏：只提交自己改的文件、显式路径暂存（**禁 `git add -A`**）、禁用破坏性命令（reset --hard/clean/stash）、冲突只处理自己的文件；再叠加 OMP 的 **worktree 隔离**——每个子代理在独立 git worktree 里干活，物理隔离。

## 六、一页纸总结

| 工具 | 一句话建议 |
|---|---|
| **OMP** | **现在就用**——已装好，接内网网关后成为日常主力；重点体验 LSP 自愈回路、debugpy 缺陷定位、/review 门禁 |
| **Pi** | **继续精读**——Agent 架构与评测方法论的教材，evals 框架是面试金矿 |
| **DSH** | **按需启用**——需要 Python SDK 嵌 pytest、权限门禁、插件化工作台时上；先试 headless 失败分析 |
| **Claude Code** | **保持关注**——SKILL 生态基本盘，能力参照系 |
| **Codex** | **了解即可**——云端模式对公司场景是合规红线 |

**组合策略一句话**：**OMP 当枪（生产工具），Pi 当书（架构教材），DSH 当台（组装框架），Claude Code / Codex 当镜（能力参照）。**

## 落地顺序建议

1. **本周**：用 OMP 跑通一个真实场景——对当前 pytest 项目做一次 `debug` 工具定位失败用例 + 一次 `/review` 提测自检
2. **两周内**：把公司模型网关配进 `~/.omp/agent/models.yml`，验证内网模型下的用例生成质量
3. **一个月内**：用 DSH Python SDK 把「接口变更 → 用例维护」封装成 pytest 命令
4. **持续**：Pi 源码精读继续推进（evals 框架部分），把评测方法论变成面试弹药

## 🔗 关联文档

- [[wiki/AI相关学习资料/OMP使用手册|OMP 使用手册]] — 安装、CLI 参数、31 个内置工具、Vibe 模式
- [[wiki/AI相关学习资料/OMP的设计经验|OMP 的设计经验]] — KDL 策略数据化、Hashline、TTSR、测试哲学
- [[wiki/AI相关学习资料/Pi的AI设计经验|Pi 的 AI 设计经验]] — faux provider、evals 框架、安全护栏
- [[wiki/AI相关学习资料/Pi源码精读顺序清单|Pi 源码精读顺序清单]] — L0-L9 分层阅读路线
- [[wiki/AI相关学习资料/测试开发如何使用DSH|测试开发如何使用 DSH]] — 五大测试领域实战
- [[wiki/AI相关学习资料/Pi与AI编程Agent对比分析|Pi 与 AI 编程 Agent 对比分析]] — 早期四工具对比（可测性四维视角）
- [[wiki/AI相关学习资料/Graph Engineering从概念到测试落地|Graph Engineering]] — 多 Agent 编排与治理
- [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点-进阶版|eval 体系工程化落地]]

## 源文件

- `.raw/AI相关学习资料/AI编码Agent五工具对比分析报告.md`
