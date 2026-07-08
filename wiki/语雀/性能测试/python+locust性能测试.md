---
type: knowledge
title: "Python+Locust性能测试"
source: "https://www.yuque.com/bbuer/cskf/bxh3a4wi8crbdcyk"
source_platform: yuque
category: "性能测试"
created: 2026-06-30
updated: 2026-06-30
tags:
  - locust
  - python
  - 性能测试
  - 分布式
status: mature
related:
  - "[[性能测试基础]]"
  - "[[性能测试学习文件]]"
  - "[[Python基础总结]]"
  - "[[Python高级总结]]"
---

# Python+Locust性能测试

## 1. Locust 简介

### 什么是 Locust

Locust 是一个用 Python 编写的开源负载测试工具，使用代码定义用户行为，支持分布式运行。

### 核心特点

| 特点 | 说明 |
|------|------|
| 代码定义 | 用Python代码定义用户行为 |
| 分布式 | 支持多机分布式压测 |
| Web UI | 实时查看测试结果 |
| 轻量级 | 资源占用少 |
| 可扩展 | 灵活的事件钩子 |
| 协议支持 | HTTP、WebSocket、自定义协议 |

### 安装

```bash
# 安装locust
pip install locust

# 验证安装
locust --version

# 安装扩展(可选)
pip install locust-plugins
```

---

## 2. Locust 基础用法

### 最小示例

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # 请求间隔1-3秒

    @task
    def index(self):
        self.client.get("/")

    @task(3)  # 权重为3，执行频率是上面的3倍
    def about(self):
        self.client.get("/about")

# 运行: locust -f locustfile.py --host=http://example.com
```

### 完整示例

```python
from locust import HttpUser, task, between, events
import json

class APIUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://localhost:8000"

    def on_start(self):
        """用户启动时执行"""
        # 登录获取token
        response = self.client.post("/api/login", json={
            "username": "testuser",
            "password": "testpass"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.client.headers.update({
                "Authorization": f"Bearer {self.token}"
            })

    def on_stop(self):
        """用户停止时执行"""
        self.client.post("/api/logout")

    @task(10)
    def get_users(self):
        """获取用户列表"""
        with self.client.get("/api/users", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(5)
    def create_user(self):
        """创建用户"""
        import time
        username = f"user_{int(time.time() * 1000)}"
        self.client.post("/api/users", json={
            "username": username,
            "email": f"{username}@test.com"
        })

    @task(3)
    def get_user_detail(self):
        """获取用户详情"""
        user_id = 1
        self.client.get(f"/api/users/{user_id}")

    @task(2)
    def update_user(self):
        """更新用户"""
        user_id = 1
        self.client.put(f"/api/users/{user_id}", json={
            "username": "updated_user"
        })

    @task(1)
    def delete_user(self):
        """删除用户"""
        user_id = 999
        self.client.delete(f"/api/users/{user_id}")
```

---

## 3. Locust 高级特性

### TaskSet 任务集

```python
from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    def on_start(self):
        """任务集开始"""
        self.login()

    def login(self):
        response = self.client.post("/api/login", json={
            "username": "testuser",
            "password": "testpass"
        })
        self.token = response.json().get("token")

    @task(3)
    def get_profile(self):
        self.client.get("/api/profile", headers={
            "Authorization": f"Bearer {self.token}"
        })

    @task(1)
    def logout(self):
        self.client.post("/api/logout")
        self.interrupt()  # 退出任务集

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
```

### 嵌套任务集

```python
from locust import HttpUser, TaskSet, task, between

class BrowseProducts(TaskSet):
    @task(3)
    def list_products(self):
        self.client.get("/api/products")

    @task(2)
    def view_product(self):
        self.client.get("/api/products/1")

    @task(1)
    def stop(self):
        self.interrupt()

class ShoppingCart(TaskSet):
    @task(2)
    def view_cart(self):
        self.client.get("/api/cart")

    @task(1)
    def add_to_cart(self):
        self.client.post("/api/cart/items", json={
            "product_id": 1,
            "quantity": 1
        })

    @task(1)
    def stop(self):
        self.interrupt()

class ShoppingUser(HttpUser):
    tasks = {
        BrowseProducts: 5,
        ShoppingCart: 2
    }
    wait_time = between(1, 3)
```

### 事件钩子

```python
from locust import events

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """测试开始"""
    print("测试开始!")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """测试结束"""
    print("测试结束!")

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, 
               response, context, exception, **kwargs):
    """每次请求后触发"""
    if exception:
        print(f"请求失败: {name} - {exception}")

@events.init.add_listener
def on_init(environment, **kwargs):
    """初始化"""
    print("Locust 初始化完成")
```

### 自定义负载形状

```python
from locust import LoadTestShape

class StepLoadShape(LoadTestShape):
    """
    阶梯加压形状
    """
    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 1},
        {"duration": 120, "users": 50, "spawn_rate": 5},
        {"duration": 180, "users": 100, "spawn_rate": 10},
        {"duration": 240, "users": 200, "spawn_rate": 20},
        {"duration": 300, "users": 100, "spawn_rate": 10},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None  # 结束测试
```

---

## 4. 分布式运行

### 主从模式

```bash
# 启动Master
locust -f locustfile.py --master --host=http://example.com

# 启动Worker(可以在不同机器上)
locust -f locustfile.py --worker --master-host=192.168.1.100

# 启动多个Worker
locust -f locustfile.py --worker --master-host=192.168.1.100
locust -f locustfile.py --worker --master-host=192.168.1.100
```

### Docker 分布式

```yaml
# docker-compose.yml
version: '3.8'

services:
  master:
    image: locustio/locust
    ports:
      - "8089:8089"
    volumes:
      - ./locustfile.py:/mnt/locust/locustfile.py
    command: -f /mnt/locust/locustfile.py --master --host=http://target-service

  worker:
    image: locustio/locust
    volumes:
      - ./locustfile.py:/mnt/locust/locustfile.py
    command: -f /mnt/locust/locustfile.py --worker --master-host=master
    deploy:
      replicas: 4
    depends_on:
      - master
```

```bash
# 启动
docker-compose up -d

# 扩展Worker
docker-compose up -d --scale worker=8
```

---

## 5. 测试报告

### 实时Web UI

```bash
# 默认访问: http://localhost:8089
locust -f locustfile.py --host=http://example.com
```

Web UI 功能：
- 实时图表：RPS、响应时间、用户数
- 统计数据：请求成功率、失败率
- 下载报告：CSV格式

### 命令行模式

```bash
# 无Web UI模式
locust -f locustfile.py --host=http://example.com \
    --headless \
    --users 100 \
    --spawn-rate 10 \
    --run-time 5m \
    --csv=results

# 生成文件:
# results_stats.csv - 统计数据
# results_stats_history.csv - 历史数据
# results_failures.csv - 失败记录
```

### HTML报告

```python
# 通过事件生成HTML报告
import json
from locust import events

stats_data = []

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, 
               response, context, exception, **kwargs):
    stats_data.append({
        "type": request_type,
        "name": name,
        "response_time": response_time,
        "response_length": response_length,
        "success": exception is None
    })

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    with open("report.json", "w") as f:
        json.dump(stats_data, f, indent=2)
    print("报告已生成: report.json")
