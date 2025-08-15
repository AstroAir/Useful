# 类型萃取（Type Extraction）

类型萃取（Type Traits / Type Extraction）是 C++编译期元编程中的重要工具。它通过操作类型信息，在编译阶段获取和判断类型的特性，实现类型推断、转换、条件编译等功能。这类技术的主要目的是在泛型编程中根据不同类型做出编译期决策，使代码更通用、更高效。

## 核心概念

- **类型萃取（Type Extraction）**：指在编译期对类型进行检查、操作和变换，生成与类型相关的元信息。C++提供了标准库`<type_traits>`支持类型萃取。
- **编译期决策**：类型萃取技术能够帮助开发者在模板编程中，根据类型特征在编译阶段决定代码的生成路径，避免运行期检查。

## 常见萃取用法

### 判断类型特性

标准库`<type_traits>`中提供了多种工具用于检查类型的特性，比如判断某类型是否为整数、浮点数、类类型等。这些工具多以`std::is_xxx`的形式提供，返回结果为`std::true_type`或`std::false_type`，分别表示真和假。

#### 整数和浮点数检查

```cpp
static_assert(std::is_integral_v<int>, "int is an integral type");
static_assert(!std::is_floating_point_v<int>, "int is not a floating-point type");
```

#### 判断类型是否相同

```cpp
static_assert(std::is_same_v<int, int>, "Types are the same");
static_assert(!std::is_same_v<int, float>, "Types are different");
```

#### 判断是否为类类型

```cpp
struct MyClass {};
static_assert(std::is_class_v<MyClass>, "MyClass is a class type");
```

### 类型转换与修饰符操作

在模板编程中，经常需要对类型进行变换，比如去除`const`、`volatile`修饰符，或者获取某类型的基础类型。

#### 去除修饰符

```cpp
using Type = const int&;
using CleanType = std::remove_const_t<std::remove_reference_t<Type>>;
static_assert(std::is_same_v<CleanType, int>, "Type is cleaned to int");
```

#### 去除指针或引用

```cpp
using PtrType = int*;
using BaseType = std::remove_pointer_t<PtrType>;
static_assert(std::is_same_v<BaseType, int>, "Base type is int");
```

#### 转换枚举类型

```cpp
enum class Color : int { Red, Green, Blue };
using UnderlyingType = std::underlying_type_t<Color>;
static_assert(std::is_same_v<UnderlyingType, int>, "Underlying type is int");
```

### 类型选择与条件处理

类型萃取技术还可以用于模板中的条件选择和类型推断，让模板在编译期根据类型特性做出不同选择。

#### `std::conditional`：条件选择类型

根据条件在编译期选择不同类型：

```cpp
using Type = std::conditional_t<true, int, double>;
static_assert(std::is_same_v<Type, int>, "Selected type is int");
```

#### `std::enable_if`：实现 SFINAE

使用`std::enable_if`进行模板选择，只允许某些特定类型通过编译：

```cpp
template <typename T>
typename std::enable_if<std::is_integral_v<T>, T>::type
add(T a, T b) {
    return a + b;
}

int result = add(1, 2);  // 正常编译
// double result = add(1.0, 2.0);  // 编译错误
```

### 判断类型是否可用

在元编程中，有时需要判断某类型是否定义了某个成员函数或操作符。常见的做法是利用**SFINAE（Substitution Failure Is Not An Error）**和类型萃取结合，实现编译期检测。

#### 判断某类型是否支持某种操作

```cpp
template <typename T>
using has_plus_operator = decltype(std::declval<T>() + std::declval<T>());

template <typename T, typename = void>
struct has_addition : std::false_type {};

template <typename T>
struct has_addition<T, std::void_t<has_plus_operator<T>>> : std::true_type {};

static_assert(has_addition<int>, "int supports + operator");
static_assert(!has_addition<std::string>, "std::string does not support + operator");
```

## 案例

### 实现类型安全的容器

我们可以利用类型萃取判断容器中的元素类型，确保只有整数类型的容器可以进行某些操作。

```cpp
#include <vector>
#include <type_traits>

template <typename Container>
typename std::enable_if<std::is_integral<typename Container_type>>::type
process(Container& c) {
    // 只允许整数类型的容器进行处理
    for (auto& elem : c) {
        elem += 1;
    }
}

int main() {
    std::vector<int> vec = {1, 2, 3};
    process(vec);  // 正常编译

    // std::vector<double> vec2 = {1.1, 2.2};
    // process(vec2);  // 编译错误：double不是整数类型
}
```
