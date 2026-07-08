# 语雀知识库索引

来源：https://www.yuque.com/bbuer/ebdyfe
抓取时间：2026-07-01

---

## 📊 知识库概览

- **文档总数：** 26篇
- **知识领域：** AI大模型、自动化测试、Claude Code、LangChain、RAG、Agent
- **核心主题：** AI驱动的接口自动化测试、VibeCoding实践、Harness Engineering

---

## 🗂️ 文档分类索引

### 一、AI基础知识（3篇）

| 文档 | 主题 | 关联文档 |
|------|------|---------|
| [[AI大模型基础知识]] | LLM原理、Transformer架构、应用场景 | [[RAG学习笔记]]、[[LangChain入门总结]] |
| [[RAG学习笔记]] | RAG架构、检索器、向量数据库 | [[AI大模型基础知识]]、[[LangChain入门总结]] |
| [[LangChain入门总结]] | LangChain框架、核心模块、RAG实现 | [[RAG学习笔记]]、[[Claude Agent SDK学习笔记]] |

### 二、Claude Code与Skills（6篇）

| 文档 | 主题 | 关联文档 |
|------|------|---------|
| [[Claude Code学习笔记]] | CLAUDE.md、MEMORY.md、Skills、Plugins | [[常用SKILL总结]]、[[Harness Engineering（驾驭工程）]] |
| [[常用SKILL总结]] | Skills分类、使用场景、推荐组合 | [[Claude Code学习笔记]]、[[vibecoding经验总结]] |
| [[Harness Engineering（驾驭工程）]] | 驾驭工程四大护栏、Agent失败模式 | [[Claude Code学习笔记]]、[[vibecoding经验总结]] |
| [[Claude Agent SDK学习笔记]] | Agent SDK简介 | [[Claude Code学习笔记]]、[[LangChain入门总结]] |
| [[vibecoding经验总结]] | Agent边界、AI编程技巧 | [[Claude Code学习笔记]]、[[Harness Engineering（驾驭工程）]] |
| [[SKILL发布L站的说明]] | 开源项目发布 | [[常用SKILL总结]] |

### 三、接口自动化SKILL实践（9篇）

| 文档 | 主题 | 关联文档 |
|------|------|---------|
| [[SKILLS问题记录]] | 会议讨论、问题收集、优化项 | [[通过Claude Code和接口用例SKILL高效编写和维护接口自动化用例]] |
| [[通过Claude Code和接口用例SKILL高效编写和维护接口自动化用例]] | 完整使用教程、4种编写方式 | [[SKILLS问题记录]]、[[capture-抓包底座使用指引]] |
| [[通过AI+SKILL编写接口用例的提效记录-表格]] | 提效数据表格 | [[接口自动化SKILL的提效记录]] |
| [[通过AI+SKILL编写自动化测试用例记录]] | 抓包生成、参考用例、cURL、Controller源码 | [[通过Claude Code和接口用例SKILL高效编写和维护接口自动化用例]] |
| [[通过AI+SKILL维护用例的测试记录]] | pytest维护、抓包维护、参考用例维护 | [[通过AI+SKILL编写自动化测试用例记录]] |
| [[通过AI实现全流程的接口自动化]] | GitNexus扫描、全流程自动化 | [[通过Claude Code和接口用例SKILL高效编写和维护接口自动化用例]] |
| [[接口自动化SKILL的提效记录]] | 4月-5月提效数据对比 | [[通过AI+SKILL编写接口用例的提效记录-表格]] |
| [[capture-抓包底座使用指引]] | mitmproxy配置、抓包流程 | [[通过Claude Code和接口用例SKILL高效编写和维护接口自动化用例]] |
| [[参考Java Controller源码分析草稿]] | PageLayoutController分析、接口覆盖情况 | [[通过AI+SKILL编写自动化测试用例记录]] |

### 四、学习与规划（5篇）

