# 方法论模式指南 —— v1.8.0

**状态：** v1.8.0 GA（2026-05-17）
**范围：** 为你的知识库选择一种组织风格，并据此路由新页面。
**起源：** 关闭 2026 年 5 月指南针制品中的优先差距 5。

---

## 摘要

选择一种与你思维方式匹配的模式：

| 你的思维方式 | 选择 |
|---|---|
| 主题聚类 + 通过链接导航 | **LYT** |
| 活跃项目 vs 持续职责 vs 参考资料 | **PARA** |
| 带有唯一 ID 的原子化观点和密集链接 | **Zettelkasten** |
| 不需要方法论 / 想要 v1.7 默认行为 | **通用** |

```bash
bash bin/setup-mode.sh              # 交互式
bash bin/setup-mode.sh --mode lyt   # 非交互式
```

选择之后，`wiki-ingest`、`save` 和 `autoresearch` 会在决定新页面存放位置之前查询模式。现有文件**不会**被移动；模式只影响未来的归档。

---

## 为什么需要方法论模式

2026 年 5 月的指南针制品确定了 5 个优先差距。claude-obsidian v1.7 关闭了其中 4 个（基础层对齐、默认传输、混合检索、多写者安全），并将第 5 个 —— 方法论支持 —— 推迟到 v1.8。

审计 §9 轴评估将方法论支持评为 2026 年 5 月的**平局**：在 Claude+Obsidian 领域中，没有人将其作为一流技能发布。Ideaverse Pro 2.0（$200 付费知识库）发布了 LYT 作为一种固定结构，但它是一个知识库，而非技能集。PARA、Zettelkasten 和模式感知路由完全没有被服务。

v1.8.0 关闭了这个差距。在此版本之后，claude-obsidian 在指南针框架的 **7 个轴中有 5 个排名第一**（复利型 wiki、多写者安全、检索架构、许可证开放性、方法论支持）。其余 2 个轴（GUI 人体工程学、衍生输出）需要更大的版本（GUI 需要 v2.5+，derive 需要 v2.0）。

---

## 四种模式

### 通用（默认）

**理念：** 不强制任何方法论。与 v1.6/v1.7 相同。

**归档约定：**
- `wiki/sources/<slug>.md` —— 导入的源文档
- `wiki/entities/<Name>.md` —— 人物、组织、产品（保留大小写）
- `wiki/concepts/<Name>.md` —— 概念和框架
- `wiki/sessions/<date>-<topic>.md` —— 来自 `/save` 的会话笔记

**适用场景：**
- 你从 v1.7 迁移，想要零行为变化
- 你还没有决定采用哪种方法论
- 你有自己的组织直觉，想要最少的约束

**优点：** 零学习曲线；与 v1.7 的肌肉记忆匹配；灵活。
**缺点：** 没有可依赖的规范；在大型知识库中容易变得杂乱。

---

### LYT（Linking Your Thinking —— Nick Milo）

**理念：** 组织原语是 **MOC**（Map of Content，内容地图）。原子笔记扁平放在一个文件夹下；MOC 将笔记链接成聚类。你通过跟随链接来导航，而不是浏览文件夹。

**归档约定：**
- `wiki/mocs/<topic>-moc.md` —— 某个主题聚类的内容地图
- `wiki/notes/<atomic-note>.md` —— 所有原子笔记扁平存放（无子文件夹）
- 每个原子笔记的 frontmatter `mocs:` 字段中至少有一个 MOC
- 新导入的内容存放在 `wiki/notes/`；消费技能同时更新相关的 MOC

**模板**（位于全局插件 `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/wiki-mode/templates/lyt/`）：
- `moc-template.md` —— MOC 脚手架，包含核心笔记 / 相邻 MOC / 开放问题部分
- `atomic-template.md` —— 带有 MOC 反向链接的原子笔记

**适用场景：**
- 中大型知识库（>100 条笔记）
- 你以概念聚类和知识图谱的方式思考
- 你是 LYT 实践者或想成为 LYT 实践者

**优点：** 扩展性出色；导航随知识库增长而丰富；知识结构显式化。
**缺点：** 需要始终更新 MOC 的纪律；扁平笔记文件夹在没有好的搜索工具时可能显得混乱。

---

### PARA（Tiago Forte）

**理念：** 按**可操作性**而非主题组织。活跃工作放在项目中（有截止日期 + 成果），持续职责放在领域中（无截止日期），参考资料放在资源中（按主题），已完成/不活跃的工作放在归档中。

