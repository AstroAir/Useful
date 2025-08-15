# C# 内置数据结构概述

C# 作为一种强类型的编程语言，内置了多种数据结构，帮助开发者高效地存储、访问和管理数据。这些数据结构主要包含在 `System.Collections`、`System.Collections.Generic` 和 `System.Collections.Concurrent` 命名空间中。下面详细介绍几种常用的 C# 内置数据结构。

## 1. 数组（Array）

数组是 C# 中最基本的集合类型，用于存储一组固定大小的同类型元素。数组中的元素通过索引访问，索引从 0 开始。

### 特点

- **固定大小**：数组的大小在创建时确定，不能动态调整。
- **支持多维数组**：C# 支持一维数组、二维数组和多维数组。
- **性能高**：由于数组的内存是连续的，因此访问速度非常快。

### 示例

```csharp
int[] numbers = new int[5]; // 创建一个包含5个元素的数组
numbers[0] = 10;             // 通过索引访问元素
numbers[1] = 20;             // 设置第二个元素
numbers[2] = 30;             // 设置第三个元素
Console.WriteLine(numbers[0]); // 输出: 10
Console.WriteLine(numbers[1]); // 输出: 20
Console.WriteLine(numbers[2]); // 输出: 30

// 使用循环遍历数组
for (int i = 0; i < numbers.Length; i++)
{
    Console.WriteLine($"Element at index {i}: {numbers[i]}");
}
// 输出:
// Element at index 0: 10
// Element at index 1: 20
// Element at index 2: 30
```

## 2. 列表（List）

`List<T>` 是一种动态数组，它在 `System.Collections.Generic` 命名空间中定义。与数组不同，`List<T>` 可以根据需要动态增长或缩小。

### 特点

- **动态调整大小**：当元素数量超过容量时，列表会自动扩展。
- **提供丰富的操作方法**：例如 `Add()`、`Remove()`、`Insert()`、`Sort()` 等。

### 示例

```csharp
List<int> numbers = new List<int>();
numbers.Add(1);  // 添加元素 1
numbers.Add(2);  // 添加元素 2
numbers.Add(3);  // 添加元素 3
numbers.Remove(1); // 移除元素 1
numbers.Insert(0, 4); // 在索引 0 插入元素 4
numbers.Sort(); // 排序列表
Console.WriteLine(string.Join(", ", numbers)); // 输出: 2, 3, 4

// 使用循环遍历列表
foreach (var number in numbers)
{
    Console.WriteLine(number);
}
// 输出:
// 2
// 3
// 4
```

## 3. 字典（Dictionary<TKey, TValue>）

`Dictionary<TKey, TValue>` 是键值对形式的数据结构，允许根据键快速查找对应的值。它使用哈希表作为底层实现。

### 特点

- **快速查找**：基于哈希算法，查找键的操作具有 O(1) 的平均时间复杂度。
- **键唯一**：每个键在字典中必须是唯一的。

### 示例

```csharp
Dictionary<string, int> ages = new Dictionary<string, int>();
ages.Add("Alice", 30); // 添加键值对
ages.Add("Bob", 25);
ages["Charlie"] = 35; // 另一种添加方式

// 使用 TryGetValue 来安全获取值
if (ages.TryGetValue("Alice", out int aliceAge))
{
    Console.WriteLine($"Alice's age is {aliceAge}"); // 输出: Alice's age is 30
}

// 遍历字典
foreach (var kvp in ages)
{
    Console.WriteLine($"{kvp.Key}: {kvp.Value}");
}
// 输出:
// Alice: 30
// Bob: 25
// Charlie: 35
```

## 4. 队列（Queue）

`Queue<T>` 是一种先进先出（FIFO）的数据结构，意味着第一个进入队列的元素将是第一个被移除的。

### 特点

- **FIFO 原则**：适用于任务排队、消息传递等场景。
- **提供 `Enqueue()` 方法添加元素，`Dequeue()` 方法移除并返回队头元素。**

