---
type: note
title: "AI 产品测试进阶版：eval 体系工程化落地"
source: ".raw/AI相关学习资料/AI产品测试进阶路线与面试考点-进阶版.md"
created: 2026-08-27
updated: 2026-08-27
tags:
  - AI测试
  - eval体系
  - LLM评测
  - Agent
  - 面试考点
status: live
---

# AI 产品测试进阶版：eval 体系工程化落地

> 面向测试开发工程师（SDET）的进阶增量资料，聚焦**工程化落地层**。与概念版 [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点|AI产品测试进阶路线与面试考点（概念版）]] 的分工：概念版覆盖概念层（LLM 评测原理、RAG 指标、Agent 四维、框架选型），本页覆盖工程化落地层（三层评分器、五维评测、双套件、基线管理、稳定性评估、成本画像、安全对抗、可观测性）。

## 0. 一句话总纲（面试开场白）

AI 测试的核心命题，是把传统测试的「精确断言」替换为 **「指标 + 阈值 + 评测集」**，把「单点测试用例」升级为 **「评测（eval）体系」**。

完整的一句话：**Eval = Agent 输入 → 执行 → 捕获 Trace + 产物 → 一组检查规则 → 可对比的分数**，目标是建立一个「可重复、可量化、可持续演进」的评估闭环。

## 一、进阶学习路线（四阶段，概念层之上的工程化递进）

### 阶段一 · LLM 评测原理 → 建立正确认知（基础，你已有 70%）

| 主题 | 关键动作 |
|------|---------|
| 非确定性认知 | 理解输出是概率分布，正确性是统计性的 |
| 幻觉分类 | 内在幻觉 vs 外在幻觉 |
| LLM-as-a-Judge | 理解三类偏差（position/verbosity/self-preference） |
| 黄金评测集 | golden dataset 构建，含边界 + 对抗用例 |

**动手任务**：用 DeepEval 写第一个评测，跑 `HallucinationMetric` / `AnswerRelevancyMetric`。

### 阶段二 · eval 体系工程化（核心进阶点）

1. **三层评分器（谁来评）**
   - 确定性评分器（脚本/断言/Lint/AST）：负责所有「能用代码判断」的事，P0 主战场。
   - Rubric 评分器（LLM-as-a-Judge + Prompt + JSON Schema）：负责「代码搞不定但能结构化描述」的软指标。
   - 人工评分器（领域专家）：黄金标准，只做校准、诊断、兜底。
   - **铁律**：能用代码判断的绝不用模型；模型用于软指标；人工只做校准（与 LLM 评委对齐，一致率 ≥ 85%）。

2. **五维评测（评什么）**
   - P0 功能正确性、P0 鲁棒性与安全、P1 过程质量、P1 效率与成本、P2 体验与对齐。

3. **能力/回归双套件（怎么运营）**
   - 能力测评（Capability）：起步通过率 20–50%，目标山峰，频繁迭代。
   - 回归测评（Regression）：接近 100%，防御漂移，只增不减，CI 每次跑。
   - 通过率稳定 100% 后「毕业」进回归套件；线上 Bad Case 反哺能力套件。

4. **基线管理**
   - 基线 = 单用例执行 1 次 + 人工确认的「预期过程 + 预期结果」快照。
   - 先跑出来，再确认，确认后就是预期——不手写黄金答案。
   - 基线更新时机：Agent 逻辑变更 / 模型升级 / 用例修改。

5. **稳定性评估（pass^k vs pass@k）**
   - `pass@k`：k 次至少 1 次通过 → 峰值能力。
   - `pass^k`：k 次全部通过 → 稳定性/一致性。
   - 容忍阈值按 Agent 类型分三档：关键决策 0% / 辅助分析 ≤10% / 创意生成 ≤40%。
   - 调试技巧：0% 通过率通常说明「任务定义有问题」，不是模型弱。

**动手任务**：选一个 E9 接口自动化场景，抽象成「确定性评分器为主」的最小 eval 闭环（输入 → 执行 → Trace → 检查规则 → 分数）。

### 阶段三 · RAG 评测（把检索器与生成器分离测）

- 五指标：Faithfulness / Answer Relevancy / Context Precision / Context Recall / Answer Correctness。
- **分层口诀**：Precision/Recall 测检索器，Faithfulness/Relevancy 测生成器，Correctness 测端到端。
- **分离测试（component-wise）**：检索召回高但回答错 → 生成器/prompt 问题；忠实度低但检索相关 → 生成没用好上下文。

### 阶段四 · Agent 评测（多步、工具、环境反馈）

