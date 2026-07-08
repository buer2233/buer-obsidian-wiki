# RAG测试必背学习资料

> 生成日期：2026-07-08
> 适用对象：邓万鹏，AI自动化测试 / AI产品测试面试
> 生成依据：RAGAS官方文档 + LangSmith RAG评估 + Obsidian RAG学习笔记 + 错题#020
> 重点目标：补齐RAG质量问题、指标和定位方法

---

## 一、官方资料来源

| 来源 | 用途 |
|------|------|
| RAGAS Metrics：https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/ | RAG评估指标 |
| RAGAS Context Precision：https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/ | 检索排序质量 |
| LangSmith RAG Evaluation：https://docs.langchain.com/langsmith/evaluate-rag-tutorial | RAG评估流程 |
| LangChain Docs：https://docs.langchain.com/ | RAG和评估相关能力 |

---

## 二、RAG是什么

RAG = Retrieval-Augmented Generation，检索增强生成。

基本流程：

```text
文档加载 -> 清洗 -> 切分chunk -> 加metadata -> embedding向量化 -> 存入向量库
用户问题 -> 问题向量化 -> Top-K检索 -> rerank -> 拼接上下文 -> LLM生成答案 -> 返回引用
```

核心理解：
```text
RAG质量由检索和生成共同决定。检索器决定事实基础，LLM决定表达能力。
```

---

## 三、RAG常见质量问题

| 问题 | 表现 | 可能原因 |
|------|------|----------|
| 检索不到 | 答案缺信息 | chunk切分差、embedding差、query改写差 |
| 检索错 | 召回无关文档 | 相似度误判、metadata缺失 |
| 上下文冲突 | 多文档说法不一致 | 版本管理差 |
| 答案幻觉 | 编造上下文没有的信息 | Prompt约束弱 |
| 引用错误 | 引用文档不支持答案 | 引用和答案未绑定 |
| 知识过期 | 返回旧规则 | 文档更新时间和版本过滤缺失 |
| 权限泄露 | 检索到无权限文档 | metadata过滤缺失 |
| 噪声干扰 | 无关文档影响回答 | rerank不足 |

---

## 四、RAG指标

### 1. 检索侧指标

| 指标 | 含义 |
|------|------|
| Context Precision | 检索结果中相关上下文是否排在前面 |
| Context Recall | 正确答案所需上下文是否被召回 |
| Top-K命中率 | 期望文档是否出现在Top-K |
| MRR | 第一个相关结果排名越靠前越好 |
| 检索延迟 | 检索耗时 |

### 2. 生成侧指标

| 指标 | 含义 |
|------|------|
| Faithfulness | 回答是否忠实于上下文 |
| Response Relevancy | 回答是否切题 |
| Answer Correctness | 答案是否正确 |
| 引用准确率 | 引用是否支撑答案 |
| 幻觉率 | 是否编造 |

### 3. 面试可说的阈值口径

注意：下面是**测试验收建议阈值**，不是简历里已经上线的产品指标，实际项目要按业务风险调整。

| 指标 | 建议阈值 | 说明 |
|------|----------|------|
| Top-K命中率 | >= 90% | 标准答案文档应进入Top-K |
| Context Recall | >= 85% | 答案所需关键上下文大部分要召回 |
| Context Precision | >= 80% | Top结果不能大量无关，避免噪声干扰 |
| Faithfulness | >= 0.85 | 答案要忠实于检索上下文 |
| Response Relevancy | >= 0.80 | 回答要切题，不跑偏 |
| 引用准确率 | >= 90% | 引用文档要能支撑答案 |
| 幻觉率 | <= 5% | 高风险业务可要求更低 |
| 权限泄露率 | 0 | 企业知识库必须零容忍 |
| P95响应时间 | 按业务SLA设定 | 例如先定3-5秒，再结合模型和检索链路优化 |

背诵表达：
```text
RAG测试不能只说看准确率，我会把指标拆成检索和生成两层。检索侧看Top-K命中、Context Recall、Context Precision，生成侧看Faithfulness、Response Relevancy、引用准确率和幻觉率。阈值不是固定死的，我会先按业务风险设基线，比如权限泄露必须为0，Top-K命中率尽量90%以上，高风险问答的幻觉率要控制在很低水平。
```

---

## 五、RAG怎么测试

### 1. 准备评测集

字段：

```json
{
  "question": "如何配置接口自动化用例？",
  "expected_answer": "基于项目规则创建接口方法和pytest用例",
  "expected_doc_ids": ["api_skill_001"],
  "category": "api_automation"
}
```

