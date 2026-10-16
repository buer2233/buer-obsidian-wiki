---
type: note
title: "TypeSafe Jev 国内使用指南：官网导航 + 四条接入路径 + 实测连通性"
source: ".raw/AI相关学习资料/jev/TypeSafe_Jev国内使用指南(官网导航+四条接入路径+实测连通性).md"
created: 2026-10-15
updated: 2026-10-15
tags:
  - Jev
  - TypeSafe
  - 接入路径
  - 连通性实测
  - 测试开发
status: live
related:
  - "[[wiki/AI相关学习资料/Jev决策模型(System One)学习参考资料]]"
  - "[[wiki/AI相关学习资料/Jev用于UI自动化测试可行性分析与AI测试工具横向对比]]"
  - "[[wiki/AI相关学习资料/测试开发如何使用DSH]]"
  - "[[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点]]"
  - "[[wiki/AI相关学习资料/index]]"
---

# TypeSafe Jev 国内使用指南：官网导航 + 四条接入路径 + 实测连通性

> **一句话定义**：这是一份**照着做就能跑通**的 Jev 接入手册——国内**直连可用**（实测 1.57s / 1.71s，无需代理），四条主流路径各有明确边界，另有第五条「自建 System One 兼容端点」作为内部项目的唯一合规解。

**阅读对象**：测试开发工程师（SDET）/ AI 测试方向求职者。**前置阅读**：《Jev 决策模型（System One）学习参考资料》《Jev 用于 UI 自动化测试可行性分析与 AI 测试工具横向对比》（同目录）。**日期与分级**：撰写/检索/本机实测均为 2026-09-21（Windows 中文环境，走代理与直连两组对照）。🟢 官方一手｜🟡 第三方实测｜🔵 **本机实测**｜🔴 不可靠/过时来源。

---

## 零、结论速览

| 问题 | 结论 |
|------|------|
| **官网 / 文档 / 控制台** | `https://typesafe.ai`（**200**）｜`https://docs.typesafe.ai`（**308** 跳转）｜`https://console.typesafe.ai`（**307** 跳转） |
| **API 端点** | `POST https://api.typesafe.ai/v1/systemone`（实测 **405 存在** + 无密钥 **403 认证错误**） |
| **国内能连上吗** | ✅ **能。走系统代理和直连都通。** 直连 `typesafe.ai` **1.57s**、`api.typesafe.ai` **1.71s** |
| **还需要候补名单吗** | ❌ **不需要**。2026-09-21 全面开放，注册即送 **$5 额度（约 1.2 亿 token）** |
| **最省事的国内路径** | **官方直连**（64k 上下文、SDK 最全）；备选 **OpenRouter**（无需海外卡） |
| **最大的两个坑** | ⚠️ 国内：以英文为主要训练语言，**CJK「能处理但准确率不等同」**（官方原话），中文场景必须先自测；⚠️ 合规：仅托管 API + 服务在美国西海岸 + 不接受客户数据微调 → 内部项目仍不能直接用（见 3.5 / 第六章） |

## 一、环境前置条件（含账号开通）

| 前置项 | 要求 | 说明 |
|------|------|------|
| **网络** | 直连即可（也可走系统代理） | 实测直连 1.5–1.7s，跨境正常水平；**不要在代码里硬编码代理**，用环境变量并在 CI 留开关 |
| **账号** | `https://console.typesafe.ai` 注册，**已无候补** | 时间线：09-15 发布需候补（官方称首 36 小时清理约 14 万注册）→ 09-16~20 生态爆发（1200+ 仓库）→ **09-21 全面开放**，注册送 $5 |
| **凭据** | API Key（`ts_...`），控制台 `/keys` 创建 | **通常只显示一次，立即保存** |
| **环境变量** | `export TYPESAFE_API_KEY="ts_..."` | SDK 默认读这个变量名 |
| **Python（走 SDK）** | **>= 3.10** | `pip install typesafe-sdk` 或 `uv add typesafe-sdk` |
| **Node（走 Agent Skill）** | 有 `npx` 即可 | 非 Claude Code 的 Agent 需要 |
| **客户端语言** | 官方直连全部（HTTP）／OpenRouter 仅 JS SDK+HTTP／Vercel **仅 AI SDK** | 见第三章 |

