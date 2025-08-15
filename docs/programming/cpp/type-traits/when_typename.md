# 什么时候模板前必须加 `typename`

在 C++ 中，`typename` 和 `class` 关键字用于声明模板参数。然而，某些特定情况下，必须在模板表达式前加上 `typename`，以告知编译器某个符号是一个类型而非成员或变量。这是因为 C++ 编译器有时无法确定模板中嵌套依赖类型的上下文，可能将其误判为非类型成员。本文将详细介绍 `typename` 关键字的使用场景，特别是模板前加 `typename` 的必要性。

## 必须使用 `typename` 的场景

### 嵌套依赖类型的声明

当嵌套类型依赖于模板参数时（即类型名依赖于另一个模板参数），需要在使用时加上 `typename`。

```cpp
template <typename T>
void foo() {
    typename T::type value;  // 告诉编译器 T::type 是一个类型
}
```

```cpp
template <typename T>
void foo() {
    T::type value;  // 错误：编译器无法确定 T::type 是类型还是变量
}
```

编译器会报错，因为它无法确定 `T::type` 是类型还是成员变量。

### 嵌套模板的类型成员

当模板类的嵌套类型成员本身也依赖于模板参数时，也必须使用 `typename`。

```cpp
template <typename T>
struct Outer {
    using Inner = typename T::type;  // 必须使用 typename
};
```

### 类型别名或 `using` 语句中的类型

在模板中声明类型别名时，也需要在模板依赖的类型前加上 `typename`。

```cpp
template <typename T>
using InnerType = typename T::type;  // 必须加 typename
```

### 当类型出现在 `decltype` 中

在 `decltype` 中使用模板类型推导时，如果该类型是模板参数的嵌套类型，仍需加上 `typename`。

```cpp
template <typename T>
auto get_type() -> typename T::type {
    return typename T::type{};
}
```

### 5. 在模板中的返回类型推导

如果返回类型是嵌套类型的成员，需要在模板中显式地使用 `typename`。

```cpp
template <typename T>
typename T::type func() {
    return typename T::type{};
}
```

## 何时不需要 `typename`

### 非依赖类型

当类型不依赖于模板参数时，不需要使用 `typename`。

```cpp
struct Foo {
    using type = int;
};

Foo::type a;  // 不需要 typename，因为 Foo 是已知类型
```
