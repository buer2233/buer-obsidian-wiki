# Compound Vault — v1.7 指南

**状态：** v1.7.0（代号 "Compound Vault refoundation"），发布于 2026-05-17
**受众：** 从 v1.6 升级的用户、新用户，以及与 v1.7+ 原语集成的技能作者
**配套文档：** [dragonscale-guide.md](dragonscale-guide.md)（可选的 Memory 扩展）、[install-guide.md](install-guide.md)、[CHANGELOG.md](../CHANGELOG.md)

---

## 为什么叫 "Compound Vault"

v1.7 系列引入了一个系统名称 —— **Compound Vault** —— 用于命名该架构，与插件名称（`claude-obsidian`）区分开来。插件名称保留以维持 SEO 连续性和现有的 4.1k+ stars；系统名称涵盖了使该架构运作的 13 个协同技能。

三句话定位：

> *"复利型知识库，而非聊天。CLI 原生，而非聊天窗口。方法论感知，而非通用。"*

- **复利型知识库（Compounding vault）** —— Karpathy 的 LLM Wiki 模式。知识在会话间累积；每次导入都让知识库更加丰富。
- **CLI 原生（CLI-native）** —— Obsidian 1.12 使 `obsidian` 二进制文件成为一流的表面。v1.7 将其作为默认传输方式，并将 MCP 降级为回退方案。
- **方法论感知（Methodology-aware）** —— 在 v1.7 中是部分实现的（模式在 v1.8 中发布）。这个定位已经影响了 v1.7 的范围。

备选标语（用于博客/营销）：

> **"Karpathy 的 wiki，就在你的 Obsidian 中。"**

---

## 与 v1.6 相比的变化（概要）

v1.7 分四个工作流发布（§3.1 基础层 / §3.2 传输层 / §3.3 检索层 / §3.4 并发控制），每个工作流都足够独立，可以在出问题时单独回滚。没有破坏性变更 —— 一个不执行任何升级操作的 v1.6 知识库在升级后行为与 v1.6 完全一致。

| 工作流 | 内容 | 原因 | 用户操作 |
|---|---|---|---|
| §3.1 基础层 | 3 个技能从软降级升级为硬优先 `kepano/obsidian-skills` | 停止与平台所有者竞争 | `claude plugin marketplace add kepano/obsidian-skills`（推荐） |
| §3.2 传输层 | 新增 `wiki-cli` 技能 + `detect-transport.sh` + 决策树 | Obsidian 1.12 CLI 是最快、最安全的写入路径 | 无需操作 —— 首次会话自动检测 |
| §3.3 检索层 | 新增 `wiki-retrieve` 技能 + 上下文前缀 + BM25 + 余弦重排序 | Anthropic 2024年9月研究：检索失败减少 35-67% | `bash bin/setup-retrieve.sh`（可选） |
| §3.4 并发控制 | 新增 `wiki-lock.sh` + 4 个技能守卫 + hook 防抖 | 关闭潜在的多写者数据损坏漏洞 | 无需操作 —— 全局有益，无需设置 |

---

## §3.1 对 kepano/obsidian-skills 的基础层依赖

**是什么：** 三个 claude-obsidian 技能（`obsidian-markdown`、`obsidian-bases`、`canvas`）与 `kepano/obsidian-skills`（由 Obsidian CEO Steph Ango 开发）中的技能存在重叠。在 v1.6 中我们采用软降级策略（"如果安装了 kepano，则优先使用它"）。在 v1.7 中我们采用硬优先策略：kepano 是权威实现；我们的版本作为兜底方案。

**原因：** 继续发布与平台所有者原语平行的实现是一场结构性的必败之战。kepano 市场有 30.5k+ stars；我们有 4.1k+。采用 kepano 作为基础层表明了对齐立场，并使我们能够专注于*工作流*层（导入、查询、检查、自动研究、保存、检索）——这是其他人没有掌控的领域。

