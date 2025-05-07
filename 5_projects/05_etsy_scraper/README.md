# Etsy SEO Data Scraper

A web scraping tool for extracting product SEO data from Etsy. This tool helps you analyze SEO aspects of Etsy listings including titles, descriptions, tags, categories, and more.

## Features

- **Basic Search Scraping:** Extract product listings from Etsy search results
- **Detailed Product Analysis:** Collect complete product information including descriptions and tags
- **SEO Analysis:** Calculate SEO scores based on various factors like title length, tag count, etc.
- **Keyword Density:** Analyze keyword usage in product descriptions
- **Data Export:** Save results in both JSON and CSV formats

## Requirements

- Python 3.7+
- Chrome browser installed
- Required Python packages (see requirements.txt)

## Installation

1. Clone or download this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Make sure you have Chrome browser installed (needed for Selenium)

## Usage

Basic usage with the command line interface:

```bash
# Search for products and collect basic information
python etsy_scraper.py --search "handmade jewelry" --pages 2

# Collect detailed product information including SEO data
python etsy_scraper.py --search "handmade jewelry" --pages 2 --detailed

# Run without headless mode (shows browser window)
python etsy_scraper.py --search "wood crafts" --pages 1 --detailed --headless False

# Save results with a custom filename
python etsy_scraper.py --search "vintage clothing" --pages 3 --output vintage_results
```

### Command Line Arguments

- `--search`: Search query for Etsy products (required)
- `--pages`: Number of search result pages to scrape (default: 1)
- `--detailed`: Scrape detailed product information and SEO data
- `--headless`: Run browser in headless mode (default: True)
- `--output`: Base filename for output data (default: etsy_data)
- `--proxy`: Use proxy servers for scraping (requires proxies.txt file or PROXY_LIST env var)

## Output Data

The scraped data is saved in the `data` directory in both JSON and CSV formats with timestamps:

```
data/
  ├── etsy_data_20250507_123045.json
  └── etsy_data_20250507_123045.csv
```

### Data Fields

Basic product data includes:
- Product ID
- Title
- Price and currency
- Shop name
- Rating and review count
- Product URL
- Search position

Detailed product data (with `--detailed` flag) also includes:
- Description
- Tags and categories
- Shop URL
- Image URLs
- Shipping information
- SEO analysis
  - Title and description length
  - Tag and image count
  - Keyword density
  - SEO score

## Using Proxies (Optional)

To use proxy servers for scraping (recommended for large scrapes):

1. Create a file named `proxies.txt` with one proxy per line in format `ip:port`
2. Alternatively, set the `PROXY_LIST` environment variable with comma-separated proxies

## Tips for Effective Scraping

- Be respectful of Etsy's servers and don't make too many requests too quickly
- For large scrapes, use the `--proxy` option with a list of rotating proxies
- Use specific search terms to get more relevant results
- The `--detailed` flag provides much more SEO data but takes longer to run

## Legal Disclaimer

This scraper is provided for educational purposes only. Be sure to review and comply with Etsy's Terms of Service when using this tool. The authors are not responsible for any misuse of this software.