# JSON Compression Tool

This Python utility provides efficient compression of JSON conversation data, specifically designed for AI training datasets and chat message collections. It transforms multi-line JSON files into compact JSONL (JSON Lines) format while preserving message structure and content.

## Overview

The JSON Compression tool is designed to:
- **Compress JSON Data** - Convert multi-line JSON to single-line format
- **Preserve Structure** - Maintain message roles and content integrity
- **Optimize Storage** - Reduce file size and improve loading performance
- **Support AI Datasets** - Handle conversation-based training data

## Features

### Data Compression
- **Single-Line Output** - Converts each JSON object to a single line
- **Whitespace Removal** - Eliminates unnecessary whitespace from content
- **Structure Preservation** - Maintains original message hierarchy
- **Unicode Support** - Handles international characters correctly

### File Processing
- **Batch Processing** - Handle large JSON files efficiently
- **Error Handling** - Robust error management for malformed data
- **Encoding Support** - UTF-8 encoding for international content
- **Progress Feedback** - Clear status reporting during processing

## Installation

### Prerequisites
```bash
# No additional packages required - uses Python standard library
python --version  # Requires Python 3.6+
```

### Dependencies
- `json` - JSON parsing and generation (built-in)
- `os` - File system operations (built-in)

## Usage

### Basic Usage
```python
from compress import compress_to_single_line

# Compress a JSON file to JSONL format
compress_to_single_line("input.json", "output.jsonl")
```

### Input Format
The tool expects JSON files with conversation structure:
```json
[
  {
    "messages": [
      {
        "role": "user",
        "content": "What is machine learning?"
      },
      {
        "role": "assistant", 
        "content": "Machine learning is a subset of artificial intelligence..."
      }
    ]
  }
]
```

### Output Format
Produces JSONL format with compressed content:
```jsonl
{"messages": [{"role": "user", "content": "What is machine learning?"}, {"role": "assistant", "content": "Machine learning is a subset of artificial intelligence..."}]}
```

## Core Functions

### Main Compression Function
```python
def compress_to_single_line(input_file, output_file):
    """
    Compress JSON conversation data to single-line format
    
    Args:
        input_file (str): Path to input JSON file
        output_file (str): Path to output JSONL file
    """
    try:
        # Read and parse input JSON
        with open(input_file, "r", encoding="utf-8") as infile:
            data = json.load(infile)

        # Process and compress data
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

        # Write compressed output
        with open(output_file, "w", encoding="utf-8") as outfile:
            for entry in compressed_data:
                json_line = json.dumps(entry, ensure_ascii=False)
                outfile.write(json_line + "\n")

        print(f"Compression complete! Results saved to {output_file}")
        
    except FileNotFoundError:
        print(f"Input file {input_file} not found.")
    except json.JSONDecodeError:
        print("Input file is not valid JSON format.")
    except Exception as e:
        print(f"Error occurred: {e}")
```

## Advanced Features

### Batch Processing
```python
import os
import glob

def compress_directory(input_dir, output_dir):
    """Compress all JSON files in a directory"""
    os.makedirs(output_dir, exist_ok=True)
    
    for json_file in glob.glob(os.path.join(input_dir, "*.json")):
        filename = os.path.basename(json_file)
        output_file = os.path.join(output_dir, filename.replace('.json', '.jsonl'))
        compress_to_single_line(json_file, output_file)
```

### Content Validation
```python
def validate_message_structure(data):
    """Validate message structure before compression"""
    required_fields = ["messages"]
    message_fields = ["role", "content"]
    
    for item in data:
        if not all(field in item for field in required_fields):
            raise ValueError(f"Missing required fields: {required_fields}")
        
        for message in item["messages"]:
            if not all(field in message for field in message_fields):
                raise ValueError(f"Message missing fields: {message_fields}")
    
    return True
```

### Statistics and Reporting
```python
def get_compression_stats(input_file, output_file):
    """Generate compression statistics"""
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

## Configuration Options

### Custom Content Processing
```python
def custom_content_processor(content):
    """Custom content processing function"""
    # Remove extra whitespace
    content = " ".join(content.split())
    
    # Remove specific patterns (optional)
    import re
    content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
    content = re.sub(r'[^\w\s.,!?-]', '', content)  # Remove special chars
    
    return content.strip()

# Use custom processor
def compress_with_custom_processor(input_file, output_file, processor=None):
    if processor is None:
        processor = lambda x: " ".join(x.split())
    
    # Apply custom processing in compression loop
    content = processor(message.get("content", ""))
```

### Output Format Options
```python
def compress_with_options(input_file, output_file, options=None):
    """Compress with configurable options"""
    default_options = {
        "preserve_formatting": False,
        "include_metadata": False,
        "sort_messages": False,
        "validate_output": True
    }
    
    if options:
        default_options.update(options)
    
    # Apply options during compression
    # ... implementation details
```

## Performance Optimization

### Memory-Efficient Processing
```python
def compress_large_file(input_file, output_file, chunk_size=1000):
    """Process large files in chunks to manage memory"""
    with open(input_file, "r", encoding="utf-8") as infile:
        with open(output_file, "w", encoding="utf-8") as outfile:
            chunk = []
            for line in infile:
                chunk.append(json.loads(line))
                
                if len(chunk) >= chunk_size:
                    process_chunk(chunk, outfile)
                    chunk = []
            
            # Process remaining items
            if chunk:
                process_chunk(chunk, outfile)
```

### Parallel Processing
```python
import concurrent.futures
import multiprocessing

def parallel_compress(file_list, output_dir, max_workers=None):
    """Compress multiple files in parallel"""
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for input_file in file_list:
            output_file = os.path.join(output_dir, 
                                     os.path.basename(input_file).replace('.json', '.jsonl'))
            future = executor.submit(compress_to_single_line, input_file, output_file)
            futures.append(future)
        
        # Wait for completion
        concurrent.futures.wait(futures)
```

## Best Practices

### Data Integrity
- **Backup Original Files** - Always keep backups before compression
- **Validate Input** - Check JSON structure before processing
- **Verify Output** - Confirm compressed data integrity
- **Handle Encoding** - Use UTF-8 for international content

### Performance
- **Chunk Large Files** - Process large datasets in manageable chunks
- **Monitor Memory Usage** - Watch memory consumption during processing
- **Use Parallel Processing** - Leverage multiple cores for batch operations
- **Optimize I/O** - Use appropriate buffer sizes for file operations

### Error Handling
- **Graceful Degradation** - Continue processing other files on individual failures
- **Detailed Logging** - Log errors with context for debugging
- **Recovery Options** - Provide options to resume interrupted operations
- **Validation Checks** - Verify data integrity throughout the process

## Use Cases

### AI Training Data
- **Dataset Preparation** - Compress training datasets for efficient storage
- **Model Fine-tuning** - Prepare conversation data for language model training
- **Data Pipeline** - Integrate into ML data preprocessing workflows

### Data Storage
- **Archive Compression** - Reduce storage requirements for historical data
- **Transfer Optimization** - Minimize bandwidth usage for data transfers
- **Database Import** - Prepare data for database ingestion

### Development Workflows
- **Testing Data** - Create compact test datasets
- **Configuration Files** - Compress configuration and settings files
- **Log Processing** - Compress structured log files for analysis

This tool provides efficient JSON compression capabilities specifically designed for AI and machine learning workflows, with robust error handling and performance optimization features.
