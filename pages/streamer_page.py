"""
Twitch Streamer Page Object
Page object for individual streamer page with video player
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from utils.logger import log
import time
from datetime import datetime


class StreamerPage(BasePage):
    """Page object for Twitch streamer page"""
    
    # Locators
    STREAMER_VIDEO = (By.XPATH, "//div[@data-a-target='video-player']")
    CHAT_WELCOME = (By.XPATH, "//div[@data-a-target='chat-welcome-message']")
    
    # Modal/Popup locators
    MATURE_CONTENT_MODAL = (By.XPATH, "//button[contains(text(), 'Start Watching') or contains(text(), 'Yes') or contains(text(), 'Continue')]")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//button[@aria-label='Close' or contains(@class, 'close')]")
    GENERIC_MODAL = (By.CSS_SELECTOR, "[role='dialog'], [data-a-target='modal']")
    OVERLAY = (By.CSS_SELECTOR, "[class*='overlay'], [class*='Overlay']")
    
    # Loading indicators
    LOADING_SPINNER = (By.CSS_SELECTOR, "[data-a-target='loading-spinner']")
    BUFFERING_INDICATOR = (By.XPATH, "//div[contains(@class, 'buffering') or contains(text(), 'buffering')]")
    
    # Stream info
    STREAM_TITLE = (By.CSS_SELECTOR, "h2[data-a-target='stream-title']")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        log.info("Initialized StreamerPage")
    
    def handle_modals_and_popups(self, timeout: int = 10):
        """
        Handle any modals or popups that appear before video loads
        
        Args:
            timeout: Maximum time to wait for modals
        """
        log.info("Checking for modals and popups")
        
        # Wait a moment for any modals to appear
        # time.sleep(2) (time.sleep(2) call removed)
        
        # Check for mature content modal
        try:
            if self.is_element_visible(self.MATURE_CONTENT_MODAL, timeout=5):
                log.info("Mature content modal detected")
                self.click(self.MATURE_CONTENT_MODAL)
                log.info("Mature content modal handled")
                # time.sleep(2) (time.sleep(2) call removed)
        except Exception as e:
            log.debug(f"No mature content modal found: {str(e)}")
        
        # Check for generic close buttons
        try:
            if self.is_element_visible(self.CLOSE_MODAL_BUTTON, timeout=3):
                log.info("Generic modal close button detected")
                self.click(self.CLOSE_MODAL_BUTTON)
                log.info("Modal closed")
                time.sleep(1)
        except Exception as e:
            log.debug(f"No generic close button found: {str(e)}")
        
        # Check for overlay elements that might be blocking
        try:
            if self.is_element_visible(self.OVERLAY, timeout=3):
                log.info("Overlay detected, attempting to dismiss")
                # Click outside the overlay or press ESC
                from selenium.webdriver.common.keys import Keys
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                time.sleep(1)
                log.info("Overlay dismissed")
        except Exception as e:
            log.debug(f"No overlay found: {str(e)}")
        
        log.info("Modal handling completed")
    
    def wait_for_page_to_load_completely(self, timeout: int = 30):
        """
        Wait for streamer page and video player to load completely
        
        Args:
            timeout: Maximum time to wait
        """
        log.info(f"Waiting for streamer page to load completely (timeout: {timeout}s)")
        start_time = time.time()
        
        try:
            # First, handle any modals
            self.handle_modals_and_popups()
            
            # Wait for loading spinner to disappear
            if self.is_element_present(self.LOADING_SPINNER):
                log.debug("Loading spinner detected, waiting for it to disappear")
                self.wait_for_element_to_disappear(self.LOADING_SPINNER, timeout=10)
            
            # Wait for page to be fully loaded
            self.wait_for_page_load(timeout=15)
            
            # Wait for video player to be present (primary check)
            log.debug("Waiting for video player element")
            try:
                self.find_element(self.STREAMER_VIDEO, timeout=15)
                log.info("Video player element found")
            except TimeoutException:
                log.warning("Video player not found, checking for chat welcome message as fallback")
                try:
                    self.find_element(self.CHAT_WELCOME, timeout=10)
                    log.info("Chat welcome message element found (fallback)")
                except TimeoutException:
                    log.warning("Neither video player nor chat welcome message found, but continuing")
            
            # Additional wait for video to initialize
            time.sleep(3)
            
            # Check if buffering
            if self.is_element_visible(self.BUFFERING_INDICATOR, timeout=2):
                log.info("Video is buffering, waiting...")
                time.sleep(5)
            
            elapsed_time = time.time() - start_time
            log.info(f"Page loaded successfully in {elapsed_time:.2f}s")
            
        except TimeoutException as e:
            elapsed_time = time.time() - start_time
            log.warning(f"Page load timeout after {elapsed_time:.2f}s, but continuing: {str(e)}")
        except Exception as e:
            log.error(f"Error during page load wait: {str(e)}")
            # Don't raise - we'll try to take screenshot anyway
    
    def is_video_player_loaded(self) -> bool:
        """
        Check if video player is loaded and visible
        
        Returns:
            bool: True if video player is loaded, False otherwise
        """
        log.debug("Checking if video player is loaded")
        try:
            # Check for video player element (primary)
            video_present = self.is_element_visible(self.STREAMER_VIDEO, timeout=5)
            
            if video_present:
                log.info("Video player is loaded and visible")
                return True
            
            # Fallback to chat welcome message
            log.debug("Video player not found, checking chat welcome message as fallback")
            chat_present = self.is_element_visible(self.CHAT_WELCOME, timeout=5)
            
            if chat_present:
                log.info("Chat welcome message is loaded and visible (fallback)")
                return True
            else:
                log.warning("Neither video player nor chat welcome message visible")
                return False
                
        except Exception as e:
            log.error(f"Error checking video player/chat status: {str(e)}")
            return False
    
    def is_chat_welcome_loaded(self) -> bool:
        """
        Check if chat welcome message is loaded and visible
        
        Returns:
            bool: True if chat welcome message is loaded, False otherwise
        """
        log.debug("Checking if chat welcome message is loaded")
        try:
            # Check for chat welcome element
            chat_present = self.is_element_visible(self.CHAT_WELCOME, timeout=5)
            
            if chat_present:
                log.info("Chat welcome message is loaded and visible")
                return True
            else:
                log.warning("Chat welcome message not visible")
                return False
                
        except Exception as e:
            log.error(f"Error checking chat welcome message status: {str(e)}")
            return False
    
    def get_streamer_info(self) -> dict:
        """
        Get information about the current streamer
        
        Returns:
            dict: Streamer information
        """
        log.debug("Getting streamer information")
        current_url = self.get_current_url()
        info = {
            'url': current_url,
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        # Extract streamer name from URL
        try:
            # URL format: https://m.twitch.tv/streamer_name or https://www.twitch.tv/streamer_name
            if 'twitch.tv/' in current_url:
                name_part = current_url.split('twitch.tv/')[-1].split('/')[0].split('?')[0]
                info['name'] = name_part if name_part else "Unknown"
            else:
                info['name'] = "Unknown"
        except:
            info['name'] = "Unknown"
        
        try:
            if self.is_element_visible(self.STREAM_TITLE, timeout=3):
                info['title'] = self.get_text(self.STREAM_TITLE)
        except:
            info['title'] = "Unknown"
        
        log.info(f"Streamer info: {info}")
        return info
    
    def take_streamer_screenshot(self, filename: str = None) -> str:
        """
        Take screenshot of the streamer page
        
        Args:
            filename: Optional custom filename
            
        Returns:
            str: Path to screenshot file
        """
        log.info("Taking streamer page screenshot")
        
        if not filename:
            info = self.get_streamer_info()
            timestamp = info['timestamp']
            streamer_name = info.get('name', 'unknown').replace(' ', '_')
            filename = f"streamer_{streamer_name}_{timestamp}.png"
        
        try:
            # Ensure video player is visible before screenshot
            if not self.is_video_player_loaded():
                log.warning("Video player may not be fully loaded, taking screenshot anyway")
            
            screenshot_path = self.take_screenshot(filename)
            log.info(f"Screenshot captured successfully: {screenshot_path}")
            return screenshot_path
            
        except Exception as e:
            log.error(f"Failed to take screenshot: {str(e)}")
            raise
    
    def verify_page_loaded(self) -> bool:
        """
        Verify that the streamer page has loaded successfully
        
        Returns:
            bool: True if page loaded successfully
        """
        log.info("Verifying streamer page loaded")
        
        try:
            # Check URL contains a channel name
            current_url = self.get_current_url()
            if "twitch.tv/" not in current_url or current_url.endswith("twitch.tv/"):
                log.error("URL does not appear to be a valid streamer page")
                return False
            
            # Check for key page elements (video player or chat welcome)
            video_present = self.is_element_present(self.STREAMER_VIDEO)
            chat_present = self.is_element_present(self.CHAT_WELCOME)
            
            if not video_present and not chat_present:
                log.error("Key page elements not found (neither video player nor chat welcome)")
                return False
            
            log.info("Streamer page verification successful")
            return True
            
        except Exception as e:
            log.error(f"Page verification failed: {str(e)}")
            return False
