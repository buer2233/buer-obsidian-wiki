---
type: knowledge
title: "Web自动化测试"
source: "xmind/08-web自动化总结.xmind"
source_platform: xmind
category: "软件测试学习资料"
created: 2026-06-30
updated: 2026-06-30
tags:
  - 软件测试
  - Web自动化
  - Selenium
status: mature
related:
  - "[[软件测试学习资料]]"
  - "[[UI自动化测试日常问题记录]]"
  - "[[安卓移动端appium环境搭建流程]]"
---

# web自动化

## 1.自动化测试

### 1.为什么要用自动化测试

#### 重复性高的测试工作

#### 提高执行测试效率

#### 在非工作时间执行

#### 每次执行的方式/步骤都是一样的

### 2.什么样的项目适合自动化

#### 1.需求稳定项目

#### 2.周期长的项目

#### 3.代码复用度高项目

### 3.自动化测试应用

#### 兼容性测试

#### 回归测试

#### 冒烟测试(接口部分)

#### 性能测试

### 4.自动化测试优缺点

#### 优点
- 提高测试执行效率,节约时间成本(只是节约执行测试的时间)
- 解放人力去做更加重要的工作(需求评审和用例设计)
- 可以重复利用, 减少对人的依赖
- 提高客户满意度
- 提升整个软件测试团队的水平
- 大幅减少兼容测试的工作量
- 部分的测试只能依靠自动化测试才能完成(压力测试, 并发测试)

#### 缺点
- 开发自动化测试脚本的时间周期较长
- 随着产品的不断迭代, 自动化脚本也需要不断的迭代, 时间成本高
- 不同项目之间的自动化脚本的重用度低
- 短期项目实施自动化测试的意义不大
- 自动化测试无法替代手工测试发现BUG
- 自动化测试对测试人员的技术要求较高

### 5.自动化测试工具

#### 单元测试
- unittest
- pytest

#### 接口测试
- postman
- jmeter
- requests

#### 页面测试
- selenium
- appium
- RF

## 2.Selenium

### 1.selenium环境搭建

#### 1.安装selenium
- pip install selenium

#### 2.安装浏览器和对应的驱动
- 谷歌浏览器
- ChromeDriver
- 火狐浏览器
- geckodriver
- Edge
- 下载 msedgedriver.exe 改名为 MicrosoftWebDriver.exe
- Ie
- IEDriverServer

#### 3.安装浏览器驱动
- 对应浏览器名称和版本

### 2.selenium环境检查

#### selenium操作对象---浏览器

#### 1.导入selenium
- from selenium import webdriver

#### 2.打开浏览器
- driver = webdriver.Chrome()

#### 3.输入网址
- driver.get(网址)

#### 4.操作项目
- 1.元素定位
- 2.元素操作

#### 5.关闭浏览器
- driver.quit()

### 3.selenium操作浏览器

#### 打开浏览器
- driver = webdriver.Chrome()

#### 浏览器窗口设置
- 设置固定大小
- driver.set_window_size(宽,高)
- 浏览器最大化
- driver.maximize_window()

#### 浏览器前进,后退,刷新
- driver.forward()
- driver.back()
- driver.refresh()

#### 关闭浏览器
- driver.close()
- driver.quit()

### 4.selenium元素定位

#### id定位
- driver.find_elements_by_id(id属性值)

#### name定位
- driver.find_element_by_name(name属性值)

#### class_name定位
- driver.find_element_by_class_name(class属性值)

#### link_text
- driver.find_element_by_link_text(链接文本值)

#### partial_link_text
- driver.find_element_by_partial_link_text(链接部分文本值)
- 是link_text定位方法的补充,项目中优先使用

#### tag_name
- driver.find_elements_by_tag_name(标签名)
- 不推荐使用

