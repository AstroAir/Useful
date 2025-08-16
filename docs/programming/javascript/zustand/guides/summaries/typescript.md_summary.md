### 函数或方法描述

#### `create<T>()(...)`

- **描述**: `create` 是 Zustand 库中的一个函数，用于创建状态管理存储。在 TypeScript 中，使用 `create<T>()(...)` 的形式来显式指定状态的类型 `T`，以便 TypeScript 能够正确推断和检查类型。
- **示例用法**:

  ```ts
  import { create } from 'zustand'

  interface BearState {
    bears: number
    increase: (by: number) => void
  }

  const useBearStore = create<BearState>()((set) => ({
    bears: 0,
    increase: (by) => set((state) => ({ bears: state.bears + by })),
  }))
  ```

- **注意事项**:
  - 必须显式指定状态类型 `T`，否则 TypeScript 无法正确推断类型。
  - 使用 `create<T>()(...)` 的形式时，注意括号的正确匹配。

#### `combine`

- **描述**: `combine` 是 Zustand 库中的一个中间件，用于组合状态。它允许你将状态分割成多个部分，并自动推断状态类型，从而避免手动指定类型。
- **示例用法**:

  ```ts
  import { create } from 'zustand'
  import { combine } from 'zustand/middleware'

  const useBearStore = create(
    combine({ bears: 0 }, (set) => ({
      increase: (by: number) => set((state) => ({ bears: state.bears + by })),
    })),
  )
  ```

- **注意事项**:
  - `combine` 会自动推断状态类型，因此不需要显式指定类型。
  - 使用 `combine` 时，`set` 和 `get` 的类型可能会与实际状态类型不完全匹配，需谨慎使用。

#### `devtools`

- **描述**: `devtools` 是 Zustand 库中的一个中间件，用于与 Redux DevTools 集成，方便调试状态变化。
- **示例用法**:

  ```ts
  import { create } from 'zustand'
  import { devtools } from 'zustand/middleware'

  interface BearState {
    bears: number
    increase: (by: number) => void
  }

  const useBearStore = create<BearState>()(
    devtools((set) => ({
      bears: 0,
      increase: (by) => set((state) => ({ bears: state.bears + by })),
    })),
  )
  ```

- **注意事项**:
  - `devtools` 中间件应尽可能放在最后使用，以确保 `setState` 的类型参数不会丢失。

#### `persist`

- **描述**: `persist` 是 Zustand 库中的一个中间件，用于持久化状态，使其在页面刷新后仍然保留。
- **示例用法**:

  ```ts
  import { create } from 'zustand'
  import { persist } from 'zustand/middleware'

  interface BearState {
    bears: number
    increase: (by: number) => void
  }

  const useBearStore = create<BearState>()(
    persist(
      (set) => ({
        bears: 0,
        increase: (by) => set((state) => ({ bears: state.bears + by })),
      }),
      { name: 'bearStore' },
    ),
  )
  ```

- **注意事项**:
  - `persist` 中间件需要指定一个 `name` 属性，用于标识存储的键名。
  - 持久化的状态类型可能会与实际状态类型不完全匹配，需谨慎使用。

#### `foo` (Middleware that changes the store type)

- **描述**: `foo` 是一个自定义中间件，用于在存储中添加一个新属性 `foo`，并改变存储的类型。
- **示例用法**:

  ```ts
  import { create } from 'zustand'
  import { foo } from 'zustand/middleware'

  const useBearStore = create(foo(() => ({ bears: 0 }), 'hello'))
  console.log(useBearStore.foo.toUpperCase())
  ```

- **注意事项**:
  - 该中间件会改变存储的类型，需确保在使用时类型推断正确。
  - 使用该中间件时，存储的类型会包含 `foo` 属性。

#### `createBoundedUseStore`

- **描述**: `createBoundedUseStore` 是一个辅助函数，用于创建一个带有类型约束的 `useStore` 钩子，以便在使用 vanilla store 时能够正确推断状态类型。
- **示例用法**:

  ```ts
  import { useStore, StoreApi } from 'zustand'
  import { createStore } from 'zustand/vanilla'

  interface BearState {
    bears: number
    increase: (by: number) => void
  }

  const bearStore = createStore<BearState>()((set) => ({
    bears: 0,
    increase: (by) => set((state) => ({ bears: state.bears + by })),
  }))

  const createBoundedUseStore = ((store) => (selector) =>
    useStore(store, selector)) as <S extends StoreApi<unknown>>(
    store: S,
  ) => {
    (): ExtractState<S>
    <T>(selector: (state: ExtractState<S>) => T): T
  }

  type ExtractState<S> = S extends { getState: () => infer X } ? X : never

  const useBearStore = createBoundedUseStore(bearStore)
  ```

- **注意事项**:
  - 该函数用于创建带有类型约束的 `useStore` 钩子，确保在使用 vanilla store 时能够正确推断状态类型。
  - 使用时需确保 `selector` 的类型与存储状态类型匹配。
