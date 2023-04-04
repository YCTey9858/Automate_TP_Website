"""
This script is to find the cheapest product in one or more category in a country in a store

How to use:
1. Run the script
2. Enter the country
3. Enter the category
4. Enter the store
5. Enter the price threshold
6. The script will show the cheapest product in the target category in the target store.
7. The script will also save the result to cheapest_product.csv

Potential Error:
1. No product found (url problem): check the category and store
2. No product found: check if the page doesn't contain any direct product
3. Package not found: check the package name and reinstall the package
4. Chrome driver not found: check the chrome driver version and download the correct version
5. No such element: check the xpath
6. URL not found: check the url, potentially country problem
7. Open file error: check the missing file path of category
"""
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import time
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def start_driver():
    """
    Start the selenium driver
    """
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

    # Country Selection
    country = input('Which country you want: '
                    'Singapore, Malaysia, Indonesia, Philippines, Vietnam, Hong Kong: ')

    # iPrice Country URL
    country_list = {'Singapore': 'https://www.iprice.sg/', 'Malaysia': 'https://www.iprice.my/',
                    'Indonesia': 'https://www.iprice.co.id/',
                    'Thailand': 'https://ipricethailand.com/', 'Philippines': 'https://www.iprice.ph/',
                    'Vietnam': 'https://www.iprice.vn/',
                    'Hong Kong': 'https://www.iprice.hk/'}

    # Category Selection find you category in iprice_sg.txt, iprice_my.txt, iprice_id.txt, iprice_ph.txt,
    # iprice_vn.txt, iprice_hk.txt or directly in the website url
    category = input('Which category you want: ')

    # Store Selection find your store in the website url
    store = input('Which store you want: ')

    # Target Price
    target_price = input('What is your target price: ')

    df = pd.DataFrame(columns=['Item Name', 'Item Price', 'Category'])

    # If category is all, the script will run through all the categories
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
        print("Total number of categories: ", len(data_into_list))
        target_file.close()

        i = 0
        # Loop through each category
        for category in data_into_list:
            i += 1

            # Form the url
            full_url = country_list[country] + category + '/?store=' + store + '&sort=price.net_asc'
            # Go to the url
            driver.get(full_url)
            time.sleep(1)

            # Find the cheapest product, if there is no product, the script will skip the category
            try:
                element = driver.find_element(By.CSS_SELECTOR, 'a[data-ga-trigger="ga-conversion"]')
                item_name = element.find_element(By.CSS_SELECTOR, 'h3').text
                item_price = element.find_element(By.XPATH, 'div[1]/div[1]/div').text
                print(item_name + ' ' + item_price + ' ' + category)
            except:
                item_name = None
                item_price = None
                print(category + ' is empty or are PDP')

            # Append the result to the dataframe
            df = df.append({'Item Name': item_name, 'Item Price': item_price, 'Category': category}, ignore_index=True)

            # Check if the price is lower than the target price, if yes, the script will stop
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
        # Form the url
        full_url = country_list[country] + category + '/?store=' + store + '&sort=price.net_asc'
        # Go to the url
        driver.get(full_url)
        # Find the cheapest product
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
