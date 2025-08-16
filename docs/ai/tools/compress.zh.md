# JSON压缩工具

这个Python工具提供了高效的JSON对话数据压缩功能，专为AI训练数据集和聊天消息集合设计。它将多行JSON文件转换为紧凑的JSONL（JSON Lines）格式，同时保留消息结构和内容。

## 概述

JSON压缩工具旨在：

- **压缩JSON数据** - 将多行JSON转换为单行格式
- **保留结构** - 维护消息角色和内容完整性
- **优化存储** - 减少文件大小并提高加载性能
- **支持AI数据集** - 处理基于对话的训练数据

## 功能

### 数据压缩

- **单行输出** - 将每个JSON对象转换为单行
- **移除空白** - 消除内容中不必要的空白
- **结构保留** - 维持原始消息层次结构
- **Unicode支持** - 正确处理国际字符

### 文件处理

- **批量处理** - 高效处理大型JSON文件
- **错误处理** - 针对格式错误数据的健壮错误管理
- **编码支持** - UTF-8编码支持国际内容
- **进度反馈** - 处理过程中提供清晰的状态报告

## 安装

### 前提条件

```bash
# 无需额外包 - 使用Python标准库
python --version  # 需要Python 3.6+
```

### 依赖项

- `json` - JSON解析和生成（内置）
- `os` - 文件系统操作（内置）

## 使用方法

### 基本用法

```python
from compress import compress_to_single_line

# 将JSON文件压缩为JSONL格式
compress_to_single_line("input.json", "output.jsonl")
```

### 输入格式

工具期望具有对话结构的JSON文件：

```json
[
  {
    "messages": [
      {
        "role": "user",
        "content": "什么是机器学习？"
      },
      {
        "role": "assistant", 
        "content": "机器学习是人工智能的一个子集..."
      }
    ]
  }
]
```

### 输出格式

生成压缩内容的JSONL格式：

```jsonl
{"messages": [{"role": "user", "content": "什么是机器学习？"}, {"role": "assistant", "content": "机器学习是人工智能的一个子集..."}]}
```

## 核心函数

### 主压缩函数

```python
def compress_to_single_line(input_file, output_file):
    """
    压缩JSON对话数据为单行格式
    
    参数:
        input_file (str): 输入JSON文件路径
        output_file (str): 输出JSONL文件路径
    """
    try:
        # 读取并解析输入JSON
        with open(input_file, "r", encoding="utf-8") as infile:
            data = json.load(infile)

        # 处理并压缩数据
        compressed_data = []
        for item in data:
            compressed_item = {"messages": []}
            for message in item.get("messages", []):
                role = message.get("role", "")
                content = " ".join(message.get("content", "").split())
                compressed_item["messages"].append({
                    "role": role, 
                    "content": content
                })
            compressed_data.append(compressed_item)

        # 写入压缩输出
        with open(output_file, "w", encoding="utf-8") as outfile:
            for entry in compressed_data:
                json_line = json.dumps(entry, ensure_ascii=False)
                outfile.write(json_line + "\n")

        print(f"压缩完成！结果已保存至 {output_file}")
        
    except FileNotFoundError:
        print(f"输入文件 {input_file} 未找到。")
    except json.JSONDecodeError:
        print("输入文件不是有效的JSON格式。")
    except Exception as e:
        print(f"发生错误: {e}")
```

## 高级功能

### 批量处理

```python
import os
import glob

def compress_directory(input_dir, output_dir):
    """压缩目录中的所有JSON文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    for json_file in glob.glob(os.path.join(input_dir, "*.json")):
        filename = os.path.basename(json_file)
        output_file = os.path.join(output_dir, filename.replace('.json', '.jsonl'))
        compress_to_single_line(json_file, output_file)
```

### 内容验证

```python
def validate_message_structure(data):
    """在压缩前验证消息结构"""
    required_fields = ["messages"]
    message_fields = ["role", "content"]
    
    for item in data:
        if not all(field in item for field in required_fields):
            raise ValueError(f"缺少必需字段: {required_fields}")
        
        for message in item["messages"]:
            if not all(field in message for field in message_fields):
                raise ValueError(f"消息缺少字段: {message_fields}")
    
    return True
```

