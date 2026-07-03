---
type: knowledge
title: "DRF框架基础总结"
source: "xmind/11-DRF框架基础总结.xmind"
source_platform: xmind
category: "软件测试学习资料"
created: 2026-06-30
updated: 2026-06-30
tags:
  - Python
  - Django
  - DRF
status: mature
related:
  - "[[软件测试学习资料]]"
  - "[[Django 学习笔记]]"
  - "[[flask平台代码简介]]"
  - "[[测试平台基础]]"
---

# 11-DRF框架基础总结

## 学习地址

### https://www.cnblogs.com/clschao/articles/10526431.html

## 常用命令

### 1. 创建项目 django-admin startproject 项目名称

### 2. 运行项目 python manage.py runserver or python manage.py runserver ip:端口

### 3. 创建子应用 python manage.py startapp 子应用名称

### 4. 数据迁移1 python manage.py makemigrations 应用名

### 5. 数据迁移2: migrate 应用名

### 6. 创建超级管理员账号: createsuperuser

## 项目目录

### 通用配置

#### settings
- 项目的全局配置

#### urls
- 项目全局的路由

### 子应用(模块)

#### model
- 定义数据库表结构

#### serializers
- 序列化器
- 序列化转换参数,已经控制查询范围和查询条件
- 常用的框架父类
- serializers.ModelSerializer

#### viwes
- 视图
- 存放接口逻辑
- 常用的框架父类
- ModelViewSet
- mixins.CreateModelMixin,
- 新增
- mixins.RetrieveModelMixin,
- 修改一个
- mixins.UpdateModelMixin,
- 修改多个
- mixins.DestroyModelMixin,
- 删除
- mixins.ListModelMixin,
- 查询
- GenericViewSet
- 其它通用的操作
- get_object
- 获取对象
- get_queryset
- 获取查询集

#### URLS
- 配置当前子应用的路由

## 数据操作

---

## 相关链接

- [[Django 学习笔记]] — Django Web框架完整学习笔记
- [[flask平台代码简介]] — Flask测试平台代码架构与实现
- [[测试平台基础]] — 测试平台核心功能与技术架构