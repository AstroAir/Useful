# Useful - Technical Documentation Collection

A comprehensive collection of useful documents, tools, and guides across programming, AI, astronomy, and more. This repository has been organized and restructured to support MkDocs static site generation for better navigation and accessibility.

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

3. **Build Static Site**
   ```bash
   mkdocs build
   ```
   The built site will be in the `site/` directory.

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
