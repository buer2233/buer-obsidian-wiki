---
type: knowledge
title: "Vue前端学习笔记"
source: "https://www.yuque.com/bbuer/cskf/uxt9ve5nvilgigdu"
source_platform: yuque
category: "测试平台开发"
created: 2026-06-30
updated: 2026-06-30
tags:
  - vue
  - 前端
  - javascript
  - web开发
status: mature
related:
  - "[[TypeScript学习笔记]]"
  - "[[Django 学习笔记]]"
  - "[[测试平台基础]]"
---

# Vue前端学习笔记

## 1. Vue 官方文档

### 核心概念

| 概念 | 说明 |
|------|------|
| 响应式数据 | 数据变化自动更新视图 |
| 组件化 | UI拆分为独立可复用的组件 |
| 指令 | 带有 `v-` 前缀的特殊属性 |
| 生命周期 | 组件从创建到销毁的过程 |

### Vue 3 vs Vue 2

| 特性 | Vue 2 | Vue 3 |
|------|-------|-------|
| API风格 | Options API | Composition API |
| 响应式 | Object.defineProperty | Proxy |
| 组件根节点 | 单根节点 | 多根节点(Fragment) |
| 性能 | 较好 | 更好(体积更小) |
| TypeScript | 支持一般 | 原生支持 |

### 官方资源

- 文档: https://cn.vuejs.org/
- GitHub: https://github.com/vuejs/vue
- Vue Router: https://router.vuejs.org/zh/
- Vuex/Pinia: https://pinia.vuejs.org/zh/

---

## 2. 开发工具

### 推荐工具

| 工具 | 说明 |
|------|------|
| VS Code | 主流编辑器 |
| Volar | Vue 3 官方插件 |
| Vue Devtools | 浏览器调试插件 |
| WebStorm | JetBrains IDE |

### VS Code 插件

```
必装:
- Volar (Vue 3 支持)
- ESLint (代码规范)
- Prettier (代码格式化)

推荐:
- Auto Rename Tag
- Path Intellisense
- GitLens
```

### 浏览器插件

```
Vue Devtools:
- Chrome: https://chrome.google.com/webstore/detail/vuejs-devtools
- Firefox: https://addons.mozilla.org/firefox/addon/vue-js-devtools
```

---

## 3. Vue 常用指令

### 模板指令

```vue
<template>
  <!-- 数据绑定 -->
  <p>{{ message }}</p>
  <p v-text="message"></p>
  <p v-html="htmlContent"></p>

  <!-- 属性绑定 -->
  <img :src="imageUrl" :alt="imageAlt">
  <div :class="{ active: isActive }"></div>
  <div :style="{ color: textColor, fontSize: size + 'px' }"></div>

  <!-- 条件渲染 -->
  <div v-if="type === 'A'">A</div>
  <div v-else-if="type === 'B'">B</div>
  <div v-else>C</div>
  <div v-show="isVisible">显示/隐藏</div>

  <!-- 列表渲染 -->
  <ul>
    <li v-for="(item, index) in items" :key="item.id">
      {{ index }}. {{ item.name }}
    </li>
  </ul>

  <!-- 事件处理 -->
  <button @click="handleClick">点击</button>
  <button @click.prevent="handleSubmit">提交</button>
  <input @input="handleInput" @keyup.enter="handleEnter">

  <!-- 表单绑定 -->
  <input v-model="username">
  <input v-model.number="age">
  <input v-model.trim="text">
  <input v-model.lazy="text">
</template>
```

### 事件修饰符

| 修饰符 | 说明 |
|--------|------|
| `.prevent` | 阻止默认行为 |
| `.stop` | 阻止事件冒泡 |
| `.once` | 只触发一次 |
| `.self` | 仅当事件源是元素本身时触发 |
| `.capture` | 使用捕获模式 |

### 按键修饰符