**开通四步**：① 注册 `https://console.typesafe.ai` → ② **强烈建议先试玩**：进 `https://console.typesafe.ai/playground`，粘一段你自己的文本作 state、加一条 Noul 问题看返回 → ③ 建 Key `https://console.typesafe.ai/keys` → ④ 配 `export TYPESAFE_API_KEY="ts_..."`。**付款与限额**：$5 额度约 **1.2 亿输入 token**（按 $0.042/百万输入 token、输出免费反推吻合）；后续充值需海外支付方式，不想绑海外卡走 OpenRouter；企业/更高限额联系 `sales@typesafe.ai`。控制台另有 Playground、API Keys、Usage（官方标注 "Stats may be delayed"）、Legal / Trust Center（企业 ZDR）、Discord。

> [!gap] 两个容易踩的认知坑
> ① 还在讲「候补通道／排队／只能走第三方」的中文教程是 **09-15～09-20** 的过时信息。② 别把 $5 类比成「1.2 亿 token 的 GPT 调用」——Jev 返回的是**极小的类型化结果**，输入通常也只是紧凑 state，不是同一种工作量。

> [!key-insight] 前置条件里唯一的「不可省」替代项
> 若目标是**代码与数据不出内网**，上面全部不成立——但 `tontoko/jev-browser` 支持把 `JEV_BASE_URL` 指向自建端点且**不需要 Jev API key**，内网实现同款 `POST /v1/systemone` 契约即可复用整套生态（见 3.5）。

## 二、官网与文档导航

| 入口 | 地址 | 用途 |
|------|------|------|
| 官网首页 / 发布博客 / **文档首页** | `https://typesafe.ai/`、`/blog/introducing-system-one-models-and-jev`、`https://docs.typesafe.ai/` | 含 193.6x / 444.6x 宣传数字；发布博客技术细节最全；文档逢事以这里为准 |
| **快速开始 / 概念** | `/introduction/quickstart`、`/introduction`、`/introduction/machine-learning-primer`、`/concepts/system-one`、`/concepts/state`、`/concepts/how-to-build-with-system-one` | ★ 四条上手路径；state 的写法与支持形状 |
| **原语 / 模式** | `/primitives`、`/primitives/advanced`、`/patterns`（`/fan-out`、`/confidence-routing`、`/composite-scoring`、`/intent-routing`） | ★ 三原语 Choice/Score/Noul；★ 四个架构模式 |
| **置信度 / 模型** | `/confidence`、`/models` | ★ 定义、近似公式、三段式路由；★ 模型 ID、别名、价格、速率限制、上下文、语言支持 |
| **缺陷页** | `/model-jaggedness/jev-1.13` | ★★ 官方自曝的 9 条缺陷（必读） |
| API / SDK / Skill / 法务 | `/api`、`/sdk`、`/agent-skill`、`/cookbooks/…`、`/legal` | HTTP 参考（含限流处理）、Python / JavaScript SDK、给 Claude Code / Codex 的 Skill、现成配方、DPA／隐私政策／企业 ZDR |
| **控制台** | `https://console.typesafe.ai/playground`、`/keys` | ★ 粘 state 加问题看结果；创建管理 API Key |
| 评测站 / API | `https://evals.typesafe.ai/`；`POST https://api.typesafe.ai/v1/systemone`、`GET /v1/models` | 工作流评测（含完整查询与分歧点）；唯一决策端点；列出账号可用模型 |
| GitHub | `typesafe-ai/system-one-adapter-python`、`typesafe-ai/skills` | ★ 把任意 LLM 包成同一接口；★ Skill 源码（含 SKILL.md） |

**四个「必读」页面的优先级**：

| 优先级 | 页面 | 为什么 |
|--------|------|--------|
| **1** | `/model-jaggedness/jev-1.13` | 官方自曝的 9 条缺陷。发布报道几乎都没走过这页，而它决定你能不能上线 |
| **2** | `/models` | 模型 ID、**别名会漂移**、价格、**速率限制是动态的**、上下文口径 |
| **3** | `/confidence` | 置信度怎么算、Noul 为什么没有 confidence、**三段式路由**、阈值随风险分级 |
| **4** | `/introduction/quickstart` | 四条上手路径（Playground / API / SDK / Agent Skill） |

