---
type: knowledge
title: "Docker"
source: "https://www.yuque.com/bbuer/cskf/rplh2y8stwza8m1i"
source_platform: yuque
category: "云原生"
created: 2026-06-30
updated: 2026-06-30
tags:
  - docker
  - 容器
  - 云原生
  - devops
status: mature
related:
  - "[[Jenkins全攻略]]"
  - "[[Linux总结]]"
---

# Docker

## 1. Docker 安装步骤

### Ubuntu 安装

```bash
# 卸载旧版本
sudo apt-get remove docker docker-engine docker.io containerd runc

# 更新apt包索引
sudo apt-get update

# 安装依赖
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 添加Docker官方GPG密钥
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 设置仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 验证安装
sudo docker run hello-world
```

### CentOS 安装

```bash
# 卸载旧版本
sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

# 安装yum-utils
sudo yum install -y yum-utils

# 设置仓库
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装Docker Engine
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 启动Docker
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
sudo docker run hello-world
```

### 配置镜像加速

```bash
# 创建配置文件
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF

# 重启Docker
sudo systemctl daemon-reload
sudo systemctl restart docker
```

---

## 2. 容器命令

### 容器生命周期

```bash
# 创建并启动容器
docker run -d --name mynginx -p 80:80 nginx

# 参数说明
# -d: 后台运行
# --name: 容器名称
# -p: 端口映射 (主机:容器)
# -v: 数据卷挂载
# -e: 环境变量
# --restart: 重启策略

# 启动容器
docker start mynginx

# 停止容器
docker stop mynginx

# 重启容器
docker restart mynginx

# 删除容器
docker rm mynginx

# 强制删除运行中的容器
docker rm -f mynginx

# 删除所有停止的容器
docker container prune
```

### 容器操作

```bash
# 查看运行中的容器
docker ps

# 查看所有容器
docker ps -a

# 查看容器日志
docker logs mynginx
docker logs -f mynginx  # 实时跟踪
docker logs --tail 100 mynginx  # 最后100行

# 进入容器
docker exec -it mynginx /bin/bash
docker exec -it mynginx sh

# 查看容器详情
docker inspect mynginx

# 查看容器资源使用
docker stats mynginx

# 查看容器进程
docker top mynginx

# 复制文件
docker cp mynginx:/etc/nginx/nginx.conf ./nginx.conf
docker cp ./index.html mynginx:/usr/share/nginx/html/

# 查看容器端口映射
docker port mynginx

# 暂停/恢复容器
docker pause mynginx
docker unpause mynginx
```

### 常用 run 参数

```bash
# 端口映射
docker run -p 8080:80 nginx
docker run -p 127.0.0.1:8080:80 nginx
docker run -p 8080:80/udp nginx

# 数据卷挂载
docker run -v /host/path:/container/path nginx
docker run -v myvolume:/data nginx

# 环境变量
docker run -e MYSQL_ROOT_PASSWORD=123456 mysql

# 限制资源
docker run --memory=512m --cpus=1 nginx

# 重启策略
docker run --restart=always nginx
docker run --restart=on-failure:5 nginx

# 网络
docker run --network=mynetwork nginx

# 特权模式
docker run --privileged nginx
```

---

## 3. 镜像命令

### 镜像管理

```bash
# 拉取镜像
docker pull nginx
docker pull nginx:1.24
docker pull mysql:8.0

# 查看本地镜像
docker images
docker image ls

# 搜索镜像
docker search nginx

# 删除镜像
docker rmi nginx
docker image rm nginx:1.24

# 删除所有未使用的镜像
docker image prune -a

# 给镜像打标签
docker tag nginx:latest myregistry/nginx:v1

# 推送镜像
docker push myregistry/nginx:v1

# 保存镜像为文件
docker save -o nginx.tar nginx:latest

# 从文件加载镜像
docker load -i nginx.tar

# 查看镜像详情
docker inspect nginx

# 查看镜像历史
docker history nginx

# 构建镜像
docker build -t myapp:v1 .
docker build -f Dockerfile.prod -t myapp:prod .
```

### Dockerfile 编写

```dockerfile
# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

# 启动命令
CMD ["python", "app.py"]
```

---

## 4. 一行命令服务

### 常用一行命令

```bash
# 启动Nginx
docker run -d -p 80:80 nginx

# 启动MySQL
docker run -d \
  --name mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -v /data/mysql:/var/lib/mysql \
  mysql:8.0

# 启动Redis
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7-alpine

# 启动PostgreSQL
docker run -d \
  --name postgres \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=123456 \
  postgres:15

# 启动MongoDB
docker run -d \
  --name mongo \
  -p 27017:27017 \
  mongo:6

# 启动Jenkins
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

# 启动GitLab
docker run -d \
  --name gitlab \
  -p 80:80 \
  -p 443:443 \
  -p 22:22 \
  gitlab/gitlab-ce

# 启动SonarQube
docker run -d \
  --name sonarqube \
  -p 9000:9000 \
  sonarqube:lts-community
```

