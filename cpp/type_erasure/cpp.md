# C++ 类型擦除

## 基本概念

### 什么是类型擦除

类型擦除是一种设计模式，用于实现一个通用接口而隐藏具体数据类型的信息。在类型擦除的机制下，客户端代码不需要关心对象的具体类型，只需要使用抽象接口即可。这样，代码提高了灵活性和可复用性。

### 类型擦除的优势

- **增强灵活性**：同一段代码能够处理多种不同的类型。
- **简化 API 设计**：为用户提供一致的接口，隐藏复杂的实现细节。
- **避免代码重复**：减少由于多个相似类型实现同样接口而导致的代码冗余。

## 类型擦除的实现

### 使用基类和虚函数

```cpp
goto cpp_virtual_table.md
```

### `std::variant`

```cpp
goto variant.md
```

### `std::any`

C++17 引入了 `std::any` 类，允许存储任意类型的对象，并提供类型擦除机制。`std::any` 是一种类型安全的容器，可以在运行时动态存储和访问不同类型的值。

```cpp
#include <iostream>
#include <any>
#include <vector>

void processAny(const std::any& value) {
    if (value.type() == typeid(int)) {
        std::cout << "Processing int: " << std::any_cast<int>(value) << std::endl;
    } else if (value.type() == typeid(double)) {
        std::cout << "Processing double: " << std::any_cast<double>(value) << std::endl;
    } else if (value.type() == typeid(std::string)) {
        std::cout << "Processing string: " << std::any_cast<std::string>(value) << std::endl;
    }
}

int main() {
    std::vector<std::any> values;
    values.push_back(10);
    values.push_back(3.14);
    values.push_back(std::string("Hello"));

    for (const auto& value : values) {
        processAny(value); 
    }

    return 0;
}
```

使用 `std::any` 可以存储任意类型的值，提供了动态类型存储的能力。可以通过 `std::any_cast` 进行类型安全的装箱与取出。

### `std::function`

`std::function` 是一个通用的类型擦除机制，用于存储可调用对象（如函数指针、lambda 表达式、绑定表达式等）。它允许使用一种统一的接口来调用不同签名的函数或可调用类型。

```cpp
#include <iostream>
#include <functional>
#include <vector>

void printInt(int value) {
    std::cout << "Integer: " << value << std::endl;
}

void printDouble(double value) {
    std::cout << "Double: " << value << std::endl;
}

int main() {
    std::vector<std::function<void()>> functions;

    // 使用 std::function 将不同类型的函数存储在同一容器中
    functions.push_back([] { printInt(10); });  // Lambda capturing int
    functions.push_back([] { printDouble(2.5); }); // Lambda capturing double

    // 调用所有的函数
    for (const auto& func : functions) {
        func(); // 输出 Integer: 10\n Double: 2.5
    }

    return 0;
}
```

### 模板与 CRTP

```cpp
goto crtp.md
```
