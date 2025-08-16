@echo off
echo 🚀 设置双语文档系统...
echo Setting up bilingual documentation system...
echo.

echo 📦 安装依赖包...
echo Installing dependencies...
pip install mkdocs-static-i18n mkdocs-material mkdocs pymdown-extensions

echo.
echo ✅ 依赖安装完成！
echo Dependencies installed successfully!
echo.

echo 🔍 验证安装...
echo Verifying installation...
python -c "import mkdocs_static_i18n; print('✅ mkdocs-static-i18n 安装成功')" 2>nul || echo "❌ mkdocs-static-i18n 安装失败"
python -c "import mkdocs; print('✅ mkdocs 安装成功')" 2>nul || echo "❌ mkdocs 安装失败"

echo.
echo 🧪 运行配置测试...
echo Running configuration tests...
python test_i18n.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 🌐 启动开发服务器...
    echo Starting development server...
    echo 访问 http://127.0.0.1:8000 查看网站
    echo Visit http://127.0.0.1:8000 to view the site
    echo 使用右上角的语言切换器切换中英文
    echo Use the language switcher in the top-right corner to switch languages
    echo.
    mkdocs serve
) else (
    echo.
    echo ❌ 配置测试失败，请检查上述错误信息
    echo Configuration tests failed, please check the error messages above
    pause
)
