---
type: index
title: "AI 相关学习资料"
created: 2026-08-27
updated: 2026-10-15
tags:
  - AI
  - 学习资料
status: live
---

# AI 相关学习资料

来自 `.raw/AI相关学习资料/` 目录的进阶学习资料，按主题归档。

## 📄 页面索引

### 大模型基础

- [[wiki/AI相关学习资料/大模型核心原理|大模型核心原理]] — Transformer/Attention/Token/训练三阶段，LLM 底层机制入门
- [[wiki/AI相关学习资料/大模型必学基础知识|大模型必学基础知识]] — 四层知识体系（基础/控制/扩展/评测），采样参数、提示词与上下文工程、Agent/Skill/MCP、RAG、评测七维

### AI 编码 Agent 调研

- [[wiki/AI相关学习资料/AI编码Agent五工具对比分析报告|AI 编码 Agent 五工具对比分析报告]] — OMP / Pi / DSH / Claude Code / Codex 横向对比
- [[wiki/AI相关学习资料/Pi与AI编程Agent对比分析|Pi 与 AI 编程 Agent 对比分析]] — Pi 极简 Coding Harness 学习指南，四大 Agent 横向对比与可测性分析
- [[wiki/AI相关学习资料/Pi的AI设计经验|Pi 的 AI 设计经验]] — 九包架构、faux provider（模型无关测试）、evals 框架
- [[wiki/AI相关学习资料/Pi源码精读顺序清单|Pi 源码精读顺序清单]] — L0–L9 分层阅读路径
- [[wiki/AI相关学习资料/OMP使用手册|OMP 使用手册]] — oh-my-pi 安装、配置、模型接入与日常使用
- [[wiki/AI相关学习资料/OMP的设计经验|OMP 的设计经验]] — OMP 架构设计取舍与生态兼容性

### AI 测试工具（Jev / REA）

- [[wiki/AI相关学习资料/Jev决策模型(System One)学习参考资料|Jev 决策模型（System One）]] — 卡尼曼双系统认知模型的工程化：state 输入、三种决策原语、置信度输出、RLCD 训练目标
- [[wiki/AI相关学习资料/Jev用于UI自动化测试可行性分析与AI测试工具横向对比|Jev 用于 UI 自动化测试可行性分析与 AI 测试工具横向对比]] — Jev 是「动作决策层」而非视觉大脑；三大工具横向对比与选型决策
- [[wiki/AI相关学习资料/TypeSafe_Jev国内使用指南(官网导航+四条接入路径+实测连通性)|TypeSafe Jev 国内使用指南]] — 四条接入路径、官网导航与实测连通性数据
- [[wiki/AI相关学习资料/REA逆向工程MCP工具学习手册|REA 逆向工程 MCP 工具学习手册]] — REA（CLI + MCP Server 双形态）逆向工具、MCP 协议接入与官方案例实操

### AI 测试与工程范式

- [[wiki/AI相关学习资料/测试开发如何使用DSH|测试开发如何使用 DSH]] — 五大测试领域的 DSH 落地方案
- [[wiki/AI相关学习资料/Graph Engineering从概念到测试落地|Graph Engineering：从概念到测试落地]] — Loop→Graph 范式跃迁、四大负向优化陷阱、三大防线、测试落地四场景
- [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点|AI 产品测试进阶路线与面试考点（概念版）]] — LLM 评测原理、RAG 指标、Agent 四维、框架选型、13 个面试考点
- [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点-进阶版|进阶版：eval 体系工程化落地]] — 三层评分器、五维评测、双套件、基线管理、10 个进阶考点

### AI 应用工程（RAG / Ontology）

- [[wiki/AI相关学习资料/RAG的流程与应用|RAG 的流程与应用]] — 六层工程链路（价值层→数据层→向量层→存储层→内核层→实战层），重点在向量检索内核 IndexFlatL2 / IVF-PQ / HNSW
- [[wiki/AI相关学习资料/Ontology本体工程从概念到企业流程与测试流程落地|Ontology 本体工程：从概念到企业流程与测试流程落地]] — 语义网技术栈、RDF 三元组与 IRI、本体驱动工作流转换、本体约束推理评测与测试落地

