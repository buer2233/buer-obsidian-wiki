---
type: note
title: "AI 产品测试进阶路线与面试考点（概念版）"
source: ".raw/AI相关学习资料/AI产品测试进阶路线与面试考点.html"
created: 2026-08-27
updated: 2026-08-27
tags:
  - AI测试
  - LLM评测
  - RAG
  - Agent
  - 面试考点
status: live
---

# AI 产品测试进阶路线与面试考点（概念版）

> 面向测试开发工程师（SDET）的进阶路径梳理，覆盖 **LLM 评测原理 → RAG 工程与评测 → Agent 架构与测试** 三阶段的概念层。工程化落地层（三层评分器、五维评测等）见 [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点-进阶版|进阶版：eval 体系工程化落地]]。

## 一、核心认知：为什么 AI 测试不一样

传统软件是确定性的：输入 A 必然输出 B。而 LLM 是**概率性、非确定性**的——正确性是一个分布而非二值，失败模式是「安静失败」（confident wrong answer）。

核心命题：**用「指标 + 阈值 + 评测集」替代「精确断言」，用「评测（eval）体系」替代「单点测试用例」**。

## 二、进阶学习路线（三阶段）

### 阶段一 · LLM 基础与评测原理

- LLM 生成机制与不确定性来源（temperature/top-p 采样）
- 幻觉检测（内在幻觉 vs 外在幻觉）
- 一致性评估
- 传统指标 BLEU / ROUGE / BERTScore 及局限
- LLM-as-a-Judge 与 G-Eval 评分法
- golden dataset（黄金评测集）构建
- 离线评测 vs 在线评测

### 阶段二 · RAG 工程与评测

- RAG 链路：检索器（Retriever）+ 生成器（Generator）
- 检索质量：Recall / Precision
- Faithfulness（忠实度）、Answer Relevancy（回答相关性）
- RAGAS 五指标体系
- 检索器与生成器**分离测试**（component-wise）

### 阶段三 · Agent 架构与测试

- Agent 与纯 LLM 评测的本质区别（多轮交互 + 工具调用 + 环境状态变化）
- 任务完成率 / success rate / pass@k / pass^k
- 工具调用正确性、轨迹追踪（LangSmith / Langfuse / Phoenix）
- 多 Agent 协作验证（MultiAgentBench / MARBLE）
- AI 自动化测试（browser-use）、prompt injection 安全对抗

## 三、技术栈迁移对照

| 你已掌握 | 迁移到 AI 测试 |
|---------|--------------|
| pytest / requests | DeepEval = 「LLM 的 pytest」；评测用例 = 测试函数 + 指标断言 |
| Playwright / Selenium | Agent 浏览器自动化（browser-use / WebArena） |
| mitmproxy 抓包 | mock 控制 LLM 外部依赖，做确定性测试 |
| LangChain / SKILL | Agent 编排与提示词工程 |
| 接口断言思维 | 「指标阈值门禁」+ 回归评测集 |

## 四、面试考点摘要（13 个）

1. **LLM 测试 vs 传统测试**：非确定性 → 指标 + 阈值 + 评测集
2. **幻觉检测**：内在 vs 外在，DeepEval HallucinationMetric / RAGAS Faithfulness
3. **离线 vs 在线评测**：离线做门禁（发布前），在线做监控（上线后），互相反哺
4. **LLM-as-a-Judge 三类偏差**：位置 / 冗长 / 自偏好；缓解靠固定 rubric + 换序 + 固定模型版本 + 人工校准
5. **BLEU/ROUGE/BERTScore 局限**：词面重叠，适合翻译/摘要，不适合开放问答
6. **RAGAS 五指标**：Faithfulness / Answer Relevancy / Context Precision / Context Recall / Answer Correctness
7. **RAG 问题定位**：分离测试——Precision/Recall 测检索器，Faithfulness/Relevancy 测生成器
8. **Agent vs 纯 LLM 评测**：行为 / 能力 / 可靠性 / 安全对齐 四维
9. **可靠性与工具调用**：pass^k 测一致性；轨迹追踪检查每一步 action
10. **多 Agent 协作**：Coordination Score，MultiAgentBench / MARBLE 基准
11. **从 0 搭 eval 体系**：六步法（定目标 → 建评测集 → 选指标框架 → 阈值门禁 → judge 校准 → 线上监控）
12. **eval 接入 CI 不被 flaky 搞崩**：容差带 + pin judge 版本 + 固定评测集
13. **框架选型**：DeepEval=开发期库，RAGAS=RAG 专用，Promptfoo=CI 门禁+红队，LangSmith=生产期追踪；**区分「评测应用」和「基准测评」**

## 五、框架选型速查（2026）

| 框架 | 定位 | 开源 |
|------|------|------|
| DeepEval | 开发期评测库（「LLM 的 pytest」） | Apache 2.0 |
| RAGAS | RAG 专用指标 | Apache 2.0 |
| Promptfoo | CI-first、红队、多模型对比 | MIT |
| LangSmith | 生产期追踪 + 评测平台 | 商业 |
| Braintrust | 商业评测平台 | 商业 |
| Arize Phoenix | 可观测 + 评测 | 开源核心 |
| lm-eval-harness | **基座模型**基准（非应用评测） | MIT |

> ⚠️ **避坑**：HELM / lm-eval-harness / MMLU-Pro 是选基座模型的，不是评价应用好坏的——面试官爱挖的坑。

## 🔗 关联文档

- [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点-进阶版|进阶版：eval 体系工程化落地]] — 概念层之上的工程化（三层评分器、五维评测、双套件、基线）
- [[wiki/AI相关学习资料/Pi与AI编程Agent对比分析|Pi 与 AI 编程 Agent 对比分析]] — 从「被测对象」视角评测编码 Agent
- [[wiki/语雀/learning/AI产品测试|AI产品测试（语雀）]] — LLM 产品测试经验与 eval 体系搭建早期笔记
- [[wiki/软件测试学习资料/13_AI产品测试方法论学习资料|13_AI产品测试方法论]]
- [[wiki/软件测试学习资料/10_RAG测试必背学习资料|10_RAG测试必背]]
- [[wiki/软件测试学习资料/11_Agent测试必背学习资料|11_Agent测试必背]]
- [[wiki/语雀/ai-basics/RAG学习笔记|RAG学习笔记]]
- [[wiki/语雀/ai-basics/AI大模型基础知识|AI大模型基础知识]]

## 来源

- `.raw/AI相关学习资料/AI产品测试进阶路线与面试考点.html`（2026-08-27 抓取）
- 框架定位参考 2026 年公开评测框架对比资料；指标定义以 RAGAS / DeepEval 官方文档为准

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[AI产品测试进阶路线与面试考点-进阶版]] — AI测试主题关联
- [[Pi与AI编程Agent对比分析]] — AI测试主题关联
- [[AI产品测试]] — AI测试主题关联
- [[11_Agent测试必背学习资料]] — AI测试主题关联
- [[13_AI产品测试方法论学习资料]] — AI测试主题关联
- [[10_RAG测试必背学习资料]] — AI测试主题关联
- [[AI大模型基础知识]] — AI测试主题关联
- [[RAG学习笔记]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
