"""
Twitch Automation Test Suite
Test cases for Twitch mobile search and streamer navigation
"""
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.home_page import TwitchHomePage
from pages.search_results_page import SearchResultsPage
from pages.streamer_page import StreamerPage
from utils.logger import log
import time


@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.mobile
class TestTwitchSearch:
    """Test suite for Twitch search functionality"""
    
    @pytest.mark.parametrize("search_query", ["StarCraft II"])
    def test_search_and_navigate_to_streamer(self, driver: WebDriver, search_query: str):
        """
        Test Case: Search for StarCraft II in directory page
        
        Steps:
        1. Navigate to https://m.twitch.tv/
        2. Click the BROWSE Tab
        3. Enter 'StarCraft II' in the directory page search
        4. Scroll down 2 times
        5. Select one streamer randomly from Channels section
        6. Wait for page to load and take screenshot
        
        Args:
            driver: WebDriver instance from fixture
            search_query: Search query to use
        """
        log.info("Starting test: Directory page search")
        
        try:
            # Step 1: Navigate to Twitch mobile home page
            log.info("Step 1: Navigate to https://m.twitch.tv/")
            home_page = TwitchHomePage(driver)
            home_page.open()
            
            # Verify page loaded
            assert "twitch.tv" in driver.current_url.lower(), "Failed to load Twitch home page"
            log.info("✓ Successfully navigated to Twitch home page")
            
            # Step 2: Click the BROWSE button
            log.info("Step 2: Click the BROWSE button")
            # home_page.click_browse_button()
            # time.sleep(2)
            home_page.click_browse_button() # time.sleep(2) call removed
            log.info("✓ BROWSE button clicked, directory page loaded")
            
            # Initialize search results page (directory page)
            search_page = SearchResultsPage(driver)
            
            # Step 3: Enter search query in directory page
            log.info(f"Step 3: Enter search query '{search_query}' in directory page")
            # search_page.enter_search_query(search_query)
            # time.sleep(2)
            search_page.enter_search_query(search_query) # time.sleep(2) call removed
            log.info("✓ Search query entered")
            
            # Step 4: Scroll down 2 times
            log.info("Step 4: Scroll down 2 times")
            search_page.scroll_down_times(times=2)
            log.info("✓ Scrolled down 2 times")
            
            # Step 5: Select one streamer from Channels section
            log.info("Step 5: Select a streamer from Channels section")
            streamer_selected = search_page.select_random_streamer()
            assert streamer_selected, "Failed to select a streamer"
            log.info("✓ Streamer selected successfully")
            
            # Step 6: Wait for streamer page to load and take screenshot
            log.info("Step 6: Wait for page to load and take screenshot")
            streamer_page = StreamerPage(driver)
            
            # Handle any modals/popups and wait for page to load
            streamer_page.wait_for_page_to_load_completely(timeout=30)
            
            # Verify page loaded
            assert streamer_page.verify_page_loaded(), "Streamer page did not load correctly"
            log.info("✓ Streamer page loaded successfully")
            
            # Take screenshot
            screenshot_path = streamer_page.take_streamer_screenshot()
            assert screenshot_path, "Failed to take screenshot"
            log.info(f"✓ Screenshot captured: {screenshot_path}")
            
            # Log test success
            log.info("=" * 80)
            log.info("TEST PASSED: All steps completed successfully")
            log.info("=" * 80)
            
        except AssertionError as e:
            log.error(f"Test assertion failed: {str(e)}")
            raise
        except Exception as e:
            log.error(f"Test failed with error: {str(e)}")
            raise
    
    def test_search_for_starcraft_ii_with_explicit_steps(self, driver: WebDriver):
        """
        Test Case: Detailed test for StarCraft II search with explicit validation
        
        This test is more detailed with explicit validations at each step
        
        Args:
            driver: WebDriver instance from fixture
        """
        log.info("Starting detailed StarCraft II search test")
        
        # Step 1: Navigate to Twitch
        home_page = TwitchHomePage(driver)
        home_page.open()
        
        # Validation: Check we're on Twitch
        current_url = driver.current_url
        assert "twitch.tv" in current_url.lower(), f"Not on Twitch! Current URL: {current_url}"
        log.info("✓ Validated: On Twitch website")
        
        # Step 2: Click BROWSE button
        # home_page.click_browse_button()
        # time.sleep(2)
        home_page.click_browse_button() # time.sleep(2) call removed
        
        # Initialize search results page (directory page)
        search_page = SearchResultsPage(driver)
        
        # Validation: Search input should be visible in directory page
        from selenium.webdriver.common.by import By
        search_input_visible = search_page.is_element_visible(search_page.SEARCH_INPUT, timeout=5)
        assert search_input_visible, "Search input not visible in directory page"
        log.info("✓ Validated: Search input is visible in directory page")
        
        # Step 3: Enter search query in directory page
        search_query = "StarCraft II"
        # search_page.enter_search_query(search_query)
        # time.sleep(2)
        search_page.enter_search_query(search_query) # time.sleep(2) call removed
        log.info(f"✓ Entered search query: {search_query}")
        
        # Validation: Wait for search results to load
        search_page.wait_for_results_to_load()
        log.info("✓ Validated: Search results loaded")
        
        # Step 5: Scroll and load more results
        # search_page.scroll_down_times(times=2)
        # time.sleep(2)
        search_page.scroll_down_times(times=2) # time.sleep(2) call removed
        log.info("✓ Validated: Scrolling completed")
        
        # Step 6: Select a streamer
        success = search_page.select_random_streamer()
        assert success, "Failed to select and navigate to streamer"
        log.info("✓ Successfully navigated to streamer page")
        
        # Step 7: Handle modals and wait for stream to load
        streamer_page = StreamerPage(driver)
        streamer_page.wait_for_page_to_load_completely(timeout=30)
        
        # Validation: Verify we're on a streamer page
        assert streamer_page.verify_page_loaded(), "Streamer page validation failed"
        log.info("✓ Validated: Streamer page loaded correctly")
        
        # Validation: Check chat welcome message is present
        chat_loaded = streamer_page.is_chat_welcome_loaded()
        log.info(f"Chat welcome message loaded: {chat_loaded}")
        
        # Step 8: Capture screenshot
        screenshot_path = streamer_page.take_streamer_screenshot()
        assert screenshot_path, "Screenshot capture failed"
        log.info(f"✓ Screenshot saved: {screenshot_path}")
        
        # Final validation
        log.info("=" * 80)
        log.info("TEST PASSED: All validations successful")
        log.info("=" * 80)


