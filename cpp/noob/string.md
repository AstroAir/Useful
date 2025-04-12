# C++字符串操作教程

## 前言

欢迎来到C++字符串操作教程！本教程将带您从基础到高级，系统地学习C++中的字符串处理技术。我们将按照历史发展顺序，从C语言继承的字符串操作讲起，直到C++20/23中的最新特性，并提供丰富的示例帮助您快速掌握这些技能。

## C风格字符串

### 什么是C风格字符串

在C++中，我们继承了C语言的字符串表示法：以空字符('\0')结尾的字符数组。

```cpp
// 创建C风格字符串的几种方式
char str1[] = "Hello";         // 编译器自动添加'\0'
char str2[6] = {'H', 'e', 'l', 'l', 'o', '\0'};
char* str3 = "World";          // 字符串字面量（C++11后不推荐）
```

### 基本操作函数

C风格字符串的操作函数都在`<cstring>`（或传统C的`<string.h>`）头文件中：

#### 字符串长度

```cpp
#include <cstring>

char greeting[] = "Hello";
size_t length = strlen(greeting);  // 返回5（不计算结束符'\0'）
```

#### 字符串复制

```cpp
char source[] = "Hello";
char destination[10];
strcpy(destination, source);    // 不安全，无边界检查
strncpy(destination, source, 9); // 较安全，复制最多9个字符
destination[9] = '\0';          // 确保结尾有空字符
```

#### 字符串连接

```cpp
char str1[20] = "Hello";
char str2[] = " World";
strcat(str1, str2);      // str1变成"Hello World"
strncat(str1, "!", 1);   // 较安全，连接最多1个字符
```

#### 字符串比较

```cpp
char str1[] = "apple";
char str2[] = "banana";
int result = strcmp(str1, str2);  // 返回负值，因为str1字典序小于str2
```

#### 字符串查找

```cpp
char text[] = "Hello World";
char* ptr = strchr(text, 'o');    // 查找字符'o'，返回指向首次出现位置的指针
char* subPtr = strstr(text, "lo"); // 查找子串"lo"，返回指向子串位置的指针
```

### C风格字符串的局限性

存在的问题：

- 缓冲区溢出风险：没有自动边界检查
- 内存管理复杂：需要手动分配和释放内存
- 操作不直观：需要使用函数而非运算符
- 没有封装：数据和操作分离

示例：缓冲区溢出问题

```cpp
char smallBuffer[5];
strcpy(smallBuffer, "This is too long");  // 危险！会溢出
```

## std::string 基础

### std::string 介绍

C++标准库提供的`std::string`类（在`<string>`头文件中）解决了C风格字符串的许多问题：

```cpp
#include <string>
#include <iostream>

int main() {
    // 创建string对象
    std::string greeting = "Hello";  // 从字符串字面量创建
    std::string empty;               // 空字符串
    std::string repeated(5, 'a');    // 创建"aaaaa"
    
    std::cout << greeting << std::endl;      // Hello
    std::cout << repeated << std::endl;      // aaaaa
    std::cout << empty.empty() << std::endl; // 1 (true)
    
    return 0;
}
```

### 基本操作

#### 字符串长度和容量

```cpp
std::string str = "Hello World";
size_t length = str.length();  // 或str.size() - 返回11
bool isEmpty = str.empty();    // 检查是否为空 - false
size_t capacity = str.capacity(); // 返回当前分配的存储空间大小
```

#### 访问字符

```cpp
std::string str = "Hello";
char first = str[0];         // 'H' - 不检查边界
char last = str.at(4);       // 'o' - 有边界检查，越界抛出异常
char front = str.front();    // 'H' - C++11
char back = str.back();      // 'o' - C++11
```

#### 修改字符串

