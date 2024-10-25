# `std::variant`

`std::variant` 是 C++17 标准库中引入的一种类型，它是一种类型安全的联合体（union），可以保存多种不同类型的值，但在任何时候只能持有其中一种类型。它提供了类似于类型擦除的能力，并能够更安全地处理多态和变体类型。

## 基本概念

### 定义

`std::variant` 是一种模板类，允许程序员在定义时指定多个类型。在实例化后，可以像使用普通对象一样使用 `std::variant`，并在运行时存储这些指定类型之一的值。

### 使用场景

- 当函数可能返回多种类型的结果时。
- 在需要存储不同类型而不使用虚继承或 `void*` 指针的场合。
- 处理不同类型输入的情况下，提高安全性和可维护性。

## 基本用法

```cpp
#include <iostream>
#include <variant>
#include <string>

int main() {
    std::variant<int, double, std::string> v; // v 可以存储 int、double 或 std::string

    v = 42; // 存储 int
    std::cout << std::get<int>(v) << std::endl; // 输出：42

    v = 3.14; // 存储 double
    std::cout << std::get<double>(v) << std::endl; // 输出：3.14

    v = "Hello Variant"; // 存储 string
    std::cout << std::get<std::string>(v) << std::endl; // 输出：Hello Variant

    return 0;
}
```

当访问 `std::variant` 中的值时，可以使用 `std::get` 函数、`std::get_if` 或者访问访式来提取存储的值。

```cpp
#include <iostream>
#include <variant>

std::variant<int, double, std::string> v;

// 存储一个 int
v = 10;

// 使用 std::get 来访问
try {
    int value = std::get<int>(v); // 成功
    std::cout << "Integer value: " << value << std::endl;

    // 试图访问不相关的类型，将抛出异常
    double d = std::get<double>(v); // 这个会抛出 std::bad_variant_access 异常
} catch (const std::bad_variant_access& e) {
    std::cout << "Caught exception: " << e.what() << std::endl;
}

// 使用 std::get_if
if (auto str_ptr = std::get_if<std::string>(&v)) {
    std::cout << "String value: " << *str_ptr << std::endl;
} else {
    std::cout << "Variant does not hold a string." << std::endl;
}
```

当尝试以不匹配的类型访问值时，抛出 `std::bad_variant_access` 异常，因此能够确保安全性。`std::get_if` 可以返回指向存储在 `std::variant` 中类型的指针，如果类型不匹配，则返回 `nullptr`。

### 2.3. 访问持有的类型

当我们需要根据持有的类型进行不同操作时，可以使用 `std::visit`，这是方式之一来安全地访问 `std::variant` 中的值。

```cpp
#include <iostream>
#include <variant>

void visitor_function(const std::variant<int, double, std::string>& v) {
    std::visit([](auto&& arg) {
        std::cout << "The value is: " << arg << std::endl;
    }, v);
}

int main() {
    std::variant<int, double, std::string> v = "Hello, Visitor!";
    visitor_function(v); // 输出：The value is: Hello, Visitor!

    return 0;
}
```
