# Getting Started with C: Day 5.5 - Standard Output

## Introduction

In the C language, output refers to the process of sending data processed by a program to a display, file, or other external devices. Corresponding to input, C provides a rich set of output functions that help us present results to users, record program status, or save data to files. This chapter systematically introduces these output methods, enabling you to clearly and safely present program results to users or store them in external media.

## Standard Output Functions

### `printf`: The Core Tool for Formatted Output

`printf` is the most commonly used output function in C, used to send formatted data to standard output (typically the screen).

```c
int printf(const char *format, ...);
```

- **format**: Format string containing ordinary characters and format specifiers (e.g., `"%d"` for integers, `"%f"` for floating-point numbers).
- **Return value**: Number of characters successfully output; returns a negative value if an error occurs.

**Example:**

```c
#include <stdio.h>

int main() {
    int age = 25;
    float height = 175.5;
    char initial = 'J';

    printf("Name: Zhang%c\nAge: %d years\nHeight: %.1f cm\n", initial, age, height);
    return 0;
}
```

**Output:**

```txt
Name: ZhangJ
Age: 25 years
Height: 175.5 cm
```

**Key Features:**

- Format specifiers must correspond one-to-one with parameters; otherwise, undefined behavior may occur.
- Supports rich format controls, such as `%.2f` to control decimal places for floating-point numbers, `%10d` to specify minimum width, etc.
- Special characters require escaping: `\n` for newline, `\t` for tab, `%%` to output a percent sign.

> **Tip**: A common mistake for beginners is mismatching format specifiers with parameter types (e.g., using `%d` to output a floating-point number). It's recommended to practice with simple examples first and gradually master format control techniques.

### `fprintf`: Formatted Output to Files

`fprintf` functions similarly to `printf`, but is used to output data to file streams.

```c
int fprintf(FILE *stream, const char *format, ...);
```

- **stream**: File pointer specifying the output target (e.g., `stdout` for screen, `stderr` for standard error, or a file opened via `fopen`).

**Example:**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("output.txt", "w");
    if (file == NULL) {
        printf("File creation failed!\n");
        return 1;
    }

    int num = 42;
    fprintf(file, "Number in file: %d\n", num);  // Write to file
    printf("Data has been written to the file!\n");  // Display prompt on screen

    fclose(file);  // Always close the file
    return 0;
}
```

**Usage Notes:**

- Always check if `fopen` succeeded before file operations.
- After using a file, **you must call `fclose` to close it**, otherwise data may not be written or resources may leak.
- Can be used to output error messages to the standard error stream: `fprintf(stderr, "Error: File does not exist!\n");`

### `sprintf` and `snprintf`: Formatted Output to Strings

These functions output formatted data to string buffers instead of directly displaying or writing to files.

```c
int sprintf(char *str, const char *format, ...);
int snprintf(char *str, size_t size, const char *format, ...);
```

- **str**: Target string buffer.
- **size** (for `snprintf` only): Buffer size to prevent overflow.

**Example:**

```c
#include <stdio.h>

int main() {
    char buffer[50];
    int id = 1001;
    float score = 89.5;

    // sprintf does not check buffer size, risking overflow
    sprintf(buffer, "Student ID: %d, Score: %.1f", id, score);
    printf("Using sprintf: %s\n", buffer);

    // snprintf is the safer version, specifying maximum write length
    snprintf(buffer, sizeof(buffer), "Student ID: %04d, Score: %.1f", id, score);
    printf("Using snprintf: %s\n", buffer);

    return 0;
}
```

**Key Differences:**

- `sprintf` **does not check buffer size**, potentially causing buffer overflow; **not recommended**.
- `snprintf` limits write length via the `size` parameter; **always prefer this**.
- `snprintf`'s return value indicates "the number of characters that would have been written if the buffer were large enough," which can be used to detect truncation.

## Character Output Functions

### `putchar`: Single Character Output

`putchar` writes a **single character** to standard output.

```c
int putchar(int c);
```

- **c**: Character to output (passed as an `int` type).
- **Return value**: Returns the output character on success; returns `EOF` on failure.

**Example:**

```c
#include <stdio.h>

