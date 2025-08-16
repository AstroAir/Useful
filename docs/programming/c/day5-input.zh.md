# 从零入门 C 语言：Day5 - 标准输入

## 引入

在 C 语言中，输入是指从用户、文件或其他外部源获取数据并存储到程序变量中的过程。C 语言提供了多种输入方式，适用于不同场景：从简单的键盘输入到复杂的文件处理。本章将系统介绍这些输入方法，帮助你掌握如何安全、有效地获取程序所需的数据。

## 标准输入函数

### `scanf`：格式化输入的基础工具

`scanf` 是 C 语言中最常用的输入函数，用于从标准输入（通常是键盘）读取格式化的数据。

```c
int scanf(const char *format, ...);
```

- **format**：格式字符串，指定要读取的数据类型（如 `"%d"` 表示整数，`"%f"` 表示浮点数）。
- **返回值**：成功读取的变量数量；若遇到文件结束或读取错误，返回 `EOF`。

**示例：**

```c
#include <stdio.h>

int main() {
    int num;
    float f;

    printf("请输入一个整数和一个浮点数：");
    scanf("%d %f", &num, &f);  // & 表示取变量地址，让 scanf 能修改变量值

    printf("您输入的是：%d 和 %.2f\n", num, f);
    return 0;
}
```

**关键注意事项：**

- 必须使用 `&` 传递变量地址，否则会导致程序崩溃。
- `scanf` 会自动跳过输入中的空白字符（空格、换行、制表符），但需用空格分隔多个输入项。
- **格式匹配问题**：若输入与格式字符串不匹配（如输入字母但要求整数），可能导致读取失败或后续输入异常。

> **小贴士**：初学者常因格式字符串与输入不匹配而困惑。建议先用简单示例练习，逐步熟悉常见格式说明符。

### `fscanf`：从文件读取格式化数据

`fscanf` 与 `scanf` 功能类似，但用于从文件流中读取数据。

```c
int fscanf(FILE *stream, const char *format, ...);
```

- **stream**：文件指针，指定数据来源（如 `fopen` 打开的文件）。

**示例：**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("文件打开失败！\n");
        return 1;
    }

    int num;
    fscanf(file, "%d", &num);  // 从文件读取整数
    printf("文件中的数字：%d\n", num);

    fclose(file);  // 务必关闭文件，避免资源泄漏
    return 0;
}
```

**使用要点：**

- 操作文件前必须检查 `fopen` 是否成功。
- 文件使用完毕后，**必须调用 `fclose` 关闭**，否则可能导致数据丢失或资源占用。

### `sscanf`：从字符串解析数据

`sscanf` 用于从字符串中提取格式化数据，适合解析已有的文本内容。

```c
int sscanf(const char *str, const char *format, ...);
```

- **str**：待解析的字符串。

**示例：**

```c
#include <stdio.h>

int main() {
    char input[] = "42 3.14";
    int num;
    float f;

    sscanf(input, "%d %f", &num, &f);  // 从字符串提取数据
    printf("解析结果：%d 和 %.2f\n", num, f);

    return 0;
}
```

## 字符输入函数

### `getchar`：单字符输入

`getchar` 从标准输入读取**单个字符**，返回类型为 `int`（用于兼容 `EOF`）。

```c
int getchar(void);
```

**示例：**

```c
#include <stdio.h>

int main() {
    char c;

    printf("请输入一个字符：");
    c = getchar();  // 读取一个字符（包括空格和换行符）

    printf("您输入的是：%c\n", c);
    return 0;
}
```

**关键特性：**

- 不会跳过空白字符，输入空格或回车也会被读取。
- 返回值为 `int`，需转换为 `char` 使用（如 `c = (char)getchar()`）。

### `fgetc` 和 `getc`：文件字符读取

两者均用于从文件流读取单个字符，区别在于 `getc` 通常是宏实现（可能多次求值参数），而 `fgetc` 是标准函数。

```c
int fgetc(FILE *stream);
int getc(FILE *stream);
```

**示例：**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("文件打开失败！\n");
        return 1;
    }

    int c;  // 必须用 int 存储，以兼容 EOF
    while ((c = fgetc(file)) != EOF) {
        putchar(c);  // 逐字符输出
    }

    fclose(file);
    return 0;
}
```

**使用建议：**

- 优先使用 `fgetc`，避免 `getc` 的潜在副作用。
- 用 `int` 存储返回值，确保能正确识别 `EOF`。

### `ungetc`：回退输入字符

`ungetc` 将字符"放回"输入流，使其成为下一次读取的目标。常用于需要预读字符的解析场景。

```c
int ungetc(int c, FILE *stream);
```

