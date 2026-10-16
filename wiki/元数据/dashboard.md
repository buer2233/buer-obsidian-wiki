---
type: meta
title: "知识库仪表盘"
updated: 2026-10-16
tags:
  - meta/dashboard
status: active
---

# 知识库仪表盘

## 链接健康
- 页面总数：153（2026-10-15 新增 10 页；2026-10-16 新增 1 页 `wiki/来源/claude-obsidian生态调研`）
- 待处理死链：77（**均为既有**，集中在 `wiki/index.md` 等历史页面里"无 `wiki/` 前缀"的旧写法；两次变更均经 `git HEAD` 差集核验，新引入 **0**）
- 无入链页面：0（新增页均已挂入主索引或分类索引）
- 注：本工具按 vault 根解析 `[[a/b]]`，而 Obsidian 按 vault 内路径解析——**无前缀的旧链接会被本工具误报**；脚本亦不剥离代码块/表格。**看明细不看总数**

## raw 覆盖面（2026-10-16 起可证明）
- `check_raw_updates.py`：**未映射 0 / 待更新 0 / 退出码 0** —— `.raw/` 173 个文件全部有可见归属
- 分桶：已同步正文页 109 ｜ 图片素材 61（归属=嵌入它们的页面）｜ 已排除 3（`.gitkeep` / `.manifest.json` / `*.stackdump`，**均附原因，非静默跳过**）
- **退出码语义**：非零 = 有内容未入账 → 可直接用作工作流门禁

## 最近活动
```dataview
TABLE type, status, updated FROM "wiki" SORT updated DESC LIMIT 15
```

## 自动索引入口
- [[wiki/index|索引]]
- [[wiki/概念/_index|概念索引]]
- [[wiki/来源/_index|来源索引]]
- [[wiki/对比/_index|对比索引]]
- [[wiki/实体/_index|实体索引]]
- [[wiki/问答/_index|问答索引]]
- [[wiki/语雀/index|语雀索引]]
- [[wiki/软件测试学习资料/index|软件测试学习资料索引]]
- [[wiki/软件测试学习资料-XMind/index|软件测试学习资料-XMind索引]]
- [[wiki/面试题/index|面试题索引]]
- [[wiki/个人信息/index|个人信息索引]]

注：① 概念/来源/对比/实体/问答 五行此前缺失（`wiki/概念/` 目录 2026-09-23 才建立）；② 本清单原写法缺 `wiki/` 前缀（vault 根为项目根，文件在 `wiki/` 下），会导致解析失败，2026-09-23 统一补全前缀。

## 待复核页面
```dataview
LIST FROM "wiki" WHERE status = "seed" SORT updated ASC
```