## 三、四条接入路径逐条讲清

源文件标题中的「四条」指 **A–D**；表里的 **E** 是内部/合规场景专用解，性质与其他四条不同（它的价值在「完全不出网」，而不在「连得上」）。

| 路径 | 国内可达性 | 海外卡 | 上下文 | 客户端语言 | 控制台 | 推荐度 | 适用场景 |
|------|-----------|--------|--------|--------|--------|--------|---------|
| **A. 官方直连** | ✅ 直连 1.71s | 充值需要 | **64k**（state+问题 32k） | **全部**（HTTP） | ✅ | ⭐⭐⭐⭐⭐ | 默认首选，SDK 最全 |
| **B. OpenRouter** | ✅ 直连 0.83s | ❌ 不需要 | **32k**（口径更小） | JS SDK / HTTP | ❌ | ⭐⭐⭐⭐ | 无海外卡、要最省事 |
| **C. Vercel AI Gateway** | ✅ 可达 | ⚠️ 需绑卡验证 | 以官方为准 | ⚠️ **仅 AI SDK** | ❌ | ⭐⭐⭐ | 本就在用 AI SDK 的 TS 项目 |
| **D. Cloudflare AI Gateway / LiteLLM / Composio** | ✅ 可达 | 视产品而定 | 以官方为准 | 视产品而定 | ❌ | ⭐⭐⭐ | 已有网关/编排平台的团队 |
| **E. 自建兼容端点** | ✅ 完全不出网 | ❌ 不需要 | 自己定 | **全部** | 自己建 | ⭐⭐⭐⭐⭐（合规场景） | 数据不出内网的内部项目 |

### 3.1 路径 A：官方直连（推荐）

优点：上下文最大（64k）、SDK 最完整、有控制台看用量与限额、**延迟最少一跳**（官方端到端 70–500ms）。

```bash
export TYPESAFE_API_KEY="ts_..."
# 本机实测可直连，无需代理
curl -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"jev-latest","state":"你的文本或 JSON 状态",
       "questions":{"department":{"type":"choice","instructions":"Which team should handle this",
         "criteria":{"billing":"Payment or subscription issues","technical":"Bugs or integration problems",
                     "sales":"Pricing or account questions"}}}}'
```

**Python SDK 版**（`pip install typesafe-sdk`，需 Python >= 3.10；或 `uv add typesafe-sdk`）：

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
client = TypeSafeClient()   # 从环境变量 TYPESAFE_API_KEY 读密钥，默认模型 jev-latest
r = client.system_one(
    state="Hi, I've been trying to connect my Stripe account for 3 days and the integration keeps failing.",
    questions={
        "department": Choice(instructions="Which team should handle this",
                             criteria={"billing": "Payment", "technical": "Bugs or integrations", "sales": "Pricing"}),
        "frustration": Score(instructions="How frustrated the customer appears",
                             criteria=["Calm", "Frustrated but civil", "Very angry"]),
        "is_urgent": Noul(instructions="The message conveys urgency or time-sensitivity"),
    },
)
print(r.answers["department"].choice, r.answers["frustration"].score, r.answers["is_urgent"].noul)  # "technical" 1.0 1.0
```

显式走代理（部分网络环境可能需要）：`import os; os.environ["HTTPS_PROXY"] = "http://127.0.0.1:<端口>"`，然后照常用 `TypeSafeClient()`。

> [!key-insight] 生产建议：把模型钉死在版本号上
> 用 `TypeSafeClient(model="jev-1.13.0")`，不要用 `jev-latest`。官方原话："An alias moves when a new release ships... **If you have tuned confidence thresholds against a specific version, pin that version's ID.**"

### 3.2 路径 B：OpenRouter（不需要海外卡）

实测直连 **0.83s**（走 Cloudflare，比官方还快）。模型 ID：`typesafe/jev-1.13`（当前版本）、`typesafe/jev-1.13-20260917`（带日期的构建）、`typesafe/jev-latest`（跟踪最新）。

**⚠️ 最大的坑：它不在 chat completions 端点上。** OpenRouter 提供的是独立的 **Decisions API**：`POST https://openrouter.ai/api/alpha/decisions`，头为 `Authorization: Bearer $OPENROUTER_API_KEY` + `Content-Type: application/json`。官方原文："It runs on the OpenRouter **Decisions API** rather than the OpenAI-compatible chat endpoint... **chat completions SDKs will not work with it.**" → **不能把一个 OpenAI 客户端指向 OpenRouter 的 base URL 就用上 Jev。**

