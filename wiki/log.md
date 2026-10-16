---
type: meta
title: "知识库日志"
created: 2026-07-01
updated: 2026-10-16
---

# 知识库日志

## [2026-10-16] fix | 去重 `.raw/`、补全覆盖面、修两个静默故障的根因

- 触发：主人三条指令 —— ① 删除完全相同的文件，只保留子目录内容；② raw 内容全部要建立 wiki；③ 查明根因并修复。
- **① 去重**：`.raw/AI相关学习资料/` 根目录 5 个文件与 `pi/` 子目录**逐字节相同**（md5 逐一核验，非仅比大小），删除根目录副本、保留 `pi/`（该目录是主人按项目重组 `.raw/` 的新结构，mtime 与会话同期）。同步改向全部引用：5 篇 wiki 页的 `source:` / `sources:`、`wiki/AI相关学习资料/index.md` 源文件清单、`.raw/.manifest.json` 的 5 个键。全 `.raw/` 哈希查重确认**别无其他重复对**（另发现 1 对同图不同名的 MCP 架构图，属两篇源各自引用的合理复用，不删）。5 个删除文件均已入 git 历史，可恢复。
- **② 覆盖面**：改造后的检查器暴露出**唯一真正被漏掉的 raw 文件**——`.raw/claude-obsidian-ecosystem-research.md`（288 行，2026-04-08 的 Claude+Obsidian 生态调研，已被 [[wiki/来源/LLM Wiki模式]] 与 [[wiki/概念/wiki一词与Wiki知识库]] 当作 `sources:` 引用，却**自己没有 wiki 页**）。补建 [[wiki/来源/claude-obsidian生态调研]]（四条技术路线、4 个同类项目、10 条设计模式 × 本 vault 缺口对照表）。此后 `未映射 0`，**覆盖率可证明为 100%**。
- **③ 根因 1 —— 检查器有"静默排除"**（这是漏收录能长期潜伏的机制）：`check_raw_updates.py` 的 `should_skip()` 用一张硬编码清单静默排除了 `assets/`/`screenshots/`/`data/`/`transcripts/` **以及 `claude-obsidian-ecosystem-research.md`**。被排除的文件既不在"已同步"也不在"未映射"——**从报告里彻底消失**。修复：`should_skip` → `exclusion_reason()`，**每个扫描到的文件都落进可见分桶**（待更新 / 已同步 / 图片素材 / 未映射 / **已排除并附原因**）；图片单独成桶（它们不单独建页，wiki 归属就是引用它们的页面）；**退出码改为"有内容未入账即非零"**，可用于工作流门禁——这正是原先缺失的闭环信号。
- **③ 根因 2 —— `wiki-lock.sh` 在 Windows 上整体失效**：`.vault-meta/hook.log` 里堆满 `wiki-lock list failed rc=1; deferred auto-commit`。追查到 `flock: command not found`——脚本第 156 行的元锁用了 **Linux 专有的 `flock`**，Git Bash / MSYS 不带。后果是**双重静默故障**：所有 `wiki-lock` 命令失败，且 PostToolUse 自动提交钩子把"锁查询失败"读作"锁状态未知"，于是**永远推迟提交**——自动提交在这台机器上已静默死亡。修复：保留 Linux 上 flock 路径不变，新增 **`mkdir` 原子互斥回退**（含 5s 超时与崩溃持有者的 stale 回收）。验证 `list`/`acquire`/`release` 全部 rc=0。
- 附带修复：`find_wiki()` 规则 6（`FILENAME_MAP`）此前对 **`.raw/` 根目录级**文件必然失败（会去 walk 一个不存在的"分类目录"），改为回退搜索整个 `wiki/`；新增 `claude-obsidian-ecosystem-research` 映射条目。
- 更新：[[wiki/index]]、[[wiki/来源/_index]]、[[wiki/元数据/dashboard]]、`wiki/hot.md`、`.raw/.manifest.json`（`last_sync=2026-10-16`，sources 40 条）。
- 安全处置：根因 2 修好意味着**自动提交重新激活**，而主人并未要求提交 → 用钩子自带的 `.vault-meta/auto-commit.disabled` 开关在会话期间按住提交，**收尾时撤销**，避免产生一笔卷入上个会话遗留改动的通用提交。
- 关键洞察：**两个故障的共同形态是"沉默"**——静默排除让内容失踪，`rc=1` 让自动化停摆，两者都不报错、不阻塞、不留用户可见痕迹。**能被静默容忍的失败，一定会长期存在。**