#### xpath
- driver.find_element_by_xpath('xpath表达式')
- xpath表达式
- //标签名[@属性名="属性值"]
- 标签+属性
- //父标签名[@父标签属性名="属性值"]/子标签名
- 层级
- //父标签名[@父标签属性名="属性值"]/子标签名[索引值]
- 索引从1开始
- last()
- //标签名[contains(@属性名,"部分属性值")]
- 模糊匹配
- //标签名[@属性名1="属性值" and @属性名2="属性值"]
- 多条件

#### css_selector
- driver.find_element_by_css_selector('css选择器')
- css选择器
- 标签+属性
- # id属性值
- . class属性值
- 标签名[属性名="属性值"]
- 层级
- 父标签名[属性名=属性值]>子标签名称
- 父标签名[属性名=属性值] 子标签名称
- > 或 空格 都可以
- 索引
- :nth_child(索引值)
- 顺位第n个标签
- 子标签名:nth_of_type(索引值)
- 指定子标签名称的第n个
- 模糊匹配
- 标签名[属性名*="部分属性值"]
- 多条件
- 标签名[属性名1="属性值1"][属性名2="属性值2"]

#### 基本定位方法

#### 专门定位a标签

### 5.元素操作

#### 1.基本操作
- 点击
- 元素.click()
- 输入
- 元素.send_keys('输入的内容')
- 清空
- 元素.clear()
- 项目中业务操作

#### 2.其他操作
- 1.获取页面标题
- driver.title
- 2.获取元素文本值
- 元素.text
- 文本指的是标签之间的文字
- 3.获取元素属性值
- 元素.get_attribute("属性名")
- 4.判断元素是否可见
- 元素.isdisplayed()
- 5.判断元素是否可用
- 元素.isenabled()
- 针对页面判断

### 6.鼠标事件

#### 1.确定需要执行鼠标事件的元素
- 元素定位

#### 2.选择对应的鼠标事件方法
- 鼠标悬停
- move_to_element(元素)
- 鼠标拖拽
- drag_and_drop(起始元素,目标元素)
- drag_and_drop_by_offset(起始元素,x坐标,y坐标)
- 鼠标双击
- double_click(元素)

#### 3.执行鼠标事件
- ActionChains(driver).鼠标事件方法.perform()

### 7.键盘事件

#### 1.使用Keys类

#### 2.借助于send_keys(Keys.键名称)

### 8.下拉菜单

#### 1.直接操作菜单中选项
- 定位选项元素
- 点击操作

#### 2.根据下拉菜单,查找选项
- 1.定位下拉菜单
- 2.定位菜单选项
- 二次定位
- 父元素-->子元素
- 3.点击操作

#### 3.使用Select类
- 1.定位下拉菜单的元素,并实例化Select类
- select = Select(定位的下拉菜单元素)
- 2.使用select类方法
- select.select_by_index()
- 根据索引选择选项
- select.select_by_value ()
- 根据value属性值选择选项
- select.select_by_visible_text()
- 根据选项文本值选择选项

### 9.滚动条(Python运行JS)

#### 1.常规操作
- js='window.scrollTo(0,1000)'
- 向下滚动1000px
- js='window.scrollTo(0,0)'
- 向上滚动到最上方
- driver.execute_script(js)
- 执行JS脚本

#### 2.聚焦元素
- 1.js代码
- js='arguments[0].scrollintoView();'
- 2.定位需要聚焦的元素
- target
- 3.driver.execute_script(js,target)

### 10.iframe操作

#### 1.确定操作的元素在iframe中
- 1.在F12最下方可以看见iframe\frame标签
- 2.使用常规的正确定位方式无法定位,大概率就在iframe里面
- 3.一般登录界面,邮箱界面和富文本输入框一般都是iframe

#### 2.进入iframe
- driver.switch_to.frame(参数)
- 参数 = iframe标签的id/name属性值
- 参数 = iframe元素
- 参数 = 索引值 从0开始
- 进入iframe时,一层一层进入, 退出可以一次退出

#### 3.操作iframe中的元素