```javascript
import { OpenRouter } from "@openrouter/sdk";
const openrouter = new OpenRouter({ apiKey: process.env.OPENROUTER_API_KEY });
const decision = await openrouter.alpha.decisions.create({
  decisionsRequest: {
    model: "typesafe/jev-1.13", state: "Help! My payouts have been failing for 3 days.",
    questions: {
      is_urgent: { type: "noul", instructions: "Does this message convey urgency?" },
      department: { type: "choice", instructions: "Which team should handle this?",
                    criteria: { billing: "Payments, invoicing, refunds", technical: "Bugs, outages",
                                sales: "Pricing, upgrades, new accounts" } },
      frustration: { type: "score", instructions: "How frustrated is the customer?",
                     criteria: ["Calm", "Frustrated", "Very angry"] },
    },
  },
});
const { is_urgent, department } = decision.answers;
if (is_urgent.noul > 0.8 && department.choice === "billing") { /* escalateToBilling(...) */ }
```

**另两个注意点**：① **上下文只有 32k**（官方直连 64k），大批量 state 迁移前必须核对天花板；② **Jev 不出现在 OpenRouter 公开模型列表 API 里**，任何「枚举模型列表生成选择器」的工具都看不到它。

### 3.3 路径 C：Vercel AI Gateway

模型 ID `typesafe-ai/jev`，TS 项目接入就是改一行模型名。**⚠️ 关键限制**：Vercel 评测文档明确——**评测能力只通过 AI SDK 提供，Gateway 的 OpenAI / Anthropic / Cohere 兼容端点都到不了 Jev**，即「把 OpenAI 客户端指向 Gateway base URL」的接入方式访问不了 Jev，**直接排除 Go / Rails / 任何走 OpenAI 形态 SDK 的服务**。

```javascript
import { experimental_evaluate as evaluate } from "ai";
const result = await evaluate({ model: "typesafe-ai/jev", state: "你的上下文内容...", questions: { /* 你的问题 */ } });
```

**生产注意**：Gateway key 是唯一凭据，**拿不到 TypeSafe 控制台、看不到按 key 用量、也看不到离 Jev 自身限额（25 万 token/秒、1200 请求/分钟）还有多远**，而那两个数字本身还是动态的。**量级重要就自己记请求数。**

### 3.4 路径 D：Cloudflare AI Gateway / LiteLLM / Composio

| 通道 | 形态 | 适合谁 |
|------|------|--------|
| **Cloudflare AI Gateway** | 控制台左侧 `AI` → `AI Gateway` 下可选 Jev | 已经在用 Cloudflare 的团队 |
| **LiteLLM** | 复杂度路由器可选 Jev 判断请求走哪个模型档位 | 已用 LiteLLM 统管模型的团队 |
| **Composio** | Jev toolkit，2 个工具（`Evaluate State` / `List Models`） | 用 Composio 编排 Agent 的团队 |
| **new-api 插件** | 给自建 LLM 网关加原生 `/v1/systemone` 端点 | 想把「决策」和「对话」放在同一网关后面 |

**LiteLLM 那条值得单独提**：有回测显示 237 个真实回合成本降约 **60%**；并得出一个反直觉结论——**置信度低于 0.5 时应降级到「中间档」模型而非顶级模型，因为降级到前沿模型会吃掉约 80% 的节省**。

### 3.5 路径 E：自建 System One 兼容端点（内部项目的唯一可行解）

