# C Programming Day 7: Structures and Unions - Comprehensive Guide

Structures (`struct`) are one of the most powerful features in C programming, allowing you to create custom data types that group related data together. This comprehensive guide covers everything from basic concepts to advanced techniques and real-world applications.

## Table of Contents

1. [Introduction to Structures](#introduction-to-structures)
2. [Structure Definition and Declaration](#structure-definition-and-declaration)
3. [Structure Initialization](#structure-initialization)
4. [Accessing Structure Members](#accessing-structure-members)
5. [Structure Arrays](#structure-arrays)
6. [Structure Pointers](#structure-pointers)
7. [Nested Structures](#nested-structures)
8. [Structures as Function Parameters](#structures-as-function-parameters)
9. [Dynamic Memory Allocation with Structures](#dynamic-memory-allocation-with-structures)
10. [Memory Layout and Alignment](#memory-layout-and-alignment)
11. [Unions vs Structures](#unions-vs-structures)
12. [Advanced Techniques](#advanced-techniques)
13. [Real-World Applications](#real-world-applications)
14. [Best Practices](#best-practices)

## Introduction to Structures

A **structure** is a user-defined data type that allows you to combine data items of different kinds. Structures are used to represent a record, such as a book in a library, a student in a university, or an employee in a company.

### Why Use Structures?

- **Data Organization**: Group related data together logically
- **Code Readability**: Make code more understandable and maintainable
- **Data Abstraction**: Create custom data types for specific domains
- **Memory Efficiency**: Organize data in memory more effectively
- **Modularity**: Enable better program structure and design

## Structure Definition and Declaration

### Basic Syntax

```c
struct structure_name {
    data_type member1;
    data_type member2;
    // ... more members
};
```

### Complete Example with Detailed Explanation

```c
#include <stdio.h>
#include <string.h>

// Structure definition - this creates a new data type
struct Book {
    char title[100];        // String to store book title
    char author[50];        // String to store author name
    char isbn[20];          // ISBN number
    int pages;              // Number of pages
    float price;            // Book price
    int publication_year;   // Year of publication
    char genre[30];         // Book genre
};

int main() {
    // Structure variable declaration
    struct Book book1;

    // Initialize structure members using strcpy for strings
    strcpy(book1.title, "The C Programming Language");
    strcpy(book1.author, "Brian W. Kernighan & Dennis M. Ritchie");
    strcpy(book1.isbn, "978-0131103627");
    book1.pages = 272;
    book1.price = 62.99;
    book1.publication_year = 1988;
    strcpy(book1.genre, "Computer Science");

    // Display book information
    printf("=== Book Information ===\n");
    printf("Title: %s\n", book1.title);
    printf("Author: %s\n", book1.author);
    printf("ISBN: %s\n", book1.isbn);
    printf("Pages: %d\n", book1.pages);
    printf("Price: $%.2f\n", book1.price);
    printf("Publication Year: %d\n", book1.publication_year);
    printf("Genre: %s\n", book1.genre);

    return 0;
}
```

**Output:**
```
=== Book Information ===
Title: The C Programming Language
Author: Brian W. Kernighan & Dennis M. Ritchie
ISBN: 978-0131103627
Pages: 272
Price: $62.99
Publication Year: 1988
Genre: Computer Science
```

## Structure Initialization

C provides several ways to initialize structure variables, each with its own advantages and use cases.

### 1. Declaration Without Initialization

```c
struct Book book1;  // Declares a structure variable (contains garbage values)
```

⚠️ **Warning**: Uninitialized structures contain garbage values. Always initialize before use.

### 2. Sequential Initialization (C89 Style)

Initialize members in the order they appear in the structure definition:

```c
#include <stdio.h>

struct Student {
    int id;
    char name[50];
    float gpa;
    int graduation_year;
};

int main() {
    // Sequential initialization - values must be in declaration order
    struct Student student1 = {12345, "Alice Johnson", 3.85, 2024};

    printf("Student ID: %d\n", student1.id);
    printf("Name: %s\n", student1.name);
    printf("GPA: %.2f\n", student1.gpa);
    printf("Graduation Year: %d\n", student1.graduation_year);

    return 0;
}
```

### 3. Designated Initializers (C99 and Later)

Initialize specific members by name - order doesn't matter:

```c
#include <stdio.h>

struct Employee {
    int emp_id;
    char name[50];
    char department[30];
    float salary;
    int years_experience;
};

int main() {
    // Designated initialization - can specify any members in any order
    struct Employee emp1 = {
        .name = "John Smith",
        .emp_id = 1001,
        .salary = 75000.0,
        .department = "Engineering",
        .years_experience = 5
    };

    // Partial initialization - unspecified members are set to zero
    struct Employee emp2 = {
        .name = "Jane Doe",
        .emp_id = 1002,
        .salary = 68000.0
        // department and years_experience will be zero/empty
    };

    printf("Employee 1:\n");
    printf("  ID: %d\n", emp1.emp_id);
    printf("  Name: %s\n", emp1.name);
    printf("  Department: %s\n", emp1.department);
    printf("  Salary: $%.2f\n", emp1.salary);
    printf("  Experience: %d years\n", emp1.years_experience);

    printf("\nEmployee 2:\n");
    printf("  ID: %d\n", emp2.emp_id);
    printf("  Name: %s\n", emp2.name);
    printf("  Department: '%s'\n", emp2.department);  // Will be empty
    printf("  Salary: $%.2f\n", emp2.salary);
    printf("  Experience: %d years\n", emp2.years_experience);  // Will be 0

    return 0;
}
```

### 4. Zero Initialization

Initialize all members to zero/null:

```c
struct Student student_zero = {0};  // All members set to 0/null
struct Student student_empty = {};  // C++ style (some compilers support in C)
```

### 5. Runtime Assignment

Assign values after declaration:

```c
#include <stdio.h>
#include <string.h>

struct Product {
    int product_id;
    char name[100];
    char category[50];
    float price;
    int stock_quantity;
};

int main() {
    struct Product product;

    // Assign values individually
    product.product_id = 12345;
    strcpy(product.name, "Wireless Bluetooth Headphones");
    strcpy(product.category, "Electronics");
    product.price = 99.99;
    product.stock_quantity = 150;

    printf("Product Information:\n");
    printf("ID: %d\n", product.product_id);
    printf("Name: %s\n", product.name);
    printf("Category: %s\n", product.category);
    printf("Price: $%.2f\n", product.price);
    printf("Stock: %d units\n", product.stock_quantity);

    return 0;
}
```

### 6. Array of Structures Initialization

```c
#include <stdio.h>

struct Point {
    int x;
    int y;
    char label[10];
};

int main() {
    // Initialize array of structures
    struct Point points[] = {
        {0, 0, "Origin"},
        {10, 20, "Point A"},
        {-5, 15, "Point B"},
        {.x = 25, .y = -10, .label = "Point C"}  // Mixed style
    };

    int num_points = sizeof(points) / sizeof(points[0]);

    printf("Points in the coordinate system:\n");
    for (int i = 0; i < num_points; i++) {
        printf("%s: (%d, %d)\n", points[i].label, points[i].x, points[i].y);
    }

    return 0;
}
```

## Structure Arrays

Structure arrays allow you to store multiple structure variables of the same type, making it easy to manage collections of related data.

### Basic Structure Array Operations

```c
#include <stdio.h>
#include <string.h>

struct Student {
    int student_id;
    char name[50];
    char major[30];
    float gpa;
    int credits_completed;
};

int main() {
    // Initialize array of structures
    struct Student students[5] = {
        {1001, "Alice Johnson", "Computer Science", 3.85, 90},
        {1002, "Bob Smith", "Mathematics", 3.92, 88},
        {1003, "Charlie Brown", "Physics", 3.67, 85},
        {1004, "Diana Prince", "Engineering", 3.95, 92},
        {1005, "Eve Wilson", "Biology", 3.78, 87}
    };

    int num_students = sizeof(students) / sizeof(students[0]);

    printf("=== Student Database ===\n");
    printf("%-6s %-20s %-20s %-6s %-8s\n",
           "ID", "Name", "Major", "GPA", "Credits");
    printf("---------------------------------------------------------------\n");

    for (int i = 0; i < num_students; i++) {
        printf("%-6d %-20s %-20s %-6.2f %-8d\n",
               students[i].student_id,
               students[i].name,
               students[i].major,
               students[i].gpa,
               students[i].credits_completed);
    }

    return 0;
}
```

**Output:**
```
=== Student Database ===
ID     Name                 Major                GPA    Credits
---------------------------------------------------------------
1001   Alice Johnson        Computer Science     3.85   90
1002   Bob Smith            Mathematics          3.92   88
1003   Charlie Brown        Physics              3.67   85
1004   Diana Prince         Engineering          3.95   92
1005   Eve Wilson           Biology              3.78   87
```

### Advanced Array Operations

```c
#include <stdio.h>
#include <string.h>

struct Product {
    int id;
    char name[50];
    float price;
    int quantity;
    char category[30];
};

// Function to display all products
void display_products(struct Product products[], int count) {
    printf("\n=== Product Inventory ===\n");
    printf("%-5s %-25s %-10s %-8s %-15s\n",
           "ID", "Name", "Price", "Qty", "Category");
    printf("----------------------------------------------------------------\n");

    for (int i = 0; i < count; i++) {
        printf("%-5d %-25s $%-9.2f %-8d %-15s\n",
               products[i].id,
               products[i].name,
               products[i].price,
               products[i].quantity,
               products[i].category);
    }
}

// Function to find product by ID
int find_product_by_id(struct Product products[], int count, int search_id) {
    for (int i = 0; i < count; i++) {
        if (products[i].id == search_id) {
            return i;  // Return index if found
        }
    }
    return -1;  // Return -1 if not found
}

// Function to calculate total inventory value
float calculate_total_value(struct Product products[], int count) {
    float total = 0.0;
    for (int i = 0; i < count; i++) {
        total += products[i].price * products[i].quantity;
    }
    return total;
}

int main() {
    struct Product inventory[] = {
        {101, "Laptop", 999.99, 25, "Electronics"},
        {102, "Mouse", 29.99, 100, "Electronics"},
        {103, "Keyboard", 79.99, 75, "Electronics"},
        {104, "Monitor", 299.99, 40, "Electronics"},
        {105, "Desk Chair", 199.99, 30, "Furniture"}
    };

    int product_count = sizeof(inventory) / sizeof(inventory[0]);

    // Display all products
    display_products(inventory, product_count);

    // Search for a specific product
    int search_id = 103;
    int index = find_product_by_id(inventory, product_count, search_id);

    if (index != -1) {
        printf("\nProduct found:\n");
        printf("ID: %d, Name: %s, Price: $%.2f\n",
               inventory[index].id,
               inventory[index].name,
               inventory[index].price);
    } else {
        printf("\nProduct with ID %d not found.\n", search_id);
    }

    // Calculate total inventory value
    float total_value = calculate_total_value(inventory, product_count);
    printf("\nTotal Inventory Value: $%.2f\n", total_value);

    return 0;
}
```

## Structure Pointers

Structure pointers are variables that store the memory address of structure variables. They provide an efficient way to access and manipulate structures, especially when passing structures to functions or working with dynamic memory allocation.

### Basic Pointer Operations

```c
#include <stdio.h>
#include <string.h>

struct Vehicle {
    char make[30];
    char model[30];
    int year;
    float price;
    int mileage;
};

int main() {
    // Create a structure variable
    struct Vehicle car1 = {"Toyota", "Camry", 2022, 28500.0, 15000};

    // Create a pointer to the structure
    struct Vehicle *car_ptr = &car1;

    printf("=== Accessing Structure via Pointer ===\n");

    // Method 1: Using arrow operator (->)
    printf("Make: %s\n", car_ptr->make);
    printf("Model: %s\n", car_ptr->model);
    printf("Year: %d\n", car_ptr->year);
    printf("Price: $%.2f\n", car_ptr->price);
    printf("Mileage: %d miles\n", car_ptr->mileage);

    // Method 2: Using dereference operator (*)
    printf("\n=== Using Dereference Operator ===\n");
    printf("Make: %s\n", (*car_ptr).make);
    printf("Model: %s\n", (*car_ptr).model);
    printf("Year: %d\n", (*car_ptr).year);

    // Modifying structure through pointer
    car_ptr->price = 26500.0;
    car_ptr->mileage = 18000;
    strcpy(car_ptr->model, "Camry Hybrid");

    printf("\n=== After Modification ===\n");
    printf("Model: %s\n", car1.model);  // Original variable reflects changes
    printf("Price: $%.2f\n", car1.price);
    printf("Mileage: %d miles\n", car1.mileage);

    return 0;
}
```

### Pointer Arithmetic with Structure Arrays

```c
#include <stdio.h>

struct Point {
    int x;
    int y;
};

void print_point(struct Point *p) {
    printf("Point: (%d, %d)\n", p->x, p->y);
}

int main() {
    struct Point points[] = {
        {1, 2}, {3, 4}, {5, 6}, {7, 8}, {9, 10}
    };

    int num_points = sizeof(points) / sizeof(points[0]);
    struct Point *ptr = points;  // Points to first element

    printf("=== Using Pointer Arithmetic ===\n");

    // Method 1: Array indexing with pointer
    for (int i = 0; i < num_points; i++) {
        printf("Point %d: (%d, %d)\n", i + 1, ptr[i].x, ptr[i].y);
    }

    printf("\n=== Using Pointer Increment ===\n");

    // Method 2: Pointer increment
    ptr = points;  // Reset pointer
    for (int i = 0; i < num_points; i++) {
        printf("Point %d: (%d, %d)\n", i + 1, ptr->x, ptr->y);
        ptr++;  // Move to next structure
    }

    return 0;
}
```

### Dynamic Memory Allocation with Structures

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Employee {
    int id;
    char name[50];
    char department[30];
    float salary;
};

// Function to create a new employee
struct Employee* create_employee(int id, const char* name,
                                const char* dept, float salary) {
    struct Employee *emp = malloc(sizeof(struct Employee));

    if (emp == NULL) {
        printf("Memory allocation failed!\n");
        return NULL;
    }

    emp->id = id;
    strcpy(emp->name, name);
    strcpy(emp->department, dept);
    emp->salary = salary;

    return emp;
}

// Function to display employee information
void display_employee(struct Employee *emp) {
    if (emp == NULL) {
        printf("Invalid employee pointer!\n");
        return;
    }

    printf("Employee ID: %d\n", emp->id);
    printf("Name: %s\n", emp->name);
    printf("Department: %s\n", emp->department);
    printf("Salary: $%.2f\n", emp->salary);
    printf("------------------------\n");
}

int main() {
    // Create employees dynamically
    struct Employee *emp1 = create_employee(1001, "John Doe", "Engineering", 75000.0);
    struct Employee *emp2 = create_employee(1002, "Jane Smith", "Marketing", 68000.0);
    struct Employee *emp3 = create_employee(1003, "Bob Johnson", "Finance", 72000.0);

    printf("=== Employee Database ===\n");
    display_employee(emp1);
    display_employee(emp2);
    display_employee(emp3);

    // Don't forget to free allocated memory
    free(emp1);
    free(emp2);
    free(emp3);

    return 0;
}
```

## 结构体嵌套

结构体可以作为另一个结构体的成员。

```c
#include <stdio.h>

struct Address {
    char city[20];
    char street[20];
};

struct Person {
    char name[20];
    int age;
    struct Address addr; // 嵌套结构体
};

int main() {
    struct Person p1;

    // 赋值
    strcpy(p1.name, "John");
    p1.age = 30;
    strcpy(p1.addr.city, "New York");
    strcpy(p1.addr.street, "5th Avenue");

    // 输出
    printf("Name: %s\n", p1.name);
    printf("Age: %d\n", p1.age);
    printf("City: %s\n", p1.addr.city);
    printf("Street: %s\n", p1.addr.street);

    return 0;

}
```

输出结果

```bash
Name: John
Age: 30
City: New York
Street: 5th Avenue
```

## 结构体作为函数参数

传值方式

```c
#include <stdio.h>

struct Point {
    int x;
    int y;
};

void printPoint(struct Point p) { // 结构体传值
    printf("Point: (%d, %d)\n", p.x, p.y);
}

int main() {
    struct Point p1 = {10, 20};
    printPoint(p1);
    return 0;
}
```

传指针方式

```c
#include <stdio.h>

struct Point {
    int x;
    int y;
};

void modifyPoint(struct Point \*p) { // 结构体传指针
    p->x += 10;
    p->y += 20;
}

int main() {
    struct Point p1 = {10, 20};
    modifyPoint(&p1);
    printf("Modified Point: (%d, %d)\n", p1.x, p1.y);
    return 0;
}
```

## 结构体与 typedef

typedef 用于简化结构体的使用，相当于取个绰号。

```c
#include <stdio.h>

typedef struct {
    char name[20];
    int age;
} Person;

int main() {
    Person p1 = {"John", 25};
    printf("Name: %s, Age: %d\n", p1.name, p1.age);
    return 0;
}
```

## 结构体大小与内存对齐

结构体的大小受内存对齐规则影响：

- 每个成员按自身类型的大小对齐。
- 结构体的总大小是最大成员大小的整数倍。

```c
#include <stdio.h>

struct Test {
    char a; // 1 字节
    int b; // 4 字节
    char c; // 1 字节
};

int main() {
    printf("Size of struct Test: %zu bytes\n", sizeof(struct Test));
    return 0;
}
```

```bash
输出：（可能为 12 字节，取决于编译器）
Size of struct Test: 12 bytes
```

## 联合体与结构体的区别

- 结构体：所有成员独立存在，占用的内存是所有成员大小之和。
- 联合体：所有成员共享一块内存，大小取决于最大成员。

```c
#include <stdio.h>

union Data {
    int i;
    float f;
    char str[20];
};

int main() {
    union Data data;

    data.i = 10;
    printf("Int: %d\n", data.i);

    data.f = 3.14;
    printf("Float: %.2f\n", data.f);

    strcpy(data.str, "Hello");
    printf("String: %s\n", data.str);

    return 0;

}
```

## 实际应用

结构体在实际项目中非常有用，例如：

- 学生管理系统：存储学生信息。
- 图形系统：定义点、线、面等结构。
- 文件系统：定义文件属性（名称、大小、路径等）。
- 当然，还有学校的C语言考试
