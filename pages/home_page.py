"""
Twitch Home Page Object
Page object for Twitch mobile home page
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from utils.logger import log
import time


class TwitchHomePage(BasePage):
    """Page object for Twitch mobile home page"""
    
    # Locators
    BROWSE_ICON = (By.XPATH, "//div[contains(@class,'CoreText-sc') and normalize-space()='Browse']")
    
    # Cookie/consent banner
    CONSENT_BANNER = (By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Reject') or contains(@class, 'consent')]")
    MATURE_CONTENT_BUTTON = (By.XPATH, "//button[contains(text(), 'Start Watching')]")
    APP_UPSELL_MODAL = (By.XPATH, "//button[.//p[contains(normalize-space(), 'Keep using web')]]")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        log.info("Initialized TwitchHomePage")
    
    def open(self):
        """Navigate to Twitch home page"""
        from config.config import Config
        log.info(f"Opening Twitch home page: {Config.BASE_URL}")
        self.navigate_to(Config.BASE_URL)
        self.wait_for_page_load()
        self.handle_consent_banner()
        self.handle_app_upsell()
    
    def handle_consent_banner(self):
        """Handle cookie consent or mature content banners if present"""
        try:
            log.debug("Checking for consent/cookie banners")
            if self.is_element_visible(self.CONSENT_BANNER, timeout=3):
                log.info("Consent banner detected, attempting to handle")
                self.click(self.CONSENT_BANNER)
                time.sleep(1)
                log.info("Consent banner handled")
        except Exception as e:
            log.debug(f"No consent banner found or already handled: {str(e)}")
            
    def handle_app_upsell(self):
        """Handle 'Open in App' vs 'Keep using web' upsell modal"""
        try:
            log.debug("Checking for app upsell modal")
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # Use explicit wait for clickable element as requested
            # Reduced timeout to 2 seconds to avoid slowing down tests when popup is not present
            keep_web = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(self.APP_UPSELL_MODAL)
            )
            keep_web.click()
            log.info("Closed bottom sheet via 'Keep using web'")
        except Exception as e:
            log.debug(f"Bottom sheet not present or not clickable: {str(e)}")
    
    def click_browse_button(self):
        """Click on the Browse button to navigate to directory page"""
        log.info("Clicking Browse button")
        try:
            self.is_element_visible(self.BROWSE_ICON, timeout=5)
            self.click(self.BROWSE_ICON)
            log.info("Browse button clicked successfully")
            
            # Wait for directory page to load by checking Channels heading from SearchResultsPage
            from pages.search_results_page import SearchResultsPage
            self.is_element_visible(SearchResultsPage.SEARCH_RESULTS_CONTAINER, timeout=10)
            log.info("Directory page loaded successfully")
            time.sleep(1)  # Additional buffer for dynamic content
        except Exception as e:
            log.error(f"Failed to click Browse button or load directory page: {str(e)}")
            raise