#### 4.退出iframe
- driver.switch_to.parent_frame()
- 退回到上一层
- driver.switch_to.default_content()
- 直接退出

### 11.多窗口切换

#### selenium官方方法
- 1.获取当前窗口句柄
- driver.current_window_handle
- 2.操作触发多窗口出现的元素
- 3.获取所有窗口句柄
- driver.window_handles
- 4.进入新窗口
- driver.switch_to.window(新窗口句柄)
- 5.操作新窗口元素
- 6.退出新窗口
- driver.switch_to.window(原窗口句柄)

#### 结合js操作
- 1.使用js去掉触发多窗口出现元素的target属性
- js = document.getElementById("id属性值").removeAttribute("target")
- driver.execute_script(js)
- 2.按照常规方式操作即可

### 12.弹窗处理

#### 1.自带弹窗
- 弹窗格式
- alert
- prompt
- confirm
- 1.操作触发弹窗出现的元素
- 2.捕获弹窗
- alert = driver.switch_to.alert
- 3.操作弹窗
- 获取弹窗文本值
- alert.text
- 点击确定按钮
- alert.accept()
- 点击取消按钮
- alert.dismiss()
- 输入文字
- alert.send_keys()

#### 2.自定义弹窗
- 不让弹窗在页面中显示
- 给元素增加属性 style.display: none

### 13.单选框和复选框

#### 单选框
- input标签 type="radio"

#### 复选框
- input标签 type="checkbox"

#### 在操作之间判断是否被选中
- 元素.isselected()

### 14.文件上传

#### 元素.send_keys(文件路径)

### 15.元素等待

#### time.sleep(强制等待时间)

#### driver.implicitly_wait(最长等待时间)

#### WebDriverWait(driver,timeout).until(方法)
- 引入from selenium.webdriver.support.wait import WebDriverWait

### 16.验证码

#### 1.去掉验证码

#### 2.万能验证码

#### 3.验证码识别技术

#### 4.绕过验证码
- 1.浏览器加载项
- 2.使用cookie
- 1 获取cookie(其中最重要的是 name 和 value)
- driver.get_cookies():获取所有cookie,以列表的形式返回,列表内的每个字典就是一个cookie
- driver.get_cookie("对应cookie的name值")
- 2.添加cookie
- driver.add_cookie(字典格式)
- 只需要添加包含 name和value键的字典即可
- 3.使用token

### 17.EC模块

#### from selenium.webdriver.support import expected_conditions as EC

#### EC.title_is(需要断言判断的页面标题名)(driver)

## 3.自动化测试实施

### 1.自动化测试用例

#### 根据用例选型标准，从手工测试用例中，选取重复度较高，流程较简单的用例，转化为自动化测试用例

### 2.自动化测试设计

#### 1.设计思路
- 1.编程语言
- python
- 2.使用工具
- selenium, appium
- 3.设计模式(面向对象)
- PO设计模式
- 4.测试用例管理
- Test Case
- 5.测试数据管理
- Test Data
- 6.测试报告生成
- Test Report
- 7.持续集成
- 8.日志模块

#### 2.设计框架
- Common
- 公共方法
- Page
- 所有测试模块的页面类
- Case
- 测试用例
- Data
- 测试数据
- Report
- 测试报告

