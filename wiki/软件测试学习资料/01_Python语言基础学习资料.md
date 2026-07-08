# Python语言基础学习资料

> 生成日期：2026-07-08
> 适用对象：邓万鹏，自动化测试 / AI自动化测试 / AI产品测试面试
> 生成依据：Python官方文档 + 当前简历 + 能力评估 + 真实面试题
> 重点目标：能把 Python 语法点讲到测试开发场景中，而不是只背概念

---

## 一、官方资料来源

| 来源 | 用途 |
|------|------|
| Python Data Model：https://docs.python.org/3/reference/datamodel.html | 对象、身份、类型和值 |
| Python Built-in Types：https://docs.python.org/3/library/stdtypes.html | list、dict、tuple、str等类型 |
| Python Expressions：https://docs.python.org/3/reference/expressions.html | lambda、yield、推导式 |
| Python contextlib：https://docs.python.org/3/library/contextlib.html | 上下文管理器 |
| Python GIL Glossary：https://docs.python.org/3/glossary.html#term-global-interpreter-lock | GIL定义 |
| Python unittest.mock：https://docs.python.org/3/library/unittest.mock.html | Mock与patch |

---

## 二、必须掌握的核心概念

### 1. 可变对象和不可变对象

Python 变量保存的是对象引用。对象本身有三个核心属性：身份、类型和值。

| 类型 | 示例 | 特点 |
|------|------|------|
| 可变对象 | list、dict、set | 对象内容可以原地修改 |
| 不可变对象 | int、float、str、tuple | 修改时通常会产生新对象 |

面试高频坑：

```python
def add_item(x, items=[]):
    items.append(x)
    return items

print(add_item(1))  # [1]
print(add_item(2))  # [1, 2]，不是 [2]
```

正确写法：

```python
def add_item(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return items
```

测试开发场景：
- 封装接口默认参数时，不要把 `headers={}`、`json={}`、`data=[]` 写成默认值。
- 公共请求方法里要避免多个用例共享同一个可变对象，导致 headers、token、测试数据被串改。

### 2. 深拷贝和浅拷贝

浅拷贝只复制外层对象，内部嵌套对象仍然共享引用。深拷贝会递归复制内部对象。

```python
import copy

template = {"user": {"name": "test"}, "roles": ["qa"]}

case1 = copy.copy(template)
case1["user"]["name"] = "dwp"
print(template["user"]["name"])  # dwp，嵌套对象被影响

case2 = copy.deepcopy(template)
case2["roles"].append("admin")
print(template["roles"])  # ['qa']
```

接口自动化场景：
- 测试数据模板经常是嵌套 dict，建议对每条用例使用 `deepcopy`。
- 如果只用浅拷贝，某条用例改了嵌套字段，后续用例可能被污染。

### 3. `*args` 和 `**kwargs`

`*args` 接收可变位置参数，`**kwargs` 接收可变关键字参数。

```python
def request_api(method, url, **kwargs):
    timeout = kwargs.pop("timeout", 10)
    print(method, url, timeout, kwargs)

request_api("GET", "/api/users", params={"page": 1}, headers={"token": "xxx"})
```

测试开发场景：
- 封装通用请求方法时，用 `**kwargs` 透传 `params/json/data/headers/cookies/files`。
- 但不要无边界透传，核心参数如 timeout、base_url、headers 合并规则要统一。

### 4. 装饰器

装饰器本质是函数作为一等对象，通过闭包包装原函数，在不改原函数代码的情况下增强行为。

```python
import time
from functools import wraps

def cost_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__} cost {time.time() - start:.3f}s")
    return wrapper

@cost_time
def test_login():
    return "ok"
```

测试开发场景：
- 统计接口耗时。
- 失败自动截图。
- 日志增强。
- 简单重试。
- 给 AI 生成的用例加统一检查规则。

