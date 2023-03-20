from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

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

    target_price = input('What is your target price: ')

    df = pd.DataFrame(columns=['Item Name', 'Item Price', 'Category'])

    if category == 'all':
        if country == 'Singapore':
            category_file = 'iprice_sg.txt'
            currency = 'S$'
        elif country == 'Malaysia':
            category_file = 'iprice_my.txt'
            currency = 'RM'
        elif country == 'Indonesia':
            category_file = 'iprice_id.txt'
            currency = 'Rp'
        elif country == 'Thailand':
            category_file = 'iprice_th.txt'
            currency = 'บาท'
        elif country == 'Philippines':
            category_file = 'iprice_ph.txt'
            currency = '₱'
        elif country == 'Vietnam':
            category_file = 'iprice_vn.txt'
            currency = 'đ'
        elif country == 'Hong Kong':
            category_file = 'iprice_hk.txt'
            currency = 'HK$'

        # opening the text file
        target_file = open(category_file, "r")
        data = target_file.read()
        data_into_list = data.split("\n")
        print(data_into_list)
        target_file.close()

        i = 0
        # Loop through each category
        for category in data_into_list:
            i += 1
            full_url = country_list[country] + category + '/?store=' + store + '&sort=price.net_asc'
            driver.get(full_url)
            time.sleep(2)
            try:
                element = driver.find_element(By.CSS_SELECTOR, 'a[data-ga-trigger="ga-conversion"]')
                item_name = element.find_element(By.CSS_SELECTOR, 'h3').text
                item_price = element.find_element(By.XPATH, 'div[1]/div[1]/div').text
                print(item_name + ' ' + item_price + ' ' + category)
            except:
                item_name = None
                item_price = None
                print(category + ' is empty or are PDP')

            df = df.append({'Item Name': item_name, 'Item Price': item_price, 'Category': category}, ignore_index=True)
            try:
                price = item_price.replace(currency, '')
                price = price.replace(',', '')
                if float(price) < float(target_price):
                    break
                else:
                    print(category + '\'s higher than expected ')
            except:
                print(category + ' is empty or are PDP')
            print(i)
        # Save to csv
        df.to_csv('iprice_' + country + '.csv', index=False)

    # If user only want to search for one category
    else:
        full_url = country_list[country] + category + '/?store=' + store + '&sort=price.net_asc'
        driver.get(full_url)
        try:
            element = driver.find_element(By.CSS_SELECTOR, 'a[data-ga-trigger="ga-conversion"]')
            item_name = element.find_element(By.CSS_SELECTOR, 'h3').text
            item_price = element.find_element(By.XPATH, 'div[1]/div[1]/div').text
        except:
            item_name = None
            item_price = None

        # Append to dataframe
        df = df.append({'Item Name': item_name, 'Item Price': item_price, 'Category': category}, ignore_index=True)

        # Save to csv
        df.to_csv('iprice_' + country + '.csv', index=False)

    driver.quit()
