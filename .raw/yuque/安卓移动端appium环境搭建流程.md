# 安卓移动端appium环境搭建流程

> 来源: https://www.yuque.com/bbuer/cskf/mtx8xut1saoox3u0
> 抓取时间: 2026-06-30
> 分组: UI自动化测试

---

## 基本步骤

1. 安装Node.js
2. 安装JDK，及配置环境变量
3. 安装SDK，及配置环境变量
4. 安装Appium桌面版本(建议安装GitHub的最新版)
5. python中pip下载Appium-Python-Client
6. 下载allure-2.13.8并加入环境变量
7. 管理员身份运行appium启动服务, 连接安卓真机

## 部分详细步骤

### 1. 安装Node.js

- 官网下载：https://nodejs.org/zh
- 安装完成后验证：`node -v`

### 2. 安装JDK

- 下载安装JDK
- 新增系统变量 `JAVA_HOME`，值为JDK安装路径
- 在 `path` 环境变量内新增以下路径：
  - `%JAVA_HOME%\bin`
  - `%JAVA_HOME%\lib\tools.jar`
  - `%JAVA_HOME%\jre\bin`

### 3. 安装SDK

- 下载地址：https://www.androiddevtools.cn/
- 添加系统变量 `ANDROID_HOME`，值为SDK安装路径
- 在 `path` 环境变量内新增以下路径：
  - `%ANDROID_HOME%\tools`
  - `%ANDROID_HOME%\platform-tools`
- 验证：`adb version`

### 4. 安装Appium桌面版本

- Appium官网：https://github.com/appium/appium-desktop/releases/tag/v1.22.3-4
- Appium Inspector（取样器）：https://github.com/appium/appium-inspector/releases
- 建议安装GitHub上的最新版本

### 5. 安装Appium-Python-Client

```bash
pip install Appium-Python-Client
```

### 6. 下载allure

- 下载 allure-2.13.8 并加入环境变量

### 7. 启动服务并连接真机

- 以管理员身份运行Appium启动服务
- 连接安卓真机（需开启USB调试模式）
