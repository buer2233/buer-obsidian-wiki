# Claude Code学习笔记

来源：https://www.yuque.com/bbuer/ebdyfe/us64qndpfpgpwo79
抓取时间：2026-07-01

---

**Claude Code官方文档：** https://code.claude.com/docs/zh-CN/overview

**Claude Code泄露源码：** https://github.com/NanmiCoder/cc-haha

---

## 一、CLAUDE.md

Claude Code 的上下文工程是一个分层体系：从静态的 CLAUDE.md，到动态的 MEMORY.md，到按需的 SKILL.md 和 Rules，再到执行层的 Hooks——它们绝大多数最终都作为 user-role context message 注入到对话历史，而不是 system prompt。理解这个分层，才能真正做好上下文工程。

### (一) CLAUDE.md简介

CLAUDE.md 最常见的位置，会放到这两个地方，一个是项目目录下面的 CLAUDE.md，一个是项目目录下面 .claude 文件夹下的 CLAUDE.md，总共包含11种放置位置。

**内容如下：**
- 项目介绍，如：目录介绍，模块介绍，命令介绍
- 开发规范，如：命名规范，代码风格，Git提交规范
- 注意事项，如：特别约束，踩坑文档

### (二) CLAUDE.md的11种位置

**1. 组织级3种**
- /组织级配置目录/CLAUDE.md
- /组织级配置目录/.claude/CLAUDE.md
- /组织级配置目录/.claude/rules/*.md

公司的全局编码标准、安全策略、合规要求等信息，适合写到这里

**2. 用户级2种**
- C:\Users\admin/.claude/CLAUDE.md
- C:\Users\admin/.claude/rules/*.md

个人的代码风格偏好、个人工具快捷方式等信息，适合写到这里

**3. 项目级5种（最常用）**
- /项目目录/CLAUDE.md
- /项目目录/.claude/CLAUDE.md
- /项目目录/.claude/rules/*.md
- /项目目录/module/rules/*.md
- /项目目录/module/sub_module/CLAUDE.md

单个项目的项目架构、编码标准、常用工作流等信息，适合写到这里

**4. 本地级1种**
- /项目目录/module/sub_module/CLAUDE.local.md

个人的沙盒 URL、偏好的测试数据等信息，适合写到这里

**5. 执行顺序（优先级从高到低）**

目录结构是"物理位置的分类"，而执行顺序是"规则生效的优先级"。CLAUDE在加载配置时，会优先应用更具体、更靠近当前文件的规则（如本地、项目），再应用更通用的规则（如用户、组织），这样可以让更具体的规则覆盖更通用的规则，确保最相关的配置生效。

### (三) CLAUDE.md的执行过程

**1. 拼接用户参数的函数：prependUserContext**

很多人会下意识以为 CLAUDE.md 的内容是被 Claude Code 拼到 system prompt 里发给模型的。这个理解其实不准确。

关键源码在 src/utils/api.ts:449，函数名叫 prependUserContext

**2. 总结思考**

CLAUDE.md = Claude Code 应用层的项目上下文；最终落到 API 请求时 = 一条插在最前面的 user-role meta message。

**思考一：** CLAUDE.md的约束力其实没有想象中那么强。它在模型那里只是一段"user message"，并不是系统层指令

**思考二：** 注入文本末尾那句"IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task." 是源码里写死的，相当于明确告诉模型可以判断当前任务和这段上下文是否相关。所以有时候模型会觉得任务和CLAUDE.md关系不大，就忽略掉部分规则，这并不是 AI 不听话，是源码层面就允许它这样做

**思考三：** 如果你希望让 AI 强制遵守某些规则，CLAUDE.md不是最强的通道。可以考虑用 agent 的 system prompt、或者 hooks 这种程序级约束来实现

### (四) 优秀的CLAUDE.md收集

https://github.com/multica-ai/andrej-karpathy-skills

---

## 二、MEMORY.md

MEMORY.md 是 Claude Code Auto Memory（自动记忆）机制的入口文件，用来让 Claude 在不同会话之间保留它"自己学到的项目知识"。它属于典型的上下文工程（Context Engineering）组件，但不是 System Prompt，而是被当作上下文注入给 Claude 使用。

**官方文档：** https://code.claude.com/docs/zh-CN/memory

### (一) MEMORY.md 是什么？

Claude Code 每个会话都会从新的上下文窗口开始，因此它本来不会记得上次调试过什么、项目有什么特殊命令、用户偏好是什么。Auto Memory 用来解决这个问题：Claude 会在工作过程中，把它认为未来有用的信息写入记忆文件，例如构建命令、调试经验、架构笔记、代码风格偏好和工作流习惯。

它不是你手写的项目规范，而是 Claude 根据会话中的修正、偏好和发现自动沉淀出来的内容。

### (二) 它解决的痛点

| 痛点 | MEMORY.md 如何解决 |
|------|-------------------|
| 每次新会话都从零开始 | 会话开始时自动加载记忆，让 Claude 继承项目经验 |
| 重复解释项目规则和偏好 | Claude 可记住"使用 pnpm 而不是 npm"等偏好 |
| 调试经验丢失 | 把曾经踩过的坑、特殊命令、环境问题保存下来 |
| 长期项目上下文断裂 | 让 Claude 在多次会话中逐渐积累项目知识 |
| 人工维护文档成本高 | Claude 自动判断哪些信息值得记住，无需每次手动写文档 |

### (三) 加载规则

MEMORY.md 并不是无限制全部塞进上下文。超过部分不会在启动时加载。Claude 会尽量保持 MEMORY.md 简洁，并把详细内容移动到其他主题文件，例如 debugging.md、patterns.md，这些文件不会启动时加载，而是在需要时由 Claude 通过文件工具按需读取。

这是一种典型的 Progressive Disclosure（渐进式披露）思路。

### (四) 如何使用

**1. 查看和编辑**
在 Claude Code 中使用 `/memory` 可以查看当前会话加载的 CLAUDE.md、CLAUDE.local.md、rules 文件，并提供打开自动记忆文件夹的入口，还可以切换 Auto Memory 开关。

**2. 让 Claude 记住某件事**
你可以直接说"记住：xxx"，Claude 会把这些信息保存到 Auto Memory 中。

**3. 禁用 Auto Memory**
Auto Memory 默认开启。可以通过 /memory 面板关闭，也可以在项目设置(settings.json)中写，或者通过环境变量关闭。

### (五) MEMORY.md、CLAUDE.md、SKILL.md 区别

| 对比项 | MEMORY.md | CLAUDE.md | SKILL.md |
|--------|-----------|-----------|----------|
| 核心定位 | Claude 的自动记忆 | 人类写给 Claude 的项目说明和规则 | 可复用任务技能 |
| 谁写 | Claude 自动写，也可用户要求记住 | 开发者、团队、组织 | 开发者、团队、插件作者 |
| 内容类型 | 学到的经验、偏好、调试发现 | 项目规则、架构、命令、约定 | 某类任务的步骤、流程、工具说明 |
| 加载时机 | 每次会话启动加载前 200 行或 25KB | 每次会话启动加载，通常完整加载 | 相关任务触发时按需加载 |
| 适合放什么 | "上次发现测试需要 Redis" | "项目使用 pnpm，API 在 src/api" | "如何生成 PR 摘要""如何做代码审查" |
| 是否版本控制 | 默认机器本地，不跨机器共享 | 项目级通常提交 Git | 项目级或插件级可提交 Git |
| 是否硬约束 | 否 | 否 | 否 |
| 是否占用上下文 | 是，但有 200 行/25KB 限制 | 是，文件越大越占 token | 触发时才占用主要上下文 |
| 主要风险 | 记住错误信息、过期信息、个人偏好污染 | 文件过长、规则冲突、过度泛化 | 技能描述不准导致误触发或不触发 |

### (六) 总结

CLAUDE.md 是项目说明书，MEMORY.md 是 Claude 的工作笔记，SKILL.md 是任务操作手册。三者都是上下文工程的重要组成部分，但都不是硬安全边界；真正需要强制执行的规则应使用 Hooks、权限配置或 CI/CD。

---

## 三、Skills

### (一) Skills简介

2025年10月16日 Anthropics 最早推出 Skills的概念，并于2025年12月18日正式将Skills定义为AI开放标准。

**Anthropics官方文章：** https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

**Skills的作用：** AI大模型目前并非全能，对特定领域可能不够了解，直接提问可能得到错误答案。通过Skills功能，用户可为AI提供说明文档（如开发流程、规范或经验），补充AI的知识，使其在需要时查阅，从而提高回答的准确性。

### (二) Skills的构成

**1. Skill存放位置**

- **项目级：** 项目目录下的 .claude/skills/xxx，适合放与你这个项目有关的Skills
- **全局级：** C:\Users\admin\.claude\skills，放到这里的Skills所有项目都能用，适合放置一些通用规范和技能

**2. SKILL.md的内容简介**

一个skills必须包括一个 SKILL.md 文件，且其中必须包含两个模块：元数据和指令。元数据必填两项是：name 和 description。name为SKILL名称，description描述SKILL的作用和触发条件。

skill默认情况下只会加载元数据name和description，在需要使用技能时，才会渐进式的按需加载SKILL内的指令。

### (三) Skills触发

**1. 自动触发**
AI会在提问的开始，将skills全局和你当前项目下的skills元数据内容（name，description等）都加载一下。所以你什么都不用管，当AI感觉需要读取某个skills的时候，会自动读取。

**2. 手动触发**
也可以直接通过斜杠指令来手动触发。

**3. 禁止自动触发**
在SKILL的描述后添加：disable-model-invocation: true。这样skills就不会自动被调用了，只能手动触发了。

### (四) Skills中添加参数

**1. $ 初步讲解**

Claude Code 里跟 $ 有关的写法，其实只有两类：

**参数占位符（接受用户输入的东西）：**
- `$ARGUMENTS` — 用户传进来的全部内容
- `$0` `$1` `$2` — 第几个参数（从 0 开始数）
- `$ARGUMENTS[0]` `$ARGUMENTS[1]` — 上面那种的「全名版」
- `$名字` — 给参数起个有意义的名字

**环境变量（运行环境自动提供的信息）：**
- `${CLAUDE_SKILL_DIR}` — 当前 Skill 自己所在的目录
- `${CLAUDE_SESSION_ID}` — 当前会话的编号

**重点：** 第一类是 $XXX，没有花括号。第二类是 ${XXX}，有花括号。这俩是被两套不同的代码处理的，写错花括号就不会替换。

**2. 最基础的 $ARGUMENTS**

$ARGUMENTS = 「用户输入的所有东西」的占位符。你把它放哪里，用户的输入就填到哪里。

$ARGUMENTS 必须全大写。写成 $arguments、$Arguments 一律不认，不会替换。

**3. $ARGUMENTS 自动兜底机制**

如果忘了写 $ARGUMENTS，用户传的参数不会丢。Claude Code 会发现正文里没有占位符，于是自动把参数贴到正文末尾。

**4. 参数切片：$0 / $1 / $2**

把参数想象成一排储物柜，编号从 0 开始：$0 是第 1 个柜子、$1 是第 2 个、$2 是第 3 个……

$0 是简写，它的「全名」是 $ARGUMENTS[0]，两种写法效果完全一样。

**5. 给参数起名字**

第一步：在 SKILL.md 最上面的 frontmatter 里，用 arguments 字段按顺序列出参数名
第二步：正文里就能直接用名字了

**关键认知：** 名字只是「外号」，本质还是按顺序。❌ 误解：以为可以这样写命令 /建任务负责人=张三优先级=高（像填表格那样指定）✅ 真相：还是严格按位置对号入座

**6. ${CLAUDE_SKILL_DIR} 介绍**

${CLAUDE_SKILL_DIR} = 「我这个 Skill 住在哪」。想引用同目录的脚本/模板，用它就对了，别写死路径。

**重点：花括号别忘了！**
- 参数家族（接用户输入的）：$ARGUMENTS、$0、$名字，没有花括号
- 环境家族（运行环境的）：${CLAUDE_SKILL_DIR}、${CLAUDE_SESSION_ID}，必须带花括号

### (五) Skills 和 Plugins 的区别

- Skills本质上就是一个.md的文件再加上其他.md拓展信息和拓展脚本
- Plugin则更全面，里面包括 Skills，hooks，mcp 等信息，可以做更复杂的场景

### (六) Skills 和 MCP 的区别

**官方原文：** https://claude.com/blog/skills-explained

MCP connects Claude to data; Skills teach Claude what to do with that data.

（MCP 适合做获取数据的场景；Skills 更适合做获取数据之后，处理数据的场景）

### (七) Skills的详细执行流程

**1. Skills开始不是全量注入**

很多人会以为 Skills 跟 CLAUDE.md 一样，启动会话时就把所有内容塞进上下文。源码里不是这样。

Skills 分两层：
- **技能清单层：** 只把 name / description 这类摘要给模型看
- **技能正文层：** 只有模型调用 Skill 工具后，完整 SKILL.md 才会进入上下文

**2. Skills 的触发是靠提示词驱动的：AI自我判断**

**3. Skills 的六类加载位置**

源码里 Skills 的来源大概有六类。Skills 最终会进入统一的commands列表。Claude Code 内部没有把 Skills 和 slash commands 完全割裂开。它们最后都被整理成Command对象，只是来源字段不同。

**4. compact 后为什么还能继续遵守已调用 Skill**

Skills 还有一个和 compact 相关的保存机制。当上下文被压缩后，如果已调用 Skill 的正文完全丢失，模型后续就可能忘掉这个 Skill 的规则。所以 Claude Code 会在 compact 后创建一个 invoked_skills attachment。

### (八) Skills 源码里的硬性限制

**1. /skills/目录不支持单个.md文件**

- 正确格式：.claude/skills/my-skill/SKILL.md
- 错误格式：.claude/skills/my-skill.md

**2. Skills有上下文预算**

默认技能清单大概占上下文窗口的 1%。如果上下文窗口是 200k tokens，那么默认字符预算就是 8000 token。如果 Skills 太多，清单会被裁剪。

单个 Skill 的描述也有上限。如果 description + whentouse 超过 250 字符，就会被截断。

**3. MCP Skills 不执行动态 shell 命令**

本地 Skills 可以支持动态 shell 命令，但 MCP Skills 不执行这类动态 shell。这样做是为了安全考虑。

---

## 四、Plugins

Plugin 是一个自包含目录，用来把 Skills、Commands、Agents、Hooks、MCP Servers、LSP Servers、Monitors、Themes 等能力打包起来，然后在个人、项目或团队范围内复用和分发。

**官方文档：** https://code.claude.com/docs/zh-CN/plugins-reference

### (一) Plugins 基础介绍

**1. Plugins 的诞生**

如果说 Skills 是一本"专业领域的说明书"，那 Plugins 就是一整个"工具箱"。

Anthropic 在推出 Skills 之后，发现单纯一个 .md 文件还不够用。有时候用户想要的不只是给 AI 加一段说明，而是希望：
- 使用特定的AI Agent
- 设置生命周期 Hook（在操作前后自动执行某段脚本）
- 接入一个 MCP 服务器（让 AI 能调用外部工具）

于是 Plugins 就诞生了——它把上面这些能力打包到一个目录里，一键安装、一键启用、一键禁用。

**简单理解：** Skills 是一本书，Plugins 是一个图书馆。一个 Plugin 里面可以包含很多 Skills，再加上 commands、agents、hooks、MCP 服务等。

**2. Plugins 解决的核心痛点**

- **痛点一：能力分散** — 你想给团队加一套"前端开发规范+自动格式化命令+Hook自动检查+MCP接入Figma"，要分别配置4个地方
- **痛点二：缺乏分发** — 就算你写好了一套规范，怎么给别人？
- **痛点三：版本管理混乱** — 你改了一个hook脚本，团队里有人在用旧版有人在用新版

**Plugins 让你：**
- 把所有能力打包到一个目录里
- 通过 Marketplace（插件市场）一键安装和卸载
- 自带版本号和作者信息，方便维护和升级
- 支持 user / project / local 三种作用域，灵活控制对谁生效

### (二) Plugins 的构成

**1. Plugin 存放位置**

- **本地缓存目录（全局）：** ~/.claude/plugins/
- **项目级 plugin 目录：** 项目下的 .claude-plugin/ 目录里

**2. plugin.json**

一个 Plugin 必须包含一个 plugin.json 文件，位于插件目录下的 .claude-plugin/plugin.json 路径。

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[SKILL发布L站的说明]] — AI测试主题关联
- [[常用SKILL总结]] — AI测试主题关联
- [[Git SSH Windows路径解析错误规避]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[安卓移动端appium环境搭建流程]] — AI测试主题关联
- [[AI产品测试]] — AI测试主题关联
- [[接口安全测试]] — AI测试主题关联
- [[02_pytest必背学习资料]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
