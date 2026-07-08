# Python测试开发框架设计学习资料

> 生成日期：2026-07-08
> 适用对象：邓万鹏，自动化测试 / AI自动化测试 / AI产品测试面试
> 生成依据：requests官方文档 + pytest官方文档 + 当前简历 + AI+接口自动化SKILL项目
> 重点目标：能讲清接口自动化框架如何从脚本升级为工程化体系

---

## 一、官方资料来源

| 来源 | 用途 |
|------|------|
| requests Quickstart：https://requests.readthedocs.io/en/latest/user/quickstart/ | 基础请求 |
| requests Advanced Usage：https://requests.readthedocs.io/en/latest/user/advanced/ | Session、PreparedRequest、SSL、超时 |
| requests API Reference：https://requests.readthedocs.io/en/latest/api/ | 异常、响应对象 |
| pytest Fixtures：https://docs.pytest.org/en/stable/how-to/fixtures.html | 前后置与资源管理 |
| pytest Configuration：https://docs.pytest.org/en/stable/reference/customize.html | 配置 |

---

## 二、框架分层设计

接口自动化框架不能只是“一个 requests 脚本”。面试建议按分层讲：

```text
config/       环境配置、base_url、账号、数据库、开关
client/       HTTP请求封装，统一headers、token、timeout、日志
api/          业务接口层，如 OrderApi、UserApi
cases/        pytest测试用例层
data/         YAML/JSON/Excel/数据库测试数据
assertions/   响应断言、数据库断言、schema断言
fixtures/     登录态、造数据、清理数据
report/       Allure/HTML/平台报告
utils/        日志、时间、文件、加密、随机数据
ci/           Jenkins/Docker执行入口
```

回答核心：
```text
分层的目标是让请求封装、业务接口、测试用例、测试数据、断言和报告解耦。这样接口变了优先改接口层，环境变了改配置层，数据变了改data层，用例逻辑不需要大面积修改。
```

结合E10低代码平台的落地说法：

```text
我在E10低代码平台里做接口自动化，不会把表单、页面、报表、流程、权限这些接口直接写成零散脚本，而是按框架分层维护。底层统一处理base_url、token、headers、timeout和日志；业务接口层按模块封装表单、页面、报表、菜单等API；用例层只表达业务场景，比如新增表单字段、发布流程、配置权限后校验结果。这样低代码配置经常变化时，只需要改接口层或测试数据，不会大面积改用例。
```

---

## 三、HTTP Client封装

基础封装示例：

```python
import requests

class ApiClient:
    def __init__(self, base_url, token=None, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = timeout
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)
        response = self.session.request(method, url, **kwargs)
        return response
```

必须强调：
- 所有请求必须有 timeout，避免CI卡死。
- Session用于复用连接、保存cookie/header。
- 日志要记录 method、url、params/body、status_code、响应耗时、trace id。
- 异常要分层：连接异常、超时、HTTP错误、断言失败、环境失败。

---

## 四、业务接口层

```python
class OrderApi:
    def __init__(self, client):
        self.client = client

    def create_order(self, sku_id, count, coupon_id=None):
        payload = {
            "skuId": sku_id,
            "count": count,
            "couponId": coupon_id,
        }
        return self.client.request("POST", "/api/orders", json=payload)
```

好处：
- 用例里不散落URL。
- 接口路径、参数结构集中维护。
- AI生成用例时可以参考已有接口方法，减少重复代码。

---

## 五、数据驱动

数据驱动不是“把数据放到Excel就行”，核心是测试逻辑和测试数据分离。

| 数据源 | 适用场景 | 注意点 |
|--------|----------|--------|
| YAML/JSON | 接口场景数据、易版本管理 | 结构清晰 |
| Excel | 非技术同事维护 | 解析和类型容易出错 |
| 数据库 | 大量业务数据 | 注意隔离和清理 |
| 代码参数化 | 小规模边界值 | 可读性强 |

pytest参数化示例：

```python
@pytest.mark.parametrize("count, expected_code", [
    (1, "SUCCESS"),
    (0, "INVALID_COUNT"),
    (-1, "INVALID_COUNT"),
])
def test_create_order(order_api, count, expected_code):
    resp = order_api.create_order("sku001", count)
    assert resp.json()["code"] == expected_code
```

E10低代码平台的数据驱动表达：

