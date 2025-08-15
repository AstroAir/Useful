# C++ 类型转换 (Cast) 详解

C++ 提供了四种类型转换操作符，也称为 `cast`，分别是 `static_cast`、`dynamic_cast`、`const_cast` 和 `reinterpret_cast`。它们各自有不同的用途和限制，在 C++ 编程中扮演着重要的角色。

---

## 1. `static_cast`

### 1.1 简介

`static_cast` 用于执行编译时的类型转换。它主要用于以下几种情况：

- 基本数据类型之间的转换：例如 `int` 到 `float`，`float` 到 `int` 等
- 具有继承关系的类型之间的转换：
  - 向上转型（将派生类指针或引用转换为基类指针或引用）
  - 向下转型（将基类指针或引用转换为派生类指针或引用）。但是，向下转型是不安全的
- `void*` 与其他类型指针之间的转换
- 类中定义的类型转换函数
- 枚举类型与整数类型之间的转换

### 1.2 使用场景及代码示例

#### 基本数据类型之间的转换

```cpp
#include <iostream>

int main() {
    int i = 10;
    float f = static_cast<float>(i); // int -> float
    std::cout << "float f = " << f << std::endl;

    float pi = 3.14159;
    int truncated_pi = static_cast<int>(pi); // float -> int (截断)
    std::cout << "int truncated_pi = " << truncated_pi << std::endl;

    return 0;
}
```

#### 具有继承关系的类型之间的转换

```cpp
#include <iostream>

class Base {
public:
    virtual void print() {
        std::cout << "Base class" << std::endl;
    }
};

class Derived : public Base {
public:
    void print() override {
        std::cout << "Derived class" << std::endl;
    }
    void derived_function() {
        std::cout << "Derived class specific function" << std::endl;
    }
};

int main() {
    Base* base_ptr = new Derived(); // 向上转型（隐式）
    base_ptr->print(); // 输出 "Derived class" (虚函数)

    Derived* derived_ptr = static_cast<Derived*>(base_ptr); // 向下转型
    derived_ptr->print(); // 输出 "Derived class"
    derived_ptr->derived_function(); // 可以调用派生类特有的函数

    return 0;
}
```

> **注意**：在上面的例子中，向下转型 `static_cast<Derived*>(base_ptr)` 是安全的，因为 `base_ptr` 实际上指向一个 `Derived` 对象。但是，如果 `base_ptr` 指向一个 `Base` 对象，那么向下转型会导致未定义行为。通常，使用 `dynamic_cast` 进行安全的向下转型是更好的选择（需要 RTTI 支持）。

#### `void*` 与其他类型指针之间的转换

```cpp
#include <iostream>

int main() {
    int i = 10;
    void* void_ptr = &i; // 任何类型的指针都可以隐式转换为 void*

    int* int_ptr = static_cast<int*>(void_ptr); // void* -> int*
    std::cout << "*int_ptr = " << *int_ptr << std::endl;

    return 0;
}
```

#### 类中定义的类型转换函数

```cpp
#include <iostream>

class MyInt {
private:
    int value;
public:
    MyInt(int val) : value(val) {}
    operator int() const { // 类型转换函数：MyInt -> int
        return value;
    }
};

int main() {
    MyInt my_int(20);
    int i = static_cast<int>(my_int); // 使用类型转换函数
    std::cout << "int i = " << i << std::endl;
    return 0;
}
```

#### 枚举类型与整数类型之间的转换

```cpp
#include <iostream>

enum class Color {
    RED,
    GREEN,
    BLUE
};

int main() {
    Color c = Color::GREEN;
    int color_index = static_cast<int>(c); // 枚举类型 -> int
    std::cout << "color_index = " << color_index << std::endl;

    Color another_color = static_cast<Color>(2); // int -> 枚举类型, 需要小心，确保值在枚举范围内
    return 0;
}
```

### 1.3 注意事项

- **编译时类型检查**：`static_cast` 在编译时进行类型检查
- **不进行运行时类型检查**：可能导致未定义行为
- **安全性**：向上转型安全，向下转型不安全
- **不要用于移除 `const` 或 `volatile`**：应使用 `const_cast`
- **优于 C 风格的类型转换**：提供了更好的类型安全性和可读性

### 1.4 安全性提升方案

`static_cast` 本身并不安全，可以使用其他方法（例如 `gsl::narrow`、列表初始化或用户定义的安全转换）来实现更安全的类型转换。

---

## 2. `dynamic_cast`

### 2.1 简介

`dynamic_cast` 主要用于运行时的类型转换，特别是在继承层次结构中。它主要用于安全的向下转型（将基类指针或引用转换为派生类指针或引用）。

### 2.2 使用场景及代码示例

#### 安全的向下转型

```cpp
#include <iostream>
#include <typeinfo> // for bad_cast

class Base {
public:
    virtual void print() {
        std::cout << "Base class" << std::endl;
    }
    virtual ~Base() {} // 必须有虚析构函数才能使用 dynamic_cast
};

class Derived : public Base {
public:
    void print() override {
        std::cout << "Derived class" << std::endl;
    }
    void derived_function() {
        std::cout << "Derived class specific function" << std::endl;
    }
};

int main() {
    Base* base_ptr = new Derived(); // 向上转型（隐式）
    base_ptr->print(); // 输出 "Derived class" (虚函数)

    // 安全的向下转型：
    Derived* derived_ptr = dynamic_cast<Derived*>(base_ptr);
    if (derived_ptr) {
        derived_ptr->print(); // 输出 "Derived class"
        derived_ptr->derived_function(); // 可以调用派生类特有的函数
    } else {
        std::cout << "dynamic_cast failed: base_ptr does not point to a Derived object" << std::endl;
    }

    delete base_ptr;
    return 0;
}
```

