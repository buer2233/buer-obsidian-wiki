# TypeScript学习笔记

> 来源: https://www.yuque.com/bbuer/cskf/wbpcn8tg4zrgshrk
> 抓取时间: 2026-06-30
> 分组: 测试平台开发

---

## 入门安装

### 安装TypeScript

```bash
npm install -g typescript
```

### 编译TypeScript

```bash
tsc hello.ts
```

### 初始化配置

```bash
tsc --init
```

## 配置文件（tsconfig.json）

```json
{
  "compilerOptions": {
    "target": "ES6",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

主要配置项说明：
- `target`：编译目标版本
- `module`：模块系统
- `strict`：启用所有严格类型检查
- `outDir`：输出目录
- `rootDir`：源文件目录
- `declaration`：生成声明文件
- `sourceMap`：生成source map文件

## 字段类型（Basic Types）

### 基础类型

```typescript
// 布尔值
let isDone: boolean = false;

// 数字
let decimal: number = 6;

// 字符串
let color: string = "blue";

// 数组
let list: number[] = [1, 2, 3];
let list2: Array<number> = [1, 2, 3];

// 元组
let x: [string, number] = ["hello", 10];

// 枚举
enum Color { Red, Green, Blue }
let c: Color = Color.Green;

// Any
let notSure: any = 4;

// Void
function warnUser(): void {
  console.log("warning");
}

// Null 和 Undefined
let u: undefined = undefined;
let n: null = null;

// Never
function error(message: string): never {
  throw new Error(message);
}

// Object
let obj: object = {};
```

## 属性修饰符（Access Modifiers）

TypeScript支持三种访问修饰符：

### public（公共）

```typescript
class Animal {
  public name: string;
  constructor(name: string) {
    this.name = name;
  }
}
```

`public` 是默认修饰符，可以在任何地方访问。

### private（私有）

```typescript
class Animal {
  private name: string;
  constructor(name: string) {
    this.name = name;
  }
}
```

`private` 修饰的属性只能在类内部访问。

### protected（受保护）

```typescript
class Animal {
  protected name: string;
  constructor(name: string) {
    this.name = name;
  }
}
```

`protected` 修饰的属性可以在类内部和子类中访问。

### readonly（只读）

```typescript
class Animal {
  readonly name: string;
  constructor(name: string) {
    this.name = name;
  }
}
```

`readonly` 修饰的属性只能在构造函数中赋值，之后不可修改。

## 抽象类（Abstract Classes）

```typescript
abstract class Animal {
  abstract makeSound(): void;

  move(): void {
    console.log("roaming the earth...");
  }
}

class Dog extends Animal {
  makeSound(): void {
    console.log("Woof! Woof!");
  }
}
```

- 抽象类不能被实例化
- 抽象方法必须在子类中实现
- 抽象类可以包含具体方法的实现

## 接口（Interfaces）

### 基本接口

```typescript
interface LabelledValue {
  label: string;
}

function printLabel(labelledObj: LabelledValue) {
  console.log(labelledObj.label);
}
```

### 可选属性

```typescript
interface SquareConfig {
  color?: string;
  width?: number;
}
```

### 只读属性

```typescript
interface Point {
  readonly x: number;
  readonly y: number;
}
```

### 函数类型接口

```typescript
interface SearchFunc {
  (source: string, subString: string): boolean;
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
```

### 接口与类型别名的区别

```typescript
// 接口 - 可以被extends和implements
interface IUser {
  name: string;
}

// 类型别名 - 可以用于联合类型、交叉类型等
type ID = string | number;
```
