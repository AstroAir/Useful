# Data Format Conversion Tool

This Python utility transforms conversation data between different formats, specifically designed for AI training datasets. It converts structured conversation data into standardized message formats suitable for language model training and fine-tuning.

## Overview

The Data Format Conversion tool is designed to:
- **Transform Data Structures** - Convert between different conversation formats
- **Standardize Messages** - Create consistent message structures for AI training
- **Add System Prompts** - Inject system-level instructions into conversations
- **Support Training Workflows** - Prepare data for various AI training frameworks

## Features

### Format Transformation
- **Conversation Restructuring** - Transform nested conversation structures
- **Message Standardization** - Create consistent role-based message format
- **System Prompt Injection** - Add system-level instructions to conversations
- **Multi-turn Support** - Handle complex multi-turn conversations

### AI Training Integration
- **Training Data Preparation** - Format data for language model training
- **Fine-tuning Support** - Create datasets for model fine-tuning
- **Prompt Engineering** - Integrate advanced prompting strategies
- **Quality Assurance** - Validate output format for training compatibility

## Installation

### Prerequisites
```bash
# No additional packages required - uses Python standard library
python --version  # Requires Python 3.6+
```

### Dependencies
- `json` - JSON parsing and generation (built-in)

## Usage

### Basic Usage
```python
from convert import transform_data

# Transform conversation data
input_data = [...]  # Your input data
transformed_data = transform_data(input_data)
```

### Input Format
The tool expects data with conversation structure:
```json
[
  {
    "system": "System instruction text",
    "conversations": [
      {
        "from": "user",
        "value": "User message content"
      },
      {
        "from": "assistant", 
        "value": "Assistant response content"
      }
    ]
  }
]
```

### Output Format
Produces standardized message format:
```json
[
  {
    "messages": [
      {
        "role": "system",
        "content": "Your role as an assistant involves thoroughly exploring questions..."
      },
      {
        "role": "user",
        "content": "User message content"
      },
      {
        "role": "assistant",
        "content": "Assistant response content"
      }
    ]
  }
]
```

## Core Functions

### Main Transformation Function
```python
def transform_data(input_data):
    """
    Transform conversation data to standardized message format
    
    Args:
        input_data (list): List of conversation objects
        
    Returns:
        list: Transformed data with standardized message structure
    """
    transformed = []
    
    for item in input_data:
        # Extract system message with advanced prompting
        system_message = {
            "role": "system",
            "content": "Your role as an assistant involves thoroughly exploring questions through a systematic long thinking process before providing the final precise and accurate solutions. This requires engaging in a comprehensive cycle of analysis, summarizing, exploration, reassessment, reflection, backtracing, and iteration to develop well-considered thinking process. Please structure your response into two main sections: Thought and Solution. In the Thought section, detail your reasoning process using the specified format: <|begin_of_thought|> {thought with steps separated with '\\n\\n'} <|end_of_thought|> Each step should include detailed considerations such as analisying questions, summarizing relevant findings, brainstorming new ideas, verifying the accuracy of the current steps, refining any errors, and revisiting previous steps. In the Solution section, based on various attempts, explorations, and reflections from the Thought section, systematically present the final solution that you deem correct. The solution should remain a logical, accurate, concise expression style and detail necessary step needed to reach the conclusion, formatted as follows: <|begin_of_solution|> {final formatted, precise, and clear solution} <|end_of_solution|> Now, try to solve the following question through the above guidelines:"
        }

        # Process conversations
        for conversation in item["conversations"]:
            user_message = {
                "role": "user",
                "content": conversation["value"]
            }
            assistant_message = {
                "role": "assistant",
                "content": conversation["value"]
            }

            # Create complete interaction
            transformed.append({
                "messages": [
                    system_message,
                    user_message,
                    assistant_message
                ]
            })

    return transformed
```

## Advanced Features

### Custom System Prompts
```python
def create_system_prompt(prompt_type="reasoning"):
    """Generate different types of system prompts"""
    prompts = {
        "reasoning": "Your role as an assistant involves thoroughly exploring questions through a systematic long thinking process...",
        "creative": "You are a creative assistant that approaches problems with innovative thinking and original solutions...",
        "analytical": "You are an analytical assistant that breaks down complex problems into manageable components...",
        "educational": "You are an educational assistant that explains concepts clearly and provides learning-focused responses..."
    }
    return prompts.get(prompt_type, prompts["reasoning"])

def transform_with_custom_prompt(input_data, prompt_type="reasoning"):
    """Transform data with custom system prompt"""
    system_content = create_system_prompt(prompt_type)
    
    # Use custom prompt in transformation
    # ... implementation details
```

