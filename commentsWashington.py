from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# URL to scrape
url = "https://talk.washingtonpost.com/embed/stream?storyURL=https%3A%2F%2Fwww.washingtonpost.com%2Fpolitics%2F2024%2F02%2F02%2Fmayorkas-impeachment-politics%2F&v=6.16.2&ts=1707178500000&initialWidth=535&childId=comments&parentTitle=The%20dicey%20push%20to%20impeach%20Secretary%20Mayorkas%20-%20The%20Washington%20Post&parentUrl=https%3A%2F%2Fwww.washingtonpost.com%2Fpolitics%2F2024%2F02%2F02%2Fmayorkas-impeachment-politics%2F"


# url = 'https://talk.washingtonpost.com/embed/stream?storyURL=https%3A%2F%2Fwww.washingtonpost.com%2Fbusiness%2F2024%2F01%2F31%2Fchild-tax-credit-vote-congress%2F&v=6.16.2&ts=1706766300000&initialWidth=535&childId=comments&parentTitle=Child%20tax%20credit%20expansion%20passes%20House%20-%20The%20Washington%20Post&parentUrl=https%3A%2F%2Fwww.washingtonpost.com%2Fbusiness%2F2024%2F01%2F31%2Fchild-tax-credit-vote-congress%2F'
# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the URL
driver.get(url)

# Wait for the initial page to load
time.sleep(5)

# Loop to click the "Load More" button
while True:
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "comments-loadMore"))
        )
        load_more_button.click()
        time.sleep(3)
    except Exception as e:
        print("Load More button not found or not clickable.")
        break

# Find all comment elements
comments_elements = driver.find_elements(By.CSS_SELECTOR, "div[class^='Box-root'] div[class^='HTMLContent-root']")

# Extract text from each comment element and store in a list
comments = []
for comment in comments_elements:
    # Extract and clean text from each comment
    comment_text = comment.text.strip()
    # Add comment text to the list if it's not empty
    if comment_text:
        comments.append(comment_text)

# Save comments to a JSON file
with open('WashingtonComments.json', 'w', encoding='utf-8') as file:
    json.dump(comments, file, ensure_ascii=False, indent=4)

# Close the browser
driver.quit()
