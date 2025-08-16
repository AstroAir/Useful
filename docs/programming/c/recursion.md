# Recursion in C

Recursion is a programming technique where a function calls itself to solve a problem by breaking it down into smaller, similar subproblems. It's a powerful tool for solving problems that have a recursive structure.

## Understanding Recursion

### Basic Concept

A recursive function has two essential components:

1. **Base case**: A condition that stops the recursion
2. **Recursive case**: The function calls itself with modified parameters

```c
#include <stdio.h>

// Simple example: countdown
void countdown(int n) {
    // Base case
    if (n <= 0) {
        printf("Blast off!\n");
        return;
    }
    
    // Recursive case
    printf("%d\n", n);
    countdown(n - 1);  // Function calls itself
}

int main() {
    countdown(5);
    return 0;
}
```

### How Recursion Works

Each recursive call creates a new stack frame with its own local variables. The calls stack up until the base case is reached, then they unwind.

```c
#include <stdio.h>

void showStack(int n) {
    printf("Entering function with n = %d\n", n);
    
    if (n <= 1) {
        printf("Base case reached with n = %d\n", n);
        return;
    }
    
    showStack(n - 1);
    printf("Returning from function with n = %d\n", n);
}

int main() {
    showStack(3);
    return 0;
}
```

## Classic Recursive Examples

### Factorial

The factorial of n (n!) is the product of all positive integers from 1 to n.

```c
#include <stdio.h>

long long factorial(int n) {
    // Base case
    if (n <= 1) {
        return 1;
    }
    
    // Recursive case: n! = n * (n-1)!
    return n * factorial(n - 1);
}

int main() {
    int num = 5;
    printf("%d! = %lld\n", num, factorial(num));
    
    // Show the calculation steps
    printf("Calculation: 5 * 4 * 3 * 2 * 1 = %lld\n", factorial(5));
    
    return 0;
}
```

### Fibonacci Sequence

Each number is the sum of the two preceding numbers.

```c
#include <stdio.h>

int fibonacci(int n) {
    // Base cases
    if (n <= 0) return 0;
    if (n == 1) return 1;
    
    // Recursive case: F(n) = F(n-1) + F(n-2)
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// More efficient version using memoization concept
int fibonacciEfficient(int n, int memo[]) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    
    if (memo[n] != -1) {
        return memo[n];  // Already calculated
    }
    
    memo[n] = fibonacciEfficient(n - 1, memo) + fibonacciEfficient(n - 2, memo);
    return memo[n];
}

int main() {
    printf("Fibonacci sequence (first 10 numbers):\n");
    for (int i = 0; i < 10; i++) {
        printf("F(%d) = %d\n", i, fibonacci(i));
    }
    
    // Efficient version
    int memo[50];
    for (int i = 0; i < 50; i++) memo[i] = -1;
    
    printf("\nEfficient F(40) = %d\n", fibonacciEfficient(40, memo));
    
    return 0;
}
```

### Power Function

Calculate x raised to the power of n.

```c
#include <stdio.h>

double power(double base, int exponent) {
    // Base case
    if (exponent == 0) {
        return 1.0;
    }
    
    // Handle negative exponents
    if (exponent < 0) {
        return 1.0 / power(base, -exponent);
    }
    
    // Recursive case
    return base * power(base, exponent - 1);
}

// More efficient version using divide and conquer
double powerEfficient(double base, int exponent) {
    if (exponent == 0) return 1.0;
    
    if (exponent < 0) {
        return 1.0 / powerEfficient(base, -exponent);
    }
    
    if (exponent % 2 == 0) {
        // Even exponent: x^n = (x^(n/2))^2
        double half = powerEfficient(base, exponent / 2);
        return half * half;
    } else {
        // Odd exponent: x^n = x * x^(n-1)
        return base * powerEfficient(base, exponent - 1);
    }
}

int main() {
    printf("2^10 = %.0f\n", power(2.0, 10));
    printf("3^4 = %.0f\n", power(3.0, 4));
    printf("2^(-3) = %.3f\n", power(2.0, -3));
    
    printf("Efficient 2^20 = %.0f\n", powerEfficient(2.0, 20));
    
    return 0;
}
```

