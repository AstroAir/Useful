### 函数或方法描述

`createWithEqualityFn` 是一个用于创建 React Hook 的函数，类似于 `create`，但它允许你定义一个自定义的相等性检查函数。这使得你可以更精细地控制组件何时重新渲染，从而提高性能和响应性。

### 示例用法

```tsx
import { createWithEqualityFn } from 'zustand/traditional';
import { shallow } from 'zustand/vanilla/shallow';

type AgeStoreState = { age: number };

type AgeStoreActions = {
  setAge: (
    nextAge:
      | AgeStoreState['age']
      | ((currentAge: AgeStoreState['age']) => AgeStoreState['age']),
  ) => void;
};

type AgeStore = AgeStoreState & AgeStoreActions;

const useAgeStore = createWithEqualityFn<AgeStore>()(
  (set) => ({
    age: 42,
    setAge: (nextAge) =>
      set((state) => ({
        age: typeof nextAge === 'function' ? nextAge(state.age) : nextAge,
      })),
  }),
  shallow,
);

export default function App() {
  const age = useAgeStore((state) => state.age);
  const setAge = useAgeStore((state) => state.setAge);

  function increment() {
    setAge((currentAge) => currentAge + 1);
  }

  return (
    <>
      <h1>Your age: {age}</h1>
      <button
        type="button"
        onClick={() => {
          increment();
          increment();
          increment();
        }}
      >
        +3
      </button>
      <button
        type="button"
        onClick={() => {
          increment();
        }}
      >
        +1
      </button>
    </>
  );
}
```

### 注意事项

1. **自定义相等性检查**：`createWithEqualityFn` 允许你传入一个自定义的相等性检查函数 `equalityFn`，默认情况下使用 `Object.is`。
2. **状态更新**：在更新状态时，建议使用不可变操作（如 `[...array]`、`concat(...)` 等），避免直接修改状态对象或数组。
3. **浅合并**：默认情况下，`set` 函数执行浅合并。如果需要完全替换状态，可以使用 `replace` 参数设置为 `true`。
4. **性能优化**：通过自定义相等性检查，可以避免不必要的重新渲染，从而提高应用的性能。
