---
type: knowledge
title: "Jenkins全攻略"
source: "https://www.yuque.com/bbuer/cskf/rc96siuwbo66is17"
source_platform: yuque
category: "云原生"
created: 2026-06-30
updated: 2026-06-30
tags:
  - Jenkins
  - CI/CD
  - 持续集成
  - devops
status: mature
related:
  - "[[Docker]]"
  - "[[Linux总结]]"
---

# Jenkins全攻略

## 1. Jenkins 安装

### Docker 安装（推荐）

```bash
# 拉取镜像
docker pull jenkins/jenkins:lts

# 创建数据目录
mkdir -p /var/jenkins_home

# 运行容器
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

# 查看初始密码
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Linux 安装

```bash
# Ubuntu/Debian
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins

# CentOS/RHEL
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key
sudo yum install jenkins

# 启动服务
sudo systemctl start jenkins
sudo systemctl enable jenkins

# 查看初始密码
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### WAR 包安装

```bash
# 下载Jenkins WAR包
wget https://get.jenkins.io/war-stable/latest/jenkins.war

# 运行
java -jar jenkins.war --httpPort=8080

# 后台运行
nohup java -jar jenkins.war --httpPort=8080 > jenkins.log 2>&1 &
```

---

## 2. Jenkins 配置

### 初始配置

```
1. 访问 http://localhost:8080
2. 输入初始密码
3. 安装推荐插件
4. 创建管理员账号
5. 配置Jenkins URL
```

### 全局配置

```
Manage Jenkins -> Configure System

1. Jenkins Location
   - Jenkins URL: http://your-server:8080/
   - System Admin e-mail: admin@example.com

2. 邮件通知
   - SMTP服务器: smtp.example.com
   - 用户名: admin@example.com
   - 密码: ****
   - 使用SSL: 是

3. 全局属性
   - 环境变量
   - 工具位置
```

### 工具配置

```
Manage Jenkins -> Global Tool Configuration

1. JDK
   - Name: JDK11
   - JAVA_HOME: /usr/lib/jvm/java-11

2. Maven
   - Name: Maven3
   - MAVEN_HOME: /opt/maven

3. Node.js
   - Name: Node16
   - 安装目录: /usr/local/node

4. Python
   - Name: Python3
   - 安装目录: /usr/local/python3
```

### 插件管理

```
Manage Jenkins -> Manage Plugins

必装插件:
├── Git
├── Pipeline
├── Blue Ocean
├── Credentials Binding
├── Docker Pipeline
├── Kubernetes
├── Email Extension
├── Role-based Authorization Strategy
├── Generic Webhook Trigger
└── Publish Over SSH

推荐插件:
├── Job DSL
├── Configuration as Code
├── Monitoring
├── Performance
└── Allure
```

---

## 3. Web 页面配置

### 创建项目

```
New Item -> 输入项目名 -> 选择项目类型

项目类型:
├── Freestyle Project    # 自由风格，简单配置
├── Pipeline             # 流水线，代码化
├── Multibranch Pipeline # 多分支流水线
├── Folder              # 文件夹，组织项目
└── Organization Folder  # 组织文件夹
```

### Freestyle 项目配置

```
General
├── 项目描述
├── Discard old builds (保留构建数)
├── This project is parameterized (参数化构建)
│   ├── String Parameter
│   ├── Choice Parameter
│   └── Boolean Parameter
└── GitHub project

Source Code Management
├── Git
│   ├── Repository URL: https://github.com/user/repo.git
│   ├── Credentials: 添加凭证
│   └── Branches to build: */main
└── Subversion

Build Triggers
├── Build periodically (定时构建)
│   └── H 2 * * * (每天凌晨2点)
├── Poll SCM (轮询代码变更)
│   └── H/5 * * * * (每5分钟轮询)
├── Trigger builds remotely (远程触发)
│   └── Authentication Token: my-token
└── GitHub hook trigger (GitHub钩子)

Build Environment
├── Delete workspace before build
├── Use secret text(s) or file(s)
│   └── Secret text: 添加密钥
└── Provide Configuration files

Build
├── Execute shell
│   └── 命令: mvn clean package
├── Invoke top-level Maven targets
│   └── Goals: clean package
└── Send files or execute commands over SSH

Post-build Actions
├── Publish JUnit test result report
│   └── Test report XMLs: **/target/surefire-reports/*.xml
├── Send build artifacts over SSH
├── E-mail Notification
├── Archive the artifacts
└── Trigger parameterized build on other projects
```

### Pipeline 项目配置

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'myapp'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: '分支名')
        choice(name: 'ENV', choices: ['dev', 'staging', 'prod'], description: '部署环境')
        booleanParam(name: 'DEPLOY', defaultValue: false, description: '是否部署')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${params.BRANCH}",
                    url: 'https://github.com/user/repo.git',
                    credentialsId: 'git-credentials'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Push') {
            when {
                expression { params.DEPLOY }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-registry',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                }
            }
        }

        stage('Deploy') {
            when {
                expression { params.DEPLOY && params.ENV != 'dev' }
            }
            steps {
                sshagent(['deploy-server']) {
                    sh """
                        ssh deploy@server "docker pull ${DOCKER_IMAGE}:${DOCKER_TAG}"
                        ssh deploy@server "docker-compose up -d"
                    """
                }
            }
        }
    }

    post {
        success {
            emailext (
                subject: "构建成功: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "构建详情: ${env.BUILD_URL}",
                to: 'team@example.com'
            )
        }
        failure {
            emailext (
                subject: "构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "构建详情: ${env.BUILD_URL}",
                to: 'team@example.com'
            )
        }
        always {
            cleanWs()
        }
    }
}
```

---

## 4. Jenkins API

### 远程触发构建

```bash
# 使用Token触发
curl -X POST http://localhost:8080/job/my-project/build \
  --user admin:token \
  --data-urlencode json='{"parameter": [{"name":"BRANCH", "value":"main"}]}'

# 使用Crumb防CSRF
CRUMB=$(curl -s 'http://admin:token@localhost:8080/crumbIssuer/api/json' | python -c "import sys,json; print json.load(sys.stdin)['crumb']")
curl -X POST "http://localhost:8080/job/my-project/build" \
  -H "Jenkins-Crumb:$CRUMB" \
  --user admin:token
```

### 查询构建状态

```bash
# 获取构建信息
curl -s http://admin:token@localhost:8080/job/my-project/lastBuild/api/json

# 获取构建日志
curl -s http://admin:token@localhost:8080/job/my-project/lastBuild/consoleText
```

---

## 5. 最佳实践

### 安全配置

```
安全配置清单
├── 启用CSRF防护
├── 禁用CLI over Remoting
├── 配置角色权限
├── 使用HTTPS
├── 定期更新插件
├── 使用Credential管理密钥
└── 限制脚本执行权限
```

### 性能优化

```
优化建议
├── 限制构建历史保留数量
├── 清理旧的工作空间
├── 使用分布式构建
├── 优化Maven本地仓库
├── 配置适当的JVM参数
└── 使用SSD存储Jenkins数据
```

---

## 相关链接

- [[Linux总结]] — Linux操作系统基础知识总结

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[Docker]] — AI测试主题关联
- [[Linux总结]] — AI测试主题关联
- [[测试平台基础]] — AI测试主题关联
- [[Git SSH Windows路径解析错误规避]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[安卓移动端appium环境搭建流程]] — AI测试主题关联
- [[移动端自动化框架搭建问题点记录]] — AI测试主题关联
- [[Claude Code学习笔记]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
