from src.scrapers.ebay_scraper import get_ebay_items
from src.config.settings import BASE_URL

def main():
    # Prompt the user for a search term and the number of pages to scrape
    search = "ceramic"  # Using "ceramic" for debugging purposes
    pages = 2  # Checking the URL for page 2

    # Construct and print the URL to check correctness
    test_url = BASE_URL.format(search, pages)
    print(f"Generated URL: {test_url}")

    # Use the eBay scraper function to get the items
    items = get_ebay_items(search, pages)
    

    # Display the results
    if items:
        print(f"\nFound {len(items)} items:\n")
        for idx, item in enumerate(items, start=1):
            print(f"{idx}. {item['title']} - {item['price']} ({item['shipping']})")
    else:
        print("No items found.")

if __name__ == "__main__":
    main()