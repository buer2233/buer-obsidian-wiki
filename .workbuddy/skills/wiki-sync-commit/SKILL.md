---
name: wiki-sync-commit
description: 将 .raw/ 中新增或修改的源文件摄入 claude-obsidian vault 的 wiki/ 目录，维护索引与清单，验证链接健康后提交并推送 git。当用户说「更新Wiki」「同步知识库」「把新文件加入wiki」「提交并push」时使用。
agent_created: true
---

# Wiki 同步与提交（claude-obsidian vault 专用）

## 适用场景

用户要求「更新 Wiki」「把新增文件加入 wiki」「同步知识库并提交 push」时执行。目标是完成
**raw → wiki 摄入 → 索引维护 → 链接验证 → commit/push** 全链路。

## 前置必读（不可跳过）

1. 读取上一轮的工作记忆（`.workbuddy/memory/` 最新日期文件 + `MEMORY.md`），确认既有约定。
2. **链接语法铁律**：本 vault 的 vault 根 = 项目根，`wiki/` 下文件的链接**必须**写成
   `[[wiki/完整路径|别名]]`。写 basename（`[[X]]`）因 `.raw/` 存在同名文件会产生歧义。
3. **绝不运行 `scripts/rebuild_wiki_links.py` 实时模式**：其内部以 `wiki/` 为 vault 根，
   会把正确的 `[[wiki/...]]` 链接改写为缺前缀的断链形式。`AUTO-CATALOG` /
   `AUTO-LINK-INDEX` 托管段一律**手工维护**。

## 执行步骤

### 1. 确定待摄入源文件

```bash
"C:/Users/admin/.workbuddy/binaries/python/versions/3.13.12/python.exe" scripts/check_raw_updates.py
```

- `■ 待更新文件` = 已映射但 raw 比 wiki 新（需重新摄入）
- `■ 未映射到 wiki` = 新文件（图片素材也会出现在此，属正常）
- 完整列出新文件：`find .raw -type f -newermt "<上次同步日期>"`

### 2. 通读源文件

用 Read 逐个读取新源（HTML 源需用 grep/sed 提取正文）。归纳出主题分组，
决定落到哪个 `wiki/<分类>/` 目录，或是否新建分类目录。

### 3. 处理图片

- 将源图复制到 `_attachments/images/<分类>/`，**镜像源目录结构**。
- 页面中用相对路径引用：`../../_attachments/images/<分类>/<子目录>/<文件名>`。
- 注意：`_attachments/` 被 `.gitignore` 排除，图片**仅本地可见**；源图随 `.raw/` 入库。

### 4. 生成 wiki 页面

frontmatter 模板：

```yaml
---
type: note | comparison | reference | index
title: "页面标题"
source: ".raw/<分类>/<源文件名>"
created: YYYY-MM-DD
tags: [...]
related:
  - "[[wiki/<分类>/<相关页>]]"
---
```

正文要求：保留源文档的关键表格 / mermaid 代码块 / 代码示例；文末固定两段
`## 关联文档`（`[[wiki/...]]` 链接）与 `## 源文件`（`.raw/...` 路径）。

### 5. 维护索引与清单

- 目标目录 `index.md`：更新 `📄 页面索引`、`🔗 关联文档`、`源文件`、`AUTO-CATALOG`（手工）
- `wiki/index.md`：新增/扩充分类章节 + 对应 `AUTO-CATALOG` 子段（手工）
- `wiki/hot.md`：重写「最后更新 / 关键事实 / 最近变更 / 活跃线程」
- `wiki/log.md`：**在 `# 知识库日志` 标题之后、最旧条目之前插入**新条目（新→旧排列）
- `.raw/.manifest.json`：为每个新源添加 `{ingested, status: "created", wiki_path}`；
  修改过的源置 `status: "updated"`；同步更新顶层 `last_sync`

### 6. 验证（必做）

```bash
# 同步性：待更新应为 0
"C:/Users/admin/.workbuddy/binaries/python/versions/3.13.12/python.exe" scripts/check_raw_updates.py

# 逐文件链接检查，末行应为「断链 0 / 歧义 0」
for f in "<新增/更新页面相对路径>"; do
  "C:/Users/admin/.workbuddy/binaries/python/versions/3.13.12/python.exe" scripts/wiki-linkcheck.py file "wiki/$f" 2>&1 | tail -1
done
```

同时 `grep -rn "pi-telemetry\|<旧术语>" wiki/` 确认无过时表述残留。

### 7. 提交与推送

```bash
git add -A -- . ':!file' ':!wiki/笔记/image-example-wiki-map-view.png.md'
git commit -F - <<'EOF'
feat: <中文一句话概述>

<分条列出新增/修正/验证结果>
EOF
GIT_SSH_COMMAND="ssh" git push origin main
GIT_SSH_COMMAND="ssh" git ls-remote origin main   # 核实远端
```

**关键坑**：直接 `git push` 会报 `Could not read from remote repository`，
但 `ssh -T git@github.com` 认证正常 —— **必须加 `GIT_SSH_COMMAND="ssh"`**。

固定排除项：`file/`、`wiki/笔记/image-example-wiki-map-view.png.md`。

### 8. 收尾

- 追加 `.workbuddy/memory/YYYY-MM-DD.md`（append-only 工作日志）
- 有长期价值的约定写入 `.workbuddy/memory/MEMORY.md`（原地更新）

## 常见问题

| 现象 | 原因 | 处理 |
|------|------|------|
| 新增页面大量「断链」 | 链接写成 basename 缺 `wiki/` 前缀 | 补 `wiki/` 前缀 |
| 链接「歧义」 | `.raw/` 与 `wiki/` 存在同名文件 | 改为 `[[wiki/完整路径\|别名]]` |
| push 报 Could not read from remote | git 调用的 ssh 未生效 | 加 `GIT_SSH_COMMAND="ssh"` |
| `wiki/log.md` 内容顺序错乱 | 历史脚本把 frontmatter 追加到了文件中部 | 一次性修正：frontmatter 置顶 + 新条目紧接标题 |