面试注意：
- 要说清楚“定义装饰器”和“调用被装饰函数”的时机。
- 使用 `functools.wraps` 保留原函数名称和文档，报告中更清晰。

结合你的真实经验：
- 在接口自动化框架里，装饰器可以用于统一记录接口方法调用、耗时、异常和重试。
- 在 UI 自动化里，装饰器可以包装关键步骤，失败时截图、保存页面源码或记录 Playwright trace。
- 在 AI+SKILL 生成用例后，可以用装饰器给生成的接口方法加统一前置校验，避免 AI 漏掉超时、日志、断言入口。

面试标准回答模板：

```text
装饰器本质是一个函数接收另一个函数，并返回增强后的新函数。我的理解不是只停留在语法上，而是会放到测试框架里用。比如接口自动化里，我可以用装饰器统一记录请求耗时、入参、异常和重试；UI自动化里可以用于失败截图；AI生成用例后，也可以通过装饰器保证所有用例都走统一的日志和校验规则。需要注意的是，装饰器在函数定义阶段完成包装，被装饰函数真正执行时才会进入wrapper逻辑，同时我会用functools.wraps保留原函数名，避免pytest报告里函数名变乱。
```

### 5. 生成器和 `yield`

生成器用 `yield` 惰性产生数据，执行到 `yield` 暂停，下次 `next()` 从暂停处继续。

```python
def page_data():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")

g = page_data()
print(next(g))  # start 后输出 1
print(next(g))  # middle 后输出 2
```

测试场景：
- 分页接口批量读取数据。
- 大日志文件逐行处理。
- 海量测试数据生成，不一次性加载到内存。

真实面试映射：
- 真实面试问过“10000台机器采集日志，本地资源有限怎么处理”。生成器和流式处理是关键表达点。

回答重点：
```text
yield 不会一次性返回全部数据，而是每次产出一个值并暂停函数状态，适合分页接口、日志流和大数据量测试数据生成，可以降低内存占用。
```

薄弱项纠偏：你之前容易把 `yield` 产出的值和 `print` 输出混在一起。面试时按三句话说清楚：

```text
第一，调用生成器函数不会立即执行函数体，只会返回生成器对象。
第二，第一次next()才开始执行，遇到yield就把yield后面的值返回给调用方，并暂停在当前位置。
第三，下一次next()会从上次暂停的位置继续执行，直到遇到下一个yield或函数结束。
```

结合 E10 自动化项目的表达：

```text
在E10低代码平台测试里，有些接口会分页返回表单、页面、报表或流程数据。如果一次性把所有数据加载到内存，既慢也容易污染调试结果。我会用生成器按页拉取、按条处理，用于数据校验、日志分析或批量生成测试数据。这样既节省内存，也便于和pytest参数化结合。
```

### 6. 上下文管理器

`with` 会调用对象的 `__enter__` 和 `__exit__`，用于资源申请和释放。

```python
from contextlib import contextmanager

@contextmanager
def temp_user():
    user_id = "test_user"
    print("create user")
    try:
        yield user_id
    finally:
        print("delete user")

with temp_user() as uid:
    print("run case", uid)
```

测试开发场景：
- 创建临时用户、订单、测试数据。
- 执行结束后自动清理。
- 管理数据库连接、文件、浏览器上下文。

### 7. GIL、多线程、多进程、协程

| 方式 | 特点 | 适用场景 |
|------|------|----------|
| 多线程 | 同进程共享内存，受GIL影响 | IO密集，如接口请求、文件读写 |
| 多进程 | 内存隔离，可绕开GIL | CPU密集，如大量计算 |
| 协程 | 单线程用户态调度，开销低 | 高并发网络IO、日志采集 |

面试回答：
```text
Python里的多线程受GIL影响，纯CPU计算不能明显提速，但接口自动化、日志采集、网络请求属于IO密集，多线程或协程仍然有价值。CPU密集任务可以考虑多进程。实际测试平台里我会加并发限制、超时、重试和队列，避免为了并发把环境打爆。
```

