"""
Twitch Search Results Page Object
Page object for Twitch search results page
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from utils.logger import log
import time


class SearchResultsPage(BasePage):
    """Page object for Twitch search results page"""
    
    # Locators
    # Directory page search
    SEARCH_INPUT = (By.XPATH, "//input[@type='search' and @placeholder='Search']")
    
    # Search results
    SEARCH_RESULTS_CONTAINER = (By.XPATH, "//h2[normalize-space()='Channels']")
    STREAMER_CARDS = (By.XPATH, "//h2[normalize-space()='Channels']/ancestor::section//div[contains(@class,'doaFqY')]/*[self::a or self::button]")
    
    # Loading indicators
    LOADING_SPINNER = (By.CSS_SELECTOR, "[data-a-target='loading-spinner']")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        log.info("Initialized SearchResultsPage")
    
    def enter_search_query(self, query: str):
        """
        Enter search query in the directory page search input
        
        Args:
            query: Search query string (e.g., 'StarCraft II')
        """
        log.info(f"Entering search query: '{query}'")
        try:
            self.send_keys(self.SEARCH_INPUT, query, clear_first=True)
            log.info("Search query typed")
            
            # Press Enter to search (crucial for mobile)
            self.driver.find_element(*self.SEARCH_INPUT).send_keys(Keys.ENTER)
            log.info("Pressed Enter to submit search")
            
            time.sleep(2)  # Wait for search results to appear
        except Exception as e:
            log.error(f"Failed to enter search query: {str(e)}")
            raise
    
    def wait_for_results_to_load(self, timeout: int = 10):
        """
        Wait for search results to load
        
        Args:
            timeout: Maximum time to wait
        """
        log.info("Waiting for search results to load")
        try:
            # Wait for loading spinner to disappear if present
            if self.is_element_present(self.LOADING_SPINNER):
                self.wait_for_element_to_disappear(self.LOADING_SPINNER, timeout)
            
            # Wait for results container
            self.find_element(self.SEARCH_RESULTS_CONTAINER, timeout)
            time.sleep(2)  # Additional wait for dynamic content
            log.info("Search results loaded successfully")
        except Exception as e:
            log.warning(f"Could not verify results loading, proceeding anyway: {str(e)}")
    
    def scroll_down_times(self, times: int = 2):
        """
        Scroll down the search results multiple times
        
        Args:
            times: Number of times to scroll
        """
        log.info(f"Scrolling down {times} time(s)")
        for i in range(times):
            log.debug(f"Scroll iteration {i + 1}/{times}")
            self.scroll_down()
            time.sleep(1.5)  # Wait for content to load after scroll
        log.info("Scrolling completed")
    
    def select_random_streamer(self) -> bool:
        """
        Select a random streamer from the Channels section
        
        Returns:
            bool: True if successful, False otherwise
        """
        log.info("Attempting to select a random streamer")
        try:
            # Wait for search results first (redundant if caller does it but safe)
            self.wait_for_results_to_load()
            
            # Find all streamer elements using the new locator
            # Using find_elements since multiple results expected
            import random
            
            # Using a broad XPath to find clickable elements under the Channels heading
            streamer_elements = self.driver.find_elements(*self.STREAMER_CARDS)
            
            # Filter for visible and enabled
            visible_elements = [el for el in streamer_elements if el.is_displayed() and el.is_enabled()]
            
            if not visible_elements:
                log.error("No visible streamer elements found")
                return False
            
            # Select random
            selected_element = random.choice(visible_elements)
            log.info(f"Selected random streamer element: {selected_element}")
            
            # Scroll and click
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selected_element)
            time.sleep(0.5)
            selected_element.click()
            log.info("Clicked streamer element")
            time.sleep(2)  # Wait for navigation
            
            return True
        except Exception as e:
            log.error(f"Failed to select random streamer: {str(e)}")
            return False

