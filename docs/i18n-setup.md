# 双语文档系统设置指南

本指南将帮助您设置和使用 `mkdocs-static-i18n` 插件来实现专业的多语言文档网站。

## 概述

我们使用 `mkdocs-static-i18n` 插件来实现：

- 自动语言切换器
- 独立的语言版本构建
- 智能的导航翻译
- SEO 友好的多语言 URL

## 安装步骤

### 1. 安装依赖

```bash
# 安装所有必需的包
pip install -r requirements.txt

# 或者手动安装
pip install mkdocs-static-i18n mkdocs-material mkdocs
```

### 2. 验证安装

```bash
# 检查 MkDocs 版本
mkdocs --version

# 检查插件是否可用
python -c "import mkdocs_static_i18n; print('✅ mkdocs-static-i18n 安装成功')"
```

## 配置说明

### MkDocs 配置 (mkdocs.yml)

根据官方最佳实践，我们的配置如下：

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
          site_name: "Useful - 技术文档集合"
          site_description: "涵盖编程、人工智能、天文学等多个领域的综合技术文档集合"
          nav_translations:
            Home: 主页
            Programming: 编程
            Artificial Intelligence: 人工智能
            Astronomy: 天文学
            Linux: Linux
            Libraries: 库
            Creative Writing: 创意写作
            Overview: 概述
            "C Programming": "C 编程"
            "C++ Programming": "C++ 编程"
            "C# Programming": "C# 编程"
            JavaScript: JavaScript
            Python: Python
            Tools: 工具
            NINA: NINA
  - search
```

### 配置参数说明

#### 核心配置

- `docs_structure: suffix` - 使用后缀结构（如 `index.zh.md`）
- `fallback_to_default: true` - 如果翻译不存在，回退到默认语言
- `reconfigure_material: true` - 自动配置 Material 主题的语言切换器
- `reconfigure_search: true` - 自动配置搜索功能支持多语言

#### 语言特定配置

- `locale` - 语言代码（ISO 639-1 标准，如 `en`、`zh`）
- `default: true` - 指定默认语言（必须有且仅有一个）
- `name` - 语言显示名称（在切换器中显示）
- `build: true` - 是否构建该语言版本
- `site_name` - 该语言版本的网站名称
- `site_description` - 该语言版本的网站描述
- `nav_translations` - 导航项的翻译映射

#### 高级选项

- `link` - 自定义语言切换器链接（默认：`/<locale>/`）
- `fixed_link` - 固定链接（用于外部链接）
- `theme` - 每种语言的主题覆盖（如颜色、字体等）

## 文件结构

### 推荐的文件命名

```
docs/
├── index.md              # 英文主页
├── index.zh.md           # 中文主页
├── programming/
│   ├── index.md          # 英文编程索引
│   ├── index.zh.md       # 中文编程索引
│   ├── c/
│   │   ├── index.md      # 英文 C 编程
│   │   └── index.zh.md   # 中文 C 编程
│   └── ...
└── ...
```

### 文件命名规则

- 英文文件：`filename.md`
- 中文文件：`filename.zh.md`
- 保持相同的目录结构
- 确保文件名一致（除了语言后缀）

## 使用方法

### 1. 启动开发服务器

```bash
mkdocs serve
```

### 2. 访问网站

- 打开浏览器访问：<http://127.0.0.1:8000>
- 使用右上角的语言切换器切换语言
- 测试不同页面的语言切换功能

### 3. 构建生产版本

```bash
mkdocs build
```

构建后的文件结构：

```
site/
├── en/                   # 英文版本
│   ├── index.html
│   └── ...
├── zh/                   # 中文版本
│   ├── index.html
│   └── ...
└── index.html           # 重定向到默认语言
```

## 高级功能

### 1. 自定义语言切换器

在主题配置中添加：

```yaml
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
  custom_dir: overrides/  # 自定义模板目录
```

### 2. 语言特定的配置

```yaml
plugins:
  - i18n:
      languages:
        - locale: en
          default: true
          name: English
          build: true
          site_name: "Technical Documentation"
        - locale: zh
          name: 中文
          build: true
          site_name: "技术文档集合"
```

### 3. 条件内容

在 Markdown 文件中使用：

```markdown
<!-- 仅在英文版本显示 -->
{% if config.theme.language == 'en' %}
This content is only shown in English.
{% endif %}

<!-- 仅在中文版本显示 -->
{% if config.theme.language == 'zh' %}
此内容仅在中文版本中显示。
{% endif %}
```

## 故障排除

### 常见问题

#### 1. 语言切换器不显示

**问题**：页面上没有语言切换器
**解决方案**：

- 确保 `reconfigure_material: true`
- 检查是否有对应的翻译文件
- 验证文件命名是否正确

#### 2. 搜索功能异常

**问题**：搜索无法找到中文内容
**解决方案**：

- 确保 `reconfigure_search: true`
- 检查搜索插件配置
- 重新构建网站

#### 3. 导航翻译不生效

**问题**：导航项没有翻译
**解决方案**：

- 检查 `nav_translations` 配置
- 确保键名与导航项完全匹配
- 注意大小写和空格

### 调试技巧

#### 1. 启用详细日志

```bash
mkdocs serve --verbose
```

#### 2. 检查构建输出

```bash
mkdocs build --verbose --clean
```

#### 3. 验证文件结构

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

### 2. SEO 优化

- 为每种语言设置正确的 `lang` 属性
- 使用 `hreflang` 标签（插件自动处理）
- 确保 URL 结构清晰

### 3. 性能优化

- 启用缓存
- 压缩静态资源
- 使用 CDN 分发

### 4. 维护策略

- 建立翻译工作流程
- 定期更新过时的翻译
- 监控用户反馈

## 部署

### GitHub Pages

```yaml
# .github/workflows/ci.yml
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
      - run: echo "cache_id=$(date --utc '+%V')" >> $GITHUB_ENV
      - uses: actions/cache@v3
        with:
          key: mkdocs-material-${{ env.cache_id }}
          path: .cache
          restore-keys: |
            mkdocs-material-
      - run: pip install -r requirements.txt
      - run: mkdocs gh-deploy --force
```

### 自定义域名

在 `docs/` 目录下创建 `CNAME` 文件：

```
your-domain.com
```

通过这个设置，您将拥有一个专业的双语文档网站，支持自动语言切换和优化的用户体验。
