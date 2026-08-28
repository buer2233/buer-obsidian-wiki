---
type: comparison
title: "Pi 与 AI 编程 Agent 对比分析"
source: ".raw/AI相关学习资料/Pi与AI编程Agent对比分析.html"
subjects:
  - "Pi（Armin Ronacher）"
  - "Claude Code"
  - "OpenAI Codex"
  - "DeepSeek Harness (dsh)"
dimensions:
  - "可观测性"
  - "可控制性"
  - "可断言性"
  - "可隔离性"
  - "安全模型"
  - "模型绑定"
verdict: "Pi 最适合做「可编程的测试驱动引擎」；dsh 适合「过程可追溯的被测对象」；Claude Code 开箱即用体验最好；Codex 性能与安全最强。"
created: 2026-08-27
updated: 2026-08-27
tags:
  - 对比
  - AI编码Agent
  - Pi
  - Claude Code
  - Codex
  - dsh
  - 测试开发
status: live
related:
  - "[[wiki/语雀/claude-code/Claude Code学习笔记]]"
  - "[[wiki/语雀/claude-code/Harness Engineering（驾驭工程）]]"
  - "[[wiki/软件测试学习资料/16_AI_UI自动化_browser-use二次开发学习资料]]"
sources:
  - ".raw/AI相关学习资料/Pi与AI编程Agent对比分析.html"
---

# Pi 与 AI 编程 Agent 对比分析

> Pi 极简 Coding Harness 学习指南（测试开发工程师版）。以 **可测性（Testability）** 为核心视角，拆解 Pi、Claude Code、OpenAI Codex、DeepSeek Harness (dsh) 四大 AI 编码 Agent。

## 一、为什么 SDET 要关注 Pi

1. **理解「AI 编码 Agent 分层架构」的最佳样本**——Pi 把「核心 harness / 扩展层 / 供应商层」拆得最干净，是 AI 测试的地基。
2. **天生可编程、可集成**——Print/JSON、RPC、SDK 三种非交互模式，可被脚本、pytest、CI 直接驱动。
3. **「能力留白」= 测试机会**——没有内置权限系统，安全边界要由测试工程师定义和验证。

> **一句话**：用 Claude Code / Codex 是「用产品」，用 Pi 是「研究 Agent 怎么被构造、怎么被测」。

## 二、快速认知：什么是 Harness

- **Pi**：minimal terminal coding harness，作者 **Armin Ronacher**（Flask 作者，mitsuhiko），**MIT 开源**。
- 核心理念：「Adapt pi to your workflows, not the other way around.」——让 pi 适配你的工作流，而非反过来。

### 三条核心理念

- **核心最小化**：默认只给模型 4 个工具——`read` / `write` / `edit` / `bash`。
- **刻意留白**：不内置子代理、plan mode、权限系统、容器化。
- **可扩展优先**：Extension / Skill / Prompt Template / Theme / Package 五层扩展机制。

### 五包架构（npm workspaces Monorepo）

| 包名 | 作用 | 测试视角 |
|------|------|---------|
| `@earendil-works/pi-telemetry` | 供应商中立的遥测契约、参考适配器、一致性测试 | ⭐ 事件契约，可观测性源头 |
| `@earendil-works/pi-ai` | 统一多提供商 LLM API | 模型适配层，跨模型对比 |
| `@earendil-works/pi-agent-core` | Agent 运行时，工具调用 + 状态管理 | ⭐ 被测对象核心 |
| `@earendil-works/pi-coding-agent` | 交互式编码 Agent CLI | 面向用户入口 |
| `@earendil-works/pi-tui` | 终端 UI 库（差分渲染） | UI 层 |

### 四种运行模式

| 模式 | 说明 | 测试/集成场景 |
|------|------|-------------|
| Interactive | 交互式 TUI | 日常手工编码 |
| Print / JSON | 无交互结构化 JSON 输出 | ⭐ 脚本、pytest、CI、管道 |
| RPC | stdin/stdout JSONL 协议 | ⭐ 进程级集成、测试驱动 |
| SDK | Node.js 库嵌入 | ⭐ 二次开发测框架 |

### 安全与隔离 ⚠️

Pi **默认不内置权限系统**，以启动用户权限运行。外部隔离方案：**Gondolin micro-VM**、**Plain Docker**、**OpenShell**。对测试工程师：权限测试、路径保护、凭据隔离需要自行架设。

## 三、Pi 的可测性分析（SDET 核心视角）

### 3.1 可观测性（Observability）

| 工具 | 可观测能力 | 测试意义 |
|------|-----------|---------|
| **dsh** | 仅追加（append-only）事件日志：消息/工具调用/中间推理/Token 指标/子 Agent 派发全记录，可回放、隔离错误 | 最强，直接支撑过程追溯 |
| **Codex** | 日志 + citations + 审批信任档案 `.codex/approvals.json` | 审批行为分析 |
| **Claude Code** | session 历史、hooks、auto memory | 中等 |
| **Pi** | `pi-telemetry` 定义事件契约 + TUI 展示；事件流可被 Extension 拦截 | 契约清晰但需自行采集 |

