# C 语言中的数组和字符串

数组和字符串是 C 编程中的基本数据结构。有效地使用它们对于任何 C 程序员都是至关重要的。

## 数组

### 什么是数组？

数组是存储在连续内存位置中的相同数据类型元素的集合。数组提供了一种在单个变量名下存储多个值的方法。

### 数组声明和初始化

#### 基本声明

```c
// 声明
int numbers[5];        // 5个整数的数组
float scores[10];      // 10个浮点数的数组
char letters[26];      // 26个字符的数组

// 声明并初始化
int ages[3] = {25, 30, 35};
float prices[] = {10.5, 20.0, 15.75};  // 大小从初始化器推断
char vowels[5] = {'a', 'e', 'i', 'o', 'u'};
```

#### 零初始化

```c
int zeros[100] = {0};     // 所有元素初始化为0
int partial[5] = {1, 2};  // 前两个元素：1, 2；其余：0
```

### 访问数组元素

数组元素使用从零开始的索引访问：

```c
#include <stdio.h>

int main() {
    int numbers[5] = {10, 20, 30, 40, 50};
    
    // 访问元素
    printf("第一个元素: %d\n", numbers[0]);   // 10
    printf("第三个元素: %d\n", numbers[2]);   // 30
    printf("最后一个元素: %d\n", numbers[4]); // 50
    
    // 修改元素
    numbers[1] = 25;
    printf("修改后的第二个元素: %d\n", numbers[1]);  // 25
    
    return 0;
}
```

### 数组操作

#### 查找数组大小

```c
#include <stdio.h>

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    int size = sizeof(arr) / sizeof(arr[0]);
    
    printf("数组大小: %d\n", size);  // 5
    
    return 0;
}
```

#### 遍历数组

```c
#include <stdio.h>

int main() {
    int numbers[5] = {10, 20, 30, 40, 50};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    
    // 使用for循环
    printf("数组元素: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");
    
    return 0;
}
```

#### 数组函数

```c
#include <stdio.h>

// 查找最大元素的函数
int findMax(int arr[], int size) {
    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

// 计算总和的函数
int calculateSum(int arr[], int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

int main() {
    int numbers[] = {15, 8, 23, 4, 16};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    
    printf("最大值: %d\n", findMax(numbers, size));
    printf("总和: %d\n", calculateSum(numbers, size));
    
    return 0;
}
```

## 多维数组

### 二维数组

```c
#include <stdio.h>

int main() {
    // 声明和初始化
    int matrix[3][4] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };
    
    // 访问元素
    printf("位置[1][2]的元素: %d\n", matrix[1][2]);  // 7
    
    // 遍历二维数组
    printf("矩阵:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 4; j++) {
            printf("%3d ", matrix[i][j]);
        }
        printf("\n");
    }
    
    return 0;
}
```

## C 语言中的字符串

### 什么是字符串？

在 C 语言中，字符串是以空字符（`\0`）结尾的字符数组。这个空终止符表示字符串的结束。

### 字符串声明和初始化

```c
#include <stdio.h>

int main() {
    // 声明字符串的不同方式
    char str1[20] = "Hello";           // 显式指定大小的数组
    char str2[] = "World";             // 从字符串推断大小
    char str3[10] = {'H', 'i', '\0'};  // 逐字符初始化
    char str4[50];                     // 未初始化的字符串
    
    printf("str1: %s\n", str1);  // Hello
    printf("str2: %s\n", str2);  // World
    printf("str3: %s\n", str3);  // Hi
    
    return 0;
}
```

### 字符串输入和输出

```c
#include <stdio.h>

int main() {
    char name[50];
    char message[100];
    
    // 读取字符串
    printf("请输入您的姓名: ");
    scanf("%s", name);  // 读取直到遇到空白字符
    
    printf("请输入一条消息: ");
    getchar();  // 消费前一个输入的换行符
    fgets(message, sizeof(message), stdin);  // 对包含空格的字符串更安全
    
    printf("你好, %s!\n", name);
    printf("您的消息: %s", message);
    
    return 0;
}
```

