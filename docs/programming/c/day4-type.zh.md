
# 从零入门 C 语言：Day4 - 数据类型与数组基础

## 引入

在 C 语言编程中，理解类型系统是构建可靠程序的基石。类型系统不仅决定了数据在内存中的存储方式，还影响着程序的性能和安全性。本章将系统讲解 C 语言的类型系统、类型转换机制以及数组和字符串的使用方法，通过清晰的示例帮助你建立扎实的基础。

## 类型系统

C 语言是一种强类型语言，这意味着每个变量在使用前必须明确指定其数据类型。数据类型决定了变量可以存储的数据范围、内存占用大小以及可执行的操作。理解类型系统对编写高效、安全的 C 程序至关重要。

### 基本数据类型

#### 整型（Integer Types）

C 语言提供了多种整型，以适应不同范围的整数值需求。需要注意的是，各种整型的具体大小取决于编译器和目标平台，以下为常见实现：

- `int`：标准整型，通常占用 4 字节（32 位系统）
- `short`：短整型，通常占用 2 字节
- `long`：长整型，通常占用 4 或 8 字节
- `long long`：更长的整型，通常占用 8 字节

```c
int age = 25;                // 标准整型
short year = 2022;           // 短整型
long population = 8000000L;  // 长整型（L 后缀表示 long 类型）
long long distance = 12345678901234LL; // 更长整型（LL 后缀）
```

#### 字符型（Character Type）

`char` 类型用于存储单个字符，占用 1 字节内存。在 C 语言中，字符本质上是整数，通过 ASCII 码表与字符对应。

```c
char letter = 'A';  // 存储字符 'A'
char numChar = 65;  // 同样存储 'A'（ASCII 码 65）
```

#### 浮点型（Floating Point Types）

浮点类型用于表示带小数部分的数值：

- `float`：单精度浮点型，通常占用 4 字节
- `double`：双精度浮点型，通常占用 8 字节
- `long double`：扩展精度浮点型，通常占用 12 或 16 字节

```c
float pi = 3.14f;  // f 后缀表示 float 类型
double e = 2.718281828459045; // 默认为 double 类型
```

#### 枚举类型（Enumerated Types）

枚举类型允许为整数常量定义有意义的名称，提高代码可读性：

```c
enum Day { SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY };
enum Day today = WEDNESDAY; // today 的值为 3
```

#### void 类型

`void` 类型表示"无类型"，主要用于：

- 函数不返回值时的返回类型声明
- 指向任意类型数据的指针（`void*`）

```c
void printMessage() {
    printf("Hello, C Programming!\n");
    // 无 return 语句或 return; 表示函数执行结束
}
```

> **重要提示**：C 语言规定，不返回值的函数必须明确声明返回类型为 `void`，省略返回类型可能导致编译错误。

#### 指针类型

指针是 C 语言的核心特性之一，用于存储内存地址。指针的类型决定了它指向的数据类型：

```c
int x = 10;
int *ptr = &x;  // ptr 是指向整数的指针，存储 x 的地址
```

### 类型转换

在表达式中混合使用不同类型的数据时，C 语言提供了两种类型转换机制：

#### 隐式类型转换（自动转换）

当表达式中包含不同类型的操作数时，编译器会自动将"窄"类型转换为"宽"类型，以避免数据丢失：

```c
int a = 5;
double b = 3.2;
double result = a + b; // a 被自动转换为 double 类型
```

隐式转换遵循以下优先级规则（从低到高）：
`char` → `short` → `int` → `unsigned int` → `long` → `unsigned long` → `float` → `double` → `long double`

#### 显式类型转换（强制转换）

当需要将"宽"类型转换为"窄"类型，或进行特定类型解释时，需使用强制类型转换：

```c
double pi = 3.14159;
int truncated_pi = (int)pi; // 将 double 转换为 int，结果为 3
```

> **注意事项**：
>
> 1. 强制转换可能导致数据丢失（如浮点数转整数会截断小数部分）
> 2. 指针类型转换需格外谨慎，错误的转换可能导致未定义行为
> 3. 从大范围类型转为小范围类型时，可能产生溢出问题

### 实用示例

#### 整数与浮点数混合运算

```c
#include <stdio.h>

int main() {
    int apples = 10;
    double price = 1.5;
    double total_cost = apples * price; // apples 自动转为 double
    printf("Total cost: $%.2f\n", total_cost);
    return 0;
}
```

#### 指针类型转换

```c
#include <stdio.h>

int main() {
    int a = 42;
    void *ptr = &a;      // 通用指针可指向任何类型
    int *int_ptr = (int *)ptr; // 转换回原始类型
    printf("Value of a: %d\n", *int_ptr);
    return 0;
}
```

## 数组

当需要处理多个相同类型的数据时，数组提供了高效的解决方案。数组在内存中连续存储，支持通过索引快速访问元素。

### 一维数组

#### 定义与初始化

