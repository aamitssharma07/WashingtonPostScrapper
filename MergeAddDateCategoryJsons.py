import os
import json
from urllib.parse import urlparse

def extract_date_and_category(url):
    path_parts = urlparse(url).path.strip('/').split('/')
    # Extracting date parts (assuming it's always in YYYY/MM/DD format)
    date_parts = path_parts[1:4]
    date = '-'.join(date_parts)
    # Extracting category (assuming it's the first part after the domain)
    category = path_parts[0]
    return date, category

def list_json_files(directory):
    return [file for file in os.listdir(directory) if file.endswith('.json')]

def read_and_modify_json_files(directory, json_files):
    data_list = []
    for file in json_files:
        with open(os.path.join(directory, file), 'r') as f:
            data = json.load(f)
            date, category = extract_date_and_category(data['url'])
            data['date'] = date
            data['category'] = category
            data_list.append(data)
    return data_list

def merge_json_data(data_list):
    merged_data = {"articles": data_list}
    return merged_data

def save_merged_json_file(directory, merged_data, output_file):
    with open(os.path.join(directory, output_file), 'w') as f:
        json.dump(merged_data, f, indent=4)

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))  # The current directory where the script is located
    output_file = 'WashingtonPostPoliticsData.json'  # Output file name

    json_files = list_json_files(directory)
    modified_data_list = read_and_modify_json_files(directory, json_files)
    merged_data = merge_json_data(modified_data_list)
    save_merged_json_file(directory, merged_data, output_file)