**归档约定：**
- `wiki/projects/<project-name>/<note>.md` —— 活跃项目
- `wiki/projects/inbox/<note>.md` —— 新导入 + 会话笔记存放在此处等待分类
- `wiki/areas/<area-name>/<note>.md` —— 持续职责
- `wiki/resources/<topic>/<note>.md` —— 参考资料
- `wiki/resources/incoming/<note>.md` —— 新源文件存放在此处等待主题分类
- `wiki/resources/people/<Name>.md` —— 实体页面
- `wiki/resources/concepts/<Name>.md` —— 概念页面
- `wiki/archives/<year>/<note>.md` —— 已完成的项目、已终止的领域

**模板**（位于全局插件 `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/wiki-mode/templates/para/`）：
- `project-template.md` —— 项目模板，包含状态 / 截止日期 / 成果 / 下一步行动
- `area-template.md` —— 领域模板，包含范围 / 标准 / 审查频率
- `resource-template.md` —— 参考资料模板，包含主题 + 来源

**适用场景：**
- 工作流密集型用户
- 管理多个项目的知识工作者
- GTD（Getting Things Done）相关实践者
- 读过 Tiago Forte 的《Building a Second Brain》的人

**优点：** 明确的项目生命周期；活跃与参考资料的清晰分离；符合知识工作者的实际运作方式。
**缺点：** 需要定期审查以将已完成的项目移至归档；"incoming" 容器需要被处理。

---

### Zettelkasten（Niklas Luhmann 的卡片盒）

**理念：** 原子笔记、唯一 ID、密集的双向链接。无文件夹。每条笔记恰好回答一个想法。笔记通过 ID 引用相互找到。

**归档约定：**
- `wiki/<YYYYMMDDHHMMSSffffff>-<slug>.md` —— 扁平放在 wiki/ 下，带时间戳的 ID（20 位数字 = 日期 + 微秒，抗冲突）
- 每条笔记的 frontmatter 中有 `id:`、`parent_id:`（可选）、`child_ids:`（可选）
- 无子目录；wiki/ 根目录就是整个知识库
- 所有组织都通过笔记正文中的 `parent_id` / `child_ids` / `[[ID]]` 引用实现

**模板**（位于全局插件 `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/wiki-mode/templates/zettel/`）：
- `atomic-template.md` —— 原子化观点，包含父/子 ID + 推理 + 来源

**适用场景：**
- 学者和研究人员
- 构建永久知识资产的长期思考者
- 读过 Sönke Ahrens 的《How to Take Smart Notes》的人
- 高纪律性、偏好小范围归档的人

**优点：** 最大的链接密度；鼓励原子化思维；经得起数十年的考验。
**缺点：** 学习曲线最陡峭；扁平文件列表在没有好的搜索工具时令人望而生畏；基于 ID 的引用不如基于名称的引用好记。

---

## 模式如何与其他技能交互

集成是**自动的** —— 一旦你设置了模式，`wiki-ingest`、`save` 和 `autoresearch` 在每个新页面上都会查询它。你永远不需要考虑这个问题。

| 技能 | 功能 | 模式如何影响 |
|---|---|---|
| `wiki-ingest` | 归档新源文件/实体/概念页面 | 路由器根据模式决定目标文件夹 |
| `save` | 归档当前对话的会话笔记 | 路由器决定 `wiki/sessions/`（通用）、`wiki/notes/` + MOC 更新（LYT）、`wiki/projects/inbox/`（PARA）或 `wiki/<ID>-session-...`（Zettel） |
| `autoresearch` | 归档研究循环后的综合页面 | 路由器决定 `wiki/concepts/`（通用）、`wiki/notes/` + 主题 MOC（LYT）、`wiki/resources/<topic>/`（PARA）或 `wiki/<ID>-...`（Zettel） |

路由器（`scripts/wiki-mode.py route <type> "<name>"`）是唯一的真相来源。技能不自行计算路径；它们调用路由器并使用返回的结果。

---

## 之后切换模式

切换模式是**安全的，但不会自动迁移**：

1. 运行 `bash bin/setup-mode.sh`（或非交互式地使用 `--mode <new-mode>`）
2. 新模式被写入 `.vault-meta/mode.json`
3. 现有文件保留在原始位置并继续正常工作
4. 新文件按新模式归档
5. （可选手动步骤）使用文件管理器或 `git mv` 将现有文件迁移到新结构