## [2026-10-15] check + ingest | 补齐 8 份 AI 学习资料、新建「学习简图」分类、修复检查器假阳性

- 触发：执行 Wiki 检查，收录未纳入 wiki 的文件。
- 检查：`scripts/check_raw_updates.py` 扫描 178 个文件 → 待更新 0 / 已同步 100 / 未映射 74 / 跳过 4。**74 项经人工核对拆为三类**：真未收录 8 篇 md、脚本假阳性 33 项、孤儿素材 3 项。
- 新建页面（`wiki/AI相关学习资料/`，7 篇）：[[wiki/AI相关学习资料/RAG的流程与应用]]、[[wiki/AI相关学习资料/REA逆向工程MCP工具学习手册]]、[[wiki/AI相关学习资料/Ontology本体工程从概念到企业流程与测试流程落地]]、[[wiki/AI相关学习资料/Anthropic源代码控制系统重设计]]、[[wiki/AI相关学习资料/AI工具资源占用沟通与面试应答]]、[[wiki/AI相关学习资料/Jev决策模型(System One)学习参考资料]]、[[wiki/AI相关学习资料/Jev用于UI自动化测试可行性分析与AI测试工具横向对比]]、[[wiki/AI相关学习资料/TypeSafe_Jev国内使用指南(官网导航+四条接入路径+实测连通性)]]（共 8 篇）。
- 新建分类：`wiki/学习简图/`（[[wiki/学习简图/数据结构总览]] + [[wiki/学习简图/_index]]）——把 `.raw/学习简图/` 下的「一图流」思维导图翻译成**可检索的结构**（内嵌原图 + 文字速查表）。
- 孤儿素材归位：`.raw/AI相关学习资料/images/raw_p4_xref182/183.png` 经看图确认是 Transformer 原论文 Figure 2 的「缩放点积注意力流程」与「多头注意力结构」，接入 [[wiki/AI相关学习资料/大模型核心原理]] §3.3（该节此前无配图）。
- 新建素材：38 张配图复制至 `_attachments/images/AI相关学习资料/{RAG的流程与应用,REA逆向工程MCP工具学习手册,Ontology本体工程,Anthropic源代码控制系统重设计}/`；1 张思维导图复制至 `_attachments/images/学习简图/`。`_attachments` 由 22 → 61 个文件。
- **检查器修复（`scripts/check_raw_updates.py`）**：① Windows 控制台 GBK 编码下 emoji 触发 `UnicodeEncodeError` 直接崩溃 → 启动时 `reconfigure(encoding='utf-8')`；② 新增规则 4b「同分类内按文件名回退匹配」——消除 `pi/` 拍平导致的 5 项假阳性（原始 33 项假阳性中，另 28 项由新增的图片引用判定消除）；③ 图片改判为「**被 wiki 页引用即视为已收录**」，同时能反向抓出「复制了却无人引用」的孤儿附件。修后报告：**未映射 0 / 待更新 0**。
- 校验：`wiki-linkcheck.py` 逐文件检查 8 篇新页 + 2 篇学习简图页 + 2 篇改动页，**断链 0、歧义 0**；38 + 7 处图片路径逐条 `[ -f ]` 验证存在；检查器单元行为测试 6/6 通过（确认放宽后仍能报出"不存在的图片/未收录文档"）。
- 更新：[[wiki/index]]（新增「学习简图」板块 + AI 分类 8 项 + 全量目录）、[[wiki/AI相关学习资料/index]]（20 页目录重排 + 源文件 8 条）、[[wiki/元数据/dashboard]]、`.raw/.manifest.json`（9 条新源登记，`last_sync=2026-10-15`）。
- 关键洞察：**检查脚本负责「召回」，人工核对负责「精确」**。74 项未映射里真正需要处理的只有 8 项（11%）；若照脚本输出批量建页，会为 5 个逐字节重复文件建 5 个冗余页、为 33 张已引用图片建页。**修检测器比改内容布局更根本**——否则每次检查都要人肉筛掉同一批假阳性，检查本身失去可信度。
- 源文件自身问题（已在页内用 `[!gap]` 标注，未静默沿用）：① `RAG的流程与应用` §7.1/§5.3 称 HNSW「三个坑」但实列 4 项，页面按事实表述为四项；② `Ontology本体工程` 中 Palantir 量化数据为厂商自述且 NHS FDP 案例有实质争议；③ `Anthropic源代码控制系统重设计` 中「CI 检出 175 秒」与「31 秒→3.5 秒」两处口径并存，未说明是否不同时期。
- **遗留（未处理，需主人决策）**：① `.raw/AI相关学习资料/pi/` 下 5 个文件与根目录**逐字节相同**（冗余副本，未删除）；② `scripts/rebuild_wiki_links.py` 仍不可整体运行——其 `wiki_target()` 生成不带 `wiki/` 前缀的链接，且会**整体覆盖 `wiki/hot.md`**；本次仅以 `import` 方式调用其 `update_root_index()` 做差异预览，**最终未运行**（预览显示它会把手写目录里的 `[[wiki/AI相关学习资料/X|X]]` 降级为裸链接 `[[X]]`，故改为手工维护目录）；③ 全库仍有约 70 处 basename 歧义链接（`.raw` 同名导致）。