**代码库中的变更：**
- `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/obsidian-markdown/SKILL.md:11` —— 前言改写为"此技能是独立的兜底方案。优先使用 `kepano/obsidian-skills`。"
- `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/obsidian-bases/SKILL.md:11` —— 相同模式。
- `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/canvas/SKILL.md:14` —— 相同模式（json-canvas 规范降级到 kepano；wiki 范围的工作流仍由 claude-obsidian 负责）。
- `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/defuddle/SKILL.md:11` —— 记录为权威实现（kepano 不提供 defuddle 技能）。
- `.claude-plugin/marketplace.json` —— `recommendedCompanions` 数组中包含 `kepano/obsidian-skills`，附带安装提示、理由和仓库链接。

**用户操作：** 运行 `claude plugin marketplace add kepano/obsidian-skills`。现有技能在没有它的情况下仍然正常工作（本地兜底方案保持功能）。

---

## §3.2 默认传输层 —— Obsidian CLI 与回退链

**是什么：** 一个四层传输栈，支持自动检测。新增技能 `wiki-cli` 记录了 CLI 操作方案。新增脚本 `scripts/detect-transport.sh` 写入 `.vault-meta/transport.json`，以便其他技能可以查询。

回退链（优先级从高到低）：
1. **cli** —— `obsidian-cli` 二进制文件（Obsidian 1.12+）。无需 MCP 服务器、无需 TLS、无需插件。
2. **mcp-obsidian** —— 基于 REST API 的 MCP 服务器（需要 Local REST API 插件）。自动检测推迟到 v1.7.x。
3. **mcpvault** —— 基于文件系统的 MCP 服务器（BM25 搜索；无需 Obsidian 插件）。自动检测推迟。
4. **filesystem** —— 直接使用 `Read`/`Write`/`Edit` 工具。始终可用；兜底方案。

**原因：** v1.6 文档中列出了四种平等的传输方式。技能默认使用直接 `Read`/`Write`。v1.7 明确了推荐方案，并使选择成为对 `.vault-meta/transport.json` 的单行查询。

**架构：**

```
detect-transport.sh（在会话启动或知识库设置时运行）
    │
    └─ 写入 → .vault-meta/transport.json
                {
                  "preferred": "cli" | "filesystem",
                  "fallback_chain": [...],
                  "available": { cli: {...}, filesystem: {...}, mcp_obsidian: null, mcpvault: null }
                }

技能（wiki-ingest、wiki-query、save、autoresearch、wiki-lint）：
    ├─ 每个技能顶部都有"## Transport (v1.7+)"部分
    ├─ 运行时读取 transport.json
    └─ 如果 "preferred": "cli" 则使用 obsidian-cli，否则使用 Read/Write
```

**用户操作：** 无需操作 —— 检测自动运行，7 天后刷新。要强制刷新：`bash scripts/detect-transport.sh --force`。要手动固定到某个 MCP 传输方式，编辑 `.vault-meta/transport.json` 并设置 `"manual_override": true`，这样检测脚本会保留你的编辑。

**参见：** [`wiki/references/transport-fallback.md`](../wiki/references/transport-fallback.md) 了解完整决策树，`~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/wiki-cli/SKILL.md`（全局插件）了解每个操作的方案。

---

## §3.3 混合检索管道 —— wiki-retrieve（可选）

