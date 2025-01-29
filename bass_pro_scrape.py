import requests
from bs4 import BeautifulSoup
import csv
from typing import List, Tuple

def scrape_bass_pro_stores(url: str) -> List[Tuple[str, str]]:
    """
    Scrapes Bass Pro Shops store locations and phone numbers.
    
    Args:
        url (str): The URL of the Bass Pro Shops store locator
        
    Returns:
        List[Tuple[str, str]]: List of (phone_number, address) pairs
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    contact_info = []
    
    # Find all store listing items
    store_items = soup.find_all('li', class_='p-4')
    
    for store in store_items:
        # Find phone number (in a link with tel: href)
        phone_link = store.find('a', href=lambda x: x and x.startswith('tel:'))
        phone = phone_link.text.strip() if phone_link else ""
        
        # Find address lines
        address_lines = store.find_all('div', class_='address-line')
        full_address = ' '.join(
            span.text.strip() 
            for div in address_lines 
            for span in div.find_all('span')
        )
        
        if phone and full_address:
            contact_info.append((phone, full_address))
    
    return contact_info

def save_to_csv(contact_info: List[Tuple[str, str]], filename: str = 'bass_pro_stores.csv') -> None:
    """
    Saves the contact information to a CSV file.
    
    Args:
        contact_info (List[Tuple[str, str]]): List of (phone_number, address) pairs
        filename (str): Name of the output CSV file
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Phone Number', 'Address'])  # Header row
            writer.writerows(contact_info)
        print(f"Successfully saved store information to {filename}")
    except IOError as e:
        print(f"Error saving to CSV file: {e}")

def main():
    url = "https://stores.basspro.com/"
    print("Scraping Bass Pro Shops store locations...")
    contact_info = scrape_bass_pro_stores(url)
    
    if contact_info:
        save_to_csv(contact_info)
        print(f"Found {len(contact_info)} store locations")
        print("Data has been saved to bass_pro_stores.csv")
    else:
        print("No store information found")

if __name__ == "__main__":
    main()