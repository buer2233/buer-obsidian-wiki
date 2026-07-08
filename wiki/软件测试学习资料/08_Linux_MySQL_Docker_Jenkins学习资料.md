# Linux / MySQL / Docker / Jenkins学习资料

> 生成日期：2026-07-08
> 适用对象：邓万鹏，自动化测试 / AI自动化测试 / AI产品测试面试
> 生成依据：Linux man pages + MySQL官方文档 + Docker官方文档 + Jenkins官方文档 + 错题#016/#014/#008/#012
> 重点目标：补齐当前薄弱的Linux、Docker、MySQL基础，并能讲到CI/CD测试工程落地

---

## 一、官方资料来源

| 主题 | 来源 |
|------|------|
| Linux tail | https://man7.org/linux/man-pages/man1/tail.1.html |
| Linux grep | https://man7.org/linux/man-pages/man1/grep.1.html |
| Linux df | https://man7.org/linux/man-pages/man1/df.1.html |
| Linux du | https://man7.org/linux/man-pages/man1/du.1.html |
| Linux find | https://man7.org/linux/man-pages/man1/find.1.html |
| MySQL SELECT | https://dev.mysql.com/doc/refman/8.4/en/select.html |
| MySQL JOIN | https://dev.mysql.com/doc/refman/8.4/en/join.html |
| MySQL EXPLAIN | https://dev.mysql.com/doc/refman/8.4/en/explain.html |
| MySQL Slow Query Log | https://dev.mysql.com/doc/refman/8.4/en/slow-query-log.html |
| Docker Docs | https://docs.docker.com/ |
| Jenkins Pipeline | https://www.jenkins.io/doc/book/pipeline/ |
| Git Book | https://git-scm.com/book/en/v2 |

---

## 二、Linux日志与磁盘排查

这是你当前最薄弱项，真实面试也问过 Linux 复制命令，必须每天复习。

### 1. 日志查看

| 命令 | 作用 |
|------|------|
| `tail -n 100 app.log` | 查看最后100行 |
| `tail -f app.log` | 实时跟踪新增日志 |
| `tail -F app.log` | 跟踪日志并适配日志轮转 |
| `grep -n "ERROR" app.log` | 查ERROR并显示行号 |
| `grep -i "timeout" app.log` | 忽略大小写搜索 |
| `grep -c "Exception" app.log` | 统计匹配行数 |
| `grep -v "DEBUG" app.log` | 反向过滤 |
| `grep -r "orderId" /var/log/app` | 递归搜索目录 |

错误示范：
```bash
grep `ERROR` app.log
```

正确写法：
```bash
grep -n "ERROR" app.log
```

### 2. 磁盘排查

| 命令 | 作用 |
|------|------|
| `df -h` | 看分区空间 |
| `df -i` | 看inode |
| `du -sh *` | 看当前目录各项大小 |
| `du -h --max-depth=1 /var/log` | 看一级目录大小 |
| `find /var/log -type f -size +100M` | 找大文件 |

排查SOP：

```bash
df -h
cd /var
du -sh * | sort -rh | head
cd /var/log
du -sh * | sort -rh | head
find /var/log -type f -size +100M
```

面试模板：
```text
Linux日志和磁盘排查我会按“先看整体，再定位目录，再定位文件，再分析原因”的顺序处理。接口报错先用tail -f看实时日志，再用grep -n搜索ERROR、Exception、Timeout。磁盘报警先用df -h看哪个分区满了，再用du逐层定位大目录。如果空间没满但不能创建文件，会补充看df -i排查inode。
```

10-20K面试可背版本：
```text
我平时排查接口自动化失败时，会先看pytest报告里的失败接口和错误信息，再到服务器上看应用日志。实时问题用tail -f app.log，历史问题用grep -n "ERROR" app.log定位行号；如果怀疑日志太大或磁盘满了，先用df -h看分区，再用du -sh *逐层找大目录。df看的是文件系统整体空间，du看的是目录或文件实际占用，这两个要结合使用。
```

必须秒答：
```bash
tail -n 200 app.log
tail -f app.log
grep -n "ERROR" app.log
grep -i "timeout" app.log
df -h
du -sh *
du -h --max-depth=1 /var/log
```

### 3. 复制文件和目录