## Recursion with Arrays

### Array Sum

```c
#include <stdio.h>

int arraySum(int arr[], int size) {
    // Base case
    if (size <= 0) {
        return 0;
    }
    
    // Recursive case: sum = first element + sum of rest
    return arr[0] + arraySum(arr + 1, size - 1);
}

// Alternative approach using index
int arraySumIndex(int arr[], int index, int size) {
    if (index >= size) {
        return 0;
    }
    
    return arr[index] + arraySumIndex(arr, index + 1, size);
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    
    printf("Array sum: %d\n", arraySum(numbers, size));
    printf("Array sum (index): %d\n", arraySumIndex(numbers, 0, size));
    
    return 0;
}
```

### Binary Search

```c
#include <stdio.h>

int binarySearch(int arr[], int left, int right, int target) {
    // Base case: element not found
    if (left > right) {
        return -1;
    }
    
    int mid = left + (right - left) / 2;
    
    // Base case: element found
    if (arr[mid] == target) {
        return mid;
    }
    
    // Recursive cases
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
        printf("Element %d found at index %d\n", target, result);
    } else {
        printf("Element %d not found\n", target);
    }
    
    return 0;
}
```

## String Recursion

### String Length

```c
#include <stdio.h>

int stringLength(char *str) {
    // Base case: end of string
    if (*str == '\0') {
        return 0;
    }
    
    // Recursive case: 1 + length of rest
    return 1 + stringLength(str + 1);
}

int main() {
    char text[] = "Hello, World!";
    printf("Length of '%s': %d\n", text, stringLength(text));
    
    return 0;
}
```

### String Reversal

```c
#include <stdio.h>
#include <string.h>

void reverseString(char *str, int start, int end) {
    // Base case
    if (start >= end) {
        return;
    }
    
    // Swap characters
    char temp = str[start];
    str[start] = str[end];
    str[end] = temp;
    
    // Recursive case
    reverseString(str, start + 1, end - 1);
}

int main() {
    char text[] = "Hello";
    printf("Original: %s\n", text);
    
    reverseString(text, 0, strlen(text) - 1);
    printf("Reversed: %s\n", text);
    
    return 0;
}
```

### Palindrome Check

```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int isPalindrome(char *str, int start, int end) {
    // Base case: single character or empty
    if (start >= end) {
        return 1;  // True
    }
    
    // Skip non-alphabetic characters
    if (!isalpha(str[start])) {
        return isPalindrome(str, start + 1, end);
    }
    if (!isalpha(str[end])) {
        return isPalindrome(str, start, end - 1);
    }
    
    // Compare characters (case insensitive)
    if (tolower(str[start]) != tolower(str[end])) {
        return 0;  // False
    }
    
    // Recursive case
    return isPalindrome(str, start + 1, end - 1);
}

int main() {
    char text1[] = "racecar";
    char text2[] = "A man a plan a canal Panama";
    char text3[] = "hello";
    
    printf("'%s' is %spalindrome\n", text1, 
           isPalindrome(text1, 0, strlen(text1) - 1) ? "" : "not ");
    printf("'%s' is %spalindrome\n", text2, 
           isPalindrome(text2, 0, strlen(text2) - 1) ? "" : "not ");
    printf("'%s' is %spalindrome\n", text3, 
           isPalindrome(text3, 0, strlen(text3) - 1) ? "" : "not ");
    
    return 0;
}
```

## Tree Traversal

### Binary Tree Structure

