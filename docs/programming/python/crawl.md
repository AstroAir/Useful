# Web Crawling and Content Analysis Tool

This comprehensive Python tool provides automated web crawling, file processing, and AI-powered content analysis capabilities. It's designed for large-scale content processing with concurrent execution, progress tracking, and intelligent summarization.

## Overview

The Web Crawling tool combines file system traversal, content extraction, and AI-powered analysis to process large collections of documents. It's particularly useful for:

- **Documentation Analysis** - Processing technical documentation and code files
- **Content Summarization** - Generating summaries of large document collections
- **Code Analysis** - Analyzing codebases for functions and methods
- **Research Automation** - Automated content analysis for research projects

## Key Features

### Multi-threaded Processing

- **Concurrent Execution** - Process multiple files simultaneously
- **Thread Pool Management** - Configurable worker thread count
- **Progress Tracking** - Real-time progress monitoring with tqdm
- **Graceful Interruption** - Signal handling for clean shutdown

### AI-Powered Analysis

- **OpenAI Integration** - Uses DeepSeek API for content analysis
- **Function Documentation** - Automatically generates function/method examples
- **Intelligent Summarization** - Creates structured summaries with usage examples
- **Retry Logic** - Automatic retry on API failures

### File Processing

- **Multiple Formats** - Supports .txt, .md, and .py files
- **Recursive Directory Traversal** - Processes entire directory trees
- **Output Management** - Organized summary file generation
- **Error Handling** - Robust file reading and processing

## Installation

### Prerequisites

```bash
pip install openai concurrent.futures tqdm
```

### API Configuration

```python
from openai import OpenAI

client = OpenAI(
    api_key='your-api-key-here',
    base_url='https://api.deepseek.com/v1'  # or your preferred endpoint
)
```

## Usage

### Basic Usage

```python
import os
from crawl import process_directory

# Process a directory with default settings
directory_path = "/path/to/documents"
process_directory(directory_path)
```

### Advanced Configuration

```python
# Custom thread count and processing
process_directory(
    directory="/path/to/documents",
    max_workers=10,  # Increase for faster processing
    file_extensions=['.txt', '.md', '.py', '.js'],  # Custom file types
    output_dir="./summaries"  # Custom output location
)
```

## Core Functions

### File Discovery

```python
def get_all_files(directory):
    """获取指定目录下所有文件的路径"""
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.txt', '.md', '.py')):
                file_paths.append(os.path.join(root, file))
    return file_paths
```

### Content Analysis

```python
def generate_summary(content):
    """生成内容摘要，提示词更精准"""
    prompt = (
        "请阅读以下文件内容，并为其中出现的函数或方法提供简要示例，"
        "输出需包含以下要点：\n1. 函数或方法描述\n2. 示例用法\n3. 注意事项\n\n"
        f"文件内容：\n\n{content}\n\n请按照上述要求为该文件输出标准化提示词。"
    )
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### Concurrent Processing

```python
def process_directory(directory, max_workers=5):
    """使用线程池并发处理整个目录"""
    files = get_all_files(directory)
    success_count = 0
    failed_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_single_file, file_path): file_path
            for file_path in files
        }
        
        with tqdm(total=len(files), desc="处理进度") as pbar:
            for future in concurrent.futures.as_completed(futures):
                # Process results and update progress
                pbar.update(1)
```

## Configuration Options

### Thread Pool Settings

```python
# Conservative setting for limited resources
max_workers = 3

# Aggressive setting for powerful machines
max_workers = 10

# Auto-detection based on CPU cores
import os
max_workers = min(os.cpu_count(), 8)
```

### API Configuration

```python
# DeepSeek API (default)
client = OpenAI(
    api_key='sk-your-key-here',
    base_url='https://api.deepseek.com/v1'
)

# OpenAI API
client = OpenAI(
    api_key='sk-your-openai-key-here'
)

# Custom endpoint
client = OpenAI(
    api_key='your-key',
    base_url='https://your-custom-endpoint.com/v1'
)
```

### File Type Configuration

```python
# Default supported types
SUPPORTED_EXTENSIONS = ('.txt', '.md', '.py')

# Extended support
SUPPORTED_EXTENSIONS = ('.txt', '.md', '.py', '.js', '.ts', '.java', '.cpp')

# Custom filter function
def should_process_file(file_path):
    return (
        file_path.endswith(SUPPORTED_EXTENSIONS) and
        not file_path.startswith('.') and
        'node_modules' not in file_path
    )
```

## Advanced Features

### Signal Handling

```python
import signal
import sys

interrupted = False

def signal_handler(sig, frame):
    global interrupted
    interrupted = True
    print("\n中断信号接收，正在停止处理...")

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
```

### Retry Logic

```python
def process_single_file(file_path):
    """处理单个文件并支持重试"""
    retry_count = 3
    while retry_count > 0:
        try:
            summary = generate_summary(content)
            if summary:
                save_summary(summary, file_path)
                return True
        except Exception as e:
            retry_count -= 1
            if retry_count == 0:
                print(f"处理文件 {file_path} 失败，已重试3次: {str(e)}")
            time.sleep(1)
    return False
```

### Output Management

```python
def save_summary(summary, original_file_path):
    """保存摘要到文件"""
    # Create output directory structure
    output_dir = "summaries"
    relative_path = os.path.relpath(original_file_path)
    output_path = os.path.join(output_dir, relative_path + "_summary.md")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write summary
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)
```

## Performance Optimization

### Memory Management

```python
# Process files in batches to manage memory
def process_in_batches(files, batch_size=100):
    for i in range(0, len(files), batch_size):
        batch = files[i:i + batch_size]
        process_batch(batch)
        # Optional: garbage collection
        import gc
        gc.collect()
```

### Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_second=1):
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = 1.0 / calls_per_second - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

@rate_limit(calls_per_second=2)  # Limit to 2 API calls per second
def generate_summary(content):
    # API call implementation
    pass
```

### Caching

```python
import hashlib
import json
import os

def get_cache_key(content):
    return hashlib.md5(content.encode()).hexdigest()

def get_cached_summary(content):
    cache_key = get_cache_key(content)
    cache_file = f"cache/{cache_key}.json"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)['summary']
    return None

def cache_summary(content, summary):
    cache_key = get_cache_key(content)
    cache_file = f"cache/{cache_key}.json"
    
    os.makedirs('cache', exist_ok=True)
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump({'summary': summary}, f, ensure_ascii=False)
```

## Best Practices

### Error Handling

- **Graceful Degradation** - Continue processing other files on individual failures
- **Detailed Logging** - Log errors with context for debugging
- **Resource Cleanup** - Ensure proper cleanup on interruption
- **Status Reporting** - Provide clear success/failure statistics

### API Usage

- **Rate Limiting** - Respect API rate limits to avoid throttling
- **Cost Management** - Monitor API usage and costs
- **Error Recovery** - Implement exponential backoff for API failures
- **Content Validation** - Validate API responses before processing

### File Management

- **Path Handling** - Use os.path for cross-platform compatibility
- **Encoding** - Specify UTF-8 encoding for international content
- **Large Files** - Consider streaming for very large files
- **Backup Strategy** - Backup original files before processing

This tool provides a robust foundation for automated content analysis and can be customized for various document processing and analysis workflows.
