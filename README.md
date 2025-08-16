# Useful - Technical Documentation Collection / 技术文档集合

[English](#english) | [中文](#中文)

## English

A comprehensive collection of useful documents, tools, and guides across programming, AI, astronomy, and more. This repository has been organized and restructured to support MkDocs static site generation for better navigation and accessibility.

## 中文

这是一个全面的技术文档集合，涵盖编程、人工智能、天文学等多个领域的实用文档、工具和指南。本仓库已经过重新组织和结构化，支持 MkDocs 静态网站生成，提供更好的导航和可访问性。

## 📚 Documentation Structure

The documentation is now organized into logical sections:

### 🖥️ Programming
- **C Programming** - Fundamentals, data structures, file operations
- **C++ Programming** - Modern C++20 features, type erasure, string operations
- **C# Programming** - Data structures and TCP programming
- **JavaScript** - PrimeVue UI components and Zustand state management
- **Python** - Automation tools and web crawling utilities

### 🤖 Artificial Intelligence
- Building effective AI agents
- Sky-T1 model documentation (cost-effective O1-preview training)
- AI tools for data compression and format conversion

### 🔭 Astronomy
- **NINA** - Touch'N'Stars mobile control interface
- **Siril** - Python integration for astronomical image processing

### 🐧 Linux
- Command-line tools and utilities (grep, system administration)

### 📚 Libraries
- Documentation for useful programming libraries (scnlib)

### ✍️ Creative Writing
- Original science fiction stories exploring quantum physics and technology

## 📚 文档结构

文档现在按逻辑部分组织：

### 🖥️ 编程
- **C 编程** - 基础知识、数据结构、文件操作
- **C++ 编程** - 现代 C++20 特性、类型擦除、字符串操作
- **C# 编程** - 数据结构和 TCP 编程
- **JavaScript** - PrimeVue UI 组件和 Zustand 状态管理
- **Python** - 自动化工具和网络爬虫实用程序

### 🤖 人工智能
- 构建有效的 AI 代理
- Sky-T1 模型文档（经济高效的 O1-preview 训练）
- 数据压缩和格式转换的 AI 工具

### 🔭 天文学
- **NINA** - Touch'N'Stars 移动控制界面
- **Siril** - 天文图像处理的 Python 集成

### 🐧 Linux
- 命令行工具和实用程序（grep、系统管理）

### 📚 库
- 有用编程库的文档（scnlib）

### ✍️ 创意写作
- 探索量子物理和技术的原创科幻故事

## 🚀 Getting Started

### View Documentation Online
The documentation is built using MkDocs with Material theme for a professional, searchable interface.

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Serve Documentation Locally**
   ```bash
   mkdocs serve
   ```
   Then open http://127.0.0.1:8000 in your browser.
   Use the language switcher in the top-right corner to switch between English and Chinese.

3. **Build Static Site**
   ```bash
   mkdocs build
   ```
   The built site will be in the `site/` directory with separate language versions.

## 🌐 多语言支持 / Multilingual Support

This documentation supports both English and Chinese with professional language switching:

- **🔄 Automatic Language Switcher** - Top-right corner language selector
- **📁 Independent Language Versions** - Separate builds for each language
- **🔍 Multilingual Search** - Search content in both English and Chinese
- **🌍 SEO Optimized** - Proper hreflang tags and language-specific URLs
- **📱 Mobile Friendly** - Language switching works on all devices

### 语言切换设置 / Language Setup

本文档系统使用 `mkdocs-static-i18n` 插件实现专业的多语言支持。
This documentation system uses the `mkdocs-static-i18n` plugin for professional multilingual support.

详细设置说明请参考：[国际化设置指南](docs/i18n-setup.md)
For detailed setup instructions, see: [Internationalization Setup Guide](docs/i18n-setup.md)

## 📖 Documentation Features

- **Material Design** - Clean, modern interface with dark/light mode
- **Full-Text Search** - Quickly find content across all documentation
- **Mobile Responsive** - Optimized for all device sizes
- **Navigation Tabs** - Organized by major topic areas
- **Code Highlighting** - Syntax highlighting for multiple languages
- **Cross-References** - Internal linking between related topics

## 🛠️ Technical Details

### MkDocs Configuration
- **Theme**: Material for MkDocs
- **Plugins**: Search, navigation enhancements
- **Extensions**: Code highlighting, admonitions, tables
- **Languages**: Multi-language support (English/Chinese)

### Project Structure
```
├── docs/                 # Documentation source files
│   ├── index.md         # Main landing page
│   ├── programming/     # Programming tutorials and guides
│   ├── ai/              # AI and machine learning content
│   ├── astronomy/       # Astronomy tools and guides
│   ├── linux/           # Linux tools and utilities
│   ├── libraries/       # Library documentation
│   └── creative/        # Creative writing content
├── mkdocs.yml           # MkDocs configuration
├── requirements.txt     # Python dependencies
└── site/                # Generated static site (after build)
```

## 🔧 Contributing

To add or update documentation:

1. Edit files in the `docs/` directory
2. Test locally with `mkdocs serve`
3. Update navigation in `mkdocs.yml` if adding new sections
4. Build and verify with `mkdocs build`

## 📝 Content Overview

This collection includes:
- **150+ pages** of technical documentation
- **Multiple programming languages** with practical examples
- **AI/ML resources** including cost-effective training approaches
- **Astronomy tools** for astrophotography and image processing
- **System administration** guides and utilities
- **Creative content** exploring science and technology themes

## 🌟 Highlights

- **Sky-T1 Model**: Train your own O1-preview model for under $450
- **Touch'N'Stars**: Mobile control interface for NINA astronomy software
- **Comprehensive C++20 Guide**: Modern C++ features and best practices
- **Web Crawling Tools**: AI-powered content analysis and summarization
- **Type Erasure Techniques**: Advanced C++ design patterns

---

*This documentation is continuously updated and improved. The MkDocs structure makes it easy to navigate, search, and maintain.*
