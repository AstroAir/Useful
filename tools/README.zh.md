# 工具目录

本目录包含 Python 实用脚本和工具，用于补充本项目中的文档。

[English](README.md) | **中文**

## 可用工具

### 🌐 网络和系统工具

#### `auto_wifi.py`
使用 Selenium WebDriver 的自动化 WiFi 连接管理。

**目的**：自动化基于网络的 WiFi 门户认证
**文档**：参见 [docs/programming/python/auto-wifi.zh.md](../docs/programming/python/auto-wifi.zh.md)
**用法**：配置 WebDriver 路径和门户 URL，然后运行脚本

### 🤖 AI 和数据处理工具

#### `compress.py`
用于 AI 训练数据集的 JSON 对话数据压缩工具。

**目的**：将多行 JSON 转换为紧凑的 JSONL 格式
**文档**：参见 [docs/ai/tools/compress.zh.md](../docs/ai/tools/compress.zh.md)
**用法**：`python compress.py input.json output.jsonl`

#### `convert.py`
用于 AI 训练工作流程的数据格式转换工具。

**目的**：在不同格式之间转换对话数据
**文档**：参见 [docs/ai/tools/convert.zh.md](../docs/ai/tools/convert.zh.md)
**用法**：在您的脚本中导入并使用转换函数

#### `crawl.py`
网络爬虫和 AI 驱动的内容分析工具。

**目的**：多线程文件处理与 AI 摘要
**文档**：参见 [docs/programming/python/crawl.zh.md](../docs/programming/python/crawl.zh.md)
**用法**：配置 API 密钥并在目标目录上运行

## 安装

### 先决条件
```bash
pip install selenium openai concurrent.futures tqdm
```

### WebDriver 设置（用于 auto_wifi.py）
1. 下载 Microsoft Edge WebDriver
2. 更新脚本中的驱动程序路径
3. 配置您的网络门户 URL

### API 配置（用于 crawl.py）
1. 设置 OpenAI 或 DeepSeek API 凭据
2. 在脚本中配置 API 端点
3. 根据需要调整处理参数

## 使用示例

### WiFi 自动化
```bash
python auto_wifi.py
```

### JSON 压缩
```python
from compress import compress_to_single_line
compress_to_single_line("conversations.json", "compressed.jsonl")
```

### 内容分析
```bash
python crawl.py /path/to/documents
```

## 文档

有关详细文档、示例和最佳实践，请参见 `docs/` 目录中的相应文档文件：

- [Python 工具概述](../docs/programming/python/index.zh.md)
- [AI 工具概述](../docs/ai/tools/index.zh.md)
- [完整文档](../docs/index.zh.md)

## 贡献

这些工具是更大文档项目的一部分。要贡献：

1. 根据需要更新工具脚本
2. 更新 `docs/` 中的相应文档
3. 彻底测试工具
4. 如果添加新工具，请更新此 README

## 许可证

这些工具按原样提供，用于教育和实际用途。有关许可信息，请参见主项目文档。
