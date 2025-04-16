class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        
    def wait_for_element(self, locator, timeout=10):
        """Wait for an element to be visible"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_clickable(self, locator, timeout=10):
        """Wait for an element to be clickable"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )