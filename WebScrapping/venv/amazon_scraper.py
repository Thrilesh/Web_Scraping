import requests
from bs4 import BeautifulSoup
import csv

# Scrape product details from a given URL
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_url = url
    product_name = soup.select_one('span.a-size-medium.a-color-base.a-text-normal').get_text(strip=True)
    product_price = soup.select_one('span.a-offscreen').get_text(strip=True)
    rating = soup.select_one('span.a-icon-alt').get_text(strip=True)
    num_reviews = soup.select_one('span.a-size-base').get_text(strip=True)

    return product_url, product_name, product_price, rating, num_reviews

# Scrape additional details from a given product URL
def scrape_additional_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    asin_element = soup.select_one('th:contains("ASIN") + td')
    asin = asin_element.get_text(strip=True) if asin_element else None
    description_element = soup.select_one('th:contains("Product Dimensions") + td')
    description = description_element.get_text(strip=True) if description_element else None
    product_description = soup.select_one('div#productDescription').get_text(strip=True)
    manufacturer_element = soup.select_one('th:contains("Manufacturer") + td')
    manufacturer = manufacturer_element.get_text(strip=True) if manufacturer_element else None


    return asin, description, product_description, manufacturer

# Scrape multiple pages of product listings
def scrape_multiple_pages(num_pages):
    all_products = []

    for page in range(1, num_pages+1):
        url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        product_links = soup.select('.s-result-item .a-link-normal.a-text-normal')
        for link in product_links:
            product_url = 'https://www.amazon.in' + link['href']
            product_details = scrape_product_details(product_url)
            all_products.append(product_details)

    return all_products

# Scrape all product details and additional details
def scrape_all_data(num_pages, num_products):
    product_list = scrape_multiple_pages(num_pages)
    product_data = []

    for i, product in enumerate(product_list[:num_products]):
        product_url = product[0]
        additional_details = scrape_additional_details(product_url)
        product_data.append(product + additional_details)

    return product_data

# Export scraped data to a CSV file
def export_to_csv(product_data):
    with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'ASIN', 'Description', 'Product Description', 'Manufacturer'])
        writer.writerows(product_data)

# Main program
num_pages_to_scrape = 20
num_products_to_fetch = 200

data = scrape_all_data(num_pages_to_scrape, num_products_to_fetch)
export_to_csv(data)