### 2. 批量运行

记录：
- 用户问题。
- 检索Top-K文档。
- rerank结果。
- 最终上下文。
- 模型答案。
- 引用。
- 评分。

### 3. 失败定位

```text
答案错 -> 先看检索结果
检索错 -> 看chunk、embedding、query、metadata、rerank
检索对但答案错 -> 看Prompt、上下文拼接、模型、后处理
引用错 -> 看引用生成逻辑
权限错 -> 看metadata过滤和租户隔离
```

---

## 六、知识库更新怎么测

测试点：
- 新文档能被检索。
- 旧文档是否失效或降权。
- 同一问题是否返回新版本。
- metadata中的版本、时间、权限是否生效。
- 增量索引是否成功。
- 失败后是否能回滚。

---

## 七、权限隔离怎么测

企业RAG必问：

```text
不同用户只能检索自己有权限的文档。测试时我会准备不同角色账号，同一个问题分别查询，断言检索结果里不出现无权限文档ID，同时检查最终答案不能泄露无权限内容。
```

---

## 八、结合个人项目

你的接口SKILL已有“结构化索引”思路，可扩展为RAG：

```text
我的接口自动化SKILL当前有接口索引和项目规则，如果引入RAG，我会做成“结构化索引 + 向量索引”。SQLite或数据库用于精确查接口URL、方法位置、文件路径；向量库用于查相似历史用例、需求说明、业务规则和失败案例。AI生成用例前先检索相关上下文，再生成pytest用例并执行，这样比只靠Prompt更可靠。
```

结合真实经验可这样落地：

```text
我做AI+接口自动化SKILL时，其实已经解决了一部分RAG里的上下文问题。比如生成接口用例前，AI要读取项目规则、接口索引、已有用例和源码片段，这相当于先找对上下文再生成。如果进一步升级为RAG，我会把历史用例、接口文档、错误日志和业务规则向量化，同时保留接口URL、文件路径、方法名这类结构化字段，做到语义检索和精确过滤结合。
```

---

## 九、常见面试追问

1. RAG系统怎么测试？
2. RAG幻觉怎么测？
3. Context Precision和Context Recall区别？
4. 答案错了怎么定位是检索问题还是生成问题？
5. 知识库更新后怎么回归？
6. RAG如何防止权限泄露？
7. 向量入库流程是什么？

---

## 十、回答模板

```text
我测RAG会分两层：第一层测检索，关注问题能不能召回正确文档，指标包括Top-K命中率、Context Precision、Context Recall；第二层测生成，关注答案是否基于上下文、是否回答问题、有没有幻觉，指标包括Faithfulness、Response Relevancy、Answer Correctness。自动化上我会准备问题、标准答案和期望文档ID，批量调用RAG接口，记录检索结果、最终答案和评分。如果失败，先判断检索是否正确，再判断模型是否忠实基于上下文回答，这样能定位问题在知识库、召回、重排还是Prompt生成环节。
```

### RAG缺陷定位模板

```text
如果RAG答案错，我不会直接说模型不好，而是按链路排查。第一看检索Top-K里有没有期望文档，如果没有，重点查chunk切分、embedding、query改写、metadata过滤和rerank；第二看检索到了但答案仍然错，就查上下文拼接、Prompt约束、模型生成和后处理；第三看引用是否能支撑答案；第四看权限和版本过滤是否生效。这样能把问题定位到知识库、检索、生成或安全控制哪一层。
```

### STAR模板

```text
S：AI生成接口用例时，模型如果缺少项目上下文，容易生成错路径、错方法或浅断言。
T：我要让AI生成结果更贴合真实项目，并且能通过自动化执行验证。
A：我用项目规则、接口索引、已有用例和源码片段作为上下文，生成后运行pytest，把失败日志回传给AI修复；如果升级为RAG，会增加向量索引检索相似用例和业务规则。
R：最终把AI输出纳入可执行闭环，接口用例编写效率在前后5周对比中提升93.43%，综合效率提升46.48%。
```

---

## 十一、练习清单

- [ ] 背出RAG流程：加载、切分、embedding、入库、检索、生成。
- [ ] 解释Context Precision和Context Recall。
- [ ] 准备一个RAG答案错误的定位流程。
- [ ] 设计一个权限隔离测试用例。
- [ ] 结合接口SKILL说清楚怎么加向量库。
