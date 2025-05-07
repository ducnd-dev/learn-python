"""
Etsy SEO Data Scraper

This script scrapes product SEO data from Etsy including:
- Product titles and descriptions
- Tags and categories
- Pricing information
- Seller information
- Reviews and ratings
- Product images
- Search ranking data

Usage:
    python etsy_scraper.py --search "handmade jewelry" --pages 3
"""

import os
import re
import time
import json
import random
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("etsy_scraper.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("etsy_scraper")


class EtsyScraper:
    """Scraper for Etsy products and SEO data"""
    
    def __init__(self, headless: bool = True, use_proxy: bool = False):
        """
        Initialize the Etsy scraper
        
        Args:
            headless: Whether to run browser in headless mode
            use_proxy: Whether to use proxy servers
        """
        self.base_url = "https://www.etsy.com"
        self.search_url = f"{self.base_url}/search"
        self.headers = self._get_headers()
        self.driver = self._setup_webdriver(headless)
        self.use_proxy = use_proxy
        self.proxies = self._load_proxies() if use_proxy else None
        self.data_dir = "data"
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
    def _get_headers(self) -> Dict[str, str]:
        """Generate random user agent headers"""
        ua = UserAgent()
        return {
            "User-Agent": ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    
    def _load_proxies(self) -> List[str]:
        """Load proxy servers from environment or file"""
        proxy_list = os.environ.get("PROXY_LIST", "")
        if proxy_list:
            return proxy_list.split(",")
        
        if os.path.exists("proxies.txt"):
            with open("proxies.txt", "r") as f:
                return [line.strip() for line in f if line.strip()]
        
        logger.warning("No proxies found. Running without proxies.")
        return []
    
    def _get_random_proxy(self) -> Dict[str, str]:
        """Get a random proxy from the list"""
        if not self.proxies:
            return {}
        
        proxy = random.choice(self.proxies)
        return {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    
    def _setup_webdriver(self, headless: bool) -> webdriver.Chrome:
        """Setup and configure Chrome WebDriver"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Add random user agent
        ua = UserAgent()
        chrome_options.add_argument(f"--user-agent={ua.random}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set a custom navigator.webdriver property
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        
        return driver
    
    def search_products(self, query: str, max_pages: int = 1) -> List[Dict[str, Any]]:
        """
        Search for products on Etsy and extract basic data
        
        Args:
            query: Search query
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of product dictionaries with basic data
        """
        logger.info(f"Searching for '{query}' (up to {max_pages} pages)")
        all_products = []
        
        for page in range(1, max_pages + 1):
            logger.info(f"Scraping page {page} of {max_pages}")
            
            # Add delay between page requests to avoid rate limiting
            if page > 1:
                sleep_time = random.uniform(2, 5)
                logger.debug(f"Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
            
            try:
                # Build the search URL with parameters
                params = {
                    "q": query,
                    "page": page,
                    "ref": "pagination",
                }
                
                search_url = f"{self.search_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
                
                # Load the page using Selenium
                self.driver.get(search_url)
                
                # Wait for product listings to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.wt-grid div.v2-listing-card"))
                )
                
                # Extract product data
                page_products = self._extract_search_results()
                
                if not page_products:
                    logger.warning(f"No products found on page {page}. Stopping search.")
                    break
                
                # Add position and page info
                for i, product in enumerate(page_products):
                    product["search_position"] = (page - 1) * len(page_products) + i + 1
                    product["search_page"] = page
                    product["search_query"] = query
                
                all_products.extend(page_products)
                
                logger.info(f"Found {len(page_products)} products on page {page}")
                
            except TimeoutException:
                logger.error(f"Timeout while loading page {page}")
                break
            except Exception as e:
                logger.error(f"Error scraping page {page}: {str(e)}")
                break
        
        logger.info(f"Total products found: {len(all_products)}")
        return all_products
    
    def _extract_search_results(self) -> List[Dict[str, Any]]:
        """Extract basic product data from search results page"""
        results = []
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        
        # Find all product listings
        product_cards = soup.select("div.wt-grid div.v2-listing-card")
        
        for card in product_cards:
            try:
                # Extract product URL
                link_elem = card.select_one("a.listing-link")
                if not link_elem:
                    continue
                
                product_url = link_elem.get("href", "")
                if not product_url.startswith("http"):
                    product_url = self.base_url + product_url if product_url.startswith("/") else f"{self.base_url}/{product_url}"
                
                # Extract product ID
                product_id = ""
                if "listing/" in product_url:
                    product_id = product_url.split("listing/")[1].split("/")[0]
                
                # Extract title
                title_elem = card.select_one("h3.v2-listing-card__title")
                title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
                
                # Extract price
                price_elem = card.select_one("span.currency-value")
                price = price_elem.get_text(strip=True) if price_elem else None
                
                currency_elem = card.select_one("span.currency-symbol")
                currency = currency_elem.get_text(strip=True) if currency_elem else "$"
                
                # Extract shop info
                shop_elem = card.select_one("p.v2-listing-card__shop")
                shop_name = shop_elem.get_text(strip=True) if shop_elem else "Unknown Shop"
                
                # Extract image URL
                img_elem = card.select_one("img.wt-width-full")
                img_url = img_elem.get("src", "") if img_elem else ""
                
                # Extract rating information
                rating_elem = card.select_one("span.stars-svg")
                rating = None
                if rating_elem:
                    rating_text = rating_elem.get("aria-label", "")
                    rating_match = re.search(r'(\d+(\.\d+)?)', rating_text)
                    if rating_match:
                        rating = float(rating_match.group(1))
                
                # Extract number of reviews
                reviews_elem = card.select_one("span.wt-text-caption.wt-text-gray")
                reviews_count = 0
                if reviews_elem:
                    reviews_text = reviews_elem.get_text(strip=True)
                    reviews_match = re.search(r'(\d+)', reviews_text)
                    if reviews_match:
                        reviews_count = int(reviews_match.group(1))
                
                # Build product data dictionary
                product_data = {
                    "product_id": product_id,
                    "title": title,
                    "price": price,
                    "currency": currency,
                    "shop_name": shop_name,
                    "rating": rating,
                    "reviews_count": reviews_count,
                    "product_url": product_url,
                    "image_url": img_url,
                    "scraped_at": datetime.now().isoformat(),
                }
                
                results.append(product_data)
                
            except Exception as e:
                logger.error(f"Error extracting product data: {str(e)}")
                continue
        
        return results
    
    def get_product_details(self, product_url: str) -> Dict[str, Any]:
        """
        Scrape detailed product information from product page
        
        Args:
            product_url: URL of the product page
            
        Returns:
            Dictionary with detailed product information
        """
        logger.info(f"Scraping product details: {product_url}")
        
        try:
            # Add random delay to avoid rate limiting
            sleep_time = random.uniform(1, 3)
            time.sleep(sleep_time)
            
            # Load the product page
            self.driver.get(product_url)
            
            # Wait for product details to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.wt-mb-xs-2"))
            )
            
            # Parse the page
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            
            # Extract product ID from URL
            product_id = ""
            if "listing/" in product_url:
                product_id = product_url.split("listing/")[1].split("/")[0]
            
            # Extract product title
            title_elem = soup.select_one("h1.wt-text-body-01")
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
            
            # Extract price
            price_elem = soup.select_one("p.wt-text-title-03 span.currency-value")
            price = price_elem.get_text(strip=True) if price_elem else None
            
            currency_elem = soup.select_one("p.wt-text-title-03 span.currency-symbol")
            currency = currency_elem.get_text(strip=True) if currency_elem else "$"
            
            # Extract description
            description = ""
            desc_iframe = self.driver.find_elements(By.CSS_SELECTOR, "iframe#listing-right-column-content")
            if desc_iframe:
                self.driver.switch_to.frame(desc_iframe[0])
                desc_elem = self.driver.find_element(By.CSS_SELECTOR, "div#description-text")
                description = desc_elem.text
                self.driver.switch_to.default_content()
            
            # Extract shop information
            shop_name_elem = soup.select_one("a.wt-text-link-no-underline span.wt-text-body-01")
            shop_name = shop_name_elem.get_text(strip=True) if shop_name_elem else "Unknown Shop"
            
            shop_url_elem = soup.select_one("a.wt-text-link-no-underline")
            shop_url = shop_url_elem.get("href", "") if shop_url_elem else ""
            if shop_url and not shop_url.startswith("http"):
                shop_url = self.base_url + shop_url if shop_url.startswith("/") else f"{self.base_url}/{shop_url}"
            
            # Extract images
            image_urls = []
            img_elems = soup.select("div.listing-page-image-carousel-component ul li img")
            for img in img_elems:
                src = img.get("src", "")
                if src and "il_75x75" in src:
                    # Convert thumbnail URL to full-size image URL
                    full_src = src.replace("il_75x75", "il_fullxfull")
                    image_urls.append(full_src)
            
            # Extract tags
            tags = []
            tag_elems = soup.select("div[data-selector='listing-page-attributes'] a[href^='/search?q=']")
            for tag_elem in tag_elems:
                tag = tag_elem.get_text(strip=True)
                if tag:
                    tags.append(tag)
            
            # Extract categories
            categories = []
            breadcrumb_elems = soup.select("ul.wt-breadcrumbs li a")
            for crumb in breadcrumb_elems:
                category = crumb.get_text(strip=True)
                if category and category != "Etsy":
                    categories.append(category)
            
            # Extract rating information
            rating = None
            rating_elem = soup.select_one("div.wt-display-flex-xs span.wt-screen-reader-only")
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'(\d+(\.\d+)?)', rating_text)
                if rating_match:
                    rating = float(rating_match.group(1))
            
            # Extract review count
            reviews_count = 0
            reviews_elem = soup.select_one("div.wt-display-flex-xs span.wt-text-body-01")
            if reviews_elem:
                reviews_text = reviews_elem.get_text(strip=True)
                reviews_match = re.search(r'(\d+)', reviews_text)
                if reviews_match:
                    reviews_count = int(reviews_match.group(1))
            
            # Extract shipping information
            shipping_info = {}
            shipping_elem = soup.select_one("div.wt-text-caption.shipping-costs")
            if shipping_elem:
                shipping_text = shipping_elem.get_text(strip=True)
                shipping_info["text"] = shipping_text
                
                # Extract shipping cost if available
                cost_match = re.search(r'(\d+(\.\d+)?)', shipping_text)
                if cost_match:
                    shipping_info["cost"] = float(cost_match.group(1))
            
            # Build product details dictionary
            product_details = {
                "product_id": product_id,
                "title": title,
                "description": description,
                "price": price,
                "currency": currency,
                "shop_name": shop_name,
                "shop_url": shop_url,
                "rating": rating,
                "reviews_count": reviews_count,
                "tags": tags,
                "categories": categories,
                "image_urls": image_urls,
                "shipping_info": shipping_info,
                "product_url": product_url,
                "scraped_at": datetime.now().isoformat(),
            }
            
            return product_details
            
        except TimeoutException:
            logger.error(f"Timeout while loading product page: {product_url}")
            return {"product_url": product_url, "error": "Timeout loading page"}
        except Exception as e:
            logger.error(f"Error scraping product details: {str(e)}")
            return {"product_url": product_url, "error": str(e)}
    
    def analyze_seo(self, product_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze SEO aspects of the product
        
        Args:
            product_details: Dictionary with product details
            
        Returns:
            Dictionary with SEO analysis results
        """
        seo_analysis = {
            "title_length": len(product_details.get("title", "")),
            "description_length": len(product_details.get("description", "")),
            "tag_count": len(product_details.get("tags", [])),
            "image_count": len(product_details.get("image_urls", [])),
            "has_categories": bool(product_details.get("categories", [])),
            "title_contains_keywords": [],
            "keyword_density": {},
            "seo_score": 0
        }
        
        # Check if title contains popular keywords
        title = product_details.get("title", "").lower()
        common_keywords = ["handmade", "custom", "personalized", "unique", "vintage", "gift", "sale"]
        
        for keyword in common_keywords:
            if keyword in title:
                seo_analysis["title_contains_keywords"].append(keyword)
        
        # Calculate keyword density
        if product_details.get("description"):
            description = product_details["description"].lower()
            words = re.findall(r'\b\w+\b', description)
            word_count = len(words)
            
            if word_count > 0:
                # Count word frequencies
                word_freq = {}
                for word in words:
                    if len(word) > 3:  # Only count words longer than 3 characters
                        word_freq[word] = word_freq.get(word, 0) + 1
                
                # Calculate density
                for word, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]:
                    density = (count / word_count) * 100
                    seo_analysis["keyword_density"][word] = {
                        "count": count,
                        "density": round(density, 2)
                    }
        
        # Calculate SEO score (simple heuristic)
        score = 0
        
        # Title length (ideal: 40-60 characters)
        title_length = seo_analysis["title_length"]
        if 40 <= title_length <= 60:
            score += 20
        elif 30 <= title_length < 40 or 60 < title_length <= 80:
            score += 15
        elif title_length > 0:
            score += 5
        
        # Description length (more is better, up to a point)
        desc_length = seo_analysis["description_length"]
        if desc_length >= 500:
            score += 20
        elif desc_length >= 300:
            score += 15
        elif desc_length >= 100:
            score += 10
        elif desc_length > 0:
            score += 5
        
        # Tags (ideal: 13 tags on Etsy)
        tag_count = seo_analysis["tag_count"]
        if tag_count >= 13:
            score += 20
        elif tag_count >= 10:
            score += 15
        elif tag_count >= 5:
            score += 10
        elif tag_count > 0:
            score += 5
        
        # Images (more is better, up to Etsy's max of 10)
        image_count = seo_analysis["image_count"]
        if image_count >= 10:
            score += 20
        elif image_count >= 7:
            score += 15
        elif image_count >= 4:
            score += 10
        elif image_count > 0:
            score += 5
        
        # Keywords in title
        score += min(len(seo_analysis["title_contains_keywords"]) * 5, 20)
        
        # Normalize score to 0-100
        seo_analysis["seo_score"] = min(score, 100)
        
        return seo_analysis
    
    def save_data(self, data: List[Dict[str, Any]], filename: str):
        """
        Save scraped data to JSON and CSV files
        
        Args:
            data: List of product dictionaries
            filename: Base filename to save data (without extension)
        """
        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{filename}_{timestamp}"
        
        # Save as JSON
        json_path = os.path.join(self.data_dir, f"{base_filename}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Save as CSV
        csv_path = os.path.join(self.data_dir, f"{base_filename}.csv")
        
        # Flatten the data for CSV export
        flattened_data = []
        for item in data:
            flat_item = {}
            for key, value in item.items():
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        flat_item[f"{key}_{subkey}"] = subvalue
                elif isinstance(value, list):
                    flat_item[key] = ", ".join(str(x) for x in value)
                else:
                    flat_item[key] = value
            flattened_data.append(flat_item)
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(flattened_data)
        df.to_csv(csv_path, index=False, encoding="utf-8")
        
        logger.info(f"Data saved to {json_path} and {csv_path}")
        
        return {
            "json_path": json_path,
            "csv_path": csv_path,
            "record_count": len(data)
        }
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Etsy SEO Data Scraper")
    
    parser.add_argument("--search", type=str, required=True, 
                        help="Search query for Etsy products")
    
    parser.add_argument("--pages", type=int, default=1, 
                        help="Number of search result pages to scrape (default: 1)")
    
    parser.add_argument("--detailed", action="store_true", 
                        help="Scrape detailed product information")
    
    parser.add_argument("--headless", action="store_true", default=True,
                        help="Run browser in headless mode (default: True)")
    
    parser.add_argument("--output", type=str, default="etsy_data",
                        help="Base filename for output data (default: etsy_data)")
    
    parser.add_argument("--proxy", action="store_true",
                        help="Use proxy servers for scraping")
    
    return parser.parse_args()


def main():
    """Main entry point for the Etsy scraper"""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Initialize scraper
    scraper = EtsyScraper(headless=args.headless, use_proxy=args.proxy)
    
    try:
        # Search for products
        logger.info(f"Starting Etsy scraper for query: {args.search}")
        products = scraper.search_products(args.search, args.pages)
        
        if not products:
            logger.error("No products found. Exiting.")
            return
        
        # Get detailed information if requested
        if args.detailed:
            logger.info("Scraping detailed product information...")
            detailed_products = []
            
            for i, product in enumerate(products):
                logger.info(f"Scraping details for product {i+1} of {len(products)}")
                product_url = product.get("product_url")
                
                if product_url:
                    # Get detailed product information
                    details = scraper.get_product_details(product_url)
                    
                    # Analyze SEO aspects
                    seo_analysis = scraper.analyze_seo(details)
                    
                    # Combine data
                    detailed_product = {**product, **details, "seo_analysis": seo_analysis}
                    detailed_products.append(detailed_product)
                    
                    # Add delay between requests
                    if i < len(products) - 1:
                        sleep_time = random.uniform(2, 5)
                        time.sleep(sleep_time)
            
            products = detailed_products
        
        # Save the data
        save_result = scraper.save_data(products, args.output)
        logger.info(f"Saved {save_result['record_count']} products to {save_result['json_path']}")
        
    except Exception as e:
        logger.error(f"Error in main scraper process: {str(e)}")
    finally:
        # Close the WebDriver
        scraper.close()
        logger.info("Scraper finished. Browser closed.")


if __name__ == "__main__":
    main()