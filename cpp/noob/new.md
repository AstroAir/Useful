
# C++中的内存管理：new&delete

> 本文详细讲解C++中new操作符的方方面面，从基础用法到C++20的最新特性，帮助你全面理解内存管理。

## 基础知识：认识new操作符

### 什么是new操作符？

在C++中，new是一个操作符而非函数，它用于在程序运行时在堆(也称自由存储区)上分配内存。与C语言中的malloc相比，new不仅分配内存，还会自动调用对象的构造函数。

许多初学者可能会混淆new和malloc，让我们看看它们的主要区别：

| 特性 | new | malloc |
|------|-----|--------|
| 类型 | 操作符 | 函数 |
| 返回类型 | 具体类型的指针 | void* |
| 内存不足时 | 抛出std::bad_alloc异常 | 返回NULL |
| 构造函数 | 自动调用 | 不调用 |
| 指定内存大小 | 自动计算 | 需手动指定 |
| 自定义能力 | 可以重载 | 不可重载 |

### new背后的魔法：执行步骤

当你写下`T* ptr = new T`这样简单的一行代码时，C++实际上在背后完成了三个关键步骤：

1. 调用operator new分配足够大的原始内存（大小至少为sizeof(T)）
2. 在分配的内存上调用T的构造函数，初始化对象
3. 返回指向新构造对象的指针（类型为T*）

如果用伪代码表示，大概是这样的：

```cpp
// new的内部实现类似于：
void* memory = operator new(sizeof(T));  // 步骤1: 分配内存
T* ptr = new(memory) T();                // 步骤2: 构造对象
return ptr;                              // 步骤3: 返回指针
```

而对应的`delete ptr`则会：

1. 调用ptr指向对象的析构函数
2. 调用operator delete释放内存

```cpp
// delete的内部实现类似于：
ptr->~T();                // 步骤1: 调用析构函数
operator delete(ptr);     // 步骤2: 释放内存
```

## 实战应用：new的基本用法

### 分配单个对象

在日常编程中，分配单个对象是最常见的操作：

```cpp
// 不带初始化的分配
int* p1 = new int;       // 分配未初始化的int（值不确定）

// 带初始化的分配
int* p2 = new int(42);   // 分配并初始化为42
int* p3 = new int();     // 分配并初始化为0
int* p4 = new int{};     // C++11起，与上面等价

// 分配自定义类型
class MyClass {
public:
    MyClass(int x) : value(x) { std::cout << "构造: " << value << std::endl; }
    ~MyClass() { std::cout << "析构: " << value << std::endl; }
private:
    int value;
};

MyClass* obj = new MyClass(10);  // 会调用MyClass的构造函数
// 用完后别忘了
delete obj;  // 会调用MyClass的析构函数
```

### 动态数组的分配

需要存储一组数据？动态数组是你的好帮手：

```cpp
// 分配int数组
int* arr1 = new int[5];       // 分配5个未初始化的int

// 分配并初始化数组
int* arr2 = new int[5]();     // 分配5个初始化为0的int
int* arr3 = new int[5]{};     // C++11起，与上面等价
int* arr4 = new int[5]{1,2,3}; // 前3个为1,2,3，后2个为0

// 从用户输入确定数组大小（C++11起支持）
int size;
std::cin >> size;
int* dynamicArr = new int[size];

// 释放数组（注意必须使用delete[]）
delete[] arr1;  // 正确的释放方式
// delete arr1;  // 错误！会导致未定义行为
```

### 多维数组的处理

二维数组的分配有两种常见方式：

```cpp
// 方法1：一次性分配（矩形内存块）
int (*arr2d1)[5] = new int[4][5];  // 4行5列

// 方法2：分段分配（更灵活，行长度可不同）
int arr2d2 = new int*[4];  // 先分配4个指针
for (int i = 0; i < 4; ++i) {
    arr2d2[i] = new int[5];  // 每个指针分配5个int
}

// 释放二维数组
// 方法1释放
delete[] arr2d1;

// 方法2释放（注意顺序）
for (int i = 0; i < 4; ++i) {
    delete[] arr2d2[i];  // 先释放每行
}
delete[] arr2d2;  // 再释放行指针数组
```

