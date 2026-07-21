# Loop Engineering（循环工程）

来源：

- 微信公众号-小盖fun: https://mp.weixin.qq.com/s/5lzXyqsLJMQIMRIXjsRLiQ

+ 吴恩达 deeplearning.ai The Batch Issue #359
+ 菜鸟教程 Loop Engineering: https://www.runoob.com/ai-agent/loop-engineering.html
抓取时间：2026-07-21

---

## 1. 什么是 Loop Engineering

Loop Engineering（循环工程）是 2026 年 6 月在 AI 编程社区迅速传播的一个新概念。**一句话概括：Loop Engineering 讨论的是如何让 AI 像工程师一样，一边干活、一边验收、一边返工，直到达到要求。**

核心思想：**你不应该再手动给编程 Agent 写提示词了。你应该设计让 Agent 自己提示自己的 Loop（循环）。**

这个概念由以下关键人物共同推动：

| 人物 | 身份 | 核心观点 |
|------|------|---------|
| **Boris Cherny** | Anthropic Claude Code 负责人 | "我不再直接提示 Claude 了。我有一套 Loop 在运行，它们负责提示 Claude 并决定下一步做什么。我的工作是编写 Loop。" |
| **Peter Steinberger** | OpenClaw 创始人（GitHub 史上获星最快的新仓库） | "你不应该再手动提示 AI 编程助手了。你应该设计让 Agent 自己提示自己的 Loop。" |
| **Addy Osmani** | Google 工程师 | 在 Substack 发表长文，将这一实践正式命名并系统化为 Loop Engineering |
| **吴恩达（Andrew Ng）** | deeplearning.ai 创始人 | 在 The Batch Issue #359 中系统阐述了产品开发的三层嵌套 Loop 模型 |

---

## 2. AI 工程的演进：从 Prompt 到 Loop

Loop Engineering 并非凭空而来，它是 AI 编程工具能力演进的自然结果。

### 2.1 四阶段演进

```
Prompt Engineering（怎么问 AI）
    ↓
Context Engineering（给 AI 什么信息）
    ↓
Harness Engineering（如何组织 AI 的能力）
    ↓
Loop Engineering（如何让 AI 持续创造结果）
```

| 工程阶段 | 核心思想 | 关注点 | 输入内容 | AI 能力 | 人的角色 | 典型场景 |
|----------|---------|--------|---------|--------|---------|---------|
| **Prompt Engineering**（提示词工程） | 通过设计提示词获得更好的输出 | 怎么问问题 | Prompt / 指令 | 单轮生成 | 提问者 | 聊天、写作、代码生成 |
| **Context Engineering**（上下文工程） | 组织并提供完整背景信息 | 给 AI 什么信息 | 知识库、历史记录、约束条件 | 上下文理解 | 信息组织者 | RAG、AI搜索、代码助手 |
| **Harness Engineering**（驾驭工程） | 连接模型、工具、数据形成工作流 | 如何调用能力 | 上下文 + API + 工具链 | 执行任务 | 系统设计者 | Agent、自动化流程、多工具协同 |
| **Loop Engineering**（循环工程） | 构建目标驱动的自主闭环系统 | 如何持续完成目标 | 目标、状态、记忆、验证机制 | 规划→执行→验证→修复→持续运行 | 规则制定者 | Claude Code、AI编程、自动运营 |

### 2.2 AI 编程工具的三代演进

| 阶段 | 代表工具 | 工作方式 | 瓶颈 |
|------|---------|---------|------|
| **第一代：自动补全** | GitHub Copilot 早期版本 | 补全当前行或函数，人类主导所有决策 | 只能辅助，不能自主 |
| **第二代：对话式** | ChatGPT、Claude.ai | 问一句，答一句，人类手动推进每一步 | 人类成为瓶颈，速度受限于打字速度 |
| **第三代：Agent 自主循环** | Claude Code、OpenAI Codex Agent | Agent 自主规划、执行、验证，循环迭代直到完成 | 如何设计让 Loop 可靠运行的系统 |

