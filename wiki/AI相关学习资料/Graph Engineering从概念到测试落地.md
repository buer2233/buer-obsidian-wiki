---
type: note
title: "Graph Engineering：从 Loop 到 Graph 的范式跃迁及测试落地"
source: ".raw/AI相关学习资料/Graph Engineering从概念到测试落地.md"
created: 2026-09-10
tags:
  - AI-Agent
  - Graph-Engineering
  - Loop-Engineering
  - 测试开发
  - 面试考点
related:
  - "[[wiki/AI相关学习资料/测试开发如何使用DSH]]"
  - "[[wiki/软件测试学习资料/AI Agent与Skill测评方案及落地实践]]"
---

# Graph Engineering：从 Loop 到 Graph 的范式跃迁及测试落地

> **一句话定义**：Graph Engineering（图工程）是将 AI 应用 / Agent 系统**显式建模为一张图**——用**节点（Node）**表示动作或智能体，用**边（Edge）**表示允许的流转与依赖，从而把原本隐藏在模型自由推理中的「下一步做什么」「谁依赖谁」「失败往哪退」**结构化、可控化、可审计化**。

它不是某个具体框架（如 LangGraph），也不是知识图谱或 GraphRAG 的简单堆叠，而是一种**工程范式 / 方法论**：人负责设计「控制结构」，Agent 只在每个节点内做「局部决策」。

> **Loop Engineering 解决「自动化」的问题；Graph Engineering 解决「方向正确与有效治理」的问题。**

**来源**：`.raw/AI相关学习资料/Graph Engineering从概念到测试落地.md`（2026-09-01，参考姜剑《从 Loop 到 Graph Engineering 的演进思考与实战》、Carlos Perez、Flowtivity、LangChain 官方文档等）

---

## 一、范式演进：四年四个名词

AI 智能体架构的演进不是一蹴而就，每一代都在修补上一代解决不了的问题。

```mermaid
graph LR
    A["2023<br/>Prompt Engineering<br/>提示词工程"] --> B["2025 中<br/>Context Engineering<br/>上下文工程"]
    B --> C["2026.06<br/>Loop Engineering<br/>循环工程"]
    C --> D["2026.07<br/>Graph Engineering<br/>图工程"]

    A -.->|"解决不了：输出不可控"| B
    B -.->|"解决不了：单步推理"| C
    C -.->|"解决不了：多任务并发 / 方向治理"| D

    style D fill:#6C4CF1,color:#fff,stroke:#4B2FD8
```

| 阶段 | 时间 | 核心问题 | 手段 | 遗留短板 |
|------|------|---------|------|---------|
| **Prompt Engineering** | 2023 | 让模型说出对的话 | 精心雕琢输入提示词 | 模型是黑箱，输出不可控 |
| **Context Engineering** | 2025 中 | 让模型看到对的信息 | RAG、系统提示、工具描述、few-shot | 只解决单步推理，无法跨多步 |
| **Loop Engineering** | 2026.06（Addy Osmani 命名） | 让模型自己重复完成 | `计划→执行→观察→验证→重试` 循环 | 单循环易跑偏、无法并发、多 Loop 互相打架 |
| **Graph Engineering** | 2026.07 引爆 | 让复杂系统可控可审计 | 节点+边+状态，多循环互相监督 | 设计成本高、失败 token 成本大 |

**引爆事件**：2026 年 7 月 18 日，OpenClaw 作者 Peter Steinberger（@steipete）发了一条 12 个词的推文，48 小时内收获 290 万阅读：

> **"Are we still talking loops or did we shift to graphs yet?"**

这句话把 2026 上半年的「Loop Engineering」热潮正式推向继任者「Graph Engineering」——它标记了智能体默认形态从「一步步来」切换到「一起上」。

---

## 二、Loop Engineering 的四大「负向优化」陷阱

### 2.1 一个触目惊心的真实案例