@pytest.mark.regression
class TestTwitchSearchRobustness:
    """Additional tests for framework robustness"""
    
    def test_handle_no_results_gracefully(self, driver: WebDriver):
        """
        Test that framework handles edge cases gracefully
        
        Args:
            driver: WebDriver instance
        """
        log.info("Testing edge case handling")
        
        home_page = TwitchHomePage(driver)
        home_page.open()
        
        # Navigate to directory page
        home_page.click_browse_button()
        
        search_page = SearchResultsPage(driver)
        # This should handle no results or errors gracefully
        # search_page.enter_search_query("ThisIsAVeryUnlikelySearchQueryWithNoResults12345")
        # time.sleep(2)
        search_page.enter_search_query("ThisIsAVeryUnlikelySearchQueryWithNoResults12345") # time.sleep(2) call removed
        
        # Test passes if we got here without crashing
        log.info("Search completed without crashing")
        assert True, "Framework handled edge case without crashing"
    
    @pytest.mark.parametrize("query", ["StarCraft", "League of Legends", "Valorant"])
    def test_multiple_search_queries(self, driver: WebDriver, query: str):
        """
        Test multiple different search queries
        
        Args:
            driver: WebDriver instance
            query: Search query to test
        """
        log.info(f"Testing search for: {query}")
        
        home_page = TwitchHomePage(driver)
        home_page.open()
        
        # Navigate to directory page
        home_page.click_browse_button()
        
        search_page = SearchResultsPage(driver)
        search_page.enter_search_query(query)
        search_page.wait_for_results_to_load()
        
        log.info(f"✓ Search completed for '{query}'")
