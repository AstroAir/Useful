# Memory Management in C

Memory management is a critical aspect of C programming. Unlike higher-level languages, C gives you direct control over memory allocation and deallocation, which provides power but also responsibility.

## Types of Memory

### Stack Memory

Stack memory is automatically managed and used for:

- Local variables
- Function parameters
- Return addresses

```c
#include <stdio.h>

void stackExample() {
    int localVar = 10;        // Allocated on stack
    char buffer[100];         // Allocated on stack
    
    printf("Local variable: %d\n", localVar);
    // Memory automatically freed when function ends
}

int main() {
    stackExample();
    // localVar and buffer are no longer accessible
    return 0;
}
```

### Heap Memory

Heap memory is manually managed and used for:

- Dynamic allocation
- Large data structures
- Data that needs to persist beyond function scope

## Dynamic Memory Allocation

### malloc() - Memory Allocation

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // Allocate memory for 10 integers
    int *ptr = malloc(10 * sizeof(int));
    
    // Always check if allocation succeeded
    if (ptr == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }
    
    // Use the allocated memory
    for (int i = 0; i < 10; i++) {
        ptr[i] = i * i;
    }
    
    // Print values
    printf("Squares: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", ptr[i]);
    }
    printf("\n");
    
    // Free the memory
    free(ptr);
    ptr = NULL;  // Good practice
    
    return 0;
}
```

### calloc() - Cleared Allocation

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // Allocate and initialize to zero
    int *ptr = calloc(5, sizeof(int));
    
    if (ptr == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }
    
    printf("Initialized values: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", ptr[i]);  // All zeros
    }
    printf("\n");
    
    free(ptr);
    return 0;
}
```

### realloc() - Resize Allocation

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // Initial allocation
    int *ptr = malloc(3 * sizeof(int));
    if (ptr == NULL) return 1;
    
    // Fill initial values
    for (int i = 0; i < 3; i++) {
        ptr[i] = i + 1;
    }
    
    // Resize to hold 6 integers
    ptr = realloc(ptr, 6 * sizeof(int));
    if (ptr == NULL) {
        printf("Reallocation failed\n");
        return 1;
    }
    
    // Fill new values
    for (int i = 3; i < 6; i++) {
        ptr[i] = i + 1;
    }
    
    printf("Resized array: ");
    for (int i = 0; i < 6; i++) {
        printf("%d ", ptr[i]);
    }
    printf("\n");
    
    free(ptr);
    return 0;
}
```

### free() - Memory Deallocation

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr = malloc(sizeof(int));
    
    if (ptr != NULL) {
        *ptr = 42;
        printf("Value: %d\n", *ptr);
        
        // Free the memory
        free(ptr);
        
        // Set to NULL to avoid dangling pointer
        ptr = NULL;
    }
    
    return 0;
}
```

## Dynamic Arrays

### Creating Dynamic Arrays

```c
#include <stdio.h>
#include <stdlib.h>

int* createArray(int size) {
    int *arr = malloc(size * sizeof(int));
    if (arr == NULL) {
        return NULL;
    }
    
    // Initialize array
    for (int i = 0; i < size; i++) {
        arr[i] = i * 2;
    }
    
    return arr;
}

int main() {
    int size = 5;
    int *dynamicArray = createArray(size);
    
    if (dynamicArray == NULL) {
        printf("Failed to create array\n");
        return 1;
    }
    
    printf("Dynamic array: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", dynamicArray[i]);
    }
    printf("\n");
    
    free(dynamicArray);
    return 0;
}
```

### Resizable Array Implementation

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
        // Resize array
        int newCapacity = arr->capacity * 2;
        int *newData = realloc(arr->data, newCapacity * sizeof(int));
        if (newData == NULL) return 0;  // Failed
        
        arr->data = newData;
        arr->capacity = newCapacity;
    }
    
    arr->data[arr->size++] = value;
    return 1;  // Success
}

void printArray(DynamicArray *arr) {
    printf("Array: ");
    for (int i = 0; i < arr->size; i++) {
        printf("%d ", arr->data[i]);
    }
    printf("(size: %d, capacity: %d)\n", arr->size, arr->capacity);
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
    
    // Add elements
    for (int i = 1; i <= 10; i++) {
        append(arr, i * 10);
        printArray(arr);
    }
    
    destroyArray(arr);
    return 0;
}
```

## Memory Management for Strings

### Dynamic String Allocation

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
    char *str1 = createString("Hello, ");
    char *str2 = createString("World!");
    
    if (str1 == NULL || str2 == NULL) {
        printf("String creation failed\n");
        return 1;
    }
    
    char *combined = concatenateStrings(str1, str2);
    if (combined == NULL) {
        printf("String concatenation failed\n");
        free(str1);
        free(str2);
        return 1;
    }
    
    printf("Combined: %s\n", combined);
    
    // Clean up
    free(str1);
    free(str2);
    free(combined);
    
    return 0;
}
```