```

---

## 6. 最佳实践

### 测试脚本组织

```
performance-tests/
├── locustfile.py          # 主入口
├── tasks/                 # 任务模块
│   ├── __init__.py
│   ├── auth.py           # 认证相关
│   ├── users.py          # 用户相关
│   └── products.py       # 产品相关
├── data/                  # 测试数据
│   ├── users.csv
│   └── products.csv
├── config/                # 配置文件
│   └── settings.py
└── reports/               # 测试报告
```

### 参数化数据

```python
import csv
from locust import HttpUser, task, between

def load_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

users_data = load_csv('data/users.csv')

class DataDrivenUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        import random
        self.user = random.choice(users_data)

    @task
    def login(self):
        self.client.post("/api/login", json={
            "username": self.user["username"],
            "password": self.user["password"]
        })
```

### 断言和校验

```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_users(self):
        with self.client.get("/api/users", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"状态码错误: {response.status_code}")
            elif len(response.json().get("data", [])) == 0:
                response.failure("返回数据为空")
            else:
                response.success()

    @task
    def get_user(self):
        with self.client.get("/api/users/1", catch_response=True) as response:
            try:
                data = response.json()
                if "id" not in data:
                    response.failure("缺少id字段")
                else:
                    response.success()
            except Exception as e:
                response.failure(f"JSON解析失败: {e}")
```

---

## 相关链接

- [[Python基础总结]] — Python编程基础知识总结
- [[Python高级总结]] — Python高级特性与设计模式

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[性能测试基础]] — AI测试主题关联
- [[Python基础总结]] — AI测试主题关联
- [[性能测试学习文件]] — AI测试主题关联
- [[Python高级总结]] — AI测试主题关联
- [[设计模式]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[UI自动化测试日常问题记录]] — AI测试主题关联
- [[移动端自动化框架搭建问题点记录]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
