# `std::declval` 在 C++ 中的应用

`std::declval` 是 C++ 标准库中的一个工具函数模板，定义在头文件 `<utility>` 中。它是一个编译期工具，用于在不实际构造对象的情况下获取对象类型的右值引用。其主要用途是在模板编程中，推断出特定类型的右值引用，而无需关心该类型是否有构造函数，或者该类型是否可以被实例化。

## 作用

`std::declval` 允许你“伪造”一个类型的右值引用，即使你没有办法实际创建该类型的对象。这对于需要在编译期推断类型、检查类型特性或者函数重载解析时特别有用。

- **编译期推断**：利用 `std::declval`，可以在编译时确定类型而不需要实例化对象。
- **SFINAE**：`std::declval` 常用于 SFINAE（Substitution Failure Is Not An Error）技巧中，通过尝试推断某个函数调用是否有效，来决定模板的特化或重载。

因为 `std::declval` 本身不会产生实际的值，仅仅是提供类型信息，所以它只能用于 `decltype` 这样的上下文中，而不能被用于运行时的实际代码。

## 语法

```cpp
template<class T>
typename std::add_rvalue_reference<T>::type declval() noexcept;
```

`std::declval<T>()` 返回类型 `T&&`，即类型 `T` 的右值引用。

## 典型用法

### 推断表达式的返回类型

如果你有一个函数 `f()`，你不知道它的返回类型，但想要推断它的返回类型而不实际调用它，可以使用 `decltype(std::declval<Foo>().f())` 这样的表达式。

### 示例

#### 推断函数返回值类型

```cpp
#include <iostream>
#include <utility>

struct Foo {
    int getValue() { return 42; }
};

template<typename T>
auto getReturnType() -> decltype(std::declval<T>().getValue()) {
    // 这个函数不会被实际调用，但可以用于推断返回类型
}

int main() {
    // 通过 decltype 推断 Foo::getValue 的返回类型
    decltype(getReturnType<Foo>()) result = 42;
    std::cout << result << std::endl;  // 输出 42
}
```

在这个例子中，`std::declval<T>().getValue()` 被用来推断 `T` 类型中 `getValue()` 函数的返回类型。

#### 无法实例化类型时的使用

```cpp
#include <iostream>
#include <utility>

struct NoDefaultConstructor {
    NoDefaultConstructor(int) {}
    int getValue() const { return 100; }
};

template<typename T>
auto test() -> decltype(std::declval<T>().getValue()) {
    // 这里我们不能实例化 NoDefaultConstructor，但可以推断它的成员函数 getValue 的类型
}

int main() {
    // 推断出 NoDefaultConstructor::getValue 的返回类型为 int
    decltype(test<NoDefaultConstructor>()) value = 100;
    std::cout << value << std::endl;  // 输出 100
}
```

### SFINAE

`std::declval` 也经常用于 SFINAE 技术中，帮助编译器在某些类型和表达式合法时选择特定的模板版本。

#### 类型特征检查

```cpp
#include <type_traits>
#include <iostream>
#include <utility>

template<typename T>
auto has_toString(int) -> decltype(std::declval<T>().toString(), std::true_type());

template<typename>
std::false_type has_toString(...);

struct A {
    void toString() const { }
};

struct B { };

int main() {
    std::cout << std::boolalpha;
    std::cout << "A has toString: " << decltype(has_toString<A>(0))::value << std::endl; // 输出 true
    std::cout << "B has toString: " << decltype(has_toString<B>(0))::value << std::endl; // 输出 false
}
```
