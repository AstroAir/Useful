### 函数或方法描述、示例用法及注意事项

#### 1. `createCounterStore`

**描述**:  
`createCounterStore` 是一个工厂函数，用于创建一个新的 Zustand 状态存储。它接受一个初始状态 `initState`，并返回一个包含状态和操作的 Zustand 存储对象。

**示例用法**:

```ts
import { createCounterStore } from '@/stores/counter-store';

const store = createCounterStore({ count: 10 });
console.log(store.getState().count); // 输出: 10
store.getState().incrementCount();
console.log(store.getState().count); // 输出: 11
```

**注意事项**:

- 该函数应在每个请求中独立调用，以确保状态不会在多个请求之间共享。
- 初始状态 `initState` 是可选的，默认值为 `{ count: 0 }`。

---

#### 2. `CounterStoreProvider`

**描述**:  
`CounterStoreProvider` 是一个 React 组件，用于在组件树中提供 Zustand 存储。它使用 `createCounterStore` 创建存储，并通过 `Context` 将其传递给子组件。

**示例用法**:

```tsx
import { CounterStoreProvider } from '@/providers/counter-store-provider';

const App = () => (
  <CounterStoreProvider>
    <HomePage />
  </CounterStoreProvider>
);
```

**注意事项**:

- 该组件应在服务器端每个请求中只渲染一次，以确保存储不会在多个请求之间共享。
- 如果组件在客户端被多次渲染，存储只会被创建一次，因为使用了 `useRef` 来缓存存储实例。

---

#### 3. `useCounterStore`

**描述**:  
`useCounterStore` 是一个自定义 Hook，用于从 `CounterStoreProvider` 提供的 Zustand 存储中选择特定状态或操作。它接受一个选择器函数 `selector`，并返回选择器的结果。

**示例用法**:

```tsx
import { useCounterStore } from '@/providers/counter-store-provider';

const HomePage = () => {
  const { count, incrementCount, decrementCount } = useCounterStore((state) => state);

  return (
    <div>
      Count: {count}
      <button onClick={() => incrementCount()}>Increment</button>
      <button onClick={() => decrementCount()}>Decrement</button>
    </div>
  );
};
```

**注意事项**:

- 该 Hook 必须在 `CounterStoreProvider` 的子组件中使用，否则会抛出错误。
- 选择器函数 `selector` 应尽可能具体，以避免不必要的重新渲染。

---

#### 4. `initCounterStore`

**描述**:  
`initCounterStore` 是一个函数，用于初始化 Zustand 存储的初始状态。它返回一个包含 `count` 属性的对象，`count` 的值为当前年份。

**示例用法**:

```ts
import { initCounterStore } from '@/stores/counter-store';

const initialState = initCounterStore();
console.log(initialState.count); // 输出: 当前年份，例如 2023
```

**注意事项**:

- 该函数通常用于在服务器端初始化存储状态，以确保服务器和客户端的初始状态一致。
- 该函数应在每个请求中独立调用，以避免状态共享。

---

#### 5. `HomePage` (Pages Router)

**描述**:  
`HomePage` 是一个 React 组件，展示了如何在使用 Pages Router 的 Next.js 应用中使用 Zustand 存储。它从 `useCounterStore` 中获取状态和操作，并渲染一个简单的计数器界面。

**示例用法**:

```tsx
import { HomePage } from '@/components/pages/home-page';

const IndexPage = () => <HomePage />;
```

**注意事项**:

- 该组件应在 `CounterStoreProvider` 的子组件中使用，以确保能够访问 Zustand 存储。
- 如果需要为每个路由创建独立的存储，可以在路由组件级别使用 `CounterStoreProvider`。

---

#### 6. `HomePage` (App Router)

**描述**:  
`HomePage` 是一个 React 组件，展示了如何在使用 App Router 的 Next.js 应用中使用 Zustand 存储。它从 `useCounterStore` 中获取状态和操作，并渲染一个简单的计数器界面。

**示例用法**:

```tsx
import { HomePage } from '@/components/pages/home-page';

const Home = () => <HomePage />;
```

**注意事项**:

- 该组件应在 `CounterStoreProvider` 的子组件中使用，以确保能够访问 Zustand 存储。
- 如果需要为每个路由创建独立的存储，可以在路由组件级别使用 `CounterStoreProvider`。

---

#### 7. `CounterStoreProvider` (Pages Router)

**描述**:  
`CounterStoreProvider` 是一个 React 组件，用于在使用 Pages Router 的 Next.js 应用中提供 Zustand 存储。它将存储传递给子组件。

**示例用法**:

```tsx
import { CounterStoreProvider } from '@/providers/counter-store-provider';

const App = ({ Component, pageProps }) => (
  <CounterStoreProvider>
    <Component {...pageProps} />
  </CounterStoreProvider>
);
```

**注意事项**:

- 该组件应在应用的根组件中使用，以确保所有子组件都能访问 Zustand 存储。
- 如果需要为每个路由创建独立的存储，可以在路由组件级别使用 `CounterStoreProvider`。

---

#### 8. `CounterStoreProvider` (App Router)

**描述**:  
`CounterStoreProvider` 是一个 React 组件，用于在使用 App Router 的 Next.js 应用中提供 Zustand 存储。它将存储传递给子组件。

**示例用法**:

```tsx
import { CounterStoreProvider } from '@/providers/counter-store-provider';

const RootLayout = ({ children }) => (
  <html lang="en">
    <body>
      <CounterStoreProvider>{children}</CounterStoreProvider>
    </body>
  </html>
);
```

**注意事项**:

- 该组件应在应用的根布局组件中使用，以确保所有子组件都能访问 Zustand 存储。
- 如果需要为每个路由创建独立的存储，可以在路由组件级别使用 `CounterStoreProvider`。