int main() {
    char text[] = "Hello, C!";
    int i = 0;

    while (text[i] != '\0') {
        putchar(text[i]);  // Output character by character
        i++;
    }
    putchar('\n');  // Output newline character

    return 0;
}
```

**Use Cases:**

- Implementing custom output logic (e.g., encrypted output, character conversion).
- Pairing with `getchar` to create simple character processing programs.

### `fputc` and `putc`: Output Single Character to File

Both functions are similar and used to write a single character to a file stream.

```c
int fputc(int c, FILE *stream);
int putc(int c, FILE *stream);
```

**Example:**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("chars.txt", "w");
    if (file == NULL) {
        printf("File creation failed!\n");
        return 1;
    }

    for (char c = 'A'; c <= 'Z'; c++) {
        fputc(c, file);  // Write uppercase letters
        fputc(' ', file); // Write space
    }
    fputc('\n', file);   // Write newline character

    fclose(file);
    printf("Alphabet has been written to the file!\n");
    return 0;
}
```

**Usage Recommendations:**

- Prefer `fputc` to avoid potential side effects from `putc` (macro implementation may evaluate parameters multiple times).
- Suitable for scenarios where file content is built character by character.

## Line Output Functions

### `puts`: Output String Line

`puts` writes a string to standard output and **automatically appends a newline character**.

```c
int puts(const char *str);
```

- **str**: String to output (null-terminated with `\0`).
- **Return value**: Returns a non-negative value on success; returns `EOF` on failure.

**Example:**

```c
#include <stdio.h>

int main() {
    char message[] = "Welcome to learn C!";
    puts(message);  // Output string with newline
    puts("This is the second line"); // Equivalent to printf("This is the second line\n");
    return 0;
}
```

**Features:**

- Simpler than `printf`, but **cannot format output**.
- **Automatically appends a newline character**, no need to manually add `\n`.
- Returns a non-negative value on success, `EOF` on failure.

### `fputs`: Output String Line to File

`fputs` is similar to `puts`, but used to output strings to file streams, and **does not automatically append a newline character**.

```c
int fputs(const char *str, FILE *stream);
```

**Example:**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("lines.txt", "w");
    if (file == NULL) {
        printf("File creation failed!\n");
        return 1;
    }

    fputs("First line content\n", file);  // Manually add newline character
    fputs("Second line content", file);   // No newline character added
    fputs("\n", file);                    // Add newline character separately

    fclose(file);
    printf("Text lines have been written to the file!\n");
    return 0;
}
```

**Key Differences:**

- `puts` is for standard output and automatically adds a newline; `fputs` is for any stream and **does not automatically add a newline**.
- `fputs` is more flexible, allowing control over whether to add a newline.

## File Output Functions

### `fwrite`: Binary Data Writing

`fwrite` is used to write raw data blocks to files, suitable for handling binary files (e.g., images, custom format files).

```c
size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream);
```

**Example:**

```c
#include <stdio.h>

int main() {
    FILE *file = fopen("data.bin", "wb");
    if (file == NULL) {
        printf("File creation failed!\n");
        return 1;
    }

    int numbers[] = {10, 20, 30, 40, 50};
    size_t count = fwrite(numbers, sizeof(int), 5, file);

    if (count != 5) {
        printf("Incomplete data write!\n");
    } else {
        printf("Successfully wrote %zu integers\n", count);
    }

    fclose(file);
    return 0;
}
```

**Usage Notes:**

- Suitable for files opened in binary mode (`"wb"`).
- Check the return value `count` to ensure the expected number of data blocks were written.
- Used with `fread`, it enables data serialization and deserialization.

## Low-Level Output

### `write` (System Call): Low-Level Data Writing

`write` is a POSIX system call used to directly manipulate file descriptors, **not a standard C library function**.

```c
ssize_t write(int fd, const void *buf, size_t count);
```

> **Note**: This function belongs to the operating system API and has low portability. Beginners are advised to prioritize standard library functions (e.g., `fwrite`).

## Secure Output Extension: `printf_s`

`printf_s` is a secure version provided by Microsoft Visual Studio, enhancing format checking to prevent security issues.

```c
int printf_s(const char *format, ...);
```

**Example:**

```c
#include <stdio.h>

