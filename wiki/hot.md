---
type: meta
title: "热缓存"
created: 2026-07-01
updated: 2026-10-15
---

# 最近上下文

## 最后更新
2026-10-15 — Wiki 检查后补齐 **8 份 AI 学习资料 + 1 个新分类「学习简图」**，并修复 `check_raw_updates.py` 使其**未映射归零**。

## 关键事实
- **规模**：`wiki/` 152 md（+10）、`.raw/` 178 文件、`_attachments/` 61 文件（+39）。
- **新建分类 `wiki/学习简图/`**：「一图流」速查页——把 `.raw/学习简图/` 的思维导图翻译成**可检索结构**（内嵌原图 + 文字速查表）。首篇：[[wiki/学习简图/数据结构总览|数据结构总览（速查图）]]（12 种数据结构 12 宫格）。
- **`wiki/AI相关学习资料/` 由 13 → 20 页**，新增 4 个分组：AI 应用工程（RAG / Ontology）、AI 测试工具（Jev / REA）、工程效能与基础设施。
- **`check_raw_updates.py` 现在可用且可信**：修后 `未映射 0 / 待更新 0`。三处修复——① GBK 控制台 emoji 崩溃；② 新增规则 4b「同分类按文件名回退匹配」（消除 raw 子目录被拍平的假阳性）；③ **图片改判为「被 wiki 页引用即已收录」**（同时能抓出"复制了却无人引用"的孤儿附件）。
- **`scripts/rebuild_wiki_links.py` 仍不可整体运行（重要）**：其 `wiki_target()` 生成**不带 `wiki/` 前缀**的链接，且会**整体覆盖本文件 `hot.md`**。需要重排目录时，只能用 `import` 方式单独调用其函数（本次已用 `update_root_index(dry_run=True)` 做差异预览），**绝不整跑**。
- **vault 与工作区不同目录**：vault 根为 `D:\AI\Hermes\claude-obsidian`；`D:\AI\Hermes\learn` 只是工作区，其下**没有** `wiki/`。脚本批量处理 wiki 时须显式进入 vault 目录。
- **`obsidian_simple_search` 全库搜索会超限**：改用 `obsidian_list_files_in_dir` + `obsidian_get_file_contents` 定向读取。

## 最近变更
- 新建：`wiki/AI相关学习资料/` 8 页 —— `RAG的流程与应用`、`REA逆向工程MCP工具学习手册`、`Ontology本体工程从概念到企业流程与测试流程落地`、`Anthropic源代码控制系统重设计`、`AI工具资源占用沟通与面试应答`、`Jev决策模型(System One)学习参考资料`、`Jev用于UI自动化测试可行性分析与AI测试工具横向对比`、`TypeSafe_Jev国内使用指南(官网导航+四条接入路径+实测连通性)`
- 新建：`wiki/学习简图/`（`数据结构总览.md`、`_index.md`）
- 新建素材：`_attachments/images/AI相关学习资料/{RAG的流程与应用,REA逆向工程MCP工具学习手册,Ontology本体工程,Anthropic源代码控制系统重设计}/`（38 张）＋ `_attachments/images/学习简图/`（1 张）
- 改动：`wiki/AI相关学习资料/大模型核心原理.md`（§3.3 接入 2 张 Transformer 原论文 Figure 2 配图）、`wiki/语雀/数据结构、算法、设计模式/数据结构.md`（回链速查图）
- 更新：`wiki/index.md`、`wiki/AI相关学习资料/index.md`、`wiki/log.md`、`wiki/hot.md`、`.raw/.manifest.json`（9 条新源，`last_sync=2026-10-15`）
- 修复：`scripts/check_raw_updates.py`（3 处，见上）

## 归档实践要点（下次 ingest 直接照做）
- **`.raw/` 引用绝不用 wikilink**：触发 git pathspec 歧义。全库约定是 frontmatter **纯字符串** `source: ".raw/..."`。
- **图片路径必须改写成相对路径**：源文件里是 `![alt](images/<folder>/<file>)`，wiki 页里要写成 `![alt](../../_attachments/images/AI相关学习资料/<folder>/<file>)`；先把图复制到 `_attachments/images/<分类>/<子目录>/`。
- **子代理只写自己那一篇页**：索引 / `log` / `hot` / `manifest` 由主控统一收口，避免并发写坏。本次 7 个并行代理全部遵守，产出 328/349/350/352/343/385/327 行。
- **`wiki-linkcheck.py file` 必须传含 `wiki/` 前缀的完整路径**，否则假报。
- **有断链标注 ≠ 真有断链**：脚本不剥离代码块与表格，必须看明细确认。
- **检查脚本的输出是「候选集」不是「结论」**：本次 74 项未映射里只有 8 项（11%）需要处理。批量建页前必须人工分类。

## 活跃线程
- 当前任务：Wiki 检查 + 未收录文件补齐，已完成；索引、子索引、hot、log、manifest 全部同步。
- **待主人决策的三项遗留**：
  1. `.raw/AI相关学习资料/pi/` 下 5 个文件与根目录**逐字节相同**（冗余副本）——本次**未删除**，仅记录。
  2. `wiki/实体/`、`wiki/概念/` 未随本轮扩充——7 个代理共产出约 30 个候选实体/概念页（如 Jev、browser-use、Scion、FAISS、HNSW、TBox/ABox、changeset…），本次**未新建**任何实体/概念页，待确认是否值得建。
  3. `scripts/rebuild_wiki_links.py` 需重写 `wiki_target()`（补 `wiki/` 前缀）并给 `update_hot()` 加保护，才能恢复可用。
- 已知长期问题：全库仍有约 70 处 basename 歧义链接（`.raw` 同名导致），建议将 `.raw/` 加入 `.obsidian/app.json` 的 `userIgnoreFilters`。