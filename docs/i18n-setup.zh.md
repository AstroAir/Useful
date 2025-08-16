# 双语文档系统设置指南

本指南将帮助您设置和使用 `mkdocs-static-i18n` 插件来实现专业的多语言文档网站。

[English](i18n-setup.md) | **中文**

## 概述

我们使用 `mkdocs-static-i18n` 插件来实现：

- 🔄 自动语言切换器
- 📁 独立的语言版本构建
- 🔍 智能的导航翻译
- 🌍 SEO 友好的多语言 URL

## 快速开始

### Windows 用户

1. 双击运行 `setup_i18n.bat` 脚本
2. 等待依赖安装完成
3. 浏览器会自动打开 <http://127.0.0.1:8000>
4. 使用右上角的语言切换器测试功能

### Linux/Mac 用户

```bash
# 运行安装脚本
./setup_i18n.sh

# 或者手动安装
pip install mkdocs-static-i18n mkdocs-material mkdocs
mkdocs serve
```

## 手动安装步骤

### 1. 安装依赖

```bash
# 安装所有必需的包
pip install -r requirements.txt

# 或者单独安装
pip install mkdocs-static-i18n mkdocs-material mkdocs pymdown-extensions
```

### 2. 验证安装

```bash
# 检查 MkDocs 版本
mkdocs --version

# 检查插件是否可用
python -c "import mkdocs_static_i18n; print('✅ mkdocs-static-i18n 安装成功')"
```

### 3. 启动服务器

```bash
mkdocs serve
```

访问 <http://127.0.0.1:8000> 查看网站，使用右上角的语言切换器切换中英文。

## 配置说明

### MkDocs 配置 (mkdocs.yml)

```yaml
plugins:
  - i18n:
      docs_structure: suffix
      fallback_to_default: true
      reconfigure_material: true
      reconfigure_search: true
      languages:
        - locale: en
          default: true
          name: English
          build: true
        - locale: zh
          name: 中文
          build: true
          nav_translations:
            Home: 主页
            Programming: 编程
            Artificial Intelligence: 人工智能
            Astronomy: 天文学
            Linux: Linux
            Libraries: 库
            Creative Writing: 创意写作
  - search
```

### 配置参数说明

- `docs_structure: suffix` - 使用后缀结构（如 `index.zh.md`）
- `fallback_to_default: true` - 如果翻译不存在，回退到默认语言
- `reconfigure_material: true` - 自动配置 Material 主题
- `reconfigure_search: true` - 自动配置搜索功能
- `nav_translations` - 导航项的翻译映射

## 文件结构

### 当前的文件命名

```
docs/
├── index.md              # 英文主页
├── index.zh.md           # 中文主页
├── programming/
│   ├── index.md          # 英文编程索引
│   ├── index.zh.md       # 中文编程索引
│   ├── c/
│   │   ├── index.zh.md   # 中文 C 编程
│   │   └── day7-structures-unions.zh.md
│   ├── cpp/
│   │   ├── index.zh.md   # 中文 C++ 编程
│   │   └── cpp20.zh.md   # C++20 指南
│   ├── csharp/
│   │   └── index.zh.md   # 中文 C# 编程
│   ├── javascript/
│   │   └── index.zh.md   # 中文 JavaScript 编程
│   └── python/
│       ├── index.zh.md   # 中文 Python 编程
│       └── auto-wifi.zh.md
├── ai/
│   ├── index.zh.md       # 中文 AI 索引
│   ├── sky-t1.zh.md      # Sky-T1 模型文档
│   └── tools/
│       ├── compress.zh.md
│       └── convert.zh.md
├── astronomy/
│   ├── index.zh.md       # 中文天文学索引
│   └── nina/
│       └── touch-n-star.zh.md
├── linux/
│   └── index.zh.md       # 中文 Linux 索引
├── libraries/
│   └── index.zh.md       # 中文库索引
└── creative/
    └── index.zh.md       # 中文创意写作索引
```

### 文件命名规则