**示例：**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("文件打开失败！\n");
        return 1;
    }

    int c = fgetc(file);
    if (c != EOF) {
        ungetc(c, file);  // 将字符放回流
        c = fgetc(file);  // 再次读取同一字符
        printf("重新读取的字符：%c\n", c);
    }

    fclose(file);
    return 0;
}
```

**重要限制：**

- 标准仅保证能放回**一个字符**，多次调用 `ungetc` 的行为未定义。
- 放回的字符必须与流的编码兼容（如文本模式下不能放回二进制数据）。

## 行输入函数

### `fgets`：安全的行读取（推荐使用）

`fgets` 用于读取整行输入，**能有效避免缓冲区溢出**，是替代 `gets` 的安全选择。

```c
char *fgets(char *str, int n, FILE *stream);
```

- **str**：存储输入的缓冲区。
- **n**：最多读取字符数（含终止符 `\0`）。
- **stream**：输入流（`stdin` 表示键盘输入）。

**示例：**

```c
#include <stdio.h>
#include <string.h>  // 用于 strcspn

int main() {
    char str[100];

    printf("请输入一段文字：");
    if (fgets(str, sizeof(str), stdin) != NULL) {
        // 移除可能的换行符
        str[strcspn(str, "\n")] = '\0';
        printf("您输入的是：%s\n", str);
    } else {
        printf("输入读取失败！\n");
    }

    return 0;
}
```

**关键优势：**

- 通过 `n` 参数限制输入长度，防止缓冲区溢出。
- 保留换行符 `\n`（需手动移除，如示例所示）。

> **为什么不用 `gets`？**  
> `gets` 因无法限制输入长度，已被 C11 标准移除。**强烈建议永远使用 `fgets` 替代 `gets`**。

## 文件与系统级输入

### `fread`：二进制数据读取

`fread` 用于读取原始数据块，适合处理二进制文件（如图片、自定义格式文件）。

```c
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);
```

**示例：**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("data.bin", "rb");
    if (file == NULL) {
        printf("文件打开失败！\n");
        return 1;
    }

    int data[5];
    size_t count = fread(data, sizeof(int), 5, file);
    for (size_t i = 0; i < count; i++) {
        printf("data[%zu] = %d\n", i, data[i]);
    }

    fclose(file);
    return 0;
}
```

**使用要点：**

- 适用于二进制模式（`"rb"`）打开的文件。
- 需检查返回值 `count`，确保读取了预期数量的数据块。

### `read`（系统调用）：底层数据读取

`read` 是 POSIX 系统调用，用于直接操作文件描述符，**非标准 C 库函数**，通常在系统编程中使用。

```c
ssize_t read(int fd, void *buf, size_t count);
```

> **注意**：此函数属于操作系统 API，可移植性较低。初学者建议优先使用标准库函数（如 `fread`）。

## 安全输入扩展：`scanf_s`

`scanf_s` 是 Microsoft Visual Studio 提供的安全版本，通过强制指定缓冲区大小防止溢出。

```c
int scanf_s(const char *format, ...);
```

**示例：**

```c
#include <stdio.h>

int main() {
    char buffer[10];
    int num;

    printf("请输入一个数字和字符串：");
    scanf_s("%d %9s", &num, buffer, (unsigned)_countof(buffer));

    printf("您输入的是：%d 和 %s\n", num, buffer);
    return 0;
}
```

**重要说明：**

- **非标准函数**：仅部分编译器支持（如 MSVC），GCC/Clang 需启用特定扩展。
- 字符串输入需额外指定缓冲区大小（如 `%9s` 中的 `9` 表示最多读取 9 字符）。

## 总结与最佳实践

| **输入类型**       | **推荐函数** | **适用场景**                     | **注意事项**                              |
|--------------------|--------------|----------------------------------|------------------------------------------|
| 格式化输入         | `scanf`      | 简单键盘输入                     | 注意格式匹配，避免缓冲区溢出             |
| 安全行输入         | `fgets`      | 读取用户输入的文本行             | **始终优先使用**，手动处理换行符         |
| 文件格式化输入     | `fscanf`     | 从文件读取结构化数据             | 检查文件打开状态，及时关闭文件           |
| 字符处理           | `fgetc`      | 逐字符解析文件或输入             | 用 `int` 存储返回值以识别 `EOF`          |
| 二进制数据         | `fread`      | 读取非文本文件（如图片、数据文件）| 确保缓冲区足够大，检查返回值             |

**核心原则：**

1. **安全第一**：避免使用 `gets`，优先选择带长度限制的函数（如 `fgets`）。
2. **错误处理**：始终检查输入函数的返回值，处理可能的失败情况。
3. **资源管理**：打开的文件必须用 `fclose` 关闭，防止资源泄漏。
4. **可移植性**：标准 C 函数（如 `fgets`）比平台扩展（如 `scanf_s`）更通用。

掌握这些输入方法后，你已具备处理大多数 C 语言输入场景的能力。下一章我们将学习如何将数据输出到屏幕或文件，构建完整的输入-输出流程！
