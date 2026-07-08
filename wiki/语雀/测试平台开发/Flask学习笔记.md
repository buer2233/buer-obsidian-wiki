---
type: knowledge
title: "Flask学习笔记"
source: "https://www.yuque.com/bbuer/cskf/di2iga98ezenhb3b"
source_platform: yuque
category: "测试平台开发"
created: 2026-06-30
updated: 2026-06-30
tags:
  - flask
  - python
  - web框架
  - ORM
status: mature
related:
  - "[[flask平台代码简介]]"
  - "[[Django 学习笔记]]"
  - "[[测试平台基础]]"
---

# Flask学习笔记

## 1. Flask 简介

### 什么是 Flask

Flask 是一个轻量级的 Python Web 框架，被称为"微框架"。

### 安装

```bash
pip install flask

# 验证
python -c "import flask; print(flask.__version__)"
```

### 最小应用

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## 2. 路由 (Route)

### 基础路由

```python
from flask import Flask

app = Flask(__name__)

# 基础路由
@app.route('/')
def index():
    return '首页'

# 带参数的路由
@app.route('/user/<username>')
def show_user(username):
    return f'用户: {username}'

# 指定参数类型
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'文章ID: {post_id}'

# 多个URL指向同一视图
@app.route('/')
@app.route('/index')
def index():
    return '首页'

# HTTP方法限制
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return '处理登录'
    return '显示登录页'
```

### 路由参数类型

| 类型 | 说明 | 示例 |
|------|------|------|
| string | 默认，字符串 | `/user/<name>` |
| int | 整数 | `/post/<int:id>` |
| float | 浮点数 | `/price/<float:amount>` |
| path | 带斜杠的字符串 | `/file/<path:filepath>` |
| uuid | UUID字符串 | `/user/<uuid:user_id>` |

### Blueprint 蓝图

```python
# auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    return '登录页面'

@auth_bp.route('/logout')
def logout():
    return '已登出'


# app.py
from flask import Flask
from auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)

# 访问: /auth/login, /auth/logout
```

---

## 3. 请求与响应

### 请求对象 (Request)

```python
from flask import request

@app.route('/api/data', methods=['POST'])
def get_data():
    # 获取JSON数据
    data = request.get_json()
    name = data.get('name')

    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('keyword', '')

    # 获取表单数据
    username = request.form.get('username')
    password = request.form.get('password')

    # 获取文件
    file = request.files.get('avatar')

    # 获取请求头
    token = request.headers.get('Authorization')

    # 获取Cookie
    session_id = request.cookies.get('session_id')

    # 获取请求方法
    method = request.method

    # 获取请求URL
    url = request.url
    path = request.path

    return {'status': 'ok'}
```

### 响应对象 (Response)

```python
from flask import jsonify, make_response, redirect, abort

# 返回JSON
@app.route('/api/users')
def get_users():
    users = [
        {'id': 1, 'name': '张三'},
        {'id': 2, 'name': '李四'}
    ]
    return jsonify({'code': 200, 'data': users})

# 自定义响应
@app.route('/api/download')
def download():
    response = make_response('文件内容')
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    return response

# 重定向
@app.route('/old-url')
def old_url():
    return redirect('/new-url')

# 错误处理
@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

# 错误处理器
@app.errorhandler(404)
def not_found(error):
    return jsonify({'code': 404, 'message': '资源不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'code': 500, 'message': '服务器内部错误'}), 500
```

---

## 4. 模板渲染 (Jinja2)

### 基础模板

```python
from flask import render_template

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name, items=['A', 'B', 'C'])
```

```html
<!-- templates/hello.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Hello</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>

    <!-- 条件判断 -->
    {% if items %}
    <ul>
        {% for item in items %}
        <li>{{ item }}</li>
        {% endfor %}
    </ul>
    {% else %}
    <p>没有数据</p>
    {% endif %}

    <!-- 过滤器 -->
    <p>{{ name | upper }}</p>
    <p>{{ name | length }}</p>

    <!-- 模板继承 -->
    {% extends "base.html" %}
    {% block content %}
    <p>页面内容</p>
    {% endblock %}
</body>
</html>
```

---

## 5. ORM (SQLAlchemy)

### 安装配置

```bash
pip install flask-sqlalchemy
```

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:pass@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

### 定义模型

```python
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联
    projects = db.relationship('Project', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### CRUD 操作

```python
# Create
user = User(username='zhangsan', email='zhangsan@example.com')
db.session.add(user)
db.session.commit()

# 批量创建
users = [User(username=f'user{i}') for i in range(10)]
db.session.add_all(users)
db.session.commit()

# Read
user = User.query.get(1)                    # 主键查询
user = User.query.filter_by(username='zhangsan').first()  # 条件查询
users = User.query.filter(User.is_active == True).all()   # 过滤查询
users = User.query.order_by(User.created_at.desc()).limit(10).all()  # 排序+分页

# 复杂查询
from sqlalchemy import or_, and_
users = User.query.filter(
    or_(User.username.like('%test%'), User.email.like('%test%'))
).all()

# Update
user = User.query.get(1)
user.username = 'new_name'
db.session.commit()

# 批量更新
User.query.filter(User.is_active == False).update({'is_active': True})
db.session.commit()

# Delete
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

### 数据库迁移 (Flask-Migrate)

```bash
pip install flask-migrate
```

```python
from flask_migrate import Migrate

migrate = Migrate(app, db)
```

```bash
# 初始化迁移
flask db init

# 生成迁移文件
flask db migrate -m "add users table"

# 执行迁移
flask db upgrade

# 回滚
flask db downgrade
```

---

## 6. 中间件与装饰器

### 登录验证装饰器

```python
from functools import wraps
from flask import session, redirect, url_for, jsonify

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def api_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'code': 401, 'message': '未授权'}), 401
        # 验证token...
        return f(*args, **kwargs)
    return decorated

@app.route('/dashboard')
@login_required
def dashboard():
    return '控制台'
```

### CORS 跨域配置

```bash
pip install flask-cors
```

```python
from flask_cors import CORS

# 允许所有来源
CORS(app)

# 指定来源
CORS(app, origins=['http://localhost:3000', 'https://example.com'])
```

### 请求钩子

```python
@app.before_request
def before_request():
    """请求前处理"""
    # 记录请求日志
    print(f'{request.method} {request.url}')

@app.after_request
def after_request(response):
    """请求后处理"""
    response.headers['X-Custom'] = 'value'
    return response

@app.teardown_appcontext
def teardown(exception):
    """请求结束清理"""
    if exception:
        print(f'请求异常: {exception}')
```

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[Django 学习笔记]] — AI测试主题关联
- [[flask平台代码简介]] — AI测试主题关联
- [[测试平台基础]] — AI测试主题关联
- [[Vue前端学习笔记]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[常用SKILL总结]] — AI测试主题关联
- [[AI产品测试]] — AI测试主题关联
- [[02_pytest必背学习资料]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