真实面试问过，必须秒答：

```bash
cp a.log /tmp/a.log
cp -r logs /tmp/logs
cp -a logs /tmp/logs
```

说明：
- `cp` 复制文件。
- `cp -r` 递归复制目录。
- `cp -a` 尽量保留权限、时间等属性。

---

## 三、MySQL必背

### 1. SELECT基础顺序

```sql
SELECT 字段
FROM 表
WHERE 行过滤条件
GROUP BY 分组字段
HAVING 分组过滤条件
ORDER BY 排序字段
LIMIT 条数;
```

常用示例：

```sql
SELECT id, name, created_at
FROM users
WHERE status = 'active'
ORDER BY created_at DESC
LIMIT 10;
```

### 2. WHERE和HAVING

```sql
-- WHERE过滤原始行
SELECT * FROM orders WHERE status = 'paid';

-- HAVING过滤分组结果
SELECT user_id, COUNT(*) AS cnt
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 3;
```

### 3. JOIN

```sql
SELECT o.id, u.name, o.amount
FROM orders o
INNER JOIN users u ON o.user_id = u.id;
```

| JOIN | 含义 |
|------|------|
| INNER JOIN | 两表都匹配才返回 |
| LEFT JOIN | 保留左表全部，右表无匹配为NULL |

测试场景：
- 查询订单和用户信息。
- 排查主表有记录但明细缺失。
- 接口返回聚合数据时做数据库校验。

### 4. 日期函数和CASE WHEN

你当前薄弱点：

```sql
-- 最近30天
SELECT *
FROM orders
WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);

-- 条件统计
SELECT
  COUNT(*) AS total,
  SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) AS success_count,
  SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed_count
FROM test_results;
```

结合测试场景背：
```sql
-- 查询最近7天失败的自动化用例
SELECT case_name, status, created_at
FROM test_results
WHERE status = 'failed'
  AND created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
ORDER BY created_at DESC;

-- 统计每个模块成功和失败数量
SELECT
  module,
  COUNT(*) AS total,
  SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) AS passed_count,
  SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed_count
FROM test_results
GROUP BY module
ORDER BY failed_count DESC;
```

面试模板：
```text
DATE_SUB我主要用来查最近N天的数据，比如最近7天失败用例、最近30天订单或日志记录。CASE WHEN常用于条件统计，比如一次查出总用例数、成功数、失败数。测试平台里这类SQL很常见，可以用于报表统计和失败趋势分析。
```

### 5. 索引、EXPLAIN、慢查询

面试表达：
```text
索引是帮助数据库快速定位数据的数据结构，不是越多越好。接口慢时，我会先看慢查询日志，再用EXPLAIN看执行计划，比如是否全表扫描、是否走索引、扫描行数是否过大、JOIN顺序是否合理。
```

常见排查：
- where字段无索引。
- 模糊查询前置 `%`。
- 函数作用在索引列。
- 低选择性字段建索引收益低。
- 排序/分组导致临时表或文件排序。

### 6. 事务ACID

| 特性 | 含义 |
|------|------|
| Atomicity 原子性 | 要么都成功，要么都失败 |
| Consistency 一致性 | 事务前后数据满足约束 |
| Isolation 隔离性 | 并发事务互不干扰 |
| Durability 持久性 | 提交后持久保存 |

---

## 四、Docker必背

### 1. 镜像、容器、仓库

| 概念 | 解释 |
|------|------|
| 镜像 image | 应用运行环境模板，包含代码、依赖、配置 |
| 容器 container | 镜像运行后的隔离进程 |
| 仓库 registry | 存储和分发镜像 |

面试模板：
```text
镜像是模板，容器是运行实例，仓库是存放镜像的地方。测试工作中我用Docker主要解决环境一致性问题。
```

项目化表达：
```text
在测试工作里，我不会把Docker讲成运维概念，而是讲它解决了测试环境一致性问题。镜像里固定应用依赖和运行环境，容器是实际跑起来的实例，仓库用于团队分发镜像。比如自动化执行依赖Python、浏览器驱动、测试工具和项目依赖，如果每台机器手动安装，环境差异很容易导致用例不稳定；用Docker后可以把执行环境标准化。
```

### 2. 常用命令

