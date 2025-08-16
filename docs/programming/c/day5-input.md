
# Getting Started with C: Day 5 - Standard Input

## Introduction

In the C language, input refers to the process of obtaining data from users, files, or other external sources and storing it into program variables. C provides various input methods suitable for different scenarios: from simple keyboard input to complex file processing. This chapter systematically introduces these input methods to help you master how to safely and effectively obtain the data your program needs.

## Standard Input Functions

### `scanf`: The Basic Tool for Formatted Input

`scanf` is the most commonly used input function in C, used to read formatted data from standard input (typically the keyboard).

```c
int scanf(const char *format, ...);
```

- **format**: Format string specifying the data types to read (e.g., `"%d"` for integers, `"%f"` for floating-point numbers).
- **Return value**: Number of variables successfully read; returns `EOF` if end-of-file or read error is encountered.

**Example:**

```c
#include <stdio.h>

int main() {
    int num;
    float f;

    printf("Please enter an integer and a floating-point number: ");
    scanf("%d %f", &num, &f);  // & takes the variable address so scanf can modify the variable

    printf("You entered: %d and %.2f\n", num, f);
    return 0;
}
```

**Key Notes:**

- Must use `&` to pass variable addresses; otherwise, the program may crash.
- `scanf` automatically skips whitespace characters (spaces, newlines, tabs) in input, but multiple input items must be separated by spaces.
- **Format matching issues**: If input doesn't match the format string (e.g., entering letters when integers are expected), it may cause read failures or subsequent input anomalies.

> **Tip**: Beginners often get confused due to mismatches between format strings and input. It's recommended to practice with simple examples first and gradually become familiar with common format specifiers.

### `fscanf`: Reading Formatted Data from Files

`fscanf` functions similarly to `scanf`, but is used to read data from file streams.

```c
int fscanf(FILE *stream, const char *format, ...);
```

- **stream**: File pointer specifying the data source (e.g., a file opened via `fopen`).

**Example:**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("File opening failed!\n");
        return 1;
    }

    int num;
    fscanf(file, "%d", &num);  // Read integer from file
    printf("Number in file: %d\n", num);

    fclose(file);  // Always close the file to avoid resource leaks
    return 0;
}
```

**Usage Notes:**

- Must check if `fopen` succeeded before file operations.
- After using a file, **you must call `fclose` to close it**, otherwise data loss or resource occupation may occur.

### `sscanf`: Parsing Data from Strings

`sscanf` is used to extract formatted data from strings, suitable for parsing existing text content.

```c
int sscanf(const char *str, const char *format, ...);
```

- **str**: String to be parsed.

**Example:**

```c
#include <stdio.h>

int main() {
    char input[] = "42 3.14";
    int num;
    float f;

    sscanf(input, "%d %f", &num, &f);  // Extract data from string
    printf("Parsing result: %d and %.2f\n", num, f);

    return 0;
}
```

## Character Input Functions

### `getchar`: Single Character Input

`getchar` reads a **single character** from standard input, with a return type of `int` (to be compatible with `EOF`).

```c
int getchar(void);
```

**Example:**

```c
#include <stdio.h>

int main() {
    char c;

    printf("Please enter a character: ");
    c = getchar();  // Read a character (including spaces and newline)

    printf("You entered: %c\n", c);
    return 0;
}
```

**Key Features:**

- Does not skip whitespace characters; spaces or newlines entered will also be read.
- Return value is `int`, which needs to be converted to `char` for use (e.g., `c = (char)getchar()`).

### `fgetc` and `getc`: File Character Reading

Both are used to read single characters from file streams, with the difference being that `getc` is typically implemented as a macro (which may evaluate parameters multiple times), while `fgetc` is a standard function.

```c
int fgetc(FILE *stream);
int getc(FILE *stream);
```

**Example:**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("File opening failed!\n");
        return 1;
    }

    int c;  // Must store with int to be compatible with EOF
    while ((c = fgetc(file)) != EOF) {
        putchar(c);  // Output character by character
    }

    fclose(file);
    return 0;
}
```

**Usage Recommendations:**

- Prefer `fgetc` to avoid potential side effects of `getc`.
- Store return value in `int` to correctly identify `EOF`.

### `ungetc`: Pushing Back Input Characters

`ungetc` "pushes back" a character into the input stream, making it the target of the next read operation. Often used in parsing scenarios where pre-reading characters is needed.

```c
int ungetc(int c, FILE *stream);
```

