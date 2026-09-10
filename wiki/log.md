---
type: meta
title: "知识库日志"
created: 2026-07-01
updated: 2026-09-10
---

# 知识库日志

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
