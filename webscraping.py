import requests
from bs4 import BeautifulSoup
import json
import markdownify
from datetime import datetime
import os

# Function to extract the title and content of a page
def extract_page_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title = soup.title.string.strip() if soup.title else ""

        # Extract the content
        content = ""
        for paragraph in soup.find_all('p'):
            content += paragraph.text.strip() + '\n'

        # Convert HTML tables to markdown
        for table in soup.find_all('table'):
            markdown_table = markdownify.markdownify(str(table))
            content += markdown_table + '\n'

        return {'title': title, 'content': content}

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

# Function to scrape new pages and save data to a JSON file
def scrape_and_save_new_pages(num_pages):
    data = []
    base_url = 'https://www.juscorpus.com/category/blogs/page/'  
    existing_data = load_existing_data()

    for page_num in range(1, num_pages + 1):
        page_url = f'{base_url}{page_num}/'
        if page_url not in existing_data:
            page_data = extract_page_data(page_url)

            if page_data:
                data.append(page_data)
                existing_data.add(page_url)

    save_data(data)
    save_existing_data(existing_data)

# Function to load existing data
def load_existing_data():
    if os.path.exists('existing_data.txt'):
        with open('existing_data.txt', 'r') as file:
            return set(file.read().splitlines())
    else:
        return set()

# Function to save data to a JSON file
def save_data(data):
    with open('scraped_data.json', 'a', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Function to save existing data
def save_existing_data(existing_data):
    with open('existing_data.txt', 'w') as file:
        file.write('\n'.join(existing_data))

# Main function to run the scraper
if __name__ == '__main__':
    num_pages_to_scrape = 5
    scrape_and_save_new_pages(num_pages_to_scrape)