第三代工具的出现意味着：**工程师的核心竞争力从"会写提示词"变成了"会设计 Loop"。**

---

## 3. 吴恩达的三层嵌套 Loop 模型

吴恩达在 The Batch Issue #359 中提出了产品开发的三层嵌套 Loop，这是理解 Loop Engineering 最清晰的框架：

![三层嵌套Loop](C:\Users\admin\Pictures\AI相关\三层嵌套Loop.png)

### 3.1 第一层：Agentic Coding Loop（智能体编码循环）

这是最内层、最快的循环。频率：**几分钟一次**。

- Agent 拿到一份产品需求文档（**Spec**）和一套评测标准（**Eval**）
- 进入循环：写代码 → 运行测试 → 发现问题 → 修改代码 → 再测试
- 如果测试没通过，继续改；如果功能不符合需求，继续改
- **整个过程不需要人工介入**

关键要素：**Spec（规范）+ Eval（评测）= Agent 自主闭环的基础**

### 3.2 第二层：Developer Feedback Loop（开发者反馈循环）

频率：**几十分钟到几小时一次**。

- 开发者审查 Agent 产出的产品，调整 Spec 和 Eval
- Agent 负责实现需求，开发者负责修正需求
- 当我们看到一个功能真正做出来之后，经常会发现自己一开始想的和真正想要的并不是一回事
- 于是重新修改 Spec，把之前没想清楚的地方补充进去，再交给 Agent 继续开发
- 如果 Agent 总是在同一个地方犯错，就补充一套 Eval，把容易踩坑的场景固定下来

**核心洞察：第二层 Loop 就是不断校准自己的认知，并将这些理解逐步沉淀进系统之中。**

吴恩达特别指出：**人类的优势不是"品味"（taste），而是拥有更多上下文（context advantage）。** 人类知道用户是谁、真实使用场景是什么、他们在为什么事情烦恼——这些信息很多不在模型的上下文里。只要人手里还有 AI 不知道的信息，就必须有人参与到这个 Loop 中，把这些关键信息持续注入系统。

### 3.3 第三层：External Feedback Loop（外部反馈循环）

频率：**几小时到几天甚至几周一次**。

- 通过用户反馈、数据分析、竞品研究等方式获取真实世界的反馈
- 关注的是：这个产品方向到底对不对？接下来要做哪些功能？
- 真实世界的反馈 → 影响开发者判断 → 更新 Spec → Agent 继续开发
- 这一层决定了产品的战略方向

**三层 Loop 的关系：外部反馈驱动开发者认知 → 开发者认知沉淀为 Spec/Eval → Spec/Eval 驱动 Agent 编码循环。**

---

## 4. Loop 的核心结构

### 4.1 五大阶段（一个完整循环的内部结构）

一个 Agent Loop 的基础结构由五个阶段构成，首尾相连，不断迭代：

| 阶段 | 英文名 | 做什么 | 典型信号来源 |
|------|--------|--------|-------------|
| **意图** | Intent | 定义目标结果：成功是什么样子，约束是什么 | 开发者或外部系统（Issue、CI 报告） |
| **上下文** | Context | 收集相关代码、文档、报错日志、约定规范 | 代码库、测试输出、历史对话 |
| **行动** | Action | 编辑文件、运行命令、调用工具、草拟方案 | Agent 自主执行 |
| **观察** | Observation | 获取测试结果、编译错误、运行时输出、代码 Diff | 测试框架、类型检查、CI、人工 Review |
| **调整** | Adjustment | 根据观察更新计划，重复循环直到任务完成或被阻塞 | 下一轮内循环 |

> Loop 的力量不在于任何单独的步骤，而在于**闭环**。测试失败不只是一条错误消息，它是新的上下文；类型错误不只是阻断，它是一个关于错误假设的信号；Code Review 评论不只是反馈，它是驱动下一步行动的新观察。

