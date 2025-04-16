from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage

class DashboardPage(BasePage):
    """Page object for the dashboard page"""
    
    # Locators
    USER_DROPDOWN = (By.CLASS_NAME, "oxd-userdropdown-tab")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Logout']")
    PIM_MENU = (By.XPATH, "//span[text()='PIM']")
    
    def is_loaded(self):
        """Verify that dashboard page is loaded"""
        return self.wait_for_element(self.USER_DROPDOWN) is not None
    
    def click_pim_menu(self):
        """Click on PIM menu"""
        from pages.pim_page import PIMPage
        
        self.wait_for_clickable(self.PIM_MENU).click()
        return PIMPage(self.driver)
    
    def logout(self):
        """Logout from the application"""
        from pages.login_page import LoginPage
        
        self.wait_for_clickable(self.USER_DROPDOWN).click()
        self.wait_for_clickable(self.LOGOUT_LINK).click()
        return LoginPage(self.driver)