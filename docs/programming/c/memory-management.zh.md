# C 语言中的内存管理

内存管理是 C 编程的关键方面。与高级语言不同，C 语言让您直接控制内存分配和释放，这提供了强大的功能，但也带来了责任。

## 内存类型

### 栈内存

栈内存是自动管理的，用于：

- 局部变量
- 函数参数
- 返回地址

```c
#include <stdio.h>

void stackExample() {
    int localVar = 10;        // 在栈上分配
    char buffer[100];         // 在栈上分配
    
    printf("局部变量: %d\n", localVar);
    // 函数结束时内存自动释放
}

int main() {
    stackExample();
    // localVar 和 buffer 不再可访问
    return 0;
}
```

### 堆内存

堆内存是手动管理的，用于：

- 动态分配
- 大型数据结构
- 需要在函数作用域之外持续存在的数据

## 动态内存分配

### malloc() - 内存分配

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 为10个整数分配内存
    int *ptr = malloc(10 * sizeof(int));
    
    // 始终检查分配是否成功
    if (ptr == NULL) {
        printf("内存分配失败\n");
        return 1;
    }
    
    // 使用分配的内存
    for (int i = 0; i < 10; i++) {
        ptr[i] = i * i;
    }
    
    // 打印值
    printf("平方数: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", ptr[i]);
    }
    printf("\n");
    
    // 释放内存
    free(ptr);
    ptr = NULL;  // 良好实践
    
    return 0;
}
```

### calloc() - 清零分配

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 分配并初始化为零
    int *ptr = calloc(5, sizeof(int));
    
    if (ptr == NULL) {
        printf("内存分配失败\n");
        return 1;
    }
    
    printf("初始化的值: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", ptr[i]);  // 全部为零
    }
    printf("\n");
    
    free(ptr);
    return 0;
}
```

### realloc() - 重新分配大小

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 初始分配
    int *ptr = malloc(3 * sizeof(int));
    if (ptr == NULL) return 1;
    
    // 填充初始值
    for (int i = 0; i < 3; i++) {
        ptr[i] = i + 1;
    }
    
    // 调整大小以容纳6个整数
    ptr = realloc(ptr, 6 * sizeof(int));
    if (ptr == NULL) {
        printf("重新分配失败\n");
        return 1;
    }
    
    // 填充新值
    for (int i = 3; i < 6; i++) {
        ptr[i] = i + 1;
    }
    
    printf("调整大小后的数组: ");
    for (int i = 0; i < 6; i++) {
        printf("%d ", ptr[i]);
    }
    printf("\n");
    
    free(ptr);
    return 0;
}
```

### free() - 内存释放

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr = malloc(sizeof(int));
    
    if (ptr != NULL) {
        *ptr = 42;
        printf("值: %d\n", *ptr);
        
        // 释放内存
        free(ptr);
        
        // 设置为NULL以避免悬空指针
        ptr = NULL;
    }
    
    return 0;
}
```

## 动态数组

### 创建动态数组

```c
#include <stdio.h>
#include <stdlib.h>

int* createArray(int size) {
    int *arr = malloc(size * sizeof(int));
    if (arr == NULL) {
        return NULL;
    }
    
    // 初始化数组
    for (int i = 0; i < size; i++) {
        arr[i] = i * 2;
    }
    
    return arr;
}

int main() {
    int size = 5;
    int *dynamicArray = createArray(size);
    
    if (dynamicArray == NULL) {
        printf("创建数组失败\n");
        return 1;
    }
    
    printf("动态数组: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", dynamicArray[i]);
    }
    printf("\n");
    
    free(dynamicArray);
    return 0;
}
```

### 可调整大小的数组实现

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    int size;
    int capacity;
} DynamicArray;

DynamicArray* createDynamicArray() {
    DynamicArray *arr = malloc(sizeof(DynamicArray));
    if (arr == NULL) return NULL;
    
    arr->data = malloc(2 * sizeof(int));
    if (arr->data == NULL) {
        free(arr);
        return NULL;
    }
    
    arr->size = 0;
    arr->capacity = 2;
    return arr;
}

int append(DynamicArray *arr, int value) {
    if (arr->size >= arr->capacity) {
        // 调整数组大小
        int newCapacity = arr->capacity * 2;
        int *newData = realloc(arr->data, newCapacity * sizeof(int));
        if (newData == NULL) return 0;  // 失败
        
        arr->data = newData;
        arr->capacity = newCapacity;
    }
    
    arr->data[arr->size++] = value;
    return 1;  // 成功
}

void printArray(DynamicArray *arr) {
    printf("数组: ");
    for (int i = 0; i < arr->size; i++) {
        printf("%d ", arr->data[i]);
    }
    printf("(大小: %d, 容量: %d)\n", arr->size, arr->capacity);
}

void destroyArray(DynamicArray *arr) {
    if (arr != NULL) {
        free(arr->data);
        free(arr);
    }
}