### 示例

```csharp
Queue<string> tasks = new Queue<string>();
tasks.Enqueue("Task 1"); // 添加任务 1
tasks.Enqueue("Task 2"); // 添加任务 2
tasks.Enqueue("Task 3"); // 添加任务 3

while (tasks.Count > 0)
{
    string nextTask = tasks.Dequeue(); // 移除并返回队头元素
    Console.WriteLine($"Processing {nextTask}"); // 输出: Processing Task 1, Processing Task 2, Processing Task 3
}
```

## 5. 栈（Stack）

`Stack<T>` 是一种后进先出（LIFO）的数据结构，意味着最后一个进入栈的元素将是第一个被移除的。

### 特点

- **LIFO 原则**：适用于递归、逆序操作等场景。
- **提供 `Push()` 方法添加元素，`Pop()` 方法移除并返回栈顶元素。**

### 示例

```csharp
Stack<int> stack = new Stack<int>();
stack.Push(1); // 添加元素 1
stack.Push(2); // 添加元素 2
stack.Push(3); // 添加元素 3

while (stack.Count > 0)
{
    int top = stack.Pop(); // 移除并返回栈顶元素
    Console.WriteLine(top); // 输出: 3, 2, 1
}
```

## 6. 集合（HashSet）

`HashSet<T>` 是一种无序集合，主要用于存储不重复的元素。它基于哈希表实现，提供快速的添加、删除和查找操作。

### 特点

- **元素唯一**：集合中的元素不会重复。
- **查找速度快**：由于使用哈希表，查找操作非常高效。

### 示例

```csharp
HashSet<int> numbers = new HashSet<int>();
numbers.Add(1); // 添加元素 1
numbers.Add(2); // 添加元素 2
numbers.Add(2); // 尝试添加重复元素 2（不会添加）

Console.WriteLine(numbers.Count); // 输出: 2

// 使用循环遍历集合
foreach (var number in numbers)
{
    Console.WriteLine(number); // 输出: 1, 2
}
```

## 7. 链表（LinkedList）

`LinkedList<T>` 是一种双向链表数据结构，每个节点包含一个数据项和指向前后节点的引用。与 `List<T>` 不同，它允许高效的插入和删除操作，尤其是在列表中间。

### 特点

- **双向链表**：每个节点包含对前一个和后一个节点的引用。
- **适合频繁插入和删除操作**：在列表的任意位置插入或删除元素的效率较高。

### 示例

```csharp
LinkedList<string> words = new LinkedList<string>();
words.AddLast("Hello"); // 添加到末尾
words.AddLast("World"); // 添加到末尾
words.AddFirst("Start"); // 添加到开头

// 遍历链表
foreach (var word in words)
{
    Console.WriteLine(word); // 输出: Start, Hello, World
}
```

## 8. 并发集合（Concurrent Collections）

在多线程环境中使用时，普通集合可能会导致数据竞争和不一致。为了解决这个问题，C# 提供了一些线程安全的并发集合，它们位于 `System.Collections.Concurrent` 命名空间中，例如：

- `ConcurrentDictionary<TKey, TValue>`：线程安全的字典。
- `ConcurrentQueue<T>`：线程安全的队列。
- `ConcurrentStack<T>`：线程安全的栈。
- `BlockingCollection<T>`：提供生产者/消费者模式的线程安全集合。

### 示例

```csharp
ConcurrentDictionary<string, int> concurrentDict = new ConcurrentDictionary<string, int>();
concurrentDict.TryAdd("key1", 1); // 尝试添加键值对
concurrentDict.TryAdd("key2", 2);
int value = concurrentDict.GetOrAdd("key1", 2); // 获取或添加键值
Console.WriteLine(value); // 输出: 1

// 遍历字典
foreach (var kvp in concurrentDict)
{
    Console.WriteLine($"{kvp.Key}: {kvp.Value}");
}
// 输出:
// key1: 1
// key2: 2
```