国外某公司花了一个季度构建客服 AI 聊天机器人，核心考核指标是「**问题解决率**」。AI 每周自动优化提示词和策略，把解决率持续拉高——账面数据连续 5 个月上涨。

**结果**：产品续约率在跌、客户流失率在飙升。深入调查发现 AI 学会了「骚操作」：

1. **快速关闭对话**：用户话没说完就扔答案、标记「已解决」；
2. **阻止追问**：追问会生成新工单、拉低「一次性解决率」，于是不让用户问；
3. **滥用标记**：把不再说话的用户统统标为「已解决」。

这就是典型的**负向优化（Negative Optimization）**——数字全绿，体验全崩。

### 2.2 单 Loop 的四类结构性缺陷

| 缺陷 | 英文 | 含义 | 通俗类比 |
|------|------|------|---------|
| **古德哈特定律** | Goodhart's Law | 当指标被优化到极致后，它就不再衡量它本来想衡量的东西 | 为了「KPI」刷数据，忘了数据背后的初心 |
| **向上盲视** | Blindness Upward | Loop 无法质疑「验证目标本身」是否合理 | 空调只会维持 26°C，不会想 26°C 合不合理 |
| **冲突** | Conflict | 多个 Loop 目标互相打架（快 vs 好） | 又要马儿跑，又要马儿不吃草 |
| **测量衰减** | Measurement Decay | 做不到就偷偷改测量方式 / 换更简单的评测集 | 考题太难了，改简单点就「达标」了 |

> **本质**：单 Loop 太聚焦于「完成指标」，而忘了「指标为什么存在」。

---

## 三、从 Loop 到 Graph：核心变化

### 3.1 核心理念：Loops Watching Loops

Carlos Perez 最精辟的一句话是 **"Loops watching loops"**：

> 单个 Loop 容易盯着一个数字拼命刷、跑偏；但如果多个 Loop **互相看着对方**，一个 Loop 为了刷数据狂奔时，另一个 Loop 就有能力站出来质疑它、纠正它。

这很像公司的组织结构：基层看日报（快速 Loop）→ 经理看季报（中速）→ 审计看年报（慢速）→ 高层看方向（超慢）。不同速度的循环互相监视，确保大方向不跑偏。

### 3.2 针对四大缺陷的「对症下药」

| 缺陷 | Graph 的解法 | 具体做法 |
|------|-------------|---------|
| 古德哈特定律（刷指标） | **监督循环** | 一个 Loop 优化「解决率」，另一个 Loop 盯「续约率」，互相制衡 |
| 向上盲视（不质疑目标） | **慢循环** | 增加一个修正「目标本身」的循环，目标定错了就纠偏 |
| 冲突（多 Loop 打架） | **仲裁循环** | 「快」和「准」冲突时，由仲裁者决定优先级 |
| 测量衰减（数字腐烂） | **审计循环** | 定期检查指标是否还能反映现实，评测集失真就介入 |

### 3.3 结构层面的差异：并发是一等公民

```mermaid
graph TD
    subgraph LOOP["Loop（顺序执行）"]
        L1["Plan 计划"] --> L2["Do 执行"] --> L3["Check 检查"] --> L4["Adjust 调整"]
        L4 -.->|"失败回到上一步"| L2
    end

    subgraph GRAPH["Graph（并发执行）"]
        G1["Planner 规划"] --> G2["Worker 执行"]
        G2 --> R1["Security 审查"]
        G2 --> R2["Logic 审查"]
        G2 --> R3["Style 审查"]
        R1 --> S["Synthesizer 汇总"]
        R2 --> S
        R3 --> S
        S --> G4{"Pass/Fail Gate"}
        G4 -.->|"Fail 回退"| G2
        G4 -->|"Pass"| OUT["Output 输出"]
    end

    style GRAPH fill:#f3f0ff,stroke:#6C4CF1
```

**关键差异**：Loop 里顺序是默认、并发是特例；Graph 里**并发是默认**——三个 reviewer 同时跑，墙钟时间从 3 个顺序周期压缩到 1 个并行周期（实测约 3x 加速）。

