from src.scrapers.ebay_scraper import get_ebay_items, save_to_csv

def main():
    search = "ceramic pottery"
    pages = 2
    
    # Fetch eBay items
    print("Starting to scrape eBay items...")
    items = get_ebay_items(search, pages)
    
    # Check if items were fetched
    print(f"Number of items fetched: {len(items)}")
    
    # Save to CSV with a dynamic filename based on search term
    print("Calling save_to_csv function...")
    save_to_csv(items, search_query=search)
    print("CSV saving completed.")

if __name__ == "__main__":
    main()