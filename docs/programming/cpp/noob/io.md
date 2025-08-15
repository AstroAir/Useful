# Day01 - C++中的输入输出控制(IO流)

C++的输入输出控制（I/O流）为开发者提供了强大且灵活的工具，能够以面向对象的方式高效处理控制台、文件和其他设备的输入输出操作。本文将通过对比分析、实用示例和常见场景，帮助你全面掌握I/O流的精髓。

## C++ vs C语言IO对比

| 特性                | C++实现               | C语言实现            | 优势对比                |
|---------------------|-----------------------|---------------------|-------------------------|
| 控制台输出          | `cout << "Hello"`     | `printf("Hello")`   | 类型安全，无需格式指定符 |
| 控制台输入          | `cin >> variable`     | `scanf("%d", &var)` | 自动类型推导，更简洁    |
| 文件写入            | `ofstream`对象        | `FILE*`+`fprintf`   | 自动资源管理（RAII）    |
| 错误处理            | 流状态检查            | 返回值检查           | 更面向对象，状态可追踪  |
| 格式化输出          | `setprecision`等      | `%f`等格式符        | 可链式调用，更易读      |

**场景对比示例**  

```cpp
// C++输出不同类型数据无需格式符
cout << "整数：" << 42 << "，浮点数：" << 3.14 << endl;

// C语言需要精确匹配格式符
printf("整数：%d，浮点数：%f", 42, 3.14);  // 类型不匹配时可能崩溃！
```

## 基本概念

### 流类层次结构

C++的IO流基于以下几个类：

- `ios_base`：这是所有输入输出类的基础类，提供了基本的功能，如设置格式和错误状态的检查。
- `istream` 和 `ostream`：分别处理输入和输出操作的基类。`istream`负责读取数据，而`ostream`负责写入数据。
- `iostream`：同时继承自`istream`和`ostream`，允许进行双向的输入输出操作，通常用于与文件或其他需要双向通信设备的交互。

### 标准流对象

C++提供了一些预定义的流对象，用于标准输入输出：

- `cin`：标准输入流，用于从键盘读取输入。
- `cout`：标准输出流，用于向屏幕输出数据。
- `cerr`：标准错误输出流，常用于输出错误信息，这些信息通常不会被重定向。
- `clog`：类似于`cerr`，但其输出可能会缓冲，具体行为由实现定义。

## 格式控制

格式控制允许你定制输入输出数据的显示方式，包括精度、宽度、对齐方式、基数和进制显示等。

### 常用格式设置符

- `setprecision`：控制浮点数的精度。例如：

  ```cpp
  double amount = 123.4567;
  cout << setprecision(2) << amount << endl; // 输出：123.46
  ```

- `setw`：设置字段宽度，用于对齐和填补空格。例如：

  ```cpp
  int number = 42;
  cout << setw(5) << number << endl; // 输出: "  42"（假设总宽度为5）
  ```

- `setfill`：设置填充字符，配合`setw`使用。例如：

  ```cpp
  cout << setw(5) << setfill('*') << number << endl; // 输出: "**42"
  ```

- `fixed` 和 `scientific`：分别用于以定点或科学记数法显示浮点数。例如：

  ```cpp
  cout << fixed << setprecision(2) << 123.4567 << endl; // 输出：123.46
  cout << scientific << setprecision(2) << 123.4567 << endl; // 输出：1.23e+02
  ```

- `left`, `right` 和 `internal`：控制对齐方式。例如：

  ```cpp
  cout << setw(10) << right << 42 << endl; // 输出：右对齐
  cout << setw(10) << left << 42 << endl; // 输出：左对齐
  ```

### 头文件和命名空间

格式控制符通常需要包含头文件`<iomanip>`，并且使用`std::`命名空间。例如：

```cpp
#include <iomanip>
...
using namespace std; // 或者在使用时加上std::
```

## 数据输入和输出操作符

### 输出运算符`<<`

左移运算符`<<`用于将数据写入流。支持多种数据类型，并会自动调用相应的流插入函数。例如：

```cpp
int num = 10;
double pi = 3.14159;
string name = "Alice";
cout << "Number: " << num << ", Pi: " << pi << ", Name: " << name << endl;
```

```cpp
#include <iomanip>

// 金额格式化：固定两位小数，千位分隔符
double price = 12345.6789;
cout << fixed << setprecision(2) 
     << "总价：" << put_money(price) << endl;
// 输出：总价：$12,345.68

// 表格对齐：不同数据类型统一对齐
cout << setw(10) << left << "姓名" 
     << setw(8) << right << "年龄" << endl
     << setw(10) << left << "张三" 
     << setw(8) << right << 25 << endl
     << setw(10) << left << "李四" 
     << setw(8) << right << 30 << endl;
/*
输出：
姓名        年龄
张三          25
李四          30
*/
```