### 工程效能与基础设施

- [[wiki/AI相关学习资料/Anthropic源代码控制系统重设计|Anthropic 源代码控制系统重设计]] — AI 让合并量 4 个月涨 10 倍后 git 触顶；Scion 重造：changeset 结构、三级缓存、检出快两个数量级
- [[wiki/AI相关学习资料/AI工具资源占用沟通与面试应答|AI 工具资源占用：向上沟通话术与面试应答]] — 界面底座/任务执行/上下文管理三层成本拆解，含实测数据与减负清单

## 🔗 关联文档

- [[wiki/语雀/learning/AI产品测试|AI产品测试（语雀）]] — LLM 产品测试经验与 eval 体系搭建的早期笔记
- [[wiki/软件测试学习资料/13_AI产品测试方法论学习资料|13_AI产品测试方法论]] — 面试八股文中的 AI 产品测试方法论
- [[wiki/软件测试学习资料/10_RAG测试必背学习资料|10_RAG测试必背]] — RAG 评测指标
- [[wiki/软件测试学习资料/11_Agent测试必背学习资料|11_Agent测试必背]] — Agent 评测指标
- [[wiki/软件测试学习资料/16_AI_UI自动化_browser-use二次开发学习资料|16_browser-use 二次开发]] — Agent 浏览器任务评测
- [[wiki/软件测试学习资料/09_AI测试基础学习资料|09_AI测试基础]] — AI 测试基础概念
- [[wiki/软件测试学习资料/15_AI接口自动化SKILL系统学习资料|15_AI 接口自动化 SKILL]] — 奖励黑客（Reward Hacking）问题的工程背景
- [[wiki/测试开发相关学习资料/JaCoCo代码覆盖率工具从入门到工程落地|JaCoCo 代码覆盖率]] — AI 补测闭环的数据输入源
- [[wiki/测试开发相关学习资料/index|测试开发相关学习资料索引]]
- [[wiki/语雀/ai-basics/RAG学习笔记|RAG学习笔记]] — RAG 架构与检索器
- [[wiki/语雀/ai-basics/AI大模型基础知识|AI大模型基础知识]] — LLM 原理与 Transformer 架构
- [[wiki/语雀/claude-code/Harness Engineering（驾驭工程）|Harness Engineering]] — Agent 设计原则
- [[wiki/语雀/claude-code/Loop Engineering（循环工程）|Loop Engineering]] — Graph Engineering 的前置范式
- [[wiki/语雀/claude-code/Claude Code学习笔记|Claude Code]]
- [[wiki/笔记/用Obsidian+Claude Code解决Git推送问题的实战记录|实战记录]]

## 源文件

- `.raw/AI相关学习资料/大模型核心原理.md`
- `.raw/AI相关学习资料/大模型必学基础知识.md`
- `.raw/AI相关学习资料/AI编码Agent五工具对比分析报告.md`
- `.raw/AI相关学习资料/pi/OMP使用手册.md`
- `.raw/AI相关学习资料/pi/OMP的设计经验.md`
- `.raw/AI相关学习资料/pi/Pi的AI设计经验.md`
- `.raw/AI相关学习资料/pi/Pi源码精读顺序清单.html`
- `.raw/AI相关学习资料/测试开发如何使用DSH.md`
- `.raw/AI相关学习资料/Graph Engineering从概念到测试落地.md`
- `.raw/AI相关学习资料/AI产品测试进阶路线与面试考点.html`
- `.raw/AI相关学习资料/AI产品测试进阶路线与面试考点-进阶版.md`
- `.raw/AI相关学习资料/pi/Pi与AI编程Agent对比分析.html`
- `.raw/AI相关学习资料/AI工具资源占用沟通与面试应答.md`
- `.raw/AI相关学习资料/Anthropic源代码控制系统重设计.md`
- `.raw/AI相关学习资料/Ontology本体工程从概念到企业流程与测试流程落地.md`
- `.raw/AI相关学习资料/RAG的流程与应用.md`
- `.raw/AI相关学习资料/REA逆向工程MCP工具学习手册.md`
- `.raw/AI相关学习资料/jev/Jev决策模型(System One)学习参考资料.md`
- `.raw/AI相关学习资料/jev/Jev用于UI自动化测试可行性分析与AI测试工具横向对比.md`
- `.raw/AI相关学习资料/jev/TypeSafe_Jev国内使用指南(官网导航+四条接入路径+实测连通性).md`

