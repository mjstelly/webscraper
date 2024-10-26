from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from src.config.settings import BASE_URL
import time

def get_ebay_items(search_query, num_pages=1):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
    chrome_options.add_argument("--disable-gpu")
    
    # Specify the full path to ChromeDriver
    service = Service("/usr/local/bin/chromedriver")  # Update with the path to your chromedriver
    
    # Create a WebDriver instance
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    items = []
    
    for page in range(1, num_pages + 1):
        url = BASE_URL.format(search_query, page)
        print(f"\nFetching URL: {url}\n")
        
        # Use Selenium to load the page
        driver.get(url)
        
        # Allow time for JavaScript to load the listings
        time.sleep(5)  # Adjust if needed
        
        # Extract listings using Selenium's find_elements
        listings = driver.find_elements(By.CLASS_NAME, "s-item")
        
        for item in listings:
            try:
                title = item.find_element(By.CLASS_NAME, "s-item__title").text
                price = item.find_element(By.CLASS_NAME, "s-item__price").text
                shipping = item.find_element(By.CLASS_NAME, "s-item__shipping").text if item.find_elements(By.CLASS_NAME, "s-item__shipping") else "Free Shipping"
                
                if title and price:
                    item_data = {
                        "title": title.strip(),
                        "price": price.strip(),
                        "shipping": shipping.strip()
                    }
                    items.append(item_data)
            except Exception as e:
                print(f"Error extracting item: {e}")
    
    # Close the driver
    driver.quit()
    
    return items