### 4.2 内循环 vs 外循环

| 层级 | 谁在驱动 | 做什么 |
|------|---------|--------|
| **内循环**（Agent 内置） | Agent 自身 | 读文件 → 修改代码 → 运行测试 → 读错误 → 再修改 |
| **外循环**（你来设计） | 你设计的系统 | 按计划发现任务 → 分派 Agent → 验证结果 → 记录状态 → 开启下一轮 |

Loop Engineering 工作在内循环的**上一层**：你不再坐在 Agent 旁边为每一步打下一条指令，而是在设计一套外部系统，它替你驾驶内循环。

---

## 5. 六大构成要素

一个能够真正独立运行的 Loop 需要六个核心组件：

### 要素一：自动触发器（Automations）

自动触发器是 Loop 的**心跳**。没有自动触发，Loop 就只是"你做了一次的操作"，而不是真正意义上的循环。

触发器定义了：**什么时候？做什么？**

示例（Claude Code）：
```bash
# 每天工作日早上 9 点运行
/loop "Read yesterday's CI failures and open issues, write findings
      to TODO.md, and draft fixes for anything labeled quick-win"
      --schedule "0 9 * * 1-5"

# /goal：运行直到一个可验证的条件成立
/goal "All tests in test/auth pass and lint is clean"
```

> **Token 成本警告**：带验证子 Agent 的定时 Loop 每次触发都会消耗 Token，且消耗量因任务复杂度变化显著。建议先设置较慢的节奏（如每天一次），观察几天成本后再加快频率。

### 要素二：并行隔离（Worktrees）

当多个 Agent 同时运行时，文件冲突是最大的风险。Git Worktree 为每个 Agent 提供独立的工作目录，各自在独立的分支上操作。

```bash
git worktree add ../agent-fix-auth feature/fix-auth-tests
git worktree add ../agent-upgrade-deps feature/upgrade-axios
```

> Worktree 消除了机械性的文件冲突，但不能消除**审查瓶颈**。你处理和批准代码变更的速度，才是决定你能并行运行多少个 Agent 的真正上限。

### 要素三：技能文件（Skills）

解决每个新对话 Agent 都要从零推断项目规范的痛点。Skill 写明了项目约定、构建步骤、"我们不这样做是因为那次事故"等知识。

示例（`.claude/skills/project-conventions/SKILL.md`）：
```markdown
---
name: project-conventions
description: 项目编码规范和构建步骤。凡是涉及代码修改的任务都应加载此技能。
---

## 技术栈
- 后端：Node.js 20 + TypeScript 5.4 + Fastify
- 数据库：PostgreSQL 16，ORM 使用 Drizzle
- 测试：Vitest

## 核心约定
- 所有数据库查询必须经过 src/db/queries/ 中的封装函数
- 错误统一使用 AppError 类，禁止 throw 裸字符串
- 新增 API 必须同时更新 docs/api.md
```

### 要素四：连接器（Connectors / MCP）

连接器让 Agent 能够读取 Issue 追踪、查询数据库、调用 API、发消息——而不只是看本地文件系统。

这是"Agent 说'这里是修复方案'"和"Loop 自动开 PR、关联 Ticket、CI 通过后通知频道"之间的核心差异。

> 高风险操作（推送代码、合并 PR、发送外部通知）应当要求人工审批，不能全自动执行。

### 要素五：子 Agent（Sub-Agents）—— Maker-Checker 模式

Loop 中最重要的架构决策之一：**把写代码的 Agent 和检查代码的 Agent 分开。**

写了代码的模型在评分自己的作业时会过于宽容。一个独立的检查器（有时使用更强的模型）能够抓住第一个 Agent 忽略的问题。Claude Code 的 `/goal` 命令在每次迭代后，会用一个单独的模型来判断是否"完成"。

### 要素六：持久记忆（Memory）

模型在每次对话之间会完全遗忘。解决方案极其简单：**把状态写在文件里，文件放在仓库里。** 仓库记得，即使模型不记得。