```vue
<input @keyup.enter="submit">
<input @keyup.esc="cancel">
<input @keyup.ctrl.s="save">
<input @keyup.shift.a="selectAll">
```

---

## 4. Vue 3 Composition API

### 基础用法

```vue
<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'

// 响应式数据
const count = ref(0)
const user = reactive({
  name: '张三',
  age: 25
})

// 计算属性
const doubleCount = computed(() => count.value * 2)

// 方法
function increment() {
  count.value++
}

// 监听器
watch(count, (newVal, oldVal) => {
  console.log(`count变化: ${oldVal} -> ${newVal}`)
})

// 生命周期
onMounted(() => {
  console.log('组件已挂载')
})
</script>
```

### 组件通信

```vue
<!-- 父组件 -->
<template>
  <ChildComponent
    :message="parentMsg"
    @update="handleUpdate"
  />
</template>

<script setup>
import { ref } from 'vue'
import ChildComponent from './ChildComponent.vue'

const parentMsg = ref('来自父组件的消息')

function handleUpdate(data) {
  console.log('子组件传来的数据:', data)
}
</script>

<!-- 子组件 ChildComponent.vue -->
<template>
  <div>
    <p>{{ message }}</p>
    <button @click="sendToParent">发送给父组件</button>
  </div>
</template>

<script setup>
const props = defineProps({
  message: String
})

const emit = defineEmits(['update'])

function sendToParent() {
  emit('update', { data: '来自子组件' })
}
</script>
```

---

## 5. Vue Router 路由

### 基础配置

```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/project/:id',
    name: 'Project',
    component: () => import('@/views/Project.vue'),
    props: true
  },
  {
    path: '/admin',
    component: () => import('@/views/Admin.vue'),
    children: [
      { path: 'users', component: () => import('@/views/Users.vue') },
      { path: 'settings', component: () => import('@/views/Settings.vue') }
    ],
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/404.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    next('/login')
  } else {
    next()
  }
})

export default router
```

### 路由使用

```vue
<template>
  <nav>
    <router-link to="/">首页</router-link>
    <router-link :to="{ name: 'Project', params: { id: 1 } }">项目1</router-link>
  </nav>
  <router-view />
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 编程式导航
function goToProject(id) {
  router.push({ name: 'Project', params: { id } })
}

function goBack() {
  router.back()
}

// 获取路由参数
console.log(route.params.id)
console.log(route.query.keyword)
</script>
```

---

## 6. Pinia 状态管理

### 安装

```bash
npm install pinia
```

### 定义Store

```javascript
// stores/project.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useProjectStore = defineStore('project', () => {
  // state
  const projects = ref([])
  const currentProject = ref(null)

  // getters
  const activeProjects = computed(() =>
    projects.value.filter(p => p.is_active)
  )

  // actions
  async function fetchProjects() {
    const response = await fetch('/api/projects')
    projects.value = await response.json()
  }

  async function createProject(project) {
    const response = await fetch('/api/projects', {
      method: 'POST',
      body: JSON.stringify(project)
    })
    const newProject = await response.json()
    projects.value.push(newProject)
    return newProject
  }

  return {
    projects,
    currentProject,
    activeProjects,
    fetchProjects,
    createProject
  }
})
```

### 使用Store

```vue
<script setup>
import { useProjectStore } from '@/stores/project'

const projectStore = useProjectStore()

// 访问state
console.log(projectStore.projects)

// 调用action
await projectStore.fetchProjects()

// 访问getter
console.log(projectStore.activeProjects)
</script>
```

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[测试平台基础]] — AI测试主题关联
- [[TypeScript学习笔记]] — AI测试主题关联
- [[Django 学习笔记]] — AI测试主题关联
- [[Flask学习笔记]] — AI测试主题关联
- [[flask平台代码简介]] — AI测试主题关联
- [[个人档案]] — AI测试主题关联
- [[Python基础总结]] — AI测试主题关联
- [[01_Python语言基础学习资料]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