### Docker Compose 示例

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:123456@db:5432/myapp
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=123456
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web

volumes:
  postgres_data:
```

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f web

# 停止所有服务
docker-compose down
```

---

## 5. Docker 与虚拟机区别

### 对比表

| 特性 | Docker容器 | 虚拟机 |
|------|-----------|--------|
| 启动速度 | 秒级 | 分钟级 |
| 性能 | 接近原生 | 有损耗 |
| 硬盘占用 | MB级 | GB级 |
| 隔离性 | 进程级隔离 | 系统级隔离 |
| 操作系统 | 共享宿主机内核 | 独立OS |
| 密度 | 单机可运行上千个 | 单机十几个 |
| 安全性 | 较弱 | 较强 |
| 镜像大小 | 较小 | 较大 |
| 运行形态 | 容器 | 完整虚拟机 |

### 架构区别

```
虚拟机架构:
┌──────────────────────────────────┐
│           应用A    应用B         │
│         ┌─────┐  ┌─────┐       │
│         │Bins │  │Bins │       │
│         │Libs │  │Libs │       │
│         ├─────┤  ├─────┤       │
│         │Guest│  │Guest│       │
│         │ OS  │  │ OS  │       │
├─────────┴─────┴──┴─────┴───────┤
│           Hypervisor            │
├─────────────────────────────────┤
│          Host OS                │
├─────────────────────────────────┤
│          Infrastructure         │
└─────────────────────────────────┘

Docker架构:
┌──────────────────────────────────┐
│           应用A    应用B         │
│         ┌─────┐  ┌─────┐       │
│         │Bins │  │Bins │       │
│         │Libs │  │Libs │       │
├─────────┴─────┴──┴─────┴───────┤
│          Docker Engine          │
├─────────────────────────────────┤
│          Host OS                │
├─────────────────────────────────┤
│          Infrastructure         │
└─────────────────────────────────┘
```

---

## 6. Docker 网络模式

### 网络类型

| 网络模式 | 说明 | 使用场景 |
|----------|------|----------|
| bridge | 桥接网络(默认) | 容器间通信 |
| host | 共享宿主机网络 | 高性能网络 |
| none | 无网络 | 安全隔离 |
| overlay | 覆盖网络 | 跨主机通信 |
| macvlan | MAC地址分配 | 直接使用物理网络 |

### 网络操作

```bash
# 查看网络
docker network ls

# 创建自定义网络
docker network create mynetwork

# 创建指定子网的网络
docker network create --subnet=172.20.0.0/16 mynetwork

# 启动容器时指定网络
docker run -d --network=mynetwork --name=web nginx

# 连接容器到网络
docker network connect mynetwork mycontainer

# 断开容器网络
docker network disconnect mynetwork mycontainer

# 查看网络详情
docker network inspect mynetwork

# 删除网络
docker network rm mynetwork

# 删除未使用的网络
docker network prune
```

### 容器间通信

```bash
# 使用自定义网络(推荐)
docker network create mynet
docker run -d --name web --network=mynet nginx
docker run -d --name api --network=mynet myapi

# 在api容器中可以直接通过名称访问web
curl http://web:80

# 使用link(已废弃)
docker run -d --name web nginx
docker run -d --name api --link web:web myapi
```

---

## 7. Docker 镜像

### 镜像层

```
镜像层结构:
┌─────────────────────────┐
│   可写层 (Container)    │  ← 运行时添加
├─────────────────────────┤
│   应用代码层            │  ← COPY . .
├─────────────────────────┤
│   依赖安装层            │  ← RUN pip install
├─────────────────────────┤
│   基础镜像层            │  ← FROM python:3.11
└─────────────────────────┘
```

### 镜像优化

```dockerfile
# 优化前
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

# 优化后
FROM python:3.11-slim  # 使用slim版本
WORKDIR /app
COPY requirements.txt .  # 先复制依赖文件
RUN pip install --no-cache-dir -r requirements.txt  # 利用缓存
COPY . .  # 最后复制代码
CMD ["python", "app.py"]
```

### 多阶段构建

```dockerfile
# 构建阶段
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# 运行阶段
FROM alpine:3.18
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
CMD ["./main"]
```

### 常用基础镜像

| 镜像 | 大小 | 说明 |
|------|------|------|
| alpine | ~5MB | 最小Linux |
| debian:slim | ~80MB | 精简版Debian |
| ubuntu | ~70MB | Ubuntu基础 |
| python:3.11-slim | ~130MB | Python精简版 |
| node:18-alpine | ~110MB | Node.js精简版 |
| nginx:alpine | ~40MB | Nginx精简版 |

---

## 相关链接

- [[Linux总结]] — Linux操作系统基础知识总结

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[Jenkins全攻略]] — AI测试主题关联
- [[Linux总结]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[常用SKILL总结]] — AI测试主题关联
- [[AI产品测试]] — AI测试主题关联
- [[Flask学习笔记]] — AI测试主题关联
- [[测试平台基础]] — AI测试主题关联
- [[02_pytest必背学习资料]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