**核心事实**：开源项目 `tontoko/jev-browser` 支持把 `JEV_BASE_URL` 指向自建端点，**且不需要 TypeSafe API key**：官方说明"For a compatible local/remote System One endpoint, set only `JEV_BASE_URL` (for example `http://127.0.0.1:8765`); it must implement `POST /v1/systemone` with the same `state/questions -> model/answers/usage` envelope. **A custom endpoint does not require a Jev API key.**"

**最小契约（这就是你要实现的东西）**：

```
请求：POST /v1/systemone
{ "model": "任意你的模型名", "state": "文本 | JSON 对象 | 文本数组",
  "questions": { "<问题ID>": { "type": "choice"|"score"|"noul", "instructions": "自然语言指令",
                               "criteria": { ...选项映射 } 或 [ ...有序档位 ] } } }   // choice/score 需要 criteria
响应：
{ "model": "<你的模型名>",
  "answers": { "<问题ID>": { "type": "choice"|"score"|"noul",
      "choice": "选中的键", "score": 1.4, "noul": 0.95,   // 按 type 取其一
      "probabilities": { "<键>": 0.97 },                  // choice/score
      "confidence": 0.95 } },                             // choice/score；noul 无
  "usage": { "input_tokens": 210, "output_tokens": 31 } }
```

**后端实现方案（从易到难）**：

| 方案 | 做法 | 门槛 |
|------|------|------|
| **① 内网 LLM + 提示词约束** | 内网 LLM 输出严格 JSON，校验层做类型约束与概率归一 | 低（**但没有校准保证**） |
| **② 自托管编码器** | ModernBERT / bge 等做分类头，输出 softmax 概率 | 中（需标注数据，但可微调、可离线、可校准） |
| **③ 混合** | 分类用编码器，评分用内网 LLM + 温度缩放后校准 | 中高（效果最好） |

> [!gap] 方案 ① 的置信度不可信
> 内网 LLM **没有 Jev 的 RLCD 校准保证**。Jev「报 70% 就真的约 70% 对」是训练出来的；普通 LLM 即使输出概率数字也不具备校准性。**若用置信度做阈值门控，必须在留出集上做温度缩放之类的后校准**，否则阈值失真。

**Agent Skill（让编码 Agent 一次写对）**：不加 Skill 的 Agent 会本能地按「聊天补全」写代码，然后你去 debug 一段从一开始就不可能工作的代码。

```bash
claude plugin marketplace add typesafe-ai/skills     # Claude Code
claude plugin install typesafe@typesafe-ai
npx skills add typesafe-ai/skills --skill typesafe-ai   # 其他 Agent：Codex / Cursor / DeepSeek Harness 等
```

也可把提示词直接粘给 Agent：`Install the TypeSafe skill. If you're in Claude Code, run claude plugin marketplace add typesafe-ai/skills, then claude plugin install typesafe@typesafe-ai. If you're in another agent, run npx skills add typesafe-ai/skills --skill typesafe-ai and select your agent. Use one installation method. You can read the skill directly at https://github.com/typesafe-ai/skills/blob/main/skills/typesafe-ai/SKILL.md. Then use the TypeSafe skill when working on this project.` 注意：Skill **不是凭据**，不会让你跳过任何审批，后面仍需要有 API Key 支撑。

---

## 四、实测连通性（🔵 本机 2026-09-21）

测试环境：本机存在系统代理（`http_proxy` / `https_proxy` 指向本机回环端口）。为排除代理影响同时做两组对照——走代理，以及 `--noproxy '*'` 强制直连。

| 目标 | 走系统代理 | 强制直连（`--noproxy '*'`） |
|------|-----------|---------------------------|
| `https://typesafe.ai` | **200** / 2.45 s | **200** / **1.57 s**（IP `31.43.161.6`，Google Cloud） |
| `https://api.typesafe.ai/v1/systemone` | **405**（Method Not Allowed）/ 1.47 s | **405** / **1.71 s**（IP `100.20.85.248`，AWS） |
| `https://openrouter.ai/typesafe/jev-1.13` | **200** / 1.37 s | **200** / **0.83 s**（IP `104.18.3.115`，Cloudflare） |
| `https://docs.typesafe.ai/` | **308**（跳转，正常）/ 5.27 s | — |
| `https://console.typesafe.ai/` | **307**（跳转，正常）/ 3.35 s | — |
| `https://evals.typesafe.ai/` | **200** / 1.16 s | — |

