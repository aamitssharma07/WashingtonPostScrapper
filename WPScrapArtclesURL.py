from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

def fetch_url_politics_section(url, email, password):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(url)
        sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sc-account-button']")))
        sign_in_button.click()
        email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_input.send_keys(email)
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sign-in-btn']")))
        next_button.click()
        password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input.send_keys(password)
        sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sign-in-btn'][type='submit']")))
        sign_in_button.click()
        for _ in range(1000):
            try:
                load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Load more')]")))
                driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
                load_more_button.click()
                time.sleep(2)  # Adjust sleep time as needed
            except TimeoutException:
                print("Load more button not found or no more articles to load.")
                break

        with open('URLSWashPostPolitics.json', 'w') as file:
            article_links = driver.find_elements(By.CSS_SELECTOR, "a.flex.hover-blue[data-pb-local-content-field='web_headline']")
            urls = [link.get_attribute('href') for link in article_links]
            json.dump(urls, file)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

email = "mailtoammit1@gmail.com"
password = "7889857046@aA"
politices_section_link = "https://www.washingtonpost.com/politics/"

print("Keep Patience, URLs are loading...")
fetch_url_politics_section(politices_section_link, email, password)
print("Congrats...URLs are successfully loaded into URLSWashPostPolitics.json")
