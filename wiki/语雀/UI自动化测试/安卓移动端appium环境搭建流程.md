---
type: knowledge
title: "安卓移动端Appium环境搭建流程"
source: "https://www.yuque.com/bbuer/cskf/mtx8xut1saoox3u0"
source_platform: yuque
category: "UI自动化测试"
created: 2026-06-30
updated: 2026-06-30
tags:
  - appium
  - 移动端测试
  - UI自动化
  - 安卓
status: mature
related:
  - "[[UI自动化测试日常问题记录]]"
  - "[[移动端自动化框架搭建问题点记录]]"
  - "[[Web自动化总结]]"
  - "[[APP测试]]"
---

# 安卓移动端Appium环境搭建流程

## 1. Node.js 安装

### 下载安装

```bash
# 官网下载: https://nodejs.org/
# 推荐 LTS 版本

# 验证安装
node -v
npm -v
```

### 配置npm镜像(可选)

```bash
# 使用淘宝镜像加速
npm config set registry https://registry.npmmirror.com

# 验证配置
npm config get registry
```

## 2. JDK 配置

### 安装 JDK

```bash
# 下载 JDK 8 或 JDK 11
# 官网: https://www.oracle.com/java/technologies/downloads/

# 验证安装
java -version
javac -version
```

### 配置环境变量

```bash
# Windows 环境变量设置
JAVA_HOME = C:\Program Files\Java\jdk-11
Path 添加: %JAVA_HOME%\bin

# 验证
echo %JAVA_HOME%
```

### Linux/Mac 配置

```bash
# 编辑 ~/.bashrc 或 ~/.zshrc
export JAVA_HOME=/usr/local/jdk-11
export PATH=$JAVA_HOME/bin:$PATH

# 生效
source ~/.bashrc
```

## 3. Android SDK 配置

### 安装方式

| 方式 | 说明 |
|------|------|
| Android Studio | 完整开发环境，包含SDK |
| 命令行工具 | 仅SDK，体积小 |

### 环境变量配置

```bash
# Windows
ANDROID_HOME = C:\Users\用户名\AppData\Local\Android\Sdk
Path 添加:
  %ANDROID_HOME%\platform-tools
  %ANDROID_HOME%\tools
  %ANDROID_HOME%\tools\bin

# Linux/Mac
export ANDROID_HOME=~/Android/Sdk
export PATH=$ANDROID_HOME/platform-tools:$PATH
export PATH=$ANDROID_HOME/tools:$PATH
export PATH=$ANDROID_HOME/tools/bin:$PATH
```

### 常用命令

```bash
# 查看已安装的SDK
sdkmanager --list

# 安装必要组件
sdkmanager "platform-tools"
sdkmanager "platforms;android-30"
sdkmanager "build-tools;30.0.3"

# 查看连接的设备
adb devices

# 查看设备详细信息
adb devices -l
```

## 4. Appium 安装配置

### 安装 Appium Server

```bash
# 全局安装 Appium
npm install -g appium

# 验证安装
appium --version

# 安装 UiAutomator2 驱动(安卓)
appium driver install uiautomator2
```

### 安装 Appium Desktop(可选)

```
# 下载地址: https://github.com/appium/appium-desktop/releases
# 提供图形界面，便于调试
```

### Python 客户端安装

```bash
# 安装 Appium Python Client
pip install Appium-Python-Client

# 验证
python -c "from appium import webdriver; print('OK')"
```

## 5. 环境验证

### 完整检查脚本

```python
import subprocess
import sys

def check_env():
    """检查Appium环境配置"""
    checks = {
        "Node.js": "node -v",
        "npm": "npm -v",
        "Java": "java -version",
        "ADB": "adb version",
        "Appium": "appium --version",
    }

    for name, cmd in checks.items():
        try:
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True
            )
            print(f"[OK] {name}: {result.stdout.strip() or result.stderr.strip()}")
        except FileNotFoundError:
            print(f"[FAIL] {name}: 未安装")

if __name__ == "__main__":
    check_env()
```

### 设备连接测试

```bash
# 1. 连接设备(USB调试已开启)
adb devices

# 2. 获取设备信息
adb -s 设备ID shell getprop ro.build.version.release  # Android版本
adb -s 设备ID shell getprop ro.product.model           # 设备型号

# 3. 启动Appium Server
appium --address 127.0.0.1 --port 4723
```

## 6. 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `adb devices` 无设备 | USB调试未开启 | 开启开发者选项和USB调试 |
| Appium启动失败 | 端口被占用 | `appium -p 4724` 指定其他端口 |
| SDK路径错误 | 环境变量配置错误 | 检查 `ANDROID_HOME` 配置 |
| Java版本不兼容 | JDK版本过高/过低 | 使用JDK 8或11 |

---

## 相关链接

- [[Web自动化总结]] — Web自动化测试Selenium完整实战
- [[APP测试]] — APP功能测试、兼容性测试与专项测试
