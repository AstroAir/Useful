# Auto WiFi Management Tool

This Python tool provides automated WiFi connection management using Selenium WebDriver. It's designed to automatically connect to specific network portals, particularly useful for institutional or public WiFi networks that require web-based authentication.

## Overview

The Auto WiFi tool automates the process of connecting to WiFi networks that require web portal authentication. It uses Selenium WebDriver to interact with web-based login pages, making it ideal for:

- **Campus Networks** - University and school WiFi systems
- **Public WiFi** - Hotels, airports, and public spaces
- **Corporate Networks** - Company guest networks
- **ISP Portals** - Internet service provider authentication pages

## Features

### Automated Web Authentication

- **Browser Automation** - Uses Microsoft Edge WebDriver for reliable web interaction
- **Form Handling** - Automatically fills and submits login forms
- **Dropdown Selection** - Handles complex form elements like operator selection
- **Wait Conditions** - Intelligent waiting for page elements to load

### Configuration Options

- **Customizable URLs** - Support for different portal addresses
- **Operator Selection** - Automatic selection of network operators
- **Timeout Management** - Configurable wait times for page loading
- **Error Handling** - Graceful handling of connection failures

## Installation

### Prerequisites

```bash
pip install selenium
```

### WebDriver Setup

1. Download Microsoft Edge WebDriver from the official Microsoft website
2. Extract the driver to a known location (e.g., `D:\webdriver\msedgedriver.exe`)
3. Update the driver path in the script

### Alternative WebDrivers

The tool can be adapted for other browsers:

- **Chrome** - Use ChromeDriver with `webdriver.Chrome()`
- **Firefox** - Use GeckoDriver with `webdriver.Firefox()`
- **Safari** - Use Safari WebDriver (macOS only)

## Usage

### Basic Usage

```python
from selenium import webdriver
from selenium.webdriver.edge.service import Service

# Configure WebDriver
service = Service('path/to/msedgedriver.exe')
driver = webdriver.Edge(service=service)

# Navigate to portal
driver.get("http://portal.example.com")

# Perform authentication steps
# ... (form filling and submission)

# Clean up
driver.quit()
```

### Current Implementation

The tool is configured for a specific network portal:

```python
# Target portal URL
portal_url = "http://10.10.244.11/a79.htm"

# Operator selection
select.select_by_visible_text("中国电信")  # China Telecom

# Login button interaction
login_button.click()
```

## Configuration

### Network Settings

- **Portal URL** - The web address of the authentication portal
- **Operator Selection** - Network provider or service type
- **Credentials** - Username and password (if required)
- **Timeout Values** - Wait times for page loading

### WebDriver Configuration

```python
# Service configuration
service = Service('D:\webdriver\msedgedriver.exe')

# Driver options (optional)
options = webdriver.EdgeOptions()
options.add_argument('--headless')  # Run without GUI
options.add_argument('--no-sandbox')  # Linux compatibility

driver = webdriver.Edge(service=service, options=options)
```

## Advanced Features

### Error Handling

```python
try:
    # Authentication logic
    driver.get(portal_url)
    # ... form interactions
except TimeoutException:
    print("Page loading timeout")
except NoSuchElementException:
    print("Required element not found")
finally:
    driver.quit()
```

### Headless Operation

```python
options = webdriver.EdgeOptions()
options.add_argument('--headless')
driver = webdriver.Edge(service=service, options=options)
```

### Multiple Portal Support

```python
portals = [
    {"url": "http://portal1.com", "operator": "Provider1"},
    {"url": "http://portal2.com", "operator": "Provider2"}
]

for portal in portals:
    try:
        connect_to_portal(portal)
        break  # Stop on successful connection
    except Exception as e:
        print(f"Failed to connect to {portal['url']}: {e}")
```

## Customization

### Adapting for Different Portals

1. **Identify Form Elements** - Use browser developer tools to find form field names
2. **Update Selectors** - Modify the element selection logic
3. **Adjust Wait Conditions** - Configure appropriate timeouts
4. **Handle Different Flows** - Adapt to specific authentication sequences

### Adding Credential Management

```python
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('WIFI_USERNAME')
password = os.getenv('WIFI_PASSWORD')

# Use credentials in form filling
username_field.send_keys(username)
password_field.send_keys(password)
```

### Logging and Monitoring

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting WiFi authentication")
logger.info(f"Connecting to portal: {portal_url}")
logger.info("Authentication successful")
```

## Best Practices

### Security Considerations

- **Credential Protection** - Store sensitive information securely
- **HTTPS Verification** - Ensure secure connections when possible
- **Network Validation** - Verify portal authenticity
- **Access Control** - Limit script access and permissions

### Performance Optimization

- **Headless Mode** - Run without GUI for better performance
- **Element Caching** - Store frequently used element references
- **Timeout Tuning** - Optimize wait times for your network
- **Resource Cleanup** - Always close browser instances

### Reliability Improvements

- **Retry Logic** - Implement automatic retry on failures
- **Health Checks** - Verify connection status after authentication
- **Fallback Options** - Support multiple authentication methods
- **Status Monitoring** - Track connection success rates

## Troubleshooting

### Common Issues

- **WebDriver Path** - Ensure correct driver location and permissions
- **Element Not Found** - Verify form element selectors
- **Timeout Errors** - Increase wait times for slow networks
- **Portal Changes** - Update selectors when portals are modified

### Debugging Tips

- **Screenshot Capture** - Take screenshots for debugging
- **Element Inspection** - Use browser tools to verify selectors
- **Verbose Logging** - Enable detailed logging for troubleshooting
- **Manual Testing** - Test portal interaction manually first

This tool provides a foundation for automated WiFi authentication that can be customized for various network environments and authentication systems.
