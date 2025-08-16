# C 编程第7天：结构体和联合体 - 综合指南

结构体（`struct`）是 C 编程中最强大的特性之一，允许您创建将相关数据组合在一起的自定义数据类型。本综合指南涵盖了从基本概念到高级技术和实际应用的所有内容。

[English](day7-structures-unions.md) | **中文**

## 目录

1. [结构体简介](#结构体简介)
2. [结构体定义和声明](#结构体定义和声明)
3. [结构体初始化](#结构体初始化)
4. [访问结构体成员](#访问结构体成员)
5. [结构体数组](#结构体数组)
6. [结构体指针](#结构体指针)
7. [嵌套结构体](#嵌套结构体)
8. [结构体作为函数参数](#结构体作为函数参数)
9. [联合体 vs 结构体](#联合体-vs-结构体)
10. [实际应用](#实际应用)

## 结构体简介

**结构体**是用户定义的数据类型，允许您组合不同类型的数据项。结构体用于表示记录，如图书馆中的书籍、大学中的学生或公司中的员工。

### 为什么使用结构体？

- **数据组织**：逻辑地将相关数据组合在一起
- **代码可读性**：使代码更易理解和维护
- **数据抽象**：为特定领域创建自定义数据类型
- **内存效率**：更有效地在内存中组织数据
- **模块化**：实现更好的程序结构和设计

## 结构体定义和声明

### 基本语法

```c
struct 结构体名称 {
    数据类型 成员1;
    数据类型 成员2;
    // ... 更多成员
};
```

### 完整示例

```c
#include <stdio.h>
#include <string.h>

// 定义学生结构体
struct Student {
    int id;                    // 学号
    char name[50];            // 姓名
    float gpa;                // 平均绩点
    int age;                  // 年龄
};

int main() {
    // 声明结构体变量
    struct Student student1;
    
    // 初始化结构体成员
    student1.id = 12345;
    strcpy(student1.name, "张三");
    student1.gpa = 3.85;
    student1.age = 20;
    
    // 输出结构体信息
    printf("学生信息：\n");
    printf("学号：%d\n", student1.id);
    printf("姓名：%s\n", student1.name);
    printf("GPA：%.2f\n", student1.gpa);
    printf("年龄：%d\n", student1.age);
    
    return 0;
}
```

## 结构体初始化

### 方法1：逐个成员初始化

```c
struct Student student1;
student1.id = 12345;
strcpy(student1.name, "张三");
student1.gpa = 3.85;
student1.age = 20;
```

### 方法2：声明时初始化

```c
struct Student student2 = {12346, "李四", 3.92, 21};
```

### 方法3：指定成员初始化（C99）

```c
struct Student student3 = {
    .id = 12347,
    .name = "王五",
    .gpa = 3.78,
    .age = 19
};
```

## 访问结构体成员

### 使用点操作符（.）

```c
struct Student student;
student.id = 12345;           // 设置成员值
int studentId = student.id;   // 获取成员值
```

### 使用箭头操作符（->）用于指针

```c
struct Student *ptr = &student;
ptr->id = 12345;              // 等价于 (*ptr).id = 12345
int studentId = ptr->id;      // 等价于 (*ptr).id
```

## 结构体数组

```c
#include <stdio.h>
#include <string.h>

struct Student {
    int id;
    char name[50];
    float gpa;
};

int main() {
    // 声明结构体数组
    struct Student students[3];
    
    // 初始化数组元素
    students[0] = (struct Student){1001, "张三", 3.85};
    students[1] = (struct Student){1002, "李四", 3.92};
    students[2] = (struct Student){1003, "王五", 3.78};
    
    // 遍历数组
    printf("所有学生信息：\n");
    for (int i = 0; i < 3; i++) {
        printf("学号：%d，姓名：%s，GPA：%.2f\n", 
               students[i].id, students[i].name, students[i].gpa);
    }
    
    return 0;
}
```

## 结构体指针

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Student {
    int id;
    char name[50];
    float gpa;
};

void printStudent(struct Student *s) {
    printf("学号：%d\n", s->id);
    printf("姓名：%s\n", s->name);
    printf("GPA：%.2f\n", s->gpa);
}

int main() {
    // 动态分配内存
    struct Student *student = malloc(sizeof(struct Student));
    
    if (student == NULL) {
        printf("内存分配失败\n");
        return 1;
    }
    
    // 使用箭头操作符设置值
    student->id = 12345;
    strcpy(student->name, "张三");
    student->gpa = 3.85;
    
    // 调用函数
    printStudent(student);
    
    // 释放内存
    free(student);
    
    return 0;
}
```

## 嵌套结构体

```c
#include <stdio.h>
#include <string.h>

// 地址结构体
struct Address {
    char street[100];
    char city[50];
    char zipcode[10];
};

// 学生结构体（包含地址）
struct Student {
    int id;
    char name[50];
    struct Address address;  // 嵌套结构体
    float gpa;
};

int main() {
    struct Student student = {
        .id = 12345,
        .name = "张三",
        .address = {
            .street = "中山路123号",
            .city = "北京",
            .zipcode = "100000"
        },
        .gpa = 3.85
    };
    
    printf("学生信息：\n");
    printf("学号：%d\n", student.id);
    printf("姓名：%s\n", student.name);
    printf("地址：%s, %s %s\n", 
           student.address.street, 
           student.address.city, 
           student.address.zipcode);
    printf("GPA：%.2f\n", student.gpa);
    
    return 0;
}
```

## 结构体作为函数参数

### 按值传递

```c
void printStudentByValue(struct Student s) {
    printf("学号：%d，姓名：%s\n", s.id, s.name);
    // 修改不会影响原始结构体
    s.id = 99999;
}
```

### 按引用传递（推荐）

```c
void printStudentByReference(struct Student *s) {
    printf("学号：%d，姓名：%s\n", s->id, s->name);
    // 修改会影响原始结构体
    s->id = 99999;
}

void updateGPA(struct Student *s, float newGPA) {
    s->gpa = newGPA;
}
```

## 联合体 vs 结构体

### 联合体（Union）

联合体允许在同一内存位置存储不同的数据类型，但一次只能使用一个成员。

```c
#include <stdio.h>

union Data {
    int integer;
    float floating;
    char character;
};

int main() {
    union Data data;
    
    data.integer = 42;
    printf("整数：%d\n", data.integer);
    
    data.floating = 3.14;
    printf("浮点数：%.2f\n", data.floating);
    printf("整数（已被覆盖）：%d\n", data.integer);  // 值已改变
    
    printf("联合体大小：%zu 字节\n", sizeof(union Data));
    
    return 0;
}
```

### 结构体 vs 联合体比较

| 特性 | 结构体 | 联合体 |
|------|--------|--------|
| 内存使用 | 所有成员都有独立内存 | 所有成员共享同一内存 |
| 同时访问 | 可以同时访问所有成员 | 一次只能使用一个成员 |
| 大小 | 所有成员大小之和（加上对齐） | 最大成员的大小 |
| 用途 | 组合相关数据 | 节省内存，类型转换 |

## 实际应用

### 学生管理系统

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STUDENTS 100

struct Student {
    int id;
    char name[50];
    float gpa;
    int age;
};

struct StudentDatabase {
    struct Student students[MAX_STUDENTS];
    int count;
};

// 添加学生
void addStudent(struct StudentDatabase *db, int id, const char *name, float gpa, int age) {
    if (db->count >= MAX_STUDENTS) {
        printf("数据库已满！\n");
        return;
    }
    
    struct Student *s = &db->students[db->count];
    s->id = id;
    strcpy(s->name, name);
    s->gpa = gpa;
    s->age = age;
    db->count++;
    
    printf("学生 %s 添加成功！\n", name);
}

// 查找学生
struct Student* findStudent(struct StudentDatabase *db, int id) {
    for (int i = 0; i < db->count; i++) {
        if (db->students[i].id == id) {
            return &db->students[i];
        }
    }
    return NULL;
}

// 显示所有学生
void displayAllStudents(struct StudentDatabase *db) {
    printf("\n=== 所有学生信息 ===\n");
    for (int i = 0; i < db->count; i++) {
        struct Student *s = &db->students[i];
        printf("学号：%d，姓名：%s，GPA：%.2f，年龄：%d\n", 
               s->id, s->name, s->gpa, s->age);
    }
}

int main() {
    struct StudentDatabase db = {0};  // 初始化数据库
    
    // 添加学生
    addStudent(&db, 1001, "张三", 3.85, 20);
    addStudent(&db, 1002, "李四", 3.92, 21);
    addStudent(&db, 1003, "王五", 3.78, 19);
    
    // 显示所有学生
    displayAllStudents(&db);
    
    // 查找特定学生
    struct Student *found = findStudent(&db, 1002);
    if (found) {
        printf("\n找到学生：%s，GPA：%.2f\n", found->name, found->gpa);
    } else {
        printf("\n未找到学生\n");
    }
    
    return 0;
}
```

## 最佳实践

### 1. 使用 typedef 简化声明

```c
typedef struct {
    int id;
    char name[50];
    float gpa;
} Student;

// 现在可以直接使用 Student 而不是 struct Student
Student student1;
Student students[10];
```

### 2. 结构体成员对齐

```c
// 不好的对齐
struct BadAlignment {
    char a;     // 1 字节
    int b;      // 4 字节（可能有3字节填充）
    char c;     // 1 字节
    double d;   // 8 字节（可能有7字节填充）
};

// 好的对齐
struct GoodAlignment {
    double d;   // 8 字节
    int b;      // 4 字节
    char a;     // 1 字节
    char c;     // 1 字节（2字节填充）
};
```

### 3. 使用常量指针保护数据

```c
void printStudent(const struct Student *s) {
    printf("姓名：%s\n", s->name);
    // s->name = "新名字";  // 编译错误，无法修改
}
```

### 4. 错误处理

```c
struct Student* createStudent(int id, const char *name, float gpa) {
    if (name == NULL || strlen(name) == 0) {
        return NULL;  // 输入验证
    }
    
    struct Student *s = malloc(sizeof(struct Student));
    if (s == NULL) {
        return NULL;  // 内存分配失败
    }
    
    s->id = id;
    strcpy(s->name, name);
    s->gpa = gpa;
    
    return s;
}
```

结构体是 C 语言中组织和管理复杂数据的强大工具。掌握结构体的使用对于编写高质量、可维护的 C 程序至关重要。

---

**语言版本：**

- [English](day7-structures-unions.md) - 英文版本
- **中文** - 当前页面