> ✅ **结论：本机可直连 TypeSafe 全链路，不需要代理。** 直连延迟 1.5–1.7 s（跨境正常水平）；405 只说明「路径存在但 HTTP 方法不对」。

**端点可用性验证（最关键的一条实证）**——再发一个**无密钥的真实 POST**看错误形态：

```bash
curl -X POST "https://api.typesafe.ai/v1/systemone" \
  -H "Content-Type: application/json" \
  -d '{"model":"jev-latest","state":"Help! My payouts have been failing for 3 days.",
       "questions":{"is_urgent":{"type":"noul","instructions":"Does this convey urgency?"}}}'
```

实测返回：`{"detail":{"error_type":"authentication_error","message":"Must supply an API key! Check your request and try again."}}` —— **[HTTP 403]**。

> ✅ 这条证据同时证明三件事：① **端点真实存在且从国内可达**（否则会超时或 404）；② **请求体结构被接受**——已通过解析层走到鉴权层（否则是 400 参数错误）；③ **缺密钥的确切错误形态**是 `403` + `authentication_error`，**可直接写进错误处理逻辑**。

**把实测固化成健康检查脚本**（`jev_healthcheck.sh`，用法 `TYPESAFE_API_KEY=ts_xxx bash jev_healthcheck.sh`）：

```bash
#!/usr/bin/env bash
set -u
API="https://api.typesafe.ai/v1/systemone"
PROBE='{"model":"jev-latest","state":"ping","questions":{"ok":{"type":"noul","instructions":"Is this text non-empty?"}}}'

echo "== 1. 端点连通性（无密钥，期望 403 + authentication_error） =="
curl -s -m 15 -X POST "$API" -H "Content-Type: application/json" -d "$PROBE" -w "\n[HTTP %{http_code}]\n"
[ -z "${TYPESAFE_API_KEY:-}" ] && { echo "== 2. 跳过密钥验证 =="; exit 0; }

echo "== 2. 密钥有效性（期望 200 + answers.ok.noul 接近 1） =="
curl -s -m 20 -X POST "$API" -H "Authorization: Bearer $TYPESAFE_API_KEY" -H "Content-Type: application/json" -d "$PROBE" -w "\n[HTTP %{http_code}]\n"
echo "== 3. 列出账号可用模型 =="
curl -s -m 15 "https://api.typesafe.ai/v1/models" -H "Authorization: Bearer $TYPESAFE_API_KEY" -w "\n[HTTP %{http_code}]\n"
```

> 💡 值得做的原因：Jev 的**速率限制是动态调整的**（官方原话），且服务只在美国西海岸。上线前有个能区分「网络问题 / 密钥问题 / 限流问题 / 模型问题」的健康检查，比事后排查便宜得多。

**官方返回形态**（用于对照实际结果；`model` 为 `jev-1.13.0`，`usage` 为 `{"input_tokens": 392, "output_tokens": 65}`）：

| 问题 | 关键返回字段 |
|------|------------|
| `department` | `type=choice`、`choice="technical"`、`confidence=0.78`、`probabilities={technical:0.85, sales:0.0, billing:0.15}` |
| `frustration` | `type=score`、`score=1.0`、`confidence=1.0`、带 `legend`（"0/1/2" 映射档位）、`probabilities={0:0.0, 1:1.0, 2:0.0}` |
| `is_urgent` | `type=noul`、`noul=1.0`（**无 confidence**） |

## 五、常见坑与排查