**为什么不自动迁移：** 知识库包含你的思维。自动重写路径可能会破坏 wikilinks、丢失数据或给你带来意外。手动迁移强制你对哪些内容适合新方法论、哪些内容留在当前位置做出明确决定。

**LYT 迁移的具体建议：** 切换到 LYT 后，运行 `lint the wiki`（技能：wiki-lint）来识别那些可以从 MOC 包含中受益的孤立页面。

---

## 模式配置文件

`.vault-meta/mode.json` 是活跃模式声明。它**默认被 gitignore** —— 该文件被视为特定于主机的运行时配置。要在多台机器/协作者之间提交你的模式选择：

```bash
git add -f .vault-meta/mode.json
git commit -m "chore: declare vault mode as <mode>"
```

文件结构：

```json
{
  "schema_version": 1,
  "mode": "lyt|para|zettelkasten|generic",
  "configured_at": "2026-05-17T00:00:00Z",
  "config": {
    "lyt": {"moc_folder": "wiki/mocs/", "notes_folder": "wiki/notes/"},
    "para": {"projects_folder": "...", "areas_folder": "...", "resources_folder": "...", "archives_folder": "..."},
    "zettelkasten": {"id_format": "YYYYMMDDHHMMSSffffff", "no_folders": true, "root_folder": "wiki/"},
    "generic": {"sources_folder": "wiki/sources/", "entities_folder": "wiki/entities/", "concepts_folder": "wiki/concepts/", "sessions_folder": "wiki/sessions/"}
  }
}
```

`config` 块始终包含全部 4 种模式。活跃模式由 `mode` 指定。每种模式的文件夹路径可以在你的 `mode.json` 中被覆盖，如果你想要非默认的约定。

---

## 何时不使用模式感知

- **小型知识库**（<20 条笔记）：组织的开销尚不值得。坚持使用通用模式。
- **你未选择组织的知识库**：如果你不在乎方法论，就不要选。通用模式是诚实的。
- **跨项目共享知识库**（按全局 CLAUDE.md `/save` 约定）：位于 `~/Documents/Obsidian Vault/` 的个人知识库有自己的组织选择；项目的模式路由器只适用于项目自己的 `wiki/`。

---

## 后续路线图

v1.8.0 关闭了优先差距 5。指南针制品的全貌：

| 轴（按审计 §9） | v1.7.2 状态 | v1.8.0 状态 | 达到领先的路径 |
|---|---|---|---|
| 复利型 wiki 原语 | #1 | #1 | ✓ |
| 多写者安全 | #1 | #1 | ✓ |
| 检索架构（免费套餐） | #1 | #1 | ✓ |
| 许可证/开放性 | #1 | #1 | ✓ |
| **方法论支持** | 平局 | **#1** ← v1.8.0 关闭 | ✓ |
| 衍生输出（音频/视频/测验） | 无 | 无 | v2.0（wiki-derive） |
| GUI/安装人体工程学 | 无 | 无 | v2.5+（社区插件 fork） |

v1.8.0 之后：**按指南针框架 7 个轴中有 5 个排名第一**。其余 2 个轴需要多个版本的努力：
- **v1.9** —— 多模态导入（YouTube / PDF / EPUB / 图片 OCR）
- **v2.0** —— `wiki-derive` 技能：音频概览、测验生成、学习指南、思维导图综合（与 NotebookLM 对齐）
- **v2.5+** —— 社区插件 GUI 外壳（覆盖主流 Obsidian 用户）

---

## 交叉引用

- `~/.claude/plugins/marketplaces/AgriciDaniel-claude-obsidian/skills/wiki-mode/SKILL.md`（全局插件）—— 技能本身
- [`scripts/wiki-mode.py`](../scripts/wiki-mode.py) —— 路由器 + 配置辅助工具
- [`bin/setup-mode.sh`](../bin/setup-mode.sh) —— 交互式设置
- [`tests/test_wiki_mode.py`](../tests/test_wiki_mode.py) —— 独立测试套件（15 个断言）
- [`docs/compound-vault-guide.md`](compound-vault-guide.md) —— v1.7 综合指南，v1.8 在其基础上构建
- v1.7.0 审计 §9 轴 6：[`docs/audits/v1.7.0-audit-2026-05-17.md`](audits/v1.7.0-audit-2026-05-17.md)
