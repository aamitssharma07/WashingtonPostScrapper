from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# User credentials
email = "mailtoammit1@gmail.com"
password = "7889857046@aA"

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the article URL
# driver.get("https://www.washingtonpost.com/national-security/2024/01/30/israel-hamas-qatar-hostage-deal/")

driver.get("https://www.washingtonpost.com/business/2024/01/31/child-tax-credit-vote-congress/")

# Wait and click on the sign-in button
wait = WebDriverWait(driver, 15)
sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sc-account-button']")))
sign_in_button.click()

# Input email and continue
email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
email_input.send_keys(email)
next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sign-in-btn']")))
next_button.click()

# Input password and sign in
password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
password_input.send_keys(password)
sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sign-in-btn'][type='submit']")))
sign_in_button.click()

try:
    # Wait for the comment button to be present and click it
    comment_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Comment']")))
    driver.execute_script("arguments[0].click();", comment_button)

    # Wait a fixed amount of time for comments to load
    time.sleep(5)

    # Find the iframe and extract its URL
    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#comments iframe")))
    iframe_url = iframe.get_attribute('src')

    # Save the URL to a JSON file
    with open('washCommentsURL.json', 'w', encoding='utf-8') as file:
        json.dump({'commentsURL': iframe_url}, file, indent=4)

    print("URL extracted and saved to 'washCommentsURL.json'.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
