---
type: knowledge
title: "pytest入门总结"
source: "https://www.yuque.com/bbuer/cskf/irubysdhn0bk95va"
source_platform: yuque
category: "接口自动化测试"
created: 2026-06-30
updated: 2026-06-30
tags:
  - python
  - pytest
  - 测试框架
  - 自动化测试
status: mature
related:
  - "[[接口自动化测试日常问题记录]]"
  - "[[接口安全测试]]"
  - "[[接口自动化总结]]"
  - "[[Django 学习笔记]]"
  - "[[Flask学习笔记]]"
---

# pytest 入门总结

> 来源：语雀 - Python测试开发 | 抓取时间：2026-06-30

---

## 一、pytest.fixture

pytest 的 fixture 是一个强大的功能，允许你在测试函数或测试类之间共享通用测试数据、共享设置和清理代码等。fixture 可以是任何你需要的对象，如数据库连接、临时文件、配置数据等。

### 1. Fixture 基本使用

一个 fixture 通常是一个带有 `@pytest.fixture` 装饰器的函数。fixture 函数在被测试函数或其他 fixture 调用时运行，并返回一个值，该值可以作为参数传递给测试函数。

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

### 2. Fixture 作用范围

通过 `scope` 参数控制 fixture 的作用范围：

| scope 值 | 说明 |
|----------|------|
| `function` | 默认，每个测试函数执行一次 |
| `class` | 每个测试类执行一次 |
| `module` | 每个模块执行一次 |
| `session` | 整个测试会话执行一次 |

```python
@pytest.fixture(scope="module")
def module_scoped_data():
    print("Setting up module scoped data...")
    data = "This data is shared across the module."
    yield data
```

### 3. Fixture 参数化

使用 `params` 参数为 fixture 提供多个值，每个值运行一次测试函数：

```python
@pytest.fixture(params=[1, 2, 3])
def number(request):
    yield request.param

def test_numbers(number):
    assert number in [1, 2, 3]
    print(f"Testing with number: {number}")
```

### 4. Fixture 依赖关系

一个 fixture 可以依赖于另一个 fixture，按特定顺序设置和清理资源。

### 5. Fixture 自动使用

通过设置 `autouse=True`，使 fixture 在所有测试函数中自动使用，无需显式传递参数。

---

## 二、pytest.mark.parametrize 参数化

`@pytest.mark.parametrize` 允许以更简洁、更灵活的方式编写测试用例。

### 1. 多组输入测试同一逻辑

```python
@pytest.mark.parametrize("a, b, expected", [(1, 2, 3), (2, 3, 5), (3, 4, 7)])
def test_addition(a, b, expected):
    assert a + b == expected
```

### 2. 与 Fixture 结合 — 间接参数化

使用 `indirect=True` 时，参数不是直接输入值，而是需要调用 fixture 函数来生成的"间接"值。

### 3. 嵌套参数化

使用多个 `@pytest.mark.parametrize` 装饰器实现参数组合测试（如 2×2 = 4 个用例）。

---

## 三、pytest.ini 配置

`pytest.ini` 是 pytest 的配置文件，位于项目根目录，遵循 INI 文件格式（不能使用中文符号）。

| 配置项 | 说明 |
|--------|------|
| `addopts = -vs --tb=short --alluredir ./results` | 默认命令行参数 |
| `testpaths = tests` | 测试收集路径 |
| `python_files = test_*.py` | 测试模块匹配模式 |
| `python_classes = Test*` | 测试类匹配模式 |
| `python_functions = test_*` | 测试函数匹配模式 |
| `markers = eb_page: @pytest.mark.eb_page` | 自定义标记定义 |

> 注意：pytest 还支持 `pytest.toml` 或 `pyproject.toml` 存储配置。

---

## 四、常用参数命令

### 基础参数
- `-s`：显示 print 语句
- `-v`：详细模式
- `-q`：静默模式

### 选择测试用例
- `-k`：关键字表达式选择用例
- `-m`：标记选择用例
- `文件名::测试类::测试方法`：直接指定运行目标

### 执行控制
- `-x`：第一个失败时停止
- `--maxfail=num`：指定数量失败后停止
- `--reruns=num`：失败重跑次数（需 pytest-rerunfailures）
- `--lf`：重新运行上次失败的用例

### 多进程测试（pytest-xdist）
- `-n=num`：启用多进程测试

### 报告和统计
- `--durations=n`：显示运行时间
- `--tb=no/line/short/long/native/auto`：回溯格式
- `--html`：生成 HTML 报告（需 pytest-html）

### pytest.main() 方法

允许在 Python 脚本中直接运行 pytest 测试。返回值为整数（0=成功，非零=失败）。

---

## 五、常用插件

| 插件 | 功能 | 安装 |
|------|------|------|
| pytest-dependency | 设置用例依赖关系 | `pip install pytest-dependency` |
| pytest-sugar | 彩色输出 + 进度条 | `pip install pytest-sugar` |
| pytest-rerunfailures | 失败重跑指定次数 | `pip install pytest-rerunfailures` |
| pytest-repeat | 重复运行测试 | `pip install pytest-repeat` |
| pytest-html | 生成 HTML 测试报告 | `pip install pytest-html` |
| pytest-ordering | 修改用例执行顺序 | `pip install pytest-ordering` |
| pytest-xdist | 并行与分布式执行 | `pip install pytest-xdist` |

---

## 六、插件开发（hook 钩子函数）

### 插件分类
- **外部插件**：pip install 安装
- **本地插件**：conftest.py 存放
- **内置插件**：_pytest 目录加载

### hook 函数特点
- 在系统消息触发时被系统调用
- 自动触发机制
- 函数名称固定

### 常用 hook 函数

| hook 函数 | 阶段 |
|-----------|------|
| `pytest_collection_modifyitems` | 收集时期 — 修改收集到的测试项 |
| `pytest_addoption(parser)` | 初始化 — 添加自定义命令行选项 |
| `pytest_configure(config)` | 初始化 — 配置阶段 |
| `pytest_unconfigure(config)` | 结束 — 清理配置 |
| `pytest_sessionstart` | 初始化 — 测试会话开始 |
| `pytest_runtest_makereport` | 执行 — 创建测试结果报告 |

### pytest_html 的 hook 函数
- `pytest_html_results_table_row`
- `pytest_html_results_table_header`
- `pytest_html_results_table_html`
- `pytest_html_results_summary`

### 参考链接
- [pytest 官方 hook 文档](https://docs.pytest.org/en/stable/reference.html#hooks)
- [pytest hook 源码](https://docs.pytest.org/en/stable/_modules/_pytest/hookspec.html)

---

## 相关链接

- [[接口自动化总结]] — 接口自动化测试的完整知识体系
- [[Django 学习笔记]] — Django Web框架学习笔记
- [[Flask学习笔记]] — Flask Web框架学习笔记
- [[接口自动化测试日常问题记录]] — 接口自动化测试常见问题与解决方案
- [[接口安全测试]] — 接口安全测试方案与工具

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[接口自动化测试日常问题记录]] — AI测试主题关联
- [[接口安全测试]] — AI测试主题关联
- [[Django 学习笔记]] — AI测试主题关联
- [[Flask学习笔记]] — AI测试主题关联
- [[接口自动化总结]] — AI测试主题关联
- [[AI自动化开发计划]] — AI测试主题关联
- [[flask平台代码简介]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
