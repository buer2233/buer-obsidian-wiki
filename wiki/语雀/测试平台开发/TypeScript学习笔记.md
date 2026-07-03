---
type: knowledge
title: "TypeScript学习笔记"
source: "https://www.yuque.com/bbuer/cskf/wbpcn8tg4zrgshrk"
source_platform: yuque
category: "测试平台开发"
created: 2026-06-30
updated: 2026-06-30
tags:
  - typescript
  - javascript
  - 前端
status: mature
related:
  - "[[Vue前端学习笔记]]"
  - "[[Django 学习笔记]]"
---

# TypeScript学习笔记

## 1. TypeScript 入门

### 什么是 TypeScript

TypeScript 是 JavaScript 的超集，添加了类型系统和其他特性。

### 安装配置

```bash
# 全局安装
npm install -g typescript

# 初始化配置
tsc --init

# 编译
tsc app.ts

# 监听模式
tsc --watch
```

### tsconfig.json 基础配置

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## 2. 字段类型

### 基础类型

```typescript
// 布尔值
let isDone: boolean = false;

// 数字
let decimal: number = 6;
let hex: number = 0xf00d;
let binary: number = 0b1010;

// 字符串
let color: string = "blue";
let greeting: string = `Hello, ${color}`;

// 数组
let list: number[] = [1, 2, 3];
let list2: Array<number> = [1, 2, 3];

// 元组
let x: [string, number] = ["hello", 10];

// 枚举
enum Color {
  Red = "RED",
  Green = "GREEN",
  Blue = "BLUE"
}
let c: Color = Color.Red;

// Any
let notSure: any = 4;
notSure = "maybe a string";
notSure = false;

// Void
function warnUser(): void {
  console.log("This is a warning message");
}

// Null 和 Undefined
let u: undefined = undefined;
let n: null = null;

// Never
function error(message: string): never {
  throw new Error(message);
}

// Object
let obj: object = { name: "TypeScript" };
```

### 联合类型

```typescript
let id: string | number;
id = 101;
id = "101";

// 类型守卫
function printId(id: string | number) {
  if (typeof id === "string") {
    console.log(id.toUpperCase());
  } else {
    console.log(id);
  }
}
```

### 字面量类型

```typescript
type Direction = "up" | "down" | "left" | "right";
let dir: Direction = "up";

type StatusCode = 200 | 201 | 400 | 404 | 500;
```

---

## 3. 接口 (Interface)

### 基础接口

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  age?: number;           // 可选属性
  readonly createdAt: Date; // 只读属性
}

const user: User = {
  id: 1,
  name: "张三",
  email: "zhangsan@example.com",
  createdAt: new Date()
};

// user.createdAt = new Date(); // 错误：只读属性
```

### 函数接口

```typescript
interface SearchFunc {
  (source: string, subString: string): boolean;
}

const mySearch: SearchFunc = (src, sub) => {
  return src.search(sub) > -1;
};
```

### 类接口

```typescript
interface Animal {
  name: string;
  sound(): string;
}

class Dog implements Animal {
  name: string;

  constructor(name: string) {
    this.name = name;
  }

  sound(): string {
    return "汪汪";
  }
}
```

### 接口继承

```typescript
interface Shape {
  color: string;
}

interface Square extends Shape {
  sideLength: number;
}

// 多继承
interface ColoredSquare extends Shape, Square {
  opacity: number;
}
```

---

## 4. 属性修饰符

### 类的访问修饰符

```typescript
class Person {
  // public: 公开的，任何地方都能访问
  public name: string;

  // private: 私有的，只能在类内部访问
  private age: number;

  // protected: 受保护的，类内部和子类可以访问
  protected gender: string;

  // readonly: 只读，初始化后不能修改
  readonly id: number;

  constructor(id: number, name: string, age: number, gender: string) {
    this.id = id;
    this.name = name;
    this.age = age;
    this.gender = gender;
  }

  // 公开方法
  public greet(): string {
    return `你好，我是${this.name}`;
  }

  // 私有方法
  private getAge(): number {
    return this.age;
  }
}

const person = new Person(1, "张三", 25, "男");
console.log(person.name);   // OK
// console.log(person.age);  // 错误：私有属性
// console.log(person.id = 2); // 错误：只读属性
```

### 参数属性

```typescript
class Animal {
  constructor(
    public name: string,
    private age: number,
    protected sound: string
  ) {}
}