### 输入运算符`>>`

右移运算符`>>`用于从流中读取数据。支持基本类型，并且会跳过空白字符。例如：

```cpp
int age;
cout << "Enter your age: ";
cin >> age;
```

## 文件流

文件流允许你将数据读取到文件中或将数据写入文件。

### 4.1 `ifstream` 和 `ofstream`

- `ifstream`：文件输入流。
- `ofstream`：文件输出流。

```cpp
#include <fstream>
using namespace std;

int main() {
    ofstream outFile("output.txt");
    if (!outFile) {
        cerr << "无法打开文件!" << endl;
        return 1;
    }
    outFile << "Hello, File!" << endl;
    outFile.close();

    ifstream inFile("output.txt");
    if (!inFile) {
        cerr << "无法打开文件!" << endl;
        return 1;
    }
    string line;
    getline(inFile, line);
    cout << line << endl;
    inFile.close();
    return 0;
}
```

### 二进制文件操作

通过设置文件打开模式为二进制，可以处理二进制文件：

```cpp
ofstream outFile("data.bin", ios::binary);
outFile.write((const char*)&num, sizeof(num));
outFile.close();

ifstream inFile("data.bin", ios::binary);
inFile.read((char*)&readNum, sizeof(readNum));
inFile.close();
```

### 安全输入模板

```cpp
template<typename T>
T getInput(const string& prompt) {
    T value;
    while(true) {
        cout << prompt;
        if(cin >> value) break;
        cin.clear();
        cin.ignore(1024, '\n');
        cerr << "输入无效，请重试！\n";
    }
    cin.ignore(1024, '\n');  // 清除非数字字符
    return value;
}

// 使用示例
double price = getInput<double>("请输入价格：");
```

## 格式化输入输出

### 格式化输出示例

控制浮点数显示：

```cpp
double amount = 1234.5678;
cout << "Amount: " << fixed << setprecision(2) << amount << endl; // 输出：Amount: 1234.57
```

对齐和填充：

```cpp
cout << "Score: " << setw(10) << setfill('*') << left << 99 << endl; // 输出：Score: ********99
```

更加现代化的 `std::format`

```cpp
#include <format>

// 类型安全的格式化（比printf更安全！）
cout << format("圆周率：{:.2f}", 3.1415926); // 输出：圆周率：3.14

// 支持复杂格式化
cout << format("{:*^20}", "居中显示"); // 用*填充使文本居中
```

更加更加现代化的 `std::print`，你需要支持c++23和`<format>`（注意gcc-13+）：

```cpp
#include <print>

// 类型安全的格式化（比printf更安全！）
std::print("圆周率：{:.2f}", 3.1415926); // 输出：圆周率：3.14
// 支持复杂格式化
std::print("{:*^20}", "居中显示"); // 用*填充使文本居中
```

### 格式化输入示例

处理输入并跳过空白：

```cpp
int a, b;
cin >> a >> b; // 读取两个整数，跳过中间的空格
```

读取特定格式的数据：

```cpp
string date;
cin >> setw(5) >> date; // 读取5个字符
```

## 流操纵器

### 自定义流操纵器

```cpp
// 创建颜色控制操纵器
ostream& red(ostream& os) {
    return os << "\033[31m";
}

ostream& reset(ostream& os) {
    return os << "\033[0m";
}

cout << red << "错误信息！" << reset << endl;
```

### 状态保存与恢复

```cpp
// 保存原始格式
ios init(nullptr);
init.copyfmt(cout);

// 修改格式
cout << hex << showbase << 255;  // 输出0xff

// 恢复原始格式
cout.copyfmt(init);
cout << 255;  // 输出255
```

---

## 性能优化技巧

   **减少格式切换**：频繁修改格式标志会影响性能

   ```cpp
   // 优化前（多次格式设置）
   cout << setw(8) << a << setw(8) << b;

   // 优化后（统一设置）
   cout << setw(8);
   cout << a << b;
   ```

   **缓冲区管理**：手动刷新提升关键输出

   ```cpp
   cout << "重要消息..." << flush;  // 立即输出
   ```

   **流绑定**：同步输入输出流

   ```cpp
   cin.tie(&cout);  // 输入前自动刷新输出缓冲区
   ```

## 其他实用函数

### 改变字符串大小写

