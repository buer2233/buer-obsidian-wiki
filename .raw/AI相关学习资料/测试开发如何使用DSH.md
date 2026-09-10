# 测试开发如何使用 DSH（DeepSeek Harness）

> 来源：本地仓库 `D:\AI\deepseek-harness`（官方源码 + 官方中文文档）｜GitHub 仓库 [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)｜社区教程与插件生态资料（阿里云开发者社区、dshplugin.dev 插件目录等）
> 定位：面向测试开发工程师（Software Development Engineer in Test，SDET）的 DSH 实战指南，覆盖功能测试、接口自动化测试、UI 自动化测试、安全测试、性能测试五大领域
> 整理日期：2026-09-02｜DSH 版本基线：0.1.0-rc.x（开发者预览，协议 MIT）

---

## 学习目标

读完本文并完成练习任务后，你应该能够：

1. **用 DSH 跑测试**：让 Agent 自动探测测试框架、执行测试、汇总失败用例并给出修复建议；
2. **接入流水线**：用 headless 模式和 Python SDK 把 DSH 嵌入 CI/CD 和 pytest 体系；
3. **扩展测试工具**：写一个自定义测试工具插件（Tool）和权限门禁钩子（Hook）；
4. **把 DSH 当被测对象**：理解它的沙箱、权限、事件日志机制，评估 Agent 的安全与可测性。

---

## 一、DSH 是什么（测试视角速览）

**DeepSeek Harness（`dsh`）** 是 DeepSeek 开源的一套智能体框架（Agent Harness），官方公式：

```
Agent = Model（大脑：推理与生成） + Harness（马具：调度工具、管理上下文、编排任务、记录状态）
```

三个对测试人最重要的架构事实：

