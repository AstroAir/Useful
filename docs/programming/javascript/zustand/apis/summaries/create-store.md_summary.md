### 函数或方法描述

#### `createStore(stateCreatorFn)`

`createStore` 是一个用于创建 vanilla store 的函数，它暴露了 API 工具，如 `setState`、`getState`、`getInitialState` 和 `subscribe`。

### 示例用法

#### 示例 1: 更新基于前一个状态的状态

```tsx
import { createStore } from 'zustand/vanilla'

type AgeStoreState = { age: number }

type AgeStoreActions = {
  setAge: (
    nextAge:
      | AgeStoreState['age']
      | ((currentAge: AgeStoreState['age']) => AgeStoreState['age']),
  ) => void
}

type AgeStore = AgeStoreState & AgeStoreActions

const ageStore = createStore<AgeStore>()((set) => ({
  age: 42,
  setAge: (nextAge) =>
    set((state) => ({
      age: typeof nextAge === 'function' ? nextAge(state.age) : nextAge,
    })),
}))

function increment() {
  ageStore.getState().setAge((currentAge) => currentAge + 1)
}

const $yourAgeHeading = document.getElementById(
  'your-age',
) as HTMLHeadingElement
const $incrementBy3Button = document.getElementById(
  'increment-by-3',
) as HTMLButtonElement
const $incrementBy1Button = document.getElementById(
  'increment-by-1',
) as HTMLButtonElement

$incrementBy3Button.addEventListener('click', () => {
  increment()
  increment()
  increment()
})

$incrementBy1Button.addEventListener('click', () => {
  increment()
})

const render: Parameters<typeof ageStore.subscribe>[0] = (state) => {
  $yourAgeHeading.innerHTML = `Your age: ${state.age}`
}

render(ageStore.getInitialState(), ageStore.getInitialState())

ageStore.subscribe(render)
```

#### 示例 2: 更新状态中的原始值

```ts
import { createStore } from 'zustand/vanilla'

type XStore = number

const xStore = createStore<XStore>()(() => 0)

const $dotContainer = document.getElementById('dot-container') as HTMLDivElement
const $dot = document.getElementById('dot') as HTMLDivElement

$dotContainer.addEventListener('pointermove', (event) => {
  xStore.setState(event.clientX, true)
})

const render: Parameters<typeof xStore.subscribe>[0] = (x) => {
  $dot.style.transform = `translate(${x}px, 0)`
}

render(xStore.getInitialState(), xStore.getInitialState())

xStore.subscribe(render)
```

#### 示例 3: 更新状态中的对象

```ts
import { createStore } from 'zustand/vanilla'

type PositionStoreState = { position: { x: number; y: number } }

type PositionStoreActions = {
  setPosition: (nextPosition: PositionStoreState['position']) => void
}

type PositionStore = PositionStoreState & PositionStoreActions

const positionStore = createStore<PositionStore>()((set) => ({
  position: { x: 0, y: 0 },
  setPosition: (position) => set({ position }),
}))

const $dotContainer = document.getElementById('dot-container') as HTMLDivElement
const $dot = document.getElementById('dot') as HTMLDivElement

$dotContainer.addEventListener('pointermove', (event) => {
  positionStore.getState().setPosition({
    x: event.clientX,
    y: event.clientY,
  })
})

const render: Parameters<typeof positionStore.subscribe>[0] = (state) => {
  $dot.style.transform = `translate(${state.position.x}px, ${state.position.y}px)`
}

render(positionStore.getInitialState(), positionStore.getInitialState())

positionStore.subscribe(render)
```

#### 示例 4: 更新状态中的数组

```ts
import { createStore } from 'zustand/vanilla'

type PositionStore = [number, number]

const positionStore = create<PositionStore>()(() => [0, 0])

const $dotContainer = document.getElementById('dot-container') as HTMLDivElement
const $dot = document.getElementById('dot') as HTMLDivElement

$dotContainer.addEventListener('pointermove', (event) => {
  positionStore.setState([event.clientX, event.clientY], true)
})

const render: Parameters<typeof positionStore.subscribe>[0] = ([x, y]) => {
  $dot.style.transform = `translate(${x}px, ${y}px)`
}

render(positionStore.getInitialState(), positionStore.getInitialState())

positionStore.subscribe(render)
```

#### 示例 5: 订阅状态更新

```ts
import { createStore } from 'zustand/vanilla'

type PositionStoreState = { position: { x: number; y: number } }

type PositionStoreActions = {
  setPosition: (nextPosition: PositionStoreState['position']) => void
}

type PositionStore = PositionStoreState & PositionStoreActions

const positionStore = createStore<PositionStore>()((set) => ({
  position: { x: 0, y: 0 },
  setPosition: (position) => set({ position }),
}))

const $dot = document.getElementById('dot') as HTMLDivElement

$dot.addEventListener('mouseenter', (event) => {
  const parent = event.currentTarget.parentElement
  const parentWidth = parent.clientWidth
  const parentHeight = parent.clientHeight

  positionStore.getState().setPosition({
    x: Math.ceil(Math.random() * parentWidth),
    y: Math.ceil(Math.random() * parentHeight),
  })
})

const render: Parameters<typeof positionStore.subscribe>[0] = (state) => {
  $dot.style.transform = `translate(${state.position.x}px, ${state.position.y}px)`
}

render(positionStore.getInitialState(), positionStore.getInitialState())

positionStore.subscribe(render)

const logger: Parameters<typeof positionStore.subscribe>[0] = (state) => {
  console.log('new position', { position: state.position })
}

positionStore.subscribe(logger)
```

### 注意事项

1. **状态更新**：`set` 函数默认执行浅合并。如果需要完全替换状态，请使用 `replace` 参数设置为 `true`。
2. **对象和数组更新**：在更新对象和数组时，应将其视为不可变数据，创建新对象或数组进行更新。
3. **订阅更新**：通过 `subscribe` 方法可以注册回调函数，当状态更新时触发。
4. **避免直接修改状态**：直接修改状态可能导致视图不更新，应通过 `set` 函数更新状态。
