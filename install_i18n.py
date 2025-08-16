#!/usr/bin/env python3
"""
安装 mkdocs-static-i18n 插件的脚本
"""

import subprocess
import sys
import os

def run_command(command):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 成功: {command}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ 失败: {command}")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def main():
    print("🚀 开始安装 mkdocs-static-i18n 插件...")
    
    # 检查 Python 版本
    print(f"Python 版本: {sys.version}")
    
    # 安装 mkdocs-static-i18n
    commands = [
        "pip install mkdocs-static-i18n",
        "pip install mkdocs-material",  # 确保 Material 主题已安装
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print(f"❌ 安装失败: {cmd}")
            return False
    
    print("\n✅ 所有依赖安装完成！")
    
    # 验证安装
    print("\n🔍 验证安装...")
    if run_command("mkdocs --version"):
        print("✅ MkDocs 安装正常")
    
    # 检查配置文件
    if os.path.exists("mkdocs.yml"):
        print("✅ 找到 mkdocs.yml 配置文件")
    else:
        print("❌ 未找到 mkdocs.yml 配置文件")
    
    print("\n📚 下一步:")
    print("1. 运行 'mkdocs serve' 启动开发服务器")
    print("2. 访问 http://127.0.0.1:8000 查看网站")
    print("3. 使用右上角的语言切换器切换中英文")
    
    return True

if __name__ == "__main__":
    main()
