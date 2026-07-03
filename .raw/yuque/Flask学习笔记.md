# Flask学习笔记

> 来源: https://www.yuque.com/bbuer/cskf/di2iga98ezenhb3b
> 抓取时间: 2026-06-30
> 分组: 测试平台开发

---

## 路由（Routing）

### 基本路由

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/user/<name>')
def user(name):
    return f'Hello, {name}!'
```

### HTTP方法

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Login POST'
    else:
        return 'Login GET'
```

### 动态路由

```python
# 字符串（默认）
@app.route('/user/<name>')
def user(name): pass

# 整数
@app.route('/post/<int:post_id>')
def post(post_id): pass

# 浮点数
@app.route('/price/<float:price>')
def price(price): pass

# 路径
@app.route('/path/<path:subpath>')
def subpath(subpath): pass
```

### URL构建

```python
from flask import url_for

@app.route('/')
def index():
    return url_for('user', name='john')  # 生成 /user/john
```

## 请求与响应

### 请求对象（Request）

```python
from flask import request

@app.route('/login', methods=['POST'])
def login():
    # 获取表单数据
    username = request.form.get('username')
    password = request.form.get('password')

    # 获取JSON数据
    data = request.get_json()

    # 获取查询参数
    page = request.args.get('page', 1, type=int)

    # 获取请求头
    user_agent = request.headers.get('User-Agent')

    # 获取文件
    file = request.files.get('file')

    # 获取请求方法
    method = request.method

    # 获取URL
    url = request.url
```

### 响应对象（Response）

```python
from flask import make_response, jsonify

@app.route('/')
def index():
    # 返回字符串
    return 'Hello'

    # 返回模板
    return render_template('index.html')

    # 返回JSON
    return jsonify({'message': 'success'})

    # 自定义响应
    response = make_response('Custom Response')
    response.headers['X-Custom'] = 'value'
    response.set_cookie('username', 'john')
    return response

    # 重定向
    return redirect(url_for('login'))
```

### 错误处理

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500
```

## ORM（对象关系映射）

### Flask-SQLAlchemy安装

```bash
pip install flask-sqlalchemy
```

### 配置数据库

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

### 定义模型

```python
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'
```

### CRUD操作

```python
# 创建
user = User(username='john', email='john@example.com')
db.session.add(user)
db.session.commit()

# 查询
users = User.query.all()
user = User.query.get(1)
user = User.query.filter_by(username='john').first()
users = User.query.filter(User.age > 18).all()

# 更新
user = User.query.get(1)
user.email = 'new@example.com'
db.session.commit()

# 删除
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

### 数据库迁移（Flask-Migrate）

```bash
pip install flask-migrate
```

```python
from flask_migrate import Migrate

migrate = Migrate(app, db)
```

```bash
# 初始化迁移仓库
flask db init

# 生成迁移脚本
flask db migrate -m "Initial migration"

# 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade
```

### 关系定义

```python
# 一对多关系
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# 多对多关系
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class Post(db.Model):
    tags = db.relationship('Tag', secondary=tags, backref='posts')
```