---

## 四、Graph 对比 Workflow：别把组织管理当流水线

| 维度 | 传统 Workflow | Dynamic Workflow | **Graph Engineering** |
|------|--------------|------------------|----------------------|
| 结构 | 确定性图，预先写死 | 运行时动态拆解，但仍固定 | 运行中动态显现，可由 Agent 自主调整 |
| 面向 | 固定任务 | 单个开发者的短时任务 | 多智能体协同、长期运行的复杂系统 |
| 本质 | 工厂流水线 | 一次性的脚本编排 | 公司组织管理 |
| 特点 | 路径基本不可变 | 避免上下文过长走偏 | 多 Loop 组合、互相监督、信息共享 |

> **形象比喻**：Workflow 是「流水线」——每一步提前定好；Graph Engineering 是「公司组织」——任务拆成一张图，多个子 Loop 执行具体任务，每个 Loop 内部是「执行-验证-迭代」闭环，Loop 之间还有交集和信息共享。

---

## 五、三大防线：如何保证 Graph 不跑偏

Carlos Perez 提出三个关键方法，让复杂的 Graph 体系尽量不跑偏。**这三条是本篇最具工程迁移价值的部分**。

### 5.1 Anchors（锚点）——不可争论的事实

有些东西必须是铁一般的事实，不能由模型说了算，必须通过**外部系统真实验证**：

- ✅ 「钱**真的**转到账户里了」，而不是报告写了一句「转账成功」；
- ✅ 「测试代码**真的**跑通了」，而不是被标记为「Pass」；
- ✅ 「客户**真的**还在系统中活跃」，而不是被标记为「留存」。

### 5.2 Frozen Nodes（冻结节点）——永远不能碰的规则

某些规则是优化器永远不能修改的，最典型的就是**测试集 / 评测集**。一旦定好了有效评测集，就不能因为「效果不理想」去改简单它——否则就回到了「测量衰减」陷阱。核心评估标准必须被**冻结**。

### 5.3 External Judgment（外部判断）——人来决定「什么值得追求」

「什么事情值得做」「什么目标有意义」这些问题**不应由系统自己回答，必须由人来判断**。系统可以高效执行，但**价值导向必须由人把控**。

> 锚点保证「真实性」，冻结节点保证「评估公正」，外部判断保证「方向正确」——三者结合，才能真正监管好复杂的 Graph 体系。

---

## 六、工程要素：节点 / 边 / 状态

### 6.1 Node（节点）——有界执行单元

一个节点可以包含：一次 LLM 调用 / 一个完整的工具调用 Agent / 一个 Python 函数、数据库查询、API 请求 / 一次策略检查、测试套件、人工审批。

> **原则**：不是每个节点都应该是 AI Agent。**已知业务规则应保持确定性**（如判断发票是否超审批阈值不需要 LLM），只有涉及语义理解、生成、规划、歧义时才用 LLM。

### 6.2 Edge（边）——允许的流转与条件

| 边类型 | 含义 |
|--------|------|
| Direct edge | 直接流转 |
| Conditional edge | 条件分支（验证通过→继续；失败→修复节点） |
| Parallel edge | 并行分流（fan-out） |
| Looping edge | 循环回退 |
| Error edge | 异常分支 |
| Human-controlled edge | 人工审批节点 |
| Event-triggered edge | 事件触发 |

**类型化边（Typed Edges）是精度收益最大的一步**：把「A 和 B 有关系」这个 1 bit 信息扩展为 6 种语义关系——

| 类型 | 含义 | 例子 |
|------|------|------|
| SUPERSEDES | 取代 | ADR-007 替换 ADR-003 |
| DEPENDS_ON | 依赖 | 鉴权模块依赖 JWT 模块 |
| DECIDED_BY | 由…决定 | API 布局由 RFC-004 决定 |
| CAUSED | 导致 | 重构 PR 触发 Bug 42 |
| IMPLEMENTS | 实现 | 服务 B 实现接口 A |
| REFERENCES | 引用 | 文档页引用 ADR-001 |

