"""
Pytest Configuration and Fixtures
Central configuration for pytest with reusable fixtures
"""
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from utils.webdriver_factory import WebDriverFactory
from utils.logger import log
from config.config import Config
from datetime import datetime
import os

# Device mapping for parallel execution with pytest-xdist
DEVICE_MAPPING = {
    'gw0': 'Pixel 5',
    'gw1': 'iPhone 12',
    'gw2': 'iPhone 14 Pro Max',
    'gw3': 'Samsung Galaxy S21'
}


def get_device_for_worker(worker_id: str) -> str:
    """
    Get device name for a specific worker
    
    Args:
        worker_id: Worker ID (e.g., 'gw0', 'gw1', 'master')
        
    Returns:
        str: Device name for the worker
    """
    # If running without xdist (master), use default device
    if worker_id == 'master':
        return Config.DEVICE_NAME
    
    # For workers beyond gw3, cycle through devices
    if worker_id in DEVICE_MAPPING:
        return DEVICE_MAPPING[worker_id]
    else:
        # Extract worker number and cycle through devices
        try:
            worker_num = int(worker_id.replace('gw', ''))
            devices = list(DEVICE_MAPPING.values())
            return devices[worker_num % len(devices)]
        except:
            return Config.DEVICE_NAME


@pytest.fixture(scope="function")
def driver(request) -> WebDriver:
    """
    Fixture to provide WebDriver instance for tests
    Supports parallel execution with device-specific configuration
    
    Args:
        request: pytest request object
        
    Yields:
        WebDriver: Configured WebDriver instance
    """
    # Get worker ID for parallel execution
    worker_id = getattr(request.config, 'workerinput', {}).get('workerid', 'master')
    device_name = get_device_for_worker(worker_id)
    
    log.info("=" * 80)
    log.info(f"[{worker_id}][{device_name}] Setting up WebDriver for test")
    log.info("=" * 80)
    
    driver_instance = None
    try:
        driver_instance = WebDriverFactory.create_driver(device_name=device_name)
        yield driver_instance
    finally:
        if driver_instance:
            log.info("=" * 80)
            log.info(f"[{worker_id}][{device_name}] Tearing down WebDriver")
            log.info("=" * 80)
            WebDriverFactory.quit_driver(driver_instance)


@pytest.fixture(scope="function", autouse=True)
def test_logger(request):
    """
    Fixture to log test start and end with worker and device info
    
    Args:
        request: pytest request object
    """
    test_name = request.node.name
    worker_id = getattr(request.config, 'workerinput', {}).get('workerid', 'master')
    device_name = get_device_for_worker(worker_id)
    
    log.info("=" * 80)
    log.info(f"[{worker_id}][{device_name}] STARTING TEST: {test_name}")
    log.info("=" * 80)
    
    yield
    
    log.info("=" * 80)
    log.info(f"[{worker_id}][{device_name}] FINISHED TEST: {test_name}")
    log.info("=" * 80)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure
    
    Args:
        item: Test item
        call: Test call information
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only process on test call (not setup/teardown)
    if report.when == "call":
        if report.failed and Config.SCREENSHOT_ON_FAILURE:
            # Get driver from test if available
            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
                try:
                    # Get worker info for unique screenshot naming
                    worker_id = getattr(item.config, 'workerinput', {}).get('workerid', 'master')
                    device_name = get_device_for_worker(worker_id)
                    device_suffix = device_name.replace(" ", "")
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    test_name = item.name.replace(" ", "_")
                    screenshot_name = f"FAILED_{test_name}_{timestamp}_{worker_id}_{device_suffix}.png"
                    screenshot_path = Config.SCREENSHOT_DIR / screenshot_name
                    
                    driver.save_screenshot(str(screenshot_path))
                    log.error(f"[{worker_id}][{device_name}] Test failed! Screenshot saved: {screenshot_path}")
                    
                    # Attach to pytest-html report if available
                    if hasattr(report, 'extra'):
                        report.extra.append(pytest.html.extra.image(str(screenshot_path)))
                        
                except Exception as e:
                    log.error(f"Failed to capture screenshot on test failure: {str(e)}")


def pytest_configure(config):
    """
    Configure pytest with custom metadata
    
    Args:
        config: pytest config object
    """
    # Add custom metadata to HTML report
    config._metadata = {
        'Project': 'Twitch Automation Framework',
        'Environment': Config.ENVIRONMENT,
        'Browser': Config.BROWSER,
        'Mobile Emulation': Config.MOBILE_EMULATION,
        'Device': Config.DEVICE_NAME if Config.MOBILE_EMULATION else 'N/A',
        'Headless Mode': Config.HEADLESS,
        'Base URL': Config.BASE_URL,
        'Python Version': os.sys.version.split()[0],
    }


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    """
    Session-level setup
    """
    log.info("=" * 80)
    log.info("TEST SESSION STARTED")
    log.info(f"Configuration: {Config.get_all_config()}")
    log.info("=" * 80)
    
    yield
    
    log.info("=" * 80)
    log.info("TEST SESSION ENDED")
    log.info("=" * 80)


@pytest.fixture(scope="function")
def screenshot_dir():
    """
    Fixture to provide screenshot directory path
    
    Returns:
        Path: Screenshot directory path
    """
    return Config.SCREENSHOT_DIR