示例（`TODO.md`，Loop 的状态文件）：
```markdown
# Loop 任务状态
最后更新：2026-06-14 09:03 UTC

## 进行中
- [ ] test/auth/login.spec.ts 中的 flaky test（CI Run #4821）
  - 假设：并发测试之间的 session 状态泄漏
  - 下一步：检查 beforeEach 中的 cleanup 逻辑

## 已完成
- [x] 修复 billing 模块中含单引号公司名称导致的 500 错误（PR #312）
```

---

## 6. 五种常见 Loop 模式

| 模式 | 核心观察信号 | 停止条件 | 典型场景 |
|------|-------------|---------|---------|
| **测试驱动 Loop** | 测试通过 / 失败 | 目标测试全部通过 | Bug 修复、回归测试 |
| **编译器驱动 Loop** | 类型错误、编译错误列表 | 类型检查零错误 | TypeScript 迁移、依赖升级、重构 |
| **Review 驱动 Loop** | 人工 Review 评论 | 所有评论被处理 | PR Review 的机械性跟进 |
| **运行时调试 Loop** | 日志、堆栈跟踪、HTTP 响应 | 问题可复现 → 提出假设 → 验证修复 | 生产 Bug、性能问题 |
| **产品迭代 Loop** | 截图、浏览器检查、可访问性报告 | 与设计稿对齐、响应式正常 | 落地页、UI 调整 |

---

## 7. 构建第一个 Loop（四步法）

### 第一步：从一个窄任务开始

任务越窄，Agent 越清楚哪些文件重要、哪些验证信号相关。

| ❌ 不好的任务定义 | ✅ 好的任务定义 |
|-----------------|----------------|
| "优化仪表盘性能" | "将仪表盘首次加载时间减少 30%，方法是推迟非关键图表加载，同时保持现有过滤器正常工作" |
| "修复 checkout 问题" | "修复 test/checkout/tax.spec.ts 中失败的税额计算测试" |

### 第二步：明确告知验证方式

```bash
# ❌ 差：没有验证条件
/goal "Fix the auth bug"

# ✅ 好：有具体的验证命令和成功标准
/goal "Fix the session leak causing flaky tests in test/auth/login.spec.ts.
      Success condition: run 'pnpm test test/auth/login.spec.ts' 5 times
      consecutively with zero failures."
```

### 第三步：设置保险机制（从只读开始）

```bash
# 推荐的第一个 Loop：只读 + 只写 TODO.md，不开 PR
/loop "Read yesterday's CI failure logs and GitHub Issues labeled 'bug'.
      Categorize findings by likely cause.
      Write a summary with prioritized action items to TODO.md.
      Do NOT edit any source files. Do NOT open any PRs."
      --schedule "0 8 * * 1-5"
```

### 第四步：逐步提升自主程度

| 阶段 | Loop 能做的事 | 人类做的事 |
|------|-------------|-----------|
| 阶段 1（只读） | 发现问题、分类任务、写状态文件 | 审查 TODO.md，手动决定处理顺序 |
| 阶段 2（草稿） | 起草修复方案、运行测试、写入分支 | 审查 diff，手动执行 git push |
| 阶段 3（半自动） | 开 Draft PR，运行 CI，通知 Slack | 审查 PR，手动点击 Merge |
| 阶段 4（全自动） | 制作者 + 检查者双 Agent，CI 通过后自动合并 | 异常时人工介入，定期审计合并历史 |

---

## 8. 三大风险与应对

### 风险一：验证仍然是你的责任

无人值守运行的 Loop，也是无人值守地制造错误的 Loop。**"通过了验证"是一个声明，不是证明。** 对合并代码的人工审查永远不能消失。

### 风险二：理解债（Comprehension Debt）积累更快

Loop 产出代码的速度越快，你实际理解的代码比例就越低。**唯一解药：读 Loop 产出的代码。**

