# 项目长期记忆 — claude-obsidian vault

## Vault 概况
- 根目录：D:\AI\Hermes\claude-obsidian，既是 Obsidian vault，也是 claude-obsidian 插件项目。
- 结构遵循 LLM Wiki 模式：`.raw/`（源文档，只读不可改）+ `wiki/`（生成的笔记）+ `_templates/`。
- CLAUDE.md 约定：每次回复开头必须称用户为"主人"；回答优先简体中文。

## Vault 根目录与链接语法（关键，已实测）
- vault 根 = 项目根（`.obsidian/` 与 `.vault-meta/transport.json` 均在根，`vault_root=/d/AI/Hermes/claude-obsidian`）。
- 因此 `wiki/` 下文件的 vault 路径必须带 `wiki/` 前缀：`[[wiki/语雀/ai-basics/X]]` 才能解析；写成 `[[语雀/ai-basics/X]]`（缺前缀）= 断链。
- `.obsidian/app.json` 的 `userIgnoreFilters` **未排除 `.raw/`**；`.raw/yuque/` 与 `wiki/语雀/` 大量同名 → basename `[[X]]` 有歧义。
- **结论：本库所有链接统一用 `[[wiki/完整路径|别名]]` 形式**，不依赖 basename 唯一性。

## 摄入流程约定（raw → wiki）
- 图片复制到 `_attachments/images/<分类>/`（镜像源目录结构），页面用相对路径 `../../_attachments/images/...` 引用。
- ⚠️ `_attachments/` 被 `.gitignore` 第 117 行排除 → **图片仅本地可见**；源图随 `.raw/` 正常入库。
- 每次摄入需更新：目标目录 `index.md`、`wiki/index.md`、`wiki/hot.md`、`wiki/log.md`、`.raw/.manifest.json`。

## 脚本与托管段落（重要限制）
- `scripts/check_raw_updates.py`：raw↔wiki 同步检查（非 yuque 文件走同路径映射）。`有待更新` 应为 0。
- `scripts/wiki-linkcheck.py`：`scan` 全库 / `file <相对路径>` 单文件。输出末行为「解析成功 N / 断链 N / 歧义 N」。
- ⚠️ **`scripts/rebuild_wiki_links.py` 实时模式不可用**：其 `WIKI='wiki'`、`wiki_target()` 去掉 `wiki/` 前缀、`link_for()` 在 stem 唯一时输出 basename → 会把正确的 `[[wiki/...]]` 改回断链形式。`AUTO-CATALOG` / `AUTO-LINK-INDEX` 托管段因此需手工维护。

## 数据质量
- 2026-08-13 扫描：全库断链 68 / basename 歧义 72（去重）。已修复 `wiki/语雀/关联分析.md`（eb5cc77）。
- 2026-09-10：新增 11 页 + 4 个索引更新，检查结果断链 0、歧义 0。
- 遗留：全库仍约 70 处 basename 歧义。根治方案 = 把 `.raw/` 加入 `.obsidian/app.json` 的 `userIgnoreFilters`。
- `.obsidian/graph.json` 每次提交都带 `scale` 浮点噪声 diff，无实际意义。

## Git 环境
- 远端 origin = git@github.com:buer2233/buer-obsidian-wiki.git，分支 main。
- ⚠️ **推送必须加 `GIT_SSH_COMMAND="ssh"`**：直接 `git push` 会报 `Could not read from remote repository`，但 `ssh -T git@github.com` 认证正常（22/443 均可）。
- 提交排除项（沿用既有规则）：`file/`、`wiki/笔记/image-example-wiki-map-view.png.md`。
- 本机怪象：`refs/remotes/origin/` 引用无法持久化，`git status` 显示 `[gone]`；纯展示性问题，用 `git ls-remote origin main` 核实远端真实状态。