## 深入理解：内存分配的底层机制

### operator new的工作原理

好奇new是如何实现的？这里是一个简化版的operator new实现：

```cpp
// operator new的典型实现
void* operator new(std::size_t size) {
    void* ptr = std::malloc(size);
    if (ptr == nullptr) {
        throw std::bad_alloc();
    }
    return ptr;
}

// operator delete的典型实现
void operator delete(void* ptr) noexcept {
    std::free(ptr);
}
```

绝大多数C++实现中，operator new最终会调用C语言的malloc函数，不同之处在于内存分配失败时的处理方式。

### 自定义全局operator new/delete

你可以重载全局的operator new和delete，以实现自定义内存分配策略：

```cpp
#include <cstdlib>
#include <iostream>

void* operator new(std::size_t size) {
    std::cout << "自定义全局new: 分配 " << size << " 字节" << std::endl;
    void* ptr = std::malloc(size);
    if (ptr == nullptr) {
        throw std::bad_alloc();
    }
    return ptr;
}

void operator delete(void* ptr) noexcept {
    std::cout << "自定义全局delete: 释放内存" << std::endl;
    std::free(ptr);
}

void operator delete(void* ptr, std::size_t size) noexcept {
    std::cout << "自定义全局delete: 释放 " << size << " 字节" << std::endl;
    std::free(ptr);
}

int main() {
    int* p = new int(42);  // 会调用自定义的operator new
    delete p;              // 会调用自定义的operator delete
    return 0;
}
```

### 类特定的内存分配

你也可以为特定类自定义内存分配策略：

```cpp
#include <iostream>

class MyClass {
public:
    MyClass() { std::cout << "MyClass构造函数" << std::endl; }
    ~MyClass() { std::cout << "MyClass析构函数" << std::endl; }

    void* operator new(std::size_t size) {
        std::cout << "MyClass::operator new: " << size << "字节" << std::endl;
        return ::operator new(size);
    }

    void operator delete(void* ptr) noexcept {
        std::cout << "MyClass::operator delete" << std::endl;
        ::operator delete(ptr);
    }
};

int main() {
    MyClass* obj = new MyClass();
    delete obj;
    return 0;
}
```

这在内存池优化、内存使用跟踪等场景非常有用。

## new的多重面貌：各种形式的new

### 普通new：我们最熟悉的形式

```cpp
int* p = new int(42);  // 分配单个int，值为42
```

### 数组new：处理多个元素

```cpp
int* arr = new int[10];  // 分配10个连续的int

// C++11起可以使用初始化列表
int* arr2 = new int[5]{1, 2, 3, 4, 5};

// 使用完毕后
delete[] arr;
delete[] arr2;
```

### placement new：在指定位置构造对象

placement new允许在已分配的内存上构造对象，不进行内存分配。这是new操作符一个不那么为人所知但非常强大的形式：

```cpp
#include <iostream>
#include <new> // clangd 可能会报未使用的警告，可以直接忽略

class MyClass {
public:
    MyClass() { std::cout << "MyClass constructed." << std::endl; }
    ~MyClass() { std::cout << "MyClass destructed." << std::endl; }
};

int main() {
    char buffer[sizeof(MyClass)];           // 预先分配的内存
    MyClass* obj = new (buffer) MyClass();  // 在buffer上构造MyClass对象

    // 使用完毕后，显式调用析构函数（不能使用delete，因为内存不是用new分配的）
    obj->~MyClass();
}

```

placement new的主要用途：

- 实现高性能内存池
- 避免内存分配的开销（特别是在实时系统中）
- 需要精确控制对象位置时（如共享内存、内存映射IO）

