# Getting Started with C Language: Day 4 - Basic Data Types and Arrays

## Introduction

In C programming, understanding the type system is the cornerstone of building reliable programs. The type system not only determines how data is stored in memory but also affects program performance and security. This chapter systematically explains C's type system, type conversion mechanisms, and the usage of arrays and strings, helping you build a solid foundation through clear examples.

## Type System

C is a strongly typed language, meaning each variable must have its data type explicitly specified before use. Data types determine the range of values a variable can store, memory footprint, and operations that can be performed. Understanding the type system is crucial for writing efficient and secure C programs.

### Basic Data Types

#### Integer Types

C provides various integer types to accommodate different ranges of integer values. Note that the specific sizes of these integer types depend on the compiler and target platform; the following are common implementations:

- `int`: Standard integer type, typically occupies 4 bytes (32-bit systems)
- `short`: Short integer type, typically occupies 2 bytes
- `long`: Long integer type, typically occupies 4 or 8 bytes
- `long long`: Extended integer type, typically occupies 8 bytes

```c
int age = 25;                // Standard integer type
short year = 2022;           // Short integer type
long population = 8000000L;  // Long integer type (L suffix denotes long type)
long long distance = 12345678901234LL; // Extended integer type (LL suffix)
```

#### Character Type

The `char` type stores single characters and occupies 1 byte of memory. In C, characters are essentially integers corresponding to ASCII codes.

```c
char letter = 'A';  // Stores character 'A'
char numChar = 65;  // Also stores 'A' (ASCII code 65)
```

#### Floating Point Types

Floating point types represent values with decimal parts:

- `float`: Single-precision floating point, typically occupies 4 bytes
- `double`: Double-precision floating point, typically occupies 8 bytes
- `long double`: Extended-precision floating point, typically occupies 12 or 16 bytes

```c
float pi = 3.14f;  // f suffix denotes float type
double e = 2.718281828459045; // Default is double type
```

#### Enumerated Types

Enumerated types allow meaningful names for integer constants, improving code readability:

```c
enum Day { SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY };
enum Day today = WEDNESDAY; // today's value is 3
```

#### Void Type

The `void` type represents "no type" and is primarily used for:

- Function return type when no value is returned
- Pointers to arbitrary data types (`void*`)

```c
void printMessage() {
    printf("Hello, C Programming!\n");
    // No return statement or return; indicates function completion
}
```

> **Important Note**: C requires functions that don't return values to explicitly declare their return type as `void`. Omitting the return type may cause compilation errors.

#### Pointer Types

Pointers are a core feature of C, used to store memory addresses. A pointer's type determines the data type it points to:

```c
int x = 10;
int *ptr = &x;  // ptr is a pointer to an integer, storing x's address
```

### Type Conversion

When mixing different data types in expressions, C provides two type conversion mechanisms:

#### Implicit Type Conversion (Automatic Conversion)

When expressions contain operands of different types, the compiler automatically converts "narrower" types to "wider" types to prevent data loss:

```c
int a = 5;
double b = 3.2;
double result = a + b; // a is automatically converted to double type
```

Implicit conversion follows this priority order (from lowest to highest):
`char` → `short` → `int` → `unsigned int` → `long` → `unsigned long` → `float` → `double` → `long double`

#### Explicit Type Conversion (Casting)

When converting "wider" types to "narrower" types or for specific type interpretation, explicit casting is required:

```c
double pi = 3.14159;
int truncated_pi = (int)pi; // Convert double to int, result is 3
```

> **Important Notes**:
>
> 1. Casting may cause data loss (e.g., converting floating-point to integer truncates decimal part)
> 2. Pointer type casting requires extra caution; incorrect casting may lead to undefined behavior
> 3. Converting from larger-range types to smaller-range types may cause overflow issues

### Practical Examples

#### Integer and Floating-Point Mixed Operations

```c
#include <stdio.h>

int main() {
    int apples = 10;
    double price = 1.5;
    double total_cost = apples * price; // apples automatically converted to double
    printf("Total cost: $%.2f\n", total_cost);
    return 0;
}
```

#### Pointer Type Conversion

```c
#include <stdio.h>

int main() {
    int a = 42;
    void *ptr = &a;      // Generic pointer can point to any type
    int *int_ptr = (int *)ptr; // Convert back to original type
    printf("Value of a: %d\n", *int_ptr);
    return 0;
}
```

## Arrays

When handling multiple data items of the same type, arrays provide an efficient solution. Arrays store elements contiguously in memory, supporting fast access via indices.

### One-Dimensional Arrays

#### Definition and Initialization

