# `decltype` 详解

`decltype` 是 C++11 引入的关键字，用于在编译期推导表达式的类型。它是类型推导的重要工具，与 `auto` 相比，`decltype` 可以更精确地获取表达式的具体类型，并且不强制对表达式进行求值。它在泛型编程、模板元编程和类型萃取中非常有用。

## 基本用法

```cpp
int x = 10;
decltype(x) y = 20;  // y 的类型是 int
```

在这里，`decltype(x)` 推导出 `x` 的类型为 `int`，因此 `y` 也是 `int` 类型。

## 规则和行为

### 1. 非引用类型推导

如果表达式是一个变量或函数返回值，`decltype` 会返回它的基础类型（包括 `const` 修饰）。

```cpp
const int a = 5;
decltype(a) b = 10;  // b 的类型是 const int
```

### 引用类型推导

如果表达式是左值，`decltype` 会推导为左值引用类型。

```cpp
int x = 5;
decltype((x)) y = x;  // y 的类型是 int&（左值引用）
y = 10;
std::cout << x;  // 输出：10
```

注意：`decltype((x))` 返回的是 `int&`，因为 `(x)` 是左值。

### 右值推导

如果表达式是右值，`decltype` 返回的是该类型本身，而不是引用。

```cpp
int x = 5;
decltype(x + 1) y = 6;  // y 的类型是 int
```

## `decltype` 与 `auto` 的区别

### 1. `auto`

`auto` 关键字用于根据初始化表达式自动推导变量的类型，但它忽略 `const` 和引用。

```cpp
int x = 5;
auto y = x;  // y 的类型是 int
x = 10;
y = 15;
std::cout << x << " " << y;  // 输出：10 15
```

### `decltype`

`decltype` 不会忽略表达式中的 `const` 和引用，因此更精确。

```cpp
int x = 5;
decltype(x) y = x;  // y 的类型是 int
decltype((x)) z = x;  // z 的类型是 int&（左值引用）

y = 15;
z = 20;
std::cout << x << " " << y;  // 输出：20 15
```

因此，`auto` 偏向于推导出基本类型，而 `decltype` 会保留引用和 `const` 修饰符，因此更加精确。

## 模板编程

```cpp
#include <utility>  // std::declval

template <typename T>
auto get_member_type() -> decltype(std::declval<T>().member) {
    // 返回某个类的成员类型
}
```

在这里，即使没有对象实例，`std::declval` 也能生成一个类型的右值引用，让 `decltype` 能推导成员的类型。

## 示例

### 模板返回类型推导

在模板函数中，`decltype` 可以根据函数体的表达式推导返回类型。

```cpp
template <typename T1, typename T2>
auto multiply(T1 a, T2 b) -> decltype(a * b) {
    return a * b;
}
```

### 泛型 Lambda 表达式

在 C++14 及以上，结合泛型 Lambda 和 `decltype` 可以实现更加灵活的代码。

```cpp
auto lambda = [](auto a, auto b) -> decltype(a + b) {
    return a + b;
};

std::cout << lambda(1, 2.5) << std::endl;  // 输出：3.5
```

### 类型萃取与 SFINAE

`decltype` 与 `std::enable_if` 结合，可以实现模板的条件编译。

```cpp
#include <type_traits>

template <typename T>
auto print_if_integer(T value) -> typename std::enable_if_v<std::is_integral<T>::value, void> {
    std::cout << "Integer: " << value << std::endl;
}

int main() {
    print_if_integer(42);  // 输出：Integer: 42
    // print_if_integer(3.14);  // 编译错误：double 不是整数
}
```
