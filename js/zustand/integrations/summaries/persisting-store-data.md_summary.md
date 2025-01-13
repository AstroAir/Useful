### 函数或方法描述、示例用法及注意事项

#### `persist`

**描述**:  
`persist` 是一个中间件，用于将 Zustand 状态持久化到存储中（如 `localStorage`, `AsyncStorage`, `IndexedDB` 等）。它支持同步和异步存储，但使用异步存储会有一定的成本。

**示例用法**:
```ts
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

export const useBearStore = create(
  persist(
    (set, get) => ({
      bears: 0,
      addABear: () => set({ bears: get().bears + 1 }),
    }),
    {
      name: 'food-storage', // 存储中的键名（必须唯一）
      storage: createJSONStorage(() => sessionStorage), // 默认使用 localStorage
    },
  ),
)
```

**注意事项**:  
- `name` 是唯一必需的选项，用于在存储中标识状态。
- 使用异步存储时，状态的 hydration 是异步的，可能会导致初始渲染时状态未加载。

---

#### `createJSONStorage`

**描述**:  
`createJSONStorage` 是一个辅助函数，用于创建符合 `StateStorage` 接口的存储对象。它支持自定义存储引擎，并可以配置序列化和反序列化的选项。

**示例用法**:
```ts
import { createJSONStorage } from 'zustand/middleware'

const storage = createJSONStorage(() => sessionStorage, {
  reviver: (key, value) => {
    if (value && value.type === 'date') {
      return new Date(value)
    }
    return value
  },
  replacer: (key, value) => {
    if (value instanceof Date) {
      return { type: 'date', value: value.toISOString() }
    }
    return value
  },
})
```

**注意事项**:  
- `reviver` 和 `replacer` 用于自定义 JSON 的序列化和反序列化。
- 返回的 `storage` 对象必须实现 `getItem`, `setItem`, 和 `removeItem` 方法。

---

#### `partialize`

**描述**:  
`partialize` 是一个选项，用于选择性地持久化状态中的某些字段。默认情况下，所有状态字段都会被持久化。

**示例用法**:
```ts
export const useBoundStore = create(
  persist(
    (set, get) => ({
      foo: 0,
      bar: 1,
    }),
    {
      partialize: (state) => ({ foo: state.foo }), // 只持久化 foo 字段
    },
  ),
)
```

**注意事项**:  
- 可以通过 `Object.fromEntries` 或直接返回部分状态对象来选择持久化的字段。

---

#### `onRehydrateStorage`

**描述**:  
`onRehydrateStorage` 是一个选项，用于在存储 hydration 过程中执行自定义逻辑。它可以在 hydration 开始和结束时调用回调函数。

**示例用法**:
```ts
export const useBoundStore = create(
  persist(
    (set, get) => ({
      // ...
    }),
    {
      onRehydrateStorage: (state) => {
        console.log('hydration starts')
        return (state, error) => {
          if (error) {
            console.log('an error happened during hydration', error)
          } else {
            console.log('hydration finished')
          }
        }
      },
    },
  ),
)
```

**注意事项**:  
- 返回的函数会在 hydration 结束时调用，可以处理错误或执行其他逻辑。

---

#### `migrate`

**描述**:  
`migrate` 是一个选项，用于处理存储版本迁移。当存储中的版本与代码中的版本不匹配时，可以使用此函数来迁移旧数据。

**示例用法**:
```ts
export const useBoundStore = create(
  persist(
    (set, get) => ({
      newField: 0, // 假设在版本 0 中字段名不同
    }),
    {
      version: 1,
      migrate: (persistedState, version) => {
        if (version === 0) {
          persistedState.newField = persistedState.oldField
          delete persistedState.oldField
        }
        return persistedState
      },
    },
  ),
)
```

**注意事项**:  
- `migrate` 函数必须返回与最新版本兼容的状态对象。

---

#### `merge`

**描述**:  
`merge` 是一个选项，用于自定义持久化状态与当前状态的合并逻辑。默认情况下，中间件执行浅合并。

**示例用法**:
```ts
export const useBoundStore = create(
  persist(
    (set, get) => ({
      foo: {
        bar: 0,
        baz: 1,
      },
    }),
    {
      merge: (persistedState, currentState) => deepMerge(currentState, persistedState),
    },
  ),
)
```

**注意事项**:  
- 浅合并可能会导致嵌套对象的字段丢失，建议在需要时使用深合并。

---

#### `skipHydration`

**描述**:  
`skipHydration` 是一个选项，用于控制是否在初始化时跳过 hydration。默认情况下，store 会在初始化时自动 hydrate。

**示例用法**:
```ts
export const useBoundStore = create(
  persist(
    () => ({
      count: 0,
    }),
    {
      skipHydration: true,
    },
  ),
)

useEffect(() => {
  useBoundStore.persist.rehydrate()
}, [])
```

**注意事项**:  
- 设置为 `true` 时，需要手动调用 `rehydrate` 方法来触发 hydration。

---

#### `getOptions`

**描述**:  
`getOptions` 是一个 API 方法，用于获取当前 Persist 中间件的配置选项。

**示例用法**:
```ts
const storageName = useBoundStore.persist.getOptions().name
```

**注意事项**:  
- 返回的选项是只读的，不能直接修改。

---

#### `setOptions`

**描述**:  
`setOptions` 是一个 API 方法，用于动态更改 Persist 中间件的配置选项。

**示例用法**:
```ts
useBoundStore.persist.setOptions({
  name: 'new-name',
  storage: createJSONStorage(() => sessionStorage),
})
```

**注意事项**:  
- 新选项会与当前选项合并，不会覆盖所有选项。

---

#### `clearStorage`

**描述**:  
`clearStorage` 是一个 API 方法，用于清除存储中与当前 store 相关的所有数据。

**示例用法**:
```ts
useBoundStore.persist.clearStorage()
```

**注意事项**:  
- 该操作会删除存储中与 `name` 键相关的所有数据。

---

#### `rehydrate`

**描述**:  
`rehydrate` 是一个 API 方法，用于手动触发 hydration 过程。

**示例用法**:
```ts
await useBoundStore.persist.rehydrate()
```

**注意事项**:  
- 该方法适用于需要手动控制 hydration 的场景。

---

#### `hasHydrated`

**描述**:  
`hasHydrated` 是一个 API 方法，用于检查存储是否已完成 hydration。

**示例用法**:
```ts
const isHydrated = useBoundStore.persist.hasHydrated()
```

**注意事项**:  
- 该方法是非响应式的，返回布尔值。

---

#### `onHydrate`

**描述**:  
`onHydrate` 是一个 API 方法，用于在 hydration 开始时注册监听器。

**示例用法**:
```ts
const unsub = useBoundStore.persist.onHydrate((state) => {
  console.log('hydration starts')
})
unsub() // 取消订阅
```

**注意事项**:  
- 返回一个取消订阅的函数。

---

#### `onFinishHydration`

**描述**:  
`onFinishHydration` 是一个 API 方法，用于在 hydration 结束时注册监听器。

**示例用法**:
```ts
const unsub = useBoundStore.persist.onFinishHydration((state) => {
  console.log('hydration finished')
})
unsub() // 取消订阅
```

**注意事项**:  
- 返回一个取消订阅的函数。

---

以上是文件中出现的函数或方法的简要描述、示例用法及注意事项。