| 文档 | 主题 | 关联文档 |
|------|------|---------|
| [[学习路线图]] | AI学习三阶段：基础→RAG→Agent | [[AI大模型基础知识]]、[[RAG学习笔记]] |
| [[学习计划和进度]] | 5月-6月学习计划 | [[学习路线图]] |
| [[学习要点]] | AI产品测试招聘要求 | [[AI产品测试]] |
| [[AI产品测试]] | LLM测试经验、eval体系 | [[学习要点]] |
| [[学习资料汇总]] | （内容为空） | - |

### 五、项目与实践（3篇）

| 文档 | 主题 | 关联文档 |
|------|------|---------|
| [[AI自动化开发计划]] | 接口自动化、UI自动化开发计划 | [[通过Claude Code和接口用例SKILL高效编写和维护接口自动化用例]] |
| [[vibecoding总结]] | 使用过程总结、编写项目 | [[vibecoding经验总结]]、[[AI自动化开发计划]] |
| [[个人博客]] | 博客规划 | - |

---

## 🔗 文档关联图谱

```
                    ┌─────────────────┐
                    │  AI大模型基础知识  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │ RAG学习笔记  │  │LangChain    │  │ 学习路线图   │
     │             │  │入门总结      │  │             │
     └──────┬──────┘  └──────┬──────┘  └─────────────┘
            │                │
            └────────┬───────┘
                     ▼
            ┌─────────────────┐
            │ Claude Code     │
            │ 学习笔记         │
            └────────┬────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│常用SKILL总结│ │Harness      │ │Claude Agent │
│             │ │Engineering  │ │SDK学习笔记  │
└──────┬──────┘ └──────┬──────┘ └─────────────┘
       │               │
       └───────┬───────┘
               ▼
      ┌─────────────────┐
      │ vibecoding经验   │
      │ 总结             │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │ 接口自动化SKILL  │
      │ 实践（9篇）      │
      └─────────────────┘
```

---

## 🏷️ 主题标签

### #AI基础
- [[AI大模型基础知识]]
- [[RAG学习笔记]]
- [[LangChain入门总结]]

### #Claude Code
- [[Claude Code学习笔记]]
- [[常用SKILL总结]]
- [[Harness Engineering（驾驭工程）]]
- [[Claude Agent SDK学习笔记]]

### #接口自动化
- [[SKILLS问题记录]]
- [[通过Claude Code和接口用例SKILL高效编写和维护接口自动化用例]]
- [[通过AI+SKILL编写自动化测试用例记录]]
- [[通过AI+SKILL维护用例的测试记录]]
- [[capture-抓包底座使用指引]]

### #提效数据
- [[接口自动化SKILL的提效记录]]
- [[语雀/api-automation/通过AI+SKILL编写接口用例的提效记录-表格|通过AI+SKILL编写接口用例的提效记录-表格]]

### #VibeCoding
- [[vibecoding经验总结]]
- [[vibecoding总结]]

### #学习规划
- [[学习路线图]]
- [[学习计划和进度]]
- [[学习要点]]
- [[AI产品测试]]

---

## 📝 阅读建议

### 入门路径
1. 先读 [[AI大模型基础知识]] 了解LLM基本概念
2. 再读 [[Claude Code学习笔记]] 了解Claude Code生态
3. 然后读 [[常用SKILL总结]] 了解Skills使用方法

### 实践路径
1. 读 [[通过Claude Code和接口用例SKILL高效编写和维护接口自动化用例]] 了解完整流程
2. 读 [[capture-抓包底座使用指引]] 配置抓包环境
3. 读 [[SKILLS问题记录]] 了解常见问题和解决方案

### 深入路径
1. 读 [[Harness Engineering（驾驭工程）]] 了解Agent设计原则
2. 读 [[RAG学习笔记]] 和 [[LangChain入门总结]] 了解RAG技术
3. 读 [[vibecoding经验总结]] 了解AI编程最佳实践

<!-- AUTO-CATALOG:START -->

## 自动页面目录

- [[个人博客]] — 个人博客
- [[关联分析]] — 关联分析

<!-- AUTO-CATALOG:END -->
