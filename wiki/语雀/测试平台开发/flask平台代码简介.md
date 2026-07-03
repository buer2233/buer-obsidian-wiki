---
type: knowledge
title: "Flask平台代码简介"
source: "https://www.yuque.com/bbuer/cskf/th3977vgsowxcgg0"
source_platform: yuque
category: "测试平台开发"
created: 2026-06-30
updated: 2026-06-30
tags:
  - flask
  - 泛微
  - 测试平台
  - SQLAlchemy
status: mature
related:
  - "[[Flask学习笔记]]"
  - "[[Django 学习笔记]]"
  - "[[测试平台基础]]"
  - "[[MySQL总结]]"
---

# Flask平台代码简介

## 1. 项目结构

```
flask-platform/
├── app/
│   ├── __init__.py          # 应用初始化
│   ├── config.py            # 配置文件
│   ├── extensions.py        # 扩展初始化
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   └── test_case.py
│   ├── api/                 # API路由
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── project.py
│   │   └── test_case.py
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── project_service.py
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── response.py
│       └── validators.py
├── migrations/              # 数据库迁移
├── tests/                   # 测试文件
├── requirements.txt
├── run.py                   # 启动入口
└── wsgi.py                  # WSGI入口
```

---

## 2. 数据库模型

### 基础模型

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
```

### 用户模型

```python
# app/models/user.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='tester')  # admin, manager, tester
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    projects = db.relationship('Project', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
```

### 项目模型

```python
# app/models/project.py
from datetime import datetime
from app.extensions import db

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    test_cases = db.relationship('TestCase', backref='project', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'owner_name': self.owner.username if self.owner else None,
            'status': self.status,
            'test_case_count': self.test_cases.count(),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
```

### 测试用例模型

```python
# app/models/test_case.py
from datetime import datetime
from app.extensions import db

class TestCase(db.Model):
    __tablename__ = 'test_cases'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    module = db.Column(db.String(100))
    title = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(10), default='P2')  # P0, P1, P2, P3
    preconditions = db.Column(db.Text)
    steps = db.Column(db.Text, nullable=False)
    expected_result = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, ready, deprecated
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    executions = db.relationship('TestExecution', backref='test_case', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'module': self.module,
            'title': self.title,
            'priority': self.priority,
            'preconditions': self.preconditions,
            'steps': self.steps,
            'expected_result': self.expected_result,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class TestExecution(db.Model):
    __tablename__ = 'test_executions'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('test_cases.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # pass, fail, block, skip
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)  # 执行时长(秒)
    remark = db.Column(db.Text)
    defect_url = db.Column(db.String(500))

    def to_dict(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'case_title': self.test_case.title if self.test_case else None,
            'status': self.status,
            'executor_id': self.executor_id,
            'executed_at': self.executed_at.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': self.duration,
            'remark': self.remark
        }
```

---

## 3. 后端路由蓝图

### 认证蓝图

```python
# app/api/auth.py
from flask import Blueprint, request, session
from app.models.user import User
from app.extensions import db
from app.utils.response import success, error

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return error('用户名和密码不能为空', 400)

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return error('用户名或密码错误', 401)

    if not user.is_active:
        return error('账号已被禁用', 403)

    session['user_id'] = user.id
    return success({
        'user': user.to_dict(),
        'token': f'fake-token-{user.id}'  # 实际应使用JWT
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.pop('user_id', None)
    return success(message='已登出')

@auth_bp.route('/me', methods=['GET'])
def me():
    """获取当前用户信息"""
    user_id = session.get('user_id')
    if not user_id:
        return error('未登录', 401)

    user = User.query.get(user_id)
    return success(user.to_dict())
```

### 项目蓝图

```python
# app/api/project.py
from flask import Blueprint, request
from app.models.project import Project
from app.extensions import db
from app.utils.response import success, error, paginate

project_bp = Blueprint('project', __name__, url_prefix='/api/projects')

@project_bp.route('', methods=['GET'])
def get_projects():
    """获取项目列表"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    keyword = request.args.get('keyword', '')

    query = Project.query
    if keyword:
        query = query.filter(Project.name.contains(keyword))

    pagination = query.order_by(Project.created_at.desc()).paginate(
        page=page, per_page=size, error_out=False
    )

    return paginate(pagination, lambda p: p.to_dict())

@project_bp.route('', methods=['POST'])
def create_project():
    """创建项目"""
    data = request.get_json()

    if not data.get('name'):
        return error('项目名称不能为空', 400)

    project = Project(
        name=data['name'],
        description=data.get('description', ''),
        owner_id=data.get('owner_id', 1)
    )
    db.session.add(project)
    db.session.commit()

    return success(project.to_dict(), 201)

@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """获取项目详情"""
    project = Project.query.get_or_404(project_id)
    return success(project.to_dict())

@project_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """更新项目"""
    project = Project.query.get_or_404(project_id)
    data = request.get_json()

    if 'name' in data:
        project.name = data['name']
    if 'description' in data:
        project.description = data['description']
    if 'status' in data:
        project.status = data['status']

    db.session.commit()
    return success(project.to_dict())

@project_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """删除项目"""
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return success(message='删除成功')
```

### 测试用例蓝图

```python
# app/api/test_case.py
from flask import Blueprint, request
from app.models.test_case import TestCase, TestExecution
from app.extensions import db
from app.utils.response import success, error, paginate

test_case_bp = Blueprint('test_case', __name__, url_prefix='/api/test-cases')

@test_case_bp.route('', methods=['GET'])
def get_test_cases():
    """获取测试用例列表"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    project_id = request.args.get('project_id', type=int)
    priority = request.args.get('priority')
    keyword = request.args.get('keyword', '')

    query = TestCase.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    if priority:
        query = query.filter_by(priority=priority)
    if keyword:
        query = query.filter(TestCase.title.contains(keyword))

    pagination = query.order_by(TestCase.created_at.desc()).paginate(
        page=page, per_page=size, error_out=False
    )

    return paginate(pagination, lambda tc: tc.to_dict())

@test_case_bp.route('', methods=['POST'])
def create_test_case():
    """创建测试用例"""
    data = request.get_json()

    required_fields = ['project_id', 'title', 'steps', 'expected_result']
    for field in required_fields:
        if not data.get(field):
            return error(f'{field}不能为空', 400)

    test_case = TestCase(
        project_id=data['project_id'],
        module=data.get('module'),
        title=data['title'],
        priority=data.get('priority', 'P2'),
        preconditions=data.get('preconditions'),
        steps=data['steps'],
        expected_result=data['expected_result'],
        created_by=data.get('created_by', 1)
    )
    db.session.add(test_case)
    db.session.commit()

    return success(test_case.to_dict(), 201)

@test_case_bp.route('/<int:case_id>/execute', methods=['POST'])
def execute_test_case(case_id):
    """执行测试用例"""
    test_case = TestCase.query.get_or_404(case_id)
    data = request.get_json()

    execution = TestExecution(
        case_id=case_id,
        status=data.get('status', 'pass'),
        executor_id=data.get('executor_id', 1),
        duration=data.get('duration'),
        remark=data.get('remark')
    )
    db.session.add(execution)
    db.session.commit()

    return success(execution.to_dict(), 201)
```

---

## 4. 工具函数

### 统一响应格式

```python
# app/utils/response.py
from flask import jsonify

def success(data=None, code=200, message='success'):
    """成功响应"""
    response = {
        'code': code,
        'message': message,
        'data': data
    }
    return jsonify(response), code

def error(message='error', code=400):
    """错误响应"""
    response = {
        'code': code,
        'message': message,
        'data': None
    }
    return jsonify(response), code

def paginate(pagination, to_dict_func):
    """分页响应"""
    return success({
        'total': pagination.total,
        'page': pagination.page,
        'size': pagination.per_page,
        'pages': pagination.pages,
        'items': [to_dict_func(item) for item in pagination.items]
    })
```

### 应用初始化

```python
# app/__init__.py
from flask import Flask
from app.extensions import db, migrate, cors
from app.api.auth import auth_bp
from app.api.project import project_bp
from app.api.test_case import test_case_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(test_case_bp)

    return app
```

### 配置文件

```python
# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:root@localhost/test_platform'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
```

### 启动文件

```python
# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

---

## 相关链接

- [[MySQL总结]] — MySQL数据库基础知识与操作总结
