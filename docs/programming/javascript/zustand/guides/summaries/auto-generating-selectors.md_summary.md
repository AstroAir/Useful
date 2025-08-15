### 函数或方法描述

#### `createSelectors`

`createSelectors` 是一个用于自动生成选择器的函数。它通过遍历存储状态中的所有属性，为每个属性生成一个选择器函数。这些选择器函数可以直接访问存储中的属性或方法。

### 示例用法

#### React Store

```typescript
import { create } from 'zustand';
import { createSelectors } from './createSelectors';

interface BearState {
  bears: number;
  increase: (by: number) => void;
  increment: () => void;
}

const useBearStoreBase = create<BearState>()((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  increment: () => set((state) => ({ bears: state.bears + 1 })),
}));

const useBearStore = createSelectors(useBearStoreBase);

// 使用自动生成的选择器
const bears = useBearStore.use.bears();
const increment = useBearStore.use.increment();
```

#### Vanilla Store

```typescript
import { createStore } from 'zustand';
import { createSelectors } from './createSelectors';

interface BearState {
  bears: number;
  increase: (by: number) => void;
  increment: () => void;
}

const store = createStore<BearState>((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  increment: () => set((state) => ({ bears: state.bears + 1 })),
}));

const useBearStore = createSelectors(store);

// 使用自动生成的选择器
const bears = useBearStore.use.bears();
const increment = useBearStore.use.increment();
```

### 注意事项

1. **类型推断**：`createSelectors` 函数依赖于 TypeScript 的类型推断，确保存储状态的类型定义正确。
2. **性能**：自动生成的选择器在每次调用时都会重新计算，因此在性能敏感的场景中，可能需要手动优化选择器。
3. **兼容性**：`createSelectors` 函数适用于 `zustand` 库，确保你使用的是兼容的版本。
4. **命名冲突**：自动生成的选择器函数名称与存储状态中的属性名称一致，避免命名冲突。

### 参考链接

- [Code Sandbox 示例](https://codesandbox.io/s/zustand-auto-generate-selectors-forked-rl8v5e?file=/src/selectors.ts)
- [auto-zustand-selectors-hook](https://github.com/Albert-Gao/auto-zustand-selectors-hook)
- [react-hooks-global-state](https://github.com/dai-shi/react-hooks-global-state)
- [zustood](https://github.com/udecode/zustood)
- [@davstack/store](https://github.com/DawidWraga/davstack)