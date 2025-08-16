### 函数或方法描述

1. **`create`**:
   - **描述**: `create` 是 Zustand 提供的一个函数，用于创建一个状态存储（store）。这个 store 是一个自定义的 React hook，可以存储任何类型的状态（如原始类型、对象、函数等）。`set` 函数用于更新状态，并且会自动合并状态对象。
   - **示例用法**:

     ```js
     import { create } from 'zustand'

     const useStore = create((set) => ({
       bears: 0,
       increasePopulation: () => set((state) => ({ bears: state.bears + 1 })),
       removeAllBears: () => set({ bears: 0 }),
       updateBears: (newBears) => set({ bears: newBears }),
     }))
     ```

   - **注意事项**:
     - `set` 函数会自动合并状态对象，因此不需要手动合并。
     - 状态更新是异步的，但组件会在状态变化时自动重新渲染。

2. **`useStore`**:
   - **描述**: `useStore` 是 Zustand 创建的 store 的 hook，用于在组件中访问和订阅状态。通过传递一个选择器函数，可以选择性地订阅特定的状态片段，从而优化性能。
   - **示例用法**:

     ```jsx
     function BearCounter() {
       const bears = useStore((state) => state.bears)
       return <h1>{bears} around here...</h1>
     }

     function Controls() {
       const increasePopulation = useStore((state) => state.increasePopulation)
       return <button onClick={increasePopulation}>one up</button>
     }
     ```

   - **注意事项**:
     - 选择器函数应尽量保持简单，以避免不必要的重新渲染。
     - 如果选择器函数返回的对象引用不变，组件不会重新渲染。

### 总结

- **`create`**: 用于创建一个状态存储，`set` 函数用于更新状态并自动合并。
- **`useStore`**: 用于在组件中访问和订阅状态，通过选择器函数优化性能。

### 注意事项

- **状态更新**: `set` 函数更新状态是异步的，但组件会在状态变化时自动重新渲染。
- **选择器函数**: 选择器函数应尽量保持简单，以避免不必要的重新渲染。如果选择器函数返回的对象引用不变，组件不会重新渲染。
