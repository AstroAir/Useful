# C++20：综合中文教程

## 介绍

C++20 代表了 C++ 编程语言的重大演进，引入了众多新特性和改进，增强了语言的表达能力和效率。本教程详细探讨了 C++20 的关键特性，提供了使用方法、优势和实现细节的深入见解。无论您是希望更新技能的资深 C++ 开发者，还是对现代 C++ 感兴趣的初学者，本指南都将作为您掌握 C++20 的综合资源。

[English](cpp20.md) | **中文**

## 核心语言特性

### 概念（Concepts）

C++20 中的概念代表了编写模板的革命性方法。它们允许您定义模板参数的约束，提高代码的可读性和可维护性。概念的主要目标是建模语义类别（如 Number、Range、RegularFunction），而不仅仅是语法限制（HasPlus、Array）。

#### 基本用法

概念使您能够指定在特定上下文中使用类型所需的操作。例如，如果您想编写一个要求其参数支持加法的函数，可以使用 `std::addable` 概念。

```cpp
#include <concepts>

template<std::addable T>
T add(T a, T b) {
    return a + b;
}

// 使用示例
int main() {
    auto result1 = add(5, 3);        // 整数加法
    auto result2 = add(2.5, 1.7);    // 浮点数加法
    auto result3 = add(std::string("Hello"), std::string(" World")); // 字符串连接
    return 0;
}
```

在概念出现之前，实现类似的类型检查需要复杂的 SFINAE（替换失败不是错误）技术，使代码更难阅读和维护。

#### 标准库概念

C++20 在标准库中引入了一组预定义概念，可用于约束模板参数：

- `std::equality_comparable` - 可以进行相等比较的类型
- `std::default_initializable` - 可以默认初始化的类型
- `std::constructible_from` - 可以从特定参数构造的类型
- `std::regular` - 可相等比较、可交换、可复制/移动的类型

```cpp
#include <concepts>

template<std::regular T>
class Container {
    T data;
public:
    Container() = default;
    Container(const T& value) : data(value) {}
    
    bool operator==(const Container& other) const {
        return data == other.data;
    }
};
```

### 模块（Modules）

C++20 中的模块为传统头文件提供了现代替代方案，解决了许多限制并改善了编译时间和代码组织。

#### 基本用法

模块是可以被其他翻译单元导入的声明和定义的集合。要创建模块，您在源文件中定义它并指定其导出：

```cpp
// mymodule.cppm
export module MyModule;

export int add(int a, int b) {
    return a + b;
}

export class Calculator {
public:
    int multiply(int a, int b) {
        return a * b;
    }
};

// 私有实现（不导出）
int internal_helper() {
    return 42;
}
```

要使用模块，您需要导入它：

```cpp
// main.cpp
import MyModule;

int main() {
    int result = add(5, 3);
    Calculator calc;
    int product = calc.multiply(4, 6);
    return 0;
}
```

#### 模块的优势

- **更快的编译**：避免重复解析头文件
- **更好的封装**：只导出需要的符号
- **避免宏污染**：模块不会泄露宏定义
- **更清晰的依赖关系**：明确的导入声明

### 协程（Coroutines）

协程是 C++20 中最令人兴奋的特性之一，它们允许函数暂停和恢复执行，使异步编程变得更加直观。

#### 基本概念

协程是可以暂停执行并稍后恢复的函数。它们使用三个新关键字：
- `co_await` - 暂停执行直到操作完成
- `co_yield` - 暂停执行并返回一个值
- `co_return` - 完成协程并返回一个值

```cpp
#include <coroutine>
#include <iostream>

// 简单的生成器协程
struct Generator {
    struct promise_type {
        int current_value;
        
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        void unhandled_exception() {}
        
        std::suspend_always yield_value(int value) {
            current_value = value;
            return {};
        }
    };
    
    std::coroutine_handle<promise_type> h;
    
    Generator(std::coroutine_handle<promise_type> handle) : h(handle) {}
    ~Generator() { if (h) h.destroy(); }
    
    bool next() {
        h.resume();
        return !h.done();
    }
    
    int value() {
        return h.promise().current_value;
    }
};

Generator fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        auto temp = a;
        a = b;
        b = temp + b;
    }
}

int main() {
    auto fib = fibonacci();
    for (int i = 0; i < 10; ++i) {
        fib.next();
        std::cout << fib.value() << " ";
    }
    return 0;
}
```

