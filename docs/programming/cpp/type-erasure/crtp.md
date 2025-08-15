# CRTP（Curiously Recurring Template Pattern）

CRTP（Curiously Recurring Template Pattern）是一种在 C++ 中使用的编程模式，通过将派生类作为模板参数传递给基类来达到静态多态的目的。这个模式的主要特点是可以在编译期进行类型确定，并借助 C++ 的模板机制来实现直接的函数调用而无需虚函数表，从而提供高效的多态实现。

## CRTP

CRTP 的基本思想是将派生类类型作为基类的模板参数。这样，基类就可以在编译时知道派生类的类型，并通过这个信息实现类型特定的操作。

### 实现模板

```cpp
template <typename Derived>
class Base {
public:
    void interface() {
        // 在基类中可以调用派生类的函数
        static_cast<Derived*>(this)->implementation();
    }
};

class Derived : public Base<Derived> {
public:
    void implementation() {
        // 实现细节
    }
};
```

在这个示例中，`Base` 是一个模板类，接受一个模板参数 `Derived`。当我们实现 `interface()` 函数时，我们可以安全地调用派生类的 `implementation()` 函数。

## 典型用法

### 静态多态

CRTP 允许在编译期间代替运行时多态，消除了虚函数的调用开销。当派生类通过 CRTP 继承基类时，所有函数都是编译时解析的。

#### 示例

```cpp
#include <iostream>

// 定义 CRTP 基类
template <typename Derived>
class Base {
public:
    void interface() {
        static_cast<Derived*>(this)->implementation(); // 调用派生类的实现
    }
};

// 派生类 A
class DerivedA : public Base<DerivedA> {
public:
    void implementation() {
        std::cout << "DerivedA implementation" << std::endl;
    }
};

// 派生类 B
class DerivedB : public Base<DerivedB> {
public:
    void implementation() {
        std::cout << "DerivedB implementation" << std::endl;
    }
};

int main() {
    DerivedA a;
    DerivedB b;

    a.interface(); // 输出：DerivedA implementation
    b.interface(); // 输出：DerivedB implementation

    return 0;
}
```

### 静态策略模式

CRTP 可以结合策略模式，以实现不同的行为，而无需引入虚函数开销。可以在基类中定义通用接口，而在派生类中实现不同的策略。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

template <typename SortAlgorithm>
class Sorter {
public:
    void sort(std::vector<int>& data) {
        static_cast<SortAlgorithm*>(this)->sort(data);
    }
};

class BubbleSort : public Sorter<BubbleSort> {
public:
    void sort(std::vector<int>& data) {
        std::cout << "BubbleSort" << std::endl;
        for (size_t i = 0; i < data.size() - 1; i++) {
            for (size_t j = 0; j < data.size() - i - 1; j++) {
                if (data[j] > data[j + 1]) {
                    std::swap(data[j], data[j + 1]);
                }
            }
        }
    }
};

class SelectionSort : public Sorter<SelectionSort> {
public:
    void sort(std::vector<int>& data) {
        std::cout << "SelectionSort" << std::endl;
        for (size_t i = 0; i < data.size() - 1; i++) {
            size_t minIndex = i;
            for (size_t j = i + 1; j < data.size(); j++) {
                if (data[j] < data[minIndex]) {
                    minIndex = j;
                }
            }
            std::swap(data[i], data[minIndex]);
        }
    }
};

int main() {
    std::vector<int> data = {5, 3, 2, 4, 1};

    BubbleSort bubble_sort;
    bubble_sort.sort(data); // 输出「BubbleSort」

    SelectionSort selection_sort;
    selection_sort.sort(data); // 输出「SelectionSort」

    return 0;
}
```

## 优缺点

### 优点

1. **性能**：由于 CRTP 是一种编译期机制，它消除了虚函数的调用开销，因此通常会比传统的虚函数实现多态更快。
2. **类型安全**：CRTP 提供了强类型检查，避免了与 `void*` 或其他类型擦除方法相关的运行时错误。
3. **灵活性**：允许在基类中定义模板参数类型，并可使用任何类型作为参数，包含派生类本身。

### 缺点

1. **复杂性**：CRTP 可能使得代码更加复杂，特别是对于不熟悉模板编程的开发者而言，理解 CRTP 的实现细节可能较为困难。
2. **可读性**：使用 CRTP 的代码在类型推断和模板参数方面可能使得代码的可读性降低，尤其是与其他类型的混合使用时。
3. **不能在运行时多态**：CRTP 只能提供编译时多态，无法动态决定类型，限制了其使用场景。
