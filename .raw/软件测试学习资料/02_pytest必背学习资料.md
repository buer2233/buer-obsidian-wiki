# pytest必背学习资料

> 适用对象：邓万鹏，自动化测试 / AI自动化测试 / AI产品测试面试  
> 生成依据：pytest官方文档 + Playwright官方文档 + 当前简历 + 真实 `conftest.py` + 错题#003/#015/#019 + 能力评估  
> 重点目标：把 fixture、conftest、parametrize、hook 从“知道概念”提升到“能结合真实框架讲清楚”

---

## 一、官方资料来源

| 来源 | 用途 | 面试要点 |
|------|------|----------|
| pytest Fixtures：https://docs.pytest.org/en/stable/how-to/fixtures.html | fixture、scope、yield清理 | fixture负责资源管理和依赖注入 |
| pytest Fixture Reference：https://docs.pytest.org/en/stable/reference/fixtures.html | conftest共享fixture | `conftest.py`自动发现，目录级生效 |
| pytest Parametrize：https://docs.pytest.org/en/stable/how-to/parametrize.html | 参数化 | 数据驱动、组合测试、indirect |
| pytest Hooks：https://docs.pytest.org/en/stable/how-to/writing_hook_functions.html | hook扩展 | pytest生命周期扩展点 |
| pytest Hooks Reference：https://docs.pytest.org/en/stable/reference/reference.html#hooks | hook函数名 | 面试必须说出具体hook名称 |
| Playwright Python Pytest：https://playwright.dev/python/docs/test-runners | pytest插件fixture | UI自动化推荐用fixture提供隔离的`context/page` |

必背一句话：

```text
fixture解决“测试用例需要什么资源”，hook解决“pytest执行到某个生命周期时框架要做什么扩展”。
资源给用例用，选fixture；框架生命周期副作用，选hook。
```

---

## 二、pytest和unittest区别

| 对比项 | pytest | unittest |
|--------|--------|----------|
| 用例写法 | 函数/类均可，语法简洁 | 主要通过类继承 `unittest.TestCase` |
| 断言 | 原生 `assert`，失败解释清晰 | `self.assertEqual`、`self.assertTrue` 等 |
| 前后置 | fixture支持依赖注入、scope、yield清理 | `setUp` / `tearDown` 层级较固定 |
| 参数化 | 原生 `@pytest.mark.parametrize` | 标准库不直接支持 |
| 插件能力 | hook + 插件生态丰富 | 扩展能力相对弱 |
| 报告集成 | pytest-html、allure、junitxml、hook自定义 | 通常依赖外部扩展 |

面试回答模板：

```text
我在自动化框架里更常用pytest。原因是pytest的fixture、参数化、marker和hook更适合测试开发框架。fixture可以管理登录态、测试数据、浏览器、环境配置；parametrize适合接口数据驱动；hook适合报告增强、失败日志采集、用例收集阶段打标签。unittest作为标准库稳定，但当框架要接入测试平台、Jenkins和自定义报告时，pytest维护成本更低。
```

结合我的项目：

```text
我在E10低代码平台接口自动化里，就是基于pytest组织用例执行。AI+接口自动化SKILL生成用例后，也会回到pytest执行闭环：生成用例 -> 小范围执行 -> 失败定位 -> 修复用例 -> 生成报告。
```

---

## 三、fixture核心机制

fixture是pytest的资源管理和依赖注入机制。测试函数声明同名参数后，pytest会自动执行fixture，并把返回值传给测试函数。

```python
import pytest

@pytest.fixture
def token():
    return "Bearer xxx"

def test_get_user(token):
    assert token.startswith("Bearer")
```

### 1. fixture scope怎么选

| scope | 执行范围 | 自动化测试场景 | 风险 |
|-------|----------|----------------|------|
| function | 每个用例执行一次 | 独立测试数据、页面对象、接口前置数据 | 执行频率高，但隔离最好 |
| class | 每个测试类执行一次 | 同类用例共享前置 | 类内用例可能互相影响 |
| module | 每个文件执行一次 | 模块级配置、模块级账号 | 文件内共享状态需谨慎 |
| package | 每个包执行一次 | 包级测试资源 | 用得少，适合大包资源 |
| session | 整个测试会话执行一次 | 全局配置、昂贵资源、浏览器进程、数据库连接池 | 状态污染和并发风险更高 |

必背口诀：

```text
越靠近function，隔离越好但成本越高；越靠近session，性能越好但共享状态风险越高。
```