### 3.2 可控制性（Controllability）

- **Pi**：Extension 可拦截 `tool_call`、注入上下文、自定义 compaction——控制粒度细，适合做「桩/拦截」式测试。
- **dsh**：插件即单元，可替换模型/工具/会话/UI。
- **Codex / Claude Code**：以 hooks 为主，控制面相对固定。

### 3.3 可断言性（Assertability）

- **Pi**：Print/JSON 与 RPC 输出结构化 JSON/JSONL，**可直接被 pytest 断言**——最大资产。
- **dsh**：事件日志统一结构格式，适合回放与基准对比。

### 3.4 可隔离性（Isolability）

- **Codex**：内核级沙箱（Seatbelt/Landlock），隔离最强。
- **Pi**：靠外挂 Gondolin/Docker/OpenShell。

> **结论**：Pi 的「可控制性 + 可断言性」顶尖、可观测性中等、可隔离性靠外部——最适合当**「可编程的测试驱动引擎」**，而 dsh 更适合当**「过程可追溯的被测对象」**。

## 四、实战：测试工程师怎么用 Pi

### 场景一：写一个「测试守护」Extension（最推荐入手）

注册 `run_tests` 工具 + 权限门控拦截危险命令（示意）：

```typescript
export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "run_tests",
    label: "Run Tests",
    description: "运行项目测试并返回结构化摘要",
    parameters: Type.Object({ path: Type.Optional(Type.String()) }),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      const result = { passed: 12, failed: 2, failures: ["test_login", "test_pay"] };
      return { content: [{ type: "text", text: `passed: ${result.passed}...` }], details: result };
    },
  });

  pi.on("tool_call", async (event, ctx) => {
    if (event.toolName === "bash" && event.input?.command?.includes("rm -rf")) {
      const ok = await ctx.ui.confirm("危险操作!", "确认执行 rm -rf?");
      if (!ok) return { block: true, reason: "用户拒绝" };
    }
  });
}
```

### 场景二：用 Print/JSON 模式接入 pytest / CI

```python
def test_pi_agent_produces_valid_json():
    out = subprocess.run(
        ["pi", "-p", "--json", "阅读 changes/ 下的变更，跑受影响用例并总结失败原因"],
        capture_output=True, text=True, timeout=120,
    ).stdout
    result = json.loads(out)
    assert "tool_calls" in result
    assert any("pytest" in str(t) for t in result["tool_calls"])
```

> ⚠️ print/JSON 模式具体 flag 以官方文档为准（示意代码）。

### 场景三：把 Pi 当作「被测对象」做 Agent 评测

四步走：定义任务集 → 注入输入（JSON/RPC 批量驱动）→ 采集轨迹（telemetry）→ 打分断言（结果正确性 + 过程合理性）。

评分维度：结果正确性（任务完成率/用例通过率）、过程合理性（工具调用冗余/越权）、安全合规（危险命令拦截率）、稳定性（重复一致性）。

## 五、四大 Agent 横向对比

### 5.1 总体速览

| 维度 | Pi | Claude Code | OpenAI Codex | DeepSeek Harness (dsh) |
|------|----|-------------|--------------|------------------------|
| 厂商/作者 | Armin Ronacher（Flask 作者） | Anthropic | OpenAI | DeepSeek |
| 开源 | ✅ MIT | ❌ 闭源（CLI） | ✅ Apache 2.0 | ✅ MIT（开发者预览） |
| 核心语言 | TypeScript | TypeScript | Rust（重写后） | 微内核 + 插件（Cordis） |
| 定位 | 极简 coding harness | 完整终端编码 Agent | 高性能终端编码 Agent | 微内核 Agent 运行时 |
| 主要模型 | 供应商中立（近 30 家） | Claude 系列 | GPT-Codex 系列 | DeepSeek 系列 |
| 首次发布 | 2025.08 | 2024.11 | 2025 中 | 2026.08.13 预览 |

### 5.2 相同点（底层范式高度一致）

终端优先、Agent Loop（感知→思考→工具→观察）、支持 MCP、支持 AGENTS.md/配置记忆、可编程平台化（Hooks/Extensions/Skills/SDK）、争夺 Agent 协议层（ACP/JSON-RPC）。

### 5.3 关键差异（含测试视角）

| 差异点 | Pi | Claude Code | Codex | dsh |
|--------|----|-------------|-------|-----|
| 设计哲学 | 极简核心 + 完全扩展 | 开箱即用全家桶 | 高性能 + 内核安全 | 微内核 + 一切皆插件 |
| 性能 | 中（TS） | 中（TS） | 最强（Rust，180ms/28MB/1000+ tok/s） | 中（思链折叠显快） |
| 安全模型 | 无内置（外部方案） | 应用层审批 | 内核级沙箱（最强） | 审批 + 守卫 + 凭据隔离 |
| 模型绑定 | 中立（近 30 家） | 绑定 Claude | 绑定 GPT | 中立（DeepSeek + OpenAI 兼容） |
| 可观测性 | 契约清晰，需自行采集 | 中（hooks/memory） | 中（citations/信任档案） | 最强（仅追加事件日志） |
| 可控制性 | 细（Extension 拦截） | 中（hooks） | 中（hooks） | 强（插件可替换） |
| 可断言性 | 强（JSON/RPC 输出） | 中 | 中 | 强（统一事件结构） |
| 子代理 | 不内置 | 成熟（团队编排） | GA（worktree 隔离） | Standard 含派发 |

