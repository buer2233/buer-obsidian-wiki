# pytest入门总结

> 来源: https://www.yuque.com/bbuer/cskf/irubysdhn0bk95va
> 抓取时间: 2026-06-30
> 分组: 接口自动化测试

---

一、pytest.fixture

pytest 的 fixture 是一个强大的功能，它允许你在测试函数或测试类之间共享通用测试数据、共享设置和清理代码等。fixture 可以是任何你需要的对象，如数据库连接、临时文件、配置数据等。fixture 的主要优点是它们可以配置为在不同的测试函数、模块、类或整个测试会话之间共享。

1、Fixture 的基本使用

一个 fixture 通常是一个带有 @pytest.fixture 装饰器的函数。fixture 函数在被测试函数或其他 fixture 调用时运行，并返回一个值，该值可以作为参数传递给测试函数。

示例：

```python
import pytest

@pytest.fixture
def example_data():
    print("Setting up example data...")
    data = "This is an example"
    print("Example data set up.")
    yield data

def test_example_data(example_data):
    assert example_data == "This is an example"
    print("Test using example data.")
```

在这个例子中，example_data 是一个 fixture。当 test_example_data 函数被调用时，example_data fixture 会首先运行，并返回字符串 "This is an example"。然后，这个值被传递给 test_example_data 函数，并在其中使用。

2、Fixture 的作用范围

通过 scope 参数，你可以控制 fixture 的作用范围。可能的值有：function（默认）、class、module 和 session。

示例：

```python
import pytest

@pytest.fixture(scope="module")
def module_scoped_data():
    print("Setting up module scoped data...")
    data = "This data is shared across the module."
    yield data

def test_module_data_1(module_scoped_data):
    assert module_scoped_data == "This data is shared across the module."

def test_module_data_2(module_scoped_data):
    assert module_scoped_data == "This data is shared across the module."
```

在这个例子中，module_scoped_data fixture 的作用范围是模块级别的。因此，它只会在第一个测试函数运行前设置一次，并在所有测试函数运行完毕后清理一次。

3、Fixture 的参数化

使用 params 参数，你可以为 fixture 提供多个值，并为每个值运行一次测试函数。当需要对参数进行二次处理加工后再使用时，建议使用 Fixture 的参数化方法。

示例：

```python
import pytest

@pytest.fixture(params=[1, 2, 3])
def number(request):
    yield request.param

def test_numbers(number):
    assert number in [1, 2, 3]
    print(f"Testing with number: {number}")
```

在这个例子中，test_numbers 函数会为 number fixture 的每个值（1、2、3）运行一次。

4、Fixture 的依赖关系

一个 fixture 可以依赖于另一个 fixture。这允许你按特定的顺序设置和清理资源。

在这个例子中，user fixture 依赖于 database_connection fixture。因此，database_connection 会首先运行，然后 user 才会运行。

5、Fixture 的自动使用

通过设置 autouse=True，你可以使 fixture 在所有测试函数中自动使用，而无需显式地将其作为参数传递。

在这个例子中，setup_and_teardown fixture 会在每个测试函数运行前和运行后自动执行。

---

二、pytest.mark.parametrize 参数化

pytest 参数化 @pytest.mark.parametrize 是一个非常有用的工具，它允许我们以更简洁、更灵活的方式编写测试用例。通过合理地使用参数化，我们可以减少重复的代码，提高测试效率，并确保软件在各种条件下的稳定性和正确性。

1、多组输入测试同一逻辑并自定义用例ID

当我们需要对同一逻辑使用多组不同的输入数据进行测试时，可以使用参数化。例如，测试一个加法函数，我们可以使用多组数字来验证它的正确性。

示例：一共3个参数(a, b, expected), 执行3用例

2、与Fixture结合使用的方式1:间接参数化（Indirect Parametrization）

当你使用 indirect=True 时，你实际上是在告诉 pytest：这个参数不是一个直接的输入值，而是一个需要调用一个 fixture 函数来生成的"间接"值。

3、与Fixture结合使用的方式2

