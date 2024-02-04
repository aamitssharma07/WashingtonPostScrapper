from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time  # Importing time module

# Replace these with your actual email and password
email = "mailtoammit1@gmail.com"
password = "7889857046@aA"

# Setup Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to the Washington Post homepage
driver.get("https://www.washingtonpost.com/national-security/2024/01/30/israel-hamas-qatar-hostage-deal/")

# Increase wait time
time.sleep(5)  # Waits for 5 seconds

# Wait for the Sign-In button and click it
wait = WebDriverWait(driver, 15)
sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sc-account-button']")))
sign_in_button.click()

time.sleep(3)  # Waits for 3 seconds

# Wait for the email input to be present, enter email and click Next
email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
email_input.send_keys(email)
next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sign-in-btn']")))
next_button.click()

time.sleep(3)  # Waits for 3 seconds

# Wait for the password input to be present, enter password
password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
password_input.send_keys(password)

time.sleep(3)  # Waits for 3 seconds

# Click the Sign-In button to log in
sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sign-in-btn'][type='submit']")))
sign_in_button.click()

# Add any additional actions here

time.sleep(5)  # Waits for 5 seconds

# Close the driver after your automation tasks are complete
driver.quit()
