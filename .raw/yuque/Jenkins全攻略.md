# Jenkins全攻略

> 来源: https://www.yuque.com/bbuer/cskf/rc96siuwbo66is17
> 抓取时间: 2026-06-30
> 分组: 云原生

---

## 安装

### 方式一：使用yum安装（CentOS/RHEL）

```bash
# 添加Jenkins仓库
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

# 安装Jenkins
sudo yum install jenkins

# 安装Java（Jenkins依赖）
sudo yum install java-11-openjdk
```

### 方式二：使用apt安装（Ubuntu/Debian）

```bash
# 添加Jenkins仓库
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

# 安装Jenkins
sudo apt-get update
sudo apt-get install jenkins
```

### 方式三：使用Docker安装

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

### 方式四：使用WAR包安装

```bash
# 下载WAR包
wget https://get.jenkins.io/war-stable/latest/jenkins.war

# 启动Jenkins
java -jar jenkins.war --httpPort=8080
```

## 配置文件

### 主配置文件

```bash
# CentOS/RHEL
/etc/sysconfig/jenkins

# Ubuntu/Debian
/etc/default/jenkins
```

### 重要配置项

```bash
# Jenkins运行端口
JENKINS_PORT="8080"

# Jenkins运行用户
JENKINS_USER="jenkins"

# Jenkins主目录
JENKINS_HOME="/var/lib/jenkins"

# Java选项
JENKINS_JAVA_OPTIONS="-Djava.awt.headless=true -Xmx2048m"
```

### Jenkins主目录结构

```
/var/lib/jenkins/
├── config.xml           # Jenkins主配置
├── users/               # 用户配置
├── jobs/                # 任务配置
├── workspace/           # 工作空间
├── plugins/             # 插件目录
├── secrets/             # 密钥
├── logs/                # 日志
└── war/                 # WAR包
```

## 启动

### 使用systemctl管理

```bash
# 启动Jenkins
sudo systemctl start jenkins

# 停止Jenkins
sudo systemctl stop jenkins

# 重启Jenkins
sudo systemctl restart jenkins

# 查看状态
sudo systemctl status jenkins

# 设置开机自启
sudo systemctl enable jenkins
```

### 使用Docker管理

```bash
# 启动
docker start jenkins

# 停止
docker stop jenkins

# 重启
docker restart jenkins

# 查看日志
docker logs jenkins
```

## Web页面配置

### 1. 初始密码获取

首次启动Jenkins后，需要输入初始管理员密码：

```bash
# 查看初始密码
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### 2. 插件安装

推荐安装的插件：

**核心插件：**
- Blue Ocean：现代化的UI界面
- Pipeline：流水线支持
- Git：Git集成
- Credentials：凭证管理

**构建工具插件：**
- Maven Integration：Maven集成
- Gradle：Gradle集成
- NodeJS：Node.js集成

**部署插件：**
- Docker Pipeline：Docker流水线
- Kubernetes：Kubernetes集成
- Publish Over SSH：SSH部署

**测试相关插件：**
- JUnit：测试报告
- Allure：Allure报告
- HTML Publisher：HTML报告
- Cobertura：代码覆盖率

**通知插件：**
- Email Extension：邮件通知
- DingTalk：钉钉通知
- Slack Notification：Slack通知

### 3. 用户配置

**创建用户：**
1. 进入 "Manage Jenkins" -> "Manage Users"
2. 点击 "Create User"
3. 填写用户名、密码、邮箱等信息

**权限配置：**
1. 安装 "Role-based Authorization Strategy" 插件
2. 进入 "Manage Jenkins" -> "Manage and Assign Roles"
3. 配置角色和权限

### 4. URL配置

进入 "Manage Jenkins" -> "Configure System"：

- **Jenkins URL**：设置Jenkins的访问地址
- **系统管理员邮件地址**：设置管理员邮箱

### 5. JDK配置

进入 "Manage Jenkins" -> "Global Tool Configuration"：

```
JDK安装：
- 名称：JDK11
- JAVA_HOME：/usr/lib/jvm/java-11-openjdk
```

或勾选 "自动安装" 让Jenkins自动下载安装。

### 6. Git配置

```
Git安装：
- 名称：Default
- 路径：/usr/bin/git
```

或勾选 "自动安装"。

### 7. Maven配置

```
Maven安装：
- 名称：Maven3
- MAVEN_HOME：/opt/maven
```

或勾选 "自动安装"。

### 8. 配置全局属性

**环境变量：**
```
JAVA_HOME = /usr/lib/jvm/java-11-openjdk
MAVEN_HOME = /opt/maven
PATH = $JAVA_HOME/bin:$MAVEN_HOME/bin:$PATH
```

**工具位置：**
```
Git = /usr/bin/git
JDK = /usr/lib/jvm/java-11-openjdk
```
