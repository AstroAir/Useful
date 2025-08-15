# C 语言中的类型擦除

在 C 语言中，尽管没有 C++ 中的泛型和多态机制，开发者依然可以通过一些编程技巧实现类似的类型擦除功能。类型擦除的目标是隐藏具体类型的细节，使代码能够以通用的方式处理不同的数据类型。C 语言中的类型擦除主要通过以下几种方式实现：

- `void*` 指针
- 函数指针
- 联合体（`union`）
- 结构体和虚表。

## 使用 `void*`

`void*` 是 C 语言中的一种通用指针类型，它可以指向任意类型的对象。`void*` 的特性使得开发者可以在不知道具体类型的情况下传递和存储数据，达到类型擦除的效果。使用 `void*` 时，必须在使用时手动进行类型转换。

```c
#include <stdio.h>

void print_int(void* data) {
    printf("%d\n", *(int*)data);  // 将 void* 转换为 int*
}

void print_double(void* data) {
    printf("%f\n", *(double*)data);  // 将 void* 转换为 double*
}

int main() {
    int a = 10;
    double b = 3.14;

    print_int(&a);    // 打印 int 类型
    print_double(&b); // 打印 double 类型

    return 0;
}
```

- **优点**：`void*` 允许函数接受和处理任意类型的数据，提高了代码复用性。
- **缺点**：使用 `void*` 会丧失类型安全，开发者需要小心处理类型转换，避免出现运行时错误。

## 函数指针与回调机制

C 语言中的函数指针可以实现类似面向对象编程中的多态。结合 `void*` 和函数指针，我们可以创建一个通用接口，在运行时调用不同的函数。

```c
#include <stdio.h>

typedef void (*print_func)(void*);

void print_int(void* data) {
    printf("%d\n", *(int*)data);
}

void print_double(void* data) {
    printf("%f\n", *(double*)data);
}

void print_data(void* data, print_func print) {
    print(data);
}

int main() {
    int a = 42;
    double b = 5.67;

    // 使用 print_data 实现多态调用
    print_data(&a, print_int);    // 打印 int 类型
    print_data(&b, print_double); // 打印 double 类型

    return 0;
}
```

- **优点**：通过函数指针，代码可以灵活地调用不同的函数，实现多态。
- **缺点**：函数指针的使用会使代码变得复杂，且不利于调试。

## `union`

`union`允许多个数据成员共享同一块内存，那么我们可以根据需要动态解释这块内存的内容，从而实现类型擦除。

```c
#include <stdio.h>

typedef union {
    int i;
    double d;
} Value;

void print_value(int type, Value val) {
    if (type == 0) {
        printf("int: %d\n", val.i);
    } else if (type == 1) {
        printf("double: %f\n", val.d);
    }
}

int main() {
    Value v1;
    v1.i = 42;

    Value v2;
    v2.d = 3.1415;

    print_value(0, v1); // 打印 int 类型
    print_value(1, v2); // 打印 double 类型

    return 0;
}
```

### 优缺点

- **优点**：`union` 提供了一种高效的方式存储多种类型的数据。
- **缺点**：开发者必须手动管理类型标识符，否则会导致类型解释错误。

## 4. 结构体和虚表

```cpp
goto c_virtual_table.md
```
