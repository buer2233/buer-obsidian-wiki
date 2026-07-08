---
type: knowledge
title: "UI自动化测试日常问题记录"
source: "https://www.yuque.com/bbuer/cskf/cg7oygq955vt5c6v"
source_platform: yuque
category: "UI自动化测试"
created: 2026-06-30
updated: 2026-06-30
tags:
  - UI自动化
  - appium
  - 元素定位
  - xpath
status: mature
related:
  - "[[安卓移动端appium环境搭建流程]]"
  - "[[移动端自动化框架搭建问题点记录]]"
  - "[[Web自动化总结]]"
---

# UI自动化测试日常问题记录

## 问题1: JavaScript暂停执行

### 问题描述

在执行UI自动化测试时，页面JavaScript可能处于暂停状态，导致页面无响应。

### 解决方案

```python
# 方案1: 等待页面加载完成
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

# 方案2: 强制继续执行JS
driver.execute_script("window.stop();")

# 方案3: 刷新页面
driver.refresh()
```

### 预防措施

- 设置合理的页面加载超时时间
- 使用显式等待替代隐式等待
- 捕获 `TimeoutException` 进行重试

---

## 问题2: XPath定位失败

### 问题描述

使用XPath定位元素时，元素无法找到或定位错误。

### 常见原因

| 原因 | 说明 |
|------|------|
| 动态ID | 元素ID每次加载都变化 |
| iframe嵌套 | 元素在iframe内部 |
| 动态加载 | 元素异步加载未完成 |
| 命名空间 | XML命名空间影响XPath |

### 解决方案

```python
# 方案1: 使用相对XPath替代绝对XPath
# 不推荐: /html/body/div[1]/div[2]/form/input
# 推荐: //input[@placeholder='请输入用户名']

# 方案2: 切换到iframe
iframe = driver.find_element(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframe)
# 操作完成后切回
driver.switch_to.default_content()

# 方案3: 等待元素出现
from selenium.webdriver.support import expected_conditions as EC
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='target']"))
)

# 方案4: 使用contains模糊匹配
driver.find_element(By.XPATH, "//*[contains(@class, 'btn-')]")
```

---

## 问题3: JavaScript获取元素样式

### 问题描述

需要通过JavaScript获取元素的CSS样式属性。

### 解决方案

```python
# 获取计算后的样式
style = driver.execute_script("""
    var element = arguments[0];
    var style = window.getComputedStyle(element);
    return {
        color: style.color,
        backgroundColor: style.backgroundColor,
        fontSize: style.fontSize,
        display: style.display,
        visibility: style.visibility
    };
""", element)

print(f"颜色: {style['color']}")
print(f"背景: {style['backgroundColor']}")
print(f"字号: {style['fontSize']}")

# 获取单个样式属性
display = driver.execute_script(
    "return window.getComputedStyle(arguments[0]).display",
    element
)

# 获取内联样式
inline_style = driver.execute_script(
    "return arguments[0].style.cssText",
    element
)

# 获取所有计算样式
all_styles = driver.execute_script("""
    var el = arguments[0];
    var styles = {};
    var computed = window.getComputedStyle(el);
    for (var i = 0; i < computed.length; i++) {
        var prop = computed[i];
        styles[prop] = computed.getPropertyValue(prop);
    }
    return styles;
""", element)
```

---

## 问题4: 键盘组合键操作

### 问题描述

需要模拟键盘组合键操作，如 Ctrl+C、Ctrl+V、Ctrl+A 等。

### 解决方案

```python
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# 方案1: 使用send_keys
element = driver.find_element(By.ID, "input")
element.send_keys(Keys.CONTROL, 'a')  # Ctrl+A 全选
element.send_keys(Keys.CONTROL, 'c')  # Ctrl+C 复制
element.send_keys(Keys.CONTROL, 'v')  # Ctrl+V 粘贴

# 方案2: 使用ActionChains(更可靠)
actions = ActionChains(driver)

# Ctrl+A 全选
actions.key_down(Keys.CONTROL)
actions.send_keys('a')
actions.key_up(Keys.CONTROL)
actions.perform()

# Ctrl+Click 多选
element = driver.find_element(By.ID, "item1")
actions.key_down(Keys.CONTROL)
actions.click(element)
actions.key_up(Keys.CONTROL)
actions.perform()

# 方案3: 组合多个按键
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL)
actions.key_down(Keys.SHIFT)
actions.send_keys('z')  # Ctrl+Shift+Z
actions.key_up(Keys.SHIFT)
actions.key_up(Keys.CONTROL)
actions.perform()

# Mac系统使用Keys.COMMAND替代Keys.CONTROL
```

### 常用键盘组合

| 组合键 | 代码 |
|--------|------|
| Ctrl+A | `Keys.CONTROL, 'a'` |
| Ctrl+C | `Keys.CONTROL, 'c'` |
| Ctrl+V | `Keys.CONTROL, 'v'` |
| Ctrl+Z | `Keys.CONTROL, 'z'` |
| Enter | `Keys.ENTER` |
| Tab | `Keys.TAB` |
| Escape | `Keys.ESCAPE` |
| Delete | `Keys.DELETE` |

---

## 问题5: XPath定位优化

### 问题描述

XPath表达式性能差或不够稳定。

### 优化建议

```python
# 1. 优先使用ID定位(最快)
driver.find_element(By.ID, "username")

# 2. 使用CSS选择器(比XPath快)
driver.find_element(By.CSS_SELECTOR, ".btn-primary")

# 3. 避免使用绝对XPath
# 慢: /html/body/div[1]/div[2]/form/div[1]/input
# 快: //form[@id='login']//input[@name='username']

# 4. 使用text()定位文本元素
driver.find_element(By.XPATH, "//*[text()='登录']")
driver.find_element(By.XPATH, "//*[contains(text(), '登')]")

# 5. 使用多个属性组合定位
driver.find_element(By.XPATH, "//input[@type='text' and @name='username']")

# 6. 使用轴定位(ancestor, following, preceding等)
driver.find_element(By.XPATH, "//label[text()='用户名']/following-sibling::input")

# 7. 使用索引定位(最后手段)
driver.find_element(By.XPATH, "(//div[@class='item'])[3]")
```

### 定位策略优先级

| 优先级 | 方式 | 速度 | 稳定性 |
|--------|------|------|--------|
| 1 | ID | 最快 | 高 |
| 2 | Name | 快 | 高 |
| 3 | CSS Selector | 快 | 中 |
| 4 | XPath | 慢 | 中 |
| 5 | Link Text | 中 | 低 |

---

## 相关链接

- [[Web自动化总结]] — Web自动化测试Selenium完整实战

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[安卓移动端appium环境搭建流程]] — AI测试主题关联
- [[移动端自动化框架搭建问题点记录]] — AI测试主题关联
- [[Web自动化总结]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[通过AI+SKILL维护用例的测试记录]] — AI测试主题关联
- [[性能测试基础]] — AI测试主题关联
- [[01_Python语言基础学习资料]] — AI测试主题关联
- [[02_pytest必背学习资料]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