### 统计与报告

```python
def get_compression_stats(input_file, output_file):
    """生成压缩统计信息"""
    import os
    
    input_size = os.path.getsize(input_file)
    output_size = os.path.getsize(output_file)
    compression_ratio = (input_size - output_size) / input_size * 100
    
    return {
        "input_size": input_size,
        "output_size": output_size,
        "compression_ratio": f"{compression_ratio:.2f}%",
        "size_reduction": input_size - output_size
    }
```

## 配置选项

### 自定义内容处理

```python
def custom_content_processor(content):
    """自定义内容处理函数"""
    # 移除额外空白
    content = " ".join(content.split())
    
    # 移除特定模式（可选）
    import re
    content = re.sub(r'\s+', ' ', content)  # 规范化空白
    content = re.sub(r'[^\w\s.,!?-]', '', content)  # 移除特殊字符
    
    return content.strip()

# 使用自定义处理器
def compress_with_custom_processor(input_file, output_file, processor=None):
    if processor is None:
        processor = lambda x: " ".join(x.split())
    
    # 在压缩循环中应用自定义处理
    content = processor(message.get("content", ""))
```

### 输出格式选项

```python
def compress_with_options(input_file, output_file, options=None):
    """使用可配置选项进行压缩"""
    default_options = {
        "preserve_formatting": False,
        "include_metadata": False,
        "sort_messages": False,
        "validate_output": True
    }
    
    if options:
        default_options.update(options)
    
    # 在压缩过程中应用选项
    # ... 实现细节
```

## 性能优化

### 内存高效处理

```python
def compress_large_file(input_file, output_file, chunk_size=1000):
    """分块处理大型文件以管理内存"""
    with open(input_file, "r", encoding="utf-8") as infile:
        with open(output_file, "w", encoding="utf-8") as outfile:
            chunk = []
            for line in infile:
                chunk.append(json.loads(line))
                
                if len(chunk) >= chunk_size:
                    process_chunk(chunk, outfile)
                    chunk = []
            
            # 处理剩余项目
            if chunk:
                process_chunk(chunk, outfile)
```

### 并行处理

```python
import concurrent.futures
import multiprocessing

def parallel_compress(file_list, output_dir, max_workers=None):
    """并行压缩多个文件"""
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for input_file in file_list:
            output_file = os.path.join(output_dir, 
                                     os.path.basename(input_file).replace('.json', '.jsonl'))
            future = executor.submit(compress_to_single_line, input_file, output_file)
            futures.append(future)
        
        # 等待完成
        concurrent.futures.wait(futures)
```

## 最佳实践

### 数据完整性

- **备份原始文件** - 压缩前始终保留备份
- **验证输入** - 处理前检查JSON结构
- **验证输出** - 确认压缩数据完整性
- **处理编码** - 对国际内容使用UTF-8

### 性能

- **分块处理大型文件** - 以可管理的块处理大型数据集
- **监控内存使用** - 处理过程中监视内存消耗
- **使用并行处理** - 利用多核进行批处理操作
- **优化I/O** - 为文件操作使用适当的缓冲区大小

### 错误处理

- **优雅降级** - 单个文件失败时继续处理其他文件
- **详细日志记录** - 用上下文记录错误以便调试
- **恢复选项** - 提供恢复中断操作的选项
- **验证检查** - 在整个过程中验证数据完整性

## 使用场景

### AI训练数据

- **数据集准备** - 压缩训练数据集以实现高效存储
- **模型微调** - 为语言模型训练准备对话数据
- **数据管道** - 集成到ML数据预处理工作流中

### 数据存储

- **归档压缩** - 减少历史数据的存储需求
- **传输优化** - 最小化数据传输的带宽使用
- **数据库导入** - 为数据库摄入准备数据

### 开发工作流

- **测试数据** - 创建紧凑的测试数据集
- **配置文件** - 压缩配置和设置文件
- **日志处理** - 压缩结构化日志文件进行分析

此工具提供了专为AI和机器学习工作流设计的高效JSON压缩功能，具有健壮的错误处理和性能优化特性。