### Multi-format Support
```python
def detect_input_format(data):
    """Automatically detect input data format"""
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
    """Transform data with automatic format detection"""
    format_type = detect_input_format(input_data)
    
    if format_type == "conversation_format":
        return transform_data(input_data)
    elif format_type == "message_format":
        return input_data  # Already in correct format
    else:
        raise ValueError(f"Unsupported format: {format_type}")
```

### Batch Processing
```python
import os
import json

def convert_directory(input_dir, output_dir, prompt_type="reasoning"):
    """Convert all JSON files in a directory"""
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

## Configuration Options

### Prompt Templates
```python
class PromptTemplate:
    def __init__(self, template_type="reasoning"):
        self.templates = {
            "reasoning": {
                "system": "Your role as an assistant involves...",
                "format": "<|begin_of_thought|>...{thought}...<|end_of_thought|>",
                "solution": "<|begin_of_solution|>...{solution}...<|end_of_solution|>"
            },
            "code": {
                "system": "You are a programming assistant that provides...",
                "format": "```{language}\n{code}\n```",
                "explanation": "## Explanation\n{explanation}"
            }
        }
    
    def get_template(self, template_type):
        return self.templates.get(template_type, self.templates["reasoning"])
```

### Validation and Quality Control
```python
def validate_transformed_data(data):
    """Validate transformed data structure"""
    required_fields = ["messages"]
    message_fields = ["role", "content"]
    valid_roles = ["system", "user", "assistant"]
    
    for item in data:
        # Check top-level structure
        if not all(field in item for field in required_fields):
            raise ValueError(f"Missing required fields: {required_fields}")
        
        # Check message structure
        for message in item["messages"]:
            if not all(field in message for field in message_fields):
                raise ValueError(f"Message missing fields: {message_fields}")
            
            if message["role"] not in valid_roles:
                raise ValueError(f"Invalid role: {message['role']}")
    
    return True

def quality_check(data):
    """Perform quality checks on transformed data"""
    stats = {
        "total_conversations": len(data),
        "total_messages": sum(len(item["messages"]) for item in data),
        "avg_messages_per_conversation": 0,
        "roles_distribution": {}
    }
    
    # Calculate statistics
    if stats["total_conversations"] > 0:
        stats["avg_messages_per_conversation"] = stats["total_messages"] / stats["total_conversations"]
    
    # Count role distribution
    for item in data:
        for message in item["messages"]:
            role = message["role"]
            stats["roles_distribution"][role] = stats["roles_distribution"].get(role, 0) + 1
    
    return stats
```

## Performance Optimization

### Memory-Efficient Processing
```python
def transform_streaming(input_file, output_file, chunk_size=1000):
    """Transform large files using streaming processing"""
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
            
            # Process remaining items
            if chunk:
                transformed_chunk = transform_data(chunk)
                for item in transformed_chunk:
                    if not first_item:
                        outfile.write(',\n')
                    json.dump(item, outfile, ensure_ascii=False)
            
            outfile.write('\n]')
```

### Parallel Processing
```python
import concurrent.futures
import multiprocessing

def parallel_transform(data_chunks, max_workers=None):
    """Transform data chunks in parallel"""
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(transform_data, chunk) for chunk in data_chunks]
        results = []
        
        for future in concurrent.futures.as_completed(futures):
            results.extend(future.result())
    
    return results
```

## Best Practices

### Data Quality
- **Input Validation** - Verify input data structure before transformation
- **Output Validation** - Confirm transformed data meets requirements
- **Content Preservation** - Ensure no data loss during transformation
- **Encoding Handling** - Use UTF-8 for international content

### Performance
- **Batch Processing** - Process multiple files efficiently
- **Memory Management** - Use streaming for large datasets
- **Parallel Processing** - Leverage multiple cores for large transformations
- **Progress Monitoring** - Track transformation progress for large datasets

### Training Integration
- **Format Compatibility** - Ensure output works with target training frameworks
- **Prompt Engineering** - Design effective system prompts for specific use cases
- **Quality Metrics** - Monitor data quality throughout the pipeline
- **Version Control** - Track different versions of transformation logic

## Use Cases

### AI Model Training
- **Fine-tuning Datasets** - Prepare conversation data for model fine-tuning
- **Instruction Following** - Create instruction-following training datasets
- **Reasoning Training** - Develop datasets for reasoning capability training

### Data Pipeline Integration
- **ETL Processes** - Integrate into data extraction, transformation, and loading workflows
- **Data Standardization** - Normalize conversation data from multiple sources
- **Quality Assurance** - Ensure consistent data format across systems

### Research and Development
- **Experiment Preparation** - Create datasets for AI research experiments
- **Prompt Engineering** - Test different prompting strategies
- **Model Evaluation** - Prepare evaluation datasets with consistent formatting

This tool provides flexible data transformation capabilities specifically designed for AI training workflows, with support for various input formats and customizable output structures.
