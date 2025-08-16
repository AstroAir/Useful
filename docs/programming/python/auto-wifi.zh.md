# 自动 WiFi 管理工具

这个 Python 工具使用 Selenium WebDriver 提供自动化的 WiFi 连接管理。它专为自动连接到特定网络门户而设计，特别适用于需要基于 Web 身份验证的机构或公共 WiFi 网络。

[English](auto-wifi.md) | **中文**

## 概述

自动 WiFi 工具自动化了连接到需要 Web 门户身份验证的 WiFi 网络的过程。它使用 Selenium WebDriver 与基于 Web 的登录页面交互，非常适合：

- **校园网络** - 大学和学校的 WiFi 系统
- **公共 WiFi** - 酒店、机场和公共场所
- **企业网络** - 公司访客网络
- **ISP 门户** - 互联网服务提供商身份验证页面

## 功能特性

### 自动化 Web 身份验证

- **浏览器自动化** - 使用 Microsoft Edge WebDriver 进行可靠的 Web 交互
- **表单处理** - 自动填写和提交登录表单
- **下拉选择** - 处理复杂的表单元素，如运营商选择
- **等待条件** - 智能等待页面元素加载

### 配置选项

- **可自定义 URL** - 支持不同的门户地址
- **运营商选择** - 自动选择网络运营商
- **超时管理** - 可配置的页面加载等待时间
- **错误处理** - 优雅处理连接失败

## 安装

### 先决条件

```bash
pip install selenium
```

### WebDriver 设置

1. 从 Microsoft 官方网站下载 Microsoft Edge WebDriver
2. 将驱动程序解压到已知位置（例如，`D:\webdriver\msedgedriver.exe`）
3. 在脚本中更新驱动程序路径

### 替代 WebDriver

该工具可以适配其他浏览器：

- **Chrome** - 使用 ChromeDriver 和 `webdriver.Chrome()`
- **Firefox** - 使用 GeckoDriver 和 `webdriver.Firefox()`
- **Safari** - 使用 Safari WebDriver（仅限 macOS）

## 使用方法

### 基本用法

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# 配置 WebDriver
driver_path = "D:\\webdriver\\msedgedriver.exe"
driver = webdriver.Edge(executable_path=driver_path)

try:
    # 打开 WiFi 门户页面
    driver.get("http://192.168.1.1/login")
    
    # 等待页面加载
    wait = WebDriverWait(driver, 10)
    
    # 选择运营商（如果需要）
    operator_dropdown = wait.until(
        EC.presence_of_element_located((By.ID, "operator"))
    )
    select = Select(operator_dropdown)
    select.select_by_visible_text("中国移动")
    
    # 点击连接按钮
    connect_button = wait.until(
        EC.element_to_be_clickable((By.ID, "connect"))
    )
    connect_button.click()
    
    print("WiFi 连接成功！")
    
except Exception as e:
    print(f"连接失败：{e}")
    
finally:
    driver.quit()
```

### 高级配置

```python
import time
from selenium.webdriver.edge.options import Options

class WiFiAutoConnector:
    def __init__(self, driver_path, portal_url, operator="中国移动"):
        self.driver_path = driver_path
        self.portal_url = portal_url
        self.operator = operator
        self.driver = None
    
    def setup_driver(self):
        """设置 WebDriver 选项"""
        options = Options()
        options.add_argument("--headless")  # 无头模式
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Edge(
            executable_path=self.driver_path,
            options=options
        )
    
    def connect_wifi(self):
        """执行 WiFi 连接"""
        try:
            self.setup_driver()
            self.driver.get(self.portal_url)
            
            wait = WebDriverWait(self.driver, 15)
            
            # 检查是否已经连接
            if self.check_connection_status():
                print("已经连接到 WiFi")
                return True
            
            # 选择运营商
            if self.select_operator():
                # 点击连接
                if self.click_connect():
                    # 验证连接
                    return self.verify_connection()
            
            return False
            
        except Exception as e:
            print(f"连接过程中出错：{e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def check_connection_status(self):
        """检查当前连接状态"""
        try:
            status_element = self.driver.find_element(By.CLASS_NAME, "status")
            return "已连接" in status_element.text
        except:
            return False
    
    def select_operator(self):
        """选择网络运营商"""
        try:
            wait = WebDriverWait(self.driver, 10)
            dropdown = wait.until(
                EC.presence_of_element_located((By.ID, "operator"))
            )
            select = Select(dropdown)
            select.select_by_visible_text(self.operator)
            time.sleep(1)  # 等待选择生效
            return True
        except Exception as e:
            print(f"选择运营商失败：{e}")
            return False
    
    def click_connect(self):
        """点击连接按钮"""
        try:
            wait = WebDriverWait(self.driver, 10)
            connect_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "connect"))
            )
            connect_btn.click()
            return True
        except Exception as e:
            print(f"点击连接按钮失败：{e}")
            return False
    
    def verify_connection(self):
        """验证连接是否成功"""
        try:
            # 等待连接完成
            time.sleep(5)
            
            # 检查成功页面或状态
            wait = WebDriverWait(self.driver, 20)
            success_indicator = wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "success")),
                    EC.presence_of_element_located((By.ID, "connected")),
                    EC.url_contains("success")
                )
            )
            
            print("WiFi 连接验证成功！")
            return True
            
        except Exception as e:
            print(f"连接验证失败：{e}")
            return False

