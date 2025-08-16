# 数据格式转换工具

这个Python工具用于在不同格式之间转换对话数据，专为AI训练数据集设计。它将结构化对话数据转换为适合语言模型训练和微调的标准消息格式。

## 概述

数据格式转换工具旨在：

- **转换数据结构** - 在不同对话格式之间进行转换
- **标准化消息** - 为AI训练创建一致的消息结构
- **添加系统提示** - 将系统级指令注入对话中
- **支持训练工作流** - 为各种AI训练框架准备数据

## 功能

### 格式转换

- **对话重构** - 转换嵌套的对话结构
- **消息标准化** - 创建基于角色的一致消息格式
- **系统提示注入** - 向对话中添加系统级指令
- **多轮对话支持** - 处理复杂的多轮对话

### AI训练集成

- **训练数据准备** - 为语言模型训练格式化数据
- **微调支持** - 创建用于模型微调的数据集
- **提示工程** - 集成高级提示策略
- **质量保证** - 验证输出格式是否与训练兼容

## 安装

### 前提条件

```bash
# 无需额外包 - 使用Python标准库
python --version  # 需要Python 3.6+
```

### 依赖项

- `json` - JSON解析和生成（内置）

## 使用方法

### 基本用法

```python
from convert import transform_data

# 转换对话数据
input_data = [...]  # 您的输入数据
transformed_data = transform_data(input_data)
```

### 输入格式

工具期望具有对话结构的数据：

```json
[
  {
    "system": "系统指令文本",
    "conversations": [
      {
        "from": "user",
        "value": "用户消息内容"
      },
      {
        "from": "assistant", 
        "value": "助手响应内容"
      }
    ]
  }
]
```

### 输出格式

生成标准化消息格式：

```json
[
  {
    "messages": [
      {
        "role": "system",
        "content": "作为助手，您的角色涉及在提供最终精确准确的解决方案之前，通过系统化的深入思考过程彻底探索问题..."
      },
      {
        "role": "user",
        "content": "用户消息内容"
      },
      {
        "role": "assistant",
        "content": "助手响应内容"
      }
    ]
  }
]
```

## 核心函数

### 主转换函数

```python
def transform_data(input_data):
    """
    将对话数据转换为标准化消息格式
    
    参数:
        input_data (list): 对话对象列表
        
    返回:
        list: 具有标准化消息结构的转换后数据
    """
    transformed = []
    
    for item in input_data:
        # 提取带有高级提示的系统消息
        system_message = {
            "role": "system",
            "content": "作为助手，您的角色涉及在提供最终精确准确的解决方案之前，通过系统化的深入思考过程彻底探索问题。这需要参与全面的分析、总结、探索、重新评估、反思、回溯和迭代循环，以开发深思熟虑的思考过程。请将您的响应结构化为两个主要部分：思考和解决方案。在思考部分，使用指定格式详细说明您的推理过程：<|begin_of_thought|> {用'\\n\\n'分隔的步骤思考} <|end_of_thought|> 每个步骤应包括详细考虑，如分析问题、总结相关发现、头脑风暴新想法、验证当前步骤的准确性、修正任何错误以及重新审视先前步骤。在解决方案部分，基于思考部分的各种尝试、探索和反思，系统地呈现您认为正确的最终解决方案。解决方案应保持逻辑清晰、准确简洁的表达风格，并详细说明得出结论所需的必要步骤，格式如下：<|begin_of_solution|> {最终格式化、精确清晰的解决方案} <|end_of_solution|> 现在，尝试通过上述指南解决以下问题："
        }

        # 处理对话
        for conversation in item["conversations"]:
            user_message = {
                "role": "user",
                "content": conversation["value"]
            }
            assistant_message = {
                "role": "assistant",
                "content": conversation["value"]
            }

            # 创建完整交互
            transformed.append({
                "messages": [
                    system_message,
                    user_message,
                    assistant_message
                ]
            })

    return transformed
```

## 高级功能

### 自定义系统提示

```python
def create_system_prompt(prompt_type="reasoning"):
    """生成不同类型的系统提示"""
    prompts = {
        "reasoning": "作为助手，您的角色涉及通过系统化的深入思考过程彻底探索问题...",
        "creative": "您是一位以创新思维和原创解决方案处理问题的创意助手...",
        "analytical": "您是一位将复杂问题分解为可管理组件的分析型助手...",
        "educational": "您是一位清晰解释概念并提供以学习为中心的响应的教育型助手..."
    }
    return prompts.get(prompt_type, prompts["reasoning"])

def transform_with_custom_prompt(input_data, prompt_type="reasoning"):
    """使用自定义系统提示转换数据"""
    system_content = create_system_prompt(prompt_type)
    
    # 在转换中使用自定义提示
    # ... 实现细节
```

### 多格式支持

```python
def detect_input_format(data):
    """自动检测输入数据格式"""
    if isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        
        if "conversations" in first_item:
            return "conversation_format"
        elif "messages" in first_item:
            return "message_format"
        elif "instruction" in first_item:
            return "instruction_format"
    
    return "unknown_format"

def transform_auto_detect(input_data):
    """使用自动格式检测转换数据"""
    format_type = detect_input_format(input_data)
    
    if format_type == "conversation_format":
        return transform_data(input_data)
    elif format_type == "message_format":
        return input_data  # 已经是正确格式
    else:
        raise ValueError(f"不支持的格式: {format_type}")
```