<!-- AUTO-CATALOG:START -->

## 自动页面目录

- [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点|AI产品测试进阶路线与面试考点]] — AI 产品测试进阶路线与面试考点（概念版）
- [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点-进阶版|AI产品测试进阶路线与面试考点-进阶版]] — AI 产品测试进阶版：eval 体系工程化落地
- [[wiki/AI相关学习资料/AI工具资源占用沟通与面试应答|AI工具资源占用沟通与面试应答]] — AI 工具资源占用：向上沟通话术与面试应答
- [[wiki/AI相关学习资料/AI编码Agent五工具对比分析报告|AI编码Agent五工具对比分析报告]] — AI 编码 Agent 五工具对比分析报告
- [[wiki/AI相关学习资料/Anthropic源代码控制系统重设计|Anthropic源代码控制系统重设计]] — Anthropic 源代码控制系统重设计（Scion）
- [[wiki/AI相关学习资料/Graph Engineering从概念到测试落地|Graph Engineering从概念到测试落地]] — Graph Engineering：从 Loop 到 Graph 的范式跃迁及测试落地
- [[wiki/AI相关学习资料/Jev决策模型(System One)学习参考资料|Jev决策模型(System One)学习参考资料]] — Jev 决策模型（System One）学习参考资料
- [[wiki/AI相关学习资料/Jev用于UI自动化测试可行性分析与AI测试工具横向对比|Jev用于UI自动化测试可行性分析与AI测试工具横向对比]] — Jev 用于 UI 自动化测试：可行性分析与 AI 测试工具横向对比
- [[wiki/AI相关学习资料/OMP使用手册|OMP使用手册]] — OMP（oh-my-pi）使用手册
- [[wiki/AI相关学习资料/OMP的设计经验|OMP的设计经验]] — OMP 的设计经验
- [[wiki/AI相关学习资料/Ontology本体工程从概念到企业流程与测试流程落地|Ontology本体工程从概念到企业流程与测试流程落地]] — Ontology 本体工程：从概念到企业流程与测试流程落地
- [[wiki/AI相关学习资料/Pi与AI编程Agent对比分析|Pi与AI编程Agent对比分析]] — Pi 与 AI 编程 Agent 对比分析
- [[wiki/AI相关学习资料/Pi源码精读顺序清单|Pi源码精读顺序清单]] — Pi 源码精读顺序清单
- [[wiki/AI相关学习资料/Pi的AI设计经验|Pi的AI设计经验]] — Pi 的 AI 设计经验
- [[wiki/AI相关学习资料/RAG的流程与应用|RAG的流程与应用]] — RAG 的流程与应用：六层工程链路与检索内核
- [[wiki/AI相关学习资料/REA逆向工程MCP工具学习手册|REA逆向工程MCP工具学习手册]] — REA：逆向工程 MCP 工具学习手册
- [[wiki/AI相关学习资料/TypeSafe_Jev国内使用指南(官网导航+四条接入路径+实测连通性)|TypeSafe_Jev国内使用指南]] — TypeSafe Jev 国内使用指南：官网导航 + 四条接入路径 + 实测连通性
- [[wiki/AI相关学习资料/大模型必学基础知识|大模型必学基础知识]] — 大模型必学基础知识
- [[wiki/AI相关学习资料/大模型核心原理|大模型核心原理]] — 大模型核心原理
- [[wiki/AI相关学习资料/测试开发如何使用DSH|测试开发如何使用DSH]] — 测试开发如何使用DSH

<!-- AUTO-CATALOG:END -->