### 2. yield fixture

`yield`前是前置，`yield`后是后置清理。

```python
@pytest.fixture
def order():
    order_id = "O001"
    yield order_id
    print("delete order", order_id)
```

适合场景：

- 登录后返回token，用例结束后清除token或会话。
- 创建测试数据，用例结束后删除测试数据。
- 启动浏览器上下文，用例结束后关闭上下文。
- 临时修改环境变量，用例结束后恢复。

### 3. 真实框架里的fixture案例

你的真实框架 `D:\workSpace_001\test-automation\E10自动化\接口自动化测试\conftest.py` 里有一个 autouse fixture：

```python
@pytest.fixture(autouse=True)
def add_interface_description_to_request_header(request):
    interface_function = request.node
    if interface_function and hasattr(interface_function, "_obj") and callable(interface_function._obj):
        des = interface_function._obj.__doc__
        interface_description = "未提供用例描述" if not des else des
        os.environ.update({"nodeid_des": interface_function.nodeid})
        os.environ.update({"case_des": interface_description})
    yield
    os.environ.update({"nodeid_des": ""})
    os.environ.update({"case_des": ""})
```

它体现了三个面试点：

| 设计点 | 说明 | 面试表达 |
|--------|------|----------|
| `autouse=True` | 每条用例自动执行，不需要用例显式声明参数 | 适合框架级通用上下文注入 |
| `request.node` | 获取当前用例对象 | 可以读取nodeid、docstring、marker |
| `yield`后清理 | 用例结束后清空环境变量 | 避免本条用例的描述污染下一条用例 |

面试回答模板：

```text
我在框架里用过autouse fixture。比如接口自动化报告需要展示用例说明，我会在每条用例执行前通过request.node拿到当前用例对象，读取docstring和nodeid，写入环境变量供请求头或报告逻辑使用；yield之后再清空这些环境变量，避免上下文串到下一条用例。这个例子说明fixture不仅能返回资源，也能围绕单条用例生命周期做上下文管理。
```

---

## 四、conftest.py必背

`conftest.py` 是pytest自动发现的本地插件文件，用来放当前目录及子目录共享的 fixture、hook 和插件配置，不需要在测试文件中手动 import。

典型结构：

```text
tests/
  conftest.py
  api/
    conftest.py
    test_order.py
  ui/
    conftest.py
    test_login.py
```

官方要点：

- pytest会自动发现 `conftest.py`。
- `conftest.py` 中定义的fixture可被同目录和子目录用例直接使用。
- 父目录的fixture对子目录可见。
- 子目录可以有自己的 `conftest.py`，用于补充或覆盖局部能力。

面试回答模板：

```text
conftest.py可以理解为pytest的本地插件文件。它主要放公共fixture、hook、命令行参数和全局配置。它不需要import，pytest会按目录层级自动发现。父目录conftest.py里的fixture可以给子目录用，子目录也可以定义自己的fixture。我的接口自动化框架里，conftest.py就承担了账号读取、测试环境展示、pytest-html报告增强、失败信息采集、用例描述注入等框架能力。
```

---

## 五、参数化：parametrize、fixture params、indirect

### 1. `@pytest.mark.parametrize`

适合“同一测试逻辑跑多组测试数据”。

```python
import pytest

@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("admin", "123456", 200),
        ("admin", "", 400),
        ("", "123456", 400),
    ],
    ids=["success", "empty_password", "empty_username"]
)
def test_login(username, password, expected):
    assert isinstance(expected, int)
```

接口自动化场景：

- 正常参数、缺失参数、非法参数、边界参数。
- HTTP状态码和业务错误码组合。
- E10低代码表单字段校验组合。
- AI评估集中同一个评估函数跑多条prompt。

### 2. fixture `params`

适合“同一个fixture资源有多种实现或配置”。

```python
@pytest.fixture(params=["dev", "test"])
def env(request):
    return request.param

def test_env(env):
    assert env in ["dev", "test"]
```

典型场景：

- 多环境：dev/test/pre。
- 多浏览器：chromium/firefox/webkit。
- 多账号角色：admin/普通用户/只读用户。

### 3. indirect参数化

适合“参数不是直接给测试函数，而是先交给fixture做前置处理”。

```python
@pytest.fixture
def user(request):
    role = request.param
    return {"role": role, "token": f"token-{role}"}

@pytest.mark.parametrize("user", ["admin", "guest"], indirect=True)
def test_permission(user):
    assert "token" in user
```

