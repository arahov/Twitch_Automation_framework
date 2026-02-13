"""
WebDriver Factory
Handles WebDriver instantiation with proper configuration
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional
from config.config import Config
from utils.logger import log


class WebDriverFactory:
    """Factory class to create and configure WebDriver instances"""
    
    @staticmethod
    def create_driver() -> webdriver.Chrome:
        """
        Create and return configured Chrome WebDriver instance
        
        Returns:
            webdriver.Chrome: Configured Chrome WebDriver
        """
        try:
            log.info(f"Initializing Chrome WebDriver with mobile emulation: {Config.MOBILE_EMULATION}")
            
            options = WebDriverFactory._get_chrome_options()
            service = ChromeService(ChromeDriverManager().install())
            
            driver = webdriver.Chrome(service=service, options=options)
            
            # Set timeouts
            driver.implicitly_wait(Config.IMPLICIT_WAIT)
            driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
            
            log.info("WebDriver initialized successfully")
            log.info(f"Configuration: {Config.get_all_config()}")
            
            return driver
            
        except Exception as e:
            log.error(f"Failed to initialize WebDriver: {str(e)}")
            raise
    
    @staticmethod
    def _get_chrome_options() -> ChromeOptions:
        """
        Configure Chrome options including mobile emulation
        
        Returns:
            ChromeOptions: Configured Chrome options
        """
        options = ChromeOptions()
        
        # Basic options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Disable notifications and location prompts
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.media_stream": 2,
        }
        options.add_experimental_option("prefs", prefs)
        
        # Mobile emulation
        if Config.MOBILE_EMULATION:
            mobile_emulation = Config.get_mobile_emulation_config()
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            log.info(f"Mobile emulation enabled for device: {Config.DEVICE_NAME}")
        
        # Headless mode
        if Config.HEADLESS:
            options.add_argument('--headless=new')
            log.info("Running in headless mode")
        
        # Additional stability options
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--start-maximized')
        
        return options
    
    @staticmethod
    def quit_driver(driver: Optional[webdriver.Chrome]):
        """
        Safely quit the WebDriver
        
        Args:
            driver: WebDriver instance to quit
        """
        if driver:
            try:
                log.info("Closing WebDriver")
                driver.quit()
                log.info("WebDriver closed successfully")
            except Exception as e:
                log.warning(f"Error while quitting driver: {str(e)}")
