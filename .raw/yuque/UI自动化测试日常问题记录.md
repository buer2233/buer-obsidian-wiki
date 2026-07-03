# UI自动化测试日常问题记录

> 来源: https://www.yuque.com/bbuer/cskf/cg7oygq955vt5c6v
> 抓取时间: 2026-06-30
> 分组: UI自动化测试

---

## 1. 前端暂停JS代码（用于抓取自动消失弹窗的元素定位）

在做UI自动化测试时，经常会遇到一些自动消失的弹窗（如Toast提示），这些弹窗显示时间很短，无法通过常规方式抓取元素定位。

**解决方案：** 通过在浏览器控制台中暂停JS代码执行，使弹窗停留在页面上，从而可以获取其元素定位信息。

## 2. Xpath定位当前目录下的所有显示文本

使用XPath定位时，需要获取当前目录下所有的显示文本内容。

**示例XPath：**
```xpath
.//text()
```

## 3. 使用JS获取元素的样式参数

通过JavaScript可以获取元素的各种样式参数，用于验证UI样式是否正确。

**示例代码：**
```javascript
window.getComputedStyle(element).getPropertyValue('style-property');
```

## 4. 键盘Ctrl+鼠标左键点击操作组合

在自动化测试中，有时需要模拟键盘Ctrl+鼠标左键的组合操作（如多选操作）。

**解决方案：** 使用ActionChains或相应的API来组合键盘和鼠标操作。

## 5. XPATH定位某个div元素下不再包含任何其它子元素

需要定位一个div元素，且该div下不包含任何子元素（即叶子节点的div）。

**示例XPath：**
```xpath
//div[not(*)]
```

该XPath表达式会选择所有不包含任何子元素的div节点。
