# Arrays and Strings in C

Arrays and strings are fundamental data structures in C programming. Understanding how to work with them effectively is crucial for any C programmer.

## Arrays

### What are Arrays?

An array is a collection of elements of the same data type stored in contiguous memory locations. Arrays provide a way to store multiple values under a single variable name.

### Array Declaration and Initialization

#### Basic Declaration

```c
// Declaration
int numbers[5];        // Array of 5 integers
float scores[10];      // Array of 10 floats
char letters[26];      // Array of 26 characters

// Declaration with initialization
int ages[3] = {25, 30, 35};
float prices[] = {10.5, 20.0, 15.75};  // Size inferred from initializer
char vowels[5] = {'a', 'e', 'i', 'o', 'u'};
```

#### Zero Initialization

```c
int zeros[100] = {0};     // All elements initialized to 0
int partial[5] = {1, 2};  // First two elements: 1, 2; rest: 0
```

### Accessing Array Elements

Array elements are accessed using zero-based indexing:

```c
#include <stdio.h>

int main() {
    int numbers[5] = {10, 20, 30, 40, 50};
    
    // Accessing elements
    printf("First element: %d\n", numbers[0]);   // 10
    printf("Third element: %d\n", numbers[2]);   // 30
    printf("Last element: %d\n", numbers[4]);    // 50
    
    // Modifying elements
    numbers[1] = 25;
    printf("Modified second element: %d\n", numbers[1]);  // 25
    
    return 0;
}
```

### Array Operations

#### Finding Array Size

```c
#include <stdio.h>

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    int size = sizeof(arr) / sizeof(arr[0]);
    
    printf("Array size: %d\n", size);  // 5
    
    return 0;
}
```

#### Iterating Through Arrays

```c
#include <stdio.h>

int main() {
    int numbers[5] = {10, 20, 30, 40, 50};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    
    // Using for loop
    printf("Array elements: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");
    
    return 0;
}
```

#### Array Functions

```c
#include <stdio.h>

// Function to find maximum element
int findMax(int arr[], int size) {
    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

// Function to calculate sum
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
    
    printf("Maximum: %d\n", findMax(numbers, size));
    printf("Sum: %d\n", calculateSum(numbers, size));
    
    return 0;
}
```

## Multi-dimensional Arrays

### Two-dimensional Arrays

```c
#include <stdio.h>

int main() {
    // Declaration and initialization
    int matrix[3][4] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };
    
    // Accessing elements
    printf("Element at [1][2]: %d\n", matrix[1][2]);  // 7
    
    // Iterating through 2D array
    printf("Matrix:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 4; j++) {
            printf("%3d ", matrix[i][j]);
        }
        printf("\n");
    }
    
    return 0;
}
```

## Strings in C

### What are Strings?

In C, strings are arrays of characters terminated by a null character (`\0`). This null terminator indicates the end of the string.

### String Declaration and Initialization

```c
#include <stdio.h>

int main() {
    // Different ways to declare strings
    char str1[20] = "Hello";           // Array with explicit size
    char str2[] = "World";             // Size inferred from string
    char str3[10] = {'H', 'i', '\0'};  // Character by character
    char str4[50];                     // Uninitialized string
    
    printf("str1: %s\n", str1);  // Hello
    printf("str2: %s\n", str2);  // World
    printf("str3: %s\n", str3);  // Hi
    
    return 0;
}
```

### String Input and Output

```c
#include <stdio.h>

int main() {
    char name[50];
    char message[100];
    
    // Reading strings
    printf("Enter your name: ");
    scanf("%s", name);  // Reads until whitespace
    
    printf("Enter a message: ");
    getchar();  // Consume newline from previous input
    fgets(message, sizeof(message), stdin);  // Safer for strings with spaces
    
    printf("Hello, %s!\n", name);
    printf("Your message: %s", message);
    
    return 0;
}
```

### String Library Functions

Include `<string.h>` to use these functions:

```c
#include <stdio.h>
#include <string.h>

int main() {
    char str1[50] = "Hello";
    char str2[50] = "World";
    char str3[100];
    
    // String length
    printf("Length of str1: %lu\n", strlen(str1));  // 5
    
    // String copy
    strcpy(str3, str1);
    printf("str3 after copy: %s\n", str3);  // Hello
    
    // String concatenation
    strcat(str1, " ");
    strcat(str1, str2);
    printf("Concatenated: %s\n", str1);  // Hello World
    
    // String comparison
    if (strcmp(str2, "World") == 0) {
        printf("str2 equals 'World'\n");
    }
    
    return 0;
}
```

### Safe String Functions

```c
#include <stdio.h>
#include <string.h>

int main() {
    char dest[20];
    char src[] = "This is a long string";
    
    // Safe copy with size limit
    strncpy(dest, src, sizeof(dest) - 1);
    dest[sizeof(dest) - 1] = '\0';  // Ensure null termination
    
    printf("Safely copied: %s\n", dest);
    
    // Safe concatenation
    char greeting[50] = "Hello, ";
    strncat(greeting, "World!", sizeof(greeting) - strlen(greeting) - 1);
    
    printf("Safe concatenation: %s\n", greeting);
    
    return 0;
}
```

### String Manipulation Examples

```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Function to convert string to uppercase
void toUpperCase(char str[]) {
    for (int i = 0; str[i] != '\0'; i++) {
        str[i] = toupper(str[i]);
    }
}

// Function to reverse a string
void reverseString(char str[]) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = temp;
    }
}

// Function to count words in a string
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
    
    printf("Original: %s\n", text);
    
    toUpperCase(copy);
    printf("Uppercase: %s\n", copy);
    
    strcpy(copy, text);
    reverseString(copy);
    printf("Reversed: %s\n", copy);
    
    printf("Word count: %d\n", countWords(text));
    
    return 0;
}
```

## Common Pitfalls and Best Practices

### Array Bounds

```c
#include <stdio.h>

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    
    // WRONG: Array index out of bounds
    // arr[5] = 10;  // Undefined behavior!
    
    // CORRECT: Stay within bounds
    for (int i = 0; i < 5; i++) {
        printf("%d ", arr[i]);
    }
    
    return 0;
}
```

### String Buffer Overflow

```c
#include <stdio.h>
#include <string.h>

int main() {
    char buffer[10];
    
    // WRONG: Potential buffer overflow
    // strcpy(buffer, "This string is too long");
    
    // CORRECT: Use safe functions
    strncpy(buffer, "Safe", sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
    
    printf("Safe string: %s\n", buffer);
    
    return 0;
}
```

### Best Practices

1. **Always check array bounds** when accessing elements
2. **Use safe string functions** like `strncpy()`, `strncat()`, `snprintf()`
3. **Initialize arrays** to avoid garbage values
4. **Null-terminate strings** manually when using character arrays
5. **Use `const` for read-only arrays** passed to functions
6. **Consider using `size_t`** for array indices and sizes

```c
#include <stdio.h>
#include <string.h>

// Good practice: const for read-only arrays
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

Arrays and strings form the foundation of data manipulation in C. Master these concepts, and you'll be well-equipped to handle more complex data structures and algorithms!