```bash
docker ps
docker images
docker logs -f --tail 200 app
docker exec -it app bash
docker stop app
docker rm app
docker pull mysql:8
docker build -t api-test:latest .
docker run -d --name api-test api-test:latest
```

排查模板：
```text
如果Jenkins里自动化任务失败，我会先看Jenkins Console Output，再看pytest报告。如果怀疑是容器内环境问题，会用docker ps确认容器状态，用docker logs查看容器日志，用docker exec进入容器检查依赖、配置和网络连通性。
```

### 3. Docker Compose

Compose用于定义和运行多容器应用。

```yaml
services:
  app:
    image: test-app:latest
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
```

注意：
- `depends_on` 短语法只保证启动顺序，不保证服务健康。
- 要等数据库可用，配合 `healthcheck` 和 `condition: service_healthy`。
- `services` 定义服务，`volumes` 做数据持久化或挂载报告，`networks` 管理服务间网络。

测试场景表达：
```text
如果一个接口自动化项目依赖应用服务、MySQL、Redis或Mock服务，我会考虑用docker-compose统一拉起。这样新同事或Jenkins节点只要执行compose命令，就能获得相对一致的测试环境。需要注意的是depends_on不等于服务真正可用，数据库这类服务最好加healthcheck。
```

---

## 五、Jenkins / Git / CI/CD

### 1. Jenkins Pipeline

核心概念：
- Pipeline as Code。
- Jenkinsfile放到Git仓库。
- Declarative Pipeline结构清晰。
- stage表示阶段，steps表示具体动作。
- agent表示在哪个节点/容器执行。

示例：

```groovy
pipeline {
  agent any
  stages {
    stage('Install') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'pytest cases/api --alluredir=report/allure-results'
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'report/**', allowEmptyArchive: true
    }
  }
}
```

更贴合pytest报告的版本：
```groovy
pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Install') {
      steps {
        sh 'python -m pip install -r requirements.txt'
      }
    }
    stage('Run API Tests') {
      steps {
        sh 'pytest cases/api --html=report/report.html --self-contained-html --junitxml=report/junit.xml'
      }
    }
  }
  post {
    always {
      junit allowEmptyResults: true, testResults: 'report/junit.xml'
      archiveArtifacts artifacts: 'report/**', allowEmptyArchive: true
    }
  }
}
```

面试要点：
```text
Jenkins执行pytest时，我会关注四件事：代码从Git拉取是否正确，依赖安装是否稳定，测试环境和账号配置是否隔离，报告是否能归档和追踪。pytest可以输出html报告、junit xml或allure结果，Jenkins再做归档、趋势展示和通知。
```

### 2. 自动化测试流水线

```text
Git拉代码 -> 安装依赖 -> 启动/连接测试环境 -> 执行pytest -> 生成报告 -> 归档 -> 通知 -> 结果回写测试平台
```

结合我的真实经验：
```text
我在测试平台和自动化项目里接触过Jenkins集成，重点是让接口自动化、UI自动化或性能任务可以持续执行，而不是只在本地跑。任务失败后，我会结合pytest报告、Jenkins控制台、Linux日志和必要的容器日志判断问题来源。如果是用例问题就修用例，如果是环境问题就修配置或服务，如果是产品缺陷就提交BUG并保留请求响应和日志证据。
```

### 3. Git常见问题

| 问题 | 回答 |
|------|------|
| Git和GitHub/GitLab区别 | Git是版本控制工具，GitHub/GitLab是代码托管平台 |
| fetch和pull区别 | fetch只拉取不合并，pull = fetch + merge/rebase |
| merge和rebase区别 | merge保留合并历史，rebase让历史更线性 |
| 冲突怎么解决 | 修改冲突文件 -> git add -> 继续merge/rebase |

---

## 六、结合个人项目表达

```text
我在测试平台和自动化项目中会把Linux、Docker、Jenkins结合起来使用。Linux主要用于日志和环境排查；Docker用于固定测试环境和依赖服务；Jenkins负责任务调度和持续集成；pytest输出报告并回写平台。比如接口自动化失败后，我会先看pytest报告和请求响应，再通过Linux日志定位服务端错误，必要时看Docker容器日志和Jenkins Console Output，判断是用例问题、环境问题还是服务问题。
```

