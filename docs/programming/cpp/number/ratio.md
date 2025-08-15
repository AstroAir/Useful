# std::ratio

`std::ratio` 是 C++11 中引入的一个模板类，位于 `<ratio>` 头文件中。它用于表示有理数，特别是用于编译时的分数值（即整数比），主要应用于定时、单位转换和静态计算等场景。`std::ratio` 利用模板参数来定义分数的分子和分母，提供了多种操作和特性，极大地方便了编译时计算。

## 基本用法

`std::ratio` 通过分子和分母的整数值（通常为负数和正数）进行定义。基本的定义如下：

```cpp
#include <ratio>

std::ratio<numerator, denominator>
```

其中 `numerator` 和 `denominator` 是整数类型的模板参数。例如，`std::ratio<1, 2>` 表示 1/2。

## 主要特性

- **编译时常量**：`std::ratio` 的值在编译时就已确定，因此对于性能极为友好。
- **加法与减法**：可以对 `std::ratio` 进行加法和减法操作。
- **乘法与除法**：同样支持乘法和除法操作。
- **绝对值**：支持获取分数的绝对值。
- **类型别名**：提供了多个别名，例如：
  - `std::ratio_add`：用于相加。
  - `std::ratio_subtract`：用于相减。
  - `std::ratio_multiply`：用于相乘。
  - `std::ratio_divide`：用于相除。

## 示例代码

### 示例 1：基本用法

```cpp
#include <iostream>
#include <ratio>

int main() {
    using Rat1 = std::ratio<1, 2>;
    using Rat2 = std::ratio<3, 4>;

    std::cout << "Rat1: " << Rat1::num << "/" << Rat1::den << std::endl; // 输出：1/2
    std::cout << "Rat2: " << Rat2::num << "/" << Rat2::den << std::endl; // 输出：3/4

    return 0;
}
```

### 示例 2：加法与减法

```cpp
#include <iostream>
#include <ratio>

int main() {
    using Rat1 = std::ratio<1, 2>;
    using Rat2 = std::ratio<3, 4>;

    using Sum = std::ratio_add<Rat1, Rat2>; // 1/2 + 3/4

    std::cout << "Sum: " << Sum::num << "/" << Sum::den << std::endl; // 输出：5/4

    return 0;
}
```

### 示例 3：乘法与除法

```cpp
#include <iostream>
#include <ratio>

int main() {
    using Rat1 = std::ratio<2, 3>;
    using Rat2 = std::ratio<4, 5>;

    using Product = std::ratio_multiply<Rat1, Rat2>; // (2/3) * (4/5)
    using Quotient = std::ratio_divide<Rat1, Rat2>; // (2/3) / (4/5)

    std::cout << "Product: " << Product::num << "/" << Product::den << std::endl; // 输出：8/15
    std::cout << "Quotient: " << Quotient::num << "/" << Quotient::den << std::endl; // 输出：10/12

    return 0;
}
```

### 示例 4：绝对值和转换

```cpp
#include <iostream>
#include <ratio>

int main() {
    using Rat = std::ratio<-3, 4>; // -3/4

    using AbsRat = std::ratio_abs<Rat>; // 3/4

    std::cout << "Absolute Ratio: " << AbsRat::num << "/" << AbsRat::den << std::endl; // 输出：3/4

    return 0;
}
```

## 应用场景

- **单位转换**：在涉及到物理量的计算时，例如时间、速度等，可以使用 `std::ratio` 来表示单位，比如秒、毫秒、微秒之间的转换。
- **编译时计算**：由于 `std::ratio` 在编译期确定值，所以适合用于需要高性能的场合。
- **参数化设计**：可用于模板编程中，提供通用的数值处理能力。

## 总结

`std::ratio` 是一个强大的工具，使编译时进行有理数计算变得简单而高效。它为开发者提供了一种灵活的方式来处理分数，在单位转换、算法设计等领域都有广泛的应用。通过运用 `std::ratio` 和相关操作，能够提升程序的性能和可维护性。
