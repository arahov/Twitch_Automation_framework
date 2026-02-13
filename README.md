# Twitch Automation Framework

A robust, scalable Selenium automation framework built with Python and Pytest for testing Twitch mobile web application.

## 🏗️ Framework Architecture

This framework follows industry best practices and design patterns:

- **Page Object Model (POM)**: Separates page structure from test logic
- **Factory Pattern**: For WebDriver initialization
- **Configuration Management**: Centralized configuration via environment variables
- **Fixture-based Setup**: Pytest fixtures for test data and driver management
- **Layered Architecture**: Clear separation of concerns

```
twitch_automation_framework/
├── config/                 # Configuration management
│   ├── __init__.py
│   └── config.py          # Centralized configuration
├── pages/                 # Page Object Models
│   ├── __init__.py
│   ├── base_page.py       # Base page with common methods
│   ├── home_page.py       # Twitch home page
│   ├── search_results_page.py
│   └── streamer_page.py   # Individual streamer page
├── tests/                 # Test cases
│   ├── __init__.py
│   └── test_twitch_search.py
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── logger.py          # Custom logger
│   └── webdriver_factory.py
├── fixtures/              # Pytest fixtures
│   └── conftest.py
├── reports/               # Test reports (generated)
├── screenshots/           # Screenshots (generated)
├── logs/                  # Log files (generated)
├── .env                   # Environment configuration
├── .env.example          # Example environment file
├── pytest.ini            # Pytest configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Features

### Framework Capabilities

1. **Mobile Emulation**: Uses Chrome DevTools Protocol for realistic mobile testing
2. **Robust Element Handling**: 
   - Explicit waits with custom timeouts
   - Retry mechanisms for flaky elements
   - Multiple locator strategies with fallbacks
   - Stale element reference handling
3. **Modal/Popup Management**: Automatic detection and handling of:
   - Mature content warnings
   - Cookie consent banners
   - Generic modal dialogs
4. **Smart Waiting Strategies**:
   - Page load detection
   - Dynamic content loading
   - Video player initialization
5. **Comprehensive Logging**: Multi-level logging with Loguru
6. **Screenshot Capture**: Automatic screenshots on failure
7. **Configurable Test Execution**: Via environment variables
8. **Parallel Execution**: Support for pytest-xdist
9. **Test Retry**: Automatic retry for flaky tests
10. **HTML Reports**: Detailed test execution reports

### Anti-Flakiness Measures

1. **Explicit Waits**: All element interactions use explicit waits
2. **Retry Mechanisms**: Click operations retry up to 3 times
3. **Multiple Locators**: Primary and fallback locators for critical elements
4. **Exception Handling**: Graceful degradation with proper error logging
5. **Dynamic Wait Times**: Configurable wait times for different scenarios
6. **JavaScript Fallbacks**: JavaScript click as fallback for standard clicks
7. **Page Load Verification**: Multiple verification points for page readiness

## 📋 Requirements

- Python 3.8+
- Google Chrome browser
- Internet connection

## 🛠️ Installation

### 1. Clone or Download the Framework

```bash
cd twitch_automation_framework
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file if needed (optional)
# Default configuration works out of the box
```

## 🎯 Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test

```bash
# Run by test name
pytest tests/test_twitch_search.py::TestTwitchSearch::test_search_and_navigate_to_streamer

# Run by marker
pytest -m smoke
pytest -m critical
pytest -m mobile
```

### Run with Different Configurations

```bash
# Run in headless mode
HEADLESS=true pytest

# Run with different device
DEVICE_NAME="iPhone 12" pytest

# Run with custom timeout
EXPLICIT_WAIT=30 pytest

# Disable mobile emulation (run as desktop)
MOBILE_EMULATION=false pytest
```

### Run Tests in Parallel

```bash
# Run with 2 workers
pytest -n 2

# Run with auto-detect workers
pytest -n auto
```

### Generate HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
```

## 📊 Test Reports

After test execution, reports are generated in:

- **HTML Report**: `reports/report.html` (detailed execution report)
- **Screenshots**: `screenshots/` (failure screenshots and final captures)
- **Logs**: `logs/framework.log` (detailed execution logs)
- **Error Logs**: `logs/errors.log` (errors only)

## 🔧 Configuration Options

All configuration is managed through environment variables in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | dev | Environment name |
| `BROWSER` | chrome | Browser to use |
| `HEADLESS` | false | Run in headless mode |
| `MOBILE_EMULATION` | true | Enable mobile emulation |
| `DEVICE_NAME` | Pixel 5 | Device to emulate |
| `IMPLICIT_WAIT` | 10 | Implicit wait in seconds |
| `EXPLICIT_WAIT` | 20 | Explicit wait in seconds |
| `PAGE_LOAD_TIMEOUT` | 30 | Page load timeout |
| `BASE_URL` | https://m.twitch.tv/ | Application URL |
| `SCREENSHOT_ON_FAILURE` | true | Capture screenshots on failure |
| `LOG_LEVEL` | INFO | Logging level |
| `MAX_RETRIES` | 3 | Max retries for operations |

