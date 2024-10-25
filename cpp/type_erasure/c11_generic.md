# C11“新特性”： `_Generic`

C11 标准引入了 `_Generic` 关键字，提供了一种泛型选择机制，允许根据表达式的类型在编译时选择特定的代码路径。这使得 C 语言能够在某种程度上实现类似于 C++ 中函数重载的效果，从而增强了代码的通用性和类型安全性。

## `_Generic` 的语法

```c
_Generic(expression, type1: result1, type2: result2, ...)
```

- **expression**：要匹配的表达式，它的类型决定了选中的路径。
- **type1, type2**：表示要匹配的类型。
- **result1, result2**：当 `expression` 的类型匹配 `type1` 或 `type2` 时，选择的返回值。
- 如果没有匹配到的类型且定义了 `default` 分支，则选择 `default` 分支的结果。

### 示例

```c
#include <stdio.h>

void print_int(int value) {
    printf("int: %d\n", value);
}

void print_double(double value) {
    printf("double: %f\n", value);
}

#define print(x) _Generic((x),                \
                          int: print_int,     \
                          double: print_double)(x)

int main() {
    print(42);      // 输出：int: 42
    print(3.14);    // 输出：double: 3.140000

    return 0;
}
```

`_Generic` 选择 `print_int` 或 `print_double` 函数，具体选择取决于传入的表达式的类型。

- 如果传入 `42`，匹配 `int`，调用 `print_int`。
- 如果传入 `3.14`，匹配 `double`，调用 `print_double`。

## 应用场景

### 2.1. 实现**类型安全**的泛型接口

`_Generic` 提供了一种类型安全的方式，允许不同类型的数据使用相同的接口，而不会丢失类型信息。这类似于 C++ 的函数重载。

```c
#include <stdio.h>
#include <math.h>

#define abs_generic(x) _Generic((x),      \
                                int: abs, \
                                double: fabs)(x)

int main() {
    printf("%d\n", abs_generic(-10));    // 输出：10
    printf("%f\n", abs_generic(-3.14));  // 输出：3.140000

    return 0;
}
```

### 类型安全的打印函数

C 语言没有原生的类型重载。使用 `_Generic`，我们可以为不同类型的数据定义通用的打印接口。

```c
#include <stdio.h>

#define print_value(x) _Generic((x),              \
                                int: print_int,   \
                                double: print_double, \
                                char*: print_string)(x)

void print_int(int value) {
    printf("int: %d\n", value);
}

void print_double(double value) {
    printf("double: %f\n", value);
}

void print_string(char* value) {
    printf("string: %s\n", value);
}

int main() {
    print_value(42);           // 输出：int: 42
    print_value(3.14159);     // 输出：double: 3.141590
    print_value("Hello C");    // 输出：string: Hello C

    return 0;
}
```

### `default` 分支处理未匹配类型

如果传入的类型没有显式匹配，可以通过 `default` 分支来处理。

```c
#include <stdio.h>

#define print_value(x) _Generic((x),             \
                                int: print_int,  \
                                double: print_double, \
                                default: print_unknown)(x)

void print_int(int value) {
    printf("int: %d\n", value);
}

void print_double(double value) {
    printf("double: %f\n", value);
}

void print_unknown(void* value) {
    printf("Unknown type\n");
}

int main() {
    print_value(42);         // 输出：int: 42
    print_value(3.14);      // 输出：double: 3.140000
    print_value('c');       // 输出：Unknown type

    return 0;
}
```

## 3. `_Generic` 的局限性

- **仅支持静态类型匹配**：`_Generic` 的匹配在编译期完成，因此无法处理动态类型。
- **不支持复杂类型**：`_Generic` 只能匹配基础类型，无法直接匹配数组、结构体或联合体类型。
- **代码可读性降低**：使用 `_Generic` 的代码在逻辑上会变得复杂，可能影响可维护性。
- **缺乏扩展性**：与 C++ 的模板相比，`_Generic` 的扩展能力有限。
