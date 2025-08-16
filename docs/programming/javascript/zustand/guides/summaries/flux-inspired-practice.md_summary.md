### 1. `set` / `setState` 方法

#### 描述

`set` 和 `setState` 是 Zustand 中用于更新 store 状态的方法。它们确保状态更新被正确合并，并且通知所有监听器。

#### 示例用法

```javascript
const useBoundStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));

// 使用示例
const { increment, decrement } = useBoundStore.getState();
increment(); // count 变为 1
decrement(); // count 变为 0
```

#### 注意事项

- `set` 和 `setState` 是同步操作，确保状态更新是原子的。
- 使用 `set` 时，传入的函数会接收当前状态并返回新的状态。

---

### 2. `dispatch` 函数

#### 描述

`dispatch` 函数类似于 Redux 中的 `dispatch`，用于触发状态更新。它通常与 reducer 结合使用，处理复杂的更新逻辑。

#### 示例用法

```typescript
const types = { increase: 'INCREASE', decrease: 'DECREASE' };

const reducer = (state, { type, by = 1 }) => {
  switch (type) {
    case types.increase:
      return { grumpiness: state.grumpiness + by };
    case types.decrease:
      return { grumpiness: state.grumpiness - by };
    default:
      return state;
  }
};

const useGrumpyStore = create((set) => ({
  grumpiness: 0,
  dispatch: (args) => set((state) => reducer(state, args)),
}));

// 使用示例
const dispatch = useGrumpyStore((state) => state.dispatch);
dispatch({ type: types.increase, by: 2 }); // grumpiness 变为 2
dispatch({ type: types.decrease }); // grumpiness 变为 1
```

#### 注意事项

- `dispatch` 通常与 reducer 结合使用，reducer 负责根据 action 类型更新状态。
- `dispatch` 的参数是一个对象，包含 `type` 和可选的 `payload`。

---

### 3. `redux` 中间件

#### 描述

`redux` 中间件允许你在 Zustand 中使用类似 Redux 的模式，包括 reducer、初始状态和 `dispatch` 函数。

#### 示例用法

```typescript
import { redux } from 'zustand/middleware';

const initialState = { grumpiness: 0 };
const reducer = (state, action) => {
  switch (action.type) {
    case 'INCREASE':
      return { grumpiness: state.grumpiness + 1 };
    case 'DECREASE':
      return { grumpiness: state.grumpiness - 1 };
    default:
      return state;
  }
};

const useReduxStore = create(redux(reducer, initialState));

// 使用示例
const { dispatch } = useReduxStore.getState();
dispatch({ type: 'INCREASE' }); // grumpiness 变为 1
dispatch({ type: 'DECREASE' }); // grumpiness 变为 0
```

#### 注意事项

- `redux` 中间件将 reducer 和初始状态绑定到 Zustand store 中。
- 使用 `dispatch` 时，action 对象必须包含 `type` 属性。

---

### 4. 外部状态更新函数

#### 描述

除了在 store 内部定义更新函数外，还可以将状态更新函数放在 store 外部，使用 `setState` 进行更新。

#### 示例用法

```javascript
const useBoundStore = create(() => ({
  count: 0,
}));

// 外部更新函数
const increment = () => useBoundStore.setState((state) => ({ count: state.count + 1 }));
const decrement = () => useBoundStore.setState((state) => ({ count: state.count - 1 }));

// 使用示例
increment(); // count 变为 1
decrement(); // count 变为 0
```

#### 注意事项

- 外部更新函数需要通过 `setState` 访问 store 状态。
- 这种方式适合处理简单的状态更新逻辑。
