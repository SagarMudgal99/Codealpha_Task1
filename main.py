"""
Complete Web Scraping Project - Modular Structure
Organized by Task Requirements
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import pandas as pd
from urllib.parse import urljoin

# ===============================================
# SECTION 1: DATASET IDENTIFICATION & SETUP
# ===============================================
class WebScraper:
    def __init__(self):
        self.dataset = []
        self.base_url = "http://books.toscrape.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    # Task: Identify relevant public datasets
    def identify_datasets(self):
        """Identify scrapeable public websites"""
        targets = {
            'quotes': 'https://quotes.toscrape.com',
            'books': 'http://books.toscrape.com',
            'products': 'https://scrapingchallenge.com'
        }
        print("📋 Identified public datasets:", list(targets.keys()))
        return targets

# ===============================================
# SECTION 2: WEB NAVIGATION & HTML HANDLING
# ===============================================
    def navigate_and_parse(self, start_url, max_pages=50):
        """Handle HTML structure and web navigation"""
        page_num = 1
        while page_num <= max_pages:
            # Handle different pagination patterns
            page_url = start_url if page_num == 1 else f"{start_url.rstrip('/')}page-{page_num}.html"
            
            try:
                response = self.session.get(page_url, timeout=10)
                if response.status_code != 200:
                    print(f"❌ Page {page_num} not found (Status: {response.status_code})")
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                books = soup.find_all('article', class_='product_pod')
                
                if not books:
                    print(f"✅ No more books on page {page_num}")
                    break
                
                # Extract structured data
                for book in books:
                    self.extract_book_data(book)
                
                print(f"📖 Page {page_num}: {len(books)} books scraped")
                page_num += 1
                time.sleep(1)  # Respectful delay
                
            except Exception as e:
                print(f"⚠️ Error on page {page_num}: {e}")
                break

    def extract_book_data(self, book_element):
        """Parse HTML structure for accurate data extraction"""
        try:
            title = book_element.find('h3').find('a')['title']
            price = book_element.find('p', class_='price_color').text.strip()
            rating = book_element.find('p', class_='star-rating')['class'][1]
            availability = book_element.find('p', class_='availability').text.strip()
            
            self.dataset.append({
                'title': title,
                'price': price,
                'rating': rating,
                'availability': availability
            })
        except Exception as e:
            print(f"⚠️ Failed to extract book data: {e}")

# ===============================================
# SECTION 3: CUSTOM DATASET CREATION
# ===============================================
    def create_custom_dataset(self, output_file='books_custom.csv'):
        """Create tailored dataset for analysis"""
        df = pd.DataFrame(self.dataset)
        
        # Custom transformations for analysis
        df['price_numeric'] = df['price'].str.replace('£', '').astype(float)
        df['in_stock'] = df['availability'].str.contains('In stock')
        
        # Save enhanced dataset
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"💾 Custom dataset saved: {output_file}")
        print(f"📊 Dataset stats:")
        print(f"   • Total books: {len(df)}")
        print(f"   • Avg price: £{df['price_numeric'].mean():.2f}")
        print(f"   • In stock: {df['in_stock'].sum()}/{len(df)}")
        
        return df

# ===============================================
# SECTION 4: MAIN EXECUTION
# ===============================================
def main():
    """Execute complete web scraping workflow"""
    scraper = WebScraper()
    
    print("🚀 Starting Web Scraping Task")
    print("=" * 50)
    
    # Task 1: Identify datasets
    scraper.identify_datasets()
    
    # Task 2: Navigate & extract (handles HTML structure)
    print("\n📡 Scraping books.toscrape.com...")
    scraper.navigate_and_parse("http://books.toscrape.com")
    
    # Task 3: Create custom dataset
    dataset_df = scraper.create_custom_dataset()
    
    print("\n✅ Web Scraping Complete!")
    print("📁 Files created: books_custom.csv")

if __name__ == "__main__":
    main()


