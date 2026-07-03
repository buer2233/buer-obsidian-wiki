# Django 学习笔记

> 来源: https://www.yuque.com/bbuer/cskf/irvnuimfmfhmyefw
> 抓取时间: 2026-06-30
> 分组: 测试平台开发

---

## 项目创建与迁移

### 创建Django项目

```bash
django-admin startproject project_name
```

### 创建应用

```bash
python manage.py startapp app_name
```

### 数据迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

## 数据迁移（Migrations）

Django通过migration机制来管理数据库结构的变更：

- `makemigrations`：根据model的变化生成迁移文件
- `migrate`：将迁移文件应用到数据库
- `showmigrations`：查看迁移状态
- `sqlmigrate`：查看迁移对应的SQL语句

## CRUD操作

### 创建（Create）

```python
Model.objects.create(field1=value1, field2=value2)
```

### 查询（Read）

```python
# 查询所有
Model.objects.all()

# 条件查询
Model.objects.filter(field=value)

# 获取单个
Model.objects.get(id=1)
```

### 更新（Update）

```python
obj = Model.objects.get(id=1)
obj.field = new_value
obj.save()

# 批量更新
Model.objects.filter(field=value).update(field=new_value)
```

### 删除（Delete）

```python
obj = Model.objects.get(id=1)
obj.delete()
```

## 类视图（Class-Based Views）

Django支持使用类来定义视图，提供了更结构化的方式：

```python
from django.views import View

class MyView(View):
    def get(self, request):
        # 处理GET请求
        pass

    def post(self, request):
        # 处理POST请求
        pass
```

常用的类视图包括：
- `View`：基础类视图
- `TemplateView`：模板视图
- `ListView`：列表视图
- `DetailView`：详情视图
- `CreateView`、`UpdateView`、`DeleteView`：增删改视图

## Django REST Framework

Django REST Framework（DRF）是Django的REST API框架：

### 安装

```bash
pip install djangorestframework
```

### 序列化器（Serializer）

```python
from rest_framework import serializers

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

### 视图集（ViewSet）

```python
from rest_framework import viewsets

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```

### 路由配置

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'mymodel', MyModelViewSet)
urlpatterns = router.urls
```