int main() {
    DynamicArray *arr = createDynamicArray();
    if (arr == NULL) return 1;
    
    // 添加元素
    for (int i = 1; i <= 10; i++) {
        append(arr, i * 10);
        printArray(arr);
    }
    
    destroyArray(arr);
    return 0;
}
```

## 字符串的内存管理

### 动态字符串分配

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* createString(const char *source) {
    if (source == NULL) return NULL;
    
    int length = strlen(source);
    char *newString = malloc((length + 1) * sizeof(char));
    
    if (newString == NULL) return NULL;
    
    strcpy(newString, source);
    return newString;
}

char* concatenateStrings(const char *str1, const char *str2) {
    if (str1 == NULL || str2 == NULL) return NULL;
    
    int len1 = strlen(str1);
    int len2 = strlen(str2);
    char *result = malloc((len1 + len2 + 1) * sizeof(char));
    
    if (result == NULL) return NULL;
    
    strcpy(result, str1);
    strcat(result, str2);
    
    return result;
}

int main() {
    char *str1 = createString("你好, ");
    char *str2 = createString("世界!");
    
    if (str1 == NULL || str2 == NULL) {
        printf("字符串创建失败\n");
        return 1;
    }
    
    char *combined = concatenateStrings(str1, str2);
    if (combined == NULL) {
        printf("字符串连接失败\n");
        free(str1);
        free(str2);
        return 1;
    }
    
    printf("合并后: %s\n", combined);
    
    // 清理
    free(str1);
    free(str2);
    free(combined);
    
    return 0;
}
```

## 常见内存错误

### 内存泄漏

```c
#include <stdio.h>
#include <stdlib.h>

// 错误：内存泄漏
void memoryLeak() {
    int *ptr = malloc(100 * sizeof(int));
    // 忘记调用 free(ptr)！
    return;  // 内存泄漏
}

// 正确：适当清理
void properCleanup() {
    int *ptr = malloc(100 * sizeof(int));
    if (ptr == NULL) return;
    
    // 使用内存...
    
    free(ptr);  // 始终释放分配的内存
}

int main() {
    properCleanup();
    return 0;
}
```

### 双重释放

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr = malloc(sizeof(int));
    
    if (ptr != NULL) {
        *ptr = 42;
        free(ptr);
        
        // 错误：双重释放
        // free(ptr);  // 未定义行为！
        
        // 正确：释放后设置为NULL
        ptr = NULL;
        
        // 现在再次调用free是安全的（什么都不做）
        free(ptr);
    }
    
    return 0;
}
```

### 释放后使用

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr = malloc(sizeof(int));
    
    if (ptr != NULL) {
        *ptr = 42;
        printf("释放前: %d\n", *ptr);
        
        free(ptr);
        
        // 错误：释放后使用
        // printf("释放后: %d\n", *ptr);  // 未定义行为！
        
        // 正确：设置为NULL并检查
        ptr = NULL;
        if (ptr != NULL) {
            printf("安全使用: %d\n", *ptr);
        }
    }
    
    return 0;
}
```

## 最佳实践

### 内存管理指南

```c
#include <stdio.h>
#include <stdlib.h>

// 良好实践：检查分配并处理错误
int* safeAllocate(int count) {
    int *ptr = malloc(count * sizeof(int));
    if (ptr == NULL) {
        fprintf(stderr, "内存分配失败\n");
        exit(1);
    }
    return ptr;
}

// 良好实践：安全释放的包装器
void safeFree(void **ptr) {
    if (ptr != NULL && *ptr != NULL) {
        free(*ptr);
        *ptr = NULL;
    }
}

int main() {
    int *array = safeAllocate(10);
    
    // 使用数组...
    for (int i = 0; i < 10; i++) {
        array[i] = i;
    }
    
    // 安全清理
    safeFree((void**)&array);
    
    // array现在是NULL，在条件中使用是安全的
    if (array != NULL) {
        printf("数组仍然有效\n");
    } else {
        printf("数组已被释放\n");
    }
    
    return 0;
}
```

### 关键规则

1. **始终检查 malloc 返回值**
2. **每个 malloc 都要有且仅有一个对应的 free**
3. **释放后将指针设置为 NULL**
4. **不要访问已释放的内存**
5. **不要两次释放同一块内存**
6. **尽可能按分配的相反顺序释放内存**

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // 规则1：始终检查malloc
    int *ptr = malloc(sizeof(int));
    if (ptr == NULL) {
        return 1;
    }
    
    // 规则2：使用内存
    *ptr = 42;
    
    // 规则3：只释放一次
    free(ptr);
    
    // 规则4：设置为NULL
    ptr = NULL;
    
    // 规则5：安全检查和使用
    if (ptr != NULL) {
        printf("值: %d\n", *ptr);
    }
    
    return 0;
}
```

适当的内存管理对于编写健壮的 C 程序至关重要。遵循这些实践来避免常见陷阱并创建高效、可靠的软件！

---

**语言版本：**

- [English](memory-management.md) - 英文版本
- **中文** - 当前页面