- Agent vs 纯 LLM 的本质区别：多轮交互 + 工具调用 + 环境状态变化。
- 前置依赖：**被测 Agent 必须输出结构化 Trace**（JSONL/JSON），否则只能做结果评测。
- 核心指标：任务完成率 / success rate / pass@k / pass^k / 工具调用正确性。
- 可观测性：LangSmith / Langfuse / Phoenix 做轨迹追踪（tracing）。
- 安全对抗：prompt injection 红队、越权/越界、错误级联放大。

## 二、技术栈迁移对照（你的存量能力复用）

| 你已掌握 | 迁移到 eval 体系 |
|---------|----------------|
| pytest | 评测用例 = 测试函数 + 指标断言 + 阈值门禁；DeepEval 就是「LLM 的 pytest」 |
| requests / 接口断言 | 转成「指标阈值 gate」+ 回归评测集；断言思维迁移到「确定性评分器」 |
| Playwright / Selenium | Agent 浏览器任务评测（browser-use / WebArena 类） |
| mitmproxy 抓包 | mock 控制 LLM 外部依赖，做确定性测试 / 故障注入 |
| Jenkins / CI | 评测作为独立 pipeline 阶段，每次 push 跑门禁 |
| Docker | 环境隔离（每次评测 clone 仓库，git checkout . && git clean -fd） |
| LangChain / SKILL | Agent 编排 + 提示词工程，落地 AI 自动化测试 |

## 三、面试考点（10 个，考点 → 考察点 → 答题要点）

### 考点 1：给你一个 LLM 产品，怎么从 0 搭一套 eval 体系？（开放设计题，必考）

六步：定目标（P0/P1/P2 优先级）→ 建评测集（黄金 + 边界 + 对抗）→ 选评分器（确定性 > Rubric > 人工）→ 设门禁（阈值 + 容差带）→ 建基线 → 上线监控（采样 + 漂移监控）。

**加分句**：分层——开发期用评测框架（DeepEval/Promptfoo）做门禁，生产期用可观测平台（LangSmith/Phoenix）做持续监控，两套并行。

### 考点 2：为什么要用「三层评分器」而不是单一的 LLM-as-a-Judge？

单一 LLM-judge：**贵**（每次 API 调用）、**抖**（非确定性）、**有偏差**（position/verbosity/self-preference）。成熟团队按需组合：P0 硬指标走代码，P1 软指标走模型，校准和异常诊断走人。

### 考点 3：怎么把 eval 接入 CI，又不被 LLM 的非确定性搞崩？

- 用**容差带**（如 faithfulness ≥ 0.7 且不较上次下降超 0.05），不用精确阈值。
- 固定 judge 模型版本（pin version）、固定黄金评测集、稳定采样。
- 评测作为独立 pipeline 阶段，跑在每次 push，超阈值才 fail。
- 环境隔离：每次 clone 仓库到临时目录，执行前 reset，产物归档。

### 考点 4：能力测评和回归测评有什么区别？为什么要分两套？

能力测评回答「能把什么做好」（起步 20–50%，目标山峰，频繁迭代）；回归测评回答「原有能力还在吗」（接近 100%，防漂移，只增不减）。混为一套会既遮住能力进步、又放过回归退化。生命周期：稳定 100% 毕业进回归；线上 Bad Case 沉淀为新能力用例。

### 考点 5：什么是基线？它和「黄金答案」有什么区别？

基线 = 单用例执行 1 次 + 人工确认的「预期过程 + 预期结果」快照。黄金答案是手写的「标准答案」；基线是「先跑出来，再确认」的真实执行快照（含完整 Trace）。好处：不预设预期过程，避免「我以为对」的偏差，支持过程评测。

### 考点 6：pass@k 和 pass^k 的区别？

`pass@k` = k 次至少 1 次通过 → **峰值能力**；`pass^k` = k 次全部通过 → **稳定性/一致性**。只测 pass@k 会放过「偶尔成功但经常翻车」的 Agent。经验：N=5——全过=稳定；1/5 失败=存在幻觉；≥2/5 失败=排查 prompt/评分器/逻辑；0/5=先查任务定义。

### 考点 7：为什么要给每个任务做「成本画像」？

一个 pass@1 高但 token 花 10 倍的方案，生产上不可接受。五要素：Token 消耗（avg/p95）、工具调用次数、端到端延迟（p50/p95/p99）、失败重试率、单任务成本（Token × 单价 → ¥/task）。没有历史成本基线，线上变贵变慢时无法定位原因。

### 考点 8：Agent 的安全测试怎么测？（prompt injection + 越权）

抗注入（红队）、越权/越界（权限断言）、合规（PII 不泄露）、拒绝合理性（误拒/漏拒 %）、幻觉率（事实核查）、出错级联放大（Trace 追踪定位）。

