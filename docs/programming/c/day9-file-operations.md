# Day9 - Detailed Explanation of File Operations in C

File operations are an essential feature in the C language, enabling the creation, reading, writing, and modification of disk files. C provides robust file operation support through standard library functions located in the `<stdio.h>` header file.

## Basic Concepts of Files

A file is a collection of data stored on a disk, which can be either a text file or a binary file:

- **Text File**: Stores data as readable characters (encoded in ASCII/UTF-8, etc.), suitable for human reading.
- **Binary File**: Stores raw data in its original form, not directly readable by humans.

In C, file operations are based on the file pointer `FILE*`, which is used to reference a file.

## Basic Steps for File Operations

The basic workflow for file operations consists of four steps:

1. **Open the file** (`fopen()` or `freopen()`)
2. **Read/write the file** (e.g., `fscanf()`, `fprintf()`, `fread()`, `fwrite()`, etc.)
3. **Close the file** (`fclose()`)
4. **Handle errors** (detected via return values or `ferror()`)

## File Pointers

`FILE*` is a pointer to a file, used to manipulate the file. After opening a file, a pointer to the file stream is returned, which is then used for subsequent read/write operations.

## Opening and Closing Files

### Opening a File: `fopen()`

**Syntax**:

```c
FILE* fopen(const char* filename, const char* mode);
```

**Parameter Description**:

- `filename`: File name (including path)
- `mode`: File opening mode

**Common File Modes**:

| Mode   | Meaning                                      |
| ------ | ----------------------------------------- |
| `"r"`  | Open file in read-only mode; file must exist          |
| `"w"`  | Open file in write mode; clears content if file exists  |
| `"a"`  | Open file in append mode; creates file if it doesn't exist          |
| `"r+"` | Open file in read-write mode; file must exist          |
| `"w+"` | Open file in read-write mode; clears content if file exists  |
| `"a+"` | Open file in read-write mode; appends data from the end of the file    |
| `"b"`  | Binary mode (can be combined with above modes, e.g., `"rb"`) |

**Example**:

```c
FILE* fp = fopen("example.txt", "w");
if (fp == NULL) {
    printf("Failed to open file!\n");
    return 1;
}
```

### Closing a File: `fclose()`

**Syntax**:

```c
int fclose(FILE* stream);
```

Closes the file and releases resources. Returns `0` on success, `EOF` on failure.

**Example**:

```c
fclose(fp);
```

### Combined Example

```c
#include <stdio.h>

int main() {
    FILE* fp = fopen("example.txt", "w");  // Open file in write mode

    if (fp == NULL) {  // Check if file opened successfully
        printf("Failed to open file!\n");
        return 1;
    }

    printf("File opened successfully!\n");

    fclose(fp);  // Close file
    printf("File closed successfully!\n");

    return 0;
}
```

## File Reading and Writing

### Text File Reading and Writing

#### Writing to a Text File: `fprintf()`

Used to write formatted text data.

**Syntax**:

```c
int fprintf(FILE* stream, const char* format, ...);
```

**Example**:

```c
FILE* fp = fopen("example.txt", "w");
if (fp != NULL) {
    fprintf(fp, "Name: %s\nAge: %d\n", "Zhang San", 25);
    fclose(fp);
}
```

#### Reading from a Text File: `fscanf()`

Used to read formatted text data.

**Syntax**:

```c
int fscanf(FILE* stream, const char* format, ...);
```

**Example**:

```c
FILE* fp = fopen("example.txt", "r");
char name[50];
int age;
if (fp != NULL) {
    fscanf(fp, "Name: %s\nAge: %d\n", name, &age);
    printf("Name: %s, Age: %d\n", name, age);
    fclose(fp);
}
```

#### Character Operations: `fgetc()` and `fputc()`

- `fgetc(FILE* stream)`: Reads one character from the file
- `fputc(int ch, FILE* stream)`: Writes one character to the file

**Example**:

```c
FILE* fp = fopen("example.txt", "w");
if (fp != NULL) {
    fputc('A', fp);  // Write character 'A'
    fclose(fp);
}

fp = fopen("example.txt", "r");
if (fp != NULL) {
    char ch = fgetc(fp);  // Read character
    printf("Read character: %c\n", ch);
    fclose(fp);
}
```

#### Line Operations: `fgets()` and `fputs()`

- `fgets(char* str, int n, FILE* stream)`: Reads a line, up to `n-1` characters
- `fputs(const char* str, FILE* stream)`: Writes a line

**Example**:

```c
FILE* fp = fopen("example.txt", "w");
if (fp != NULL) {
    fputs("Hello, World!\n", fp);
    fclose(fp);
}

fp = fopen("example.txt", "r");
if (fp != NULL) {
    char line[100];
    fgets(line, sizeof(line), fp);  // Read a line
    printf("Read line: %s", line);
    fclose(fp);
}
```