**Example:**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("File opening failed!\n");
        return 1;
    }

    int c = fgetc(file);
    if (c != EOF) {
        ungetc(c, file);  // Push character back into stream
        c = fgetc(file);  // Read the same character again
        printf("Re-read character: %c\n", c);
    }

    fclose(file);
    return 0;
}
```

**Important Limitations:**

- The standard only guarantees the ability to push back **one character**; behavior of multiple `ungetc` calls is undefined.
- The pushed-back character must be compatible with the stream's encoding (e.g., binary data cannot be pushed back in text mode).

## Line Input Functions

### `fgets`: Safe Line Reading (Recommended)

`fgets` is used to read entire lines of input and **effectively prevents buffer overflow**, making it a safe alternative to `gets`.

```c
char *fgets(char *str, int n, FILE *stream);
```

- **str**: Buffer to store input.
- **n**: Maximum number of characters to read (including terminating `\0`).
- **stream**: Input stream (`stdin` represents keyboard input).

**Example:**

```c
#include <stdio.h>
#include <string.h>  // For strcspn

int main() {
    char str[100];

    printf("Please enter some text: ");
    if (fgets(str, sizeof(str), stdin) != NULL) {
        // Remove possible newline character
        str[strcspn(str, "\n")] = '\0';
        printf("You entered: %s\n", str);
    } else {
        printf("Input reading failed!\n");
    }

    return 0;
}
```

**Key Advantages:**

- Limits input length through the `n` parameter, preventing buffer overflow.
- Retains newline character `\n` (needs manual removal, as shown in the example).

> **Why not use `gets`?**  
> `gets` has been removed from the C11 standard because it cannot limit input length. **It is strongly recommended to always use `fgets` instead of `gets`**.

## File and System-Level Input

### `fread`: Binary Data Reading

`fread` is used to read raw data blocks, suitable for handling binary files (e.g., images, custom format files).

```c
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);
```

**Example:**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("data.bin", "rb");
    if (file == NULL) {
        printf("File opening failed!\n");
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

**Usage Notes:**

- Suitable for files opened in binary mode (`"rb"`).
- Check the return value `count` to ensure the expected number of data blocks were read.

### `read` (System Call): Low-Level Data Reading

`read` is a POSIX system call used to directly manipulate file descriptors, **not a standard C library function**, typically used in system programming.

```c
ssize_t read(int fd, void *buf, size_t count);
```

> **Note**: This function belongs to the operating system API and has low portability. Beginners are advised to prioritize standard library functions (e.g., `fread`).

## Secure Input Extension: `scanf_s`

`scanf_s` is a secure version provided by Microsoft Visual Studio, preventing overflow by requiring buffer size specifications.

```c
int scanf_s(const char *format, ...);
```

**Example:**

```c
#include <stdio.h>

int main() {
    char buffer[10];
    int num;

    printf("Please enter a number and string: ");
    scanf_s("%d %9s", &num, buffer, (unsigned)_countof(buffer));

    printf("You entered: %d and %s\n", num, buffer);
    return 0;
}
```

**Important Notes:**

- **Non-standard function**: Supported only by some compilers (e.g., MSVC); GCC/Clang require specific extensions.
- String input requires specifying buffer size (e.g., `9` in `%9s` means read at most 9 characters).

## Summary and Best Practices

| **Input Type**       | **Recommended Function** | **Use Case**                     | **Notes**                              |
|----------------------|--------------------------|----------------------------------|----------------------------------------|
| Formatted Input      | `scanf`                  | Simple keyboard input            | Pay attention to format matching, avoid buffer overflow |
| Safe Line Input      | `fgets`                  | Reading user-entered text lines  | **Always prefer this**, manually handle newline characters |
| File Formatted Input | `fscanf`                 | Reading structured data from files | Check file open status, close files promptly |
| Character Processing | `fgetc`                  | Parsing files or input character by character | Store return value in `int` to identify `EOF` |
| Binary Data          | `fread`                  | Reading non-text files (e.g., images, data files) | Ensure buffer is large enough, check return value |

**Core Principles:**

1. **Safety First**: Avoid using `gets`; prioritize functions with length limits (e.g., `fgets`).
2. **Error Handling**: Always check return values of input functions and handle potential failures.
3. **Resource Management**: Files opened with `fopen` must be closed with `fclose` to prevent resource leaks.
4. **Portability**: Standard C functions (e.g., `fgets`) are more universal than platform extensions (e.g., `scanf_s`).

After mastering these input methods, you now have the ability to handle most C language input scenarios. The next chapter will teach you how to output data to screens or files, building complete input-output workflows!