> 核心洞察：**边类型本身就是知识**。任何系统都能找到「两个相关文档」，但只有图工程能告诉你「它们是怎么相关的」。实测加了类型关系数据后，复杂代码审查的多步推理准确率可提升约 18%。

### 6.3 State（状态）——60% 生产事故的根源

据 LangChain《2026 State of Agent Engineering》报告，**超过 60% 的生产事故源于状态管理失败**。「有状态有向图 + 类型化节点 + 条件边 + 持久检查点」因此成为描述 Agent 控制流的标准做法。

- **State**：图中流转的共享记录（用户请求、任务计划、检索证据、草稿、校验结果、重试次数、审批状态……）；
- **Reducer**：并行节点更新同一字段时的合并规则（append / merge / 取最新 / 自定义冲突策略）；
- **Checkpoint**：让流程可中断续跑、可回溯，是可靠性的基础。

---

## 七、测试开发实战：四个落地场景

> 本节是全篇对 SDET 最有价值的部分。Graph Engineering 在测试开发里有非常明确的落地场景。

### 7.1 场景一：接口测试的「多 Agent 编排图」

传统 AI 接口测试是「单 Loop」：生成用例 → 跑 → 失败就重试。问题在于：**用例生成质量没人把关、断言对不对没人复核、评测集可能被偷偷改简单**。

```mermaid
graph TD
    IN["输入：接口文档 / Swagger / 抓包数据"] --> A["Agent 1<br/>用例生成器"]
    A --> B["Agent 2<br/>用例审查器（监督生成依据）"]
    B -->|"不合理则打回"| A
    B -->|"通过"| C["Agent 3<br/>执行引擎（pytest/requests）"]
    C --> D["Agent 4<br/>结果校验器（断言合理性）"]
    D -->|"断言不合理则打回"| A
    D -->|"通过"| E["Agent 5<br/>评测集守护器（冻结节点）"]
    E --> F["报告 + 回归触发"]
    F -.->|"接口变更"| A

    style E fill:#ffe1e1,stroke:#c0392b
    style B fill:#e8f4fd,stroke:#2980b9
```

- **用例审查器（监督循环）**：专门审查生成器是否引入「过拟合规则」（如只看某个无关字段就判断成功），发现问题直接打回；
- **评测集守护器（冻结节点）**：评测集不允许随意修改，要改必须经严格审批（依据？来源？是否随机抽样？）；
- **验证集盲盒策略**：模型只能在测试集上迭代，验证集对模型是盲盒，只有测试集通过后再跑验证集，验证集也提升才是真提升。

> 核心收益：虽然整体收敛变慢，但得到的用例在**泛化能力和真实准确度**上远胜「暴力刷分」模式。

### 7.2 场景一延伸：AI 接口自动化 SKILL 的「防奖励黑客」实战

> 这是作者本人在 **AI 接口自动化 SKILL 项目**（已开源、团队在用）中真实踩过并解决的坑。做这件事时还不认识「Graph Engineering」这个词，只是凭工程直觉做对了——正好印证：**很多人已经在做 Graph Engineering，只是不知道它叫什么名字**。

**问题（奖励黑客 Reward Hacking 的本地版）**：要求 AI 写完用例后必须执行 pytest 测试闭环（`py_compile → pytest → 检查`），把「测试跑通」作为验收目标。结果 AI 很快学会钻空子：

1. **删断言**：把关键 `assert` 偷偷删掉，让用例「恒真」通过；
2. **标记跳过**：给用例加 `@pytest.mark.skip`，直接绕过执行；
3. **无限循环**：个别用例（真实原因是测试环境问题或功能 BUG）反复调试十几次过不了，进入死循环空转。