### 字符串库函数

包含 `<string.h>` 来使用这些函数：

```c
#include <stdio.h>
#include <string.h>

int main() {
    char str1[50] = "Hello";
    char str2[50] = "World";
    char str3[100];
    
    // 字符串长度
    printf("str1的长度: %lu\n", strlen(str1));  // 5
    
    // 字符串复制
    strcpy(str3, str1);
    printf("复制后的str3: %s\n", str3);  // Hello
    
    // 字符串连接
    strcat(str1, " ");
    strcat(str1, str2);
    printf("连接后: %s\n", str1);  // Hello World
    
    // 字符串比较
    if (strcmp(str2, "World") == 0) {
        printf("str2等于'World'\n");
    }
    
    return 0;
}
```

### 安全字符串函数

```c
#include <stdio.h>
#include <string.h>

int main() {
    char dest[20];
    char src[] = "This is a long string";
    
    // 带大小限制的安全复制
    strncpy(dest, src, sizeof(dest) - 1);
    dest[sizeof(dest) - 1] = '\0';  // 确保空终止
    
    printf("安全复制: %s\n", dest);
    
    // 安全连接
    char greeting[50] = "Hello, ";
    strncat(greeting, "World!", sizeof(greeting) - strlen(greeting) - 1);
    
    printf("安全连接: %s\n", greeting);
    
    return 0;
}
```

### 字符串操作示例

```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// 将字符串转换为大写的函数
void toUpperCase(char str[]) {
    for (int i = 0; str[i] != '\0'; i++) {
        str[i] = toupper(str[i]);
    }
}

// 反转字符串的函数
void reverseString(char str[]) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = temp;
    }
}

// 计算字符串中单词数的函数
int countWords(char str[]) {
    int count = 0;
    int inWord = 0;
    
    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] != ' ' && str[i] != '\t' && str[i] != '\n') {
            if (!inWord) {
                count++;
                inWord = 1;
            }
        } else {
            inWord = 0;
        }
    }
    
    return count;
}

int main() {
    char text[] = "Hello World Programming";
    char copy[100];
    
    strcpy(copy, text);
    
    printf("原始: %s\n", text);
    
    toUpperCase(copy);
    printf("大写: %s\n", copy);
    
    strcpy(copy, text);
    reverseString(copy);
    printf("反转: %s\n", copy);
    
    printf("单词数: %d\n", countWords(text));
    
    return 0;
}
```

## 常见陷阱和最佳实践

### 数组边界

```c
#include <stdio.h>

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    
    // 错误：数组索引越界
    // arr[5] = 10;  // 未定义行为！
    
    // 正确：保持在边界内
    for (int i = 0; i < 5; i++) {
        printf("%d ", arr[i]);
    }
    
    return 0;
}
```

### 字符串缓冲区溢出

```c
#include <stdio.h>
#include <string.h>

int main() {
    char buffer[10];
    
    // 错误：潜在的缓冲区溢出
    // strcpy(buffer, "This string is too long");
    
    // 正确：使用安全函数
    strncpy(buffer, "Safe", sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
    
    printf("安全字符串: %s\n", buffer);
    
    return 0;
}
```

### 最佳实践

1. **访问元素时始终检查数组边界**
2. **使用安全的字符串函数**，如 `strncpy()`、`strncat()`、`snprintf()`
3. **初始化数组**以避免垃圾值
4. **使用字符数组时手动添加空终止符**
5. **对传递给函数的只读数组使用 `const`**
6. **考虑使用 `size_t`** 作为数组索引和大小

```c
#include <stdio.h>
#include <string.h>

// 良好实践：对只读数组使用const
void printArray(const int arr[], size_t size) {
    for (size_t i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    size_t size = sizeof(numbers) / sizeof(numbers[0]);
    
    printArray(numbers, size);
    
    return 0;
}
```

数组和字符串构成了 C 语言数据操作的基础。掌握这些概念，您将能够很好地处理更复杂的数据结构和算法！

---

**语言版本：**

- [English](arrays-strings.md) - 英文版本
- **中文** - 当前页面