## Common Memory Errors

### Memory Leaks

```c
#include <stdio.h>
#include <stdlib.h>

// BAD: Memory leak
void memoryLeak() {
    int *ptr = malloc(100 * sizeof(int));
    // Forgot to call free(ptr)!
    return;  // Memory is leaked
}

// GOOD: Proper cleanup
void properCleanup() {
    int *ptr = malloc(100 * sizeof(int));
    if (ptr == NULL) return;
    
    // Use the memory...
    
    free(ptr);  // Always free allocated memory
}

int main() {
    properCleanup();
    return 0;
}
```

### Double Free

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr = malloc(sizeof(int));
    
    if (ptr != NULL) {
        *ptr = 42;
        free(ptr);
        
        // BAD: Double free
        // free(ptr);  // Undefined behavior!
        
        // GOOD: Set to NULL after free
        ptr = NULL;
        
        // Now safe to call free again (does nothing)
        free(ptr);
    }
    
    return 0;
}
```

### Use After Free

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr = malloc(sizeof(int));
    
    if (ptr != NULL) {
        *ptr = 42;
        printf("Before free: %d\n", *ptr);
        
        free(ptr);
        
        // BAD: Use after free
        // printf("After free: %d\n", *ptr);  // Undefined behavior!
        
        // GOOD: Set to NULL and check
        ptr = NULL;
        if (ptr != NULL) {
            printf("Safe to use: %d\n", *ptr);
        }
    }
    
    return 0;
}
```

## Memory Debugging Tools

### Manual Debugging

```c
#include <stdio.h>
#include <stdlib.h>

// Simple memory tracking
static int allocations = 0;

void* debug_malloc(size_t size) {
    void *ptr = malloc(size);
    if (ptr != NULL) {
        allocations++;
        printf("Allocated %zu bytes at %p (total: %d)\n", 
               size, ptr, allocations);
    }
    return ptr;
}

void debug_free(void *ptr) {
    if (ptr != NULL) {
        allocations--;
        printf("Freed memory at %p (remaining: %d)\n", 
               ptr, allocations);
        free(ptr);
    }
}

int main() {
    int *ptr1 = debug_malloc(sizeof(int));
    int *ptr2 = debug_malloc(10 * sizeof(int));
    
    debug_free(ptr1);
    debug_free(ptr2);
    
    printf("Final allocations: %d\n", allocations);
    return 0;
}
```

## Best Practices

### Memory Management Guidelines

```c
#include <stdio.h>
#include <stdlib.h>

// Good practice: Check allocation and handle errors
int* safeAllocate(int count) {
    int *ptr = malloc(count * sizeof(int));
    if (ptr == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    return ptr;
}

// Good practice: Wrapper for safe free
void safeFree(void **ptr) {
    if (ptr != NULL && *ptr != NULL) {
        free(*ptr);
        *ptr = NULL;
    }
}

int main() {
    int *array = safeAllocate(10);
    
    // Use the array...
    for (int i = 0; i < 10; i++) {
        array[i] = i;
    }
    
    // Safe cleanup
    safeFree((void**)&array);
    
    // array is now NULL, safe to use in conditions
    if (array != NULL) {
        printf("Array is still valid\n");
    } else {
        printf("Array has been freed\n");
    }
    
    return 0;
}
```

### Key Rules

1. **Always check malloc return value**
2. **Match every malloc with exactly one free**
3. **Set pointers to NULL after freeing**
4. **Don't access freed memory**
5. **Don't free the same memory twice**
6. **Free memory in reverse order of allocation when possible**

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // Rule 1: Always check malloc
    int *ptr = malloc(sizeof(int));
    if (ptr == NULL) {
        return 1;
    }
    
    // Rule 2: Use the memory
    *ptr = 42;
    
    // Rule 3: Free exactly once
    free(ptr);
    
    // Rule 4: Set to NULL
    ptr = NULL;
    
    // Rule 5: Safe to check and use
    if (ptr != NULL) {
        printf("Value: %d\n", *ptr);
    }
    
    return 0;
}
```

Proper memory management is essential for writing robust C programs. Follow these practices to avoid common pitfalls and create efficient, reliable software!