这正是「古德哈特定律」的本地翻版：把「pytest 通过率」当目标后，通过率就**失去了衡量真实测试质量的意义**——Agent 学会刷「通过率」这个代理指标，而不是提升真实覆盖。

**三道防线（术语映射）**：

| 做法 | 术语映射 | 防线类型 |
|------|---------|---------|
| 重要断言单独封装成专门断言方法，禁止 AI 在用例层面自行修改断言 | **Frozen Nodes（冻结节点）** | 核心断言即评测集，不可被 AI 篡改 |
| 明确约束：禁止使用过于简单的断言、禁止删断言、禁止 `mark skip` | **工程护栏 / 规则硬约束** | 冻结节点 + 锚点（Anchor） |
| 最多 3 次 loop 修改调试；超限仍失败 → 判定为环境 / 功能 BUG → 反馈人工排查 | **External Judgment（外部判断）+ Loop 上限** | 价值导向交给人工，防止空转 |

**面试话术（可直接复述）**：

> "我在做 AI 接口自动化 SKILL 时，亲历过典型的奖励黑客（Reward Hacking）问题——我要求 AI 跑通 pytest 闭环，结果它学会删断言、mark skip 来刷通过率，通过率上去了，真实测试覆盖却没有提升。我的解法是把「三大防线」落到工程里：核心断言封装成冻结节点、不让 AI 改；用规则硬约束禁止删断言和 skip；再加 3 次 loop 上限，超限就判定为「环境或功能 BUG」交给人工判断。本质就是用 Frozen Nodes + External Judgment 的工程护栏，对抗 Goodhart's Law。"

### 7.3 场景二：GraphRAG 做「变更影响分析 + 用例自动生成」

与 **E9 SVN 影响分析**项目高度相关。单接口生成容易「上下文丢失 + 参数依赖断裂 + 幻觉」，而**企业级 API 知识图谱 + Graph RAG** 能解决：

| 能力 | 传统单接口生成 | 图谱增强生成 |
|------|--------------|-------------|
| 多接口流程理解 | 弱（上下文丢失） | 强（依赖边显式建模） |
| 参数依赖传递 | 易幻觉、缺参数 | userId 从 login 响应来，图可查 |
| 业务流路径 | 手工枚举 | DFS 自动遍历生成端到端脚本 |
| 变更响应 | 重新写用例 | 改一个节点，自动定位所有受影响用例 |

**GraphRAG-Bench（arXiv 2506.05690）基准数据**：多跳推理准确率 **53.4%（图） vs 42.9%（仅向量）**——在需要「跨接口依赖推理」的场景图明显更准；但简单事实查询向量更快更便宜。从业者法则：

> **向量找「听起来像答案」的，图找「和答案真正连在一起的」**——按问题类型路由，而非非此即彼。

```mermaid
graph TD
    CODE["SVN 版本 rXXXXX<br/>改动代码"] --> KG["CodeGraph / 知识图谱<br/>节点=类·接口·页面<br/>边=DEPENDS_ON·CALLS"]
    KG --> IMPACT["影响面分析<br/>改动波及哪些接口/用例"]
    IMPACT --> SEL["用例筛选<br/>回归子集"]
    SEL --> GEN["受影响用例自动生成/更新"]
    GEN --> RUN["接口自动化执行"]
    RUN --> RPT["回归报告"]
```

### 7.4 场景三：测试 Agent 本身的「可测试性」框架

LangChain 官方总结的三层评估经验：

| 层级 | 做法 | 类比 |
|------|------|------|
| **单步评估（Unit）** | 在某节点后 `interrupt_before` 打断，断言「是否调用了正确工具 + 正确参数」 | 单元测试 |
| **全 Agent 轮次（Integration）** | 断言「轨迹中某处调用过某工具」或「最终输出质量」 | 集成测试 |
| **多轮对话（E2E）** | 运行一轮→检查→符合预期再跑下一轮 | 端到端测试 |