# 使用示例
if __name__ == "__main__":
    connector = WiFiAutoConnector(
        driver_path="D:\\webdriver\\msedgedriver.exe",
        portal_url="http://192.168.1.1/login",
        operator="中国移动"
    )
    
    if connector.connect_wifi():
        print("WiFi 自动连接成功！")
    else:
        print("WiFi 自动连接失败！")
```

## 配置文件支持

### JSON 配置

```python
import json

class ConfigManager:
    def __init__(self, config_file="wifi_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置"""
        default_config = {
            "driver_path": "D:\\webdriver\\msedgedriver.exe",
            "portal_url": "http://192.168.1.1/login",
            "operator": "中国移动",
            "timeout": 15,
            "retry_attempts": 3,
            "headless": True
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        return default_config
    
    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)

# 配置文件示例 (wifi_config.json)
{
  "driver_path": "D:\\webdriver\\msedgedriver.exe",
  "portal_url": "http://192.168.1.1/login",
  "operator": "中国移动",
  "timeout": 15,
  "retry_attempts": 3,
  "headless": true,
  "custom_selectors": {
    "operator_dropdown": "#operator",
    "connect_button": "#connect",
    "status_indicator": ".status"
  }
}
```

## 故障排除

### 常见问题

#### WebDriver 问题

- **驱动程序版本不匹配**：确保 WebDriver 版本与浏览器版本兼容
- **路径错误**：检查驱动程序路径是否正确
- **权限问题**：确保驱动程序具有执行权限

#### 网络问题

- **门户 URL 错误**：验证 WiFi 门户的正确 URL
- **网络超时**：增加等待时间或检查网络连接
- **页面元素变化**：更新选择器以匹配新的页面结构

#### 身份验证问题

- **运营商选择失败**：检查运营商名称是否正确
- **表单提交失败**：验证表单字段和提交按钮

### 调试技巧

```python
import logging

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wifi_auto.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class DebugWiFiConnector(WiFiAutoConnector):
    def connect_wifi(self):
        """带调试信息的连接方法"""
        logger.info("开始 WiFi 自动连接")
        
        try:
            self.setup_driver()
            logger.info(f"访问门户：{self.portal_url}")
            self.driver.get(self.portal_url)
            
            # 保存页面截图用于调试
            self.driver.save_screenshot("portal_page.png")
            logger.info("已保存页面截图：portal_page.png")
            
            # 继续连接流程...
            return super().connect_wifi()
            
        except Exception as e:
            logger.error(f"连接失败：{e}")
            # 保存错误时的截图
            if self.driver:
                self.driver.save_screenshot("error_page.png")
            return False
```

## 最佳实践

### 安全考虑

- 不要在代码中硬编码敏感信息
- 使用环境变量或配置文件存储凭据
- 定期更新 WebDriver 版本

### 性能优化

- 使用无头模式减少资源消耗
- 设置合理的超时时间
- 实现连接状态缓存

### 可维护性

- 使用配置文件管理设置
- 实现详细的日志记录
- 编写单元测试验证功能

这个自动 WiFi 管理工具为需要频繁连接到 Web 门户认证网络的用户提供了便利的自动化解决方案。

---

**语言版本：**

- [English](auto-wifi.md) - 英文版本
- **中文** - 当前页面