### nothrow new：不抛出异常的分配

如果你不想处理异常，可以使用nothrow new：

```cpp
#include <iostream>
#include <new>

int main() {
    // 失败时不抛出异常，而是返回nullptr
    int* p = new (std::nothrow) int(42);
    if (p == nullptr) {
        // 处理内存分配失败
        std::cout << "内存分配失败" << std::endl;
    }
    else {
        std::cout << "分配的值: " << *p << std::endl;
        delete p;  // 释放内存
    }
}

```

### 带自定义参数的placement new

你甚至可以创建带有自定义参数的placement new：

```cpp
#include <iostream>

void* operator new(std::size_t size, const char* file, int line) {
    std::cout << "Allocation at " << file << ":" << line << std::endl;
    return ::operator new(size);
}

#define MY_NEW new (__FILE__, __LINE__)

int main() {
    int* p = MY_NEW int(42);
    std::cout << "分配的值: " << *p << std::endl;
    delete p;
}

```

这在调试内存问题时特别有用。

## C++演化：各版本中的new改进

### C++11：现代C++的奠基石

C++11对new操作符带来了这些改进：

#### 统一初始化语法

```cpp
// 使用花括号初始化
int* p = new int{42};
double* d = new double{3.14};

// 数组初始化
int* arr = new int[3]{1, 2, 3};
```

#### 对齐内存分配

```cpp
// 使用alignas指定对齐要求
struct alignas(16) AlignedStruct {
    int data[4];
};

AlignedStruct* as = new AlignedStruct();  // 16字节对齐
```

#### 可变参数模板支持

```cpp
template<typename T, typename... Args>
T* createObject(Args&&... args) {
    return new T(std::forward<Args>(args)...);
}

// 使用
class Test {
public:
    Test(int a, double b, std::string c) {}
};

Test* t = createObject<Test>(1, 2.5, "test");
```

### C++14：更多便利性改进

C++14添加了std::make_unique，使创建unique_ptr更安全：

```cpp
auto p = std::make_unique<int>(42);  // 替代 unique_ptr<int>(new int(42))，谁知道标准为啥一开始忘了加这个？
```

### C++17：内存管理的进一步标准化

C++17主要带来了这些改进：

#### 对齐内存分配标准化

C++17进一步标准化了over-aligned类型的new和delete操作符：

```cpp
struct alignas(64) BigAligned {
    char data[64];
};

BigAligned* ptr = new BigAligned();
```

#### 多态内存资源(PMR)

C++17引入了多态内存资源(PMR)库，允许容器使用自定义内存分配策略：

```cpp
#include <memory_resource>

int main() {
    // 使用栈上缓冲区作为内存源
    char buffer[1024];
    std::pmr::monotonic_buffer_resource pool{buffer, sizeof(buffer)};
    
    // 使用自定义内存资源的容器
    std::pmr::vector<int> vec{&pool};
    for (int i = 0; i < 100; ++i) {
        vec.push_back(i);  // 从自定义内存池分配
    }
}
```

## C++20新特性：内存分配的革新

> 如果想要测试下面的特性，你需要一个现代化的c++编译器，dev-cpp承担不了重任

### constexpr new：编译期动态内存

C++20带来了一个重大突破：new和delete操作符可以在constexpr上下文中使用。这意味着可以在编译期进行动态内存分配和释放！

```cpp
#include <iostream>

constexpr int getValue() {
    int* p = new int(42);  // 编译期内存分配！
    int value = *p;
    delete p;  // 编译期内存释放
    return value;
}

int main() {
    constexpr int result = getValue();  // 编译期计算
    static_assert(result == 42);
    
    std::cout << "编译期计算结果: " << result << std::endl;
    return 0;
}
```

这个特性有一些限制：

- 所有动态分配的内存必须在同一个constexpr评估中释放
- 不能有内存泄漏
- 只能用于直接初始化的字面量类型

### PMR库的增强

C++20进一步完善了多态内存资源(PMR)库：

