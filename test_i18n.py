#!/usr/bin/env python3
"""
测试 mkdocs-static-i18n 配置的脚本
Test script for mkdocs-static-i18n configuration
"""

import os
import yaml
import subprocess
import sys
from pathlib import Path

def test_mkdocs_config():
    """测试 MkDocs 配置文件"""
    print("🔍 测试 MkDocs 配置...")
    
    # 检查配置文件是否存在
    if not os.path.exists("mkdocs.yml"):
        print("❌ 未找到 mkdocs.yml 配置文件")
        return False
    
    try:
        # 加载并验证 YAML 配置
        with open("mkdocs.yml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("✅ mkdocs.yml 配置文件语法正确")
        
        # 检查 i18n 插件配置
        plugins = config.get('plugins', [])
        i18n_config = None
        
        for plugin in plugins:
            if isinstance(plugin, dict) and 'i18n' in plugin:
                i18n_config = plugin['i18n']
                break
        
        if not i18n_config:
            print("❌ 未找到 i18n 插件配置")
            return False
        
        print("✅ 找到 i18n 插件配置")
        
        # 检查语言配置
        languages = i18n_config.get('languages', [])
        if not languages:
            print("❌ 未配置语言")
            return False
        
        default_count = sum(1 for lang in languages if lang.get('default', False))
        if default_count != 1:
            print(f"❌ 必须有且仅有一个默认语言，当前有 {default_count} 个")
            return False
        
        print(f"✅ 配置了 {len(languages)} 种语言")
        for lang in languages:
            locale = lang.get('locale', 'unknown')
            name = lang.get('name', 'unknown')
            is_default = lang.get('default', False)
            default_str = " (默认)" if is_default else ""
            print(f"   - {locale}: {name}{default_str}")
        
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ YAML 配置文件语法错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 配置文件检查失败: {e}")
        return False

def test_file_structure():
    """测试文件结构"""
    print("\n📁 测试文件结构...")
    
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("❌ docs 目录不存在")
        return False
    
    print("✅ docs 目录存在")
    
    # 检查主要的双语文件
    required_files = [
        ("index.md", "index.zh.md"),
        ("programming/index.md", "programming/index.zh.md"),
        ("ai/index.md", "ai/index.zh.md"),
        ("astronomy/index.md", "astronomy/index.zh.md"),
        ("linux/index.md", "linux/index.zh.md"),
        ("libraries/index.md", "libraries/index.zh.md"),
        ("creative/index.md", "creative/index.zh.md"),
    ]
    
    missing_files = []
    for en_file, zh_file in required_files:
        en_path = docs_dir / en_file
        zh_path = docs_dir / zh_file
        
        if en_path.exists() and zh_path.exists():
            print(f"✅ {en_file} ↔ {zh_file}")
        elif en_path.exists():
            print(f"⚠️  {en_file} 存在，但缺少 {zh_file}")
            missing_files.append(zh_file)
        elif zh_path.exists():
            print(f"⚠️  {zh_file} 存在，但缺少 {en_file}")
            missing_files.append(en_file)
        else:
            print(f"❌ 两个文件都不存在: {en_file}, {zh_file}")
            missing_files.extend([en_file, zh_file])
    
    if missing_files:
        print(f"\n⚠️  发现 {len(missing_files)} 个缺失文件")
        return False
    
    print("\n✅ 所有主要双语文件都存在")
    return True

def test_dependencies():
    """测试依赖包"""
    print("\n📦 测试依赖包...")
    
    required_packages = [
        "mkdocs",
        "mkdocs_material",
        "mkdocs_static_i18n",
        "pymdownx"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ 缺少 {len(missing_packages)} 个依赖包")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("\n✅ 所有依赖包都已安装")
    return True

def test_build():
    """测试构建"""
    print("\n🔨 测试构建...")
    
    try:
        # 尝试构建
        result = subprocess.run(
            ["mkdocs", "build", "--clean", "--verbose"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ MkDocs 构建成功")
            
            # 检查构建输出
            site_dir = Path("site")
            if site_dir.exists():
                print("✅ site 目录已创建")
                
                # 检查语言目录
                en_dir = site_dir / "index.html"
                zh_dir = site_dir / "zh"
                
                if en_dir.exists():
                    print("✅ 英文版本已构建")
                else:
                    print("❌ 英文版本构建失败")
                
                if zh_dir.exists() and zh_dir.is_dir():
                    print("✅ 中文版本已构建")
                    zh_index = zh_dir / "index.html"
                    if zh_index.exists():
                        print("✅ 中文主页已生成")
                    else:
                        print("❌ 中文主页生成失败")
                else:
                    print("❌ 中文版本构建失败")
                
                return True
            else:
                print("❌ site 目录未创建")
                return False
        else:
            print("❌ MkDocs 构建失败")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 构建超时")
        return False
    except FileNotFoundError:
        print("❌ 未找到 mkdocs 命令，请确保已安装 MkDocs")
        return False
    except Exception as e:
        print(f"❌ 构建测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试 mkdocs-static-i18n 配置...")
    print("=" * 50)
    
    tests = [
        ("配置文件", test_mkdocs_config),
        ("文件结构", test_file_structure),
        ("依赖包", test_dependencies),
        ("构建测试", test_build),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(tests)} 项测试通过")
    
    if passed == len(tests):
        print("\n🎉 所有测试通过！双语文档系统配置正确。")
        print("运行 'mkdocs serve' 启动开发服务器。")
        return True
    else:
        print(f"\n⚠️  有 {len(tests) - passed} 项测试失败，请检查配置。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