### 风险三：认知投降（Cognitive Surrender）

当 Loop 自动运转时，接受它返回的任何结果是最舒适的选择。**两个人可以构建完全相同的 Loop，却得到截然相反的结果：一个用它更快推进，一个用它回避理解工作本身。**

### 四类故障模式

| 故障模式 | 表现 | 根本原因 | 解决方法 |
|---------|------|---------|---------|
| **空转**（Thrashing） | Agent 反复修改代码但不收敛 | 目标不清晰，或验证信号有噪声 | 缩小目标范围，减少每次 diff 大小 |
| **过拟合测试** | 所有测试通过但功能是错的 | 测试覆盖太窄 | 结合人工验收，增加端到端测试 |
| **上下文漂移** | Agent 基于过期假设持续工作 | 没有在关键观察后刷新上下文 | 在重要观察后重新收集上下文 |
| **不安全的自主** | Agent 无授权执行破坏性操作 | 权限范围过宽 | 最小权限原则，高风险操作必须人工审批 |

---

## 9. 最佳实践总结

| 原则 | 具体做法 |
|------|---------|
| 从窄任务开始 | 每次只定义一个边界明确的目标 |
| 告诉 Agent 如何验证 | 在指令中直接写明验证命令和验收标准 |
| 偏好小的可逆变更 | 最小连贯修改，运行验证后再扩展 |
| 尊重现有代码模式 | 让 Agent 先检查相邻实现，复用现有模式 |
| 人类保持判断席位 | Agent 处理机械性修复；产品判断、架构决策留给人类 |
| 沉淀可复用 Loop | 跑得好的 Loop 固化为 Skill 文件或标准化触发器 |

---

## 10. 面试黄金回答模板

> **问：什么是 Loop Engineering？**

**黄金回答（约 90 秒）：**

> Loop Engineering（循环工程）是 2026 年由 Google 工程师 Addy Osmani 系统化提出的一个概念，核心思想是：**不再手动给 AI Agent 写提示词，而是设计一套让 Agent 自己提示自己、自己验证自己、自己修正自己的闭环系统。**
>
> 吴恩达把它总结为三层嵌套的 Loop：
> 1. **最内层是 Agentic Coding Loop**（分钟级）：Agent 拿到 Spec 和 Eval，自动完成 写代码→测试→发现Bug→修复→再测试 的循环，不需人工介入。
> 2. **中间层是 Developer Feedback Loop**（小时级）：开发者审查 Agent 产出后，修订 Spec、补充 Eval，把认知逐步沉淀进系统。
> 3. **最外层是 External Feedback Loop**（天/周级）：通过用户反馈和数据分析，调整产品战略方向。
>
> Loop Engineering 和传统 Prompt Engineering 的区别在于：前者优化的是"一条指令怎么措辞"，后者优化的是"一个系统如何自主完成目标"。它需要六个核心组件：自动触发器、并行隔离、技能文件、MCP连接器、Maker-Checker子Agent、持久记忆。
>
> 最大的风险是**认知投降**——Loop 自动运转后，人倾向于接受它返回的任何结果而不再思考。所以 Loop Engineering 的终极原则是：**人类掌舵，Agent 执行**。

---

## 11. Loop Engineering vs Harness Engineering：对比分析

### 11.1 相同点

| 共同维度 | 说明 |
|---------|------|
| **层次定位** | 两者都属于 AI 工程的高级阶段，位于 Prompt Engineering 和 Context Engineering 之上 |
| **核心哲学** | 都强调**人类掌舵、Agent 执行**——人做判断，AI 做执行 |
| **系统思维** | 都不聚焦单次对话的质量，而是关注整个 Agent 运行系统的可靠性 |
| **反馈机制** | 都高度重视反馈循环——Harness 有反馈循环护栏，Loop 本身就是反馈循环 |
| **失败预防** | 都关注 Agent 的常见失败模式并设计机制来预防 |
| **工具链** | 都需要 Skills、MCP 连接器、记忆系统等基础设施 |
| **人与 AI 的分工** | 都强调人类保持判断席位，不做甩手掌柜 |
| **目标** | 都是让 Agent 开发更稳定、可维护、可进化 |

