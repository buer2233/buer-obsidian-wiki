---
type: knowledge
title: "flask平台代码简介(泛微)"
source: "https://www.yuque.com/bbuer/cskf/th3977vgsowxcgg0"
source_platform: yuque
category: "测试平台开发"
created: 2026-06-30
updated: 2026-06-30
tags:
  - flask
  - python
  - 测试平台
  - 泛微
  - SQLAlchemy
related:
  - "[[Flask学习笔记]]"
  - "[[Django 学习笔记]]"
  - "[[测试平台基础]]"
---

## 数据库模型

Flask平台使用SQLAlchemy作为ORM，定义了系统所需的数据库模型。

### 用户模型

```python
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='tester')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 项目模型

```python
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 用例模型

```python
class TestCase(db.Model):
    __tablename__ = 'test_case'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    steps = db.Column(db.Text)
    expected_result = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
```

## 后端

### 路由

Flask平台的路由采用蓝图（Blueprint）方式进行组织，按功能模块划分不同的路由文件。

### 蓝图（Blueprint）

蓝图是Flask中用于组织路由的方式，可以将不同功能模块的路由分开管理：

```python
from flask import Blueprint

# 创建蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
project_bp = Blueprint('project', __name__, url_prefix='/project')
case_bp = Blueprint('case', __name__, url_prefix='/case')

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)
app.register_blueprint(case_bp)
```

### 视图函数

视图函数处理具体的请求逻辑：

```python
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({'code': 0, 'message': '登录成功'})
    return jsonify({'code': 1, 'message': '用户名或密码错误'})
```

### Session管理

Flask使用session来管理用户会话状态：

```python
from flask import session

app.secret_key = 'your-secret-key'

# 设置session
session['user_id'] = user.id
session['username'] = user.username

# 获取session
user_id = session.get('user_id')

# 删除session
session.pop('user_id', None)

# 清除所有session
session.clear()
```

### 登录装饰器

使用装饰器来保护需要登录才能访问的接口：

```python
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'code': 401, 'message': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated_function

@project_bp.route('/list')
@login_required
def project_list():
    projects = Project.query.all()
    return jsonify({'code': 0, 'data': [p.to_dict() for p in projects]})
```

### 泛微集成

该平台集成了泛微OA系统，实现了以下功能：

- 单点登录（SSO）：通过泛微OAuth接口实现免登录
- 流程对接：测试结果与泛微审批流程打通
- 消息通知：测试报告通过泛微消息推送
- 数据同步：用户和组织架构从泛微同步

---

## 🔗 关联文档

- [[Flask学习笔记]] — Flask 基础知识
- [[Django 学习笔记]] — Django 对比学习
- [[测试平台基础]] — 测试平台整体介绍

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[Flask学习笔记]] — AI测试主题关联
- [[Django 学习笔记]] — AI测试主题关联
- [[测试平台基础]] — AI测试主题关联
- [[接口自动化测试日常问题记录]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[常用SKILL总结]] — AI测试主题关联
- [[AI产品测试]] — AI测试主题关联
- [[AI自动化开发计划]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