```text
E10低代码平台的接口自动化很适合数据驱动，因为同一套表单、流程、权限逻辑会被不同字段类型、不同配置开关、不同角色组合反复验证。我会把字段类型、必填规则、长度限制、默认值、权限角色、流程节点这些变化点抽成参数化数据；用例逻辑保持稳定，只替换输入数据和预期结果。这样新增一种字段类型或权限组合时，只需要补数据，不需要复制一堆用例。
```

可背示例：

```python
@pytest.mark.parametrize("field_type, value, expected_code", [
    ("text", "合同审批", "SUCCESS"),
    ("text", "", "REQUIRED_FIELD"),
    ("number", 100, "SUCCESS"),
    ("number", -1, "INVALID_RANGE"),
])
def test_form_field_rule(form_api, field_type, value, expected_code):
    resp = form_api.create_field(field_type=field_type, value=value)
    assert resp.json()["code"] == expected_code
```

---

## 六、断言设计

接口自动化最忌只断言状态码。

| 断言层级 | 示例 |
|----------|------|
| HTTP层 | status_code、headers、Content-Type |
| 业务层 | code、message、success |
| 数据结构 | 字段存在、类型、schema |
| 数据库 | 订单落库、状态、金额、库存扣减 |
| 副作用 | MQ消息、缓存、日志、文件 |
| 性能 | 响应时间阈值 |
| AI质量 | 相关性、准确性、幻觉、拒答 |

面试表达：
```text
我会把断言分层，状态码只是第一层。核心业务接口必须校验业务码、关键字段、数据库落库和状态流转。对于下单接口，还要校验订单明细、金额、优惠、库存和幂等。
```

---

## 七、测试数据和环境配置

环境配置：

```yaml
test:
  base_url: "https://test.example.com"
  db: "test_db"
  timeout: 10
staging:
  base_url: "https://staging.example.com"
  db: "staging_db"
  timeout: 10
```

测试数据策略：
- 前置接口造数。
- 数据库造数。
- fixture创建和清理。
- 测试数据加唯一标识，避免重复。
- 核心数据不要依赖人工预置。

---

## 八、稳定性设计

| 问题 | 处理方式 |
|------|----------|
| 环境不稳定 | 预检查、健康检查、失败分类 |
| 数据污染 | fixture清理、唯一数据、事务回滚 |
| 接口依赖 | 上下文变量、链式fixture |
| 偶发超时 | timeout、有限重试、日志保留 |
| 报告不可定位 | 请求响应日志、trace id、失败截图/附件 |
| 多项目执行冲突 | 环境隔离、任务队列、并发限制 |

---

## 九、pytest工程化能力

你的能力评估里 pytest Hook 名称是薄弱项，面试要至少能说出几个具体名字和用途。

| 能力点 | 面试表达 |
|--------|----------|
| fixture | 管理登录态、测试数据、数据库连接、浏览器上下文 |
| fixture scope | function隔离用例，session管理全局资源 |
| yield fixture | yield前做前置，yield后做清理 |
| autouse fixture | 自动注入公共上下文，不需要每条用例显式声明 |
| parametrize | 把等价类、边界值、权限组合转成数据驱动 |
| conftest.py | 存放共享fixture和本地插件能力，pytest会自动发现 |
| pytest_collection_modifyitems | 收集阶段修改用例、补marker、调整执行顺序 |
| pytest_runtest_makereport | 执行阶段拿到setup/call/teardown结果，用于失败信息和报告增强 |
| pytest_sessionstart / pytest_sessionfinish | 记录测试开始结束、汇总全局结果 |

结合真实框架表达：

```text
我在pytest框架里会把conftest.py作为共享能力入口。比如用fixture管理登录态、测试数据和清理逻辑，用autouse fixture记录每条用例的上下文，用pytest_runtest_makereport获取失败阶段和失败信息，再把结果写入HTML报告或测试平台。这样失败后不仅知道哪条用例失败，还能看到接口、参数、响应、耗时和环境信息。
```

---

## 十、接入CI/CD

典型流程：

```text
Git提交 -> Jenkins拉代码 -> 安装依赖 -> 选择环境 -> 执行pytest -> 生成Allure/HTML报告 -> 归档报告 -> 通知结果 -> 失败回写测试平台
```

pytest命令示例：

```bash
pytest cases/api -m smoke --env=test --alluredir=report/allure-results
```

---

## 十一、结合AI+接口自动化SKILL项目

