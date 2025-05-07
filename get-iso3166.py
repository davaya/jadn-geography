from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# import pandas as pd
# import html
# import datetime


def initialize_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)


def get_product_data(driver, url):
    driver.implicitly_wait(5)
    driver.get(url)
    header = driver.find_element(By.CLASS_NAME, "core-view-header")
    hsoup = BeautifulSoup(header.get_attribute('outerHTML'))
    # he = header.find_elements(By.XPATH, './/*')   # recursive
    # he = header.find_elements(By.XPATH, './child::*')   # first level
    print(f'header "{driver.title}"')
    content = driver.find_element(By.ID, "country-additional-info")
    csoup = BeautifulSoup(content.get_attribute('outerHTML'), features="html.parser")

"""
    products, prices, currencies, ratings = [], [], [], []

    for a in soup.findAll('a', href=True, attrs={'class': 'ratio-box product-link'}):
        name = a.find('h4', attrs={'class': 'name'})
        price = a.find('div', attrs={'class': 'price'})
        currency, amount = html.unescape(price.text).split()
        rating = a.find('span', attrs={'class': 'product-rating-count'})

        prices.append(amount.strip())
        currencies.append(currency.strip())
        products.append(name.text.strip())
        ratings.append(rating.text.strip().strip('()'))

    return products, prices, currencies, ratings
"""

def main():
    # url = "https://uae.sharafdg.com/c/computing/laptops/macbooks/"
    # url = "https://www.iso.org/obp/ui/#iso:pub:PUB500001:en"
    url = "https://www.iso.org/obp/ui/#iso:code:3166:US"

    with initialize_driver() as driver:
        products, prices, currencies, ratings = get_product_data(driver, url)

"""
        df = pd.DataFrame({
            'Product Name': products,
            'Price': prices,
            'Currency': currencies,
            'Rating': ratings
        })

        print(f'dataframe')

        current_date = datetime.date.today()
        df['year'] = current_date.year
        df['month'] = current_date.month

        df.to_csv('products.csv', index=False, encoding='utf-8')
        df.to_parquet('data.parquet', engine='pyarrow',
                      partition_cols=['year', 'month'])
"""

if __name__ == "__main__":
    main()