虽然C++标准库没有直接提供字符串大小写的转换函数，但可以使用自定义函数或利用平台特定的函数如`strupr`和`strlwr`（但在Windows环境下）。例如：

```cpp
char text[] = "hello, world!";
strupr(text); // 结果："HELLO, WORLD!"
strlwr(text); // 结果："hello, world!"
```

### 实用函数和方法

- `getline`：读取一行输入，包括空格。
- `tellg` 和 `seekg`：用于获取和设置输入流的位置指针。
- `tellp` 和 `seekp`：用于获取和设置输出流的位置指针。

## 常见问题和解决方法

### 输入多余的字符

当用`cin >>`读取输入时，多余的字符会被留在输入流中，可能导致后续的输入操作异常。处理这种情况可以使用`cin.ignore()`和`cin.clear()`。例如：

```cpp
int num;
cin >> num;
if (cin.fail()) {
    cin.clear(); // 重置错误状态
    cin.ignore(numeric_limits<streamsize>::max(), '\n'); // 忽略剩余字符
}
```

### 设置文本对齐

使用`setw`和`setfill`来对齐文本：

```cpp
cout << setw(20) << setfill(' ') << "Hello" << endl; // 左对齐
cout << setw(20) << setfill('-') << "World" << endl; // 填充字符为'-'，左对齐
```

### 浮点数精度问题

浮点数在存储时可能会出现精度损失，使用`fixed`和`setprecision`可以控制显示的精度。对于高精度需求，可以使用`long double`类型或转向定点数处理库。

### 文件操作异常处理

在文件操作中，应检查文件是否正确打开：

```cpp
ofstream outfile("data.txt");
if (!outfile) {
    cerr << "无法打开文件!" << endl;
    return 1;
}
```

## 小结

C++的IO流提供了一种强大的机制来处理输入输出，格式控制灵活多样，支持文件操作，且易于扩展。通过掌握这些基本概念和方法，您能够编写更加高效和可读的C++代码。

## 给新手的建议

1. **忘记printf/scanf**：用cout/cin更安全，不会出现`%d`与变量类型不匹配的崩溃
2. **优先使用RAII**：文件流对象会自动关闭，避免忘记fclose
3. **尝试现代特性**：std::format比拼接字符串更高效安全
4. **善用IDE提示**：输入`cout <<`时IDE会自动提示可用操作符

## 常见陷阱

```cpp
int a;
string s;

// 错误：混合使用时缓冲区问题
cin >> a;
getline(cin, s); // 会读取到换行符！

// 正确做法：
cin >> a;
cin.ignore(); // 清除换行符
getline(cin, s);
```

## 9. 示例代码

以下是一个综合示例，展示了C++ IO流的各种功能：

```cpp
#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <limits>
#include <cctype> // for tolower and toupper

using namespace std;

// 自定义大小写转换函数
void toUpper(char* str) {
    while (*str) {
        *str = toupper(*str);
        ++str;
    }
}

void toLower(char* str) {
    while (*str) {
        *str = tolower(*str);
        ++str;
    }
}

int main() {
    // 格式化输出
    double pi = 3.1415926535;
    cout << fixed << setprecision(2) << "Pi: " << pi << endl;
    cout << scientific << setprecision(4) << "Pi: " << pi << endl;

    // 对齐和填充
    cout << "Scores: " << setw(5) << setfill('*') << 100 << endl;

    // 文件写入
    ofstream outfile("test.txt");
    if (outfile.is_open()) {
        outfile << "这是一个测试文件。" << endl;
        outfile << "第二行内容。" << endl;
        outfile.close();
    } else {
        cerr << "无法打开文件!" << endl;
    }

    // 文件读取
    ifstream infile("test.txt");
    if (infile.is_open()) {
        string line;
        while (getline(infile, line)) {
            cout << line << endl;
        }
        infile.close();
    } else {
        cerr << "无法打开文件!" << endl;
    }

    // 字符串大小写转换
    char text[] = "Hello, World!";
    toUpper(text);
    cout << text << endl; // 输出：HELLO, WORLD!

    // 输入处理
    string input;
    cout << "输入一行文本: ";
    getline(cin, input);
    cout << "你输入的内容: " << input << endl;

    // 处理输入错误
    int num;
    cout << "输入一个整数: ";
    if (cin >> num) {
        cout << "你输入的整数是: " << num << endl;
    } else {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cerr << "输入错误，请输入整数!" << endl;
    }

    return 0;
}
```

这个示例涵盖了格式化输出、文件操作、字符串处理以及输入错误处理等内容，帮助您全面理解C++ IO流的使用方法。
