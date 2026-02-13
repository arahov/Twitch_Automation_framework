"""
Configuration Manager
Centralized configuration management for the framework
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class to manage all framework settings"""
    
    # Project paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    SCREENSHOT_DIR = BASE_DIR / os.getenv('SCREENSHOT_DIR', 'screenshots')
    LOG_DIR = BASE_DIR / os.getenv('LOG_DIR', 'logs')
    REPORT_DIR = BASE_DIR / os.getenv('REPORT_DIR', 'reports')
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')
    
    # Browser Configuration
    BROWSER = os.getenv('BROWSER', 'chrome').lower()
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    MOBILE_EMULATION = os.getenv('MOBILE_EMULATION', 'true').lower() == 'true'
    DEVICE_NAME = os.getenv('DEVICE_NAME', 'Pixel 5')
    
    # Timeout Configuration
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    
    # Application URLs
    BASE_URL = os.getenv('BASE_URL', 'https://m.twitch.tv/')
    
    # Screenshot Configuration
    SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Retry Configuration
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', '2'))
    
    # Chrome Mobile Devices Configuration
    MOBILE_DEVICES = {
        'Pixel 5': {
            'deviceMetrics': {'width': 393, 'height': 851, 'pixelRatio': 2.75},
            'userAgent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'
        },
        'iPhone 12': {
            'deviceMetrics': {'width': 390, 'height': 844, 'pixelRatio': 3},
            'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        },
        'iPhone 14 Pro Max': {
            'deviceMetrics': {'width': 430, 'height': 932, 'pixelRatio': 3},
            'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        },
        'Samsung Galaxy S21': {
            'deviceMetrics': {'width': 360, 'height': 800, 'pixelRatio': 3},
            'userAgent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'
        }
    }
    
    @classmethod
    def get_mobile_emulation_config(cls) -> Dict[str, Any]:
        """Get mobile emulation configuration for Chrome"""
        device = cls.MOBILE_DEVICES.get(cls.DEVICE_NAME, cls.MOBILE_DEVICES['Pixel 5'])
        return {
            'deviceMetrics': device['deviceMetrics'],
            'userAgent': device['userAgent']
        }
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        cls.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        cls.REPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_all_config(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            'environment': cls.ENVIRONMENT,
            'browser': cls.BROWSER,
            'headless': cls.HEADLESS,
            'mobile_emulation': cls.MOBILE_EMULATION,
            'device_name': cls.DEVICE_NAME,
            'base_url': cls.BASE_URL,
            'implicit_wait': cls.IMPLICIT_WAIT,
            'explicit_wait': cls.EXPLICIT_WAIT,
            'page_load_timeout': cls.PAGE_LOAD_TIMEOUT,
        }


# Initialize directories on import
Config.ensure_directories()