#### 使用引用进行 `dynamic_cast`

```cpp
#include <iostream>
#include <typeinfo> // for bad_cast

class Base {
public:
    virtual void print() {
        std::cout << "Base class" << std::endl;
    }
    virtual ~Base() {}
};

class Derived : public Base {
public:
    void print() override {
        std::cout << "Derived class" << std::endl;
    }
    void derived_function() {
        std::cout << "Derived class specific function" << std::endl;
    }
};

int main() {
    Base* base_ptr = new Derived();
    Base& base_ref = *base_ptr; // 基类引用

    try {
        Derived& derived_ref = dynamic_cast<Derived&>(base_ref); // 安全的向下转型（引用）
        derived_ref.print();
        derived_ref.derived_function();
    } catch (const std::bad_cast& e) {
        std::cout << "dynamic_cast failed: " << e.what() << std::endl;
    }

    delete base_ptr;
    return 0;
}
```

### 2.3 注意事项

- **RTTI 支持**：需要运行时类型信息（RTTI）的支持
- **只能用于指针或引用**：不能用于基本数据类型之间的转换
- **必须有虚函数**：基类必须至少包含一个虚函数
- **性能开销**：比 `static_cast` 慢
- **向下转型**：主要用于安全的向下转型

### 2.4 安全性

`dynamic_cast` 在传递有效指针（包括 NULL 指针）时是安全的，但如果传递悬垂指针或垃圾值会导致未定义行为。

### 2.5 使用局限性

- 运行时开销
- RTTI 要求
- 设计问题：过度使用可能表明代码中存在其他问题

### 2.6 最佳实践

- 避免过度使用
- 使用虚函数
- 优先选择静态多态性

---

## 3. `const_cast`

### 3.1 简介

`const_cast` 主要用于移除或添加类型的 `const` 或 `volatile` 限定符。

### 3.2 使用场景及代码示例

#### 与 C API 交互

```cpp
#include <iostream>
#include <cstring>

void c_function(char* str) {
    std::cout << "C function received: " << str << std::endl;
}

int main() {
    const char* const_string = "Hello from C++";
    c_function(const_cast<char*>(const_string));
    return 0;
}
```

#### 修改非常量对象

```cpp
#include <iostream>

struct Data {
    int value;
};

void modify_data(const Data* const_data) {
    Data* mutable_data = const_cast<Data*>(const_data);
    mutable_data->value = 42;
}

int main() {
    Data data = { 10 };
    const Data* const_data = &data;
    modify_data(const_data);
    std::cout << "Data value: " << data.value << std::endl;
    return 0;
}
```

### 3.3 注意事项

- **修改 `const` 对象**：绝对禁止
- **`volatile` 对象**：也可以用于添加或移除 `volatile` 限定符
- **类型安全**：不提供类型安全检查
- **只能修改 `const/volatile`**：不能用于改变对象的类型

### 3.4 最佳实践

- 尽量避免使用
- 只在必要时使用
- 考虑替代方案

---

## 4. `reinterpret_cast`

### 4.1 简介

`reinterpret_cast` 是 C++ 中最危险的类型转换操作符，可以将一个指针或引用转换为任何其他类型的指针或引用，而不进行任何类型检查。

> **重要警告**：应该极少使用，只有在绝对必要的情况下才能使用。

### 4.2 使用场景及代码示例

#### 指针类型之间的转换

```cpp
#include <iostream>

int main() {
    int i = 10;
    int* int_ptr = &i;
    float* float_ptr = reinterpret_cast<float*>(int_ptr);
    std::cout << "*float_ptr = " << *float_ptr << std::endl; // 未定义行为！
    return 0;
}
```

#### 将指针转换为整数类型

```cpp
#include <iostream>

int main() {
    int i = 10;
    int* int_ptr = &i;
    uintptr_t ptr_address = reinterpret_cast<uintptr_t>(int_ptr);
    std::cout << "int_ptr address = " << int_ptr << std::endl;
    std::cout << "ptr_address = " << ptr_address << std::endl;
    return 0;
}
```

### 4.3 注意事项

- 不进行任何类型检查
- 可能导致未定义行为
- 仅在绝对必要时使用
- 理解内存布局
- 避免使用

### 4.4 如何规避限制

- 使用 `std::bit_cast` (C++20)
- 避免类型双关

---

## 5. 四种类型转换 `cast` 对比表格

| 特性           | `static_cast`                                                                 | `dynamic_cast`                                                                 | `const_cast`                                                                 | `reinterpret_cast`                                                     |
|----------------|-------------------------------------------------------------------------------|--------------------------------------------------------------------------------|------------------------------------------------------------------------------|------------------------------------------------------------------------|
| 类型检查       | 编译时                                                                        | 运行时（需要 RTTI 支持）                                                       | 无                                                                           | 无                                                                    |
| 安全性         | 向上转型安全，向下转型不安全                                                  | 向上转型安全，向下转型会进行运行时类型检查                                     | 相对安全                                                                     | 最不安全                                                              |
| 适用场景       | 基本类型转换、继承关系转换、`void*` 转换等                                    | 主要用于具有继承关系的类型之间的安全向下转型                                   | 移除 `const` 或 `volatile` 限定符                                           | 极少使用，用于底层编程                                                |
| 性能           | 快                                                                            | 较慢                                                                           | 很快                                                                         | 最快                                                                  |
| 是否可移植     | 高                                                                            | 中                                                                             | 高                                                                           | 低                                                                    |
| 错误处理       | 不进行运行时错误检查                                                          | 指针类型返回 `nullptr`，引用类型抛出 `std::bad_cast` 异常                      | 不进行类型检查                                                               | 不进行任何错误检查                                                    |