## [2026-09-23] archive + ingest | wiki 概念问答归档（首次贯通问答闭环）

- 来源：`.raw/笔记/2026-09-23_wiki一词与Wiki知识库.md`（WorkBuddy 会话原始记录）
- 归档问答：[[wiki/问答/2026-09-23_wiki一词与Wiki知识库|wiki、wiki技术、Wiki知识库三者关系]]
- 创建的页面：[[wiki/概念/wiki一词与Wiki知识库]]、[[wiki/来源/LLM Wiki模式]]、[[wiki/对比/LLM Wiki与chunk-first RAG对比]]、[[wiki/实体/Ward Cunningham]]、[[wiki/笔记/2026-09-23_wiki一词与Wiki知识库]]、[[wiki/概念/_index]]
- 更新的页面：[[wiki/index]]、[[wiki/笔记/index]]、[[wiki/元数据/dashboard]]、[[wiki/问答/_index]]、[[wiki/实体/_index]]、[[wiki/对比/_index]]、[[wiki/来源/_index]]
- 关键洞察：**本 vault 第一个归档问答，「好答案写回 wiki 形成复利」这一环首次跑通**。此前 `wiki/问答/` 自 2026-07-01 创建以来一直为空——知识在聊天中产生却从未沉淀，正是 Karpathy 所指的「不累积」问题的具体表现。
- 概念层结论：`wiki` 三层含义（单词 → 技术 → 知识库）构成单向链，**单词命名技术，技术生产知识库**；本 vault 属 Karpathy LLM Wiki 模式（三层架构 + ingest/query/lint）。
- 附带纠正三条环境事实：① vault 根为 `D:\AI\Hermes\claude-obsidian`（非工作区 `learn`）；② `.raw/` 源引用**不能用 wikilink**（触发 git pathspec 歧义），全库约定为 frontmatter 纯字符串；③ `obsidian_simple_search` 全库搜索会因返回量超限而失败，须改用目录列举 + 定向读取。
- 流程修正：`.raw/笔记/X.md` 须 1:1 映射到 `wiki/笔记/X.md`（`check_raw_updates.py` 对 `笔记/`、`Codex/` 走同路径直接映射），仅建 `wiki/问答/` 会被判「未映射」且静默不报错 → 已补齐笔记页。
- 校验结果：`wiki-linkcheck.py` 逐文件校验新页**歧义 0**；`git show HEAD` 差集确认**新引入断链 0**，并修复 `dashboard.md` 既有断链 5 处；`check_raw_updates.py` **待更新 0**。
- 核实动作：词源与 LLM Wiki 模式事实经在线检索复核（检索日期 2026-09-23）。

## 2026-09-10 - 摄入 | 11 份新学习资料（AI + 测试开发）