```cpp
std::string str = "Hello";
str += " World";           // 追加，现在str为"Hello World"
str.append("!");           // 追加，现在str为"Hello World!"
str.push_back('!');        // 添加单个字符，现在str为"Hello World!!"

str = "Hello";             // 重新赋值
str.insert(5, " beautiful"); // 在位置5插入，现在str为"Hello beautiful"
str.erase(5, 10);          // 从位置5开始删除10个字符，恢复到"Hello"
str.replace(1, 2, "i");    // 替换位置1开始的2个字符，变为"Hillo"
str.clear();               // 清空字符串
```

#### 字符串比较

```cpp
std::string s1 = "apple";
std::string s2 = "banana";

bool equal = (s1 == s2);             // false
bool less = (s1 < s2);               // true，字典序比较
int comparison = s1.compare(s2);     // 负值，s1小于s2
```

### 子串操作

```cpp
std::string str = "Hello World";

// 提取子串
std::string sub = str.substr(6, 5);  // 从位置6开始，长度5："World"
std::string tail = str.substr(6);    // 从位置6到结尾："World"

// 查找操作
size_t pos = str.find("World");      // 返回6
size_t notFound = str.find("C++");   // 返回string::npos

// 查找字符
pos = str.find_first_of("aeiou");    // 返回1 (e是第一个元音)
pos = str.find_last_of("aeiou");     // 返回7 (o是最后一个元音)
```

## std::string 进阶操作

### 字符串输入输出

```cpp
#include <string>
#include <iostream>

int main() {
    std::string name;
    
    std::cout << "请输入您的名字: ";
    std::cin >> name;  // 读取到空白字符为止
    std::cout << "您好, " << name << "!" << std::endl;
    
    std::cin.ignore();  // 忽略之前输入缓冲区中的换行符
    
    std::cout << "请输入您的全名: ";
    std::getline(std::cin, name);  // 读取整行
    std::cout << "您好, " << name << "!" << std::endl;
    
    return 0;
}
```

### 字符串流

```cpp
#include <string>
#include <sstream>
#include <iostream>

int main() {
    // 字符串输出流
    std::ostringstream oss;
    oss << "年龄: " << 25 << ", 身高: " << 175.5;
    std::string info = oss.str();
    std::cout << info << std::endl;  // 年龄: 25, 身高: 175.5
    
    // 字符串输入流
    std::string data = "123 456.7 文本";
    std::istringstream iss(data);
    int a;
    double b;
    std::string c;
    iss >> a >> b >> c;
    std::cout << "a=" << a << ", b=" << b << ", c=" << c << std::endl;
    
    return 0;
}
```

### 字符串分割

C++标准库没有直接提供字符串分割函数，但我们可以实现一个：

```cpp
#include <string>
#include <vector>
#include <iostream>

std::vector<std::string> split(const std::string& s, char delimiter) {
    std::vector<std::string> tokens;
    std::string token;
    std::istringstream tokenStream(s);
    
    while (std::getline(tokenStream, token, delimiter)) {
        if (!token.empty()) {
            tokens.push_back(token);
        }
    }
    
    return tokens;
}

int main() {
    std::string text = "apple,banana,orange,grape";
    std::vector<std::string> fruits = split(text, ',');
    
    for (const auto& fruit : fruits) {
        std::cout << fruit << std::endl;
    }
    
    return 0;
}
```

## C++11字符串新特性

C++11为字符串处理带来了许多实用的增强功能。

### 移动语义

```cpp
#include <string>
#include <iostream>
#include <utility>  // 为std::move

std::string createLongString() {
    std::string result(10000, 'X');  // 创建大字符串
    return result;  // 返回值优化，可能会使用移动语义
}

int main() {
    // 移动赋值
    std::string source = "这是一个很长的字符串...";
    std::string dest;
    dest = std::move(source);  // 移动而非复制，source现在可能为空
    
    std::cout << "dest: " << dest << std::endl;
    std::cout << "source: " << source << std::endl;  // source可能为空
    
    // 函数返回大字符串
    std::string large = createLongString();  // 使用移动语义避免复制
    
    return 0;
}
```

### 原始字符串字面量

使用`R"()"`语法创建原始字符串，避免大量转义字符：

