from selenium import webdriver
from selenium.webdriver.common.by import By


def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)


def get_country_data(driver, url):
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
    # url = "https://www.iso.org/obp/ui/#iso:pub:PUB500001:en"  # List of countries (3166-1)
    url = "https://www.iso.org/obp/ui/#iso:code:3166:US"    # List of subdivisions within a country (3166-2)

    with initialize_driver() as driver:
        summary, info, subdivisions = get_country_data(driver, url)
        title = driver.title

    print(f'{len(subdivisions)} ISO 3166-2 Subdivisions in "{title}"')

    """
    for v in summary:
        assert len(v) == 2
        print(f'{v[0]:>25}: {v[1]}')

    print('\nAdditional Info:')
    for v in info:
        assert len(v) == 3
        print(f'  {v}')
    """
    for n, s in enumerate(subdivisions, start=1):
        print(f'{n:>4} {s}')


if __name__ == "__main__":
    main()