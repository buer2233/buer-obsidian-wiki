---
type: meta
title: "仪表盘"
created: 2026-07-01
updated: 2026-07-01
---

# 知识库仪表盘

## 最近活动
```dataview
TABLE type, status, updated FROM "wiki" SORT updated DESC LIMIT 15
```

## 种子页面（待开发）
```dataview
LIST FROM "wiki" WHERE status = "seed" SORT updated ASC
```

## 目标进度
```dataview
TABLE area, priority, progress, target_date FROM "wiki/目标" SORT progress ASC
```

## 缺少来源的实体
```dataview
LIST FROM "wiki/实体" WHERE !sources OR length(sources) = 0
```
