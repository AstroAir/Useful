# SCNLib 用户指南

## 目录

- 基本使用
- 错误处理和返回值
- 文件与标准流
- 格式字符串
- 扫描单个值
- Unicode 和宽字符源范围
- 用户自定义类型
- 本地化

---

## 基本使用

`scn::scan` 是用于从源范围或文件中扫描各种值的核心函数。源范围可以是字符串、容器（如 `std::string` 或 `std::vector<char>`）。该函数接受两个主要参数：源范围和格式字符串。

### 范围

源范围可以是任何具有开始和结束迭代器的对象。以下是可以作为源的常见类型：

- 字符串文字（如 `"hello"`）
- `std::string`
- `std::vector<char>`

### 格式字符串

格式字符串类似于 `printf` 的格式化，但使用大括号 `{}` 来表示每个要扫描的值。例如，`{}` 将被用于表示单个值，无需在格式字符串中指定类型。

### 例子

**扫描单个整数**

```cpp
auto result = scn::scan<int>("123", "{}");
auto i = result->value(); // 结果: i == 123
```

**扫描多个值**

```cpp
auto result = scn::scan<int, int>("0 1 2", "{} {}");
auto& [a, b] = result->values(); // 结果: a == 0, b == 1
// 暂不解析后面的 "2"
```

**扫描字符串**

```cpp
auto result = scn::scan<std::string>("hello world", "{}");
// 结果: result->value() == "hello"
```

这些示例展示了 `scnlib` 的效率与便利，相较于使用其他 C++ 输入方式，如 `std::istringstream` 或 `std::scanf`，`scnlib` 提供了更现代的接口和格式化能力。

---

## 错误处理和返回值

`scnlib` 不依赖于异常来处理错误，而是使用一种基于返回的错误处理机制。`scn::scan` 返回 `scn::scan_expected` 类型，它是一个类，封装了扫描的结果或错误信息。

### 检查错误

```cpp
auto result = scn::scan<int>("foo", "{}");
if (!result) {
    std::cout << result.error().msg() << '\n'; // 输出 "foo" 不是一个整数的错误信息。
}
```

### 部分成功

与 `std::scanf` 不同，`scnlib` 不支持部分成功的情况。如果扫描部分失败，整个操作将返回失败。

**示例**

```cpp
auto result = scn::scan<int, int>("123 foo", "{} {}");
if (!result) {
    // 这里 result 是 false
}
```

### 处理未解析部分

可以通过 `->range()` 方法访问未扫描的输入部分，返回一个子范围，以便后续处理。

**示例**

```cpp
auto result = scn::scan<int>("123 456"sv, "{}");
// result->value() == 123
// result->range() == " 456"  // 后续输入范围
```

---

## 文件与标准流

要从标准输入读取数据，可以使用 `scn::input` 和 `scn::prompt`。这两者的工作方式与 `scn::scan` 类似，但不需要输入范围作为参数，默认从 `stdin` 读取。

```cpp
if (auto result = scn::input<int>("{}")) {
    // 如果输入成功...
}
```

### 从文件读取

可以使用 `scn::scan` 直接从 `FILE *` 类型的文件中读取数据。在这种情况下，返回值不包含范围，而是文件本身。

```cpp
auto result = scn::scan<int>(stdin, "{}");
// result->file() == stdin
```

### 文件与标准流的同步

`scn::input`、`scn::prompt` 和 `scn::scan` 会自动与传递的文件（如 `std::cin`）进行同步，确保可与 C I/O 和 C++ iostreams 兼容使用。

---

## 格式字符串

格式字符串用来定制数据解析的具体方式，其语法基于 `{fmt}` 和 `std::format`。在此字符串中，`{}` 表示一个要解析的值，类型由 `scn::scan` 的模板参数决定。

### 控制空格的解析

所有空白字符在格式字符串中会被指示跳过。

```cpp
auto result = scn::scan<char, char>("x   y", "{} {}");
// 结果: a == 'x', b == 'y'
```

### 特殊字符处理

格式字符串中的其他字符被期望出现在源范围内并被丢弃，例如：

```cpp
auto result = scn::scan<char>("abc", "ab{}");
// result->value() == 'c'
```

### 使用标志

可以在格式字符串中使用标志，例如限制解析方式：

```cpp
// 接受十六进制浮点数
auto result = scn::scan<double>("1a.2f", "{:a}");
```

---

## 扫描单个值

对于简单的情况，可以使用 `scn::scan_value` 来快速扫描单个值，默认格式为 `{}`。

```cpp
auto result = scn::scan_value<int>("456");
// result->value() == 456
```

---

## Unicode 和宽字符源范围

`scnlib` 预期输入为 Unicode 编码。`char` 类型的输入假设为 UTF-8，`wchar_t` 类型的输入则假设为 UTF-16 或 UTF-32（取决于该类型的宽度）。

### 示例：扫描宽字符串

```cpp
auto result = scn::scan<std::wstring>(L"foo bar", L"{}");
// result->value() == L"foo"
```

### 混合字符类型扫描

可以在宽范围和窄范围之间进行扫描，`scnlib` 会在必要时进行 Unicode 转换。

```cpp
auto result2 = scn::scan<std::string>(result->range(), L"{}");
// result2->value() == "bar"
```

---

## 用户自定义类型

要支持自定义类型的扫描，需要特化 `scn::scanner` 结构体，并实现 `parse` 和 `scan` 两个成员函数。

### 示例：实现自定义扫描

```cpp
struct mytype {
    int i;
    double d;
};

template <>
struct scn::scanner<mytype, char> {
    template <typename ParseContext>
    constexpr auto parse(ParseContext& pctx) -> scan_expected<typename ParseContext::iterator>;

    template <typename Context>
    auto scan(mytype& val, Context& ctx) -> scan_expected<typename Context::iterator>;
};
```

### 使用其他扫描器

可以选择将扫描操作委托给其他已有的扫描器，或者通过继承来自定义解析选项。

---

## 本地化

默认情况下，`scnlib` 不会受全局 C 或 C++ 区域设置的影响，所有函数在 C 区域下运行。因此，处理浮点数时使用指定的小数点。

### 使用区域扫描

将 `std::locale` 传递给 `scn::scan` 可以实现本地化解析，但性能会相比于不使用区域设置更低。

```cpp
auto result = scn::scan(std::locale{"fi_FI.UTF-8"}, "2,73", "{:L}");
// result->value() == 2.73
```

> 注意：本地化的结果可能与未使用区域时的结果略有不同，这取决于平台和设计的限制。

---

GitHub • 报告问题 • 更新日志 • 许可证 • Doxygen 文档

如需获取其他详细信息和示例，请查阅文档的相关章节。有关具体实现的代码示例和更多应用场景，可以访问 `scnlib` 的 GitHub 页面或其他相关资源。
