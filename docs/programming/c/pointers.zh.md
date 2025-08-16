# C 语言中的指针

指针是 C 编程最强大和最独特的特性之一。它们提供对内存地址的直接访问，实现高效的内存管理和高级编程技术。

## 什么是指针？

指针是存储另一个变量内存地址的变量。指针不直接保存值，而是"指向"存储值的位置。

### 基本指针概念

```c
#include <stdio.h>

int main() {
    int num = 42;        // 普通变量
    int *ptr = &num;     // 指向int的指针，存储num的地址
    
    printf("num的值: %d\n", num);           // 42
    printf("num的地址: %p\n", &num);        // 内存地址
    printf("ptr的值: %p\n", ptr);          // 与&num相同
    printf("ptr指向的值: %d\n", *ptr);      // 42（解引用）
    
    return 0;
}
```

### 关键操作符

- **取地址操作符（`&`）**：获取变量的地址
- **解引用操作符（`*`）**：访问指针存储地址处的值

## 指针声明和初始化

### 声明语法

```c
int *ptr;        // 指向int的指针
float *fptr;     // 指向float的指针
char *cptr;      // 指向char的指针
double *dptr;    // 指向double的指针
```

### 初始化

```c
#include <stdio.h>

int main() {
    int x = 10;
    
    // 方法1：分别声明和初始化
    int *ptr1;
    ptr1 = &x;
    
    // 方法2：声明和初始化一起进行
    int *ptr2 = &x;
    
    // 方法3：初始化为NULL
    int *ptr3 = NULL;
    
    printf("x = %d\n", x);
    printf("*ptr1 = %d\n", *ptr1);
    printf("*ptr2 = %d\n", *ptr2);
    
    // 解引用前始终检查NULL
    if (ptr3 != NULL) {
        printf("*ptr3 = %d\n", *ptr3);
    } else {
        printf("ptr3是NULL\n");
    }
    
    return 0;
}
```

## 指针算术

指针支持按其指向的数据类型大小缩放的算术操作。

```c
#include <stdio.h>

int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int *ptr = arr;  // 指向第一个元素
    
    printf("使用指针算术访问数组元素:\n");
    for (int i = 0; i < 5; i++) {
        printf("arr[%d] = %d, *(ptr + %d) = %d\n", 
               i, arr[i], i, *(ptr + i));
    }
    
    // 移动指针
    printf("\n通过数组移动指针:\n");
    ptr = arr;
    for (int i = 0; i < 5; i++) {
        printf("*ptr = %d, 地址 = %p\n", *ptr, ptr);
        ptr++;  // 移动到下一个元素
    }
    
    return 0;
}
```

## 指针和数组

数组和指针在 C 语言中密切相关。数组名本质上是指向其第一个元素的指针。

```c
#include <stdio.h>

void printArray(int *arr, int size) {
    printf("数组元素: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);  // 或 *(arr + i)
    }
    printf("\n");
}

int main() {
    int numbers[] = {10, 20, 30, 40, 50};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    
    // 数组名作为指针
    printf("第一个元素: %d\n", *numbers);        // 10
    printf("第二个元素: %d\n", *(numbers + 1)); // 20
    
    // 将数组传递给函数
    printArray(numbers, size);
    
    return 0;
}
```

## 指针和字符串

C 语言中的字符串是字符数组，因此指针与字符串自然配合。

```c
#include <stdio.h>

int main() {
    char str[] = "Hello, World!";
    char *ptr = str;
    
    // 使用指针打印字符串
    printf("字符串: %s\n", ptr);
    
    // 使用指针逐字符打印
    printf("字符: ");
    while (*ptr != '\0') {
        printf("%c", *ptr);
        ptr++;
    }
    printf("\n");
    
    // 字符串字面量和指针
    char *message = "Programming";  // 指向字符串字面量
    printf("消息: %s\n", message);
    
    return 0;
}
```

## 函数指针

指针也可以指向函数，实现动态函数调用。

```c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

int main() {
    int (*funcPtr)(int, int);  // 函数指针声明
    
    // 指向add函数
    funcPtr = add;
    printf("5 + 3 = %d\n", funcPtr(5, 3));
    
    // 指向multiply函数
    funcPtr = multiply;
    printf("5 * 3 = %d\n", funcPtr(5, 3));
    
    return 0;
}
```

## 指针和结构体

```c
#include <stdio.h>
#include <stdlib.h>

struct Person {
    char name[50];
    int age;
};

int main() {
    struct Person person = {"Alice", 25};
    struct Person *ptr = &person;
    
    // 通过指针访问结构体成员
    printf("姓名: %s\n", ptr->name);      // 箭头操作符
    printf("年龄: %d\n", ptr->age);
    
    // 替代语法
    printf("姓名: %s\n", (*ptr).name);
    
    return 0;
}
```

## 常见陷阱

### 空指针解引用

```c
#include <stdio.h>

int main() {
    int *ptr = NULL;
    
    // 错误：解引用空指针
    // printf("%d\n", *ptr);  // 段错误！
    
    // 正确：解引用前检查
    if (ptr != NULL) {
        printf("值: %d\n", *ptr);
    } else {
        printf("指针是NULL\n");
    }
    
    return 0;
}
```

### 悬空指针

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr = malloc(sizeof(int));
    *ptr = 42;
    
    free(ptr);      // 内存已释放
    ptr = NULL;     // 设置为NULL以避免悬空指针
    
    if (ptr != NULL) {
        printf("值: %d\n", *ptr);
    } else {
        printf("指针是NULL\n");
    }
    
    return 0;
}
```

## 最佳实践

1. **始终初始化指针**为 NULL 或有效地址
2. **解引用前检查 NULL**
3. **释放内存后将指针设置为 NULL**
4. **每个 malloc 都要有对应的 free**
5. **对只读数据使用 const**

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 良好实践：初始化为NULL
    int *ptr = NULL;
    
    // 分配内存
    ptr = malloc(sizeof(int));
    if (ptr == NULL) {
        printf("内存分配失败\n");
        return 1;
    }
    
    *ptr = 42;
    printf("值: %d\n", *ptr);
    
    // 良好实践：释放并置空
    free(ptr);
    ptr = NULL;
    
    return 0;
}
```

指针是一个强大的特性，能够实现高效的内存管理、动态数据结构和高级编程技术。掌握它们，您将释放 C 编程的全部潜力！

---

**语言版本：**

- [English](pointers.md) - 英文版本
- **中文** - 当前页面