```cpp
#include <memory_resource>
#include <string>
#include <vector>
#include <iostream>

int main() {
    // 使用同步池内存资源
    std::pmr::synchronized_pool_resource pool;

    // 使用pmr字符串和容器
    std::pmr::string str{"Hello PMR", &pool};

    std::pmr::vector<std::pmr::string> vec{&pool};
    vec.push_back(std::pmr::string{"C++20", &pool});
    vec.push_back(std::move(str));

    // 所有内存来自同一个池

    for (const auto& s : vec) {
        std::cout << s << " ";
    }
}
```

### 协程与内存管理

C++20引入的协程也与内存管理密切相关：

```cpp
#include <coroutine>
#include <iostream>

struct task {
    struct promise_type {
        task get_return_object() { return {}; }
        std::suspend_never initial_suspend() { return {}; }
        std::suspend_never final_suspend() noexcept { return {}; }
        void return_void() {}
        void unhandled_exception() {}
    };
};

task example() {
    // 协程内部的内存分配由编译器管理
    int* data = new int[1000];

    for (int i = 0; i < 1000; i++) {
        data[i] = i;
    }

    std::cout << "Data: ";
    for (int i = 0; i < 10; i++) {
        std::cout << data[i] << " ";
    }
    std::cout << std::endl;

    delete[] data;
    co_return;
}

int main() {
    example();
    return 0;
}
```

协程框架内部需要高效的内存管理来存储协程状态，这给C++内存管理带来了新的挑战和机遇。

## 内存管理最佳实践

### 使用智能指针，告别手动管理

总是优先使用智能指针而非裸指针：

```cpp
// 不好的做法
void badFunction() {
    MyClass* obj = new MyClass();
    // 如果这里发生异常，内存将泄漏
    delete obj;  // 可能忘记执行
}

// 好的做法
void goodFunction() {
    auto obj = std::make_unique<MyClass>();
    // 不需要手动delete，离开作用域时自动释放
}

// shared_ptr用于共享所有权
std::shared_ptr<MyClass> sharedObj = std::make_shared<MyClass>();
```

### 防止内存泄漏的常见陷阱

```cpp
// 危险模式：忘记delete
void leakyFunction() {
    int* array = new int[1000];
    // 忘记 delete[] array;
} // 内存泄漏!

// 忘记使用delete[]释放数组
void wrongDeleteFunction() {
    int* array = new int[1000];
    delete array;  // 错误!应该使用delete[]
}

// 正确做法
void correctFunction() {
    auto array = std::make_unique<int[]>(1000);
    // 自动正确释放
}
```

### 异常安全：资源获取即初始化(RAII)

```cpp
class Resource {
public:
    Resource() { std::cout << "资源获取" << std::endl; }
    ~Resource() { std::cout << "资源释放" << std::endl; }
};

// 不安全的方式
void unsafeFunction() {
    Resource* r1 = new Resource();
    Resource* r2 = new Resource();  // 如果这里抛出异常
    
    // 处理r1和r2
    
    delete r2;
    delete r1;  // 如果前面有异常，这里不会执行
}

// 安全的方式
void safeFunction() {
    auto r1 = std::make_unique<Resource>();
    auto r2 = std::make_unique<Resource>();
    
    // 即使有异常，r1和r2也会被正确释放
}
```

### 大内存分配的技巧

当需要分配大块内存时：

```cpp
// 尝试分配大内存时，考虑使用nothrow new
void allocateLargeMemory() {
    const size_t largeSize = 1024 * 1024 * 1024;  // 1GB
    
    // nothrow new
    int* largeArray = new(std::nothrow) int[largeSize];
    if (largeArray == nullptr) {
        std::cout << "内存分配失败，优雅处理" << std::endl;
        return;
    }
    
    // 使用内存
    
    delete[] largeArray;
}
```

## 实战案例：内存管理在实际项目中的应用

### 自定义内存池：提升性能的秘密武器