## 六、各自优缺点

| 工具 | 优点 | 缺点 |
|------|------|------|
| **Pi** | 极简哲学、五层扩展、模型中立、JSON/RPC/SDK 集成最强、MIT 开源 | 无内置权限、无子代理/plan mode、性能不如 Rust、核心留白 |
| **Claude Code** | 代码质量口碑领先、生态最成熟、全流程闭环、企业支持完善 | 闭源、绑定 Claude、token 消耗高（约 Codex 3-4 倍）、启动偏重 |
| **Codex** | 性能最强、安全最强（内核级沙箱）、成本最低、CI 友好、开源 | 绑定 GPT、真实 bug 修复略逊 CC、输出啰嗦、迭代过快 |
| **dsh** | 微内核扩展天花板高、可追溯性最强、社区爆发（5 天 13.5 万星）、模型中立 | 开发者预览（0.1.x）契约可能变、插件生态刚起步、需配合 DeepSeek 模型 |

### 选型建议

| 你的需求 | 推荐 |
|---------|------|
| 极致可定制、模型中立、自己拼装测试工具 | **Pi** |
| 开箱即用、代码质量最好、生态最全 | **Claude Code** |
| 性能最强、最安全、最省钱、上 CI | **OpenAI Codex** |
| 研究 Agent 架构、过程可追溯、插件生态 / DeepSeek 模型 | **dsh** |

## 七、测试面试考点

- **Q1 什么是 coding harness？** harness 是「驱动 + 脚手架」层，类比 pytest：核心只负责发现与执行，插件机制才是生态。
- **Q2 如何对 Agent 做「过程可追溯」的测试？** 事件/轨迹采集：dsh 仅追加事件日志、Pi telemetry 事件契约；记录 tool_call + 中间推理，做到回放/错误隔离/跨模型基准对比/审计合规。
- **Q3 对「无内置权限系统」的 Agent（如 Pi）安全测试怎么做？** 测试点就在边界：危险命令拦截、敏感路径保护（.env/node_modules）、凭据隔离、越权/逃逸尝试。
- **Q4 模型中立 vs 模型绑定对测试有什么影响？** 中立工具可做跨模型 A/B 对比评测；绑定工具难做纯模型维度的对照实验。先想清楚测的是「工具」还是「模型」。

## 八、练习任务

- 安装 Pi 跑通第一个会话
- 手写 `run_tests` Extension 让 Agent 调用 pytest 返回结构化结果
- 用 print/JSON 模式非交互跑任务，思考可断言字段
- 阅读 `pi-telemetry` 事件契约，理解 telemetry 如何用于测试断言
- 对比 dsh 仅追加日志与 Pi telemetry，写「过程可追溯」测试方案
- 针对 Pi 权限边界列 3 条安全测试用例
- 用 Pi 与绑定模型工具做一次 A/B 评测

## 🔗 关联文档

- [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点|AI 产品测试概念版]] — LLM 评测原理与框架选型
- [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点-进阶版|eval 体系工程化]] — 三层评分器、五维评测、双套件
- [[wiki/语雀/claude-code/Claude Code学习笔记|Claude Code学习笔记]] — CC 生态（subagents/CLAUDE.md/hooks/MCP）
- [[wiki/语雀/claude-code/Harness Engineering（驾驭工程）|Harness Engineering]] — Agent 设计原则、四大护栏
- [[wiki/语雀/ai-basics/RAG学习笔记|RAG学习笔记]]
- [[wiki/软件测试学习资料/16_AI_UI自动化_browser-use二次开发学习资料|browser-use 二次开发]]
- [[wiki/软件测试学习资料/11_Agent测试必背学习资料|11_Agent测试必背]]

## 来源

- `.raw/AI相关学习资料/Pi与AI编程Agent对比分析.html`（2026-08-27）
- Pi 官方仓库：github.com/earendil-works/pi；文档：pi.dev/docs/latest
- Claude Code：code.claude.com/docs；Codex：github.com/openai/codex；dsh：github.com/deepseek-ai/deepseek-harness
- ⚠️ Stars/版本/性能指标为 2026-08-27 时点快照，迭代极快，以官方仓库为准

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[AI产品测试进阶路线与面试考点-进阶版]] — AI测试主题关联
- [[16_AI_UI自动化_browser-use二次开发学习资料]] — AI测试主题关联
- [[AI产品测试进阶路线与面试考点]] — AI测试主题关联
- [[Claude Code学习笔记]] — AI测试主题关联
- [[AI产品测试]] — AI测试主题关联
- [[11_Agent测试必背学习资料]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[邓万鹏-AI自动化测试]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