## 9. SortedList<TKey, TValue>

`SortedList<TKey, TValue>` 是一种根据键自动排序的键值对集合。它结合了数组和哈希表的特点，能够通过键进行高效查找，同时保证键按顺序排列。

### 特点

- **自动排序**：键会根据比较规则进行自动排序。
- **二分查找**：可以快速定位元素。

### 示例

```csharp
SortedList<int, string> sortedList = new SortedList<int, string>();
sortedList.Add(2, "Two");
sortedList.Add(1, "One");
sortedList.Add(3, "Three");

foreach (var kvp in sortedList)
{
    Console.WriteLine($"{kvp.Key}: {kvp.Value}");
}
// 输出:
// 1: One
// 2: Two
// 3: Three
```

## 10. SortedSet

`SortedSet<T>` 是一种自动排序且无重复的集合，它结合了 `HashSet<T>` 和 `SortedList<TKey, TValue>` 的特点。它基于红黑树实现。

### 特点

- **无重复元素**：像 `HashSet<T>` 一样，元素不能重复。
- **自动排序**：像 `SortedList<T>` 一样，集合中的元素保持排序。

### 示例

```csharp
SortedSet<int> sortedSet = new SortedSet<int>();
sortedSet.Add(3);
sortedSet.Add(1);
sortedSet.Add(2);

foreach (var number in sortedSet)
{
    Console.WriteLine(number); // 输出: 1, 2, 3
}
```

## C# 内置数据结构扩展

C# 中的内置数据结构非常丰富，除了前面介绍的几种常见数据结构外，还有更多数据结构适用于不同的场景。以下是更多 C# 内置的数据结构，以及它们的特点和适用场景。

## 11. BitArray

`BitArray` 是一种用于高效存储和处理布尔值集合的数据结构，它使用位表示法存储布尔值，因此在存储空间和效率上有明显优势。

### 特点

- **节省空间**：每个布尔值仅用 1 位存储。
- **可以执行位操作**：支持按位与 (AND)、按位或 (OR)、按位异或 (XOR) 等操作。

### 示例

```csharp
BitArray bitArray = new BitArray(8); // 创建一个长度为8的BitArray
bitArray[0] = true;
bitArray[1] = false;
bitArray[2] = true;

Console.WriteLine(bitArray[0]); // 输出: True
Console.WriteLine(bitArray[1]); // 输出: False

// 使用位操作
bitArray.Set(3, true); // 设置第 3 位为 true
Console.WriteLine(bitArray); // 输出: {True, False, True, True, False, False, False, False}
```

## 12. NameValueCollection

`NameValueCollection` 是一种特殊的键值对集合，支持在同一个键下存储多个值。它属于 `System.Collections.Specialized` 命名空间。

### 特点

- **键可以重复**：同一个键可以存储多个值。
- **适合处理 HTTP 请求头、查询字符串等需要一对多关系的数据**。

### 示例

```csharp
NameValueCollection collection = new NameValueCollection();
collection.Add("Name", "Alice");
collection.Add("Name", "Bob"); // 同一键下存储多个值
collection.Add("Age", "30");
collection.Add("Age", "25"); // 同一键下存储多个值

Console.WriteLine(string.Join(", ", collection.GetValues("Name"))); // 输出: Alice, Bob
Console.WriteLine(string.Join(", ", collection.GetValues("Age"))); // 输出: 30, 25
```

## 13. Queue

除了泛型版本的 `Queue<T>`，C# 还有非泛型版本的 `Queue`，用于存储非类型安全的对象集合。

### 特点

- **适合不需要类型安全的场景**。
- **与 `Queue<T>` 一样，遵循先进先出（FIFO）的原则**。

### 示例