### Supported Mobile Devices

- Pixel 5 (default)
- iPhone 12
- iPhone 14 Pro Max
- Samsung Galaxy S21

To change device:
```bash
DEVICE_NAME="iPhone 12" pytest
```

## 🧪 Test Cases

### Test Case 1: Basic Search Flow
**File**: `test_twitch_search.py::test_search_and_navigate_to_streamer`

Steps:
1. Navigate to https://m.twitch.tv/
2. Click search icon
3. Input "StarCraft II"
4. Scroll down 2 times
5. Select one streamer
6. Wait for page to load
7. Take screenshot

**Markers**: `@pytest.mark.smoke`, `@pytest.mark.critical`, `@pytest.mark.mobile`

### Test Case 2: Detailed Validation Flow
**File**: `test_twitch_search.py::test_search_for_starcraft_ii_with_explicit_steps`

Same steps as Test Case 1 but with explicit validation at each step:
- URL verification
- Element visibility checks
- Result count validation
- Page load verification
- Video player detection

## 🏆 Framework Highlights

### 1. Scalability

- **Modular Design**: Easy to add new pages and tests
- **Reusable Components**: Base page with common methods
- **Configuration Management**: Easy to manage different environments
- **Parallel Execution**: Support for running tests in parallel

### 2. Maintainability

- **Page Object Model**: Changes to UI only require updates to page objects
- **Clear Separation**: Tests, pages, utilities are clearly separated
- **Comprehensive Logging**: Easy to debug issues
- **Type Hints**: Python type hints for better IDE support

### 3. Reliability

- **Anti-Flakiness**: Multiple strategies to handle flaky tests
- **Retry Mechanisms**: Automatic retries for transient failures
- **Multiple Locators**: Fallback locators for robustness
- **Proper Waits**: Explicit waits throughout

### 4. Observability

- **Detailed Logging**: Multi-level logging with timestamps
- **Screenshots**: Automatic capture on failure
- **HTML Reports**: Beautiful, detailed reports
- **Test Metadata**: Context about test execution

## 🔍 Debugging

### View Logs

```bash
# View full logs
cat logs/framework.log

# View only errors
cat logs/errors.log

# Live tail logs
tail -f logs/framework.log
```

### Common Issues

**Issue**: Tests fail with timeout
- **Solution**: Increase `EXPLICIT_WAIT` or `PAGE_LOAD_TIMEOUT` in `.env`

**Issue**: Can't find elements
- **Solution**: Check if mobile emulation is enabled. Some selectors may differ between mobile and desktop.

**Issue**: Video player not loading
- **Solution**: Framework handles this with retries and fallbacks. Check logs for specific errors.

**Issue**: Modal/popup blocking
- **Solution**: Framework automatically handles modals. If new modal types appear, add them to `StreamerPage.handle_modals_and_popups()`

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Twitch Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: |
          HEADLESS=true pytest --html=reports/report.html
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: test-reports
          path: |
            reports/
            screenshots/
```

## 📚 Adding New Tests

### 1. Create New Page Object

```python
# pages/new_page.py
from pages.base_page import BasePage

class NewPage(BasePage):
    # Define locators
    BUTTON = (By.ID, "button-id")
    
    def click_button(self):
        self.click(self.BUTTON)
```

### 2. Create Test

```python
# tests/test_new_feature.py
def test_new_feature(driver):
    page = NewPage(driver)
    page.click_button()
    assert page.verify_something()
```

## 🎓 Best Practices Used

1. **DRY Principle**: Don't Repeat Yourself - common code in base classes
2. **SOLID Principles**: Single responsibility, open/closed, etc.
3. **Explicit > Implicit**: Always use explicit waits
4. **Fail Fast**: Validations throughout tests
5. **Meaningful Names**: Clear, descriptive names for methods and variables
6. **Comprehensive Logging**: Log everything for debugging
7. **Error Handling**: Graceful failure with proper exceptions
8. **Configuration**: Never hardcode values
9. **Documentation**: Code comments and docstrings
10. **Version Control**: Framework ready for Git

## 🤝 Contributing

To extend the framework:

1. Follow existing code structure
2. Add docstrings to all methods
3. Use type hints
4. Add appropriate logging
5. Handle exceptions properly
6. Update README if adding new features

## 📝 Notes

- The framework uses Chrome mobile emulation via DevTools Protocol
- Screenshots are automatically taken on test failure
- All page interactions include retry mechanisms
- The framework handles common Twitch modals automatically
- Tests can be run in parallel using pytest-xdist
- Framework is designed to be easily extensible

## 📞 Support

For issues or questions:
1. Check logs in `logs/framework.log`
2. Review screenshots in `screenshots/`
3. Enable DEBUG logging: Set `LOG_LEVEL=DEBUG` in `.env`
4. Run single test in verbose mode: `pytest -vv -s test_file.py::test_name`

---

**Built with best practices for SDET excellence** 🚀
