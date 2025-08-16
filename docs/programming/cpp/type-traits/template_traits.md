# 模板萃取

## 模板萃取的核心概念

1. **模板参数**：模板参数可以是类型参数（如 `T`）、非类型参数（如 `int`），甚至是模板本身。

2. **模板特化与偏特化**：通过模板的偏特化，可以实现对模板参数的精细匹配和提取。

3. **SFINAE 与条件编译**：结合类型萃取和模板元编程，可以在编译期选择合适的模板实例。

4. **Concepts**：C++20 中的 Concepts 提供了更简洁的模板参数约束和匹配。

## 类模板萃取

### 类模板参数萃取

类模板的萃取常用模板偏特化来提取模板的参数类型。这种技术适用于容器类、智能指针等模板类的类型分析。

#### 提取 `std::vector` 的元素类型

```cpp
#include <iostream>
#include <vector>
#include <type_traits>

// 定义一个通用的模板类，用于提取容器元素类型
template <typename T>
struct extract_element_type;

// 偏特化：匹配 std::vector，并提取其元素类型
template <typename T>
struct extract_element_type<std::vector<T>> {
    using type = T;
};

int main() {
    using vec_type = std::vector<int>;
    using element_type = extract_element_type<vec_type>::type;

    static_assert(std::is_same_v<element_type, int>, "Element type is int");
    std::cout << "Element type extracted successfully!" << std::endl;
}
```

### 检测模板类型是否符合某条件

结合 `std::enable_if` 和模板萃取，可以实现模板参数的条件编译。例如，我们希望某个函数只接受容器类型参数。

#### 检测类型是否为容器类型

```cpp
#include <iostream>
#include <vector>
#include <type_traits>

// 通用模板：假设类型不是容器
template <typename T, typename = void>
struct is_container : std::false_type {};

// 偏特化：如果类型有 `value_type` 成员，则判断为容器类型
template <typename T>
struct is_container<T, std::void_t<typename T::value_type>> : std::true_type {};

// 使用条件编译确保函数只接受容器类型
template <typename T>
typename std::enable_if<is_container<T>::value>::type
print_size(const T& container) {
    std::cout << "Container size: " << container.size() << std::endl;
}

int main() {
    std::vector<int> vec = {1, 2, 3};
    print_size(vec);  // 输出：Container size: 3

    // int x = 42;
    // print_size(x);  // 编译错误：int 不是容器类型
}
```

**说明**：在这个例子中，我们利用模板偏特化和 `std::void_t` 检测类型是否为容器，并通过 `std::enable_if` 实现 SFINAE。

## 模板萃取与 Concepts

C++20 引入了 Concepts，使得模板参数的约束更加简洁直观。Concepts 是对模板萃取和类型匹配的进一步封装。

```cpp
#include <iostream>
#include <concepts>

template <typename T>
concept Integral = std::is_integral_v<T>;

// 只接受整数
void print(Integral auto value) {
    std::cout << "Integer: " << value << std::endl;
}

int main() {
    print(42);      // 输出：Integer: 42
    // print(3.14);  // 编译错误：3.14 不是整数类型
}
```

```cpp
#include <iostream>
#include <vector>
#include <concepts>

template <typename T>
concept Container = requires(T t) {
    typename T::value_type;
    { t.size() } -> std::convertible_to<std::size_t>;
};

void print_size(const Container auto& container) {
    std::cout << "Container size: " << container.size() << std::endl;
}

int main() {
    std::vector<int> vec = {1, 2, 3};
    print_size(vec);

    // int x = 42;
    // print_size(x);
}
```