| # | 坑 | 事实 | 应对 |
|---|----|------|------|
| **1** | **中文准确率**（最需注意） | 官方 `/models`："English is the primary training language... Other languages, including CJK scripts, are handled but not equally well" | 先用自己的真实内容做小样本测试；可把 `instructions` 写成英文、state 保留中文；**中文 workload 必须重新校准置信度阈值**（不能套用英文的 0.9/0.7） |
| **2** | **模型别名会漂移** | `jev-latest` → `jev-1.13.0`；`jev-preview` 当前也指向 `jev-1.13.0`（无 preview 构建） | 把响应里的 `model` 字段记进日志；**做阈值门控的系统必须钉版本** |
| **3** | **上下文口径有三套数字** | 官方 64k（state+最长问题 32k）／OpenRouter 32k／早期文章 32k 与 64k 不一 | **按最小的 32k 设计**；注意 64k 是「state + 所有问题合计」、32k 是「state + 单个最长问题」，两个约束不同 |
| **4** | **速率限制是动态的** | 官方："Rate limits are adjusting dynamically... can change without notice"；当前 250,000 token/秒、1,200 请求/分钟，超限 `429` | 官方 SDK 默认退避重试并遵循 `retry-after`；**直接调 HTTP 要自己处理** |
| **5** | **输出免费 ≠ 没成本** | 输出免费是架构结果（无自回归生成）；成本全在输入侧（state + 所有问题的 instructions 与 criteria） | 别把 255 个选项的 criteria 写太长；**批量调用比「每问题一次调用」便宜 12.2 倍、快 10.0 倍**（文档型负载，答案不变），**能合并就合并** |
| **6** | **不能在你的数据上微调** | 官方："Jev is **not fine-tuned or LoRA-adapted with customer data**... the same weights serve every account" | 好消息=数据不会被训进模型（另有 ZDR 条款）；坏消息=**领域语义只能靠 state + instructions/criteria 设计解决** |
| **7** | **无本地化承诺** | 部署在**美国西海岸**；无自托管、无权重、无参数、无架构论文；有 DPA/隐私政策/企业 ZDR，但**没有中国区节点** | 内部项目**不能直接使用**，走 3.5 自建兼容端点 |

**失败模式 → 排查动作**：

| 现象 | 可能原因 | 先查什么 |
|------|---------|---------|
| 连接超时 / 无响应 | 网络问题或端点不可达 | 先跑健康检查第 1 步（期望 403）；同时核对 `--noproxy` 直连 |
| `403` + `authentication_error` | 缺密钥或密钥无效 | 检查 `TYPESAFE_API_KEY` 是否为 `ts_...` 且未过期 |
| `400` 参数错误 | 请求体结构不对 | 核对 choice/score 是否给了 `criteria`、type 拼写（`noul` 不是 `bool`） |
| `405` | 用了 GET 打端点 | 决策端点是 `POST`；`GET /v1/models` 才是列表 |
| `429` | 触发动态速率限制 | 读 `retry-after` 加退避；或合并成批量调用 |
| 答案不符预期但有值 | CJK 语言准确率问题（坑 1） | 小样本复测 + 重新校准阈值；把 instructions 改英文再试一次 |
| 昨天好好的今天变了 | 别名漂移（坑 2） | 看响应 `model` 字段；把模型钉到 `jev-1.13.0` |
| 阈值失灵 | 路径切换导致上下文口径变小（坑 3，如切 OpenRouter 的 32k） | 核对实际路径的上下文上限 |

## 六、落地判断（对测试开发）

| 建议 | 做法 |
|------|------|
| **① 用 $5 额度做「可行性探针」** | 挑一个真实高频判断（如失败分诊），用真实数据跑 100–200 条，记录准确率、置信度分布、**高置信是否真的更准** |
| **② 用 `/model-jaggedness/jev-1.13` 当测试用例清单** | 那 9 条缺陷（字面理解／不会计数／日期当文本／多跳掉分／context rot／**不防注入**／指令矛盾／不变量不成立／不能生成）**本身就是 9 条现成的 AI 组件测试用例** |
| **③ 把健康检查脚本固化** | 用第四章的脚本进日常自检——尤其因为**速率限制是动态的** |

