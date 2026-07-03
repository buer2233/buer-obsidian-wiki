# Vue前端学习笔记

> 来源: https://www.yuque.com/bbuer/cskf/uxt9ve5nvilgigdu
> 抓取时间: 2026-06-30
> 分组: 测试平台开发

---

## Vue官方文档

- Vue2官方文档：https://cn.vuejs.org/
- Vue3官方文档：https://v3.cn.vuejs.org/

## 开发工具

### VSCode推荐插件

- **Vetur**：Vue开发工具，提供语法高亮、智能提示、格式化等功能
- **Vue 2 Snippets**：Vue2代码片段
- **Vue VSCode Snippets**：Vue代码片段集合
- **ESLint**：代码规范检查工具
- **Prettier**：代码格式化工具
- **Auto Close Tag**：自动闭合HTML标签
- **Auto Rename Tag**：自动重命名配对的HTML标签
- **HTML CSS Support**：HTML中CSS类名提示
- **JavaScript (ES6) code snippets**：ES6代码片段

## Vue常用指令（Vue2）

### v-bind（:）

动态绑定属性：

```html
<img v-bind:src="imageUrl">
<!-- 缩写 -->
<img :src="imageUrl">
```

### v-on（@）

绑定事件监听器：

```html
<button v-on:click="handleClick">点击</button>
<!-- 缩写 -->
<button @click="handleClick">点击</button>
```

### v-model

双向数据绑定：

```html
<input v-model="message">
```

### v-if / v-else-if / v-else

条件渲染：

```html
<p v-if="type === 'A'">A</p>
<p v-else-if="type === 'B'">B</p>
<p v-else>其他</p>
```

### v-show

根据条件显示/隐藏元素（通过display属性）：

```html
<p v-show="isVisible">可见</p>
```

### v-for

列表渲染：

```html
<li v-for="(item, index) in items" :key="index">
  {{ item.name }}
</li>
```

### v-text / v-html

更新元素的textContent / innerHTML：

```html
<p v-text="message"></p>
<div v-html="htmlContent"></div>
```

### v-pre

跳过该元素和其子元素的编译：

```html
<span v-pre>{{ 这里的内容不会被编译 }}</span>
```

### v-cloak

保持元素在实例编译完成后才显示：

```css
[v-cloak] {
  display: none;
}
```

### v-once

只渲染一次，后续数据变化不再更新：

```html
<p v-once>{{ message }}</p>
```

## Vue环境安装

### 使用npm安装

```bash
# 安装Vue CLI
npm install -g @vue/cli

# 创建项目
vue create my-project

# 启动开发服务器
npm run serve
```

### 使用CDN引入

```html
<script src="https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.js"></script>
```

### 项目目录结构

```
my-project/
├── node_modules/     # 依赖包
├── public/           # 静态资源
│   ├── index.html
│   └── favicon.ico
├── src/              # 源代码
│   ├── assets/       # 资源文件
│   ├── components/   # 组件
│   ├── views/        # 页面
│   ├── router/       # 路由
│   ├── store/        # 状态管理
│   ├── App.vue       # 根组件
│   └── main.js       # 入口文件
├── package.json      # 项目配置
└── vue.config.js     # Vue配置
```
