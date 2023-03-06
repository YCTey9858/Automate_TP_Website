from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def start_driver():
    options = ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    # chrome_options.add_argument('--headless')
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
               'Thailand': 'https://www.iprice.co.th/', 'Philippines': 'https://www.iprice.ph/', 'Vietnam': 'https://www.iprice.vn/',
               'Hong Kong': 'https://www.iprice.hk/'}

    category = input('Which category you want: '
                     'If you want to search for all categories, please enter "all": ')

    country
    store = input('Which store you want: ')

    # if category == 'all':
    if category == 'all':
        if country == 'Singapore':
            category = ["computers", "mobile-phones", "cameras", "tv-audio-video", "home-appliances", "health-beauty", "watches",]
        elif country == 'Malaysia':
            pass
        elif country == 'Indonesia':
            pass
        elif country == 'Thailand':
            pass
        elif country == 'Philippines':
            pass
        elif country == 'Vietnam':
            pass
        elif country == 'Hong Kong':
            pass
    # else:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
    full_url = country_list[country] + '/' + category + '/?store=' + store + '&sort=price.net_asc'
    driver.get(full_url)
    time.sleep(60)