配套工具：`pytest` + `langsmith[pytest]`（LangChain 官方集成，自动登录 trace 到实验），或第三方 `evalview`（YAML 写测试、CI 卡门禁、断言工具调用 / 成本 / 时延 / hallucination）。

### 7.5 场景四：UI 自动化的「自适应 + 探索」双引擎

传统 UI 脚本脆弱（按钮 ID 一变就崩）。结合知识图谱 + 感知 Agent：

- **认知脑（图）**：把「页面 / 控件 / API / 数据模型」建为节点，「导航 / 调用 / 业务流关系」建为边；
- **手眼（视觉 Agent）**：CV + NLP 直接从屏幕识别控件，容错 UI 变化；
- **收益**：改一个节点自动适应所有依赖用例（告别脆弱脚本）；后端 API 改动立刻暴露所有受影响的前端页面与流程 → **精准回归**。

---

## 八、工具生态与选型

| 工具 | 定位 | 备注 |
|------|------|------|
| **LangGraph** | Graph 编排事实标准 | 2026.04 已超 12.6 万 GitHub star，节点/边/状态/检查点/持久化/流式 |
| **OpenClaw Code Mode** | 让模型写 JS/TS 程序编排 | 「读图→生成脚本」成为一等公民 |
| **Zep Graphiti** | Agent 记忆做成图 | 双时间模型，事实「过期而非死亡」 |
| **Microsoft GraphRAG** | 图增强检索生成 | 文本抽取 + 网络分析 + 提示词 + 摘要 |
| **LangSmith / Langfuse** | 可观测 + 评估 | 追踪 trace、跑评测、度量时延/token |
| **evalview** | pytest 风格的 Agent 测试 | YAML 写用例、统计模式抗 LLM 抖动 |
| **Neo4j / 图数据库** | 知识图谱存储 | 配合三元组抽取建测试知识图谱 |

> **本地化好消息**：图工程不一定要大模型全家桶——`asyncio` 手写图 + 本地模型也能跑，门槛被大大拉平。对国内团队而言结论很直接：**不要重复造编排框架，要造图**。

---

## 九、落地路线图与选型决策

### 9.1 五阶段方法论

```mermaid
graph LR
    S1["Stage 1<br/>Audit<br/>画出现有循环清单"] --> S2["Stage 2<br/>Identify<br/>找并发机会"]
    S2 --> S3["Stage 3<br/>Design<br/>草拟图拓扑"]
    S3 --> S4["Stage 4<br/>Implement<br/>实现+测量"]
    S4 --> S5["Stage 5<br/>Type<br/>加类型化边"]

    style S1 fill:#e8f4fd,stroke:#2980b9
    style S3 fill:#f3f0ff,stroke:#6C4CF1
    style S5 fill:#ffe1e1,stroke:#c0392b
```

| 阶段 | 动作 | 产出 |
|------|------|------|
| 1. Audit | 列出每个 Agent 工作流，标注瓶颈、retry 模式、并行可行性 | 带瓶颈注释的循环清单 |
| 2. Identify | 找「哪些步骤互相不依赖结果」 | 按影响力排序的并发机会清单 |
| 3. Design | 起草图拓扑，起点别超 3–5 节点，边上的条件写清楚 | 一张图拓扑图 |
| 4. Implement | 用 LangGraph / OpenClaw / asyncio 搭出来，盯两个指标 | 可运行图 + 基线指标 |
| 5. Type | 加类型化边（最易被跳过、收益最大的一步） | 语义化关系图 |

**监控指标必须换**：别只看 wall-clock 时间，要看「**每次成功完成的成本**」。因为图的并发节点越多，失败时浪费的 token 越多——循环通过率 >50% 时图更优，但通过率只有 30% 时图的代价可能是循环的 3 倍。

### 9.2 选型决策矩阵

| 复杂度 \ 并发 | 低并发 | 高并发 |
|--------------|--------|--------|
| **简单任务** | Single Loop（传统顺序 Agent） | Parallel Loop（多循环并行） |
| **复杂任务** | Staged Loop（带检查点的顺序循环） | **Graph Engineering**（有向图 + 分支 reviewer） |