### 范围（Ranges）

范围库为处理元素序列提供了一种更现代、更组合的方法。它建立在迭代器概念之上，但提供了更高级的抽象。

#### 基本用法

```cpp
#include <ranges>
#include <vector>
#include <iostream>
#include <algorithm>

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    // 传统方法
    std::vector<int> even_squares_old;
    for (int n : numbers) {
        if (n % 2 == 0) {
            even_squares_old.push_back(n * n);
        }
    }
    
    // 使用范围的现代方法
    auto even_squares = numbers 
        | std::views::filter([](int n) { return n % 2 == 0; })
        | std::views::transform([](int n) { return n * n; });
    
    for (int square : even_squares) {
        std::cout << square << " ";
    }
    
    return 0;
}
```

#### 范围适配器

范围库提供了许多有用的适配器：

- `std::views::filter` - 过滤元素
- `std::views::transform` - 转换元素
- `std::views::take` - 取前 N 个元素
- `std::views::drop` - 跳过前 N 个元素
- `std::views::reverse` - 反转序列

### 三路比较（Spaceship Operator）

三路比较操作符 `<=>` 简化了比较操作的实现，自动生成所有六个比较操作符。

#### 基本用法

```cpp
#include <compare>

class Point {
    int x, y;
    
public:
    Point(int x, int y) : x(x), y(y) {}
    
    // 只需定义一个操作符
    auto operator<=>(const Point& other) const = default;
    
    // 相等比较通常也需要显式定义
    bool operator==(const Point& other) const = default;
};

int main() {
    Point p1(1, 2);
    Point p2(3, 4);
    
    // 所有这些操作符都自动可用
    bool less = p1 < p2;
    bool greater = p1 > p2;
    bool less_equal = p1 <= p2;
    bool greater_equal = p1 >= p2;
    bool equal = p1 == p2;
    bool not_equal = p1 != p2;
    
    return 0;
}
```

### 指定初始化器（Designated Initializers）

指定初始化器允许您按名称初始化结构体成员，提高代码的可读性。

```cpp
struct Config {
    int width = 800;
    int height = 600;
    bool fullscreen = false;
    std::string title = "Default";
};

int main() {
    // 使用指定初始化器
    Config config {
        .width = 1920,
        .height = 1080,
        .fullscreen = true,
        .title = "My Game"
    };
    
    return 0;
}
```

## 标准库改进

### 新的实用程序

#### std::span

`std::span` 提供了对连续内存序列的非拥有视图：

```cpp
#include <span>
#include <vector>
#include <array>

void process_data(std::span<const int> data) {
    for (int value : data) {
        // 处理数据
    }
}

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5};
    std::array<int, 3> arr = {6, 7, 8};
    int c_array[] = {9, 10, 11};
    
    // 所有这些都可以传递给同一个函数
    process_data(vec);
    process_data(arr);
    process_data(c_array);
    
    return 0;
}
```

#### std::format

新的格式化库提供了类型安全的字符串格式化：

```cpp
#include <format>
#include <iostream>

int main() {
    std::string name = "Alice";
    int age = 30;
    double height = 1.75;
    
    std::string message = std::format(
        "姓名：{}，年龄：{}，身高：{:.2f}米", 
        name, age, height
    );
    
    std::cout << message << std::endl;
    return 0;
}
```

## 最佳实践

### 何时使用概念

- 在编写泛型代码时使用概念来约束模板参数
- 优先使用标准库概念而不是自定义概念
- 使用概念来改善错误消息的可读性

### 模块迁移策略

- 逐步将头文件转换为模块
- 从叶子依赖开始迁移
- 保持向后兼容性直到完全迁移

### 协程使用指南

- 对于异步 I/O 操作使用协程
- 实现生成器和迭代器
- 避免在性能关键的同步代码中使用协程

### 范围编程

- 使用范围视图进行数据转换管道
- 组合多个视图以创建复杂的数据处理链
- 利用惰性求值提高性能

C++20 带来了现代 C++ 编程的新时代，这些特性使代码更加表达性强、安全且高效。掌握这些特性将显著提升您的 C++ 编程能力。

---

**语言版本：**
- [English](cpp20.md) - 英文版本
- **中文** - 当前页面
