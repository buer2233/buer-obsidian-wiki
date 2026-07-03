# 常用SKILL总结

来源：https://www.yuque.com/bbuer/ebdyfe/aevmm7hpiieq03td
抓取时间：2026-07-01

---

## 1. 全局统筹执行类

| SKILL | 项目定位 | 使用场景 |
|-------|---------|---------|
| using-superpowers | 会话入口技能 | 每次开始任务时用于识别是否有适用技能 |
| planning-with-files | 文件化计划与进度管理 | 复杂任务、多步骤开发、需要维护 task_plan.md、findings.md、progress.md 时 |
| test-driven-development | 全项目 TDD 流程 | 新功能、Bugfix、阶段开发 |
| brainstorming | 需求和方案澄清 | 新阶段、大改动、跨模块设计、需求不明确时 |
| systematic-debugging | 根因定位 | 测试失败、构建失败、Jenkins/DRF/Vue 联调异常 |
| receiving-code-review | 处理评审意见 | 用户给出代码审查意见、需要判断建议是否合理时 |
| subagent-driven-development | 独立任务并行执行 | 大型实现计划中存在可拆分并行任务时 |

**推荐组合：**

| 场景 | 推荐组合 |
|------|---------|
| 普通阶段开发 | using-superpowers + planning-with-files + test-driven-development |
| 新阶段方案设计 | using-superpowers + planning-with-files + brainstorming |
| 问题排查 | systematic-debugging + 对应模块技能 |
| 处理评审反馈 | receiving-code-review + 对应模块技能 |

---

## 2. 后端开发类（DRF）

| SKILL | 项目定位 | 使用场景 | 备注 |
|-------|---------|---------|------|
| django-tdd | Django/DRF 后端主技能 | 账户、权限、测试任务、失败用例、Jenkins API 开发 | 与 pytest-django、DRF 测试匹配 |
| api-design | REST API 设计 | URL、状态码、分页、过滤、错误响应、版本边界设计 | 适合后端 API |
| python-patterns | Python 代码质量 | 服务层、工具函数、类型标注、异常处理、可维护性优化 | 用于实现和重构 |
| python-testing | pytest 测试策略 | fixture、mock、参数化、fake HTTP 响应、覆盖率补强 | 后端测试和 api-test 测试都可使用 |
| systematic-debugging | 后端问题排查 | Django 配置、MySQL、迁移、DRF 认证、Jenkins fake client 异常 | 建议补充到后端场景使用 |

**推荐组合：**

| 场景 | 推荐组合 |
|------|---------|
| 新增 DRF API | django-tdd + api-design + python-testing |
| 后端实现和重构 | django-tdd + python-patterns |
| Jenkins 集成 API | api-design + python-testing + systematic-debugging |
| MySQL、迁移或测试失败 | systematic-debugging + django-tdd |

---

## 3. 前端开发类（Vue 3）

使用如下技术栈的Vue3项目：Vue 3、Vite、TypeScript、Vue Router、Pinia、Axios、Element Plus、Vitest 和 Vue Test Utils，应优先使用 Vue 官方相关技能。

| SKILL | 项目定位 | 使用场景 | 备注 |
|-------|---------|---------|------|
| vue-best-practices | Vue 3 主技能 | 任意 .vue、Vue Router、Pinia、Vite with Vue 工作 | 前端目录标记为必须执行 |
| frontend-design | 前端界面设计与实现 | 页面、组件、布局、交互和视觉质量优化 | 前端目录标记为必须执行 |
| vue-pinia-best-practices | Pinia 状态管理 | 登录态、筛选条件、失败用例选择、任务状态 | 适合 src/stores/ 和复杂页面状态 |
| vue-router-best-practices | Vue Router 4 | 登录守卫、平台路由、报告跳转、参数路由 | 适合 src/router/ 和页面生命周期问题 |
| vue-testing-best-practices | Vue 测试 | Vitest、Vue Test Utils、组件测试、mock、异步渲染 | 适合 front-end/tests/ |
| vue-debug-guides | Vue 调试 | 响应式、computed、watch、template、Teleport、异步问题 | 遇到前端异常时使用 |
| create-adaptable-composable | 可复用组合式函数 | 创建 useXxx composable，且入参需要支持普通值、ref、getter 时 | 按场景使用，不作为默认技能 |
| ui-ux-pro-max | UI/UX 质量检查 | 可访问性、表格、弹窗、表单、响应式、数据展示体验评审 | 可选，用于界面质量提升 |
| ckm:design-system | 设计系统和令牌 | CSS 变量、组件状态、设计令牌、组件规格整理 | 可选，用于统一主题和组件规范 |

**推荐组合：**

| 场景 | 推荐组合 |
|------|---------|
| 新页面或新组件 | vue-best-practices + frontend-design |
| 登录态和状态管理 | vue-best-practices + vue-pinia-best-practices |
| 路由守卫和页面跳转 | vue-best-practices + vue-router-best-practices |
| 前端测试 | test-driven-development + vue-testing-best-practices |
| 前端异常排查 | systematic-debugging + vue-debug-guides |
| 抽取复用 composable | vue-best-practices + create-adaptable-composable |
| UI 体验优化 | frontend-design + ui-ux-pro-max |

---

## 4. 项目信息、架构和图形类

| SKILL | 项目定位 | 使用场景 | 备注 |
|-------|---------|---------|------|
| drawio-skill | 架构图和流程图主技能 | 架构图、执行流程图、ER 图、时序图、泳道图、可导出的正式图 | project-info/AGENTS.md 推荐使用 |
| imagegen | 位图生成辅助技能 | 展示型图片、概念图、封面图、视觉化说明图 | 适合生成 PNG，不适合作为架构真源 |
| planning-with-files | 分析整理支撑技能 | 项目总结、阶段复盘、交接材料、复杂说明文档整理 | 适合先梳理内容，再交给图形技能出图 |
| brainstorming | 架构方案澄清 | 架构重构、流程改造、图形表达方案不明确时 | 用于复杂设计前置澄清 |

**推荐组合：**

| 场景 | 推荐组合 |
|------|---------|
| 项目架构说明书 | planning-with-files |
| 正式架构图或流程图 | planning-with-files + drawio-skill |
| 展示型图片 | imagegen |
| 架构调整方案 | brainstorming + planning-with-files |

---

## 5. 需求分析类

| SKILL | 项目定位 | 使用场景 | 备注 |
|-------|---------|---------|------|
| product-requirements | - | 需求分析时使用 | - |
| prototype-prompt-generator | - | 生成原型时使用 | - |

---

## 6. 测试类

| SKILL | 项目定位 | 使用场景 | 备注 |
|-------|---------|---------|------|
| test-cases | - | 通过需求生成测试用例时使用 | - |

---

## 7. SKILL 管理类

| SKILL | 项目定位 | 使用场景 | 备注 |
|-------|---------|---------|------|
| find-skills | 查找新技能 | 用户明确要求查找、比较、安装外部技能时 | 日常开发不默认使用 |
| skill-installer | 安装技能 | 用户确认需要安装某个技能时 | 需要用户意图明确 |
| skill-creator | 创建或优化技能 | 编写项目专用技能、调整技能触发描述、优化技能内容时 | 当前环境存在系统版和用户版同名技能 |
| plugin-creator | 创建 Codex 插件 | 需要开发 Codex 插件时 | 当前项目日常开发不使用 |
