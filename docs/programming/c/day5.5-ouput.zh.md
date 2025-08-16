# 从零入门 C 语言：Day5.5 - 标准输出

## 引入

在 C 语言中，输出是将程序处理的数据发送到显示器、文件或其他外部设备的过程。与输入相对应，C 语言提供了丰富的输出函数，帮助我们向用户展示结果、记录程序状态或保存数据到文件。本章将系统介绍这些输出方法，让你能够清晰、安全地将程序结果呈现给用户或存储到外部介质。

## 标准输出函数

### `printf`：格式化输出的核心工具

`printf` 是 C 语言中最常用的输出函数，用于将格式化的数据发送到标准输出（通常是屏幕）。

```c
int printf(const char *format, ...);
```

- **format**：格式字符串，包含普通字符和格式说明符（如 `"%d"` 表示整数，`"%f"` 表示浮点数）。
- **返回值**：成功输出的字符数；若发生错误，返回负值。

**示例：**

```c
#include <stdio.h>

int main() {
    int age = 25;
    float height = 175.5;
    char initial = 'J';

    printf("姓名：张%c\n年龄：%d 岁\n身高：%.1f 厘米\n", initial, age, height);
    return 0;
}
```

**输出结果：**

```txt
姓名：张J
年龄：25 岁
身高：175.5 厘米
```

**关键特性：**

- 格式说明符与参数必须一一对应，否则会导致未定义行为。
- 支持丰富的格式控制，如 `%.2f` 控制浮点数小数位数，`%10d` 指定最小宽度等。
- 特殊字符需转义：`\n` 换行，`\t` 制表符，`%%` 输出百分号。

> **小贴士**：初学者常犯的错误是格式说明符与参数类型不匹配（如用 `%d` 输出浮点数）。建议先用简单示例练习，逐步掌握格式控制技巧。

### `fprintf`：向文件输出格式化数据

`fprintf` 与 `printf` 功能类似，但用于向文件流输出数据。

```c
int fprintf(FILE *stream, const char *format, ...);
```

- **stream**：文件指针，指定输出目标（如 `stdout` 表示屏幕，`stderr` 表示标准错误，或 `fopen` 打开的文件）。

**示例：**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("output.txt", "w");
    if (file == NULL) {
        printf("文件创建失败！\n");
        return 1;
    }

    int num = 42;
    fprintf(file, "文件中的数字：%d\n", num);  // 写入文件
    printf("数据已写入文件！\n");             // 同时在屏幕显示提示

    fclose(file);  // 务必关闭文件
    return 0;
}
```

**使用要点：**

- 文件操作前必须检查 `fopen` 是否成功。
- 文件使用完毕后，**必须调用 `fclose` 关闭**，否则可能导致数据未写入或资源泄漏。
- 可用于向标准错误流输出错误信息：`fprintf(stderr, "错误：文件不存在！\n");`

### `sprintf` 和 `snprintf`：格式化输出到字符串

这两个函数将格式化数据输出到字符串缓冲区，而非直接显示或写入文件。

```c
int sprintf(char *str, const char *format, ...);
int snprintf(char *str, size_t size, const char *format, ...);
```

- **str**：目标字符串缓冲区。
- **size**（仅 `snprintf`）：缓冲区大小，防止溢出。

**示例：**

```c
#include <stdio.h>

int main() {
    char buffer[50];
    int id = 1001;
    float score = 89.5;

    // sprintf 不检查缓冲区大小，有溢出风险
    sprintf(buffer, "学生ID：%d，成绩：%.1f", id, score);
    printf("使用 sprintf：%s\n", buffer);

    // snprintf 安全版本，指定最大写入长度
    snprintf(buffer, sizeof(buffer), "学生ID：%04d，成绩：%.1f", id, score);
    printf("使用 snprintf：%s\n", buffer);

    return 0;
}
```

**关键区别：**

- `sprintf` **不检查缓冲区大小**，可能导致缓冲区溢出，**不推荐使用**。
- `snprintf` 通过 `size` 参数限制写入长度，**始终优先使用**。
- `snprintf` 返回值表示"如果缓冲区足够大，本应写入的字符数"，可用于判断是否截断。

## 字符输出函数

### `putchar`：单字符输出

`putchar` 向标准输出写入**单个字符**。

```c
int putchar(int c);
```

- **c**：要输出的字符（作为 `int` 类型传递）。
- **返回值**：成功时返回输出的字符；失败时返回 `EOF`。

**示例：**

```c
#include <stdio.h>

