# C 语言格式修饰符详细指南

格式修饰符是 C 语言中用于指定输入输出格式的特殊字符序列。它们在 printf 和 scanf 函数中广泛使用,用于控制数据的显示和读取方式。本指南将详细介绍这些修饰符在 printf 和 scanf 中的用法。

## 目录

1. [基本格式修饰符](#基本格式修饰符)
2. [printf 中的格式修饰符](#printf中的格式修饰符)
3. [scanf 中的格式修饰符](#scanf中的格式修饰符)
4. [标志、宽度、精度和长度修饰符](#标志宽度精度和长度修饰符)
5. [示例和最佳实践](#示例和最佳实践)

## 基本格式修饰符

最常用的基本格式修饰符包括：

- `%d`: 整数
- `%f`: 浮点数
- `%c`: 字符
- `%s`: 字符串
- `%p`: 指针

这些修饰符在 printf 和 scanf 中的基本用法是相同的,但在细节上有所不同。

## printf 中的格式修饰符

printf 函数使用格式修饰符来控制输出的格式。以下是详细说明：

### 1. 整数类型

- `%d`, `%i`: 有符号十进制整数
- `%u`: 无符号十进制整数
- `%o`: 无符号八进制整数
- `%x`, `%X`: 无符号十六进制整数（小写/大写）

示例:

```c
int num = 42;
printf("%d\n", num);  // 输出: 42
printf("%x\n", num);  // 输出: 2a
```

### 2. 浮点类型

- `%f`: 十进制浮点数
- `%e`, `%E`: 科学记数法（小写/大写）
- `%g`, `%G`: 根据值的大小自动选择 %f 或 %e

示例:

```c
double pi = 3.14159;
printf("%f\n", pi);    // 输出: 3.141590
printf("%.2f\n", pi);  // 输出: 3.14
printf("%e\n", pi);    // 输出: 3.141590e+00
```

### 3. 字符和字符串

- `%c`: 单个字符
- `%s`: 字符串

示例:

```c
char ch = 'A';
char str[] = "Hello";
printf("%c\n", ch);   // 输出: A
printf("%s\n", str);  // 输出: Hello
```

### 4. 指针

- `%p`: 指针地址

示例:

```c
int *ptr = &num;
printf("%p\n", (void *)ptr);  // 输出: 地址值（如 0x7ffd5e7e9e44）
```

## scanf 中的格式修饰符

scanf 函数使用格式修饰符来控制输入的解析。以下是详细说明：

### 1. 整数类型

- `%d`, `%i`: 有符号十进制整数
- `%u`: 无符号十进制整数
- `%o`: 无符号八进制整数
- `%x`, `%X`: 无符号十六进制整数

示例:

```c
int num;
scanf("%d", &num);  // 用户输入整数
```

### 2. 浮点类型

- `%f`, `%e`, `%E`, `%g`, `%G`: 浮点数（所有这些在 scanf 中等效）

示例:

```c
float f;
scanf("%f", &f);  // 用户输入浮点数
```

### 3. 字符和字符串

- `%c`: 单个字符
- `%s`: 字符串（注意缓冲区溢出风险）

示例:

```c
char ch;
char str[50];
scanf(" %c", &ch);  // 注意前面的空格，用于跳过之前可能的换行符
scanf("%49s", str); // 限制输入长度以防止缓冲区溢出
```

### 4. 特殊用法

- `%*`: 跳过输入项

示例:

```c
int a, b;
scanf("%d%*c%d", &a, &b);  // 跳过两个数字之间的字符
```

## 标志、宽度、精度和长度修饰符

格式修饰符可以包含额外的控制字符：

### 1. 标志（仅用于 printf）

- `-`: 左对齐
- `+`: 显示正号
- `空格`: 正数前加空格
- `0`: 用 0 填充

### 2. 宽度

- 数字: 最小字段宽度
- `*`: 宽度作为参数传递

### 3. 精度

- `.数字`: 小数点后的位数
- `.*`: 精度作为参数传递

### 4. 长度修饰符

- `h`: short int 或 unsigned short int
- `l`: long int 或 unsigned long int
- `ll`: long long int 或 unsigned long long int
- `L`: long double

示例:

```c
printf("%+10.2f\n", 3.14159);  // 输出:     +3.14
printf("%.*f\n", 3, 3.14159);  // 输出: 3.142
```

## 示例和最佳实践

1. 使用 printf 格式化输出:

```c
int age = 30;
float height = 175.5;
printf("Age: %d, Height: %.1f cm\n", age, height);
// 输出: Age: 30, Height: 175.5 cm
```

2. 使用 scanf 安全地读取输入:

```c
char name[50];
int age;
printf("Enter name and age: ");
scanf("%49s %d", name, &age);
printf("Name: %s, Age: %d\n", name, age);
```

3. 使用标志和宽度控制输出格式:

````c
printf("%-10s|%10s\n", "Name", "Score");
printf("%-10s|%10.2f\n", "Alice", 92.5);
printf("%-10s|%10.2f\n", "Bob", 87.3);
// 输出:
// Name      |     Score
// Alice     |     92.50
// Bob       |     87

[前面的内容保持不变，我们从"示例和最佳实践"部分继续]

4. 使用精度控制浮点数输出:

```c
double pi = 3.14159265359;
printf("默认精度: %f\n", pi);
printf("保留2位小数: %.2f\n", pi);
printf("保留6位小数: %.6f\n", pi);

// 输出:
// 默认精度: 3.141593
// 保留2位小数: 3.14
// 保留6位小数: 3.141593
````

5. 使用 \* 动态指定宽度和精度:

```c
int width = 10;
int precision = 2;
double value = 123.456789;

printf("%*.*f\n", width, precision, value);
// 输出:    123.46
```

6. 在 scanf 中使用字段宽度限制输入:

```c
char name[10];
printf("输入您的名字 (最多9个字符): ");
scanf("%9s", name);
printf("您好, %s!\n", name);
```

## 高级用法

### 1. 处理 long long int 类型

```c
long long int big_number = 1234567890123456789LL;
printf("%lld\n", big_number);
```

### 2. 使用 %n 获取已打印的字符数

```c
int chars_printed;
printf("Hello, World!%n\n", &chars_printed);
printf("打印的字符数: %d\n", chars_printed);
// 输出:
// Hello, World!
// 打印的字符数: 13
```

### 3. 打印百分号

```c
printf("这里有一个百分号: %%\n");
// 输出: 这里有一个百分号: %
```

## 常见陷阱和注意事项

1. 格式修饰符不匹配

错误示例:

```c
int num = 42;
printf("%f\n", num);  // 错误：用 %f 打印整数
```

正确示例:

```c
printf("%d\n", num);
```

2. 缓冲区溢出风险

风险示例:

```c
char buffer[10];
scanf("%s", buffer);  // 危险：没有限制输入长度
```

安全示例:

```c
scanf("%9s", buffer);  // 限制输入最多9个字符（留1个给结束符'\0'）
```

3. 忽略 scanf 的返回值

错误示例:

```c
int age;
scanf("%d", &age);  // 没有检查输入是否成功
```

正确示例:

```c
if (scanf("%d", &age) != 1) {
    printf("输入错误\n");
    // 错误处理...
}
```

## 错误处理和安全性

1. 使用 sscanf 进行安全的字符串解析:

```c
char input[] = "42 3.14";
int num;
float fnum;

if (sscanf(input, "%d %f", &num, &fnum) == 2) {
    printf("成功读取: %d 和 %f\n", num, fnum);
} else {
    printf("输入格式错误\n");
}
```

2. 使用 fgets 和 sscanf 组合来安全读取输入:

```c
char input[100];
int age;

printf("请输入您的年龄: ");
if (fgets(input, sizeof(input), stdin) != NULL) {
    if (sscanf(input, "%d", &age) == 1) {
        printf("您的年龄是: %d\n", age);
    } else {
        printf("输入无效\n");
    }
}
```

3. 处理整数溢出:

```c
#include <limits.h>

long long input;
printf("输入一个整数: ");
if (scanf("%lld", &input) == 1) {
    if (input > INT_MAX || input < INT_MIN) {
        printf("输入值超出int范围\n");
    } else {
        int safe_int = (int)input;
        printf("有效的int值: %d\n", safe_int);
    }
} else {
    printf("输入无效\n");
}
```

## 性能考虑

1. printf vs puts:
   对于简单的字符串输出，puts 通常比 printf 更快。

```c
puts("Hello, World!");  // 通常比 printf("Hello, World!\n"); 更快
```

2. 格式化字符串的重用:
   如果需要多次使用相同的格式，将其存储为常量可以提高性能。

```c
const char *format = "Name: %s, Age: %d\n";
printf(format, "Alice", 30);
printf(format, "Bob", 25);
```

## 结论

掌握 C 语言中的格式修饰符对于编写清晰、正确和高效的代码至关重要。通过正确使用这些修饰符，您可以精确控制程序的输入和输出，提高代码的可读性和健壮性。记住要始终考虑安全性，特别是在处理用户输入时。随着经验的积累，相信你一定能编写出更高质量的 C 程序。