// 等价于
class Animal2 {
  public name: string;
  private age: number;
  protected sound: string;

  constructor(name: string, age: number, sound: string) {
    this.name = name;
    this.age = age;
    this.sound = sound;
  }
}
```

### 存取器 (Getters/Setters)

```typescript
class Temperature {
  private _celsius: number;

  constructor(celsius: number) {
    this._celsius = celsius;
  }

  get fahrenheit(): number {
    return this._celsius * 9 / 5 + 32;
  }

  set fahrenheit(value: number) {
    this._celsius = (value - 32) * 5 / 9;
  }

  get celsius(): number {
    return this._celsius;
  }

  set celsius(value: number) {
    if (value < -273.15) {
      throw new Error("温度不能低于绝对零度");
    }
    this._celsius = value;
  }
}

const temp = new Temperature(100);
console.log(temp.fahrenheit); // 212
temp.fahrenheit = 32;
console.log(temp.celsius);    // 0
```

---

## 5. 抽象类 (Abstract Class)

### 定义抽象类

```typescript
abstract class Shape {
  abstract area(): number;      // 抽象方法，子类必须实现
  abstract perimeter(): number;

  // 普通方法
  describe(): string {
    return `面积: ${this.area()}, 周长: ${this.perimeter()}`;
  }
}

class Circle extends Shape {
  constructor(private radius: number) {
    super();
  }

  area(): number {
    return Math.PI * this.radius ** 2;
  }

  perimeter(): number {
    return 2 * Math.PI * this.radius;
  }
}

class Rectangle extends Shape {
  constructor(private width: number, private height: number) {
    super();
  }

  area(): number {
    return this.width * this.height;
  }

  perimeter(): number {
    return 2 * (this.width + this.height);
  }
}

// const shape = new Shape(); // 错误：不能实例化抽象类
const circle = new Circle(5);
console.log(circle.describe()); // 面积: 78.54, 周长: 31.42
```

### 抽象类 vs 接口

| 特性 | 抽象类 | 接口 |
|------|--------|------|
| 实例化 | 不能 | 不能 |
| 实现 | 可以有实现 | 纯声明 |
| 构造函数 | 可以有 | 不能 |
| 访问修饰符 | 支持 | 不支持 |
| 多继承 | 单继承 | 多继承 |

---

## 6. 泛型 (Generics)

### 泛型函数

```typescript
function identity<T>(arg: T): T {
  return arg;
}

let output1 = identity<string>("hello");
let output2 = identity<number>(42);
let output3 = identity("hello"); // 类型推断
```

### 泛型接口

```typescript
interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

interface User {
  id: number;
  name: string;
}

async function getUser(): Promise<ApiResponse<User>> {
  const response = await fetch('/api/user');
  return response.json();
}
```

### 泛型类

```typescript
class DataStore<T> {
  private items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }

  getById(index: number): T | undefined {
    return this.items[index];
  }

  getAll(): T[] {
    return [...this.items];
  }

  remove(index: number): T | undefined {
    return this.items.splice(index, 1)[0];
  }
}

const userStore = new DataStore<User>();
userStore.add({ id: 1, name: "张三" });
```

### 泛型约束

```typescript
interface HasLength {
  length: number;
}

function logLength<T extends HasLength>(arg: T): T {
  console.log(arg.length);
  return arg;
}

logLength("hello");     // OK
logLength([1, 2, 3]);   // OK
// logLength(123);       // 错误：number没有length属性
```

---

## 7. 工具类型

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  age: number;
}

// Partial: 所有属性变为可选
type PartialUser = Partial<User>;

// Required: 所有属性变为必选
type RequiredUser = Required<PartialUser>;

// Readonly: 所有属性变为只读
type ReadonlyUser = Readonly<User>;

// Pick: 选取部分属性
type UserBasic = Pick<User, "id" | "name">;

// Omit: 排除部分属性
type UserWithoutEmail = Omit<User, "email">;

// Record: 构造键值对类型
type UserRoles = Record<string, string[]>;

// Exclude: 从联合类型中排除
type Status = "active" | "inactive" | "deleted";
type ActiveStatus = Exclude<Status, "deleted">;

// Extract: 从联合类型中提取
type NonDeleted = Extract<Status, "active" | "inactive">;

// ReturnType: 获取函数返回类型
function getUser() {
  return { id: 1, name: "张三" };
}
type UserType = ReturnType<typeof getUser>;
```
