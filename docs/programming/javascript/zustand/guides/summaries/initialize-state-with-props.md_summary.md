### 1. `createStore` 函数

**描述**:  
`createStore` 是 Zustand 库中的一个函数，用于创建一个状态管理存储。它允许你定义状态的初始值以及状态的更新方法。

**示例用法**:
```ts
const createBearStore = (initProps?: Partial<BearProps>) => {
  const DEFAULT_PROPS: BearProps = {
    bears: 0,
  }
  return createStore<BearState>()((set) => ({
    ...DEFAULT_PROPS,
    ...initProps,
    addBear: () => set((state) => ({ bears: ++state.bears })),
  }))
}
```

**注意事项**:
- `createStore` 返回的是一个函数，该函数接受一个 `set` 函数，用于更新状态。
- 初始状态可以通过 `initProps` 参数进行部分初始化。

---

### 2. `React.createContext` 方法

**描述**:  
`React.createContext` 是 React 提供的一个方法，用于创建一个上下文对象，允许在组件树中共享数据，而不需要通过 props 逐层传递。

**示例用法**:
```ts
export const BearContext = createContext<BearStore | null>(null)
```

**注意事项**:
- 上下文的默认值为 `null`，表示在没有提供 `Provider` 的情况下，上下文值为空。
- 在使用上下文时，确保在组件树中有一个 `Provider` 提供上下文值。

---

### 3. `useRef` 钩子

**描述**:  
`useRef` 是 React 提供的一个钩子，用于创建一个可变的引用对象，该对象在组件的整个生命周期内保持不变。

**示例用法**:
```tsx
function App() {
  const store = useRef(createBearStore()).current
  return (
    <BearContext.Provider value={store}>
      <BasicConsumer />
    </BearContext.Provider>
  )
}
```

**注意事项**:
- `useRef` 返回的对象包含一个 `current` 属性，该属性可以存储任意值。
- `useRef` 的值在组件重新渲染时不会改变，除非手动更新 `current` 属性。

---

### 4. `useContext` 钩子

**描述**:  
`useContext` 是 React 提供的一个钩子，用于在函数组件中消费上下文数据。

**示例用法**:
```tsx
function BasicConsumer() {
  const store = useContext(BearContext)
  if (!store) throw new Error('Missing BearContext.Provider in the tree')
  const bears = useStore(store, (s) => s.bears)
  const addBear = useStore(store, (s) => s.addBear)
  return (
    <>
      <div>{bears} Bears.</div>
      <button onClick={addBear}>Add bear</button>
    </>
  )
}
```

**注意事项**:
- 使用 `useContext` 时，确保在组件树中有一个 `Provider` 提供上下文值，否则会抛出错误。
- 上下文值的变化会触发使用该上下文的组件重新渲染。

---

### 5. `useStore` 钩子

**描述**:  
`useStore` 是 Zustand 提供的一个钩子，用于从存储中选择和订阅特定的状态片段。

**示例用法**:
```tsx
const bears = useStore(store, (s) => s.bears)
const addBear = useStore(store, (s) => s.addBear)
```

**注意事项**:
- `useStore` 的第一个参数是存储实例，第二个参数是一个选择器函数，用于从状态中提取所需的数据。
- 选择器函数返回的值会被订阅，当状态变化时，组件会重新渲染。

---

### 6. `useBearContext` 自定义钩子

**描述**:  
`useBearContext` 是一个自定义钩子，用于从上下文中获取存储实例，并从中选择特定的状态片段。

**示例用法**:
```tsx
function useBearContext<T>(selector: (state: BearState) => T): T {
  const store = useContext(BearContext)
  if (!store) throw new Error('Missing BearContext.Provider in the tree')
  return useStore(store, selector)
}
```

**注意事项**:
- 该钩子封装了 `useContext` 和 `useStore`，简化了从上下文中获取状态的逻辑。
- 使用该钩子时，确保在组件树中有一个 `Provider` 提供上下文值。

---

### 7. `useStoreWithEqualityFn` 钩子

**描述**:  
`useStoreWithEqualityFn` 是 Zustand 提供的一个钩子，类似于 `useStore`，但允许自定义相等性检查函数。

**示例用法**:
```tsx
function useBearContext<T>(
  selector: (state: BearState) => T,
  equalityFn?: (left: T, right: T) => boolean,
): T {
  const store = useContext(BearContext)
  if (!store) throw new Error('Missing BearContext.Provider in the tree')
  return useStoreWithEqualityFn(store, selector, equalityFn)
}
```

**注意事项**:
- `equalityFn` 参数允许你定义如何比较选择器返回的值，从而控制组件是否重新渲染。
- 如果没有提供 `equalityFn`，默认使用浅比较。