# LangChain入门总结

来源：https://www.yuque.com/bbuer/ebdyfe/kglru1g9hbgh6q8g
抓取时间：2026-07-01

---

**官方文档：** https://python.langchain.com/

**deepLearning：** https://learn.deeplearning.ai/

---

## 1. 基础知识

### 1.1 LangChain 是什么？

LangChain 是一个用于构建大语言模型（LLM）应用的开发框架，它通过模块化设计简化了 LLM 应用的开发流程，支持开发者快速搭建基于语言模型的复杂应用（如聊天机器人、知识库问答、自动化工作流等）。其核心思想是通过"链（Chain）"将不同组件（如模型、数据、工具）灵活组合，实现端到端的功能。

**应用场景：**
- 自然语言交互：构建聊天机器人、问答系统
- 文档处理：自动化文本摘要、文档分析
- 智能代理：创建能自主执行任务的AI Agent
- 多模型集成：连接不同LLM（如OpenAI、Hugging Face等）

### 1.2 LangChain 核心模块

| 模块 | 功能 | 代码示例 |
|------|------|---------|
| Models | 集成多种LLM（GPT、Llama等）和Embedding模型 | `from langchain.llms import OpenAI` |
| Prompts | 模板化提示词，动态生成输入 | - |
| Output Parsers | 解析模型输出为结构化数据 | - |
| Chains | 组合多步操作（如LLM调用 + 结果解析） | `chain = LLMChain(llm=llm, prompt=prompt)` |
| Memory | 维护对话历史或上下文状态 | `memory = ConversationBufferMemory()` |
| Agents | 创建自主决策的AI代理（使用工具/API） | `agent = initialize_agent(tools, llm)` |
| Indexes | 文档检索与向量数据库集成（如Chroma、FAISS） | `docsearch = FAISS.from_documents(docs)` |
| Tools | 调用外部 API、计算器、搜索引擎等工具，扩展模型能力 | 包含在Agents中 |

### 1.3 LangChain 的常用应用场景

1. **智能问答系统** — 企业知识库、教育辅助
2. **自动化文档处理** — 合同分析、法律/医疗文档
3. **聊天机器人** — 电商客服、心理健康助手
4. **代码生成与调试** — 代码补全、错误诊断
5. **数据洞察与分析** — 商业报告、舆情监控
6. **个性化内容生成** — 营销文案、故事创作

### 1.4 LangChain 的优势

- **模块化设计：** 自由组合数据、模型、工具，适应多样化需求
- **降低开发门槛：** 抽象底层复杂性，开发者聚焦业务逻辑
- **生态丰富：** 支持多种数据库、工具和第三方服务（如 Slack、Notion）

---

## 2. LangChain核心模块

### 2.1 Model I/O(模型的输入和输出)

**Prompts(提示模板)**
- 功能：通过模板动态生成提示词，支持变量注入和上下文管理，提升提示的可维护性
- 示例：定义包含对话历史和用户输入的模板，自动生成符合格式的提示

**Model(模型封装)**
- 功能：统一封装不同厂商（如 OpenAI、Anthropic）的语言模型 API，支持灵活切换和参数调优（如温度、最大令牌数）
- 示例：使用 OpenAI 模型生成文本，或通过 ChatOpenAI 处理结构化对话

**高级用法-核心参数解析：**

| 参数 | 作用 | 建议 |
|------|------|------|
| model | 指定使用的模型版本 | gpt-4o适合复杂推理；gpt-3.5-turbo性价比高 |
| temperature (0-1) | 控制生成文本的随机性 | 事实性回答：0-0.5；创意任务：0.7-1 |
| max_tokens | 限制单次生成的 token 数 | 短回复：50-200；长文本：200-1000 |
| top_p (0-1) | 通过核采样控制生成多样性 | 低值(0.5)：更保守；高值(0.9)：更开放 |
| frequency_penalty (-2到2) | 惩罚重复词汇，减少冗余 | 高值(1-2)：长文本避免重复 |
| presence_penalty (-2到2) | 鼓励生成新话题 | 高值(1-2)：适合创意任务 |

**Parser(输出解析器)**
- 功能：将模型的非结构化输出解析为结构化数据（如 JSON），便于后续处理
- 实现步骤：第一步通过系统提示词要求AI返回指定格式的结构化字符串数据，第二步通过解析方法解析为自己想要的格式

### 2.2 Memory(对话记忆)

**Memory 类型对比：**

| Memory 类型 | 特点 | 应用场景 |
|-------------|------|---------|
| ConversationBufferMemory | 存储完整对话历史（原始形式），简单易用 | 短对话场景（如客服机器人） |
| ConversationSummaryMemory | 动态生成对话摘要，减少 token 消耗 | 长对话、对成本敏感的场景 |
| ConversationBufferWindowMemory | 仅保留最近 N 轮对话（窗口大小可调） | 需要近期上下文的场景 |
| FileChatMessageHistory | 对话历史持久化存储（本地文件） | 需要长期记忆的场景 |
| ConversationTokenBufferMemory | 根据 token 数量动态截断对话 | 严格限制 token 使用的场景 |

