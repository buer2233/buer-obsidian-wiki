# TypeSafe Jev 国内使用指南：官网导航 + 四条接入路径 + 实测连通性

> **阅读对象**：测试开发工程师（SDET）/ AI 测试方向求职者
> **前置阅读**：《Jev 决策模型（System One）学习参考资料.md》《Jev 用于 UI 自动化测试可行性分析与 AI 测试工具横向对比.md》（同目录）
> **撰写日期**：2026-09-21
> **在线检索日期**：2026-09-21
> **本机实测日期**：2026-09-21（Windows 中文环境，含走代理与直连两组对照）
> **信息来源分级**：🟢 官方一手｜🟡 第三方实测｜🔵 **本机实测**｜🔴 不可靠/过时来源（已标注）

---

## 目录

- [第零章 结论速览](#第零章-结论速览)
- [第一章 官网与官方入口全图](#第一章-官网与官方入口全图)
- [第二章 本机实测：国内能不能连上](#第二章-本机实测国内能不能连上)
- [第三章 官方账号开通流程（已无需候补）](#第三章-官方账号开通流程已无需候补)
- [第四章 国内可用的四条接入路径](#第四章-国内可用的四条接入路径)
- [第五章 三分钟跑通：cURL → Python → Agent Skill](#第五章-三分钟跑通curl--python--agent-skill)
- [第六章 国内使用的七个坑](#第六章-国内使用的七个坑)
- [第七章 对测试开发的实际建议](#第七章-对测试开发的实际建议)
- [附录 A 不可靠来源识别](#附录-a-不可靠来源识别)
- [附录 B 参考资料](#附录-b-参考资料)

---

## 第零章 结论速览

| 问题 | 结论 |
|------|------|
| **官网** | `https://typesafe.ai`（已实测 HTTP 200） |
| **文档** | `https://docs.typesafe.ai`（已实测 308 跳转，可达） |
| **控制台 / 注册 / API Key** | `https://console.typesafe.ai`（已实测 307 跳转，可达） |
| **API 端点** | `POST https://api.typesafe.ai/v1/systemone`（已实测 **405 存在** + 无密钥 **403 认证错误**） |
| **国内能连上吗** | ✅ **能。走系统代理和直连都通。** 本机直连 `typesafe.ai` **1.57s**、`api.typesafe.ai` **1.71s** |
| **还需要候补名单吗** | ❌ **不需要**。2026-09-21 官方已全面开放，注册即送 **$5 额度（约 1.2 亿 token）** |
| **最省事的国内路径** | **官方直连**（64k 上下文、SDK 最全）；备选 **OpenRouter**（无需海外卡） |
| **最大的国内坑** | ⚠️ **Jev 以英文为主要训练语言，CJK 语言"能处理但准确率不等同"**（官方原话）——**中文场景必须自己先测** |
| **最大的合规坑** | ⚠️ 仅托管 API + 服务在美国西海岸 + **不接受客户数据微调** → 内部项目仍不能直接使用（见 7.2） |

---

## 第一章 官网与官方入口全图

```
TypeSafe AI 官网矩阵
│
├── https://typesafe.ai/                       官网首页（含 193.6x / 444.6x 宣传数字）
│   └── /blog/introducing-system-one-models-and-jev   ← 发布博客（技术细节最全的一篇）
│
├── https://docs.typesafe.ai/                  官方文档（最重要，逢事以这里为准）
│   ├── /introduction                          总览：三个原语
│   ├── /introduction/quickstart               ★ 快速开始（Playground → API → SDK → Skill）
│   ├── /introduction/machine-learning-primer  AI 基础：为什么训练"校准决策"
│   ├── /concepts/system-one                   System One 概念
│   ├── /concepts/state                        state 的写法与支持形状
│   ├── /concepts/how-to-build-with-system-one 如何用 System One 构建
│   ├── /primitives                            ★ 三种原语（Choice / Score / Noul）
│   ├── /primitives/advanced                   高级：嵌套结构
│   ├── /patterns                              ★ 四个架构模式
│   │   ├── /fan-out                           推测性扇出
│   │   ├── /confidence-routing                置信度门控路由
│   │   ├── /composite-scoring                 复合评分
│   │   └── /intent-routing                    意图路由
│   ├── /confidence                            ★ 置信度的定义、近似公式、三段式路由
│   ├── /models                                ★ 模型 ID、别名、价格、速率限制、上下文
│   ├── /model-jaggedness/jev-1.13             ★★ 官方自曝的 9 条缺陷（必读）
│   ├── /api                                   HTTP API 参考（含速率限制处理）
│   ├── /sdk                                   Python / JavaScript SDK
│   ├── /agent-skill                           ★ 给 Claude Code / Codex 的 Agent Skill
│   ├── /cookbooks/…                           现成配方（护栏、RAG 段落筛选、引用核查等）
│   └── /legal                                 DPA、隐私政策、企业零数据保留（ZDR）
│
├── https://console.typesafe.ai/               控制台
│   ├── /playground                            ★ Playground：直接粘 state、加问题、看结果
│   └── /keys                                  ★ 创建 / 管理 API Key
│
├── https://evals.typesafe.ai/                 工作流评测站（含完整查询与分歧点）
│
├── https://api.typesafe.ai/v1/systemone       唯一 API 端点（决策）
│   └── /v1/models                             列出账号可用模型（GET）
│
└── GitHub 官方组织
    ├── typesafe-ai/system-one-adapter-python  ★ 把任意 LLM 包成同一接口（对自建极有用）
    └── typesafe-ai/skills                     ★ Agent Skill 源码（含 SKILL.md）
```

**四个"必读"页面的优先级**（这是官方文档里信息密度最高的四页）：

| 优先级 | 页面 | 为什么 |
|--------|------|--------|
| **1** | `/model-jaggedness/jev-1.13` | **官方自曝的 9 条缺陷**。几乎所有发布报道都没走过这一页，而它决定了你能不能上线 |
| **2** | `/models` | 模型 ID、**别名会漂移**、价格、**速率限制是动态的**、上下文口径 |
| **3** | `/confidence` | 置信度怎么算、Noul 为什么没有 confidence、**三段式路由**、阈值随风险分级 |
| **4** | `/introduction/quickstart` | 四条上手路径（Playground / API / SDK / Agent Skill） |

---

## 第二章 本机实测：国内能不能连上

> 🔵 **以下全部为本机 2026-09-21 实测结果**，非检索所得，非推测。

### 2.1 测试环境

本机存在一个系统代理（`http_proxy` / `https_proxy` 指向本机回环端口）。为排除代理的影响，**同时做了两组对照**：走代理，以及 `--noproxy '*'` 强制直连。

### 2.2 结果一：走系统代理

| 目标 | HTTP 状态 | 耗时 |
|------|----------|------|
| `https://typesafe.ai` | **200** | 2.45 s |
| `https://docs.typesafe.ai/` | **308**（跳转，正常） | 5.27 s |
| `https://console.typesafe.ai/` | **307**（跳转，正常） | 3.35 s |
| `https://api.typesafe.ai/v1/systemone` | **405**（Method Not Allowed） | 1.47 s |
| `https://openrouter.ai/typesafe/jev-1.13` | **200** | 1.37 s |
| `https://evals.typesafe.ai/` | **200** | 1.16 s |

### 2.3 结果二：强制直连（`--noproxy '*'`）

| 目标 | HTTP 状态 | 耗时 | 直连 IP | 归属 |
|------|----------|------|---------|------|
| `https://typesafe.ai` | **200** | **1.57 s** | `31.43.161.6` | Google Cloud |
| `https://api.typesafe.ai/v1/systemone` | **405** | **1.71 s** | `100.20.85.248` | AWS |
| `https://openrouter.ai/typesafe/jev-1.13` | **200** | **0.83 s** | `104.18.3.115` | Cloudflare |

> ✅ **结论：本机可以直连 TypeSafe 全链路，不需要代理。** 直连延迟 1.5–1.7 s（跨境正常水平）。

### 2.4 结果三：端点可用性验证（最关键的一条实证）

光看到 405 只能说明"路径存在但方法不对"。所以再发一个**无密钥的真实 POST**，看错误形态：

```bash
curl -X POST "https://api.typesafe.ai/v1/systemone" \
  -H "Content-Type: application/json" \
  -d '{"model":"jev-latest","state":"Help! My payouts have been failing for 3 days.",
       "questions":{"is_urgent":{"type":"noul","instructions":"Does this convey urgency?"}}}'
```

**实测返回**：

```json
{"detail":{"error_type":"authentication_error",
           "message":"Must supply an API key! Check your request and try again."}}

[HTTP 403]
```

> ✅ **这条证据同时证明了三件事**：
> 1. **端点真实存在且从国内可达**（否则会是超时或 404）
> 2. **请求体结构被接受**——请求已经通过了解析层，走到了鉴权层（否则会是 400 参数错误）
> 3. **缺密钥时的确切错误形态**是 `403` + `authentication_error`——**这可以直接写进你的错误处理逻辑**

### 2.5 把这条实测变成一个健康检查脚本

既然连通性可用，可以把它固化成一个小脚本，放进 CI 或本地自检：

```bash
#!/usr/bin/env bash
# jev_healthcheck.sh —— 检查 TypeSafe 连通性与密钥有效性
# 用法: TYPESAFE_API_KEY=ts_xxx bash jev_healthcheck.sh

set -u
API="https://api.typesafe.ai/v1/systemone"

echo "== 1. 端点连通性（无密钥，期望 403 + authentication_error） =="
code=$(curl -s -o /tmp/jev_probe.json -w "%{http_code}" -m 15 \
  -X POST "$API" -H "Content-Type: application/json" \
  -d '{"model":"jev-latest","state":"ping","questions":{"ok":{"type":"noul","instructions":"Is this text non-empty?"}}}')
echo "HTTP $code"
cat /tmp/jev_probe.json; echo

if [ -z "${TYPESAFE_API_KEY:-}" ]; then
  echo
  echo "== 2. 跳过密钥验证（未设置 TYPESAFE_API_KEY） =="
  exit 0
fi

echo
echo "== 2. 密钥有效性（期望 200 + answers.ok.noul 接近 1） =="
curl -s -m 20 -X POST "$API" \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"jev-latest","state":"ping","questions":{"ok":{"type":"noul","instructions":"Is this text non-empty?"}}}' \
  -w "\n[HTTP %{http_code}]\n"

echo
echo "== 3. 列出账号可用模型 =="
curl -s -m 15 "https://api.typesafe.ai/v1/models" \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" -w "\n[HTTP %{http_code}]\n"
```

> 💡 **为什么值得做**：Jev 的**速率限制是"动态调整"的**（官方原话），且服务目前只在美国西海岸。上线前有一个能区分"网络问题 / 密钥问题 / 限流问题 / 模型问题"的健康检查，比事后排查便宜得多。

---

## 第三章 官方账号开通流程（已无需候补）

### 3.1 状态变化：候补名单已在 2026-09-21 取消

```
2026-09-15  Jev 发布，进入 early access，需候补
            · TypeSafe 称首 36 小时清理了约 14 万个注册
            · 官方表态"尽快把开发者从候补名单里放出来"
2026-09-16~20  生态爆发（1200+ 仓库），API 一度被打爆
2026-09-21  ★ 全面开放：无候补名单，所有注册用户送 $5 额度（约 1.2 亿 token）
```

> ⚠️ **注意时效**：如果你看到的中文教程还在讲"候补通道""排队""只能走第三方"——**那是 09-15 到 09-20 之间的过时信息**。

### 3.2 开通四步

| 步骤 | 操作 | 地址 |
|------|------|------|
| **1. 注册** | 打开控制台注册账号 | `https://console.typesafe.ai` |
| **2. 试玩（强烈建议先做这个）** | 进 Playground，**粘一段你自己的文本**作为 state，加一条 Noul 问题，看返回 | `https://console.typesafe.ai/playground` |
| **3. 建 Key** | 创建 API Key（**通常只显示一次，立即保存**） | `https://console.typesafe.ai/keys` |
| **4. 配置环境变量** | `export TYPESAFE_API_KEY="ts_..."` | SDK 默认读这个变量 |

**官方文档给的第一个 Playground 示例**（可以直接照抄来验证账号是否正常）：

```jsonc
// state（随便粘一段真实文本，建议用你自己的工作内容而不是官方示例）
"Hi, I've been trying to connect my Stripe account for 3 days and the
 integration keeps failing. I'm losing sales. Please help ASAP."

// questions
{
  "urgency": {
    "type": "noul",
    "instructions": "Does this message express urgency?"
  }
}
```

### 3.3 在控制台里能做什么

从官方 console 的实际界面来看，至少有这些区块：

- **Playground** —— 粘贴 state、加问题、实时看三类答案与概率
- **API Keys** —— 创建 / 管理密钥
- **Usage** —— 用量（官方标注 "Stats may be delayed"）
- **Documentation** —— 文档入口
- **Legal / Trust Center** —— 数据政策、企业零数据保留（ZDR）
- **Discord** —— 官方社区

### 3.4 关于付款

- **$5 免费额度**：约 **1.2 亿输入 token**。按官方定价（$0.042/百万输入 token、输出免费）反推吻合。
- ⚠️ **这个换算不能直接类比 LLM 用量**：Jev 的一次调用返回的是**极小的类型化结果**，输入侧通常也只是紧凑的 state，**与"120 亿 token 的 GPT 调用"不是同一种工作量**。
- 后续充值与付款：官方需要海外支付方式；**如果不想绑海外卡，走 OpenRouter（见 4.2）**。
- **企业/更高限额**：官方指向 `sales@typesafe.ai`（文档里明确写了"自定义与企业计划有更高限额"）。

---

## 第四章 国内可用的四条接入路径

### 4.0 四条路径总览

| 路径 | 国内可达性 | 需要海外卡 | 上下文口径 | 支持的客户端语言 | 有无控制台 | 推荐度 |
|------|-----------|-----------|-----------|----------------|-----------|--------|
| **A. 官方直连** | ✅ **实测直连 1.71s** | 后续充值需要 | **64k**（state+问题 32k） | **全部**（HTTP） | ✅ 有 | ⭐⭐⭐⭐⭐ |
| **B. OpenRouter** | ✅ **实测直连 0.83s** | ❌ 不需要（可微信登录） | **32k**（⚠️ 口径更小） | JS SDK / HTTP | ❌ 无（用 OR 的） | ⭐⭐⭐⭐ |
| **C. Vercel AI Gateway** | ✅ 可达 | ⚠️ 需绑卡验证 | 以官方为准 | ⚠️ **仅 AI SDK** | ❌ 无 | ⭐⭐⭐ |
| **D. Cloudflare AI Gateway / LiteLLM / Composio** | ✅ 可达 | 视产品而定 | 以官方为准 | 视产品而定 | ❌ 无 | ⭐⭐⭐ |
| **E. 自建兼容端点** | ✅ **完全不出网** | ❌ 不需要 | 自己定 | **全部** | 自己建 | ⭐⭐⭐⭐⭐（合规场景） |

---

### 4.1 路径 A：官方直连（推荐）

**优点**：上下文最大（64k）、SDK 最完整、有控制台可看用量与限额、**延迟最少一跳**（官方端到端 70–500ms，少一跳很重要）。

**做法**：

```bash
# 1. 配置密钥
export TYPESAFE_API_KEY="ts_..."

# 2. 直接调（本机实测可直连，无需代理）
curl -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jev-latest",
    "state": "你的文本或 JSON 状态",
    "questions": {
      "department": {
        "type": "choice",
        "instructions": "Which team should handle this",
        "criteria": {
          "billing": "Payment or subscription issues",
          "technical": "Bugs or integration problems",
          "sales": "Pricing or account questions"
        }
      }
    }
  }'
```

> ⚠️ **如果直连在你的网络下不稳定**，可以显式走代理：
> ```bash
> curl -x http://127.0.0.1:<你的端口> ...
> ```
> 但**不要**在代码里硬编码代理——用环境变量，并在 CI 里留一个开关。

---

### 4.2 路径 B：OpenRouter（不需要海外卡，最省事）

**为什么推荐**：`openrouter.ai` 已上线 Jev，**无需候补、注册门槛低**，本机实测直连 **0.83 s**（走 Cloudflare，比官方还快）。

**模型 ID**：

```
typesafe/jev-1.13            当前版本
typesafe/jev-1.13-20260917   带日期的构建
typesafe/jev-latest          跟踪最新
```

**⚠️ 最大的坑：它不在 chat completions 端点上**

OpenRouter 为 Jev 提供的是**独立的 Decisions API**，**不是** OpenAI 兼容的 `/chat/completions`：

```
POST https://openrouter.ai/api/alpha/decisions
Authorization: Bearer $OPENROUTER_API_KEY
Content-Type: application/json
```

> 官方对 OpenRouter 页面的说明原文：
> "It runs on the OpenRouter **Decisions API** rather than the OpenAI-compatible chat endpoint, so the request and response shapes below are specific to structured decisions — **chat completions SDKs will not work with it.**"

**含义**：**你不能把一个 OpenAI 客户端指向 OpenRouter 的 base URL 就来用 Jev。** 必须走 `alpha.decisions` 这个接口形态。

**JavaScript 示例（官方给出）**：

```javascript
import { OpenRouter } from "@openrouter/sdk";

const openrouter = new OpenRouter({ apiKey: process.env.OPENROUTER_API_KEY });

const decision = await openrouter.alpha.decisions.create({
  decisionsRequest: {
    model: "typesafe/jev-1.13",
    state: "Help! My payouts have been failing for 3 days.",
    questions: {
      is_urgent: {
        type: "noul",
        instructions: "Does this message convey urgency?",
        criteria: { true: "Explicitly time-sensitive", false: "No urgency expressed" },
      },
      department: {
        type: "choice",
        instructions: "Which team should handle this?",
        criteria: {
          billing:   "Payments, invoicing, refunds",
          technical: "Bugs, outages, integrations",
          sales:     "Pricing, upgrades, new accounts",
        },
      },
      frustration: {
        type: "score",
        instructions: "How frustrated is the customer?",
        criteria: ["Calm", "Frustrated", "Very angry"],
      },
    },
  },
});

const { is_urgent, department, frustration } = decision.answers;
if (is_urgent.noul > 0.8 && department.choice === "billing") {
  // escalateToBilling(...)
}
```

**另外两个 OpenRouter 侧的注意点**：

1. **上下文只有 32k**（官方直连是 64k）。**大批量 state 的工作负载迁移前必须核对这个天花板。**
2. **Jev 不出现在 OpenRouter 的公开模型列表 API 里** —— 任何"枚举模型列表来生成选择器"的工具都看不到它。

---

### 4.3 路径 C：Vercel AI Gateway

**优点**：模型 ID 是 `typesafe-ai/jev`，接入一行改动。

**⚠️ 关键限制**：Vercel 的评测文档明确说明——**评测能力只通过 AI SDK 提供，Gateway 的 OpenAI 兼容 / Anthropic 兼容 / Cohere 兼容端点都到不了 Jev**。

> 这意味着：**如果你的服务是通过"把 OpenAI 客户端指向 Gateway base URL"来接入的，那个客户端访问不了 Jev。** 必须在链路里引入 AI SDK。
> 这直接排除了 Go / Rails / 任何走 OpenAI 形态 SDK 的服务。

**TypeScript 项目（AI SDK 已在用的话，就是改一行模型名）**：

```javascript
import { experimental_evaluate as evaluate } from "ai";

const result = await evaluate({
  model: "typesafe-ai/jev",
  state: "你的上下文内容...",
  questions: {
    // 定义你的问题
  },
});
```

**生产环境的额外注意点**：Gateway key 是唯一的凭据，所以 **你拿不到 TypeSafe 控制台、看不到按 key 的用量、也看不到自己离 Jev 自身限额（25 万 token/秒、1200 请求/分钟）还有多远**。而那两个数字本身还是动态的。**如果量级重要，自己记请求数。**

---

### 4.4 路径 D：Cloudflare AI Gateway / LiteLLM / Composio

| 通道 | 形态 | 适合谁 |
|------|------|--------|
| **Cloudflare AI Gateway** | 控制台左侧 `AI` → `AI Gateway` 下可选 Jev | 已经在用 Cloudflare 的团队 |
| **LiteLLM** | 复杂度路由器可选 Jev 判断请求该走哪个模型档位 | 已用 LiteLLM 统管模型的团队 |
| **Composio** | Jev toolkit，2 个工具（`Evaluate State` / `List Models`） | 用 Composio 编排 Agent 的团队 |
| **new-api 插件** | 给自建 LLM 网关加原生 `/v1/systemone` 端点 | 自建网关、想把"决策"和"对话"放在同一个网关后面 |

**LiteLLM 那条值得单独提**：有回测显示 237 个真实回合成本降约 **60%**；并且发现一个反直觉的结论——**置信度低于 0.5 时应该降级到"中间档"模型而不是顶级模型，因为降级到前沿模型会吃掉约 80% 的节省**。

---

### 4.5 路径 E：自建 System One 兼容端点（**内部项目的唯一可行解**）

对"代码与数据不出内网"的场景，前面四条全部不可用。但有一条**很干净的替代路径**：

**核心事实**：开源项目 `tontoko/jev-browser` 明确支持把 `JEV_BASE_URL` 指向自建端点，**且不需要 TypeSafe API key**：

> "For a compatible local/remote System One endpoint, set only `JEV_BASE_URL` (for example `http://127.0.0.1:8765`); it must implement `POST /v1/systemone` with the same `state/questions -> model/answers/usage` envelope. **A custom endpoint does not require a Jev API key.**"

**含义**：你只要在内网实现一个**遵循同款契约**的 `POST /v1/systemone`，就能**复用整套 Jev 生态工具**（jev-browser 的 MCP / CLI / SDK 等），而数据一步都不出网。

**最小契约（这就是你要实现的东西）**：

```
请求：
POST /v1/systemone
{
  "model":   "任意你的模型名",
  "state":   "文本 | JSON 对象 | 文本数组",
  "questions": {
    "<问题ID>": {
      "type":         "choice" | "score" | "noul",
      "instructions": "自然语言指令",
      "criteria":     { ...选项映射 } 或 [ ...有序档位 ]     // choice/score 需要
    }
  }
}

响应：
{
  "model": "<你的模型名>",
  "answers": {
    "<问题ID>": {
      "type":          "choice" | "score" | "noul",
      "choice":        "选中的键",                    // type=choice
      "score":         1.4,                          // type=score
      "noul":          0.95,                         // type=noul
      "probabilities": { "<键>": 0.97, ... },        // choice/score
      "confidence":    0.95                          // choice/score；noul 无
    }
  },
  "usage": { "input_tokens": 210, "output_tokens": 31 }
}
```

**怎么实现这个后端**（从易到难）：

| 方案 | 做法 | 门槛 |
|------|------|------|
| **① 内网 LLM + 提示词约束** | 用内网可用的 LLM，让它输出严格 JSON，再在校验层做类型约束与概率归一 | 低（**但没有校准保证**） |
| **② 自托管编码器** | ModernBERT / bge 等做分类头，输出 softmax 概率 | 中（需要标注数据，但**可以自己微调、可离线、可校准**） |
| **③ 混合** | 分类用编码器，评分用内网 LLM + 温度缩放后校准 | 中高（效果最好） |

> ⚠️ **必须说清楚一个差别**：方案 ① 里的内网 LLM **没有 Jev 的 RLCD 校准保证**。Jev 的"报 70% 就真的约 70% 对"是训练出来的，普通 LLM 即使输出一个概率数字，也**不具备校准性**。所以如果你要用置信度做阈值门控，**必须自己在留出集上做温度缩放之类的后校准**，否则阈值会失真。

---

## 第五章 三分钟跑通：cURL → Python → Agent Skill

### 5.1 第一步：cURL（验证账号可用）

```bash
export TYPESAFE_API_KEY="ts_..."

curl -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{
  "state": "Hi, I've been trying to connect my Stripe account for 3 days and the integration keeps failing. I'm losing sales. Please help ASAP.",
  "model": "jev-latest",
  "questions": {
    "department": {
      "type": "choice",
      "instructions": "Which team should handle this",
      "criteria": {
        "billing": "Payment or subscription issues",
        "technical": "Bugs or integration problems",
        "sales": "Pricing or account questions"
      }
    },
    "frustration": {
      "type": "score",
      "instructions": "How frustrated the customer appears",
      "criteria": ["Calm, just stating facts", "Frustrated but civil", "Very angry, strong language"]
    },
    "is_urgent": {
      "type": "noul",
      "instructions": "The message conveys urgency or time-sensitivity"
    }
  }
}
EOF
```

**官方文档给出的返回形态**（可以用来对照你的实际结果）：

```jsonc
{
  "model": "jev-1.13.0",
  "answers": {
    "department": {
      "type": "choice", "choice": "technical", "confidence": 0.78,
      "probabilities": { "technical": 0.85, "sales": 0.0, "billing": 0.15 }
    },
    "frustration": {
      "type": "score", "score": 1.0, "confidence": 1.0,
      "legend": { "0": "Calm, just stating facts", "1": "Frustrated but civil", "2": "Very angry, strong language" },
      "probabilities": { "0": 0.0, "1": 1.0, "2": 0.0 }
    },
    "is_urgent": { "type": "noul", "noul": 1.0 }
  },
  "usage": { "input_tokens": 392, "output_tokens": 65 }
}
```

### 5.2 第二步：Python SDK

```bash
pip install typesafe-sdk      # 需要 Python >= 3.10
# 或
uv add typesafe-sdk
```

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

client = TypeSafeClient()     # 从环境变量 TYPESAFE_API_KEY 读取密钥，默认模型 jev-latest

ticket = ("Hi, I've been trying to connect my Stripe account for 3 days "
          "and the integration keeps failing. I'm losing sales. Please help ASAP.")

response = client.system_one(
    state=ticket,
    questions={
        "department": Choice(
            instructions="Which team should handle this",
            criteria={
                "billing":   "Payment or subscription issues",
                "technical": "Bugs or integration problems",
                "sales":     "Pricing or account questions",
            },
        ),
        "frustration": Score(
            instructions="How frustrated the customer appears",
            criteria=["Calm, just stating facts",
                      "Frustrated but civil",
                      "Very angry, strong language"],
        ),
        "is_urgent": Noul(
            instructions="The message conveys urgency or time-sensitivity",
        ),
    },
)

print(response.answers["department"].choice)    # "technical"
print(response.answers["frustration"].score)    # 1.0
print(response.answers["is_urgent"].noul)       # 1.0
```

**如果要显式走代理**（部分网络环境下可能需要）：

```python
import os
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:<端口>"
# 然后照常使用 TypeSafeClient()
```

> 💡 **生产建议**：**把模型钉死在版本号上**（`TypeSafeClient(model="jev-1.13.0")`），不要用 `jev-latest`。官方文档明确提醒："An alias moves when a new release ships, so the answers behind it can change without a change on your side. **If you have tuned confidence thresholds against a specific version, pin that version's ID.**"

### 5.3 第三步：Agent Skill（让编码 Agent 一次写对）

这一步**很关键**，因为不加 Skill 的 Agent 会本能地按"聊天补全"去写代码，然后你去 debug 一段从一开始就不可能工作的代码。

```bash
# Claude Code
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai

# 其他 Agent（Codex / Cursor / DeepSeek Harness 等）
npx skills add typesafe-ai/skills --skill typesafe-ai
```

也可以直接让 Agent 自己装（把这段提示词粘给 Agent）：

```
Install the TypeSafe skill. If you're in Claude Code, run `claude plugin marketplace add typesafe-ai/skills`,
then `claude plugin install typesafe@typesafe-ai`. If you're in another agent, run
`npx skills add typesafe-ai/skills --skill typesafe-ai` and select your agent. Use one installation method.
You can read the skill directly at
https://github.com/typesafe-ai/skills/blob/main/skills/typesafe-ai/SKILL.md
Then use the TypeSafe skill when working on this project.
```

**注意**：Skill **不是凭据**，它不会让你跳过任何审批，后面仍然需要有 API Key 支撑。

---

## 第六章 国内使用的七个坑

### 坑 1：⚠️ **中文准确率——最需要国内用户注意的一条**

官方 `/models` 页面原文：

> "**English is the primary training language and where accuracy is currently best. Other languages, including CJK scripts, are handled but not equally well; test on your own content before relying on Jev for a non-English workload**, and pay close attention to Confidence when routing."

第三方交叉验证也得出一致结论：**中文结果不稳，英文短文本才稳定**。

**所以**：
- 如果 state 和 instructions 都是中文 → **必须先用自己的真实内容做小样本测试**，别直接上生产
- **一个实用的缓解办法**：把 `instructions` 写成英文（问题定义用英文，通常比 state 用英文更可行），state 保留中文原文
- 所有中文 workload 都要**重新校准置信度阈值**，不能套用英文场景的 0.9 / 0.7

### 坑 2：模型别名会漂移

`jev-latest` → `jev-1.13.0`，`jev-preview` → 目前也指向 `jev-1.13.0`（**当前没有 preview 构建**）。

**别名一发新版本就换，你这边什么都不改，答案就变了。** 响应里的 `model` 字段会告诉你这次是哪个版本答的，**建议把它记进日志**。

**做阈值门控的系统必须钉版本。**

### 坑 3：上下文口径有三套数字

| 来源 | 口径 |
|------|------|
| 官方 docs `/models` | **每请求 64k**；其中 `state` + 最长问题 **32k** |
| OpenRouter 模型页 | **32k** |
| 早期第三方文章 | 有写 32k 的，有写 64k 的 |

**按最小的那个设计**（32k），**并且注意 64k 是"state + 所有问题合计"、32k 是"state + 单个最长问题"**——这两个约束不同，不要混。

### 坑 4：速率限制是动态的

官方原话：

> "**Rate limits are adjusting dynamically.** We are serving a very large volume of demand, and the limits above **can change without notice** while we do, as upcoming large GPU deals land and we let in more users."

当前数字：**250,000 token/秒、1,200 请求/分钟**，超限返回 `429`。**官方 SDK 默认带退避重试，并会遵循 `retry-after` 头**；如果你直接调 HTTP，要自己处理。

### 坑 5：输出免费，但"免费"不等于"没成本"

- **输出 token 免费**是架构结果（没有自回归生成），不是促销。
- 但**成本全在输入侧**。而 Jev 的输入包括 **state + 所有问题的 instructions 与 criteria**。
- **一个常见浪费**：把 255 个选项的 criteria 写得很长。官方提示"每个选项只花几个 token"，但 255 × 长描述会显著推高输入量。
- **省钱的正确姿势**：官方测量显示，**批量调用比"每个问题一次调用"便宜 12.2 倍、快 10.0 倍**（文档为主的工作负载），答案不变。**能合并就合并。**

### 坑 6：不能在你的数据上微调

官方 `/models` 明文：

> "Jev is **not fine-tuned or LoRA-adapted with customer data**. It is trained with RLCD to return calibrated decisions, and **the same weights serve every account**."

**含义**：
- ✅ 好消息：**你的数据不会被训进模型**——官方另有说明"Jev is not trained on customer requests or responses"，企业客户另有零数据保留（ZDR）条款
- ❌ 坏消息：**领域特有的语义没法靠微调解决**，只能靠 state 里的资料 + instructions/criteria 的设计

### 坑 7：官方不做数据处理承诺之外的任何本地化

- 服务**部署在美国西海岸**（官方博客原话：evals 一般从西海岸的笔记本上跑，"this is where our service is currently based"）
- **无自托管、无权重、无参数、无架构论文**
- 有 DPA / 隐私政策 / 企业 ZDR，但**没有中国区节点**

> **对内部项目（如 E9）的直接结论**：**不能直接使用**。走 [4.5 自建兼容端点](#45-路径-e自建-system-one-兼容端点内部项目的唯一可行解)。

---

## 第七章 对测试开发的实际建议

### 7.1 三个可以今天就做的（零成本）

| 建议 | 做法 |
|------|------|
| **① 用 $5 额度做一次"可行性探针"** | 挑一个你真实的高频判断（比如失败分诊），用**真实数据**跑 100–200 条，记录：准确率、置信度分布、**高置信是否真的更准**。这比看任何基准都有用 |
| **② 用 `/model-jaggedness/jev-1.13` 当测试用例清单** | 那 9 条缺陷（字面理解 / 不会计数 / 日期当文本 / 多跳掉分 / context rot / **不防注入** / 指令矛盾 / 不变量不成立 / 不能生成）**本身就是 9 条现成的 AI 组件测试用例**。逐条设计一条测试，你就有了第一套 AI 组件测试套件 |
| **③ 把健康检查脚本固化** | 用 [2.5 节](#25-把这条实测变成一个健康检查脚本)的脚本，加进你的日常自检——尤其因为**速率限制是动态的** |

### 7.2 内部项目的合规判断（重点）

```
判定链：
  Jev 是否提供自托管？        → ❌ 否（无权重、无参数、无架构论文）
  Jev 是否可离线部署？        → ❌ 否（仅托管 API）
  服务部署在哪？              → ⚠️ 美国西海岸
  是否可用客户数据微调？      → ❌ 否（同一套权重服务所有账号）
  ↓
  结论：❌ 数据会出境，不满足"代码与数据不出内网"的要求
```

**但有三条可落地路径**（按推荐度）：

| 路径 | 做法 | 收益 |
|------|------|------|
| **① 借接口契约（最强）** | 在内网实现 `POST /v1/systemone` 同款契约。**`tontoko/jev-browser` 原生支持 `JEV_BASE_URL`，且不需要 Jev key** | 整套 Jev 生态工具**立刻可用**，数据一步不出网 |
| **② 借架构，换模型** | 自托管编码器实现 Choice/Noul，配合温度缩放做**后校准** | 效果最接近，可离线、可微调、可真校准 |
| **③ 只借方法论** | 抄"原子化问题 + 代码里组合 + 置信度三段式路由 + 逐项问再汇总" | 零成本、今天就能做 |

### 7.3 学习路径建议（给求职目标）

```
第 1 天  官网四页精读（quickstart / models / confidence / jaggedness）
         + Playground 跑通第一条 Noul
第 2 天  用 Python SDK 接一个真实小场景（推荐：失败分诊或邮件/工单分类）
         记录准确率与置信度分布，**做一次校准检查**
第 3 天  把 jaggedness 的 9 条缺陷变成 9 条测试用例 → 这是你面试最能讲的素材
第 4 天  装 Agent Skill，让 Claude Code / Codex 帮你写一个完整的小工具
第 5 天  写一份 1 页的评估报告：能做什么 / 不能做什么 / 阈值怎么定 / 成本多少
```

> 💡 **面试时最有说服力的，不是"我知道 Jev 很快很便宜"，而是**：
> "我用它跑了我自己的 N 条真实样本，准确率是 X%，**但它的置信度在中文场景下需要重新校准**——因为我实测发现报 0.9 的那些只有约 Y% 是对的。所以我把它定位成**过滤器而不是裁判**，并且用 `inconclusive` 状态兜住了低置信的情形。"

### 7.4 一条容易被忽视的提醒

> **趁现在赶紧把这条能力学会。** 社区里已经有人在讨论：**"这种能力很快会被下一代通用模型内化"**。
> 不管这个判断对不对，**现在学它，学会的是"如何把判断从生成里剥出来"这个架构思维**——而那个思维即使 Jev 消失了也仍然有效。

---

## 附录 A 不可靠来源识别

检索过程中遇到几处**需要明确标注为不可靠**的信息，列在这里是为了避免你以后被同一类内容误导：

| 说法 | 判定 | 理由 |
|------|------|------|
| "TypeSafe 官网候补通道对大陆邮箱**审核通过率超 87%**，平均等待时间 **3.2 小时**" | ❌ **不可信** | ① 官方从未公布任何通过率或等待时长（官方原话只有"as quickly as we can"）；② **09-21 起候补已取消**，该信息已过时；③ 数字精确到小数位但无出处，是典型的 AI 生成式 SEO 内容特征 |
| "**APUS 开源**的本地 Jev 复现版 `jev-ultrafast` 已适配国产显卡驱动" | ❌ **事实错误** | `jev-ultrafast` 由 **browser-use** 团队创建（2026-09-16），与 APUS 无关 |
| "OpenRouter 可通过**微信快捷登录**" | ⚠️ **需自行核实** | 微信登录类说法多见于中文 SEO 稿。**以 `openrouter.ai` 实际注册页为准** |
| "Vercel AI Gateway 提供免费促销**有效期至 09-25**" | ⚠️ **需自行核实** | 促销期限类信息时效性极强，且此说法只出现在单一来源 |

**识别这类内容的通用方法**：
1. **有没有出处**？官方文档 / 官方博客 / 官方 X 是硬来源；"社区实践""据了解"是软来源。
2. **数字是否过于精确而无出处**？（"87%"、"3.2 小时"就是典型）
3. **是否与官方明文冲突**？（"适配国产显卡"与"仅托管 API、无权重"直接冲突）
4. **时效**（候补、促销、限额都可能一天一变）

---

## 附录 B 参考资料

### 官方一手 🟢

| 内容 | 链接 |
|------|------|
| 官网首页 | https://typesafe.ai |
| 官方博客（技术细节最全的一篇） | https://typesafe.ai/blog/introducing-system-one-models-and-jev |
| 官方文档 · 总览 | https://docs.typesafe.ai/ |
| **官方文档 · 快速开始**（Playground → API → SDK → Skill 四路） | https://docs.typesafe.ai/introduction/quickstart |
| **官方文档 · Models**（模型 ID / 别名 / 价格 / 速率限制 / 上下文 / 语言支持 / 数据处理） | https://docs.typesafe.ai/models |
| 官方文档 · Confidence（含近似公式与三段式路由） | https://docs.typesafe.ai/confidence |
| **官方文档 · Jev 1.13 jaggedness（9 条缺陷）** | https://docs.typesafe.ai/model-jaggedness/jev-1.13 |
| 官方文档 · 四个架构模式 | https://docs.typesafe.ai/patterns |
| 官方文档 · HTTP API 参考（含速率限制处理） | https://docs.typesafe.ai/api |
| 官方文档 · Agent Skill | https://docs.typesafe.ai/agent-skill |
| 官方文档 · Legal（DPA / 隐私政策 / 企业 ZDR） | https://docs.typesafe.ai/legal |
| 控制台 | https://console.typesafe.ai |
| Playground | https://console.typesafe.ai/playground |
| API Keys | https://console.typesafe.ai/keys |
| 工作流评测站 | https://evals.typesafe.ai/ |
| 官方 GitHub · 技能库 | https://github.com/typesafe-ai/skills |
| 官方 GitHub · system-one-adapter-python | https://github.com/typesafe-ai/system-one-adapter-python |
| 企业/更高限额联系 | sales@typesafe.ai |

### 第三方通道 🟢

| 内容 | 链接 |
|------|------|
| **OpenRouter · Jev 1.13**（Decisions API、模型 ID、32k 上下文、Quick Start） | https://openrouter.ai/typesafe/jev-1.13 |
| OpenRouter · Decisions API 端点说明 | `POST https://openrouter.ai/api/alpha/decisions` |

### 接入方式与解读 🟡

| 内容 | 链接 |
|------|------|
| 六种访问 Jev 的方式（含 Vercel Gateway 的 AI-SDK-only 限制说明） | https://apidog.com/blog/how-to-access-jev |
| Jev 全面开放公告解读（含 14 万候补、$5 额度换算的分析） | https://www.explainx.ai/blog/jev-general-availability-no-waitlist-2026 |
| 日本开发者整理的接入步骤（Vercel / Cloudflare / OpenRouter 三通道对比） | https://note.com/mait_it/n/n85ed5539cab4 |
| OpenRouter 接入 Jev 的参数适配与避坑 | https://www.php.cn/faq/3163988.html |

### 中文报道 🔴（口径需交叉验证）

| 内容 | 链接 |
|------|------|
| 新浪财经 ·《TypeSafe AI 的 Jev 全面开放 注册用户获 5 美元额度》（2026-09-21） | https://finance.sina.com.cn/stock/estate/integration/2026-09-21/doc-inispyne8962439.shtml |
| 腾讯新闻 · 中信证券研报观点 | https://news.qq.com/rain/a/20260921A02VTI00 |

---

> **文档校验说明**
> - 官网矩阵、模型信息、价格、速率限制、上下文口径、语言支持、数据处理条款均来自 🟢 官方文档当日页面。
> - 连通性与端点可用性为 🔵 **本机 2026-09-21 实测**，含走代理与强制直连两组对照，以及无密钥 POST 的真实返回（403 + `authentication_error`）。
> - ⚠️ **时效风险**：Jev 处于早期访问阶段，**价格、速率限制、模型版本、别名指向、通道可用性均可能变化**。落地前请以 `docs.typesafe.ai` 当期版本为准。
> - ⚠️ 附录 A 单独列出了本次检索中发现的**不可靠来源**，避免重复踩坑。
> - 本文不含外链图片；脚本中的密钥位置均为占位符，**请勿把真实密钥写入仓库或提交到版本控制**。