**是什么：** 一个新增的可选技能，替代 v1.6 的静态 `Read(hot.md) → Read(index.md) → Read(N pages)` 查询路径，转而使用基于上下文前缀分块的 BM25 + 余弦重排序进行分块级检索。实现了 Anthropic 的 [2024年9月上下文检索](https://www.anthropic.com/news/contextual-retrieval) 模式，作为 agent 技能管道。

**原因：** 页面级粒度在答案位于特定段落时总是输给分块级粒度。Anthropic 测量到上下文前缀减少了 35% 的检索失败，混合 BM25+向量减少了 49%，加上重排序器减少了 67%。v1.7 实现了上下文 + 稀疏 + 重排序栈。（独立的稠密向量阶段在 v1.7.x 路线图上。）

**架构：**

```
INGEST（一次性 + 增量）：

  wiki/<page>.md
       │
       ▼
  scripts/contextual-prefix.py
       │  ├─ 按段落边界分块（约500 tokens目标，200字符重叠）
       │  └─ 为每个分块生成1-2句话的前缀
       │       层级1：ANTHROPIC_API_KEY → Anthropic API（Haiku，prompt-cached
       │                                    当正文 ≥ ~16 KB / Haiku 4.5 下限时）
       │       层级2：claude on PATH   → `claude -p` 子进程
       │       层级3：合成式           → frontmatter 标题 + 第一段
       │
       ▼  .vault-meta/chunks/<address>/chunk-NNN.json

  scripts/bm25-index.py build
       └─ 对分块的上下文化文本构建倒排索引 → .vault-meta/bm25/index.json

QUERY：

  query string
       │
       ▼
  scripts/retrieve.py "<query>" --top 5
       ├─ scripts/bm25-index.py query → BM25 排名前20的候选
       ├─ scripts/rerank.py           → 通过 ollama 的 nomic-embed-text 计算余弦相似度
       │     （如果 ollama 不可达则跳过；保留 BM25 排序）
       └─ 页面地址去重              → 最终 top-5 及绝对路径
       │
       ▼
  调用者（wiki-query / autoresearch）读取被引用的页面并进行综合
```

**功能门控：** 其他技能通过以下方式检测 wiki-retrieve：

```bash
[ -x scripts/retrieve.py ] && [ -d .vault-meta/chunks ] && [ -f .vault-meta/bm25/index.json ]
```

如果检测失败，技能回退到 v1.6 的遗留读取顺序。该技能永远不会破坏基础插件。

**成本上限：** 按 Anthropic 公布的数据，约 $12/1000 个文档（Haiku + prompt caching，层级1）。层级2（claude CLI）在费用上免费但较慢。层级3（合成式）免费且完全离线；会失去大部分上下文收益，但 BM25 + 重排序仍然有效。

**用户操作：**

```bash
bash bin/setup-retrieve.sh           # 完整配置（自动选择前缀层级）
bash bin/setup-retrieve.sh --no-llm  # 强制使用层级3（零 LLM 依赖）
bash bin/setup-retrieve.sh --check   # 仅诊断；不进行配置
```

设置完成后，`wiki-query` 的标准/深度模式自动使用新管道。快速模式（仅 hot.md）保持不变。

**参见：** `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/wiki-retrieve/SKILL.md`（全局插件）了解完整技能规范、方案参考和 v1.7.x 路线图（BGE 交叉编码器、Cohere Rerank、独立稠密向量阶段）。

---

## §3.4 多写者安全 —— wiki-lock（核心）

**是什么：** 通过 `scripts/wiki-lock.sh` 实现的基于文件的建议性锁。每次 wiki 页面写入**必须**在之前执行 `wiki-lock acquire <path>`，之后执行 `wiki-lock release <path>`。

**原因：** v1.6 存在一个潜在的数据损坏漏洞。`~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/wiki-ingest/SKILL.md:259-264` 将"单写者"记录为惯例，但实际的页面写入路径没有强制执行。两个并行的子 agent 写入同一个 wiki 页面可能会互相静默覆盖。Karpathy-LLM-Wiki-Stack 的 README 明确警告了这一点。v.1.7 堵住了这个漏洞。

**设计（基于时间戳，而非 flock 风格）：**

`flock(2)` 建议性锁在持有进程退出时释放。这不符合我们的模型，因为 `acquire` 和 `release` 是同一技能的**独立** bash 调用（每次 Bash 工具调用都是自己短暂的进程 —— 两个 PID 存活时间都不够长，没有意义）。所以 `wiki-lock.sh` 使用：

- **原子性的 noclobber 锁文件写入**（在 POSIX 文件系统上竞争安全）。
- **基于纪元时间的 AGE 过期**：超过 `STALE_AFTER_SEC`（默认60秒）的锁会自动回收。崩溃的持有者在 ≤60 秒内自动解除阻塞，无需人工干预。
- **允许跨进程释放**：`release` 是 `rm -f`（不需要 PID 匹配）。信任技能作者释放他们获取的锁。`wiki-lock clear-stale --max-age 0` 命令是规范的恢复路径。
- **锁文件中的 PID 仅供参考**（有助于 `list` 和调试）。

**技能集成：**

四个技能新增了"## Concurrency (v1.7+)"部分，包含以下方案：

```bash
if bash scripts/wiki-lock.sh acquire wiki/concepts/Foo.md; then
  # … 通过 §Transport 选择的方法进行写入 …
  bash scripts/wiki-lock.sh release wiki/concepts/Foo.md
else
  # rc=75 = EX_TEMPFAIL = 另一个写者正在写入。等待2秒后重试一次；
  # 如果仍被锁定，记录到 wiki/log.md 并跳过此页面。
  sleep 2
  bash scripts/wiki-lock.sh acquire wiki/concepts/Foo.md && {
    # 写入 …
    bash scripts/wiki-lock.sh release wiki/concepts/Foo.md
  } || echo "skipped wiki/concepts/Foo.md (locked)"
fi
```

**Hook 集成：** 全局插件 `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/hooks/hooks.json` 的 PostToolUse 现在会在有锁被持有时延迟 `git add`。防止多 agent 导入期间的不完整提交。当 `wiki-lock.sh` 不存在时优雅降级。

**用户操作：** 无需操作 —— `wiki-lock.sh` 在 v1.7 中是核心功能（无需手动启用）。不遵循 acquire/release 模式的子 agent 与任何其他写者存在竞争风险（与之前相同 —— 但现在有工具可以修复）。

**测试覆盖：** `tests/test_wiki_lock.sh`（14 个独立断言）和 `tests/test_concurrent_write.sh`（关键的正确性门槛 —— 10 个并行工作者，无丢失，无乱行）。`make test-concurrent` 和 `make test-lock`。

**参见：** [`scripts/wiki-lock.sh`](../scripts/wiki-lock.sh) 头部注释了解完整语义，`~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/wiki-ingest/SKILL.md` §Concurrency 了解规范集成模式。

---

## 技能清单（v1.7）

共 13 个技能。v1.7 新增：`wiki-cli`、`wiki-retrieve`。

| 技能 | 状态 | 角色 |
|---|---|---|
| `wiki` | 核心 | 设置 / 脚手架 / 子技能路由器 |
| `wiki-ingest` | 核心 | 源文件 → wiki 页面，含交叉引用 |
| `wiki-query` | 核心 | 问答（现在如果已安装则使用 wiki-retrieve） |
| `wiki-lint` | 核心 | 健康检查（孤立页面、死链接、地址、平铺） |
| `wiki-fold` | DragonScale 机制 1 | 提取式日志滚动 |
| `wiki-cli` | **v1.7 新增（§3.2）** | Obsidian CLI 传输包装器 |
| `wiki-retrieve` | **v1.7 新增（§3.3，可选）** | 上下文 + BM25 + 重排序 |
| `save` | 核心 | 将对话保存为 wiki 笔记 |
| `autoresearch` | 核心 | 迭代式网络研究 → wiki |
| `canvas` | 核心（降级到 kepano json-canvas） | 可视化 wiki 层 |
| `defuddle` | 核心（权威实现） | 网页清理器 |
| `obsidian-markdown` | 核心（降级到 kepano） | Obsidian 风格 Markdown 参考 |
| `obsidian-bases` | 核心（降级到 kepano） | Bases YAML 参考 |

---

## 脚本清单（v1.7）

| 脚本 | 状态 | 角色 |
|---|---|---|
| `allocate-address.sh` | DragonScale 机制 2 | 原子性 c-NNNNNN 分配器（flock） |
| `tiling-check.py` | DragonScale 机制 3 | 基于嵌入的重复检查（fcntl） |
| `boundary-score.py` | DragonScale 机制 4 | 自动研究的前沿评分 |
| `detect-transport.sh` | **v1.7 新增（§3.2）** | 传输检测 → transport.json |
| `contextual-prefix.py` | **v1.7 新增（§3.3）** | 分块 + 3层前缀生成 |
| `bm25-index.py` | **v1.7 新增（§3.3）** | 稀疏倒排索引（flock） |
| `rerank.py` | **v1.7 新增（§3.3）** | 通过 ollama 的余弦重排序（fcntl 缓存） |
| `retrieve.py` | **v1.7 新增（§3.3）** | 混合检索编排器 |
| `wiki-lock.sh` | **v1.7 新增（§3.4）** | 基于文件的建议性锁（noclobber） |

---

## 测试（v1.7）

`make test` 运行 7 个测试套件。全部独立 —— 零网络、零 ollama、零 LLM 调用。

| 目标 | 文件 | 断言数 | 覆盖范围 |
|---|---|---|---|
| `make test-address` | `tests/test_allocate_address.sh` | ~10 | DragonScale 机制 2 |
| `make test-tiling` | `tests/test_tiling_check.py` | ~15 | DragonScale 机制 3 |
| `make test-boundary` | `tests/test_boundary_score.py` | ~35 | DragonScale 机制 4 |
| `make test-bm25` | `tests/test_bm25_index.py` | ~30 | 分词、BM25 单调性、IDF |
| `make test-retrieve` | `tests/test_retrieve.py` | 22 | 余弦相似度、重排序、端到端子进程 |
| `make test-lock` | `tests/test_wiki_lock.sh` | 14 | 获取、释放、基于时间戳的回收 |
| `make test-concurrent` | `tests/test_concurrent_write.sh` | 6 | **关键的多写者正确性门槛** |

"独立测试不变量"得到保持：`make test` 中没有任何内容需要网络、ollama 或任何 API 密钥。可选管道（使用 Anthropic API 的上下文前缀、使用 ollama 余弦的重排序）通过 mock 和优雅降级进行测试。

---

## v1.7 不是什么

- 不是重写。DragonScale 机制 1-4 得到保留且未改变。
- 不是破坏性变更。不运行 setup-retrieve.sh 的 v1.6 知识库不会看到行为差异（wiki-lock 集成除外，这是全局有益的且无需设置）。
- 不是付费插件。许可证保持 MIT。
- 不是 GUI Obsidian 插件外壳。推迟到 v2.5+（Claudian/deivid11 包装模式是 2026 年 5 月差距分析待办列表中的第 7 项）。
- 不是多知识库联邦。推迟到 v2.x。

---

## 路线图指引

2026 年 5 月的差距分析确定了 20 个待办事项。v1.7 发布了第 1、2、3、4 项（按价值/工作量排在前四分之一）加上潜在漏洞修复。下一个里程碑（取决于用户优先级）：

- **v1.8** —— 方法论模式（LYT / PARA / Zettelkasten / 通用，通过 `wiki-mode`）+ 定期回顾（`wiki-review`）。关闭差距 #6 + #11。
- **v1.9** —— 多模态导入适配器（YouTube、PDF、EPUB、图片 OCR，通过 `wiki-ingest-multimodal`）。关闭差距 #8 + #12。
- **v2.0** —— NotebookLM 级别的衍生输出（音频、测验、闪卡、学习指南，通过 `wiki-derive`）。关闭差距 #5 + #9 + #14。

完整计划：`~/.claude/plans/read-in-full-the-hidden-sun.md`。

---

## 另请参见

- [CHANGELOG.md](../CHANGELOG.md) —— v1.7.0 条目
- [docs/dragonscale-guide.md](dragonscale-guide.md) —— DragonScale Memory 扩展（机制 1-4）
- [docs/install-guide.md](install-guide.md) —— 安装指南
- [wiki/references/transport-fallback.md](../wiki/references/transport-fallback.md) —— 传输决策树
- [wiki/concepts/DragonScale Memory.md](../wiki/concepts/DragonScale%20Memory.md) —— 规范
- Anthropic 上下文检索：https://www.anthropic.com/news/contextual-retrieval
- kepano/obsidian-skills：https://github.com/kepano/obsidian-skills
- Karpathy LLM Wiki gist：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
