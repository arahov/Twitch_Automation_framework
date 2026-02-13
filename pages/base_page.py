"""
Base Page Object
Contains common methods for all page objects
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)
from typing import List, Tuple, Optional
import time
from config.config import Config
from utils.logger import log


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.short_wait = WebDriverWait(driver, 5)
    
    def navigate_to(self, url: str):
        """
        Navigate to a specific URL
        
        Args:
            url: URL to navigate to
        """
        try:
            log.info(f"Navigating to: {url}")
            self.driver.get(url)
            log.info(f"Successfully navigated to: {url}")
        except Exception as e:
            log.error(f"Failed to navigate to {url}: {str(e)}")
            raise
    
    def find_element(
        self, 
        locator: Tuple[By, str], 
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        Find element with explicit wait
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout
            
        Returns:
            WebElement: Found element
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        try:
            log.debug(f"Finding element: {locator}")
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            log.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            log.error(f"Timeout waiting for element: {locator}")
            raise
    
    def find_elements(
        self, 
        locator: Tuple[By, str], 
        timeout: Optional[int] = None
    ) -> List[WebElement]:
        """
        Find multiple elements with explicit wait
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout
            
        Returns:
            List[WebElement]: List of found elements
        """
        wait_time = timeout or Config.EXPLICIT_WAIT
        try:
            log.debug(f"Finding elements: {locator}")
            elements = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_all_elements_located(locator)
            )
            log.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            log.error(f"Timeout waiting for elements: {locator}")
            return []
    
    def click(self, locator: Tuple[By, str], retry: int = 3):
        """
        Click element with retry mechanism
        
        Args:
            locator: Tuple of (By, locator_string)
            retry: Number of retry attempts
        """
        for attempt in range(retry):
            try:
                log.debug(f"Attempting to click element: {locator} (Attempt {attempt + 1}/{retry})")
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
                log.debug(f"Successfully clicked element: {locator}")
                return
            except (ElementClickInterceptedException, StaleElementReferenceException) as e:
                if attempt == retry - 1:
                    log.error(f"Failed to click element after {retry} attempts: {locator}")
                    # Try JavaScript click as fallback
                    try:
                        element = self.find_element(locator)
                        self.driver.execute_script("arguments[0].click();", element)
                        log.info(f"Successfully clicked using JavaScript: {locator}")
                        return
                    except Exception as js_error:
                        log.error(f"JavaScript click also failed: {str(js_error)}")
                        raise
                log.warning(f"Click attempt {attempt + 1} failed, retrying...")
                time.sleep(1)
    
    def send_keys(self, locator: Tuple[By, str], text: str, clear_first: bool = True):
        """
        Send keys to element
        
        Args:
            locator: Tuple of (By, locator_string)
            text: Text to send
            clear_first: Whether to clear field first
        """
        try:
            log.debug(f"Sending keys to element: {locator}")
            element = self.wait.until(EC.visibility_of_element_located(locator))
            if clear_first:
                element.clear()
            element.send_keys(text)
            log.debug(f"Successfully sent keys to element: {locator}")
        except Exception as e:
            log.error(f"Failed to send keys to element {locator}: {str(e)}")
            raise
    
    def is_element_visible(self, locator: Tuple[By, str], timeout: int = 5) -> bool:
        """
        Check if element is visible
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Timeout for check
            
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            log.debug(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            log.debug(f"Element is not visible: {locator}")
            return False
    
    def is_element_present(self, locator: Tuple[By, str]) -> bool:
        """
        Check if element is present in DOM
        
        Args:
            locator: Tuple of (By, locator_string)
            
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            log.debug(f"Element is present: {locator}")
            return True
        except NoSuchElementException:
            log.debug(f"Element is not present: {locator}")
            return False
    
    def wait_for_element_to_disappear(self, locator: Tuple[By, str], timeout: int = 10):
        """
        Wait for element to disappear from DOM
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Timeout for wait
        """
        try:
            log.debug(f"Waiting for element to disappear: {locator}")
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located(locator)
            )
            log.debug(f"Element disappeared: {locator}")
        except TimeoutException:
            log.warning(f"Element did not disappear within {timeout}s: {locator}")
    
    def scroll_to_element(self, locator: Tuple[By, str]):
        """
        Scroll to element
        
        Args:
            locator: Tuple of (By, locator_string)
        """
        try:
            log.debug(f"Scrolling to element: {locator}")
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Brief pause for scroll animation
            log.debug(f"Scrolled to element: {locator}")
        except Exception as e:
            log.error(f"Failed to scroll to element {locator}: {str(e)}")
            raise
    
    def scroll_down(self, pixels: Optional[int] = None):
        """
        Scroll down the page
        
        Args:
            pixels: Number of pixels to scroll (if None, scrolls one viewport)
        """
        try:
            if pixels:
                script = f"window.scrollBy(0, {pixels});"
            else:
                script = "window.scrollBy(0, window.innerHeight);"
            
            log.debug(f"Scrolling down: {script}")
            self.driver.execute_script(script)
            time.sleep(0.5)  # Brief pause for content to load
            log.debug("Scroll completed")
        except Exception as e:
            log.error(f"Failed to scroll down: {str(e)}")
            raise
    
    def get_text(self, locator: Tuple[By, str]) -> str:
        """
        Get text from element
        
        Args:
            locator: Tuple of (By, locator_string)
            
        Returns:
            str: Element text
        """
        try:
            log.debug(f"Getting text from element: {locator}")
            element = self.find_element(locator)
            text = element.text
            log.debug(f"Retrieved text: '{text}' from {locator}")
            return text
        except Exception as e:
            log.error(f"Failed to get text from element {locator}: {str(e)}")
            raise
    
    def wait_for_page_load(self, timeout: int = 30):
        """
        Wait for page to fully load
        
        Args:
            timeout: Timeout for page load
        """
        try:
            log.debug("Waiting for page to load")
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            log.debug("Page loaded successfully")
        except TimeoutException:
            log.warning(f"Page did not fully load within {timeout}s")
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        url = self.driver.current_url
        log.debug(f"Current URL: {url}")
        return url
    
    def take_screenshot(self, filename: str) -> str:
        """
        Take screenshot and save to file
        
        Args:
            filename: Name for screenshot file
            
        Returns:
            str: Path to saved screenshot
        """
        try:
            filepath = Config.SCREENSHOT_DIR / filename
            self.driver.save_screenshot(str(filepath))
            log.info(f"Screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            log.error(f"Failed to take screenshot: {str(e)}")
            raise
