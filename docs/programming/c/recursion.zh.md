# C 语言中的递归

递归是一种编程技术，函数调用自身来解决问题，通过将问题分解为更小的、相似的子问题。这是解决具有递归结构问题的强大工具。

## 理解递归

### 基本概念

递归函数有两个基本组成部分：

1. **基本情况**：停止递归的条件
2. **递归情况**：函数使用修改后的参数调用自身

```c
#include <stdio.h>

// 简单示例：倒计时
void countdown(int n) {
    // 基本情况
    if (n <= 0) {
        printf("发射！\n");
        return;
    }
    
    // 递归情况
    printf("%d\n", n);
    countdown(n - 1);  // 函数调用自身
}

int main() {
    countdown(5);
    return 0;
}
```

### 递归的工作原理

每个递归调用都会创建一个新的栈帧，包含自己的局部变量。调用会堆叠直到达到基本情况，然后开始展开。

```c
#include <stdio.h>

void showStack(int n) {
    printf("进入函数，n = %d\n", n);
    
    if (n <= 1) {
        printf("达到基本情况，n = %d\n", n);
        return;
    }
    
    showStack(n - 1);
    printf("从函数返回，n = %d\n", n);
}

int main() {
    showStack(3);
    return 0;
}
```

## 经典递归示例

### 阶乘

n 的阶乘（n!）是从 1 到 n 所有正整数的乘积。

```c
#include <stdio.h>

long long factorial(int n) {
    // 基本情况
    if (n <= 1) {
        return 1;
    }
    
    // 递归情况：n! = n * (n-1)!
    return n * factorial(n - 1);
}

int main() {
    int num = 5;
    printf("%d! = %lld\n", num, factorial(num));
    
    // 显示计算步骤
    printf("计算：5 * 4 * 3 * 2 * 1 = %lld\n", factorial(5));
    
    return 0;
}
```

### 斐波那契数列

每个数字是前两个数字的和。

```c
#include <stdio.h>

int fibonacci(int n) {
    // 基本情况
    if (n <= 0) return 0;
    if (n == 1) return 1;
    
    // 递归情况：F(n) = F(n-1) + F(n-2)
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// 使用记忆化概念的更高效版本
int fibonacciEfficient(int n, int memo[]) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    
    if (memo[n] != -1) {
        return memo[n];  // 已经计算过
    }
    
    memo[n] = fibonacciEfficient(n - 1, memo) + fibonacciEfficient(n - 2, memo);
    return memo[n];
}

int main() {
    printf("斐波那契数列（前10个数字）：\n");
    for (int i = 0; i < 10; i++) {
        printf("F(%d) = %d\n", i, fibonacci(i));
    }
    
    // 高效版本
    int memo[50];
    for (int i = 0; i < 50; i++) memo[i] = -1;
    
    printf("\n高效 F(40) = %d\n", fibonacciEfficient(40, memo));
    
    return 0;
}
```

### 幂函数

计算 x 的 n 次方。

```c
#include <stdio.h>

double power(double base, int exponent) {
    // 基本情况
    if (exponent == 0) {
        return 1.0;
    }
    
    // 处理负指数
    if (exponent < 0) {
        return 1.0 / power(base, -exponent);
    }
    
    // 递归情况
    return base * power(base, exponent - 1);
}

// 使用分治法的更高效版本
double powerEfficient(double base, int exponent) {
    if (exponent == 0) return 1.0;
    
    if (exponent < 0) {
        return 1.0 / powerEfficient(base, -exponent);
    }
    
    if (exponent % 2 == 0) {
        // 偶数指数：x^n = (x^(n/2))^2
        double half = powerEfficient(base, exponent / 2);
        return half * half;
    } else {
        // 奇数指数：x^n = x * x^(n-1)
        return base * powerEfficient(base, exponent - 1);
    }
}

int main() {
    printf("2^10 = %.0f\n", power(2.0, 10));
    printf("3^4 = %.0f\n", power(3.0, 4));
    printf("2^(-3) = %.3f\n", power(2.0, -3));
    
    printf("高效 2^20 = %.0f\n", powerEfficient(2.0, 20));
    
    return 0;
}
```

## 数组递归

### 数组求和

```c
#include <stdio.h>

int arraySum(int arr[], int size) {
    // 基本情况
    if (size <= 0) {
        return 0;
    }
    
    // 递归情况：和 = 第一个元素 + 其余元素的和
    return arr[0] + arraySum(arr + 1, size - 1);
}

// 使用索引的替代方法
int arraySumIndex(int arr[], int index, int size) {
    if (index >= size) {
        return 0;
    }
    
    return arr[index] + arraySumIndex(arr, index + 1, size);
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    
    printf("数组和：%d\n", arraySum(numbers, size));
    printf("数组和（索引）：%d\n", arraySumIndex(numbers, 0, size));
    
    return 0;
}
```

