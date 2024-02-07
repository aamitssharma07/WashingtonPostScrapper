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


#Function for Scraping heading, subheading and content of an article
def scrape_article_content(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize a dictionary to hold the content
    article_content = {
        "url": url,
        "headline": None,
        "subheading": None,
        "additional_content": []
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
    for paragraph in content_paragraphs:
        if paragraph:
            # Append each paragraph to the additional_content list
            article_content["additional_content"].append(paragraph.text.strip())

    # Serialize the dictionary to JSON and write it to a file
    with open('article_content.json', 'w', encoding='utf-8') as f:
        json.dump(article_content, f, ensure_ascii=False, indent=4)

    # print("Content saved to article_content.json.")
    
   
#Function for Scraping URL for iframe
def fetch_comments_iframe_url(article_url, email, password):
    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 15)
    
    try:
        # Navigate to the article URL
        driver.get(article_url)
        
        # Log in process
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

        # Navigate to comments section
        comment_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Comment']")))
        driver.execute_script("arguments[0].click();", comment_button)
        time.sleep(5)  # Wait for comments iframe to load

        # Extract the iframe URL
        iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#comments iframe")))
        iframe_url = iframe.get_attribute('src')
        
        return iframe_url  # Return the extracted iframe URL

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        driver.quit()  # Ensure the driver is quit regardless of success or failure
  
  
 # Function to scrape comments and add them to the existing JSON
def scrape_and_save_comments(url):
    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Open the URL
    driver.get(url)

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
        comment_text = comment.text.strip()
        # Add comment text to the list if it's not empty
        if comment_text:
            comments.append(comment_text)

    # Close the browser
    driver.quit()

    # Read the existing JSON file, update it with comments, and save back
    with open('article_content.json', 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data['comments'] = comments  # Add comments to the existing dictionary
        file.seek(0)  # Rewind to the start of the file
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.truncate()  # Truncate file to the new size

    # print("Comments added to article_content.json.")   
  
  
#******New logic Of Reading the url's from file"    
# # Function to read URLs from the JSON file
# def read_urls_from_json(filename):
#     with open(filename, 'r') as file:
#         urls = json.load(file)
#     return urls

# # Main function that orchestrates the scraping
# def main():
#     email = "mailtoammit1@gmail.com"
#     password = "7889857046@aA"
#     urls = read_urls_from_json('URLSWashPostPolitics.json')
    
#     for i, url in enumerate(urls, start=1):
#         print(f"Processing URL {i} of {len(urls)}: {url}")
        
#         # Scraping article content
#         scrape_article_content(url)
        
#         # Fetching the URL of Embedded HTML for comments
#         iframe_url = fetch_comments_iframe_url(url, email, password)
        
#         if iframe_url:
#             # Fetching the comments if iframe URL was successfully retrieved
#             scrape_and_save_comments(iframe_url, f'article_content_{i}.json')
#         else:
#             print("Could not fetch iframe URL for comments.")
            
#         print(f"Data for URL {i} loaded successfully.\n")

# if __name__ == "__main__":
#     print("Keep the patience, data is getting loaded...")
#     main()
#     print("Congrats, data Loaded Successfully for all URLs.")
  

# Main Program(OLd)

email = "mailtoammit1@gmail.com"
password = "7889857046@aA"
url = 'https://www.washingtonpost.com/national-security/2024/01/30/israel-hamas-qatar-hostage-deal/'

print("Keep the patience, data is getting loaded...")
#Function call for scrapping headline, subheadline and article content
scrape_article_content(url)

#Function Call for Fetching the URL of Embedded HTML
iframe_url = fetch_comments_iframe_url(url, email, password)


#Function Call for fetching the comments
scrape_and_save_comments(iframe_url)
print("Congrats, data Loaded Succesfully")