```csharp
Queue queue = new Queue();
queue.Enqueue(1);
queue.Enqueue("Hello");
queue.Enqueue(3.14);

while (queue.Count > 0)
{
    var item = queue.Dequeue(); // 移除并返回队头元素
    Console.WriteLine(item); // 输出: 1, Hello, 3.14
}
```

## 14. Stack

类似于 `Queue`，C# 也提供了非泛型版本的 `Stack`，用于存储非类型安全的对象集合。

### 特点

- **不限定存储的对象类型**。
- **遵循后进先出（LIFO）的原则**。

### 示例

```csharp
Stack stack = new Stack();
stack.Push(1);
stack.Push("Hello");
stack.Push(3.14);

while (stack.Count > 0)
{
    var item = stack.Pop(); // 取出最后入栈的元素
    Console.WriteLine(item); // 输出: 3.14, Hello, 1
}
```

## 15. Hashtable

`Hashtable` 是一种非泛型的键值对集合，键和值都可以是任意对象类型。它与 `Dictionary<TKey, TValue>` 类似，但不具备类型安全性，适用于较早版本的 C# 项目。

### 特点

- **键和值都是对象类型**。
- **提供快速查找键的能力，但效率不如 `Dictionary<TKey, TValue>`**。

### 示例

```csharp
Hashtable hashtable = new Hashtable();
hashtable.Add("Name", "Alice");
hashtable.Add(1, 100);
hashtable.Add("Age", 30);

Console.WriteLine(hashtable["Name"]); // 输出: Alice
Console.WriteLine(hashtable[1]); // 输出: 100
Console.WriteLine(hashtable["Age"]); // 输出: 30
```

## 16. SortedDictionary<TKey, TValue>

`SortedDictionary<TKey, TValue>` 是 `Dictionary<TKey, TValue>` 的变体，它在添加键值对时自动对键进行排序。它基于红黑树实现。

### 特点

- **自动排序**：键会按照自然顺序或自定义的比较规则进行排序。
- **查找、添加、删除操作的时间复杂度为 O(log n)，比 `Dictionary<TKey, TValue>` 略慢**。

### 示例

```csharp
SortedDictionary<int, string> sortedDict = new SortedDictionary<int, string>();
sortedDict.Add(2, "Two");
sortedDict.Add(1, "One");
sortedDict.Add(3, "Three");

foreach (var kvp in sortedDict)
{
    Console.WriteLine($"{kvp.Key}: {kvp.Value}");
}
// 输出:
// 1: One
// 2: Two
// 3: Three
```

## 17. SortedList<TKey, TValue>

`SortedList<TKey, TValue>` 类似于 `SortedDictionary<TKey, TValue>`，但它在内部使用数组而非树结构。因此在小规模数据集上的访问速度更快，但插入和删除操作较慢。

### 特点

- **按照键的顺序存储元素**。
- **访问和查找速度快，但插入和删除效率较低**。

### 示例

```csharp
SortedList<int, string> sortedList = new SortedList<int, string>();
sortedList.Add(1, "One");
sortedList.Add(3, "Three");
sortedList.Add(2, "Two");

foreach (var kvp in sortedList)
{
    Console.WriteLine($"{kvp.Key}: {kvp.Value}");
}
// 输出:
// 1: One
// 2: Two
// 3: Three
```

## 18. ArrayList

`ArrayList` 是一种非类型安全的动态数组，可以存储任何类型的对象。在泛型引入之前，它是最常用的动态集合之一。

### 特点

- **动态调整大小**。
- **不限定元素类型，但不如 `List<T>` 类型安全**。

### 示例

```csharp
ArrayList arrayList = new ArrayList();
arrayList.Add(1);
arrayList.Add("Hello");
arrayList.Add(3.14);

foreach (var item in arrayList)
{
    Console.WriteLine(item); // 输出: 1, Hello, 3.14
}
```

## 19. HybridDictionary

`HybridDictionary` 是一种结合了 `ListDictionary` 和 `Hashtable` 优点的数据结构。当集合较小时，它使用 `ListDictionary`，当集合较大时，它会切换为 `Hashtable` 以提高性能。

