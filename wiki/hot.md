---
type: meta
title: "热缓存"
created: 2026-07-01
updated: 2026-08-13
---

# 最近上下文

## 最后更新
2026-08-13 — 修复 `wiki/语雀/关联分析.md` 的 17 条断链，新增链接健康检查脚本。

## 关键事实
- vault 根目录 = 项目根（`.obsidian/` 与 `transport.json` 均在根）；`wiki/` 下文件的 vault 路径必须带 `wiki/` 前缀。
- `.raw/yuque/` 与 `wiki/语雀/` 存在大量同名文件 → basename 链接有歧义；路径式链接须带 `wiki/` 前缀才能精确解析。
- 关联分析.md 原 17 条断链实为链接语法错误（缺 `wiki/` 前缀），目标页均已存在，非缺页。

## 最近变更
- 修复：[[wiki/语雀/关联分析|关联分析]] — 25 处 wikilink 补 `wiki/` 前缀，路径式断链归零。
- 新增：`scripts/wiki-linkcheck.py` — wikilink 图谱扫描 / 断链 / 孤儿页检测工具。

## 活跃线程
- 当前任务：Obsidian 关系图谱查询与链接健康维护。
- 后续建议：① 全库 basename 歧义扫描（`.raw` 同名）；② 修正 `wiki/index.md` 等同样缺 `wiki/` 前缀的路径式链接。
