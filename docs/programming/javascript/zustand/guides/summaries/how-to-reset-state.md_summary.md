### 函数或方法描述

1. **`create` (Zustand Store Creator)**
   - **描述**: 用于创建一个 Zustand 状态管理存储。它接受一个状态创建函数，并返回一个包含状态和操作的存储对象。
   - **示例用法**:

     ```ts
     const useSlice = create<State & Actions>()((set, get) => ({
       ...initialState,
       addSalmon: (qty: number) => {
         set({ salmon: get().salmon + qty })
       },
       addTuna: (qty: number) => {
         set({ tuna: get().tuna + qty })
       },
       reset: () => {
         set(initialState)
       },
     }))
     ```

   - **注意事项**:
     - `set` 用于更新状态。
     - `get` 用于获取当前状态。
     - `initialState` 是状态的初始值。

2. **`reset` (State Reset Function)**
   - **描述**: 用于将状态重置为其初始值。
   - **示例用法**:

     ```ts
     const reset = () => {
       set(initialState)
     }
     ```

   - **注意事项**:
     - `set` 函数用于更新状态。
     - `initialState` 是状态的初始值。

3. **`resetAllStores` (Reset Multiple Stores)**
   - **描述**: 用于重置多个 Zustand 存储的状态。
   - **示例用法**:

     ```ts
     const resetAllStores = () => {
       storeResetFns.forEach((resetFn) => {
         resetFn()
       })
     }
     ```

   - **注意事项**:
     - `storeResetFns` 是一个包含所有存储重置函数的集合。
     - `resetFn` 是每个存储的重置函数。

4. **`create` (Custom Store Creator for Resetting Multiple Stores)**
   - **描述**: 自定义的 Zustand 存储创建函数，用于在创建存储时自动注册重置函数。
   - **示例用法**:

     ```ts
     export const create = (<T>() => {
       return (stateCreator: StateCreator<T>) => {
         const store = actualCreate(stateCreator)
         const initialState = store.getInitialState()
         storeResetFns.add(() => {
           store.setState(initialState, true)
         })
         return store
       }
     }) as typeof actualCreate
     ```

   - **注意事项**:
     - `actualCreate` 是原始的 Zustand 存储创建函数。
     - `storeResetFns` 是一个包含所有存储重置函数的集合。
     - `store.setState(initialState, true)` 用于将存储状态重置为初始值。

### 示例用法总结

- **`create`**: 用于创建 Zustand 存储，定义状态和操作。
- **`reset`**: 用于将单个存储的状态重置为初始值。
- **`resetAllStores`**: 用于重置多个存储的状态。
- **`create` (Custom)**: 用于创建存储时自动注册重置函数，以便支持多个存储的重置。

### 注意事项总结

- **`set` 和 `get`**: 在 Zustand 中，`set` 用于更新状态，`get` 用于获取当前状态。
- **`initialState`**: 状态的初始值，用于重置状态。
- **`storeResetFns`**: 一个集合，用于存储所有存储的重置函数。
- **`store.setState(initialState, true)`**: 用于将存储状态重置为初始值，并确保状态的更新是深层次的。