补强版：
```text
结合我的经历，我更适合把这几项能力放在测试工程落地里讲。比如E10接口自动化或测试平台任务执行失败，我不会只说“看日志”，而是按链路排查：先看pytest报告确认失败用例、请求参数和响应；再看Jenkins Console Output确认依赖、环境变量和执行命令；如果服务部署在容器里，就看docker logs和容器状态；最后用Linux的tail、grep定位服务日志，用MySQL查询相关业务数据是否落库或状态异常。这样回答既真实，也能体现我具备自动化测试工程化排查能力。
```

---

## 七、常见面试追问

1. Linux怎么查看日志和磁盘？
2. `df` 和 `du` 区别？
3. `tail -f` 和 `tail -F` 区别？
4. 最近30天数据怎么查？
5. `WHERE` 和 `HAVING` 区别？
6. `INNER JOIN` 和 `LEFT JOIN` 区别？
7. Docker镜像、容器、仓库区别？
8. `depends_on` 是否等服务真正可用？
9. Jenkins Pipeline两种语法区别？
10. CI/CD中自动化测试放在哪个阶段？

---

## 八、回答模板

### 1. 综合模板

```text
Linux、MySQL、Docker、Jenkins我会结合测试工程来讲。Linux用于日志和磁盘排查，接口报错看tail和grep，磁盘报警用df和du逐层定位；MySQL用于数据准备、接口落库校验和慢接口排查，慢SQL通过慢查询日志和EXPLAIN定位；Docker用于保证测试环境一致，Compose可以拉起应用、数据库和Mock服务；Jenkins负责持续集成，拉代码、装依赖、跑pytest、生成报告和通知。这样自动化测试不是单机脚本，而是可持续执行、可追踪、可排查的工程体系。
```

### 2. Linux专项模板

```text
Linux我主要用于测试环境排查。接口报错时，我会用tail -f实时看日志，用grep -n按ERROR、Exception、trace id或接口路径定位关键行；磁盘问题先用df -h看哪个分区满，再用du -sh *逐层找大目录，必要时用df -i看inode。这个能力在自动化任务失败、服务异常、日志过大时很实用。
```

### 3. MySQL专项模板

```text
MySQL在测试里主要用于准备数据、校验接口落库和做报表统计。基础查询我会用SELECT、WHERE、ORDER BY、LIMIT；查最近N天数据会用DATE_SUB；做成功失败统计会用CASE WHEN；接口慢时会结合慢查询日志和EXPLAIN看是否走索引、扫描行数和JOIN是否合理。
```

### 4. Docker专项模板

```text
Docker我会重点讲镜像、容器、仓库和Compose。镜像是环境模板，容器是运行实例，仓库用于分发镜像。测试场景里Docker主要解决环境一致性，docker-compose可以把应用、数据库、Mock服务一起编排起来。排查时常用docker ps、docker logs、docker exec。
```

### 5. Jenkins执行pytest模板

```text
Jenkins里跑pytest一般是拉代码、安装依赖、加载环境配置、执行pytest、生成报告、归档并通知。pytest报告可以是html、junit xml或allure结果。任务失败后我会先看Jenkins控制台和pytest报告，再结合Linux日志、Docker容器日志和数据库数据判断是用例、环境还是产品问题。
```

---

## 九、练习清单

- [ ] 每天默写 `tail -f`、`grep -n`、`df -h`、`du -sh *`、`cp -r`。
- [ ] 写出最近30天SQL和CASE WHEN条件统计。
- [ ] 背熟镜像、容器、仓库区别。
- [ ] 解释Docker Compose的services、volumes、networks。
- [ ] 口述Jenkins执行pytest的流水线。
- [ ] 用1分钟讲清楚“自动化任务失败后我怎么排查”。
- [ ] 背熟 `DATE_SUB(CURDATE(), INTERVAL 7 DAY)` 和 `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`。

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[00_Python自动化AI测试面试必背八股文]] — AI测试主题关联
- [[02_pytest必背学习资料]] — AI测试主题关联
- [[03_Python测试开发框架设计学习资料]] — AI测试主题关联
- [[13_AI产品测试方法论学习资料]] — AI测试主题关联
- [[17_测试平台开发学习资料]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[AI产品测试]] — AI测试主题关联
- [[01_Python语言基础学习资料]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
