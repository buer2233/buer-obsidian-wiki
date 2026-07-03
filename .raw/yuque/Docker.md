# Docker

> 来源: https://www.yuque.com/bbuer/cskf/rplh2y8stwza8m1i
> 抓取时间: 2026-06-30
> 分组: 云原生

---

## 安装步骤

### CentOS安装Docker

```bash
# 卸载旧版本
sudo yum remove docker \
  docker-client \
  docker-client-latest \
  docker-common \
  docker-latest \
  docker-latest-logrotate \
  docker-logrotate \
  docker-engine

# 安装依赖
sudo yum install -y yum-utils

# 添加Docker仓库
sudo yum-config-manager \
  --add-repo \
  https://download.docker.com/linux/centos/docker-ce.repo

# 安装Docker
sudo yum install docker-ce docker-ce-cli containerd.io

# 启动Docker
sudo systemctl start docker

# 设置开机自启
sudo systemctl enable docker

# 验证安装
docker --version
```

### Ubuntu安装Docker

```bash
# 卸载旧版本
sudo apt-get remove docker docker-engine docker.io containerd runc

# 更新apt
sudo apt-get update

# 安装依赖
sudo apt-get install \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

# 添加Docker GPG密钥
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 添加仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# 验证安装
docker --version
```

### 配置镜像加速

```bash
# 编辑daemon.json
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://registry.docker-cn.com"
  ]
}
EOF

# 重启Docker
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 容器命令

### 容器生命周期命令

```bash
# 创建并启动容器
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

# 常用参数
docker run -d --name mycontainer -p 8080:80 nginx
# -d: 后台运行
# --name: 指定容器名称
# -p: 端口映射（宿主机端口:容器端口）
# -v: 挂载卷
# -e: 设置环境变量
# --restart: 重启策略（always/unless-stopped/no）

# 启动已停止的容器
docker start container_name

# 停止运行中的容器
docker stop container_name

# 重启容器
docker restart container_name

# 暂停容器
docker pause container_name

# 恢复暂停的容器
docker unpause container_name

# 删除容器
docker rm container_name

# 强制删除运行中的容器
docker rm -f container_name
```

### 容器操作命令

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a

# 进入容器
docker exec -it container_name /bin/bash

# 查看容器日志
docker logs container_name
docker logs -f container_name  # 持续输出
docker logs --tail 100 container_name  # 最后100行

# 查看容器详情
docker inspect container_name

# 查看容器资源使用
docker stats

# 从容器复制文件到宿主机
docker cp container_name:/path/file /host/path

# 从宿主机复制文件到容器
docker cp /host/path container_name:/path/file

# 查看容器端口映射
docker port container_name

# 更新容器配置
docker update --restart=always container_name
```

## 镜像管理命令

```bash
# 搜索镜像
docker search image_name

# 拉取镜像
docker pull image_name:tag

# 推送镜像
docker push image_name:tag

# 查看本地镜像
docker images

# 查看镜像详情
docker inspect image_name

# 删除镜像
docker rmi image_name

# 强制删除镜像
docker rmi -f image_name

# 删除所有未使用的镜像
docker image prune

# 删除所有镜像
docker rmi $(docker images -q)

# 给镜像打标签
docker tag old_image:tag new_image:tag

# 构建镜像
docker build -t image_name:tag .

# 从容器创建镜像
docker commit container_name image_name:tag

# 导出镜像
docker save -o image.tar image_name:tag

# 导入镜像
docker load -i image.tar

# 查看镜像历史
docker history image_name
```

### Dockerfile

```dockerfile
# 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "app.py"]
```

## 一行命令启用服务

### Nginx

```bash
docker run -d --name nginx -p 80:80 -v /data/nginx/conf:/etc/nginx/conf.d -v /data/nginx/html:/usr/share/nginx/html nginx
```

### MySQL

```bash
docker run -d --name mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -v /data/mysql/data:/var/lib/mysql \
  -v /data/mysql/conf:/etc/mysql/conf.d \
  mysql:8.0
```

### Jenkins

```bash
docker run -d --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /data/jenkins:/var/jenkins_home \
  jenkins/jenkins:lts
```

### Jira

```bash
docker run -d --name jira \
  -p 8080:8080 \
  -v /data/jira:/var/atlassian/application-data/jira \
  atlassian/jira-software
```

### TestLink

```bash
docker run -d --name testlink \
  -p 8080:80 \
  -e TESTLINK_DATABASE_HOST=mysql \
  -e TESTLINK_DATABASE_USER=testlink \
  -e TESTLINK_DATABASE_PASSWORD=testlink \
  bitnami/testlink:latest
```

## Docker与虚拟机区别

| 特性 | Docker容器 | 虚拟机 |
|------|-----------|-------|
| 启动速度 | 秒级 | 分钟级 |
| 性能 | 接近原生 | 有一定损耗 |
| 硬盘占用 | MB级 | GB级 |
| 隔离性 | 进程级隔离 | 系统级隔离 |
| 操作系统 | 共享宿主机内核 | 独立操作系统 |
| 密度 | 单机可运行上千个 | 单机几十个 |
| 交付标准 | Docker镜像 | VM镜像 |
| 资源占用 | 少 | 多 |

### Docker的优势

1. **更快速的交付和部署**
2. **更高效的虚拟化**
3. **更轻松的迁移和扩展**
4. **更简单的管理**

### Docker的局限

1. **隔离性不如虚拟机**
2. **不适合运行Windows应用**
3. **存储管理复杂**

## 网络模式

### bridge（桥接模式）

默认网络模式。容器拥有独立的Network Namespace，通过docker0虚拟网桥与宿主机通信。

```bash
docker run -d --network bridge --name mycontainer nginx
```

### host（主机模式）

容器与宿主机共享Network Namespace，直接使用宿主机的IP和端口。

```bash
docker run -d --network host --name mycontainer nginx
```

### none（无网络模式）

容器拥有独立的Network Namespace，但不进行任何网络配置。

```bash
docker run -d --network none --name mycontainer nginx
```

### container（容器模式）

与指定的容器共享Network Namespace。

```bash
docker run -d --network container:existing_container --name mycontainer nginx
```

### 自定义网络

```bash
# 创建自定义网络
docker network create mynetwork

# 使用自定义网络
docker run -d --network mynetwork --name mycontainer nginx

# 查看网络
docker network ls

# 查看网络详情
docker network inspect mynetwork

# 连接容器到网络
docker network connect mynetwork container_name

# 断开容器与网络的连接
docker network disconnect mynetwork container_name
```

## 镜像（Image）

### 镜像分层

Docker镜像采用分层存储机制，每一层都是只读的。当容器启动时，Docker会在最顶层添加一个可写层。

### 镜像仓库

- **Docker Hub**：官方公共仓库
- **私有仓库**：Harbor、Nexus等

### 最佳实践

1. **使用精简基础镜像**：如alpine、slim版本
2. **合并RUN指令**：减少镜像层数
3. **使用.dockerignore**：排除不必要的文件
4. **多阶段构建**：减小最终镜像大小
5. **及时清理缓存**：减小镜像体积

```dockerfile
# 多阶段构建示例
FROM golang:1.19 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o main .

FROM alpine:3.17
WORKDIR /app
COPY --from=builder /app/main .
CMD ["./main"]
```
