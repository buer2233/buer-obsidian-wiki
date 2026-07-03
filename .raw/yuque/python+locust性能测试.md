# python+locust性能测试

> 来源: https://www.yuque.com/bbuer/cskf/bxh3a4wi8crbdcyk
> 抓取时间: 2026-06-30
> 分组: 性能测试

---

## Locust简介

Locust是一个开源的负载测试工具，使用Python编写测试脚本，可以模拟数百万用户对系统进行压力测试。

### 官方网站

- GitHub：https://github.com/locustio/locust
- 官方文档：https://docs.locust.io/

### 安装

```bash
pip install locust
```

## Locust的特点

### 1. 简单易用

Locust使用纯Python编写测试脚本，不需要学习特定的脚本语言或GUI工具。只需要了解基本的Python语法即可上手。

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        self.client.get("/")

    @task(3)
    def about(self):
        self.client.get("/about")
```

### 2. 分布式测试

Locust支持分布式测试，可以在多台机器上运行负载测试，从而模拟大量并发用户。

```bash
# 主节点
locust -f locustfile.py --master

# 从节点
locust -f locustfile.py --slave --master-host=192.168.1.100
```

### 3. 实时监控

Locust提供了一个简洁的Web界面，可以实时监控测试进度和结果。

```bash
# 启动Web界面（默认端口8089）
locust -f locustfile.py

# 指定端口
locust -f locustfile.py --port 9000
```

Web界面展示的信息包括：
- 当前活跃用户数
- 每秒请求数（RPS）
- 响应时间分布
- 错误率
- 各接口的详细统计

### 4. 跨平台

Locust基于Python开发，可以在任何支持Python的平台上运行：
- Windows
- macOS
- Linux

### 5. 功能强大

Locust提供了丰富的功能：

- **自定义负载形状**：可以自定义用户增长的形状
- **事件钩子**：支持在测试各阶段执行自定义逻辑
- **多种请求方式**：支持HTTP/HTTPS、REST API等
- **数据驱动**：支持从文件或数据库读取测试数据
- **断言验证**：支持对响应结果进行验证
- **统计报告**：支持导出CSV格式的测试报告

## 基本使用

### Locust脚本结构

```python
from locust import HttpUser, task, between, events

class MyUser(HttpUser):
    # 用户等待时间：1-3秒
    wait_time = between(1, 3)

    # 用户权重（用于控制不同类型用户的比例）
    weight = 1

    # 目标主机
    host = "http://example.com"

    # 测试开始前执行
    def on_start(self):
        """用户启动时执行，用于登录等操作"""
        self.client.post("/login", json={
            "username": "test",
            "password": "123456"
        })

    # 测试结束后执行
    def on_stop(self):
        """用户停止时执行，用于清理操作"""
        self.client.post("/logout")

    @task(3)  # 权重为3
    def index(self):
        self.client.get("/")

    @task(1)  # 权重为1
    def about(self):
        self.client.get("/about")

    @task(2)
    def api_test(self):
        with self.client.get("/api/data", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Request failed!")
```

### SequentialTaskSet（顺序任务集）

```python
from locust import HttpUser, SequentialTaskSet, task, between

class UserBehavior(SequentialTaskSet):
    @task
    def first_task(self):
        self.client.get("/step1")

    @task
    def second_task(self):
        self.client.get("/step2")

    @task
    def third_task(self):
        self.client.get("/step3")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
```

### 自定义负载形状

```python
from locust import LoadTestShape

class StepLoadShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 1},
        {"duration": 120, "users": 50, "spawn_rate": 5},
        {"duration": 180, "users": 100, "spawn_rate": 10},
        {"duration": 240, "users": 100, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])
        return None
```

## 命令行参数

```bash
# 基本启动
locust -f locustfile.py

# 指定参数
locust -f locustfile.py \
  --host http://example.com \
  --users 100 \
  --spawn-rate 10 \
  --run-time 5m \
  --headless  # 无Web界面模式

# 生成报告
locust -f locustfile.py \
  --host http://example.com \
  --users 100 \
  --spawn-rate 10 \
  --run-time 5m \
  --headless \
  --csv=report \
  --html=report.html
```

## 常用命令行选项

| 参数 | 说明 |
|------|------|
| `-f` | 指定Locust文件 |
| `--host` | 指定目标主机 |
| `--users` | 模拟用户数 |
| `--spawn-rate` | 每秒启动用户数 |
| `--run-time` | 运行时间 |
| `--headless` | 无Web界面模式 |
| `--csv` | CSV报告前缀 |
| `--html` | HTML报告文件 |
| `--master` | 以主节点模式运行 |
| `--slave` | 以从节点模式运行 |
| `--master-host` | 主节点地址 |
| `--master-port` | 主节点端口 |
