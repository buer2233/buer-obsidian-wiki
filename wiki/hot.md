---
type: meta
title: "热缓存"
created: 2026-07-01
updated: 2026-09-10
---

# 最近上下文

## 最后更新
2026-09-10 — 摄入 11 份新学习资料（9 份 AI + 2 份测试开发），新建「测试开发相关学习资料」分类目录。

## 关键事实
- 新增分类 `wiki/测试开发相关学习资料/`，含 2 页：`Flask-DRF与Java后端框架对照学习`、`JaCoCo代码覆盖率工具从入门到工程落地`。
- `wiki/AI相关学习资料/` 从 3 页扩充至 12 页，涵盖大模型基础、AI 编码 Agent 调研（OMP/Pi/DSH/五工具对比）、AI 测试与工程范式（Graph Engineering）。
- 25 张源图按 wiki-ingest 约定复制到 `_attachments/images/AI相关学习资料/`，页面用 `../../_attachments/...` 相对路径引用。
- **Pi 架构修正**：`Pi与AI编程Agent对比分析` 由「5 包架构」更正为「9 包架构」（`agent`/`evals`/`coding-agent`/`protocol`/`server`/`ai`/`tui`/`client`/`session-backends/sqlite-node`），并清除全文 `pi-telemetry` 旧包名。
- **链接约定**：因 `.raw/` 未被 `userIgnoreFilters` 排除，导语类同名文件产生 basename 歧义，全库新页与索引统一使用 `[[wiki/完整路径|别名]]` 形式。
- `.raw/.manifest.json` 已登记全部 11 条新源（`Pi与AI编程Agent对比分析.html` 标记为 `updated`），`last_sync` 更新为 2026-09-10。
- 同步检查结果：待更新 **0**，已同步 99，未映射 23（全部为图片素材，属预期）。

## 最近变更
- 新建：`wiki/测试开发相关学习资料/`（3 个文件：2 页面 + index）
- 新建：`wiki/AI相关学习资料/` 下 9 个页面（大模型核心原理、大模型必学基础知识、AI编码Agent五工具对比分析报告、OMP使用手册、OMP的设计经验、Pi的AI设计经验、Pi源码精读顺序清单、测试开发如何使用DSH、Graph Engineering从概念到测试落地）
- 更新：`wiki/AI相关学习资料/index.md`、`wiki/AI相关学习资料/Pi与AI编程Agent对比分析.md`、`wiki/index.md`
- 更新：`.raw/.manifest.json`
- 追加：`_attachments/images/AI相关学习资料/`（25 张图）

## 活跃线程
- 当前任务：新源摄入完成，链接健康检查通过（新增页面断链 0 / 歧义 0）。
- 待办建议：全库仍存约 70 处 basename 歧义链接（`.raw` 同名），可考虑将 `.raw/` 加入 `.obsidian/app.json` 的 `userIgnoreFilters` 从根上消除；另**勿在未改造脚本前运行 `scripts/rebuild_wiki_links.py` 实时模式**，其内部以 `wiki/` 为 vault 根，会把正确的 `[[wiki/...]]` 链接改回缺前缀形式。