```c
int scores[5]; // Define array containing 5 integers

// Full initialization
int values[5] = {85, 90, 78, 92, 88};

// Partial initialization (unspecified elements automatically initialized to 0)
int partial[5] = {1, 2}; // Equivalent to {1, 2, 0, 0, 0}

// Automatic size deduction
int autoSize[] = {10, 20, 30}; // Size is 3
```

#### Accessing Elements

Array indices start at 0, a common source of errors for beginners:

```c
int first = values[0]; // Get first element
values[2] = 85;        // Modify third element
```

> **Important Note**: C does not check array boundaries; out-of-bounds access may cause serious errors (such as segmentation faults).

### Multi-Dimensional Arrays

#### Two-Dimensional Arrays

Two-dimensional arrays can be viewed as "arrays of arrays," commonly used to represent matrices or tabular data:

```c
// Define 3-row, 4-column two-dimensional array
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

// Access element
int element = matrix[1][2]; // Get element at row 2, column 3 (value is 7)
```

In memory, two-dimensional arrays are stored in **row-major** order: all elements of the first row are stored first, followed by the second row, and so on.

### Relationship Between Pointers and Arrays

In C, array names are treated as pointers to their first element in most expressions:

```c
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr; // p points to arr[0]

printf("%d\n", *(p + 2)); // Outputs 3 (equivalent to arr[2])
```

#### Pointer Arrays vs. Array Pointers

- **Pointer Array**: Array elements are pointers

  ```c
  char *names[3] = {"Alice", "Bob", "Charlie"};
  ```

- **Array Pointer**: Pointer to an array

  ```c
  int arr[5] = {1, 2, 3, 4, 5};
  int (*p)[5] = &arr; // p points to an array of 5 integers
  ```

### Dynamic Arrays

When array size can only be determined at runtime, dynamic memory allocation can be used:

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int size = 5;
    int *dynamicArr = (int *)malloc(size * sizeof(int));
    
    if (dynamicArr == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }
    
    // Use array
    for (int i = 0; i < size; i++) {
        dynamicArr[i] = i * 2;
    }
    
    // Free memory
    free(dynamicArr);
    return 0;
}
```

> **Memory Management Tips**:
>
> 1. Dynamically allocated memory must be manually freed (`free`)
> 2. Use `realloc` to adjust the size of already allocated memory
> 3. Avoid memory leaks (allocated but not freed) and dangling pointers (using after freeing)

## Strings

In C, strings are special character arrays terminated by a null character `\0`.

### String Representation

```c
char greeting[] = "Hello"; // Automatically adds \0, actual size is 6 bytes
char *message = "World";   // Pointer to string literal
```

> **Key Difference**:
>
> - Array form (`greeting`): Content can be modified at runtime
> - Pointer form (`message`): Typically points to read-only memory; modification leads to undefined behavior

### Common String Operations

The standard library `<string.h>` provides rich string processing functions:

```c
#include <stdio.h>
#include <string.h>

int main() {
    char src[] = "Hello";
    char dest[20];
    
    // Copy string
    strcpy(dest, src);
    
    // Concatenate strings
    strcat(dest, ", World!");
    
    // Get length (excluding \0)
    int len = strlen(dest);
    
    // Compare strings
    int cmp = strcmp("apple", "banana");
    
    printf("Result: %s (length: %d)\n", dest, len);
    printf("Comparison result: %d\n", cmp);
    
    return 0;
}
```

### String Operation Considerations

1. **Buffer Overflow**: Ensure destination array is large enough

   ```c
   char small[5];
   strcpy(small, "Hello"); // Dangerous! Causes buffer overflow
   ```

2. **Null Character `\0`**: Must exist to properly mark string end

3. **String Literals**: Should not be modified

   ```c
   char *str = "Hello";
   str[0] = 'h'; // Illegal operation, may cause program crash
   ```

### Practical String Examples

#### String Reversal

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

#### Palindrome Check

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

## Summary and Best Practices

1. **Type Selection**: Choose appropriate data types based on data range and precision requirements
2. **Type Conversion**: Use explicit casting cautiously to avoid data loss
3. **Array Usage**:
   - Always be mindful of array boundaries to prevent out-of-bounds access
   - Manually manage memory for dynamic arrays
   - Understand the relationship between pointers and arrays
4. **String Handling**:
   - Ensure buffers are sufficiently large
   - Always terminate with `\0`
   - Prefer safer string functions (e.g., `strncpy` instead of `strcpy`)

> **Programming Wisdom**: C grants programmers powerful control but demands greater responsibility. Understanding the type system and memory management is key to writing robust C programs.
