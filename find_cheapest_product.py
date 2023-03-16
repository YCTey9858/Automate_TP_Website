from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def start_driver():
    options = ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    driver = Chrome(options=options)
    return driver

if __name__ == '__main__':
    driver = start_driver()
    country = input('Which country you want: '
                    'Singapore, Malaysia, Indonesia, Thailand, Philippines, Vietnam, Hong Kong: ')

    # iPrice Country URL
    country_list = {'Singapore': 'https://www.iprice.sg/', 'Malaysia': 'https://www.iprice.my/', 'Indonesia': 'https://www.iprice.co.id/',
               'Thailand': 'https://ipricethailand.com/', 'Philippines': 'https://www.iprice.ph/', 'Vietnam': 'https://www.iprice.vn/',
               'Hong Kong': 'https://www.iprice.hk/'}

    category = input('Which category you want: ')

    store = input('Which store you want: ')

    if category == 'all':
        if country == 'Singapore':
            category_file = 'iprice_sg.txt'
        elif country == 'Malaysia':
            category_file = 'iprice_my.txt'
        elif country == 'Indonesia':
            category_file = 'iprice_id.txt'
        elif country == 'Thailand':
            category_file = 'iprice_th.txt'
        elif country == 'Philippines':
            category_file = 'iprice_ph.txt'
        elif country == 'Vietnam':
            category_file = 'iprice_vn.txt'
        elif country == 'Hong Kong':
            category_file = 'iprice_hk.txt'

        # opening the text file
        target_file = open(category_file, "r")
        data = target_file.read()
        data_into_list = data.split("\n")
        print(data_into_list)
        target_file.close()
        for category in data_into_list:
            full_url = country_list[country] + '/' + category + '/?store=' + store + '&sort=price.net_asc'
            driver.get(full_url)
    else:
        full_url = country_list[country] + '/' + category + '/?store=' + store + '&sort=price.net_asc'
        driver.get(full_url)
        time.sleep(60)
