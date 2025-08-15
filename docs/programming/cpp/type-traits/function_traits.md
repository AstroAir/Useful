# 函数萃取

函数萃取是 C++ 元编程中的一项技术，用于在编译期分析和获取函数类型、参数类型、返回类型等特性。通过函数萃取，我们可以实现更加灵活的泛型编程，例如通过模板根据函数签名自动推导返回类型，或者判断对象是否为可调用对象。C++ 标准库也提供了一些工具来支持函数萃取，特别是 `<functional>` 和 `<type_traits>` 中的工具。

## 函数萃取的核心

1. **函数签名**：函数的完整类型描述，包括返回值类型、参数类型及其顺序。

2. **可调用对象（Callable Object）**：在 C++ 中，函数、函数指针、lambda 表达式、仿函数（functor）等都属于可调用对象。

3. **函数类型推导**：C++ 的模板元编程和 `decltype` 可以在编译期推导函数的返回值类型或参数类型，从而减少代码冗余。

函数萃取主要包括：

- 获取返回类型：推导一个函数或可调用对象的返回类型。
- 参数类型分析：检查参数类型是否符合特定要求。
- 判断对象是否为可调用对象。

## 函数萃取使用

### 推导返回值类型

#### 使用 `decltype`

`decltype` 是 C++11 引入的关键字，用于获取表达式的类型，常用于推导函数的返回类型。

```cpp
#include <iostream>

template <typename Func, typename... Args>
auto invoke(Func&& f, Args&&... args) -> decltype(f(std::forward<Args>(args)...)) {
    return f(std::forward<Args>(args)...);
}

int add(int a, int b) { return a + b; }

int main() {
    std::cout << invoke(add, 1, 2) << std::endl;  // 输出：3
}
```

#### 使用 `std::invoke_result`（C++17）

`std::invoke_result` 用于获取可调用对象调用后的返回类型。

```cpp
#include <iostream>
#include <type_traits>

int add(int a, int b) { return a + b; }

int main() {
    using result_type = std::invoke_result_t<decltype(add), int, int>;
    static_assert(std::is_same_v<result_type, int>, "Result type should be int");
}
```

### 判断对象是否为可调用对象

#### 使用 `std::is_invocable`

C++17 引入了 `std::is_invocable`，用于在编译期判断某对象是否为可调用对象，且其参数是否正确。

```cpp
#include <iostream>
#include <type_traits>

void func(int) {}

int main() {
    static_assert(std::is_invocable_v<decltype(func), int>, "Function is callable with int");
    static_assert(!std::is_invocable_v<decltype(func), double>, "Cannot call with double");
}
```

#### 使用 `std::is_invocable_r`

`std::is_invocable_r` 还可以判断返回类型是否符合预期。

```cpp
#include <type_traits>

int add(int a, int b) { return a + b; }

int main() {
    static_assert(std::is_invocable_r_v<int, decltype(add), int, int>,
                  "The function should return an int");
}
```

### 推导函数参数类型

使用 `std::tuple_element` 和 `std::tuple_size` 将函数的参数列表包装成 `std::tuple`，并使用这些工具分析参数类型。

```cpp
#include <tuple>
#include <type_traits>
#include <iostream>

template <typename T>
struct function_traits;

// 偏特化：提取函数参数类型和返回值类型
template <typename Ret, typename... Args>
struct function_traits<Ret(Args...)> {
    using return_type = Ret;
    using argument_tuple = std::tuple<Args...>;
};

int func(int, double) { return 42; }

int main() {
    using traits = function_traits<decltype(func)>;
    using first_arg_type = std::tuple_element_t<0, traits::argument_tuple>;

    static_assert(std::is_same_v<first_arg_type, int>, "First argument should be int");
}
```

### 成员函数指针的萃取

C++ 中，成员函数指针也可以通过模板进行推导和操作。

```cpp
#include <iostream>
#include <type_traits>

struct MyClass {
    void member_func(int) {}
};

template <typename T>
struct member_function_traits;

template <typename ClassType, typename Ret, typename... Args>
struct member_function_traits<Ret (ClassType::*)(Args...)> {
    using return_type = Ret;
    using class_type = ClassType;
    using argument_tuple = std::tuple<Args...>;
};

int main() {
    using traits = member_function_traits<decltype(&MyClass::member_func)>;
    static_assert(std::is_same_v<traits::return_type, void>, "Return type should be void");
}
```