#### 3.具体步骤
- 项目名称
- Common: 公共方法
- Base类
- 基础类
- 对selenium二次封装
- 操作文件方法
- OperationData
- Page:页面类
- 项目中每一个页面,作为一个对象/类
继承Base类
- 表现层
- 封装本页面的所有元素的定位器
- 操作层
- 封装本页面的所有操作
- Case: 测试用例
- 用例的编写规则
- 0.unittest的测试py文件名,最好以test开头. 例:test_login.py
- 1.创建测试类,测试类名仍然以Test开头.且必须继承unittest.TestCase
- 2.创建测试方法,必须以test开头
- 3.执行文本中测试用例, 使用unittest.main()
- 4.在测试类中可以写普通的方法,但必须被测试方法调用
- 用例的执行顺序
- 默认执行顺序是按照ASCII字符集的顺序进行执行
- 控制执行顺序的方法,规范测试用例命名: test_01
- 断言
- assertEqual(a, b, "断言失败的提示")
- 断言a和b是否相等(值相等, 等同于==)
- assertTrue(表达式, "断言失败的提示")
- 断言表达式是否为真
- 跳过测试
- @unittest.skip()
- 无条件跳过装饰的测试用例
- @unittest.skipif(条件, 原因)
- 满足条件时(条件为真), 跳过装饰的测试用例
- @unittest.skipUnless(条件, 原因)
- 不满足条件时(条件为假), 跳过装饰的测试用例
- TestFixture(测试夹具)
- 类级别
- setUpClass(cls)
- 在测试类执行之前,先执行的方法
- tearDownClass(cls)
- 在整个测试类执行完之后,执行收尾的方法
- 方法级别
- setUp(self)
- 在每次执行测试用例前执行的前置条件
- tearDown(self)
- 在每次用例执行完毕之后,执行的收尾的方法
- Data: 测试数据
- 使用XLS文件或CSV文件保存测试所需的数据, 通过ddt模块实现参数化
- Report: 测试报告
- 使用HTMLTestRunnerPlugins模块插件

## 自动化测试总结

### 什么是关键字驱动？

#### 简单而言，就是根据实际的业务需求对selenium的常用功能记性的二次封装

#### 可以让不懂代码的测试人员也能做自动化测试，彻底地实现测试步骤、测试数据和程序的分离

### 什么是数据驱动？

#### 也可叫测试用例参数化。固定的程序，固定的测试步骤，使用不同的数据进行测试，就叫数据驱动测试。

#### 将代码和数据进行分离，单纯由数据组成文件，在由文件来驱动关键字，最终实现整个自动化的过程

### 什么是关键字驱动+数据驱动？

#### 读取数据
- 读取数据， 将固定格式的数据进行拼接

#### 传入数据
- 拼接后的内容作为关键字所需要的参数，进行传入

#### 执行关键字，断言结果
- 调用关键字，将执行结果和预期结果进行对比，从而获取单条测试用例执行是否通过的结果

#### 也是一种设计模式

### 什么是PO设计模式
（page object model）

#### 把待测页面当做一个页面对象，一般包含了元素对象的定位和元素对象的操作，将页面对象和真实的网站页面一一映射起来

### PO模式的分层

#### 三层
- 对象库层（基础方法）
- 根据实际的项目需求对selenium进行的二次封装
- 页面操作层（逻辑层）
- Page类：封装元素操作和元素定单位
- 测试层（业务层）
- 多个页面操作完成一个业务测试，一般结合单元测试框（unittest、pytest）来测试

#### 四层
- 对象库层
- 根据实际的项目需求对selenium进行的二次封装
- 表情层
- page中封装的元素定位
- 操作层
- page中分装的元素操作
- 测试层（业务层）
- 多个页面操作完成一个业务测试，一般结合单元测试框（unittest、pytest）来测试

### PO模式的优势

#### 明显降低代码冗余
- 二次封装selenium方法和提取公共方法，提高代码的复用性

#### 提升代码的可阅读性
- 因为多层分级， 将不同的内容进行不同的封装，整体提升了代码的可阅读性

#### 提升代码的可维护性
- 在UI测试中，页面经常变动，代码的维护量也随之增加，多层分级，我们只需要修改page页面对象的代码，如元素低定位器，不用修改用例， 也能正常的执行用例

#### 降低代码的耦合性
- 达到高内聚、低耦合的效果

---

## 相关链接

- [[UI自动化测试日常问题记录]] — UI自动化测试常见问题与解决方案
- [[安卓移动端appium环境搭建流程]] — Appium移动端自动化环境搭建