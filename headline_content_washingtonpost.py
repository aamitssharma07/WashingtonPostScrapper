import requests
from bs4 import BeautifulSoup
import json

# Define the URL of the article
url = "https://www.washingtonpost.com/politics/2024/02/02/mayorkas-impeachment-politics/"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize a dictionary to hold the content
article_content = {
    "headline": None,
    "subheading": None,
    "body": []
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
        article_content["body"].append(paragraph.text.strip())

# Serialize the dictionary to JSON and write it to a file
with open('washington_post_content.json', 'w', encoding='utf-8') as f:
    json.dump(article_content, f, ensure_ascii=False, indent=4)

print("Content saved to article_content.json.")
