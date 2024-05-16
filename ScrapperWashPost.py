import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os

# Function for generating the name of JSON from URL
def generate_json_name(url):
    match = re.search(r'https://www.washingtonpost.com/([\w-]+)/(\d{4})/(\d{2})/(\d{2})/([\w-]+)/?$', url)
    if match:
        category = match.group(1)
        year = match.group(2)
        month = match.group(3)
        day = match.group(4)
        remaining_part = match.group(5)
        file_name = f"{category}_{year}_{month}_{day}_{remaining_part}.json"
        return file_name
    else:
        return "Invalid URL format"

# Function for Scraping heading, subheading, and content of an article
def scrape_article_content(url, json_name):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize a dictionary to hold the content
        article_content = {
            "url": url,
            "headline": None,
            "subheading": None,
            "article_body": None  # Storing as a single string
        }

        # Extract the headline
        headline = soup.find('span', class_='PJLV')
        if headline:
            article_content["headline"] = headline.text.strip()

        # Extract the subheading
        subheading = soup.find('h2', class_='font--subhead font-light offblack mb-sm pb-xxs-ns subheadline')
        if subheading:
            article_content["subheading"] = subheading.text.strip()

        # Extract the additional content
        content_paragraphs = soup.find_all('p', class_='wpds-c-cYdRxM wpds-c-cYdRxM-iPJLV-css overrideStyles font-copy')
        article_body = "".join(paragraph.text.strip() for paragraph in content_paragraphs)
        article_content["article_body"] = article_body

        # Serialize the dictionary to JSON and write it to a file
        with open(json_name, 'w', encoding='utf-8') as f:
            json.dump(article_content, f, ensure_ascii=False, indent=4)

        # print("Content saved to article_content.json."
    except Exception as e:
        print(f"Error scraping article content: {e}")

# Function for Scraping URL for iframe
def fetch_comments_iframe_url(article_url, email, password):
    try:
        # Initialize WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        wait = WebDriverWait(driver, 2)

        # Navigate to the article URL
        driver.get(article_url)

        # Increase wait time
        time.sleep(3)  # Waits for 5 seconds
        # Wait for the Sign-In button and click it
        wait = WebDriverWait(driver, 3)
        sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sc-account-button']")))
        sign_in_button.click()

        time.sleep(3)  # Waits for 3 seconds

        # Wait for the email input to be present, enter email and click Next
        email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_input.send_keys(email)
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sign-in-btn']")))
        next_button.click()

        time.sleep(2)  # Waits for 3 seconds

        # Wait for the password input to be present, enter password
        password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_input.send_keys(password)

        time.sleep(3)  # Waits for 3 seconds

        # Click the Sign-In button to log in
        sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='sign-in-btn'][type='submit']")))
        sign_in_button.click()
        # Navigate to comments section
        comment_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Comment']")))
        driver.execute_script("arguments[0].click();", comment_button)
        time.sleep(10)  # Wait for comments iframe to load

        # Extract the iframe URL
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#comments iframe")))
        iframe_url = iframe.get_attribute('src')

        return iframe_url  # Return the extracted iframe URL
    except Exception as e:
        print(f"Error fetching comments iframe URL: {e}")
        return None
    finally:
        driver.quit()  # Ensure the driver is quit regardless of success or failure

# Function to scrape comments and add them to the existing JSON
def scrape_and_save_comments(iframe_url, json_name):
    try:
        # Set up the WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        # Open the iframe_url
        driver.get(iframe_url)

        # Wait for the initial page to load
        time.sleep(5)

        # Loop to click the "Load More" button
        comments = []
        while True:
            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "comments-loadMore"))
                )
                load_more_button.click()
                time.sleep(3)
            except Exception as e:
                # print("Load More button not found or not clickable.")
                break

        # Find all comment elements
        comments_elements = driver.find_elements(By.CSS_SELECTOR, "div[class^='Box-root'] div[class^='HTMLContent-root']")

        # Extract text from each comment element and store in a list
        for comment in comments_elements:
            # Extract and clean text from each comment
            comment_text = comment.text.strip().replace('\n', '').replace('\\', '').replace('\"', '"')
            # Add comment text to the list if it's not empty
            if comment_text:
                comments.append(comment_text)

        # Close the browser
        driver.quit()

        # Read the existing JSON file, update it with comments, and save back
        with open(json_name, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data['comments'] = comments  # Store comments as a list
            file.seek(0)  # Rewind to the start of the file
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()  # Truncate file to the new size
    except Exception as e:
        print(f"Error scraping and saving comments: {e}")

# Main Program

email = "mailtoammit1@gmail.com"
password = "7889857046@aA"
count = 0
delete_count = 0
print("Keep the patience, data is getting loaded...")
# url = 'https://www.washingtonpost.com/national-security/2024/01/30/israel-hamas-qatar-hostage-deal/'

# Path to your JSON file
file_path = 'URL/WPPoliticsURL_September-06,-2022_to_February-09,-2024.json'
# Ensure the 'Data' directory exists
output_dir = 'Data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open and read the JSON file
with open(file_path, 'r') as file:
    # Load the content of the JSON file into a Python list
    urls = json.load(file)
    # Iterate over the list of URLs
    for url in urls:
        count += 1
        print(f" {count}. {url} is processing...")
        # Function call for generating the json name
        json_name = generate_json_name(url)
        json_name = os.path.join(output_dir, json_name)
        # Function call for scraping headline, subheading, and article content
        scrape_article_content(url, json_name)

        # Function Call for Fetching the URL of Embedded HTML
        iframe_url = fetch_comments_iframe_url(url, email, password)

        # Proceed only if iframe_url is valid (a non-empty string)
        if iframe_url and isinstance(iframe_url, str):
            # Function Call for fetching the comments
            scrape_and_save_comments(iframe_url, json_name)
        else:
            delete_count += 1
            print(f"Unable to fetch comments for {url} due to invalid iframe URL {iframe_url}.")
            if json_name and isinstance(json_name, str):
                try:
                    os.remove(json_name)
                    print(f"Deleted JSON file: {json_name}")
                except OSError as e:
                    print(f"Error deleting JSON file {json_name}: {e}")
            else:
                print("No JSON file found to delete.")

print(f"Congrats, data from {count - delete_count} articles is loaded successfully.")
