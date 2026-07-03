---
type: knowledge
title: "Django 学习笔记"
source: "https://www.yuque.com/bbuer/cskf/irvnuimfmfhmyefw"
source_platform: yuque
category: "测试平台开发"
created: 2026-06-30
updated: 2026-06-30
tags:
  - django
  - python
  - web框架
  - 后端开发
status: mature
related:
  - "[[Flask学习笔记]]"
  - "[[Vue前端学习笔记]]"
  - "[[测试平台基础]]"
  - "[[DRF框架基础总结]]"
---

# Django 学习笔记

## 1. 项目创建与迁移

### 创建项目

```bash
# 安装Django
pip install django

# 创建项目
django-admin startproject myproject

# 创建应用
cd myproject
python manage.py startapp myapp
```

### 项目结构

```
myproject/
├── manage.py           # 管理脚本
├── myproject/
│   ├── __init__.py
│   ├── settings.py     # 配置文件
│   ├── urls.py         # 路由配置
│   ├── wsgi.py         # WSGI入口
│   └── asgi.py         # ASGI入口
└── myapp/
    ├── __init__.py
    ├── admin.py         # 后台管理
    ├── apps.py          # 应用配置
    ├── models.py        # 数据模型
    ├── tests.py         # 测试
    ├── urls.py          # 应用路由
    └── views.py         # 视图函数
```

### 数据库迁移

```bash
# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 查看迁移状态
python manage.py showmigrations

# 回滚迁移
python manage.py migrate myapp 0001
```

---

## 2. Model 数据模型

### 定义模型

```python
from django.db import models

class Project(models.Model):
    """项目模型"""
    name = models.CharField('项目名称', max_length=100)
    description = models.TextField('项目描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        db_table = 'projects'
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class TestCase(models.Model):
    """测试用例模型"""
    LEVEL_CHOICES = [
        ('P0', '核心'),
        ('P1', '重要'),
        ('P2', '一般'),
        ('P3', '低'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='test_cases',
        verbose_name='所属项目'
    )
    title = models.CharField('用例标题', max_length=200)
    level = models.CharField('优先级', max_length=2, choices=LEVEL_CHOICES, default='P2')
    steps = models.TextField('测试步骤')
    expected = models.TextField('预期结果')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'test_cases'
        verbose_name = '测试用例'
```

### 常用字段类型

| 字段类型 | 说明 | 示例 |
|----------|------|------|
| CharField | 字符串 | `max_length=100` |
| TextField | 长文本 | `blank=True` |
| IntegerField | 整数 | `default=0` |
| FloatField | 浮点数 | `null=True` |
| BooleanField | 布尔值 | `default=True` |
| DateField | 日期 | `auto_now_add=True` |
| DateTimeField | 日期时间 | `auto_now=True` |
| EmailField | 邮箱 | 内置验证 |
| URLField | URL | 内置验证 |
| ForeignKey | 外键 | `on_delete=CASCADE` |
| ManyToManyField | 多对多 | `blank=True` |

---

## 3. CURD 操作

### Create (创建)

```python
# 方式1: 直接创建
project = Project.objects.create(
    name='测试项目',
    description='这是一个测试项目'
)

# 方式2: 先实例化再保存
project = Project(name='测试项目', description='描述')
project.save()

# 方式3: 批量创建
projects = [
    Project(name='项目1'),
    Project(name='项目2'),
]
Project.objects.bulk_create(projects)
```

### Read (查询)

```python
# 查询所有
projects = Project.objects.all()

# 条件查询
project = Project.objects.get(id=1)
projects = Project.objects.filter(is_active=True)

# 排序
projects = Project.objects.order_by('-created_at')

# 链式查询
projects = Project.objects.filter(
    is_active=True
).exclude(
    name='测试'
).order_by('-created_at')[:10]

# 复杂查询
from django.db.models import Q
projects = Project.objects.filter(
    Q(name__contains='测试') | Q(description__contains='测试')
)

# 聚合查询
from django.db.models import Count, Avg
Project.objects.aggregate(total=Count('id'))
Project.objects.values('is_active').annotate(count=Count('id'))
```

