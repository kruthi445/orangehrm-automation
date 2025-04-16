from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from pages.base_page import BasePage

class PIMPage(BasePage):
    """Page object for the PIM page"""
    
    # Locators
    ADD_EMPLOYEE_LINK = (By.XPATH, "//a[contains(., 'Add Employee')]")
    EMPLOYEE_LIST_LINK = (By.XPATH, "//a[contains(., 'Employee List')]")
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    EMPLOYEE_LIST = (By.XPATH, "//div[contains(@class, 'oxd-table-body')]/div")
    
    # Search form locators
    EMPLOYEE_NAME_SEARCH = (By.XPATH, "//label[contains(text(), 'Employee Name')]/following::input[1]")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
    RESET_BUTTON = (By.XPATH, "//button[normalize-space()='Reset']")
    
    def click_add_employee(self):
        """Click on Add Employee link"""
        self.wait_for_clickable(self.ADD_EMPLOYEE_LINK).click()
        return self
    
    def add_employee(self, first_name, middle_name, last_name):
        """Add a new employee"""
        self.click_add_employee()
        
        self.wait_for_element(self.FIRST_NAME_INPUT).send_keys(first_name)
        self.wait_for_element(self.MIDDLE_NAME_INPUT).send_keys(middle_name)
        self.wait_for_element(self.LAST_NAME_INPUT).send_keys(last_name)
        
        # Wait for the loader to disappear
        try:
            loader = (By.CLASS_NAME, "oxd-form-loader")
            WebDriverWait(self.driver, 5).until_not(
                EC.presence_of_element_located(loader)
            )
        except:
            pass
        
        # Try to click with JavaScript if regular click fails
        try:
            save_button = self.wait_for_clickable(self.SAVE_BUTTON)
            save_button.click()
        except:
            save_button = self.driver.find_element(*self.SAVE_BUTTON)
            self.driver.execute_script("arguments[0].click();", save_button)
        
        # Wait for save to complete
        time.sleep(2)
        
        return self
    
    def go_to_employee_list(self):
        """Navigate to Employee List page"""
        self.wait_for_clickable(self.EMPLOYEE_LIST_LINK).click()
        
        # Wait for the page to load
        try:
            self.wait_for_presence_of_all_elements(self.EMPLOYEE_LIST)
        except TimeoutException:
            pass
        
        return self
    
    def wait_for_presence_of_all_elements(self, locator, timeout=10):
        """Wait for elements to be present in the DOM"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
    
    def search_employee(self, first_name, last_name):
        """Search for employee by name"""
        # First reset any existing filters
        try:
            reset_button = self.wait_for_clickable(self.RESET_BUTTON)
            reset_button.click()
            time.sleep(1)
        except:
            pass
        
        # Enter search term
        employee_name_input = self.wait_for_clickable(self.EMPLOYEE_NAME_SEARCH)
        employee_name_input.clear()
        employee_name_input.send_keys(f"{first_name} {last_name}")
        
        # Click search button
        self.wait_for_clickable(self.SEARCH_BUTTON).click()
        
        # Wait for search results
        time.sleep(2)
        
        return self
    
    def verify_employee(self, first_name, last_name):
        """Verify if employee exists in the list"""
        # First search for the employee
        self.search_employee(first_name, last_name)
        
        # Wait for employee list to update
        try:
            employees = self.wait_for_presence_of_all_elements(self.EMPLOYEE_LIST, timeout=5)
        except TimeoutException:
            return False
        
        # Check each row for employee name
        for employee in employees:
            try:
                cells = employee.find_elements(By.XPATH, ".//div[contains(@class, 'oxd-table-cell')]")
                row_text = ' '.join([cell.text for cell in cells])
                
                # Check if both first and last name appear in the row
                if first_name in row_text and last_name in row_text:
                    return True
                    
            except Exception:
                continue
        
        return False