**核心方法：**
- `save_context()`：写-向记忆中添加新对话
- `load_memory_variables()`：读-提取记忆内容供 LLM 使用
- `clear()`：清空记忆数据

**最佳实践：**
- 短对话：优先使用 ConversationBufferMemory
- 长对话：结合 ConversationSummaryMemory 和 ConversationBufferWindowMemory
- 持久化需求：使用 FileChatMessageHistory 或集成数据库存储

### 2.3 Chains(链式流程)

**常用Chains模块：**

| 模块名称 | 特点 | 使用场景 |
|---------|------|---------|
| LLMChain | 基础链，直接组合提示模板和语言模型；简单灵活 | 简单问答、文本生成 |
| SimpleSequentialChain | 顺序执行子链，输入输出格式严格匹配；线性流程 | 多步骤文本处理 |
| SequentialChain | 支持复杂输入输出映射，明确变量传递；可扩展 | 复杂业务流程 |
| LLMRouteChain | 动态路由，基于语言模型选择子链；自适应 | 多任务处理 |

**SequentialChain vs SimpleSequentialChain：**

| 特性 | SequentialChain | SimpleSequentialChain |
|------|-----------------|----------------------|
| 分支支持 | ✅ 动态路由和条件判断 | ❌ 仅线性流程 |
| 输入输出映射 | ✅ 明确指定变量传递路径 | ❌ 依赖自然参数传递 |
| 嵌套结构 | ✅ 支持多层嵌套链 | ❌ 仅平面结构 |
| 复杂逻辑处理 | ✅ 支持复杂业务逻辑 | ❌ 仅简单任务序列 |

### 2.4 Agents(智能代理)

**Agents简介：**
Agents 是 LangChain 框架中处理复杂任务的核心模块，其核心目标是通过动态调用工具（Tools）和 LLM 推理实现自主决策。

**核心特点：**
1. 任务分解能力：将复杂任务拆解为多个子步骤
2. 动态工具调用：根据当前状态选择最合适的工具
3. 持续反馈循环：通过"思考-行动-观察"循环逐步逼近答案
4. 支持多模态输入：可整合 API 调用、数据库查询等外部资源

**Agents的设计思路（ReAct 范式）：**
1. **工具集成系统** — 支持自定义工具、工具注册机制、工具调用协议
2. **决策引擎** — 循环执行：观察→思考→行动、状态管理、终止条件
3. **推理增强层** — 提示模板、计划生成、结果解析

**Agents vs 其他模型：**

| 维度 | Agents | SequentialChain | RouterChain |
|------|--------|-----------------|-------------|
| 任务复杂度 | 高（支持多步决策） | 低（线性流程） | 中（条件路由） |
| 自主性 | 高（自主选择工具） | 低（预设流程） | 中（条件判断） |
| 扩展性 | 强（动态添加工具） | 弱（需修改代码） | 中（需配置路由规则） |
| 典型案例 | 数据分析报告生成 | 文本翻译流水线 | 多语言客服路由 |

### 2.5 Indexes(检索增强)

**核心概念：RAG（检索增强生成）**

检索增强生成（Retrieval-Augmented Generation, RAG）是 LangChain 处理长文本/文档的核心技术，通过以下步骤实现：
1. 文档加载：从本地/云端加载各类文档（文本、PDF、Markdown 等）
2. 文档预处理：将文档拆分为可处理的文本块（Chunking）
3. 向量化：将文本块转换为向量嵌入（Embedding）
4. 向量存储：将向量存入专用数据库（FAISS、Chromadb 等）
5. 检索与生成：通过向量检索获取相关文档片段，结合 LLM 生成回答

**文档加载支持格式：**

| 类型 | Loader 类 | 示例文件 |
|------|----------|---------|
| 纯文本 | TextLoader | .txt |
| PDF | PyPDFLoader | .pdf |
| Markdown | MarkdownLoader | .md |
| CSV | CSVLoader | .csv |
| 网页 | BeautifulSoupWebBaseLoader | 网页 URL |

**向量存储工具：**

| 工具 | 特点 | 适用场景 |
|------|------|---------|
| FAISS | 高性能本地向量库 | 中小规模数据（<10 万条） |
| ChromaDB | 轻量级嵌入式数据库 | 快速原型开发 |
| Milvus | 分布式向量数据库 | 大规模数据（>100 万条） |
| Pinecone | 云端托管向量数据库 | 高可用生产环境 |

**检索链模式：**
- RetrievalQA：直接返回检索结果的整合回答
- RetrievalQAWithSources：返回回答 + 来源文档引用
- ConversationalRetrievalChain：支持多轮对话的检索问答

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[AI大模型基础知识]] — AI测试主题关联
- [[RAG学习笔记]] — AI测试主题关联
- [[vibecoding总结]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[UI自动化测试日常问题记录]] — AI测试主题关联
- [[移动端自动化框架搭建问题点记录]] — AI测试主题关联
- [[通过AI+SKILL维护用例的测试记录]] — AI测试主题关联
- [[学习路线图]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
