### 函数或方法描述

1. **`ReactDOMServer.renderToPipeableStream`**
   - **描述**: 该方法用于在服务器端将 React 组件渲染为可管道化的流。它生成一个 HTML 字符串，并将其通过管道传输到响应对象中。
   - **示例用法**:
     ```tsx
     const { pipe } = ReactDOMServer.renderToPipeableStream(<App />, {
       onShellReady() {
         res.setHeader('content-type', 'text/html');
         pipe(res);
       },
     });
     ```
   - **注意事项**:
     - 该方法通常用于服务器端渲染 (SSR)，生成的 HTML 字符串会被发送到客户端。
     - `onShellReady` 回调函数在 HTML 外壳准备好时触发，此时可以设置响应头并开始管道传输。

2. **`ReactDOMClient.hydrateRoot`**
   - **描述**: 该方法用于在客户端对服务器端渲染的 HTML 进行 hydration，使其变为一个完全交互式的 React 应用。
   - **示例用法**:
     ```tsx
     ReactDOMClient.hydrateRoot(document, <App />);
     ```
   - **注意事项**:
     - 传递给 `hydrateRoot` 的 React 树必须与服务器端生成的 HTML 输出一致，否则会导致 hydration 错误。
     - 常见的 hydration 错误包括：额外的空白字符、使用浏览器特定的 API、服务器和客户端渲染不同的数据等。
     - React 可以恢复一些 hydration 错误，但必须修复这些错误以避免性能下降或事件处理程序附加到错误的元素上。

### 总结

- **`ReactDOMServer.renderToPipeableStream`** 用于服务器端渲染，生成 HTML 字符串并通过管道传输到客户端。
- **`ReactDOMClient.hydrateRoot`** 用于客户端 hydration，将服务器端生成的静态 HTML 转换为交互式的 React 应用。
- 在使用这些方法时，确保服务器和客户端的渲染输出一致，避免常见的 hydration 错误。