- 英文文件：`filename.md`
- 中文文件：`filename.zh.md`
- 保持相同的目录结构
- 确保文件名一致（除了语言后缀）

## 功能特性

### 1. 自动语言切换

- 右上角显示语言切换器
- 自动检测用户语言偏好
- 保持用户的语言选择

### 2. 独立语言版本

构建后的文件结构：

```
site/
├── en/                   # 英文版本
│   ├── index.html
│   ├── programming/
│   └── ...
├── zh/                   # 中文版本
│   ├── index.html
│   ├── programming/
│   └── ...
└── index.html           # 重定向到默认语言
```

### 3. 多语言搜索

- 英文内容搜索英文结果
- 中文内容搜索中文结果
- 智能语言检测

### 4. SEO 优化

- 自动生成 `hreflang` 标签
- 语言特定的 URL 结构
- 正确的 `lang` 属性设置

## 故障排除

### 常见问题

#### 1. 语言切换器不显示

**症状**：页面上没有语言切换器
**解决方案**：

- 确保 `reconfigure_material: true`
- 检查是否有对应的翻译文件
- 验证文件命名是否正确（必须是 `.zh.md` 后缀）

#### 2. 搜索功能异常

**症状**：搜索无法找到中文内容
**解决方案**：

- 确保 `reconfigure_search: true`
- 重新构建网站：`mkdocs build --clean`
- 检查搜索插件配置

#### 3. 导航翻译不生效

**症状**：导航项没有翻译
**解决方案**：

- 检查 `nav_translations` 配置
- 确保键名与导航项完全匹配
- 注意大小写和空格

#### 4. 构建错误

**症状**：`mkdocs build` 失败
**解决方案**：

```bash
# 清理并重新构建
mkdocs build --clean --verbose

# 检查配置文件语法
python -c "import yaml; yaml.safe_load(open('mkdocs.yml'))"
```

### 调试技巧

#### 1. 启用详细日志

```bash
mkdocs serve --verbose
```

#### 2. 检查文件结构

```python
import os

def check_i18n_files(docs_dir="docs"):
    """检查国际化文件结构"""
    for root, dirs, files in os.walk(docs_dir):
        md_files = [f for f in files if f.endswith('.md')]
        
        for file in md_files:
            if not file.endswith('.zh.md'):
                # 检查是否有对应的中文文件
                zh_file = file.replace('.md', '.zh.md')
                zh_path = os.path.join(root, zh_file)
                
                if os.path.exists(zh_path):
                    print(f"✅ {file} -> {zh_file}")
                else:
                    print(f"❌ 缺少中文翻译: {zh_file}")

check_i18n_files()
```

## 最佳实践

### 1. 内容同步

- 保持英文和中文版本的结构一致
- 定期检查翻译的完整性
- 使用版本控制跟踪变更

### 2. 翻译质量

- 保持技术术语的准确性
- 适应中文的表达习惯
- 保留代码示例的完整性

### 3. 维护策略

- 建立翻译工作流程
- 定期更新过时的翻译
- 监控用户反馈

### 4. 性能优化

- 启用缓存
- 压缩静态资源
- 使用 CDN 分发

## 部署

### GitHub Pages

创建 `.github/workflows/ci.yml`：

```yaml
name: ci
on:
  push:
    branches:
      - master
      - main
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: 3.x
      - run: pip install -r requirements.txt
      - run: mkdocs gh-deploy --force
```

### 自定义域名

在 `docs/` 目录下创建 `CNAME` 文件：

```
your-domain.com
```

## 总结

通过 `mkdocs-static-i18n` 插件，我们成功实现了：

- ✅ 专业的双语文档系统
- ✅ 自动语言切换功能
- ✅ 独立的语言版本构建
- ✅ 多语言搜索支持
- ✅ SEO 优化的多语言 URL

这个系统为中文技术社区提供了高质量、全面的技术文档资源，支持持续扩展和维护。

---

**语言版本：**

- [English](i18n-setup.md) - 英文版本
- **中文** - 当前页面