int main() {
    char name[20] = "Zhang San";
    int age = 25;

    printf_s("Name: %s, Age: %d\n", name, age);
    return 0;
}
```

**Important Notes:**

- **Non-standard function**: Supported only by some compilers (e.g., MSVC); GCC/Clang require specific extensions.
- Provides additional security checks, such as detecting invalid format specifiers.
- Still requires matching format specifiers with parameters; cannot fully replace good programming practices.

## Summary and Best Practices

| **Output Type**       | **Recommended Function** | **Use Case**                     | **Notes**                              |
|-----------------------|--------------------------|----------------------------------|----------------------------------------|
| Formatted Output      | `printf`                 | Simple screen output             | Ensure format specifiers match to avoid undefined behavior |
| Secure String Output  | `snprintf`               | Building strings (e.g., logs, messages) | **Always prefer this**, avoid `sprintf` |
| File Formatted Output | `fprintf`                | Writing structured data to files | Check file open status, close files promptly |
| Character Processing  | `fputc`                  | Building file content character by character | Suitable for scenarios requiring fine control |
| Text Line Output      | `fputs`                  | Writing text lines to files      | **Does not automatically add newline**, handle manually |
| Binary Data           | `fwrite`                 | Writing non-text data (e.g., images, data files) | Ensure buffer data is correct, check return value |

**Core Principles:**

1. **Safety First**: Avoid using `sprintf`; prioritize `snprintf` with length limits.
2. **Error Handling**: Check return values of file operations and handle potential failures.
3. **Resource Management**: Files opened with `fopen` must be closed with `fclose` to prevent data loss.
4. **Portability**: Standard C functions (e.g., `printf`, `snprintf`) are more universal than platform extensions.
5. **Clear Output**: Use newline characters and spaces appropriately to ensure output is readable.

**Common Errors and Solutions:**

- **Format Mismatch**: Using `%d` to output a floating-point number → Verify format specifiers match parameter types
- **Buffer Overflow**: `sprintf` writing excessively long strings → Switch to `snprintf` with buffer size specified
- **Unclosed Files**: Program crashes causing data not to be written → Ensure every `fopen` has a corresponding `fclose`
- **Missing Newline**: `fputs` output without newline → Manually add `\n` or use `fprintf` for format control

## Practical Exercise

Try writing a program that implements the following features:

1. Read user name and age from the keyboard (using `fgets` for safe input)
2. Format the information and write it to the file `user_info.txt`
3. Display confirmation information on the screen simultaneously
4. Verify if the file was successfully written

```c
#include <stdio.h>
#include <string.h>

int main() {
    char name[50];
    int age;
    
    // Safely read name
    printf("Please enter your name: ");
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = '\0';  // Remove newline character
    
    // Read age (simple example, actual implementation should validate input)
    printf("Please enter your age: ");
    scanf("%d", &age);
    
    // Write to file
    FILE *file = fopen("user_info.txt", "w");
    if (file != NULL) {
        fprintf(file, "Name: %s\nAge: %d years\n", name, age);
        fclose(file);
        
        // Confirmation message
        printf("\nInformation has been saved to the file!\n");
        printf("---------- User Information ----------\n");
        printf("Name: %s\n", name);
        printf("Age: %d years\n", age);
        printf("------------------------------\n");
    } else {
        printf("Error: Unable to create file!\n");
    }
    
    return 0;
}
```

Through this chapter, you have mastered the usage techniques of various output methods in the C language. Combined with the input knowledge from the previous chapter, you can now build complete input-output workflows to interact with users and persistently store data. The next chapter will explore file operations in C, delving deeper into efficient file resource management!