#### Two Examples

```c
#include <stdio.h>

int main() {
    FILE* fp = fopen("example.txt", "w");  // Open file in write mode
    if (fp == NULL) {
        printf("Failed to open file!\n");
        return 1;
    }

    fprintf(fp, "Name: %s\n", "Zhang San");
    fprintf(fp, "Age: %d\n", 25);  // Write text

    fclose(fp);  // Close file
    printf("Write completed!\n");

    return 0;
}
```

```c
#include <stdio.h>

int main() {
    FILE* fp = fopen("example.txt", "r");  // Open file in read mode
    if (fp == NULL) {
        printf("Failed to open file!\n");
        return 1;
    }

    char name[50];
    int age;
    fscanf(fp, "Name: %s\n", name);
    fscanf(fp, "Age: %d\n", &age);  // Read content by format

    printf("Name: %s\n", name);
    printf("Age: %d\n", age);

    fclose(fp);  // Close file
    return 0;
}
```

### Binary File Reading and Writing

#### Writing to a Binary File: `fwrite()`

Used to write data blocks to a file.

**Syntax**:

```c
size_t fwrite(const void* ptr, size_t size, size_t count, FILE* stream);
```

**Example**:

```c
FILE* fp = fopen("data.bin", "wb");
int data[] = {1, 2, 3, 4, 5};
fwrite(data, sizeof(int), 5, fp);
fclose(fp);
```

#### Reading from a Binary File: `fread()`

Used to read data blocks from a file.

**Syntax**:

```c
size_t fread(void* ptr, size_t size, size_t count, FILE* stream);
```

**Example**:

```c
FILE* fp = fopen("data.bin", "rb");
int data[5];
fread(data, sizeof(int), 5, fp);
for (int i = 0; i < 5; i++) {
    printf("%d ", data[i]);
}
fclose(fp);
```

```c
#include <stdio.h>

int main() {
    FILE* fp = fopen("data.bin", "wb");  // Open binary file
    if (fp == NULL) {
        printf("Failed to open file!\n");
        return 1;
    }

    int numbers[] = {10, 20, 30, 40, 50};
    fwrite(numbers, sizeof(int), 5, fp);  // Write 5 integers

    fclose(fp);
    printf("Binary data write completed!\n");

    return 0;
}
```

```c
#include <stdio.h>

int main() {
    FILE* fp = fopen("data.bin", "rb");  // Open binary file
    if (fp == NULL) {
        printf("Failed to open file!\n");
        return 1;
    }

    int numbers[5];
    fread(numbers, sizeof(int), 5, fp);  // Read 5 integers

    for (int i = 0; i < 5; i++) {
        printf("Number %d: %d\n", i + 1, numbers[i]);
    }

    fclose(fp);
    return 0;
}
```

## File Pointer Position Operations

### (1) `ftell()`

Returns the current position of the file pointer.

**Syntax**:

```c
long ftell(FILE* stream);
```

### (2) `fseek()`

Moves the file pointer to a specified position.

**Syntax**:

```c
int fseek(FILE* stream, long offset, int origin);
```

**Example**:

```c
FILE* fp = fopen("example.txt", "r");
fseek(fp, 10, SEEK_SET);  // Move pointer to the 10th byte of the file
printf("Current position: %ld\n", ftell(fp));
fclose(fp);
```

### (3) `rewind()`

Resets the file pointer to the beginning of the file.

**Syntax**:

```c
void rewind(FILE* stream);
```

```c
#include <stdio.h>

int main() {
    FILE* fp = fopen("example.txt", "r");
    if (fp == NULL) {
        printf("Failed to open file!\n");
        return 1;
    }

    fseek(fp, 5, SEEK_SET);  // Move pointer to the 5th byte of the file
    long pos = ftell(fp);   // Get current pointer position
    printf("Current pointer position: %ld\n", pos);

    fclose(fp);
    return 0;
}
```

## Error Handling in File Operations

### (1) `ferror()`

Checks if an error occurred during file operations.

**Syntax**:

```c
int ferror(FILE* stream);
```

### (2) `perror()`

Prints error messages related to file operations.

**Syntax**:

```c
void perror(const char* str);
```

```c
#include <stdio.h>

int main() {
    FILE* fp = fopen("nonexistent.txt", "r");  // Attempt to open non-existent file
    if (fp == NULL) {
        perror("Failed to open file");  // Print error message
        return 1;
    }

    char ch = fgetc(fp);
    if (ferror(fp)) {  // Check if an error occurred
        printf("File read error!\n");
    }

    fclose(fp);
    return 0;
}
```

## Common Issues and Notes

- Always check if the return value is `NULL` when opening a file.
- Always close files after operations to release resources.
- Choose the correct file read/write mode to avoid data loss.
- Ensure data size matches when handling binary files.

The above code covers all common C language file operations, with complete example code for each function that can be directly run and tested.