```c
#include <stdio.h>
#include <stdlib.h>

struct TreeNode {
    int data;
    struct TreeNode *left;
    struct TreeNode *right;
};

struct TreeNode* createNode(int data) {
    struct TreeNode *node = malloc(sizeof(struct TreeNode));
    node->data = data;
    node->left = NULL;
    node->right = NULL;
    return node;
}

// Preorder traversal: Root -> Left -> Right
void preorderTraversal(struct TreeNode *root) {
    if (root == NULL) {
        return;  // Base case
    }
    
    printf("%d ", root->data);
    preorderTraversal(root->left);
    preorderTraversal(root->right);
}

// Inorder traversal: Left -> Root -> Right
void inorderTraversal(struct TreeNode *root) {
    if (root == NULL) {
        return;
    }
    
    inorderTraversal(root->left);
    printf("%d ", root->data);
    inorderTraversal(root->right);
}

// Postorder traversal: Left -> Right -> Root
void postorderTraversal(struct TreeNode *root) {
    if (root == NULL) {
        return;
    }
    
    postorderTraversal(root->left);
    postorderTraversal(root->right);
    printf("%d ", root->data);
}

int main() {
    // Create a simple binary tree
    struct TreeNode *root = createNode(1);
    root->left = createNode(2);
    root->right = createNode(3);
    root->left->left = createNode(4);
    root->left->right = createNode(5);
    
    printf("Preorder: ");
    preorderTraversal(root);
    printf("\n");
    
    printf("Inorder: ");
    inorderTraversal(root);
    printf("\n");
    
    printf("Postorder: ");
    postorderTraversal(root);
    printf("\n");
    
    return 0;
}
```

## Common Pitfalls and Best Practices

### Stack Overflow

```c
#include <stdio.h>

// BAD: No base case - infinite recursion
void infiniteRecursion(int n) {
    printf("%d\n", n);
    infiniteRecursion(n + 1);  // Stack overflow!
}

// GOOD: Proper base case
void safeRecursion(int n, int limit) {
    if (n > limit) {
        return;  // Base case prevents infinite recursion
    }
    
    printf("%d\n", n);
    safeRecursion(n + 1, limit);
}

int main() {
    // infiniteRecursion(1);  // Don't run this!
    safeRecursion(1, 5);
    
    return 0;
}
```

### Efficiency Considerations

```c
#include <stdio.h>
#include <time.h>

// Inefficient: Exponential time complexity
int fibonacciSlow(int n) {
    if (n <= 1) return n;
    return fibonacciSlow(n - 1) + fibonacciSlow(n - 2);
}

// Efficient: Linear time with memoization
int fibonacciFast(int n, int memo[]) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    
    memo[n] = fibonacciFast(n - 1, memo) + fibonacciFast(n - 2, memo);
    return memo[n];
}

int main() {
    int n = 35;
    
    clock_t start = clock();
    int result1 = fibonacciSlow(n);
    clock_t end = clock();
    double time1 = ((double)(end - start)) / CLOCKS_PER_SEC;
    
    int memo[100];
    for (int i = 0; i < 100; i++) memo[i] = -1;
    
    start = clock();
    int result2 = fibonacciFast(n, memo);
    end = clock();
    double time2 = ((double)(end - start)) / CLOCKS_PER_SEC;
    
    printf("Slow fibonacci(%d) = %d, Time: %.6f seconds\n", n, result1, time1);
    printf("Fast fibonacci(%d) = %d, Time: %.6f seconds\n", n, result2, time2);
    
    return 0;
}
```

## Best Practices

1. **Always have a base case** to prevent infinite recursion
2. **Make progress toward the base case** in each recursive call
3. **Consider iterative alternatives** for better performance
4. **Use memoization** to avoid redundant calculations
5. **Be mindful of stack depth** for large inputs
6. **Test with small inputs** first

Recursion is a powerful technique that can make complex problems more manageable by breaking them into smaller, similar subproblems. Master these concepts, and you'll be able to solve a wide range of algorithmic challenges!
