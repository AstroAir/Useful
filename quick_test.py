#!/usr/bin/env python3
"""
快速测试 mkdocs-static-i18n 配置
Quick test for mkdocs-static-i18n configuration
"""

import os
import sys

def quick_test():
    """快速测试"""
    print("🚀 快速测试 mkdocs-static-i18n 配置...")
    
    # 检查关键文件
    files_to_check = [
        "mkdocs.yml",
        "docs/index.md",
        "docs/index.zh.md",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ 缺少 {len(missing_files)} 个关键文件")
        return False
    
    # 检查依赖
    try:
        import mkdocs_static_i18n
        print("✅ mkdocs-static-i18n 已安装")
    except ImportError:
        print("❌ mkdocs-static-i18n 未安装")
        print("请运行: pip install mkdocs-static-i18n")
        return False
    
    try:
        import mkdocs
        print("✅ mkdocs 已安装")
    except ImportError:
        print("❌ mkdocs 未安装")
        return False
    
    print("\n✅ 基本配置检查通过！")
    print("运行 'mkdocs serve' 启动开发服务器")
    print("或运行 'python test_i18n.py' 进行完整测试")
    return True

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