### 二分查找

```c
#include <stdio.h>

int binarySearch(int arr[], int left, int right, int target) {
    // 基本情况：未找到元素
    if (left > right) {
        return -1;
    }
    
    int mid = left + (right - left) / 2;
    
    // 基本情况：找到元素
    if (arr[mid] == target) {
        return mid;
    }
    
    // 递归情况
    if (arr[mid] > target) {
        return binarySearch(arr, left, mid - 1, target);
    } else {
        return binarySearch(arr, mid + 1, right, target);
    }
}

int main() {
    int arr[] = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
    int size = sizeof(arr) / sizeof(arr[0]);
    int target = 7;
    
    int result = binarySearch(arr, 0, size - 1, target);
    
    if (result != -1) {
        printf("元素 %d 在索引 %d 处找到\n", target, result);
    } else {
        printf("未找到元素 %d\n", target);
    }
    
    return 0;
}
```

## 字符串递归

### 字符串长度

```c
#include <stdio.h>

int stringLength(char *str) {
    // 基本情况：字符串结束
    if (*str == '\0') {
        return 0;
    }
    
    // 递归情况：1 + 其余部分的长度
    return 1 + stringLength(str + 1);
}

int main() {
    char text[] = "Hello, World!";
    printf("'%s' 的长度：%d\n", text, stringLength(text));
    
    return 0;
}
```

### 字符串反转

```c
#include <stdio.h>
#include <string.h>

void reverseString(char *str, int start, int end) {
    // 基本情况
    if (start >= end) {
        return;
    }
    
    // 交换字符
    char temp = str[start];
    str[start] = str[end];
    str[end] = temp;
    
    // 递归情况
    reverseString(str, start + 1, end - 1);
}

int main() {
    char text[] = "Hello";
    printf("原始：%s\n", text);
    
    reverseString(text, 0, strlen(text) - 1);
    printf("反转：%s\n", text);
    
    return 0;
}
```

### 回文检查

```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int isPalindrome(char *str, int start, int end) {
    // 基本情况：单个字符或空
    if (start >= end) {
        return 1;  // 真
    }
    
    // 跳过非字母字符
    if (!isalpha(str[start])) {
        return isPalindrome(str, start + 1, end);
    }
    if (!isalpha(str[end])) {
        return isPalindrome(str, start, end - 1);
    }
    
    // 比较字符（不区分大小写）
    if (tolower(str[start]) != tolower(str[end])) {
        return 0;  // 假
    }
    
    // 递归情况
    return isPalindrome(str, start + 1, end - 1);
}

int main() {
    char text1[] = "racecar";
    char text2[] = "A man a plan a canal Panama";
    char text3[] = "hello";
    
    printf("'%s' %s回文\n", text1, 
           isPalindrome(text1, 0, strlen(text1) - 1) ? "是" : "不是");
    printf("'%s' %s回文\n", text2, 
           isPalindrome(text2, 0, strlen(text2) - 1) ? "是" : "不是");
    printf("'%s' %s回文\n", text3, 
           isPalindrome(text3, 0, strlen(text3) - 1) ? "是" : "不是");
    
    return 0;
}
```

## 常见陷阱和最佳实践

### 栈溢出

```c
#include <stdio.h>

// 错误：没有基本情况 - 无限递归
void infiniteRecursion(int n) {
    printf("%d\n", n);
    infiniteRecursion(n + 1);  // 栈溢出！
}

// 正确：适当的基本情况
void safeRecursion(int n, int limit) {
    if (n > limit) {
        return;  // 基本情况防止无限递归
    }
    
    printf("%d\n", n);
    safeRecursion(n + 1, limit);
}

int main() {
    // infiniteRecursion(1);  // 不要运行这个！
    safeRecursion(1, 5);
    
    return 0;
}
```

## 最佳实践

1. **始终有基本情况**以防止无限递归
2. **在每次递归调用中向基本情况前进**
3. **考虑迭代替代方案**以获得更好的性能
4. **使用记忆化**避免冗余计算
5. **注意栈深度**对于大输入
6. **首先用小输入测试**

递归是一种强大的技术，可以通过将复杂问题分解为更小的、相似的子问题来使其更易于管理。掌握这些概念，您将能够解决广泛的算法挑战！

---

**语言版本：**

- [English](recursion.md) - 英文版本
- **中文** - 当前页面