```cpp
#include <string>
#include <iostream>
#include <regex>

int main() {
    // 传统字符串中的转义序列
    std::string path1 = "C:\\Program Files\\Some App\\file.txt";
    
    // 原始字符串 - 不需要转义
    std::string path2 = R"(C:\Program Files\Some App\file.txt)";
    
    std::cout << path1 << std::endl;
    std::cout << path2 << std::endl;
    
    // 对正则表达式特别有用
    std::string regexPattern = R"(\d{3}-\d{2}-\d{4})";  // 匹配SSN格式
    std::regex regexObj(regexPattern);
    
    // 使用定界符处理包含右括号的字符串
    std::string code = R"code(
    if (x > 0) {
        std::cout << "x is positive" << std::endl;
    }
    )code";
    
    std::cout << code << std::endl;
    
    return 0;
}
```

### 数值转换函数

C++11引入了方便的字符串和数值之间的转换函数：

```cpp
#include <string>
#include <iostream>

int main() {
    // 字符串转数值
    std::string numStr = "42";
    int num = std::stoi(numStr);             // 字符串转整数
    
    std::string floatStr = "3.14159";
    double pi = std::stod(floatStr);         // 字符串转双精度浮点
    float piFloat = std::stof(floatStr);     // 字符串转单精度浮点
    
    std::string bigNumStr = "123456789012345";
    long long bigNum = std::stoll(bigNumStr); // 字符串转长整型
    
    // 数值转字符串
    int age = 25;
    std::string ageStr = std::to_string(age);
    
    double value = 3.14159;
    std::string valueStr = std::to_string(value);
    
    std::cout << "整数: " << num << std::endl;
    std::cout << "双精度: " << pi << std::endl;
    std::cout << "年龄字符串: " << ageStr << std::endl;
    std::cout << "值字符串: " << valueStr << std::endl;
    
    return 0;
}
```

## C++17字符串视图

### std::string_view 介绍

C++17引入了`std::string_view`（在`<string_view>`头文件中）：一个轻量级的、非拥有型的字符串引用，可以显著提高性能。

```cpp
#include <string>
#include <string_view>
#include <iostream>

// 接受string_view作为参数，避免字符串复制
void printSubstring(std::string_view sv, size_t pos, size_t len) {
    std::cout << sv.substr(pos, len) << std::endl;
}

int main() {
    // 从不同来源创建string_view
    std::string str = "Hello World";
    std::string_view sv1 = str;              // 从std::string创建
    std::string_view sv2 = "直接字面量";      // 从字符串字面量创建
    const char* cstr = "C风格字符串";
    std::string_view sv3 = cstr;             // 从C风格字符串创建
    
    std::cout << "sv1: " << sv1 << std::endl;
    std::cout << "sv2: " << sv2 << std::endl;
    std::cout << "sv3: " << sv3 << std::endl;
    
    // 基本操作
    std::cout << "长度: " << sv1.length() << std::endl;
    std::cout << "第一个字符: " << sv1[0] << std::endl;
    std::cout << "子字符串: " << sv1.substr(0, 5) << std::endl;
    
    // 作为函数参数
    printSubstring(str, 6, 5);        // 从string
    printSubstring("Hello C++17", 6, 6); // 从字面量
    
    return 0;
}
```

### string_view vs string

优点：

- 减少复制：不创建新的字符串副本
- 性能更好：处理只读字符串时效率高
- 接口一致：许多操作与`std::string`相同

局限性：

- 只读：不能修改字符串内容
- 生命周期：必须确保引用的数据在`string_view`使用期间有效
- 无终止符：不保证有空终止符'\0'