你的核心项目不能只说“AI写用例”，要说框架如何承接AI输出：

```text
我的AI+接口自动化SKILL是在已有pytest接口自动化框架上做增强。它支持抓包驱动、参考已有用例、cURL手工、Java Controller源码参考四种输入。AI生成接口方法和pytest用例后，不是直接结束，而是必须执行最小范围pytest，根据真实响应修复断言，再检查Git diff和人工确认关键业务逻辑。这个闭环让AI生成的内容能真正落到框架里，而不是停留在草稿。
```

效率数据表达：
```text
我对比了AI使用前后5周的数据，接口用例编写效率提升约93%，综合效率提升约46%。这个提升主要来自接口分析、用例草稿生成、重复结构代码生成和失败修复辅助，但业务断言仍然需要人工把关。
```

最小范围执行闭环背诵版：

```text
我做AI+接口自动化SKILL时，最关键的不是让AI一次性生成很多代码，而是给AI加工程约束。流程是先提供上下文，比如抓包数据、已有用例、cURL或Java Controller源码；再让AI按现有pytest+requests框架生成接口方法和用例；生成后必须执行最小范围pytest，只跑本次新增或修改的用例；如果失败，要求AI根据真实报错、请求响应和断言信息修复；最后检查Git diff，排除运行产物，人工确认业务断言。这个闭环保证AI输出不是草稿，而是能进入现有自动化框架的可执行用例。
```

四种工作流表达：

| 工作流 | 适用场景 | 面试说法 |
|--------|----------|----------|
| 抓包驱动 | 有真实页面操作 | 通过mitmproxy抓取请求，AI识别接口并生成用例 |
| 参考已有 | 有相似用例 | AI复用已有fixture、接口方法和断言风格 |
| cURL手工 | 已拿到请求响应 | 直接用cURL和响应体生成接口方法与用例 |
| Java Controller源码 | 后端接口未覆盖 | 从Controller定义中补齐未覆盖接口，再落到pytest用例 |

---

## 十二、常见面试追问

1. 你怎么从0到1设计接口自动化框架？
2. requests为什么要用Session？
3. timeout为什么必须设置？
4. token过期怎么处理？
5. 如何保证用例互不影响？
6. 数据驱动怎么设计？
7. 接口依赖怎么处理？
8. 断言除了状态码还断什么？
9. 框架怎么接入Jenkins和测试平台？
10. AI生成用例如何保证质量？

---

## 十三、回答模板

```text
我设计接口自动化框架会按分层来做。底层是requests封装的HTTP client，统一处理base_url、headers、token、timeout、日志和异常；中间是业务接口层，把具体接口封装成可复用方法；上层是pytest用例层，通过fixture管理登录态、测试数据和环境，通过参数化做数据驱动，通过marker做用例分层。断言不会只看状态码，还会校验业务码、关键字段、数据库、副作用和响应时间。结合我做过的AI+接口自动化SKILL，AI可以辅助生成用例和分析失败，但必须经过pytest执行闭环和人工确认业务断言，这样才能保证稳定可信。
```

E10项目标准回答模板：

```text
以E10低代码平台为例，我的框架设计重点是应对低代码配置多、业务模块多、回归频繁的问题。底层用requests Session封装公共请求，统一token、headers、timeout、日志和异常；业务层按表单、页面、报表、菜单、权限、流程等模块封装API；用例层用pytest组织，fixture负责登录态、造数和清理，parametrize负责字段类型、边界值、权限角色等数据驱动；断言层同时看业务响应、数据库状态、配置是否生效和关键日志。AI+SKILL接入后，AI只负责提升接口分析和用例生成效率，最终仍要跑最小范围pytest、修复失败、检查diff、人工确认业务断言，所以质量边界是可控的。
```

---

## 十四、练习清单

- [ ] 画出接口自动化框架分层图并口述每层职责。
- [ ] 准备一个 `ApiClient` 封装思路。
- [ ] 说清楚 Session、timeout、日志、异常处理的必要性。
- [ ] 用下单接口举例说明断言层级。
- [ ] 用2分钟讲清AI+SKILL如何接入pytest框架。
- [ ] 背出至少4个pytest Hook或fixture相关能力：`pytest_runtest_makereport`、`pytest_collection_modifyitems`、`pytest_sessionstart`、`pytest_sessionfinish`、autouse fixture、yield fixture。
