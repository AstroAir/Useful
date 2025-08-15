# Tools Directory

This directory contains Python utility scripts and tools that complement the documentation in this project.

## Available Tools

### 🌐 Network and System Tools

#### `auto_wifi.py`
Automated WiFi connection management using Selenium WebDriver.

**Purpose**: Automates web-based WiFi portal authentication
**Documentation**: See [docs/programming/python/auto-wifi.md](../docs/programming/python/auto-wifi.md)
**Usage**: Configure WebDriver path and portal URL, then run the script

### 🤖 AI and Data Processing Tools

#### `compress.py`
JSON conversation data compression tool for AI training datasets.

**Purpose**: Converts multi-line JSON to compact JSONL format
**Documentation**: See [docs/ai/tools/compress.md](../docs/ai/tools/compress.md)
**Usage**: `python compress.py input.json output.jsonl`

#### `convert.py`
Data format conversion tool for AI training workflows.

**Purpose**: Transforms conversation data between different formats
**Documentation**: See [docs/ai/tools/convert.md](../docs/ai/tools/convert.md)
**Usage**: Import and use the transformation functions in your scripts

#### `crawl.py`
Web crawling and AI-powered content analysis tool.

**Purpose**: Multi-threaded file processing with AI summarization
**Documentation**: See [docs/programming/python/crawl.md](../docs/programming/python/crawl.md)
**Usage**: Configure API keys and run on target directories

## Installation

### Prerequisites
```bash
pip install selenium openai concurrent.futures tqdm
```

### WebDriver Setup (for auto_wifi.py)
1. Download Microsoft Edge WebDriver
2. Update the driver path in the script
3. Configure your network portal URL

### API Configuration (for crawl.py)
1. Set up OpenAI or DeepSeek API credentials
2. Configure the API endpoint in the script
3. Adjust processing parameters as needed

## Usage Examples

### WiFi Automation
```bash
python auto_wifi.py
```

### JSON Compression
```python
from compress import compress_to_single_line
compress_to_single_line("conversations.json", "compressed.jsonl")
```

### Content Analysis
```bash
python crawl.py /path/to/documents
```

## Documentation

For detailed documentation, examples, and best practices, see the corresponding documentation files in the `docs/` directory:

- [Python Tools Overview](../docs/programming/python/index.md)
- [AI Tools Overview](../docs/ai/tools/)
- [Complete Documentation](../docs/)

## Contributing

These tools are part of the larger documentation project. To contribute:

1. Update the tool scripts as needed
2. Update the corresponding documentation in `docs/`
3. Test the tools thoroughly
4. Update this README if adding new tools

## License

These tools are provided as-is for educational and practical use. See the main project documentation for licensing information.