```cpp
#include <string>
#include <string_view>
#include <iostream>
#include <chrono>

// 测量性能差异
void performanceTest() {
    const size_t iterations = 10000000;
    std::string longStr(1000, 'x');
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // 使用std::string
    size_t count1 = 0;
    for (size_t i = 0; i < iterations; ++i) {
        std::string s = longStr;
        count1 += s.length();
    }
    
    auto mid = std::chrono::high_resolution_clock::now();
    
    // 使用std::string_view
    size_t count2 = 0;
    for (size_t i = 0; i < iterations; ++i) {
        std::string_view sv = longStr;
        count2 += sv.length();
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    
    auto string_time = std::chrono::duration_cast<std::chrono::milliseconds>(mid - start).count();
    auto view_time = std::chrono::duration_cast<std::chrono::milliseconds>(end - mid).count();
    
    std::cout << "std::string 耗时: " << string_time << " ms" << std::endl;
    std::cout << "std::string_view 耗时: " << view_time << " ms" << std::endl;
}

int main() {
    performanceTest();
    return 0;
}
```

### string_view 注意事项

小心使用以避免悬垂引用：

```cpp
std::string_view dangerous() {
    std::string local = "临时字符串";
    return local;  // 危险! local在函数结束时销毁
}

void safe() {
    std::string persistent = "持久字符串";
    std::string_view sv = persistent;  // 安全，只要persistent存活
    
    // 处理sv...
}
```

## C++20/23最新特性

### std::format (C++20)

C++20引入了`std::format`，提供类似Python的字符串格式化功能：

```cpp
#include <format>
#include <string>
#include <iostream>

int main() {
    std::string name = "张三";
    int age = 30;
    double height = 175.5;
    
    // 基本格式化
    std::string result = std::format("姓名: {}, 年龄: {}, 身高: {}", name, age, height);
    std::cout << result << std::endl;
    
    // 指定参数顺序
    std::string result2 = std::format("身高: {2}, 姓名: {0}, 年龄: {1}", name, age, height);
    std::cout << result2 << std::endl;
    
    // 格式说明符
    std::string result3 = std::format("姓名: {:10}|价格: {:8.2f}|数量: {:04d}", "苹果", 5.2, 12);
    std::cout << result3 << std::endl;
    
    return 0;
}
```

### C++23字符串新方法

C++23为`std::string`和`std::string_view`添加了几个实用的方法：

```cpp
#include <string>
#include <iostream>

int main() {
    std::string str = "Hello World";
    
    // contains方法检查是否包含子串
    bool has_hello = str.contains("Hello");  // true
    std::cout << "Contains 'Hello': " << std::boolalpha << has_hello << std::endl;
    
    // starts_with检查前缀
    bool starts = str.starts_with("Hello");  // true
    std::cout << "Starts with 'Hello': " << starts << std::endl;
    
    // ends_with检查后缀
    bool ends = str.ends_with("World");  // true
    std::cout << "Ends with 'World': " << ends << std::endl;
    
    return 0;
}
```

## C与C++字符串对比

### C风格与C++风格字符串的区别

| 特性 | C风格字符串 (char[]) | C++ std::string | C++ std::string_view |
|---------|------------------------|-------------------|------------------------|
| 定义 | `char str[20] = "Hello";` | `std::string str = "Hello";` | `std::string_view sv = "Hello";` |
| 内存管理 | 手动（固定大小） | 自动（动态大小） | 无所有权（引用现有内存） |
| 大小调整 | 不可调整（需要新数组） | 自动调整 | 不可调整（只读视图） |
| 长度获取 | `strlen(str)` | `str.length()` 或 `str.size()` | `sv.length()` 或 `sv.size()` |
| 连接 | `strcat(dest, src)` | `str1 + str2` 或 `str1.append(str2)` | 不支持（只读） |
| 复制 | `strcpy(dest, src)` | `str1 = str2` | `sv = str` |
| 比较 | `strcmp(s1, s2)` | `s1 == s2`, `s1 < s2` 等 | `sv1 == sv2`, `sv1 < sv2` 等 |
| 子串提取 | 手动复制字符 | `str.substr(pos, len)` | `sv.substr(pos, len)` |
| 修改 | 直接通过索引 | 多种方法（insert, replace等） | 不支持（只读） |
| 查找 | `strchr`, `strstr` | `find`, `find_first_of` 等 | 同std::string |
| 安全性 | 低（容易溢出） | 高（自动边界检查） | 中（只读但注意生命周期） |
| 性能 | 高（直接内存操作） | 中（额外开销） | 高（无复制开销） |
| C++11数值转换 | 需要`atoi`, `strtol`等 | `stoi`, `stod`, `to_string`等 | 需先转为string |
| C++20格式化 | 需要`sprintf` | 使用`std::format` | 使用`std::format` |