### 特点

- **适用于大小未知的集合**。
- **在小数据量时节省内存，大数据量时提供高效查找**。

### 示例

```csharp
HybridDictionary hybridDict = new HybridDictionary();
hybridDict.Add("Key1", "Value1");
hybridDict.Add("Key2", "Value2");

Console.WriteLine(hybridDict["Key1"]); // 输出: Value1
Console.WriteLine(hybridDict["Key2"]); // 输出: Value2
```

## 20. ListDictionary

`ListDictionary` 是一种内部使用链表实现的字典结构，适用于小规模的键值对集合。

### 特点

- **适用于存储少量键值对的场景**。
- **插入和查找速度较慢（O(n)），但在少量数据时表现优异**。

### 示例

```csharp
ListDictionary listDict = new ListDictionary();
listDict.Add("Key1", "Value1");
listDict.Add("Key2", "Value2");

Console.WriteLine(listDict["Key1"]); // 输出: Value1
Console.WriteLine(listDict["Key2"]); // 输出: Value2
```

## 21. OrderedDictionary

`OrderedDictionary` 保留键值对的插入顺序，并允许通过索引访问元素。

### 特点

- **保留插入顺序**：不像 `Dictionary`，它按插入顺序存储元素。
- **允许根据索引访问元素**：可以像数组一样访问。

### 示例

```csharp
OrderedDictionary orderedDict = new OrderedDictionary();
orderedDict.Add("Key1", "Value1");
orderedDict.Add("Key2", "Value2");

Console.WriteLine(orderedDict[0]); // 根据索引访问，输出: Value1
Console.WriteLine(orderedDict[1]); // 根据索引访问，输出: Value2
```

## 22. LinkedList

除了前面提到的 `LinkedList<T>`，C# 中还提供了双向链表的实现，这在频繁插入、删除操作的场景下非常高效。

### 特点

- **适合频繁在列表中间插入和删除操作**。
- **节点包含对前后节点的引用**。

### 示例

```csharp
LinkedList<int> linkedList = new LinkedList<int>();
linkedList.AddLast(1);
linkedList.AddLast(2);
linkedList.AddFirst(0); // 在开头添加元素

Console.WriteLine(string.Join(", ", linkedList)); // 输出: 0, 1, 2
```

## 23. BlockingCollection

`BlockingCollection<T>` 是一种线程安全的数据结构，特别适合生产者/消费者模型。它可以用于多个线程之间安全地共享数据。

### 特点

- **提供线程安全的添加和移除操作**。
- **支持限量的队列，防止过度生产导致内存溢出**。

### 示例

```csharp
BlockingCollection<int> blockingCollection = new BlockingCollection<int>(5); // 容量为5
blockingCollection.Add(1);
blockingCollection.Add(2);

int item = blockingCollection.Take(); // 从集合中取出元素
Console.WriteLine(item); // 输出: 1
```

## 24. ConcurrentBag

`ConcurrentBag<T>` 是一种线程安全的集合，适合频繁插入和移除数据的场景。它与其他并发集合不同的是，它允许多个线程同时访问。

### 特点

- **无序**：不保证元素按任何特定顺序存储。
- **支持多个线程同时添加和删除数据**。

### 示例

```csharp
ConcurrentBag<int> concurrentBag = new ConcurrentBag<int>();
concurrentBag.Add(1);
concurrentBag.Add(2);
int item;
if (concurrentBag.TryTake(out item))
{
    Console.WriteLine(item); // 成功获取一个元素，输出: 1 或 2
}
```

## 总结

C# 提供的这些内置数据结构为开发者提供了灵活性和高效性，能够应对多种不同的场景和需求。选择合适的数据结构不仅可以提高代码的可读性，还可以提升性能，尤其是在处理大量数据或并发任务时。开发者应根据具体需求选择最合适的集合类型。
