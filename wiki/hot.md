---
type: meta
title: "热缓存"
created: 2026-07-01
updated: 2026-10-16
---

# 最近上下文

## 最后更新
2026-10-16 — `.raw/` 去重、覆盖面补齐到 **100%**，并修掉**两个长期静默失效**的根因（检查器静默排除 + Windows 上 `wiki-lock` 整体失效）。

## 关键事实
- **规模**：`wiki/` 153 md、`.raw/` 173 文件（−5 重复副本）、`_attachments/` 61 文件。
- **`check_raw_updates.py` 现在"无可藏"**：无静默排除，每个扫描到的文件都落进可见分桶（待更新 / 已同步 / 图片素材 / 未映射 / **已排除并附原因**）；**退出码非零 = 有内容未入账**。当前 `未映射 0`、退出码 `0` —— **覆盖率可证明为 100%**。
- **`wiki-lock.sh` 在 Windows 上已可用**：根因是元锁依赖 Linux 专有的 `flock`（Git Bash 不带）→ 所有命令 rc=1 → PostToolUse 自动提交钩子判为"锁状态未知"→ **永远推迟提交**。已加 `mkdir` 原子互斥回退（保留 Linux flock 路径）。
- **`.raw/` 目录结构**：`.raw/AI相关学习资料/` 下按项目分子目录（`pi/`、`jev/`），**根目录不再保留同名副本**。检查器规则 4b 会按文件名回退匹配，故子目录内容仍能对上 `wiki/AI相关学习资料/` 的扁平页面。
- **`scripts/rebuild_wiki_links.py` 仍不可整跑**：其 `wiki_target()` 生成不带 `wiki/` 前缀的链接，且会整体覆盖本文件。需重排目录时只能 `import` 后单独调函数并先 `dry_run=True` 看差异，**绝不整跑**。
- **vault 与工作区不同目录**：vault 根为 `D:\AI\Hermes\claude-obsidian`；`D:\AI\Hermes\learn` 只是工作区。
- **`obsidian_simple_search` 全库搜索会超限**：改用目录列举 + 定向读取。

## 最近变更
- 删除：`.raw/AI相关学习资料/` 根目录 5 个与 `pi/` **逐字节相同**的副本（md5 核验；均在 git 历史中可恢复）
- 新建：`wiki/来源/claude-obsidian生态调研.md` —— 此前被检查器**静默排除**、唯一真正漏收录的 raw 文件
- 修复：`scripts/check_raw_updates.py`（静默排除 → 显式分桶；退出码语义；`FILENAME_MAP` 支持根目录级 raw 文件）
- 修复：`scripts/wiki-lock.sh`（`flock` 缺失时回退 `mkdir` 原子互斥）
- 改向引用：5 篇 wiki 页的 `source:`/`sources:`、`wiki/AI相关学习资料/index.md`、`.raw/.manifest.json` 指向 `pi/`
- 更新：`wiki/index.md`、`wiki/来源/_index.md`、`wiki/log.md`、`wiki/hot.md`、`wiki/元数据/dashboard.md`

## 归档实践要点（下次 ingest 直接照做）
- **先跑检查器，再动手**：`python scripts/check_raw_updates.py`；**退出码非零就是有内容没入账**。「未映射」才是待办，「图片素材」是正常归属。
- **检查脚本的输出是「候选集」不是「结论」**：批量建页前必须人工分类（上一次 74 项里只有 8 项真需处理）。
- **`.raw/` 引用绝不用 wikilink**：触发 git pathspec 歧义。全库约定是 frontmatter **纯字符串** `source: ".raw/..."`。
- **图片路径必须改写成相对路径**：`![alt](../../_attachments/images/<分类>/<子目录>/<file>)`；先把图复制到 `_attachments/images/<分类>/`。`_attachments/` 被 gitignore，图片**仅本地可见**。
- **子代理只写自己那一篇页**：索引 / `log` / `hot` / `manifest` 由主控统一收口。
- **`wiki-linkcheck.py file` 必须传含 `wiki/` 前缀的完整路径**；有断链标注 ≠ 真有断链（脚本不剥离代码块与表格），必须看明细。
- **删除任何文件前先做哈希核验**，确认删除的是副本而非内容。

## 活跃线程
- 当前任务：三条指令（去重 / 全覆盖 / 根因修复）均已完成并验证。
- **待主人决策**：
  1. **提交**：会话期间用 `.vault-meta/auto-commit.disabled` 按住了自动提交（主人未要求提交）。该开关**已在收尾时撤销**，即自动提交已恢复；若想用精选消息提交本轮成果，请走 `wiki-sync-commit` 技能。
  2. **`wiki/实体/`、`wiki/概念/` 仍未扩充**：两次 ingest 共产出约 30 个候选实体/概念页（Jev、browser-use、Scion、FAISS、HNSW、TBox/ABox、changeset…），均未新建。
  3. **`scripts/rebuild_wiki_links.py`** 仍需重写 `wiki_target()`（补 `wiki/` 前缀）并给 `update_hot()` 加保护才能恢复可用（主人自建技能已明令"绝不整跑"）。
- 已知长期问题：全库仍有约 70 处 basename 歧义链接（`.raw` 同名导致），建议将 `.raw/` 加入 `.obsidian/app.json` 的 `userIgnoreFilters`。