## 实战技巧与最佳实践

### 字符串处理技巧

字符串拼接的高效方式

```cpp
// 低效方式：重复的+操作导致多次分配内存
std::string buildMessage(const std::vector<std::string>& words) {
    std::string result;
    for (const auto& word : words) {
        result = result + word + " ";  // 每次循环都创建新字符串
    }
    return result;
}

// 高效方式1：使用+=操作符
std::string buildMessageBetter(const std::vector<std::string>& words) {
    std::string result;
    for (const auto& word : words) {
        result += word;
        result += " ";  // 减少内存分配次数
    }
    return result;
}

// 高效方式2：使用std::ostringstream
std::string buildMessageStream(const std::vector<std::string>& words) {
    std::ostringstream oss;
    for (const auto& word : words) {
        oss << word << " ";
    }
    return oss.str();
}

// 高效方式3：预分配内存
std::string buildMessageReserve(const std::vector<std::string>& words) {
    // 计算需要的总长度
    size_t totalLength = 0;
    for (const auto& word : words) {
        totalLength += word.length() + 1;  // +1为空格
    }
    
    std::string result;
    result.reserve(totalLength);  // 预分配内存
    
    for (const auto& word : words) {
        result += word + " ";
    }
    
    return result;
}
```

大小写转换

```cpp
#include <string>
#include <algorithm>
#include <cctype>
#include <iostream>

// 转换为大写
std::string toUpper(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c) { return std::toupper(c); });
    return s;
}

// 转换为小写
std::string toLower(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    return s;
}

int main() {
    std::string text = "Hello World";
    std::cout << toUpper(text) << std::endl;  // HELLO WORLD
    std::cout << toLower(text) << std::endl;  // hello world
    return 0;
}
```

### 中文和Unicode处理

处理中文和Unicode字符串需要特别注意编码问题：

```cpp
#include <string>
#include <iostream>

int main() {
    // UTF-8编码的中文字符串
    std::string chinese = "你好，世界！";
    
    // 注意：size()返回的是字节数，而不是字符数
    std::cout << "字节数: " << chinese.size() << std::endl;
    
    // 使用C++11的u8、u、U前缀
    const char* u8str = u8"UTF-8字符串";        // UTF-8编码
    const char16_t* u16str = u"UTF-16字符串";   // UTF-16编码
    const char32_t* u32str = U"UTF-32字符串";   // UTF-32编码
    
    // C++20引入了char8_t类型
#if __cplusplus > 201703L
    const char8_t* cpp20_u8str = u8"C++20的UTF-8字符串";
#endif
    
    return 0;
}
```

### 使用建议

1. 选择合适的字符串类型
   - 对于只读操作，优先使用`std::string_view`
   - 需要修改字符串时，使用`std::string`
   - 接口设计时，考虑同时支持`std::string`和`std::string_view`

2. 避免C风格字符串的常见错误
   - 总是检查缓冲区大小
   - 使用`strncpy`而非`strcpy`，使用`strncat`而非`strcat`
   - 确保字符串正确终止

3. 性能优化技巧
   - 使用`reserve()`预分配内存
   - 对频繁修改的字符串，考虑使用`std::stringstream`
   - 传递大字符串时使用const引用或string_view

## 总结

C++的字符串处理功能随着语言标准的发展不断增强，从最初继承自C语言的字符数组，到现代的`std::string`、`std::string_view`和`std::format`，提供了更安全、更高效、更灵活的字符串处理方案。