### 批量处理

```python
import os
import json

def convert_directory(input_dir, output_dir, prompt_type="reasoning"):
    """转换目录中的所有JSON文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            with open(input_path, 'r', encoding='utf-8') as f:
                input_data = json.load(f)
            
            transformed_data = transform_with_custom_prompt(input_data, prompt_type)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(transformed_data, f, ensure_ascii=False, indent=2)
```

## 配置选项

### 提示模板

```python
class PromptTemplate:
    def __init__(self, template_type="reasoning"):
        self.templates = {
            "reasoning": {
                "system": "作为助手，您的角色涉及...",
                "format": "<|begin_of_thought|>...{thought}...<|end_of_thought|>",
                "solution": "<|begin_of_solution|>...{solution}...<|end_of_solution|>"
            },
            "code": {
                "system": "您是一位提供...的编程助手",
                "format": "```{language}\n{code}\n```",
                "explanation": "## 解释\n{explanation}"
            }
        }
    
    def get_template(self, template_type):
        return self.templates.get(template_type, self.templates["reasoning"])
```

### 验证与质量控制

```python
def validate_transformed_data(data):
    """验证转换后的数据结构"""
    required_fields = ["messages"]
    message_fields = ["role", "content"]
    valid_roles = ["system", "user", "assistant"]
    
    for item in data:
        # 检查顶层结构
        if not all(field in item for field in required_fields):
            raise ValueError(f"缺少必需字段: {required_fields}")
        
        # 检查消息结构
        for message in item["messages"]:
            if not all(field in message for field in message_fields):
                raise ValueError(f"消息缺少字段: {message_fields}")
            
            if message["role"] not in valid_roles:
                raise ValueError(f"无效角色: {message['role']}")
    
    return True

def quality_check(data):
    """对转换后的数据执行质量检查"""
    stats = {
        "total_conversations": len(data),
        "total_messages": sum(len(item["messages"]) for item in data),
        "avg_messages_per_conversation": 0,
        "roles_distribution": {}
    }
    
    # 计算统计信息
    if stats["total_conversations"] > 0:
        stats["avg_messages_per_conversation"] = stats["total_messages"] / stats["total_conversations"]
    
    # 统计角色分布
    for item in data:
        for message in item["messages"]:
            role = message["role"]
            stats["roles_distribution"][role] = stats["roles_distribution"].get(role, 0) + 1
    
    return stats
```

## 性能优化

### 内存高效处理

```python
def transform_streaming(input_file, output_file, chunk_size=1000):
    """使用流式处理转换大型文件"""
    with open(input_file, 'r', encoding='utf-8') as infile:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write('[\n')
            
            chunk = []
            first_item = True
            
            for line in infile:
                if line.strip():
                    chunk.append(json.loads(line))
                
                if len(chunk) >= chunk_size:
                    transformed_chunk = transform_data(chunk)
                    
                    for item in transformed_chunk:
                        if not first_item:
                            outfile.write(',\n')
                        json.dump(item, outfile, ensure_ascii=False)
                        first_item = False
                    
                    chunk = []
            
            # 处理剩余项目
            if chunk:
                transformed_chunk = transform_data(chunk)
                for item in transformed_chunk:
                    if not first_item:
                        outfile.write(',\n')
                    json.dump(item, outfile, ensure_ascii=False)
            
            outfile.write('\n]')
```

### 并行处理

```python
import concurrent.futures
import multiprocessing

def parallel_transform(data_chunks, max_workers=None):
    """并行转换数据块"""
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(transform_data, chunk) for chunk in data_chunks]
        results = []
        
        for future in concurrent.futures.as_completed(futures):
            results.extend(future.result())
    
    return results
```

## 最佳实践

### 数据质量

- **输入验证** - 转换前验证输入数据结构
- **输出验证** - 确认转换后的数据满足要求
- **内容保留** - 确保转换过程中无数据丢失
- **编码处理** - 对国际内容使用UTF-8

### 性能

- **批量处理** - 高效处理多个文件
- **内存管理** - 对大型数据集使用流式处理
- **并行处理** - 利用多核进行大型转换
- **进度监控** - 跟踪大型数据集的转换进度

### 训练集成

- **格式兼容性** - 确保输出与目标训练框架兼容
- **提示工程** - 为特定用例设计有效的系统提示
- **质量指标** - 在整个管道中监控数据质量
- **版本控制** - 跟踪不同版本的转换逻辑

## 使用场景

### AI模型训练

- **微调数据集** - 为模型微调准备对话数据
- **指令遵循** - 创建指令遵循训练数据集
- **推理训练** - 开发用于推理能力训练的数据集

### 数据管道集成

- **ETL流程** - 集成到数据提取、转换和加载工作流中
- **数据标准化** - 从多个来源规范化对话数据
- **质量保证** - 确保系统间数据格式一致

### 研究与开发

- **实验准备** - 为AI研究实验创建数据集
- **提示工程** - 测试不同的提示策略
- **模型评估** - 准备具有统一格式的评估数据集

此工具提供了专为AI训练工作流设计的灵活数据转换功能，支持各种输入格式和可定制的输出结构。