三者区别一句话：

```text
parametrize偏测试数据组合；fixture params偏资源组合；indirect是把参数先交给fixture加工，适合需要登录、造数据、切环境的复杂前置。
```

结合我的项目：

```text
E10接口自动化中，我会用parametrize覆盖接口入参组合；用fixture params表达不同账号、租户或环境；如果参数要先登录换token、创建前置数据，就用indirect让fixture先加工再交给测试函数。
```

---

## 六、pytest Hook必背

你当前能力评估里的问题是：知道hook分类，但说不出具体函数名。下面这些要能直接背出来。

| Hook | 阶段 | 作用 | 自动化框架场景 |
|------|------|------|----------------|
| `pytest_addoption(parser)` | 初始化 | 增加命令行参数 | `--env=test`、`--base-url`、`--browser=chromium` |
| `pytest_configure(config)` | 配置完成后 | 初始化配置、注册marker、读取ini | 读取 `pytest.ini` markers，初始化报告上下文 |
| `pytest_collection_modifyitems(config, items)` | 用例收集后 | 修改收集到的用例 | 自动加marker、排序、按模块过滤 |
| `pytest_generate_tests(metafunc)` | 参数生成 | 动态参数化 | 从YAML/Excel/接口平台加载用例数据 |
| `pytest_runtest_setup(item)` | 单条用例setup前 | 执行前检查 | 环境检查、依赖检查 |
| `pytest_runtest_call(item)` | 单条用例执行时 | 包裹执行过程 | 少直接用，通常不替代fixture |
| `pytest_runtest_makereport(item, call)` | 生成报告 | 获取setup/call/teardown结果 | 失败截图、日志、失败原因、耗时 |
| `pytest_sessionstart(session)` | 会话开始 | 测试会话初始化 | 记录开始时间、启动全局服务 |
| `pytest_sessionfinish(session, exitstatus)` | 会话结束 | 测试会话收尾 | 汇总结果、清理缓存、推送通知 |
| `pytest_terminal_summary(terminalreporter)` | 终端总结 | 自定义终端输出 | 输出通过率、耗时、失败摘要 |

注意：hook函数名和参数签名不是随便写的，必须符合pytest hookspec。

面试回答模板：

```text
pytest hook是pytest暴露的生命周期扩展点。我常用的有pytest_addoption做命令行参数，pytest_configure做全局配置初始化，pytest_collection_modifyitems在收集阶段给用例打标签或调整顺序，pytest_runtest_makereport拿到用例setup/call/teardown阶段结果用于失败截图、日志采集和报告增强，pytest_sessionstart/sessionfinish做会话级初始化和收尾。
```

---

## 七、真实 `conftest.py` 案例拆解

你的真实框架里，hook主要用于“框架生命周期扩展”和“报告增强”，fixture主要用于“单条用例上下文管理”。这是面试时最有价值的真实案例。

### 1. 真实hook清单

| 真实Hook | 框架中做了什么 | 面试价值 |
|----------|----------------|----------|
| `pytest_configure(config)` | 读取 `pytest.ini` 的 `markers`，保存到全局 `tags`，初始化 `session_start_time` | 可以讲“初始化配置、读取marker” |
| `pytest_sessionstart(session)` | 会话开始时记录模块测试开始时间 | 可以讲“会话级生命周期” |
| `pytest_sessionfinish(session)` | 清空 `_case_timestamps`，防止残留 | 可以讲“会话结束清理” |
| `pytest_html_results_summary(prefix, summary, postfix)` | 在HTML报告摘要中增加测试环境、账号表、通过率、开始/结束时间 | 可以讲“pytest-html报告定制” |
| `pytest_html_results_table_header(cells)` | 增加Description、Test_nodeid、failinfo、tags、caseStartTime、caseEndTime列 | 可以讲“报告表头定制” |
| `pytest_runtest_makereport(item, call)` | 获取用例docstring、nodeid、AssertionError、setup/call时间，去掉teardown噪声 | 可以讲“失败信息和执行时间采集” |
| `pytest_html_results_table_row(report, cells)` | 写入用例描述、nodeid、失败类型、标签、开始结束时间，并生成 `prerun_results.txt` | 可以讲“结果落盘给平台/预检测使用” |
| `pytest_html_results_table_html(report, data)` | 通过用例清空冗余日志，报告更简洁 | 可以讲“报告可读性优化” |

### 2. 重点hook：`pytest_runtest_makereport`

