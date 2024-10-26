import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from src.config.settings import BASE_URL
import time
import csv
import os

def get_ebay_items(search_query, num_pages=1):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # Encode the search term for use in a URL
    encoded_search_query = urllib.parse.quote_plus(search_query)
    
    service = Service("/usr/local/bin/chromedriver")  # Use the correct path here
    driver = webdriver.Chrome(service=service, options=chrome_options)

    items = []

    for page in range(1, num_pages + 1):
        # Format the URL with the encoded search query
        url = BASE_URL.format(encoded_search_query, page)
        print(f"\nFetching URL: {url}\n")
        
        driver.get(url)
        time.sleep(5)

        listings = driver.find_elements(By.CLASS_NAME, "s-item")
        for item in listings:
            try:
                title = item.find_element(By.CLASS_NAME, "s-item__title").text
                price = item.find_element(By.CLASS_NAME, "s-item__price").text
                shipping = item.find_element(By.CLASS_NAME, "s-item__shipping").text if item.find_elements(By.CLASS_NAME, "s-item__shipping") else "Free Shipping"
                category = item.get_attribute("data-category")
                url = item.find_element(By.CLASS_NAME, "s-item__link").get_attribute("href")

                if title and price:
                    item_data = {
                        "title": title.strip(),
                        "price": price.strip(),
                        "shipping": shipping.strip(),
                        "category": category or "N/A",
                        "url": url
                    }
                    items.append(item_data)
            except Exception as e:
                print(f"Error extracting item: {e}")

    driver.quit()
    return items

def save_to_csv(items, search_query, filename_prefix="cleaned"):
    # Replace spaces with underscores for filenames
    sanitized_search_term = search_query.replace(" ", "_").lower()
    timestamp = int(time.time())  # Current UNIX timestamp
    filename = f"{filename_prefix}_{sanitized_search_term}_{timestamp}.csv"
    
    output_dir = "src/data/output"
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, filename)
    
    keys = ["title", "price", "shipping", "category", "url"]
    with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(items)
    
    print(f"Data successfully saved to {output_file_path}")