### Update (更新)

```python
# 方式1: 单个更新
project = Project.objects.get(id=1)
project.name = '新名称'
project.save()

# 方式2: 批量更新
Project.objects.filter(is_active=False).update(is_active=True)

# 方式3: F表达式(避免竞态条件)
from django.db.models import F
Project.objects.filter(id=1).update(
    views=F('views') + 1
)
```

### Delete (删除)

```python
# 方式1: 单个删除
project = Project.objects.get(id=1)
project.delete()

# 方式2: 批量删除
Project.objects.filter(is_active=False).delete()

# 方式3: 软删除(推荐)
Project.objects.filter(id=1).update(is_deleted=True)
```

---

## 4. 类视图 (Class-Based Views)

### 基础类视图

```python
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@method_decorator(csrf_exempt, name='dispatch')
class ProjectView(View):
    """项目管理视图"""

    def get(self, request):
        """获取项目列表"""
        projects = Project.objects.all()
        data = [
            {
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'created_at': p.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for p in projects
        ]
        return JsonResponse({'code': 200, 'data': data})

    def post(self, request):
        """创建项目"""
        try:
            body = json.loads(request.body)
            project = Project.objects.create(
                name=body['name'],
                description=body.get('description', '')
            )
            return JsonResponse({
                'code': 201,
                'message': '创建成功',
                'data': {'id': project.id}
            })
        except Exception as e:
            return JsonResponse({'code': 400, 'message': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class ProjectDetailView(View):
    """项目详情视图"""

    def get(self, request, pk):
        """获取项目详情"""
        try:
            project = Project.objects.get(id=pk)
            return JsonResponse({
                'code': 200,
                'data': {
                    'id': project.id,
                    'name': project.name,
                    'description': project.description,
                }
            })
        except Project.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '项目不存在'})

    def put(self, request, pk):
        """更新项目"""
        try:
            project = Project.objects.get(id=pk)
            body = json.loads(request.body)
            project.name = body.get('name', project.name)
            project.description = body.get('description', project.description)
            project.save()
            return JsonResponse({'code': 200, 'message': '更新成功'})
        except Project.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '项目不存在'})

    def delete(self, request, pk):
        """删除项目"""
        try:
            project = Project.objects.get(id=pk)
            project.delete()
            return JsonResponse({'code': 200, 'message': '删除成功'})
        except Project.DoesNotExist:
            return JsonResponse({'code': 404, 'message': '项目不存在'})
```

### 路由配置

```python
# myapp/urls.py
from django.urls import path
from .views import ProjectView, ProjectDetailView

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]
```

### 通用类视图

```python
from django.views.generic import ListView, DetailView, CreateView

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    paginate_by = 10

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'
```

---

## 5. DRF (Django REST Framework)

### 安装配置

```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Serializer 序列化器

```python
from rest_framework import serializers
from .models import Project, TestCase

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class TestCaseSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = TestCase
        fields = ['id', 'project', 'project_name', 'title', 'level', 'steps', 'expected', 'created_at']
```

### ViewSet 视图集

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

class ProjectViewSet(viewsets.ModelViewSet):
    """项目视图集"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=['get'])
    def test_cases(self, request, pk=None):
        """获取项目的测试用例"""
        project = self.get_object()
        test_cases = project.test_cases.all()
        serializer = TestCaseSerializer(test_cases, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """获取启用的项目"""
        projects = Project.objects.filter(is_active=True)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)
```

### DRF路由

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### DRF常用功能

```python
# 分页
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100


# 过滤
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']


# 权限
from rest_framework.permissions import BasePermission

class IsProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
```

---

## 相关链接

- [[DRF框架基础总结]] — Django REST Framework核心用法总结