真实框架的核心逻辑：

```python
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")
    if call.when == 'call' and report.failed == True:
        if 'AssertionError' in str(call.excinfo):
            report.__setattr__('failinfo', call.excinfo)
```

要能讲清楚：

- `hookwrapper=True`：先让其他hook/pytest正常执行，`yield`后拿到结果。
- `tryfirst=True`：尽量优先执行这个hook。
- `outcome.get_result()`：拿到pytest生成的report对象。
- `item.function.__doc__`：读取测试函数docstring作为用例描述。
- `call.when`：区分 `setup` / `call` / `teardown` 阶段。
- `call.excinfo`：拿到异常信息。
- `report`对象可挂自定义字段，例如 `description`、`failinfo`。

面试回答模板：

```text
我在真实框架里用pytest_runtest_makereport增强过报告。这个hook会在pytest生成测试报告时触发，我用hookwrapper先让pytest正常生成report，然后通过outcome.get_result拿到report对象。之后把测试函数docstring写入description，把中文nodeid做解码，如果call阶段失败并且是AssertionError，就把异常信息挂到report.failinfo。后续pytest-html的table_row hook再把这些字段写入HTML报告。这样报告里不仅有通过失败，还能看到用例描述、失败类型、标签和开始结束时间。
```

### 3. 重点hook：pytest-html报告增强

真实框架做了这些事：

- 报告摘要区展示测试环境URL。
- 报告摘要区展示测试账号、账号备注、团队。
- 报告摘要区展示全量测试通过率。
- 报告摘要区展示模块测试开始和结束时间。
- 报告表格增加用例描述、nodeid、失败类型、标签、开始时间、结束时间。
- 通过用例清空日志，避免报告过大。
- 写入 `prerun_results.txt`，用于预检测或平台读取。

面试回答模板：

```text
我不只是用pytest-html生成默认报告，还做过二次定制。比如在summary里展示测试环境、测试账号、通过率、开始结束时间；在表格里增加Description、nodeid、failinfo、tags、caseStartTime、caseEndTime。失败时我会区分AssertionError和非断言异常，并把结果写入prerun_results.txt，方便低代码平台或Jenkins后续读取。
```

### 4. 真实fixture与hook的分工

| 能力 | 在真实框架中的实现 | 为什么这么分 |
|------|--------------------|--------------|
| 读取用例docstring和nodeid，按用例写入环境变量 | autouse fixture | 这是每条用例的上下文，生命周期围绕单条用例 |
| HTML报告增加列和摘要 | pytest-html hook | 这是报告插件生命周期，不是某个用例要直接使用的资源 |
| 记录会话开始/结束时间 | session hook | 这是整个pytest会话级别的框架信息 |
| 采集失败异常、用例阶段耗时 | `pytest_runtest_makereport` | 只有report生成阶段能拿到完整结果 |

一句话：

```text
我的框架里，hook主要做报告和生命周期扩展；fixture主要做用例上下文和资源管理。
```

---

## 八、重点追问：启动浏览器用session fixture还是hook？

问题：

```text
以启动浏览器为例，启动浏览器都需要在session会话开始时启动、session会话结束时关闭并释放，通过hook和fixture都可以实现。这两种实现有什么区别？更推荐使用哪种方式？为什么？
```

### 1. 两种方式都能实现

#### 方式一：session fixture

```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
```

特点：

- 浏览器进程整个session启动一次。
- 每条用例创建独立context/page，隔离登录态、cookie、localStorage。
- 测试函数通过参数显式声明依赖。
- `yield`后自动关闭资源。

#### 方式二：hook

```python
browser = None
playwright = None

def pytest_sessionstart(session):
    global playwright, browser
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)

def pytest_sessionfinish(session, exitstatus):
    browser.close()
    playwright.stop()
```

特点：

- 也能做到session开始启动，session结束关闭。
- 但浏览器对象通常要靠全局变量、单例或其他间接方式给用例使用。
- 用例依赖不显式，维护和并发更容易出问题。

### 2. 核心区别

| 对比项 | session fixture | hook |
|--------|-----------------|------|
| 设计定位 | 资源管理 + 依赖注入 | pytest生命周期扩展 |
| 用例如何拿资源 | 测试函数声明参数，如 `def test_x(page)` | 通常从全局变量/单例取 |
| 依赖是否清晰 | 清晰，函数签名可见 | 不清晰，用例看不出依赖 |
| teardown | `yield`后自然清理 | 在 `pytest_sessionfinish` 手动清理 |
| 参数化 | 容易支持浏览器类型、headless、环境 | 不适合复杂参数化 |
| 并发执行 | 更容易和pytest-xdist/Playwright隔离模型配合 | 全局变量并发风险高 |
| 适合场景 | 浏览器、数据库连接、登录态等测试资源 | 报告、通知、全局初始化、插件集成 |

