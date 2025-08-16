# Pointers in C

Pointers are one of the most powerful and distinctive features of C programming. They provide direct access to memory addresses, enabling efficient memory management and advanced programming techniques.

## What are Pointers?

A pointer is a variable that stores the memory address of another variable. Instead of holding a value directly, a pointer "points to" the location where the value is stored.

### Basic Pointer Concepts

```c
#include <stdio.h>

int main() {
    int num = 42;        // Regular variable
    int *ptr = &num;     // Pointer to int, stores address of num
    
    printf("Value of num: %d\n", num);           // 42
    printf("Address of num: %p\n", &num);        // Memory address
    printf("Value of ptr: %p\n", ptr);          // Same as &num
    printf("Value pointed by ptr: %d\n", *ptr);  // 42 (dereferencing)
    
    return 0;
}
```

### Key Operators

- **Address-of operator (`&`)**: Gets the address of a variable
- **Dereference operator (`*`)**: Accesses the value at the address stored in a pointer

## Pointer Declaration and Initialization

### Declaration Syntax

```c
int *ptr;        // Pointer to int
float *fptr;     // Pointer to float
char *cptr;      // Pointer to char
double *dptr;    // Pointer to double
```

### Initialization

```c
#include <stdio.h>

int main() {
    int x = 10;
    
    // Method 1: Declare and initialize separately
    int *ptr1;
    ptr1 = &x;
    
    // Method 2: Declare and initialize together
    int *ptr2 = &x;
    
    // Method 3: Initialize to NULL
    int *ptr3 = NULL;
    
    printf("x = %d\n", x);
    printf("*ptr1 = %d\n", *ptr1);
    printf("*ptr2 = %d\n", *ptr2);
    
    // Always check for NULL before dereferencing
    if (ptr3 != NULL) {
        printf("*ptr3 = %d\n", *ptr3);
    } else {
        printf("ptr3 is NULL\n");
    }
    
    return 0;
}
```

## Pointer Arithmetic

Pointers support arithmetic operations that are scaled by the size of the data type they point to.

```c
#include <stdio.h>

int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int *ptr = arr;  // Points to first element
    
    printf("Array elements using pointer arithmetic:\n");
    for (int i = 0; i < 5; i++) {
        printf("arr[%d] = %d, *(ptr + %d) = %d\n", 
               i, arr[i], i, *(ptr + i));
    }
    
    // Moving pointer
    printf("\nMoving pointer through array:\n");
    ptr = arr;
    for (int i = 0; i < 5; i++) {
        printf("*ptr = %d, address = %p\n", *ptr, ptr);
        ptr++;  // Move to next element
    }
    
    return 0;
}
```

### Pointer Arithmetic Operations

```c
#include <stdio.h>

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    int *ptr1 = &arr[1];  // Points to arr[1]
    int *ptr2 = &arr[4];  // Points to arr[4]
    
    // Pointer subtraction
    printf("Difference between ptr2 and ptr1: %ld\n", ptr2 - ptr1);  // 3
    
    // Pointer comparison
    if (ptr2 > ptr1) {
        printf("ptr2 points to a later element than ptr1\n");
    }
    
    // Increment and decrement
    ptr1++;  // Now points to arr[2]
    printf("After increment, *ptr1 = %d\n", *ptr1);  // 3
    
    ptr1--;  // Back to arr[1]
    printf("After decrement, *ptr1 = %d\n", *ptr1);  // 2
    
    return 0;
}
```

## Pointers and Arrays

Arrays and pointers are closely related in C. An array name is essentially a pointer to its first element.

```c
#include <stdio.h>

void printArray(int *arr, int size) {
    printf("Array elements: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);  // or *(arr + i)
    }
    printf("\n");
}

int main() {
    int numbers[] = {10, 20, 30, 40, 50};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    
    // Array name as pointer
    printf("First element: %d\n", *numbers);        // 10
    printf("Second element: %d\n", *(numbers + 1)); // 20
    
    // Passing array to function
    printArray(numbers, size);
    
    // Pointer to array
    int *ptr = numbers;
    printf("Using pointer: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", ptr[i]);
    }
    printf("\n");
    
    return 0;
}
```

## Pointers and Strings

Strings in C are arrays of characters, so pointers work naturally with strings.

```c
#include <stdio.h>
#include <string.h>

int main() {
    char str[] = "Hello, World!";
    char *ptr = str;
    
    // Printing string using pointer
    printf("String: %s\n", ptr);
    
    // Character by character using pointer
    printf("Characters: ");
    while (*ptr != '\0') {
        printf("%c", *ptr);
        ptr++;
    }
    printf("\n");
    
    // String literals and pointers
    char *message = "Programming";  // Points to string literal
    printf("Message: %s\n", message);
    
    // Note: String literals are read-only
    // message[0] = 'p';  // This would cause undefined behavior
    
    return 0;
}
```

### String Functions with Pointers

```c
#include <stdio.h>

// Custom strlen implementation
int myStrlen(char *str) {
    int length = 0;
    while (*str != '\0') {
        length++;
        str++;
    }
    return length;
}

// Custom strcpy implementation
void myStrcpy(char *dest, char *src) {
    while (*src != '\0') {
        *dest = *src;
        dest++;
        src++;
    }
    *dest = '\0';  // Add null terminator
}

int main() {
    char source[] = "Hello";
    char destination[20];
    
    printf("Length of '%s': %d\n", source, myStrlen(source));
    
    myStrcpy(destination, source);
    printf("Copied string: %s\n", destination);
    
    return 0;
}
```

