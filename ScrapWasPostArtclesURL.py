from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime
import os
import time

def parse_date_from_string(date_string):
    try:
        return datetime.strptime(date_string.strip(), "%B %d, %Y")
    except Exception as e:
        print(f"Error parsing date from string {date_string}: {e}")
    return None

def fetch_url_politics_section(url, email, password, start_date, end_date):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 15)
    start_date_dt = datetime.strptime(start_date, "%B %d, %Y")
    end_date_dt = datetime.strptime(end_date, "%B %d, %Y")
    all_urls = []
    valid_urls = []
    output_dir = 'URL'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = f"WP_{url.split('/')[-2]}_URL_{start_date.replace(' ', '-')}_to_{end_date.replace(' ', '-')}.json"

    try:
        driver.get(url)
        sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sc-account-button']")))
        sign_in_button.click()
        time.sleep(3)  # Wait for modal to appear

        email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_input.send_keys(email)
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sign-in-btn']")))
        next_button.click()

        time.sleep(3)  # Wait for password field to appear

        password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input.send_keys(password)
        sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sign-in-btn'][type='submit']")))
        sign_in_button.click()

        # Wait for authentication to complete
        time.sleep(5)

        while True:
            try:
                article_elements = driver.find_elements(By.CSS_SELECTOR, "a.flex.hover-blue[data-pb-local-content-field='web_headline']")
                if not article_elements:
                    print("No more articles found.")
                    break

                stop_loading = False
                for article in article_elements:
                    href = article.get_attribute('href')
                    try:
                        parent_element = article.find_element(By.XPATH, "..")
                        date_element = parent_element.find_element(By.CSS_SELECTOR, "span[data-testid='timestamp']")
                        article_date_str = date_element.text
                        article_date = parse_date_from_string(article_date_str)
                        if article_date:
                            print(f"Processing article dated: {article_date_str} - URL: {href}")
                            all_urls.append((href, article_date))
                            if start_date_dt <= article_date <= end_date_dt:
                                valid_urls.append(href)
                                print(f"Valid URL: {href} - Date: {article_date}")
                            if article_date < start_date_dt:
                                print("Article is older than the start date, stopping.")
                                stop_loading = True
                                break
                    except NoSuchElementException:
                        print(f"No date found for article {href}, skipping.")
                        continue
                    except Exception as e:
                        print(f"Error processing article {href}: {e}")
                        continue

                if stop_loading:
                    break

                try:
                    load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Load more')]")))
                    driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
                    load_more_button.click()
                except TimeoutException:
                    print("Load more button not found or no more articles to load.")
                    break

            except WebDriverException as e:
                print(f"Error interacting with the page: {e}")
                break

        with open(os.path.join(output_dir, filename), 'w') as file:
            json.dump(valid_urls, file)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    return filename, valid_urls

# User inputs
email = input("Enter your email: ")
password = input("Enter your password: ")
start_date = input("Enter the start date (e.g., January 01, 2017): ")
end_date = input("Enter the end date (e.g., February 08, 2024): ")

# Valid subsections for Washington Post
valid_subsections = [
    "politics", "election-2024", "opinions", "style", 
    "investigations", "climate-environment", "business", 
    "technology", "world", "sports"
]

print(f"\nPlease choose a subsection to scrape. The valid subsections are:\n{', '.join(valid_subsections)}\n")

while True:
    subsection = input(f"Enter the subsection you want to scrape: ").strip()
    if subsection in valid_subsections:
        break
    else:
        print("Invalid subsection. Please enter one of the valid options.")

politics_section_link = f"https://www.washingtonpost.com/{subsection}/"

print("Keep patience, URLs are loading...")
filename, valid_urls = fetch_url_politics_section(politics_section_link, email, password, start_date, end_date)
print(f"Congrats... URLs are successfully loaded into '{filename}', total {len(valid_urls)} articles.")