### 3. 推荐结论

更推荐使用 fixture 管理浏览器资源，尤其是测试用例需要直接使用 `browser/context/page` 时。

原因：

1. **显式依赖**：用例参数里写了 `page`，一眼知道该用例依赖浏览器。
2. **可组合**：`browser -> context -> page -> login_page` 可以层层组合。
3. **可参数化**：可以轻松支持不同浏览器、不同环境、headless开关。
4. **隔离更好**：session级browser节省启动成本，function级context/page保证用例隔离。
5. **清理自然**：`yield`后清理资源，逻辑和资源生命周期写在一起。
6. **更符合Playwright官方pytest用法**：官方插件通过fixture提供隔离的 `context/page`。

hook适合什么时候？

- 测试会话开始时初始化全局报告信息。
- 启动外部服务，但用例不直接依赖该对象。
- 记录session开始结束时间。
- 统一发送测试完成通知。
- 做pytest-html、allure、Jenkins、测试平台集成。

### 4. 面试标准回答

```text
如果浏览器对象要给测试用例使用，我更推荐用session fixture，而不是hook。因为fixture本身就是pytest的资源管理和依赖注入机制，用例通过参数声明依赖，资源从哪里来、什么时候释放都很清楚。比如browser可以是session级，只启动一次；context和page可以是function级，每条用例隔离cookie和登录态。这样既能减少浏览器启动成本，也能保证用例隔离。

hook也能在pytest_sessionstart启动浏览器、pytest_sessionfinish关闭浏览器，但它更适合做框架生命周期副作用，比如初始化报告、记录开始时间、推送通知。如果用hook启动浏览器，测试用例通常要从全局变量或单例里拿browser，依赖不显式，参数化和并发执行也更难维护。

所以我的原则是：资源给用例用，用fixture；pytest生命周期扩展，用hook。我的真实conftest.py也是这个思路，hook主要做pytest-html报告增强、session时间记录和失败信息采集，autouse fixture则围绕每条用例写入和清理用例描述上下文。
```

### 5. 追问：如果所有UI用例都要浏览器，能不能autouse？

可以，但要谨慎。

推荐：

```python
@pytest.fixture(scope="session")
def browser():
    ...

@pytest.fixture
def page(browser):
    ...
```

用例显式声明：

```python
def test_login(page):
    page.goto("https://example.com")
```

不优先推荐把浏览器page做成全局autouse，因为：

- 用例函数签名看不出依赖浏览器。
- 接口用例也可能被迫启动UI资源。
- 对混合接口/UI项目不够清晰。

---

## 九、pytest接入Jenkins和测试平台

典型流程：

```text
拉代码 -> 安装依赖 -> 准备环境和测试账号 -> pytest执行 -> 生成HTML/Allure/JUnit报告 -> Jenkins归档报告 -> 平台读取结果 -> 通知团队
```

结合你的真实框架可这样讲：

```text
我的接口自动化框架执行后会通过pytest-html生成报告，并通过hook把测试环境、测试账号、通过率、用例描述、nodeid、失败类型、标签、开始时间、结束时间写进报告。同时还会把预检测结果写入prerun_results.txt，方便平台或流水线读取。Jenkins侧只需要执行pytest命令、归档报告文件，并根据退出码或结果文件判断构建状态。
```

可背命令：

```bash
pytest -m smoke --html=report.html --self-contained-html
```

---

## 十、结合个人项目的完整表达

```text
我的pytest实践主要来自E10低代码平台的接口自动化框架和AI+接口自动化SKILL系统。框架里用fixture管理测试上下文、账号数据、环境变量和用例描述；用parametrize做接口数据驱动；用conftest.py集中放公共fixture和hook；用marker区分不同模块和标签；用pytest_runtest_makereport、pytest_html_results_summary、pytest_html_results_table_row等hook增强pytest-html报告。

一个真实例子是：用例函数的docstring会被autouse fixture和report hook读取，最终展示到HTML报告里；失败时通过pytest_runtest_makereport采集AssertionError，再在pytest-html表格里展示failinfo；同时记录caseStartTime和caseEndTime，最后写入prerun_results.txt给平台或预检测流程使用。

AI+接口自动化SKILL生成用例以后，我不会只停留在生成代码，而是用pytest执行最小范围验证，再根据失败信息修复生成结果，形成“AI生成 -> pytest验证 -> 失败定位 -> 修复沉淀”的闭环。这也是我简历里AI+测试效率提升能够落地的关键。
```