int main() {
    char text[] = "Hello, C!";
    int i = 0;

    while (text[i] != '\0') {
        putchar(text[i]);  // 逐字符输出
        i++;
    }
    putchar('\n');  // 输出换行符

    return 0;
}
```

**使用场景：**

- 实现自定义输出逻辑（如加密输出、字符转换）。
- 与 `getchar` 配合实现简单的字符处理程序。

### `fputc` 和 `putc`：向文件输出单个字符

两者功能类似，用于向文件流写入单个字符。

```c
int fputc(int c, FILE *stream);
int putc(int c, FILE *stream);
```

**示例：**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("chars.txt", "w");
    if (file == NULL) {
        printf("文件创建失败！\n");
        return 1;
    }

    for (char c = 'A'; c <= 'Z'; c++) {
        fputc(c, file);  // 写入大写字母
        fputc(' ', file); // 写入空格
    }
    fputc('\n', file);   // 写入换行符

    fclose(file);
    printf("字母表已写入文件！\n");
    return 0;
}
```

**使用建议：**

- 优先使用 `fputc`，避免 `putc` 可能的副作用（宏实现可能导致参数多次求值）。
- 适合逐字符构建文件内容的场景。

## 行输出函数

### `puts`：输出字符串行

`puts` 向标准输出写入一个字符串，并**自动添加换行符**。

```c
int puts(const char *str);
```

- **str**：要输出的字符串（以 `\0` 结尾）。
- **返回值**：成功时返回非负值；失败时返回 `EOF`。

**示例：**

```c
#include <stdio.h>

int main() {
    char message[] = "欢迎学习C语言！";
    puts(message);  // 输出字符串并换行
    puts("这是第二行"); // 等价于 printf("这是第二行\n");
    return 0;
}
```

**特点：**

- 比 `printf` 更简单，但**无法格式化输出**。
- **自动添加换行符**，无需手动添加 `\n`。
- 输出成功返回非负值，失败返回 `EOF`。

### `fputs`：向文件输出字符串行

`fputs` 与 `puts` 类似，但用于向文件流输出字符串，**不会自动添加换行符**。

```c
int fputs(const char *str, FILE *stream);
```

**示例：**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("lines.txt", "w");
    if (file == NULL) {
        printf("文件创建失败！\n");
        return 1;
    }

    fputs("第一行内容\n", file);  // 需手动添加换行符
    fputs("第二行内容", file);    // 不添加换行符
    fputs("\n", file);            // 单独添加换行符

    fclose(file);
    printf("文本行已写入文件！\n");
    return 0;
}
```

**关键区别：**

- `puts` 用于标准输出，自动换行；`fputs` 用于任意流，**不自动换行**。
- `fputs` 更灵活，可控制是否添加换行符。

## 文件输出函数

### `fwrite`：二进制数据写入

`fwrite` 用于向文件写入原始数据块，适合处理二进制文件（如图片、自定义格式文件）。

```c
size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream);
```

**示例：**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("data.bin", "wb");
    if (file == NULL) {
        printf("文件创建失败！\n");
        return 1;
    }

    int numbers[] = {10, 20, 30, 40, 50};
    size_t count = fwrite(numbers, sizeof(int), 5, file);

    if (count != 5) {
        printf("写入数据不完整！\n");
    } else {
        printf("成功写入 %zu 个整数\n", count);
    }

    fclose(file);
    return 0;
}
```

**使用要点：**

- 适用于二进制模式（`"wb"`）打开的文件。
- 需检查返回值 `count`，确保写入了预期数量的数据块。
- 与 `fread` 配合使用，可实现数据的序列化与反序列化。

## 低级别输出

### `write`（系统调用）：底层数据写入

`write` 是 POSIX 系统调用，用于直接操作文件描述符，**非标准 C 库函数**。

```c
ssize_t write(int fd, const void *buf, size_t count);
```