### 11.2 不同点

| 对比维度 | Loop Engineering | Harness Engineering |
|---------|-----------------|-------------------|
| **核心概念** | 循环（Loop）——重复迭代直到目标达成 | 驾驭（Harness）——约束和引导 |
| **隐喻来源** | 编程中的循环结构（for/while loop） | 马具（缰绳、马鞍、嚼子）——引导强大但不可预测的动物 |
| **核心动作** | **设计循环**：定义触发条件、验证标准、停止条件 | **设置护栏**：上下文工程、架构约束、反馈循环、熵管理 |
| **时间维度** | 强调**持续运行**——Loop 不停运转 | 强调**约束框架**——在任何时刻都有效 |
| **关注重点** | 如何让 Agent **自主完成目标**（朝目标收敛） | 如何让 Agent **在安全范围内运行**（防止跑偏） |
| **典型产出** | 定时触发的自动化任务、/goal 命令、自运行的 CI 修复流程 | 项目级的 AGENTS.md、自定义 Linter 规则、Code Review Agent、Doc-Gardening |
| **层次结构** | 三层嵌套（内→中→外），时间频率递减 | 四大护栏（并列），协同作用 |
| **失败关注** | 空转、过拟合、上下文漂移、过度自主 | One-Shotting、过早宣布胜利、上下文窗口耗尽 |
| **代表工具** | Claude Code `/loop`、`/goal`、OpenAI Codex Automations | 静态配置文件（AGENTS.md、SKILL.md）、CI/Linter 集成 |
| **提出者** | Boris Cherny、Peter Steinberger、Addy Osmani、吴恩达 | 语雀作者 bbuery（社区实践总结） |

### 11.3 两者如何结合使用

Loop Engineering 和 Harness Engineering 不是竞争关系，而是**互补关系**——一个负责"跑起来"，一个负责"不跑偏"。

**类比：**
- **Harness Engineering = 给赛马装好缰绳、马鞍、嚼子**（确保它不会失控）
- **Loop Engineering = 告诉赛马从起点跑到终点，中途自己调整步伐**（确保它能到达目标）

**结合策略：**

```
第一层：Harness Engineering 打下基础
├── 设置上下文工程护栏 → 确保 Agent 每次都有正确的信息
├── 设置架构约束护栏 → 确保 Agent 不会破坏代码结构
├── 设置反馈循环护栏 → 确保 Agent 能从错误中学习
└── 设置熵管理护栏 → 确保系统长期健康

第二层：Loop Engineering 释放效能
├── 在最内层 Loop 中：护栏确保每次迭代安全
├── 在中间层 Loop 中：开发者反馈沉淀为新的护栏规则
└── 在最外层 Loop 中：真实世界反馈校准护栏的方向
```

**具体做法：**

1. **先用 Harness 建护栏，再用 Loop 跑起来**
   - 先写好 AGENTS.md、SKILL.md，配置好 Linter 和 MCP
   - 然后设计第一个只读 Loop 验证系统是否稳定

2. **Loop 跑出来的问题，反哺 Harness**
   - Loop 中发现的 Agent 反复犯的错误 → 沉淀为新的架构约束
   - Loop 中上下文不足导致的问题 → 优化上下文工程策略
   - Loop 跑久了积累的混乱 → 触发熵管理（Doc-Gardening）

3. **Harness 的"反馈循环"护栏和 Loop 天然同构**
   - Harness 的反馈循环护栏本质上就是一个 Loop
   - 可以把这个反馈循环升级为标准的 Loop Engineering 实践，加入自动触发和持久记忆

**一句话总结：Harness 是 Loop 的安全网，Loop 是 Harness 的动力引擎。两者配合，才能让 Agent 既跑得快，又不翻车。**
