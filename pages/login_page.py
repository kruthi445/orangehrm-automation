from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage

class LoginPage(BasePage):
    """Page object for the login page"""
    
    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//p[contains(text(), 'Forgot your password?')]")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class, 'oxd-alert')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    
    def open(self):
        """Open the login page"""
        self.driver.get(self.url)
        return self
    
    def enter_username(self, username):
        """Enter username in the username field"""
        self.wait_for_element(self.USERNAME_INPUT).send_keys(username)
        return self
    
    def enter_password(self, password):
        """Enter password in the password field"""
        self.wait_for_element(self.PASSWORD_INPUT).send_keys(password)
        return self
    
    def click_login_button(self):
        """Click on the login button"""
        self.wait_for_clickable(self.LOGIN_BUTTON).click()
        return DashboardPage(self.driver)
    
    def login(self, username, password):
        """Perform login with provided credentials"""
        self.enter_username(username)
        self.enter_password(password)
        return self.click_login_button()
    
    def get_error_message(self):
        """Get the error message text"""
        return self.wait_for_element(self.ERROR_MESSAGE).text