- 新增源：`.raw/AI相关学习资料/` 9 份（大模型核心原理、大模型必学基础知识、AI编码Agent五工具对比分析报告、OMP使用手册、OMP的设计经验、Pi的AI设计经验、Pi源码精读顺序清单、测试开发如何使用DSH、Graph Engineering从概念到测试落地）。
- 新增源：`.raw/测试开发相关学习资料/` 2 份（Flask-DRF与Java后端框架对照学习、JaCoCo代码覆盖率工具从入门到工程落地）。
- 新建分类目录 `wiki/测试开发相关学习资料/`（2 页面 + index）。
- `wiki/AI相关学习资料/` 由 3 页扩充至 12 页；新增 images 素材 25 张，复制至 `_attachments/images/AI相关学习资料/`，页面以相对路径引用。
- **架构修正**：`Pi与AI编程Agent对比分析` 由「5 包架构」更正为「9 包架构」（`agent`/`evals`/`coding-agent`/`protocol`/`server`/`ai`/`tui`/`client`/`session-backends/sqlite-node`），并清除全文 `pi-telemetry` 旧包名；同页 6 条 basename 歧义链接改为 `[[wiki/完整路径|别名]]`。
- 更新：`wiki/AI相关学习资料/index.md`、`wiki/index.md`、`wiki/hot.md`、`.raw/.manifest.json`（11 条新源登记，`last_sync=2026-09-10`）。
- 验证：`check_raw_updates.py` 待更新 **0**（已同步 99 / 未映射 23 均为图片素材）；`wiki-linkcheck.py` 对 14 个新增及更新页面检查，**断链 0、歧义 0**。
- 遗留：全库仍有约 70 处 basename 歧义链接（`.raw` 同名导致），建议将 `.raw/` 加入 `.obsidian/app.json` 的 `userIgnoreFilters`；**`scripts/rebuild_wiki_links.py` 实时模式暂不可用**，其内部以 `wiki/` 为 vault 根，会破坏 `[[wiki/...]]` 链接。

## 2026-08-27 - 重建 Wiki 链接索引

- 扫描 `wiki/` 全部 Markdown 页面。
- 刷新主索引、目录索引、页面级自动关联索引。
- 更新 Obsidian 图谱颜色分组、仪表盘和概览 Canvas。
- 生成 `[[元数据/lint-report-2026-08-27|链接健康报告]]`。

## [2026-08-13] 修复 | 关联分析.md 断链归零

- 文件：`wiki/语雀/关联分析.md`
- 问题：17 条 wikilink 写成路径式 `[[语雀/.../X]]`，缺 `wiki/` 前缀；vault 根为项目根，文件实位于 `wiki/` 下，Obsidian 按路径解析失败。
- 核实：17 条断链目标 wiki 页面**全部已存在**（非缺页），`.raw/yuque/` 另有同名源文件。
- 修复：25 处链接补 `wiki/` 前缀改为 `[[wiki/语雀/.../X]]`；`[[学习/_index]]`（无对应页）改指向真实存在的 `[[wiki/语雀/learning/index|学习目录]]`。
- 验证：路径式断链归零。
- 遗留：basename 链接因 `.raw/yuque` 与 `wiki/语雀` 同名存在歧义（全库问题），建议后续全库链接语法扫描。
- 新增工具：`scripts/wiki-linkcheck.py`（图谱 / 断链 / 孤儿页扫描）。

## 2026-07-08 - 重建 Wiki 链接索引

- 扫描 `wiki/` 全部 Markdown 页面。
- 刷新主索引、目录索引、页面级自动关联索引。
- 更新 Obsidian 图谱颜色分组、仪表盘和概览 Canvas。
- 生成 `[[元数据/lint-report-2026-07-08|链接健康报告]]`。

## [2026-07-01] 初始化 | 知识库创建
- 模式：D — 个人知识库
- 创建：完整文件夹结构、核心文件、模板
- 创建页面：概览、索引、日志、热缓存、各领域索引
- 关键洞察：知识库已就绪，等待第一批导入。
- 文件夹中文化：目标、学习、人脉、领域、资源、来源、实体、概念、对比、问答、元数据