---

## 十一、常见面试追问与回答要点

### 1. fixture和setup/teardown区别？

```text
setup/teardown更像固定生命周期函数，粒度和组合能力有限；fixture是依赖注入机制，可以按函数参数显式声明依赖，可以设置scope，可以被其他fixture依赖，也可以用yield做清理。复杂测试框架里fixture更灵活。
```

### 2. conftest.py为什么不用import？

```text
conftest.py是pytest自动发现的本地插件文件。pytest收集用例时会按目录层级加载conftest.py，所以里面的fixture和hook可以直接生效，不需要测试文件手动import。
```

### 3. `pytest_runtest_makereport`能做什么？

```text
它在pytest生成测试报告时触发，可以拿到setup、call、teardown各阶段结果。常见用途是失败截图、异常信息采集、日志附件、用例耗时统计、自定义报告字段。我在框架里用它读取docstring、解码nodeid、采集AssertionError、记录case开始结束时间。
```

### 4. fixture scope越大越好吗？

```text
不是。scope越大，资源复用越好，但状态污染风险越高。像浏览器进程、数据库连接池可以session级；page、测试数据、登录态一般function级更安全。选择scope要平衡执行效率和用例隔离。
```

### 5. hook能不能替代fixture？

```text
不能简单替代。hook是pytest生命周期扩展，适合做报告、收集、通知、全局初始化；fixture是资源管理和依赖注入，适合给用例提供token、page、测试数据、数据库连接。两者可以配合，但职责不同。
```

---

## 十二、必背清单

- [ ] 能背出5个fixture scope：`function`、`class`、`module`、`package`、`session`。
- [ ] 能解释 `yield fixture` 的前置和后置清理。
- [ ] 能说清 `conftest.py` 自动发现、目录层级、无需import。
- [ ] 能区分 `parametrize`、fixture `params`、`indirect`。
- [ ] 能背出至少8个hook：`pytest_addoption`、`pytest_configure`、`pytest_collection_modifyitems`、`pytest_generate_tests`、`pytest_runtest_makereport`、`pytest_sessionstart`、`pytest_sessionfinish`、`pytest_terminal_summary`。
- [ ] 能结合真实框架讲 `pytest_runtest_makereport` 如何采集失败信息和用例时间。
- [ ] 能讲清 `pytest_html_results_summary` 和 `pytest_html_results_table_row` 如何增强报告。
- [ ] 能回答“启动浏览器用fixture还是hook”：资源给用例用选fixture，框架生命周期副作用选hook。
- [ ] 能把pytest和AI+接口自动化SKILL闭环联系起来：AI生成 -> pytest执行 -> 失败修复 -> 报告沉淀。

---

## 十三、3分钟面试版总结

```text
pytest我会从五个点讲：fixture、参数化、conftest、marker和hook。

fixture是资源管理和依赖注入机制，我会用它管理登录态、测试数据、环境变量、浏览器和清理逻辑。scope有function、class、module、package、session，选择时要平衡隔离和效率。比如浏览器进程可以session级，但page/context最好function级，保证用例隔离。

参数化方面，parametrize适合接口入参组合，fixture params适合环境、浏览器、账号这种资源组合，indirect适合参数先进入fixture做登录、造数据等复杂前置。

conftest.py是pytest自动发现的本地插件文件，不需要import，可以放公共fixture和hook。我的真实接口自动化框架里，conftest.py承担了账号读取、环境展示、报告增强、失败采集、用例描述注入等能力。

hook方面，我能说出具体函数，比如pytest_configure做配置初始化，pytest_collection_modifyitems修改收集到的用例，pytest_runtest_makereport采集执行结果，pytest_sessionstart/sessionfinish做会话级开始和收尾。我在真实框架里用pytest_runtest_makereport读取docstring、解码nodeid、采集AssertionError和用例执行时间，再通过pytest-html的hook写入HTML报告。

我的原则是：资源给用例用，用fixture；pytest生命周期扩展，用hook。AI+接口自动化SKILL生成用例后，也会通过pytest执行和报告反馈形成闭环。
```
