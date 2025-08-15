### 函数或方法描述

#### `immer`

`immer` 是 Zustand 的一个中间件，用于简化处理不可变数据结构的过程。通过 `immer`，你可以在 Zustand 中以更直观的方式更新状态，而不必手动创建新的状态对象。

### 示例用法

#### 更新简单状态

```ts
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

type State = {
  count: number
}

type Actions = {
  increment: (qty: number) => void
  decrement: (qty: number) => void
}

export const useCountStore = create<State & Actions>()(
  immer((set) => ({
    count: 0,
    increment: (qty: number) =>
      set((state) => {
        state.count += qty
      }),
    decrement: (qty: number) =>
      set((state) => {
        state.count -= qty
      }),
  })),
)
```

#### 更新复杂状态

```ts
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

interface Todo {
  id: string
  title: string
  done: boolean
}

type State = {
  todos: Record<string, Todo>
}

type Actions = {
  toggleTodo: (todoId: string) => void
}

export const useTodoStore = create<State & Actions>()(
  immer((set) => ({
    todos: {
      '82471c5f-4207-4b1d-abcb-b98547e01a3e': {
        id: '82471c5f-4207-4b1d-abcb-b98547e01a3e',
        title: 'Learn Zustand',
        done: false,
      },
      '354ee16c-bfdd-44d3-afa9-e93679bda367': {
        id: '354ee16c-bfdd-44d3-afa9-e93679bda367',
        title: 'Learn Jotai',
        done: false,
      },
      '771c85c5-46ea-4a11-8fed-36cc2c7be344': {
        id: '771c85c5-46ea-4a11-8fed-36cc2c7be344',
        title: 'Learn Valtio',
        done: false,
      },
      '363a4bac-083f-47f7-a0a2-aeeee153a99c': {
        id: '363a4bac-083f-47f7-a0a2-aeeee153a99c',
        title: 'Learn Signals',
        done: false,
      },
    },
    toggleTodo: (todoId: string) =>
      set((state) => {
        state.todos[todoId].done = !state.todos[todoId].done
      }),
  })),
)
```

### 注意事项

1. **订阅未被调用**：如果你在使用 `immer` 时发现订阅未被调用，确保你遵循了 [Immer 的规则](https://immerjs.github.io/immer/pitfalls)。例如，对于类对象，你需要添加 `[immerable] = true`，否则 Immer 将不会将其视为代理对象，从而导致状态未实际更新。

2. **复杂对象处理**：对于复杂对象（如类实例），确保你正确地处理了它们，否则可能会导致状态更新不正确。

3. **性能影响**：虽然 `immer` 简化了不可变状态的处理，但在某些情况下可能会引入性能开销，尤其是在处理非常大的数据结构时。