## Pointers to Pointers

A pointer can point to another pointer, creating multiple levels of indirection.

```c
#include <stdio.h>

int main() {
    int num = 42;
    int *ptr = &num;        // Pointer to int
    int **pptr = &ptr;      // Pointer to pointer to int
    
    printf("Value of num: %d\n", num);
    printf("Value via ptr: %d\n", *ptr);
    printf("Value via pptr: %d\n", **pptr);
    
    printf("Address of num: %p\n", &num);
    printf("Value of ptr: %p\n", ptr);
    printf("Address of ptr: %p\n", &ptr);
    printf("Value of pptr: %p\n", pptr);
    
    // Modifying value through double pointer
    **pptr = 100;
    printf("Modified value: %d\n", num);
    
    return 0;
}
```

## Function Pointers

Pointers can also point to functions, enabling dynamic function calls and callback mechanisms.

```c
#include <stdio.h>

// Function prototypes
int add(int a, int b);
int multiply(int a, int b);
int calculate(int x, int y, int (*operation)(int, int));

int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

int calculate(int x, int y, int (*operation)(int, int)) {
    return operation(x, y);
}

int main() {
    int (*funcPtr)(int, int);  // Function pointer declaration
    
    // Point to add function
    funcPtr = add;
    printf("5 + 3 = %d\n", funcPtr(5, 3));
    
    // Point to multiply function
    funcPtr = multiply;
    printf("5 * 3 = %d\n", funcPtr(5, 3));
    
    // Using function pointers as parameters
    printf("Calculate add: %d\n", calculate(10, 5, add));
    printf("Calculate multiply: %d\n", calculate(10, 5, multiply));
    
    return 0;
}
```

## Pointers and Structures

Pointers work with structures to enable efficient data manipulation and dynamic data structures.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Person {
    char name[50];
    int age;
    float height;
};

void printPerson(struct Person *p) {
    printf("Name: %s\n", p->name);      // Arrow operator
    printf("Age: %d\n", p->age);
    printf("Height: %.1f\n", p->height);
}

int main() {
    struct Person person1 = {"Alice", 25, 165.5};
    struct Person *ptr = &person1;
    
    // Accessing structure members through pointer
    printf("Using arrow operator:\n");
    printPerson(ptr);
    
    // Alternative syntax using dereference
    printf("\nUsing dereference operator:\n");
    printf("Name: %s\n", (*ptr).name);
    printf("Age: %d\n", (*ptr).age);
    
    // Dynamic allocation
    struct Person *dynamicPerson = malloc(sizeof(struct Person));
    strcpy(dynamicPerson->name, "Bob");
    dynamicPerson->age = 30;
    dynamicPerson->height = 175.0;
    
    printf("\nDynamically allocated person:\n");
    printPerson(dynamicPerson);
    
    free(dynamicPerson);  // Don't forget to free memory
    
    return 0;
}
```

## Common Pointer Pitfalls

### Null Pointer Dereference

```c
#include <stdio.h>

int main() {
    int *ptr = NULL;
    
    // WRONG: Dereferencing NULL pointer
    // printf("%d\n", *ptr);  // Segmentation fault!
    
    // CORRECT: Check before dereferencing
    if (ptr != NULL) {
        printf("Value: %d\n", *ptr);
    } else {
        printf("Pointer is NULL\n");
    }
    
    return 0;
}
```

### Dangling Pointers

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr = malloc(sizeof(int));
    *ptr = 42;
    
    printf("Value: %d\n", *ptr);
    
    free(ptr);      // Memory freed
    ptr = NULL;     // GOOD: Set to NULL to avoid dangling pointer
    
    // WRONG: Using freed memory
    // printf("%d\n", *ptr);  // Undefined behavior!
    
    // CORRECT: Check for NULL
    if (ptr != NULL) {
        printf("Value: %d\n", *ptr);
    } else {
        printf("Pointer is NULL\n");
    }
    
    return 0;
}
```

### Memory Leaks

```c
#include <stdio.h>
#include <stdlib.h>

void memoryLeakExample() {
    int *ptr = malloc(sizeof(int) * 100);
    // WRONG: Forgetting to free memory
    // return;  // Memory leak!
    
    // CORRECT: Always free allocated memory
    free(ptr);
}

int main() {
    memoryLeakExample();
    printf("Function completed without memory leak\n");
    return 0;
}
```

## Best Practices

1. **Always initialize pointers** to NULL or a valid address
2. **Check for NULL** before dereferencing pointers
3. **Set pointers to NULL** after freeing memory
4. **Match every malloc with free**
5. **Use const for read-only data**
6. **Avoid pointer arithmetic on non-array pointers**

```c
#include <stdio.h>
#include <stdlib.h>

// Good practice: const for read-only data
void printString(const char *str) {
    printf("String: %s\n", str);
    // str[0] = 'X';  // Compiler error - good!
}

int main() {
    // Good practice: Initialize to NULL
    int *ptr = NULL;
    
    // Allocate memory
    ptr = malloc(sizeof(int));
    if (ptr == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }
    
    *ptr = 42;
    printf("Value: %d\n", *ptr);
    
    // Good practice: Free and nullify
    free(ptr);
    ptr = NULL;
    
    // Good practice: Use const for strings
    char message[] = "Hello, World!";
    printString(message);
    
    return 0;
}
```

Pointers are a powerful feature that enables efficient memory management, dynamic data structures, and advanced programming techniques. Master them, and you'll unlock the full potential of C programming!