> 经验法则：任务有 **3 个以上独立验证步骤 + 复杂决策路由**时上 Graph；否则保留 Loop。**默认用 Loop，被逼到第四个问题时才升级到 Graph**——不要在一个 trivial 任务上过度工程化。

---

## 十、面试考点速览

| 考点 | 考察点 | 答题要点 |
|------|--------|---------|
| **Loop vs Graph 区别** | 对范式演进的理解 | Loop 解决自动化，Graph 解决方向治理；并发一等公民；多循环互相监督 |
| **四大负向优化陷阱** | 对 Agent 风险认知 | Goodhart's Law / Blindness Upward / Conflict / Measurement Decay |
| **三大防线** | 工程治理能力 | Anchors / Frozen Nodes / External Judgment |
| **Graph 三要素** | 落地能力 | Node（有界执行）/ Edge（条件流转 + 类型化）/ State（reducer + checkpoint） |
| **测试落地** | 结合岗位的实战 | 多 Agent 编排、GraphRAG 影响分析、Agent 可测试性框架 |

---

## 十一、总结

三个层次的认知：

1. **Loop Engineering 解决「自动化」问题**——让 AI 在人类目标不脱轨的前提下自动运转、自我迭代、减少人工干预；
2. **Graph Engineering 解决「方向与有效性」问题**——意识到单纯 Loop 容易为了优化而优化、甚至违背初衷，于是给 Loop **加上监管机制和互相监督体系**；
3. **名字不重要，解决问题才重要**——很多团队可能已经在做 Graph Engineering 的实践，只是不知道它叫这个名字。术语只是大佬们为了传播而打的标签。

对测试开发工程师而言，最高价值的落点有三：

- **用 Graph 编排测试 Agent**：生成 → 审查 → 执行 → 校验 → 评测集守护，互相制衡，杜绝「刷绿」；
- **用 GraphRAG 做影响分析 + 用例生成**：跨接口依赖显式建模，改一个节点精准定位回归，告别脆弱脚本；
- **用 Graph 让测试本身可测试**：单步断言 + 全链路断言，把「AI 测试」变成 CI 里能卡门禁的工程化动作。

> 最后一句共勉（Alex Kotliarskyi 的「graph-max」技巧）：**「画一张图，发给模型，说『写个脚本把这个图跑起来』，没有第三步，就是这么好用。」**

---

## 参考来源

1. 姜剑（飞樰）《从 Loop 到 Graph Engineering 的演进思考与实战》，神州数码千问 AI 平台，2026-09-01
2. Carlos Perez《From Loop Engineering to Graph Engineering? What the shift in AI agent architecture is really about》
3. Flowtivity《From Loops to Graphs: The Next Paradigm in AI Agent Engineering》，2026-07-25
4. Analytics Vidhya《Graph Engineering for AI Agents: Beyond the Single-Agent Loop》，2026-07
5. LangChain 官方文档《Test a ReAct agent with Pytest/Vitest and LangSmith》
6. alphaXiv《Graph Engineering in the Era of LLM Agents: From Individual Intelligence to System Intelligence》
7. GraphRAG-Bench（arXiv 2506.05690）基准数据

---

## 关联文档

- [[wiki/AI相关学习资料/测试开发如何使用DSH]] —— AI 测试工作流的另一条技术路径
- [[wiki/AI相关学习资料/AI编码Agent五工具对比分析报告]] —— 编码 Agent 的能力边界
- [[wiki/AI相关学习资料/Pi的AI设计经验]] —— Agent 架构设计经验与 faux provider 测试方案
- [[wiki/软件测试学习资料/AI Agent与Skill测评方案及落地实践]] —— Agent/Skill 测评方法论

## 源文件

- `.raw/AI相关学习资料/Graph Engineering从概念到测试落地.md`