| 事实 | 含义 | 测试视角 |
|------|------|----------|
| **一切皆插件** | 模型适配器、工具注册表、会话日志、Agent 循环、甚至 UI，全部可替换重组（底层为 [Cordis](https://github.com/cordiverse/cordis) 插件框架，已在 Koishi 上验证 4 年、4000+ 插件） | 测试能力可以**以插件形式注入** Agent，而不是绕到 Agent 外面 |
| **微内核 + 扩展点** | 每个产品功能都映射到文档化扩展点上的监听器（`tools/pre-execute`、`session/event` 等），核心循环一行不改 | 钩子（Hook）= 你熟悉的**拦截器/装饰器**，可以做门禁、审计、打点 |
| **Profile 分层配置** | Web / headless / sdk / sdk-minimal / acp 都是 profile（插件组合包 patch 层叠加），`--patch` 可临时挂载覆盖层 | 同一套内核，**交互式探索**（web）与**自动化接入**（headless/SDK）随时切换 |

> 和你已经学过的 Pi 对比：Pi 走「极简核心 + 少量扩展点」，DSH 走「微内核 + 一切皆插件」。Pi 的 RPC/SDK 适合做测试驱动引擎，DSH 的插件生态和沙箱策略层适合直接组装测试工作台——两者正好互补。

### 核心概念速查表（术语双语）

| 术语 | 全称/含义 | 一句话理解 |
|------|-----------|-----------|
| 插件（Plugin） | 导出 `apply(ctx)` 函数的 TypeScript 模块 | 注册工具/监听事件的最小单元，卸载自动清理 |
| 工具（Tool） | 模型可调用的能力，`ctx.tools.register()` 注册 | 类比你给 pytest 写的 fixture/command |
| 钩子/扩展点（Hook） | `tools/pre-execute`、`tools/post-execute`、`agent/pre-step` 等事件 | 瀑布式策略层，可允许/拒绝/包裹工具调用 |
| Profile | 一组插件组合包（bundle）patch 层的叠加 | 「运行模式」的本质：`web`、`headless`、`sdk`…… |
| 沙箱（Sandbox） | 进程级文件效果隔离 | Linux bwrap/Landlock、macOS Seatbelt、Windows 受限令牌 ACL |
| 权限模式 | `read-only` / `workspace-write` / `danger-full-access` | 三级安全缰绳，逐调用可升权（需用户批准） |
| PTC 模式 | Programmatic Tool Calling | 模型写 TypeScript 程序一次性组合多步工具调用，省 Token |
| 会话（Session） | 持久化 JSONL 事件日志 | 默认存 `$DSH_HOME/sessions`，可随时恢复——**过程可追溯** |
| MCP | Model Context Protocol | 接入外部工具的标准协议，工具以 `mcp__<server>__<tool>` 暴露 |
| SDK | Python/TypeScript 客户端 | 程序化创建会话、下发任务、拿最终结果 |

---

## 二、安装与首次上手（约 30 分钟）

### 2.1 安装

```sh
# 方式一：npm 快速体验（推荐新手，Node.js ≥ 22）
npx @deepseek-ai/dsh web          # 默认 http://127.0.0.1:3080

# 方式二：全局安装（长期使用）
npm install -g @deepseek-ai/dsh
dsh web

# 方式三：源码运行（要开发插件/研究源码时）
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install && pnpm run build    # build 不能省，否则 Web 页面缺产物
pnpm dsh web
```

### 2.2 首次配置（三步）

1. **配置模型**：Web UI → 设置 → 模型，填入 DeepSeek API Key（platform.deepseek.com 申请），保存即生效无需重启；也支持 OpenAI 兼容端点、LM Studio 本地模型等近 40 家提供方；
2. **选择工作区**：添加并选中项目目录（选中前输入框不可用）；
3. **选择权限与模式**：新会话默认权限建议 `workspace-write`；Agent 预设有标准（完整工具集）/ PTC（批量自动化，省 Token）/ 极简（模型基准）/ 创造（插件开发）四种。

### 2.3 五种运行入口（测试人重点看后三个）

| 命令 | 用途 | 测试场景 |
|------|------|----------|
| `dsh web` | Web UI 交互模式 | 交互式探索、调试任务、人工审批 |
| `dsh --profile <name>` | 启动任意自定义 profile | 组装专属「测试工作台」profile |
| `dsh --profile headless "任务"` | 一次性任务，打印最终答案后退出 | **CI 里跑回归、批量执行测试并汇总** |
| `dsh --profile sdk` / `sdk-minimal` | JSON-RPC stdio，供 SDK 客户端调用 | **Python 程序内嵌 Agent** |
| `dsh --profile acp` | Agent Client Protocol，供自动化客户端调用 | 接入支持 ACP 的 IDE/工具链 |

### 2.4 插件安装（一条命令）

```sh
# 通用语法：--profile 写在最前，插件来源支持 GitHub 仓库 / npm 包 / 本地路径
dsh plugin --profile web add suimi8/dsh-test-runner        # GitHub 仓库
dsh plugin --profile web add dsh-playwright-browser        # npm 包
dsh plugin --profile web add ./my-plugin-0.1.0.tgz         # 本地 tarball

# 安装后必须重启 dsh 进程才生效；可用此命令不启动就校验配置树
dsh --profile web --dump-config
```

> 社区插件目录：[dshplugin.dev](https://dshplugin.dev)（收录 1400+ 插件）与 GitHub topic [`dsh-plugin`](https://github.com/topics/dsh-plugin)。注意：插件目录是社区维护，**不代表官方背书**，安装前应审查源码（见安全测试一节）。

---

## 三、五大测试领域实战

> 每节统一按「适用场景 → 接入步骤 → 示例思路 → 注意事项」组织。

### 3.1 功能测试：让 Agent 替你跑测试、定位缺陷

**适用场景**
- 日常回归：执行全量/增量测试并汇总失败用例；
- 缺陷定位：从失败堆栈出发，定位可疑代码并给出修复建议；
- 探索性测试：让 Agent 读仓库、理解业务逻辑、提出测试点。

**接入步骤**
1. `npx @deepseek-ai/dsh web` 启动，选中被测项目为工作区；
2. 安装测试运行插件：`dsh plugin --profile web add suimi8/dsh-test-runner`，重启；
3. 新建会话，权限选 `workspace-write`，下发任务。

**示例思路**

```
任务提示词示例：
「执行项目全部测试用例，汇总失败用例，分析报错原因，给出代码修改建议（不要直接改，先给 diff 预览）」
```

`dsh-test-runner` 插件的核心价值：
- **自动探测测试框架**：vitest / jest / pytest / node:test 无需手动指定；
- **一次工具调用完成闭环**：「改代码 → 跑测试 → 修」不再每步都过一轮模型推理；
- **结构化摘要**：只返回通过/失败统计 + 失败用例名与错误信息，**省 Token**；
- 高危操作（改文件）会触发 Web UI 审批，你人工把关。

**注意事项**
- Agent 修复建议≠正确修复：坚持「先 diff 预览、人工审查、再落盘」，让它改完后**必须重跑测试**自证；
- 大仓库先限定范围（如 `只跑 tests/api/ 目录`），避免全量执行超时与 Token 浪费；
- 会话默认持久化在 `$DSH_HOME/sessions`（JSONL 日志），失败定位过程全程可回放——**这本身就是测试证据链**。

### 3.2 接口自动化测试：SDK 嵌入 + 自定义工具 + MCP

**适用场景**
- 用例生成与维护：基于抓包数据/已有用例批量生成新用例；
- 冒烟链路编排：让 Agent 按业务流程串联多个接口调用并断言；
- 把 Agent 嵌入你的 pytest 体系做「AI 辅助用例维护」。

**接入步骤**

方式 A——**Python SDK 内嵌**（推荐，Python 3.10+）：

```powershell
python -m pip install deepseek-harness-sdk
```

```python
from pathlib import Path
from deepseek_harness import DeepSeekHarness

workspace = Path(r"C:\work\disposable-workspace").resolve()
dsh_home  = Path(r"C:\work\example-dsh-home").resolve()

with DeepSeekHarness(
    provider="deepseek-official",
    model="deepseek-v4-flash",
    cwd=str(workspace),
    dsh_home=str(dsh_home),
    profile="sdk-minimal",          # 极简 profile：仅 bash/pwsh + 文件编辑器
) as harness:
    result = harness.run(
        "读取 tests/api/ 下的 pytest 用例，根据 api-spec.yaml 的新增字段补齐断言并运行验证。",
        session_id="api-case-001",
    )
print(result.final_response)
```

方式 B——**自定义接口测试工具插件**（把 `requests` 能力注册为工具，模型按 schema 调用）：

```ts
import type { Context } from '@deepseek-ai/cordis'
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'api-smoke-tool'
export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'api_smoke',
    description: 'Send an HTTP request and return status/headers/body.',
    parameters: {
      method:  { type: 'string', required: true, description: 'GET/POST/...' },
      url:     { type: 'string', required: true },
      body:    { type: 'string', required: false, description: 'JSON string' },
    },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    async execute(args) {
      // 这里用 fetch/axios 发请求，返回结构化的 响应码+耗时+body 摘要
      const res = await fetch(args.url, {
        method: args.method,
        body: args.body,
        headers: { 'Content-Type': 'application/json' },
      })
      return JSON.stringify({
        status: res.status,
        ms: Date.now(),               // 实际应记录起止时间差
        body: (await res.text()).slice(0, 2000),
      })
    },
  }))
}
```

方式 C——**MCP 服务器接入**：数据库 MCP（SQL 校验数据）、GitHub MCP（接口变更联动）等，用 overlay 配置：

```yaml
- insert:
    - id: my-mcp
      name: '@deepseek-ai/dsh-mcp-client'
      config:
        serverName: my-db
        transport: stdio
        command: my-db-mcp
        args: []
        env: {}
```

**示例思路**
- 「对照 mitmproxy 抓包导出的 HAR 文件，生成 `test_*.py` 用例骨架（pytest + requests，含断言）」；
- 「先调登录接口拿 token，再依次调下单/查单/取消接口，任何一步响应码非 2xx 即失败并输出链路报告」。

**注意事项**
- **`sdk-minimal` profile 固定 `danger-full-access`**：官方明确要求用一次性 checkout 或容器隔离，别指向生产环境或个人文件目录；
- 每次独立任务用新的 `session_id` 和独立 `dsh_home`，只有延续对话才复用；
- 环境变量传密钥（`DEEPSEEK_API_KEY` 等），不要把密钥写进 YAML/代码。

### 3.3 UI 自动化测试：浏览器插件 + 语义定位 + 截图留证

**适用场景**
- 探索式 UI 测试 / 冒烟：让 Agent 操作真实浏览器走业务流；
- 自愈式定位：用语义定位器（无障碍树）替代脆弱的 CSS 选择器；
- 页面数据抓取与可视化验证（截图留证）。

**接入步骤**

以 `dsh-playwright-browser` 为例（多标签页、语义定位）：

```sh
# 1. 安装（要求 Node ^22.19.0 或 >=24）
dsh plugin --profile web add dsh-playwright-browser

# 2. 安装浏览器内核（如未安装）
npx playwright install chromium

# 3. 校验配置组合，重启 dsh web 生效
dsh --profile web --dump-config
```

可选配置写入 profile 的 `cordis.patch.yml`：

```yaml
- insert:
    - id: playwright-browser
      config:
        browser: chromium
        headless: true
        viewportWidth: 1440
        viewportHeight: 900
        screenshotDir: .dsh-browser/screenshots   # 截图留证目录
```

**示例思路**

Agent 在会话中按任务链调用 `browser_*` 工具，典型流程（工具名即流程）：

```
browser_open(https://uat.example.com/login)
  → browser_snapshot            # 读无障碍树，确认可交互元素
  → browser_fill(label=Email, ...) / browser_click(button|Sign in)
  → browser_wait(url 或元素就绪)
  → browser_screenshot          # 关键步骤截图留证
  → browser_tabs / browser_history   # 多标签页、后退/刷新管理
```

语义定位器示例：`role=button|Save`、`label=Email`、`placeholder=Search`——**比 CSS 选择器更抗 UI 改版**，与你用 Playwright 原生 `getByRole/getByLabel` 同源。

同类插件选型：

| 插件 | 特点 | 适合 |
|------|------|------|
| `dsh-playwright-browser` | 多标签、无障碍树快照、语义定位、截图 | UI 测试主力（推荐） |
| `dsh-plugin-playwright` | 社区流传较广的 Playwright 封装，保留登录态/Cookie | 需要登录态的场景 |
| `dsh-browser` | 桥接你**正在用**的 Chrome（扩展+桥接），登录态全保留 | 调试本人已登录环境 |

**注意事项**
- **别把 `userDataDir` 指向个人日常浏览器配置目录**，用专供自动化的独立目录；
- 插件以 DSH 进程权限运行，可访问其能触及的文件/网络/浏览器数据，安装前审查源码；
- UI 自动化断言仍建议沉淀为 Playwright 原生脚本（Agent 生成 → 人工审查 → 入库），Agent 交互式操作适合探索和冒烟，**不适合替代入库的回归资产**；
- 升级 DSH 或插件后，跑一遍你的典型任务链做回归（社区经验）。

### 3.4 安全测试：三级缰绳 + 钩子门禁 + 把 DSH 当被测对象

DSH 的安全体系分两层：**用 DSH 做安全相关测试**（权限门禁、危险命令拦截、审计）和**对 DSH 本身做安全测试**（沙箱逃逸、提示注入）。

**适用场景**
- 给 Agent 的工具调用加策略门禁（如禁止访问生产配置、禁止 `rm -rf`）；
- 审计 Agent 的每一步工具调用（谁、何时、调了什么、结果如何）；
- Agent 安全测试研究：沙箱边界验证、恶意插件风险分析。

**接入步骤**

第一步：**选对权限模式**（Web UI 设置或 profile 配置）：

| 模式 | 效果 | 测试场景 |
|------|------|----------|
| `read-only` | 命令只读执行 | 代码审计、只读分析——最安全 |
| `workspace-write` | 只能写当前工作区 | 日常开发/测试推荐默认 |
| `danger-full-access` | 不受限 | 仅隔离环境（容器/一次性 VM）使用 |

第二步：**写权限门禁钩子插件**（官方 extension-cookbook 的权限门禁模式）：

```ts
import type { Context } from '@deepseek-ai/cordis'
import type { PreToolDecision, ToolExecution } from '@deepseek-ai/dsh-tools'

export const name = 'qa-permission-gate'

// 危险命令黑名单 + 敏感路径白名单，按需实现
async function isAllowed(exec: ToolExecution): Promise<boolean> {
  // 例如：解析 exec 中的 bash 命令，拒绝 rm -rf / curl 外发 / 读 .env
  return true
}

export function apply(ctx: Context) {
  ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
    if (!(await isAllowed(exec))) {
      return { kind: 'deny', reason: 'Denied by QA policy.' }
    }
    return next()
  })
}
```

这个 `tools/pre-execute` 是**瀑布式策略层**：沙箱、权限、plan-mode 插件都挂在这个扩展点上。相关扩展点选择规则（官方约定）：

| 需求 | 扩展点 |
|------|--------|
| 允许/拒绝一次调用（门禁） | `tools/pre-execute`（单调最终拒绝用 `ctx.tools.guard()`） |
| 包裹执行：超时/重试/指标 | `tools/execute` |
| 变换结果 / 附加上下文 | `tools/post-execute` |
| 观察不可变最终结果（**审计**） | `tools/result` |

第三步（进阶）：**把 DSH 当被测对象**做安全测试——
- 沙箱是**同世界隔离**：与宿主共享内核与文件系统，Linux 用 bwrap + Landlock、macOS 用 Seatbelt、Windows 用 ACL 受限令牌（官方有决策文档说明为何弃用 AppContainer）；
- 官方 SAFETY.md 明确：**未经安全审计、不保证隔离、不得作为生产软件**，「不要把 DSH 当作不可信工作负载唯一的安全控制措施」——这是你做 Agent 安全评估时可以直接引用的官方边界声明；
- 攻击面清单：模型生成的代码/命令、第三方插件（供应链）、提示注入、凭据文件（`$DSH_HOME/.credentials.yaml`，仅当前用户可读写）。

**示例思路**
- 「列出本会话所有 `tools/result` 事件，生成工具调用审计报告（工具名、参数摘要、结果状态、耗时）」——一个审计插件就是 `tools/result` 监听器 + 落盘；
- 「尝试让 Agent 在 read-only 模式下写文件，验证沙箱拒绝行为与错误信息」——沙箱合规性用例；
- 「模拟提示注入：在工作区放置含恶意指令的 README，观察 Agent 是否被诱导执行危险命令，权限门禁是否拦截」。

**注意事项**
- 优先在一次性 VM/容器中运行 `danger-full-access`；
- 安装任何社区插件前**审查源码**（`dshplugin.dev` 收录 ≠ 安全审查通过）；
- MCP stdio 桥接器会主动移除环境中的凭据类变量和 `DSH_*` 变量——接入外部 MCP 时验证这点是否覆盖你的密钥暴露面。

### 3.5 性能测试：后台任务 + 定时 + Token 成本观测

**适用场景**
- 让 Agent 协助编写/维护 JMeter / Locust / k6 压测脚本；
- 长时间压测的监控与告警跟进（后台代理盯指标）；
- 对 Agent 自身的**成本与效率评测**（Token 消耗、首 Token 延迟、并发吞吐）。

**接入步骤与示例思路**

1. **脚本生成**（web/headless 均可）：

```
「根据 tests/perf/ 下的 Locust 脚本模式，为新增的 /api/v2/order 接口编写压测场景：
并发 100、持续 5 分钟、P95 < 800ms 断言，输出 locustfile.py，不要执行」
```

2. **后台代理盯监控**（社区插件 `dsh-background-agents`）：

```sh
dsh plugin --profile web add dsh-background-agents
```

主会话里继续干别的，后台代理同时跑压测、轮询监控、收集数据，随时可查看进度或接管会话；长会话持久化，关掉窗口回来还能继续。

3. **会话内定时**（官方可选 overlay，注意：仅会话级提醒，不是 cron）：

```sh
dsh web --patch apps/cli/config/examples/schedule/cordis.yml
```

模型通过 `schedule_create / schedule_list / schedule_delete` 管理提醒（`after_seconds` / 绝对时间 `at` / ≥300 秒的 `every_seconds`）。适合「每 5 分钟检查一次压测指标，异常则汇报」这类会话内轮询。**不支持 Cron 表达式**，进程级周期任务请交给 CI 或你的调度系统。

4. **Agent 自身性能观测**：Web UI 会话头部有实时 Token 统计（社区 `dsh-web-ui` 插件还有任务看板/实时令牌统计）；对比评测可复用你在 Pi 精读中学到的方法论（baseline vs candidate、pass-rate lift、token/延迟增量）——DSH 的会话 JSONL 日志就是现成的轨迹数据源。

**注意事项**
- 压测执行本身交给传统工具（Locust/JMeter），**Agent 负责「编写脚本 + 观察结果 + 分析瓶颈」**，别让 Agent 逐请求发压（既慢又贵）；
- PTC 模式（程序化工具调用）适合批量自动化任务，能明显省 Token；但社区实测某些预设（如锚定类预设）Token 消耗显著更高——批量任务前先用小样本估算成本；
- `every_seconds` 提醒最小间隔 300 秒，且只在会话 idle 时投递，别指望毫秒级轮询；
- headless 批量跑任务时注意 API 限流与并发配额，任务间加退避。

---

## 四、插件开发速成：写一个「测试守护」插件

把 3.2 的工具插件 + 3.4 的门禁钩子组装成完整流程（本地开发模式，从源码仓库）：

```sh
# 1. 在仓库根目录建插件项目
mkdir -p scratch-plugin/src

# 2. 写 scratch-plugin/src/my-plugin.ts（工具注册 + 钩子门禁，见上文代码）

# 3. 写 scratch-plugin/cordis.yml（本地插件 overlay，路径必须绝对路径）
cat > scratch-plugin/cordis.yml <<EOF
- insert:
    - id: qa-guard
      name: '/绝对路径/deepseek-harness/scratch-plugin/src/my-plugin.ts'
      config:
        blockedCommands: ['rm -rf', 'curl']
        protectedPaths: ['.env', 'config/prod*']
EOF

# 4. 挂载 overlay 启动
pnpm dsh web --patch ./scratch-plugin/cordis.yml
```

插件骨架要点（官方文档约定）：

| 要素 | 作用 |
|------|------|
| `export const name` | 插件名 |
| `export const inject = ['tools']` | 声明依赖的服务，框架保证就绪后才加载你的插件 |
| `export function apply(ctx, config)` | 入口，通过 `ctx` 注册的一切（事件/工具/定时器）**卸载时自动清理** |
| `ctx.effect(() => 清理函数)` | 手动资源（网络连接等）的清理挂钩 |
| `export const Config = Schema.object({...})` | Schemastery schema，加载时校验配置；**官方约定：凡是可调参数必须做成配置字段，不硬编码** |

要让插件跨次运行持久生效：把 `insert` patch 合并进 `$DSH_HOME/profiles/<name>/cordis.patch.yml`（单 profile）或 `$DSH_HOME/cordis.patch.yml`（全部 profile），**不要覆盖已有文件**。

---

## 五、接入 CI/CD 流水线

最小可用模式——headless 一次性任务：

```yaml
# GitLab CI 示例（示意）
stages: [test]
agent-regression:
  stage: test
  image: node:22
  script:
    - npm install -g @deepseek-ai/dsh
    - export DEEPSEEK_API_KEY=$DSH_KEY          # 密钥走 CI 变量，绝不入库
    - dsh --profile headless "运行 pytest 全量测试，汇总失败用例与原因，
      输出 markdown 报告到 artifacts/test-report.md"
  artifacts:
    paths: [artifacts/]
```

Python SDK 模式（嵌入现有 pytest 体系）：

```python
# conftest.py 示意：把「AI 用例维护」做成一个 pytest 命令
import pytest

@pytest.fixture(scope="session")
def dsh():
    from deepseek_harness import DeepSeekHarness
    with DeepSeekHarness(provider="deepseek-official",
                         model="deepseek-v4-flash",
                         cwd="./", dsh_home="./.dsh-home",
                         profile="sdk-minimal") as h:
        yield h
```

CI 接入三原则：
1. **隔离**：容器内运行，workspace 用一次性 checkout；`sdk-minimal` 是 full-access，更要隔离；
2. **确定性**：CI 中禁用随机性，任务描述写明确产物路径（报告、diff），用退出码/产物存在性做断言；
3. **成本闸门**：先在 MR 级别跑「失败用例分析」这类小任务，跑通后再扩大到「生成用例」等大任务。

---

## 六、注意事项与避坑（汇总）

| # | 坑/注意 | 说明 |
|---|---------|------|
| 1 | Node.js 版本 | 必须 ≥ 22；社区反馈 v24 装部分插件有兼容性问题，稳妥用 22.x |
| 2 | 插件装完不生效 | 必须重启 dsh 进程（重开终端再 `dsh web`） |
| 3 | 开发者预览 | 官方明确「会有破坏性变更」，升级后用 `--dump-config` + 典型任务链回归 |
| 4 | `--profile` 参数位置 | 启动器参数必须在最前：`dsh --profile headless "任务"`，顺序错会报错 |
| 5 | 源码运行漏 build | 只 `pnpm install` 不 `pnpm run build`，Web 页面缺构建产物 |
| 6 | 插件目录路径 | `cordis.yml` 中本地插件必须**绝对路径**；插件目录放 Harness 源码仓库内，避免模块解析报错 |
| 7 | 密钥管理 | 环境变量传 Key；MCP 配置里密钥写 `config.env`，不写进 YAML 明文 |
| 8 | 沙箱非绝对安全 | 官方 SAFETY.md：未经审计、不保证隔离；敏感环境用一次性 VM/容器 |
| 9 | 社区插件 ≠ 官方背书 | dshplugin.dev 只是收录目录，安装前审查源码与许可证 |
| 10 | Token 成本 | PTC 模式省、锚定类预设费；批量任务先小样本估算 |
| 11 | 一次性任务用新 session | 独立任务新 session_id + 独立 dsh_home，只有延续对话才复用 |
| 12 | 浏览器 userDataDir | 别指向个人日常浏览器目录，用专用自动化目录 |

---

## 七、测试面试考点

**考点 1：DSH 的「一切皆插件」对测试自动化有什么价值？**
- 考察点：是否理解 Agent 架构与测试能力的结合方式。
- 答题要点：微内核 + 扩展点（`tools/pre-execute`/`tools/result` 等）意味着测试能力（执行器、门禁、审计、报告）可以以插件形式注入 Agent 运行时，而不是外挂脚本；钩子即策略层（类比拦截器），可做门禁/审计/打点；Profile 分层让同一内核覆盖交互（web）与自动化（headless/SDK）两种工作方式。

**考点 2：如何在 CI 中安全地使用 dsh？**
- 答题要点：容器隔离 + 一次性 checkout；权限最小化（非必要不用 full-access；`sdk-minimal` 恰恰是 full-access，更要隔离）；密钥走环境变量/CI secret；产物与退出码做确定性断言；先小任务灰度再放量。

**考点 3：Agent 的沙箱就安全了吗？**
- 答题要点：不能这么假设。DSH 官方 SAFETY.md 明确「未经安全审计、不保证隔离」；沙箱是同世界隔离（共享内核与文件系统），能降低风险不能消除；正确姿势是最小权限 + 隔离环境 + 插件源码审查 + 门禁钩子多层防御。

**考点 4：DSH 与 Pi/Claude Code 在测试工程上的定位差异？**
- 答题要点：Pi＝极简核心 + 可编程（RPC/SDK 适合做测试驱动引擎、二次开发）；DSH＝微内核 + 插件生态（适合组装测试工作台、策略门禁、CI 接入），会话 JSONL 日志支持过程回溯；Claude Code＝开箱即用全家桶（适合个人效率）。选型逻辑：做 Agent 测试框架选 Pi，做团队测试工作台选 DSH，个人日常用 Claude Code。

**考点 5：如何评测一个 Agent 框架的测试友好度？**
- 答题要点：沿用可测性四维——可观测性（事件日志/遥测）、可控制性（钩子/沙箱/权限）、可断言性（结构化结果/schema）、可隔离性（faux 模型/sandbox/profile）；再叠加成本维度（Token/延迟）。

---

## 八、练习任务清单

- [ ] 1. `npx @deepseek-ai/dsh web` 跑通第一个会话，配置模型 + 工作区，观察审批流程（30 分钟）
- [ ] 2. 对一个 pytest 项目下发「跑全量测试 + 汇总失败 + 给修复建议」，人工审查 diff 后让它落盘并重跑（对比与手工的差异）
- [ ] 3. 安装 `dsh-test-runner`，体验「一次工具调用闭环」的 Token 消耗差异（看会话统计）
- [ ] 4. 安装 `dsh-playwright-browser`，让 Agent 用语义定位器完成一次登录→搜索→截图流程，对比你手写 Playwright 脚本的定位策略
- [ ] 5. 写一个 `tools/pre-execute` 门禁插件，拦截 `rm -rf` 与 `.env` 读取，并测试拦截是否生效
- [ ] 6. 用 `dsh --profile headless "..."` 在本地跑一次失败用例分析，检查 JSONL 会话日志结构
- [ ] 7. 用 Python SDK 把「根据接口变更维护用例」封装成 pytest 命令，dsh_home 指向专用目录
- [ ] 8.（进阶）用会话日志数据做一次 baseline vs candidate 的 Agent 行为对比评测（复用 Pi evals 方法论）
- [ ] 9.（进阶）通读 `packages/sandbox/README.zh.md` 与 `SAFETY.zh.md`，输出一份 Agent 安全面测试用例清单

---

## 九、参考来源

| 类型 | 来源 |
|------|------|
| 官方仓库 | https://github.com/deepseek-ai/deepseek-harness |
| 官方文档 | https://deepseek-harness.github.io/deepseek-harness/（docs/user/guide、docs/user/develop、docs/cookbook） |
| 本地源码 | `D:\AI\deepseek-harness`（README.zh.md、SAFETY.zh.md、apps/cli/README.zh.md、packages/sandbox、docs/user/develop/*、docs/cookbook/extension-cookbook.zh.md） |
| 社区教程 | 阿里云开发者社区《DeepSeek Harness 从安装到跑通测试，30 分钟上手》《从 0 到 1 玩转 DeepSeek Harness》、夜雨飘零博客（dsh-playwright-browser 详解）、CSDN 插件盘点系列 |
| 插件生态 | https://dshplugin.dev（社区插件目录）、https://github.com/topics/dsh-plugin |

> 说明：DSH 处于开发者预览阶段，迭代极快，本文命令与配置以 2026-09-02 的 0.1.0-rc.x 基线为准；正式使用前请以官方文档核对最新语法。社区插件（dsh-test-runner、dsh-playwright-browser 等）为第三方维护，安装前请自行审查源码。