### 考点 9：评测框架怎么选？（DeepEval / RAGAS / Promptfoo / LangSmith）

DeepEval = 开发期评测库（pytest 风格，指标最全）；RAGAS = RAG 专用指标（无需 ground truth）；Promptfoo = CI 门禁 + 红队/多模型对比（YAML 声明式）；LangSmith = 生产期追踪 + 评测平台。**避坑**：HELM/lm-eval-harness/MMLU-Pro 是选基座模型的。

### 考点 10：被测 Agent 不支持结构化 Trace 怎么办？

三档：可改造 → 推动 Agent 侧增加 Trace 输出（标准做法）；有日志但非结构化 → 写解析器提取（成本高、易碎）；仅有最终输出 → 只能做结果评测。**加分句**：结构化 Trace 不仅服务测评，也利于线上排查和可观测性建设。

## 四、一页速记卡（考前 10 分钟过一遍）

- **一句话总纲**：指标 + 阈值 + 评测集 替代 精确断言；Eval = 输入 → 执行 → Trace → 检查规则 → 分数。
- **三层评分器**：确定性（代码）> Rubric（LLM-judge）> 人工（校准/诊断/兜底）。
- **五维评测**：功能正确性 P0、鲁棒性安全 P0、过程质量 P1、效率成本 P1、体验对齐 P2。
- **双套件**：能力测评（20–50% 起步）→ 稳定 100% 毕业 → 回归测评（接近 100%，防漂移）。
- **基线**：跑 1 次 + 人工确认 = 预期快照，不手写黄金答案。
- **稳定性**：pass@k=峰值能力，pass^k=稳定性；容忍阈值 0% / ≤10% / ≤40% 三档。
- **RAG 分层**：Precision/Recall 测检索，Faithfulness/Relevancy 测生成，Correctness 测端到端。
- **CI 防 flaky**：容差带 + pin judge 版本 + 固定评测集。
- **成本画像**：token / 工具调用 / p95 延迟 / 重试率 / ¥/task。
- **框架**：开发用 DeepEval/Promptfoo，生产用 LangSmith/Phoenix；别混淆「评测应用」和「基准测评」。

## 五、阶段学习资源建议

| 阶段 | 推荐资源 |
|------|---------|
| eval 体系方法论 | Anthropic《Demystifying evals for AI agents》《Evaluating AI agents》；OpenAI《Eval skills》 |
| 落地实战 | 腾讯 TEG 网关测试团队《AI Agent 与 Skill 测评方案及落地实践》 |
| 框架 | DeepEval / RAGAS / Promptfoo / LangSmith 官方文档 |
| RAG 指标 | RAGAS 官方论文与文档 |
| Agent 追踪 | LangSmith / Langfuse / Arize Phoenix |

## 🔗 关联文档

- [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点|概念版：LLM 评测原理与框架选型]] — 概念层，本页的配套
- [[wiki/AI相关学习资料/Pi与AI编程Agent对比分析|Pi 与 AI 编程 Agent 对比分析]] — 把 Agent 当「被测对象」做行为评测与安全测试
- [[wiki/语雀/learning/AI产品测试|AI产品测试（语雀）]] — 早期 eval 体系搭建笔记
- [[wiki/软件测试学习资料/AI Agent与Skill测评方案及落地实践|AI Agent 与 Skill 测评方案及落地实践]] — 腾讯 TEG 实战
- [[wiki/软件测试学习资料/13_AI产品测试方法论学习资料|13_AI产品测试方法论]]
- [[wiki/软件测试学习资料/15_AI接口自动化SKILL系统学习资料|15_AI接口自动化SKILL]]
- [[wiki/语雀/ai-basics/RAG学习笔记|RAG学习笔记]]
- [[wiki/语雀/api-automation/通过AI实现全流程的接口自动化|全流程接口自动化]]

## 来源

- `.raw/AI相关学习资料/AI产品测试进阶路线与面试考点-进阶版.md`（2026-08-27）
- 框架定位参考 2026 年公开评测框架对比资料；指标定义以 RAGAS / DeepEval 官方文档为准
- 建议结合 E9 接口自动化项目，把「阈值门禁 + 回归评测集 + 三层评分器」理念迁移验证

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[AI产品测试进阶路线与面试考点]] — AI测试主题关联
- [[Pi与AI编程Agent对比分析]] — AI测试主题关联
- [[AI产品测试]] — AI测试主题关联
- [[13_AI产品测试方法论学习资料]] — AI测试主题关联
- [[15_AI接口自动化SKILL系统学习资料]] — AI测试主题关联
- [[通过AI实现全流程的接口自动化]] — AI测试主题关联
- [[AI Agent与Skill测评方案及落地实践]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