**内部项目合规判定链**：无自托管（无权重/参数/架构论文）→ 不可离线部署（仅托管 API）→ 服务在美国西海岸 → 不可用客户数据微调（同一套权重服务所有账号）→ **结论：数据会出境，不满足「代码与数据不出内网」要求**。**三条可落地路径（按推荐度）**：① **借接口契约（最强）**——内网实现同款 `POST /v1/systemone`，`tontoko/jev-browser` 原生支持 `JEV_BASE_URL` 且不需 Jev key，整套生态工具立刻可用；② **借架构，换模型**——自托管编码器实现 Choice/Noul + 温度缩放后校准；③ **只借方法论**——抄「原子化问题 + 代码里组合 + 置信度三段式路由 + 逐项问再汇总」，零成本。**学习路径（5 天）**：Day1 官网四页精读 + Playground 跑通第一条 Noul；Day2 Python SDK 接真实小场景并做一次校准检查；Day3 把 9 条缺陷变成 9 条测试用例；Day4 装 Agent Skill 让编码 Agent 写完整小工具；Day5 写 1 页评估报告（能做什么／不能做什么／阈值怎么定／成本多少）。

> [!key-insight] 面试时最有说服力的说法
> 不是「我知道 Jev 很快很便宜」，而是：「我用它跑了自己的 N 条真实样本，准确率 X%，**但它的置信度在中文场景下需要重新校准**——我实测发现报 0.9 的那些只有约 Y% 是对的。所以我把它定位成**过滤器而不是裁判**，并用 `inconclusive` 状态兜住低置信情形。」

## 附录：不可靠来源识别

| 说法 | 判定 | 理由 |
|------|------|------|
| 「TypeSafe 候补对大陆邮箱**审核通过率超 87%**，平均等待 **3.2 小时**」 | ❌ **不可信** | 官方从未公布通过率或等待时长；09-21 起候补已取消（信息过时）；数字精确到小数却无出处 |
| 「**APUS 开源**的本地 Jev 复现版 `jev-ultrafast` 已适配国产显卡驱动」 | ❌ **事实错误** | `jev-ultrafast` 由 **browser-use** 团队创建（2026-09-16），与 APUS 无关 |
| 「OpenRouter 可通过**微信快捷登录**」；「Vercel AI Gateway 免费促销**有效期至 09-25**」 | ⚠️ **需自行核实** | 微信登录类说法多见于中文 SEO 稿，以 `openrouter.ai` 实际注册页为准；促销期限时效极强，且只见于单一来源 |

**通用识别方法**：① 有没有出处（官方文档/博客/X 是硬来源）；② 数字是否过于精确而无出处；③ 是否与官方明文冲突（如「适配国产显卡」与「仅托管 API、无权重」直接冲突）；④ 时效（候补、促销、限额可能一天一变）。

> [!gap] 本文自身的时效风险
> Jev 处于早期访问阶段，**价格、速率限制、模型版本、别名指向、通道可用性均可能变化**。落地前请以 `docs.typesafe.ai` 当期版本为准。脚本中密钥位置均为占位符，**切勿把真实密钥写入仓库或提交到版本控制**。

## 🔗 关联文档

- [[wiki/AI相关学习资料/Jev决策模型(System One)学习参考资料|Jev 决策模型（System One）学习参考资料]] — 前置阅读：System One / 三种原语 / 置信度的原理底稿，本页只讲怎么连
- [[wiki/AI相关学习资料/Jev用于UI自动化测试可行性分析与AI测试工具横向对比|Jev 用于 UI 自动化测试可行性分析与横向对比]] — 前置阅读：把本文的接入能力落到 UI 自动化与工具选型结论上
- [[wiki/AI相关学习资料/测试开发如何使用DSH|测试开发如何使用 DSH]] — 3.5 的 Agent Skill 安装命令同样覆盖 DeepSeek Harness 等编码 Agent
- [[wiki/AI相关学习资料/AI产品测试进阶路线与面试考点|AI 产品测试进阶路线与面试考点]] — 第六章的 5 天学习路径与「校准/阈值」话术对应的面试考点框架
- [[wiki/AI相关学习资料/index|AI 相关学习资料索引]] — 本页所属分类

## 源文件

- `.raw/AI相关学习资料/jev/TypeSafe_Jev国内使用指南(官网导航+四条接入路径+实测连通性).md`
