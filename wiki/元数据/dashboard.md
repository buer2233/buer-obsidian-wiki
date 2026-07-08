---
type: meta
title: "知识库仪表盘"
updated: 2026-07-08
tags:
  - meta/dashboard
status: active
---

# 知识库仪表盘

## 链接健康
- 页面总数：119
- 待处理死链：0
- 无入链页面：0

## 最近活动
```dataview
TABLE type, status, updated FROM "wiki" SORT updated DESC LIMIT 15
```

## 自动索引入口
- [[index|索引]]
- [[语雀/index|语雀索引]]
- [[软件测试学习资料/index|软件测试学习资料索引]]
- [[软件测试学习资料-XMind/index|软件测试学习资料-XMind索引]]
- [[面试题/index|面试题索引]]
- [[个人信息/index|个人信息索引]]

## 待复核页面
```dataview
LIST FROM "wiki" WHERE status = "seed" SORT updated ASC
```
