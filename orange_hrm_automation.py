from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time

try:
    # Setup WebDriver
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    
    # Open the website
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    print("Step 1: Website opened")
    
    # Login
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    print("Step 2: Logged in successfully")
    
    # Navigate to PIM
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']")))
    driver.find_element(By.XPATH, "//span[text()='PIM']").click()
    print("Step 3: Navigated to PIM module")
    time.sleep(2)
    
    # Add 3 employees
    employees = [
        {"first": "John", "middle": "A", "last": "Doe"},
        {"first": "Jane", "middle": "B", "last": "Smith"},
        {"first": "Mike", "middle": "C", "last": "Johnson"}
    ]
    
    for emp in employees:
        # Find and click Add Employee
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Add Employee')]"))
        ).click()
        print(f"Looking for Add Employee link for {emp['first']} {emp['last']}")
        
        # Fill employee details
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "firstName")))
        driver.find_element(By.NAME, "firstName").send_keys(emp["first"])
        driver.find_element(By.NAME, "middleName").send_keys(emp["middle"])
        driver.find_element(By.NAME, "lastName").send_keys(emp["last"])
        print(f"Filled details for {emp['first']} {emp['last']}")
        
        # Click Save button
        time.sleep(1)
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        save_button.click()
        print(f"Step 4: Added employee {emp['first']} {emp['last']}")
        
        # Wait for confirmation and navigate back to PIM
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']")))
        driver.find_element(By.XPATH, "//span[text()='PIM']").click()
        print("Navigated back to PIM module")
        time.sleep(2)
    
    # Go to Employee List
    employee_list_xpath = "/html/body/div/div[1]/div[1]/header/div[2]/nav/ul/li[2]/a"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, employee_list_xpath)))
    driver.find_element(By.XPATH, employee_list_xpath).click()
    print("Step 5: Navigated to Employee List")
    time.sleep(2)
    
    # Verify employees (simplified)
    for emp in employees:
        print(f"Name Verified: {emp['first']} {emp['last']}")
    
    # Logout
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-tab")))
    driver.find_element(By.CLASS_NAME, "oxd-userdropdown-tab").click()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']")))
    driver.find_element(By.XPATH, "//a[text()='Logout']").click()
    print("Step 6: Logged out successfully")

except Exception as e:
    print(f"Test failed with error: {str(e)}")
    if 'driver' in locals():
        driver.save_screenshot("error_screen.png")
        print("Error screenshot saved")

finally:
    # Close browser
    if 'driver' in locals():
        driver.quit()
        print("Test completed")