---

## 三、结合个人项目的表达

你的简历写了 Python 8年、pytest、requests、Playwright、Locust、AI+接口自动化。面试时不要只说“我会 Python”，要落到测试开发框架能力：

```text
我使用 Python 主要不是写零散脚本，而是搭建自动化测试框架。比如接口自动化里，我会用 dict/list 组织请求数据，用 deepcopy 避免模板污染，用装饰器统一处理请求日志和耗时统计，用上下文管理器做测试数据创建和清理，用生成器处理分页接口和日志流。结合 pytest fixture 和 requests，可以把这些语言特性落到稳定可维护的测试框架里。
```

E10项目背诵版：

```text
我在泛微E10低代码平台的自动化测试中，Python主要承担框架工程能力。接口层用requests和Session封装公共请求，pytest负责用例组织、fixture前后置和参数化，Python的dict/list承载表单、流程、权限这些复杂测试数据。为了避免数据污染，我会对嵌套模板做deepcopy；为了统一日志、耗时和异常处理，会用装饰器；为了处理分页接口和日志流，会用生成器；为了创建和清理测试数据，会用上下文管理器或fixture yield。后面做AI+接口自动化SKILL时，这些框架约束也会作为AI生成用例的边界，让AI生成的代码能直接进入现有pytest框架执行。
```

---

## 四、常见面试追问

1. Python参数传递是值传递还是引用传递？
2. `is` 和 `==` 的区别是什么？
3. 为什么默认参数不要用 list/dict？
4. 深拷贝和浅拷贝在接口测试数据中有什么用？
5. 生成器 `yield` 的执行顺序是什么？
6. 装饰器在测试框架里怎么用？
7. 上下文管理器如何保证测试数据清理？
8. GIL 对自动化测试并发有什么影响？

---

## 五、回答模板

```text
Python语言基础我会结合测试开发场景理解。比如可变对象和深浅拷贝影响接口测试数据是否互相污染；装饰器可以做日志、重试、耗时统计和失败截图；生成器适合分页接口和大日志流式处理；上下文管理器适合创建和清理测试数据。并发方面，我会区分IO密集和CPU密集，接口自动化大多是IO密集，多线程或协程能提升效率，但要配合限流、超时和重试，保证自动化执行稳定。
```

项目深挖模板：

```text
如果面试官问我Python 8年经验体现在哪里，我会从框架稳定性回答，而不是只说语法。我的Python经验主要体现在接口/UI自动化框架、测试平台后端和AI测试工具落地上。比如E10项目里，我用pytest+requests组织接口自动化，用fixture管理登录态和测试数据，用参数化覆盖等价类和边界值，用装饰器统一日志和耗时统计，用生成器处理分页和日志流。AI+SKILL项目里，我还把这些框架规范固化成AI生成用例的约束，让AI生成后必须能跑最小范围pytest，并根据失败日志修复。
```

---

## 六、练习清单

- [ ] 用自己的话解释可变对象、不可变对象，并举一个接口测试参数污染例子。
- [ ] 写出一个装饰器，用来统计接口请求耗时。
- [ ] 口述 `yield` 的执行顺序，不再把 `yield` 返回值和 `print` 输出混淆。
- [ ] 说明多线程、多进程、协程分别适合什么测试场景。
- [ ] 用 STAR 结构讲一个 Python 特性提升框架稳定性的例子。

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[02_pytest必背学习资料]] — AI测试主题关联
- [[09_AI测试基础学习资料]] — AI测试主题关联
- [[13_AI产品测试方法论学习资料]] — AI测试主题关联
- [[17_测试平台开发学习资料]] — AI测试主题关联
- [[AI产品测试]] — AI测试主题关联
- [[03_Python测试开发框架设计学习资料]] — AI测试主题关联
- [[04_测试理论与用例设计学习资料]] — AI测试主题关联
- [[14_AI辅助测试工具必背学习资料]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
