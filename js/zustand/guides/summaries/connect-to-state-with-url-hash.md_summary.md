### 函数或方法描述、示例用法及注意事项

#### 1. `hashStorage` 对象

**描述**:  
`hashStorage` 是一个自定义的 `StateStorage` 实现，用于将状态存储在 URL 的 hash 部分。它提供了 `getItem`、`setItem` 和 `removeItem` 方法，用于从 URL hash 中读取、写入和删除状态。

**示例用法**:
```ts
const hashStorage: StateStorage = {
  getItem: (key): string => {
    const searchParams = new URLSearchParams(location.hash.slice(1))
    const storedValue = searchParams.get(key) ?? ''
    return JSON.parse(storedValue)
  },
  setItem: (key, newValue): void => {
    const searchParams = new URLSearchParams(location.hash.slice(1))
    searchParams.set(key, JSON.stringify(newValue))
    location.hash = searchParams.toString()
  },
  removeItem: (key): void => {
    const searchParams = new URLSearchParams(location.hash.slice(1))
    searchParams.delete(key)
    location.hash = searchParams.toString()
  },
}
```

**注意事项**:
- `getItem` 方法从 URL hash 中读取状态，并将其解析为 JSON 格式。
- `setItem` 方法将状态写入 URL hash，并更新页面的 hash 部分。
- `removeItem` 方法从 URL hash 中删除指定键的状态。

---

#### 2. `useBoundStore` 钩子

**描述**:  
`useBoundStore` 是一个使用 `zustand` 和 `persist` 中间件创建的存储，它将状态持久化到 URL hash 中。

**示例用法**:
```ts
export const useBoundStore = create(
  persist(
    (set, get) => ({
      fishes: 0,
      addAFish: () => set({ fishes: get().fishes + 1 }),
    }),
    {
      name: 'food-storage',
      storage: createJSONStorage(() => hashStorage),
    },
  ),
)
```

**注意事项**:
- `name` 属性用于指定存储的唯一标识符。
- `storage` 属性指定了使用 `hashStorage` 作为持久化存储。

---

#### 3. `persistentStorage` 对象

**描述**:  
`persistentStorage` 是一个自定义的 `StateStorage` 实现，用于将状态存储在 URL 查询参数中，并在必要时回退到 `localStorage`。

**示例用法**:
```ts
const persistentStorage: StateStorage = {
  getItem: (key): string => {
    if (getUrlSearch()) {
      const searchParams = new URLSearchParams(getUrlSearch())
      const storedValue = searchParams.get(key)
      return JSON.parse(storedValue as string)
    } else {
      return JSON.parse(localStorage.getItem(key) as string)
    }
  },
  setItem: (key, newValue): void => {
    if (getUrlSearch()) {
      const searchParams = new URLSearchParams(getUrlSearch())
      searchParams.set(key, JSON.stringify(newValue))
      window.history.replaceState(null, '', `?${searchParams.toString()}`)
    }
    localStorage.setItem(key, JSON.stringify(newValue))
  },
  removeItem: (key): void => {
    const searchParams = new URLSearchParams(getUrlSearch())
    searchParams.delete(key)
    window.location.search = searchParams.toString()
  },
}
```

**注意事项**:
- `getItem` 方法首先检查 URL 查询参数，如果不存在则从 `localStorage` 中读取。
- `setItem` 方法首先尝试更新 URL 查询参数，然后同步到 `localStorage`。
- `removeItem` 方法从 URL 查询参数中删除指定键的状态。

---

#### 4. `useLocalAndUrlStore` 钩子

**描述**:  
`useLocalAndUrlStore` 是一个使用 `zustand` 和 `persist` 中间件创建的存储，它将状态持久化到 URL 查询参数和 `localStorage` 中。

**示例用法**:
```ts
const useLocalAndUrlStore = create(
  persist<LocalAndUrlStore>(
    (set) => ({
      typesOfFish: [],
      addTypeOfFish: (fishType) =>
        set((state) => ({ typesOfFish: [...state.typesOfFish, fishType] })),
      numberOfBears: 0,
      setNumberOfBears: (numberOfBears) => set(() => ({ numberOfBears })),
    }),
    storageOptions,
  ),
)
```

**注意事项**:
- `storageOptions` 指定了存储的名称和使用 `persistentStorage` 作为持久化存储。

---

#### 5. `buildURLSuffix` 函数

**描述**:  
`buildURLSuffix` 函数用于生成 URL 查询参数的后缀，基于 `zustand` 存储的状态。

**示例用法**:
```ts
const buildURLSuffix = (params, version = 0) => {
  const searchParams = new URLSearchParams()
  const zustandStoreParams = {
    state: {
      typesOfFish: params.typesOfFish,
      numberOfBears: params.numberOfBears,
    },
    version: version,
  }
  searchParams.set('fishAndBearsStore', JSON.stringify(zustandStoreParams))
  return searchParams.toString()
}
```

**注意事项**:
- `params` 参数包含需要转换为 URL 查询参数的状态。
- `version` 参数用于标识状态的版本。

---

#### 6. `buildShareableUrl` 函数

**描述**:  
`buildShareableUrl` 函数用于生成一个可分享的 URL，包含当前的状态信息。

**示例用法**:
```ts
export const buildShareableUrl = (params, version) => {
  return `${window.location.origin}?${buildURLSuffix(params, version)}`
}
```

**注意事项**:
- 生成的 URL 包含当前页面的 origin 和通过 `buildURLSuffix` 生成的查询参数。
- 示例生成的 URL 可能类似于：`https://localhost/search?fishAndBearsStore={"state":{"typesOfFish":["tilapia","salmon"],"numberOfBears":15},"version":0}}`。