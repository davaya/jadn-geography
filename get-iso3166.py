import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


def initialize_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless=new')      # Comment out to see what's happening
    options.add_argument('--disable-gpu')       # Not needed, reduce dependencies
    return webdriver.Chrome(options=options)


def get_country_codes(driver, url) -> list[list[str]]:
    """
    Retrieve ISO 3166-1 Country Code info from Online Browsing Platform

    :returns: Table of country names and codes, first row = column names
    """
    driver.implicitly_wait(15)
    driver.get(url)
    driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()    # Get rid of cookie blocking popup

    e_pages = driver.find_elements(By.CLASS_NAME, 'v-radiobutton')    # Navigate to country codes pages
    pg = {p.find_element(By.TAG_NAME, 'label').text.lower().strip(): p.find_element(By.TAG_NAME, 'input') for p in e_pages}
    pg['country codes'].click()     # Select "Country codes"
    driver.find_element(By.CLASS_NAME, 'v-button-go').find_element(By.CLASS_NAME, 'v-button-caption').click() # SEARCH

    e_page = driver.find_element(By.CLASS_NAME, 'search-result-layout')
    soup = BeautifulSoup(e_page.find_element(By.TAG_NAME, 'thead').get_attribute('innerHTML'), 'html.parser')
    codes = [[v.text for v in soup.find_all('th')]]
    while True:
        print('.', end='')
        e_page = driver.find_element(By.CLASS_NAME, 'search-result-layout')
        page = e_page.find_element(By.TAG_NAME, 'tbody').get_attribute('innerHTML')
        for row in BeautifulSoup(page, 'html.parser').find_all('tr'):
            codes.append([v.text for v in row])
        last = e_page.find_element(By.CLASS_NAME, 'paging-align-fix').find_elements(By.CLASS_NAME, 'v-button')[-1].get_attribute('tabindex')
        if last != '0':
            break
        e_page.find_element(By.CLASS_NAME, 'last').click()    # Go to next page
        sleep(1)
    driver.quit()
    print(f'\n{len(codes)}')
    return codes


def get_countries(driver, url):
    """
    Retrieve Country selection grid from ISO Online Browsing Platform

    Warning!: Very slow and puts an abnormal load on server intended for manual selection.
    Run only once and save data in JSON format for offline processing later.

    :param driver: Selenium WebDriver for headless browser
    :param url:
    :returns: Table of [Alpha-2 country code, Status Category (1-7), Subdivision URL]
    """
    driver.implicitly_wait(5)
    driver.get(url)
    countries = []
    grid = driver.find_element(By.CLASS_NAME, 'grs-grid')
    for n, row in enumerate(grid.find_elements(By.TAG_NAME, 'tr'), start=1):
        print(f'{n:>3} ', end='')
        for col in row.find_elements(By.TAG_NAME, 'td'):
            print('.', end='')
            links = col.find_elements(By.XPATH, './child::*')
            assert len(links) <= 1
            link = links[0].get_attribute('href') if links else ''
            countries.append([col.text, col.get_attribute('class'), link])
        print()
    return countries

def get_country_data(driver, url):
    """
    Retrieve an ISO 3166-2 Subdivision list and additional Country info from Online Browsing Platform

    :param driver: Selenium WebDriver for headless browser
    :param url: ISO Online Browsing Platform URL for selected country
    :returns: ISO 3166-2 Subdivision list for selected country
    """
    driver.implicitly_wait(5)
    driver.get(url)
    summary = []
    for line in driver.find_elements(By.CLASS_NAME, "core-view-line"):
        summary.append([v.text for v in line.find_elements(By.XPATH, './/*')])

    inf = driver.find_element(By.ID, 'country-additional-info')
    info = [[v.text for v in inf.find_elements(By.TAG_NAME, 'th')]]
    body = inf.find_element(By.TAG_NAME,'tbody')
    for e in body.find_elements(By.TAG_NAME, 'tr'):
        info.append([v.text for v in e.find_elements(By.TAG_NAME, 'td')])

    sub = driver.find_element(By.ID, "subdivision")
    subdivisions = [[v.text for v in sub.find_elements(By.TAG_NAME, 'th')]]
    body = sub.find_element(By.TAG_NAME,'tbody')
    for e in body.find_elements(By.TAG_NAME, 'tr'):
        subdivisions.append([v.text for v in e.find_elements(By.TAG_NAME, 'td')])

    # X.find_elements(By.XPATH, './/*')         # recursive
    # X.find_elements(By.XPATH, './child::*')   # first level
    # Y = BeautifulSoup(X.get_attribute('outerHTML'), features='html.parser')

    return summary, info, subdivisions


def main():
    url_0 = "https://www.iso.org/obp/ui/#search"    # ISO 3166-1 country codes (paged)
    url_1 = "https://www.iso.org/obp/ui/#iso:pub:PUB500001:en"  # Grid of individual country pages
    url_2 = "https://www.iso.org/obp/ui/#iso:code:3166:US"    # List of subdivisions within a country (3166-2)

    with initialize_driver() as driver:
        codes = get_country_codes(driver, url_0)
        # countries = get_countries(driver, url_1)
        # summary, info, subdivisions = get_country_data(driver, url_2)
        # title = driver.title
        # print(f'{len(subdivisions)} ISO 3166-2 Subdivisions in "{title}"')

    os.makedirs('out', exist_ok=True)
    with open('out/codes.json', 'w', encoding='utf8') as fp:
        json.dump(codes, fp)

    """
    for v in summary:
        assert len(v) == 2
        print(f'{v[0]:>25}: {v[1]}')

    print('\nAdditional Info:')
    for v in info:
        assert len(v) == 3
        print(f'  {v}')
    """
    # for n, s in enumerate(subdivisions, start=1):
    #    print(f'{n:>4} {s}')


if __name__ == "__main__":
    main()