有时，我们可能需要在测试中使用一些预置的数据或条件，而这些数据或条件可以通过 fixture 来提供。在这种情况下，我们可以将参数化与 fixture 结合使用。

示例：3个fixture的参数组合2个参数化用例,一共参数化执行6用例

4、多个参数组合测试:嵌套参数化（Nested Parametrization）

在某些情况下，我们可能需要将多个参数进行组合测试。这可以通过在测试函数上使用多个 @pytest.mark.parametrize 装饰器来实现。

示例：2 X 2 执行4用例

---

三、pytest.ini

pytest.ini 是 pytest 测试框架用于配置其运行行为的一个配置文件。尽管这个文件是可选的，但它在大型项目或需要特定配置的测试中非常有用。pytest.ini 文件通常位于项目的根目录下，并且它遵循标准的 INI 文件格式（不能使用任何中文符号，包括汉字、空格、引号、冒号等等）。

常用配置项：

1、addopts = -vs --tb=short --alluredir ./results

命令行选项列表，用作添加默认参数。-v 详细输出，--tb=short 简洁回溯，--alluredir ./results 指定 allure 报告地址。

2、testpaths = tests

pytest 将只从这些路径中收集测试。

3、python_files = test_*.py

匹配测试模块的模式列表。

4、python_classes = Test*

匹配测试类的模式列表。

5、python_functions = test_*

匹配测试函数的模式列表。

6、markers = eb_page: @pytest.mark.eb_page

自定义标记定义列表，可用 pytest -m 选项基于标记选择或排除测试。

注意：pytest 还支持 pytest.toml 或 pyproject.toml 存储配置。

7、log日志配置

---

四、pytest的常用参数命令

1. 基础参数
- -s：允许在输出中显示 print 语句
- -v：详细模式
- -q：静默模式

2. 选择测试用例
- -k：通过关键字表达式选择用例
- -m：通过标记选择用例
- 文件名::测试类::测试方法：直接指定运行目标

3. 执行控制
- -x：第一个失败时停止
- --maxfail=num：指定数量失败后停止
- --reruns=num：失败重跑次数（需 pytest-rerunfailures）
- --lf：重新运行上次失败的用例

4. 多进程测试（pytest-xdist）
- -n=num：启用多进程测试

5. 报告和统计
- --durations=n：显示运行时间
- --tb=no/line/short/long/native/auto：回溯格式
- --html：生成 HTML 报告（需 pytest-html）
- --self-contained-html：HTML 报告附带资源

6. pytest.main() 方法

允许在 Python 脚本中直接运行 pytest 测试。返回值为整数（0=成功，非零=失败）。

---

五、pytest的常用插件

- pytest-dependency：设置用例依赖关系
- pytest-sugar：彩色输出 + 进度条
- pytest-rerunfailures：失败重跑指定次数
- pytest-repeat：重复运行测试
- pytest-html：生成 HTML 测试报告
- pytest-ordering：修改用例执行顺序
- pytest-xdist：并行与分布式执行

---

六、pytest插件开发（hook钩子函数）

1、插件分类
- 外部插件：pip install 安装
- 本地插件：conftest.py 存放
- 内置插件：_pytest 目录加载

2、hook 函数特点
- 在系统消息触发时被系统调用
- 自动触发机制
- 函数名称固定

3、常用自带 hook 函数
- pytest_collection_modifyitems：修改收集到的测试项（收集时期）
- pytest_addoption(parser)：添加自定义命令行选项
- pytest_configure(config)：配置阶段（初始化时期）
- pytest_unconfigure(config)：清理配置（结束时期）
- pytest_sessionstart：测试会话开始（初始化时期）
- pytest_runtest_makereport：创建测试结果报告（执行时期）

4、pytest_html 的 hook 函数
- pytest_html_results_table_row
- pytest_html_results_table_header
- pytest_html_results_table_html
- pytest_html_results_summary

参考链接：
- https://docs.pytest.org/en/stable/reference.html#hooks
- https://github.com/pytest-dev/pytest/issues/3261