当程序需要频繁创建和销毁小对象时，自定义内存池可以显著提升性能：

```cpp
#include <iostream>
#include <vector>
#include <cstdlib>

class MemoryPool {
private:
    struct Block {
        void* data;
        bool used;
    };
    
    std::vector<Block> blocks;
    size_t blockSize;
    
public:
    MemoryPool(size_t size, size_t count) : blockSize(size) {
        for (size_t i = 0; i < count; ++i) {
            void* data = std::malloc(blockSize);
            blocks.push_back({data, false});
        }
    }
    
    ~MemoryPool() {
        for (auto& block : blocks) {
            std::free(block.data);
        }
    }
    
    void* allocate() {
        for (auto& block : blocks) {
            if (!block.used) {
                block.used = true;
                return block.data;
            }
        }
        return nullptr;  // 内存池已满
    }
    
    void deallocate(void* ptr) {
        for (auto& block : blocks) {
            if (block.data == ptr) {
                block.used = false;
                return;
            }
        }
    }
};

// 使用内存池的类
class PooledObject {
private:
    int data;
    static MemoryPool pool;
    
public:
    PooledObject(int val) : data(val) {
        std::cout << "构造: " << data << std::endl;
    }
    
    ~PooledObject() {
        std::cout << "析构: " << data << std::endl;
    }
    
    // 重载operator new和delete使用我们的内存池
    static void* operator new(size_t size) {
        return pool.allocate();
    }
    
    static void operator delete(void* ptr) {
        pool.deallocate(ptr);
    }
};

// 初始化静态内存池
MemoryPool PooledObject::pool(sizeof(PooledObject), 100);
```

### 序列化与反序列化：placement new的绝佳用例

placement new在序列化领域有着广泛应用：

```cpp
#include <fstream>
#include <iostream>
#include <new>

class Serializable {
public:
    int x;
    double y;
    char data[16];

    Serializable(int _x = 0, double _y = 0.0) : x(_x), y(_y) {
        std::fill(data, data + 16, 'A');
    }

    void serialize(std::ostream& os) const {
        os.write(reinterpret_cast<const char*>(this), sizeof(*this));
    }

    static Serializable* deserialize(std::istream& is) {
        char* buffer = new char[sizeof(Serializable)];
        is.read(buffer, sizeof(Serializable));

        if (!is) {
            delete[] buffer;
            return nullptr;
        }

        return reinterpret_cast<Serializable*>(buffer);
    }

    void operator delete(void* ptr) {
        char* charPtr = reinterpret_cast<char*>(ptr);
        delete[] charPtr;
    }
};

int main() {
    Serializable obj(42, 3.14);

    std::ofstream ofs("data.bin", std::ios::binary);
    if (!ofs) {
        std::cerr << "无法打开文件进行写入" << std::endl;
        return 1;
    }
    obj.serialize(ofs);
    ofs.close();

    std::ifstream ifs("data.bin", std::ios::binary);
    if (!ifs) {
        std::cerr << "无法打开文件进行读取" << std::endl;
        return 1;
    }

    Serializable* newObj = Serializable::deserialize(ifs);
    if (newObj) {
        std::cout << "反序列化成功: x = " << newObj->x << ", y = " << newObj->y
                  << std::endl;
        delete newObj;
    } else {
        std::cerr << "反序列化失败" << std::endl;
    }

    return 0;
}
```

---

通过本文，你应该已经对C++中的new操作符有了全面的了解。从基础用法到C++20的最新特性，从内存泄漏的防范到高性能内存池的实现，这些知识将帮助你写出更健壮、更高效的C++代码。

记住：在现代C++中，直接使用new和delete的场景正在减少，智能指针和RAII技术是更安全的选择。但理解底层内存分配机制依然是C++程序员的必备技能，特别是在需要优化性能或处理特殊场景时。

你有什么关于C++内存管理的问题或经验？欢迎在评论区分享！
