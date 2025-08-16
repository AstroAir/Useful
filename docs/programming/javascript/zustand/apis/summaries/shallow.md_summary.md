### 函数或方法描述

`shallow` 是一个用于快速比较简单数据结构的函数。它能够有效地识别数据结构中**顶层**属性的变化，特别适用于不包含嵌套对象或数组的数据结构。

### 示例用法

#### 比较原始类型（Primitives）

```ts
const stringLeft = 'John Doe';
const stringRight = 'John Doe';

shallow(stringLeft, stringRight); // -> true

const numberLeft = 10;
const numberRight = 10;

shallow(numberLeft, numberRight); // -> true

const booleanLeft = true;
const booleanRight = true;

shallow(booleanLeft, booleanRight); // -> true

const bigIntLeft = 1n;
const bigIntRight = 1n;

shallow(bigIntLeft, bigIntRight); // -> true
```

#### 比较对象（Objects）

```ts
const objectLeft = {
  firstName: 'John',
  lastName: 'Doe',
  age: 30,
};
const objectRight = {
  firstName: 'John',
  lastName: 'Doe',
  age: 30,
};

shallow(objectLeft, objectRight); // -> true
```

#### 比较集合（Sets）

```ts
const setLeft = new Set([1, 2, 3]);
const setRight = new Set([1, 2, 3]);

shallow(setLeft, setRight); // -> true
```

#### 比较映射（Maps）

```ts
const mapLeft = new Map([
  [1, 'one'],
  [2, 'two'],
  [3, 'three'],
]);
const mapRight = new Map([
  [1, 'one'],
  [2, 'two'],
  [3, 'three'],
]);

shallow(mapLeft, mapRight); // -> true
```

### 注意事项

1. **浅比较**：`shallow` 函数仅对**顶层**属性进行比较，不涉及嵌套对象或深层属性的比较。如果对象包含嵌套结构，即使内容相同，`shallow` 也会返回 `false`。

2. **引用比较**：对于对象、集合和映射，`shallow` 比较的是顶层属性的引用，而不是内容。因此，即使两个对象的内容相同，但如果它们的引用不同，`shallow` 也会返回 `false`。

3. **性能优势**：`shallow` 的浅比较使得它在处理简单数据结构时非常高效，但在处理复杂嵌套结构时可能会导致意外的结果。

### 示例：嵌套对象的比较

```ts
const objectLeft = {
  firstName: 'John',
  lastName: 'Doe',
  age: 30,
  address: {
    street: 'Kulas Light',
    suite: 'Apt. 556',
    city: 'Gwenborough',
    zipcode: '92998-3874',
    geo: {
      lat: '-37.3159',
      lng: '81.1496',
    },
  },
};
const objectRight = {
  firstName: 'John',
  lastName: 'Doe',
  age: 30,
  address: {
    street: 'Kulas Light',
    suite: 'Apt. 556',
    city: 'Gwenborough',
    zipcode: '92998-3874',
    geo: {
      lat: '-37.3159',
      lng: '81.1496',
    },
  },
};

shallow(objectLeft, objectRight); // -> false
```

在这个例子中，尽管 `objectLeft` 和 `objectRight` 的内容完全相同，但由于 `address` 属性是一个嵌套对象，`shallow` 函数返回 `false`。
