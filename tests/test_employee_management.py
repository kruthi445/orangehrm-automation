import unittest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from pages.login_page import LoginPage

class TestEmployeeManagement(unittest.TestCase):
    
    def setUp(self):
        """Setup for each test"""
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service)
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
    
    def test_employee_workflow(self):
        """Test the complete employee management workflow"""
        # Employee data
        employees = [
            {"first": "John", "middle": "A", "last": "Doe"},
            {"first": "Jane", "middle": "B", "last": "Smith"},
            {"first": "Mike", "middle": "C", "last": "Johnson"}
        ]
        
        # 1. Login
        dashboard_page = self.login_page.open().login("Admin", "admin123")
        self.assertTrue(dashboard_page.is_loaded(), "Dashboard page failed to load")
        print("Step 1: Logged in successfully")
        
        # 2. Navigate to PIM
        pim_page = dashboard_page.click_pim_menu()
        print("Step 2: Navigated to PIM module")
        
        # 3. Add Employees
        for emp in employees:
            pim_page.add_employee(emp["first"], emp["middle"], emp["last"])
            print(f"Step 3: Added employee {emp['first']} {emp['last']}")
            # Navigate back to PIM
            dashboard_page.click_pim_menu()
        
        # 4. Verify Employees
        pim_page.go_to_employee_list()
        print("Step 4: Navigated to Employee List")
        
        for emp in employees:
            verified = pim_page.verify_employee(emp["first"], emp["last"])
            self.assertTrue(verified, f"Employee {emp['first']} {emp['last']} not found in the list")
        
        # 5. Logout
        login_page = dashboard_page.logout()
        print("Step 5: Logged out successfully")
    
    def tearDown(self):
        """Cleanup after each test"""
        if self.driver:
            self.driver.quit()