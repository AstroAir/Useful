from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# 设置WebDriver路径
service = Service('D:\webdriver\msedgedriver.exe')  # 替换为你的chromedriver路径
driver = webdriver.Edge(service=service)

try:
    # 打开指定的URL
    driver.get("http://10.10.244.11/a79.htm")

    # 等待页面加载完成，并找到标签为“请选择运营商”的选择框
    operator_select = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "operator"))  # 假设选择框的name属性为"operator"
    )

    # 创建Select对象并选择“中国电信”
    select = Select(operator_select)
    select.select_by_visible_text("中国电信")

    # 等待页面加载完成，并找到标签为“登录”的按钮
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "登录"))
    )

    # 点击登录按钮
    login_button.click()

finally:
    # 关闭浏览器
    driver.quit()