> **注意**：此函数属于操作系统 API，可移植性较低。初学者建议优先使用标准库函数（如 `fwrite`）。

## 安全输出扩展：`printf_s`

`printf_s` 是 Microsoft Visual Studio 提供的安全版本，通过增强格式检查防止安全问题。

```c
int printf_s(const char *format, ...);
```

**示例：**

```c
#include <stdio.h>

int main() {
    char name[20] = "张三";
    int age = 25;

    printf_s("姓名：%s，年龄：%d\n", name, age);
    return 0;
}
```

**重要说明：**

- **非标准函数**：仅部分编译器支持（如 MSVC），GCC/Clang 需启用特定扩展。
- 提供额外的安全检查，如检测无效格式说明符。
- 仍需确保格式说明符与参数匹配，不能完全替代良好的编程习惯。

## 总结与最佳实践

| **输出类型**       | **推荐函数** | **适用场景**                     | **注意事项**                              |
|--------------------|--------------|----------------------------------|------------------------------------------|
| 格式化输出         | `printf`     | 简单屏幕输出                     | 注意格式匹配，避免未定义行为             |
| 安全字符串输出     | `snprintf`   | 构建字符串（如日志、消息）       | **始终优先使用**，避免 `sprintf`         |
| 文件格式化输出     | `fprintf`    | 向文件写入结构化数据             | 检查文件打开状态，及时关闭文件           |
| 字符处理           | `fputc`      | 逐字符构建文件内容               | 适合需要精细控制的场景                   |
| 文本行输出         | `fputs`      | 写入文本行到文件                 | **不会自动添加换行符**，需手动处理       |
| 二进制数据         | `fwrite`     | 写入非文本数据（如图片、数据文件）| 确保缓冲区数据正确，检查返回值           |

**核心原则：**

1. **安全第一**：避免使用 `sprintf`，优先选择带长度限制的 `snprintf`。
2. **错误处理**：检查文件操作函数的返回值，处理可能的失败情况。
3. **资源管理**：打开的文件必须用 `fclose` 关闭，防止数据丢失。
4. **可移植性**：标准 C 函数（如 `printf`、`snprintf`）比平台扩展更通用。
5. **清晰输出**：合理使用换行符和空格，确保输出内容易于阅读。

**常见错误与解决方案：**

- **格式不匹配**：用 `%d` 输出浮点数 → 检查格式说明符与参数类型是否一致
- **缓冲区溢出**：`sprintf` 写入过长字符串 → 改用 `snprintf` 并指定缓冲区大小
- **文件未关闭**：程序崩溃导致数据未写入 → 确保每个 `fopen` 都有对应的 `fclose`
- **缺少换行符**：`fputs` 输出无换行 → 手动添加 `\n` 或使用 `fprintf` 控制格式

## 实战练习

尝试编写一个程序，实现以下功能：

1. 从键盘读取用户姓名和年龄（使用 `fgets` 安全输入）
2. 将信息格式化后写入到文件 `user_info.txt`
3. 同时在屏幕上显示确认信息
4. 验证文件是否成功写入

```c
#include <stdio.h>
#include <string.h>

int main() {
    char name[50];
    int age;
    
    // 安全读取姓名
    printf("请输入您的姓名：");
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = '\0';  // 移除换行符
    
    // 读取年龄（简单示例，实际应验证输入）
    printf("请输入您的年龄：");
    scanf("%d", &age);
    
    // 写入文件
    FILE *file = fopen("user_info.txt", "w");
    if (file != NULL) {
        fprintf(file, "姓名：%s\n年龄：%d 岁\n", name, age);
        fclose(file);
        
        // 确认信息
        printf("\n信息已保存到文件！\n");
        printf("---------- 用户信息 ----------\n");
        printf("姓名：%s\n", name);
        printf("年龄：%d 岁\n", age);
        printf("------------------------------\n");
    } else {
        printf("错误：无法创建文件！\n");
    }
    
    return 0;
}
```

通过本章学习，你已经掌握了 C 语言中各种输出方法的使用技巧。结合前一章的输入知识，你现在能够构建完整的输入-输出流程，实现与用户的交互和数据的持久化存储。下一章我们将探讨 C 语言中的文件操作，深入理解如何高效管理文件资源！