```c
int scores[5]; // 定义包含 5 个整数的数组

// 完全初始化
int values[5] = {85, 90, 78, 92, 88};

// 部分初始化（未指定元素自动初始化为 0）
int partial[5] = {1, 2}; // 等价于 {1, 2, 0, 0, 0}

// 自动推导大小
int autoSize[] = {10, 20, 30}; // 大小为 3
```

#### 访问元素

数组索引从 0 开始，这是初学者常犯错误的地方：

```c
int first = values[0]; // 获取第一个元素
values[2] = 85;        // 修改第三个元素
```

> **重要提示**：C 语言不检查数组边界，越界访问可能导致严重错误（如段错误）。

### 多维数组

#### 二维数组

二维数组可视为"数组的数组"，常用于表示矩阵或表格数据：

```c
// 定义 3 行 4 列的二维数组
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

// 访问元素
int element = matrix[1][2]; // 获取第 2 行第 3 列的元素（值为 7）
```

内存中，二维数组按**行优先**顺序存储：先存储第一行所有元素，再存储第二行，依此类推。

### 指针与数组的关系

在 C 语言中，数组名在大多数表达式中会被视为指向首元素的指针：

```c
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr; // p 指向 arr[0]

printf("%d\n", *(p + 2)); // 输出 3（等价于 arr[2]）
```

#### 指针数组 vs 数组指针

- **指针数组**：数组元素是指针

  ```c
  char *names[3] = {"Alice", "Bob", "Charlie"};
  ```

- **数组指针**：指向数组的指针

  ```c
  int arr[5] = {1, 2, 3, 4, 5};
  int (*p)[5] = &arr; // p 指向包含 5 个整数的数组
  ```

### 动态数组

当数组大小在运行时才能确定时，可使用动态内存分配：

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int size = 5;
    int *dynamicArr = (int *)malloc(size * sizeof(int));
    
    if (dynamicArr == NULL) {
        printf("内存分配失败！\n");
        return 1;
    }
    
    // 使用数组
    for (int i = 0; i < size; i++) {
        dynamicArr[i] = i * 2;
    }
    
    // 释放内存
    free(dynamicArr);
    return 0;
}
```

> **内存管理提示**：
>
> 1. 动态分配的内存必须手动释放（`free`）
> 2. 使用 `realloc` 可调整已分配内存的大小
> 3. 避免内存泄漏（分配后未释放）和悬空指针（释放后继续使用）

## 字符串

C 语言中，字符串是特殊的字符数组，以空字符 `\0` 结尾。

### 字符串表示

```c
char greeting[] = "Hello"; // 自动添加 \0，实际大小为 6 字节
char *message = "World";   // 指向字符串常量的指针
```

> **关键区别**：
>
> - 数组形式（`greeting`）：可在运行时修改内容
> - 指针形式（`message`）：通常指向只读内存，修改会导致未定义行为

### 常用字符串操作

标准库 `<string.h>` 提供了丰富的字符串处理函数：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char src[] = "Hello";
    char dest[20];
    
    // 复制字符串
    strcpy(dest, src);
    
    // 连接字符串
    strcat(dest, ", World!");
    
    // 获取长度（不包括 \0）
    int len = strlen(dest);
    
    // 比较字符串
    int cmp = strcmp("apple", "banana");
    
    printf("Result: %s (length: %d)\n", dest, len);
    printf("Comparison result: %d\n", cmp);
    
    return 0;
}
```

### 字符串操作注意事项

1. **缓冲区溢出**：确保目标数组足够大

   ```c
   char small[5];
   strcpy(small, "Hello"); // 危险！会导致缓冲区溢出
   ```

2. **空字符 `\0`**：必须存在才能正确标识字符串结束

3. **字符串常量**：不应尝试修改

   ```c
   char *str = "Hello";
   str[0] = 'h'; // 非法操作，可能导致程序崩溃
   ```

### 实用字符串示例

#### 字符串反转

```c
void reverseString(char str[]) {
    int length = strlen(str);
    for (int i = 0; i < length/2; i++) {
        char temp = str[i];
        str[i] = str[length - i - 1];
        str[length - i - 1] = temp;
    }
}
```

#### 回文检查

```c
int isPalindrome(char str[]) {
    int left = 0;
    int right = strlen(str) - 1;
    
    while (left < right) {
        if (str[left] != str[right]) {
            return 0;
        }
        left++;
        right--;
    }
    return 1;
}
```

## 总结与最佳实践

1. **类型选择**：根据数据范围和精度需求选择合适的数据类型
2. **类型转换**：谨慎使用强制类型转换，避免数据丢失
3. **数组使用**：
   - 始终注意数组边界，避免越界访问
   - 动态数组需手动管理内存
   - 理解指针与数组的关系
4. **字符串处理**：
   - 确保缓冲区足够大
   - 始终以 `\0` 结尾
   - 优先使用安全的字符串函数（如 `strncpy` 代替 `strcpy`）

> **编程箴言**：C 语言赋予程序员强大的控制力，但也要求更高的责任意识。理解类型系统和内存管理是编写健壮 C 程序的关键。
