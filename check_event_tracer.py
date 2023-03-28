from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from fuzzywuzzy import fuzz


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
    # driver = start_driver()
    #
    # driver.get('https://partner.ipricegroup.com/admin/stats/event_tracer')
    # time.sleep(5)

    # Login
    # username = input('Enter your username: ')
    # password = input('Enter your password: ')
    # username = 'yi.chuan@ipricegroup.com'
    # password = '@@Iprice2023'
    # driver.find_element(By.XPATH, '//*[@id="UserEmail"]').send_keys(username)
    # driver.find_element(By.XPATH, '//*[@id="UserPassword"]').send_keys(password)
    #
    # driver.find_element(By.XPATH, '//*[@id="loginButton"]').click()
    #
    # time.sleep(5)
    #
    # # Event Tracer
    # driver.get('https://partner.ipricegroup.com/admin/stats/event_tracer')
    #
    # time.sleep(15)
    # # Select Partner
    # driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]').click()
    # time.sleep(2)
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[1]/div[1]').click()
    # time.sleep(2)
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[3]/span/input').click()
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[4]/span/input').click()
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[5]/span/input').click()
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[6]/span/input').click()
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[7]/span/input').click()
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[8]/span/input').click()
    #
    # # Select Advertiser
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[4]/div[1]/div[1]').click()
    # time.sleep(2)
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[4]/div[2]/div/ul/li[3]/span/input').click()
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[4]/div[2]/div/ul/li[4]/span/input').click()
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[4]/div[2]/div/ul/li[5]/span/input').click()
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[4]/div[2]/div/ul/li[6]/span/input').click()
    # driver.find_element(By.XPATH,
    #                     '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[4]/div[2]/div/ul/li[7]/span/input').click()
    #
    # driver.find_element(By.XPATH,)
    # # Run Event Tracer
    # driver.find_element(By.XPATH, '//*[@id="run-eventLog"]').click()
    #
    # # Export Event Tracer
    # driver.find_element(By.XPATH, '//*[@id="export-eventLog"]').send_keys(Keys.ENTER)

    # Find the Event Tracer Download Path
    event_tracer_file = input('Enter the event tracer file path: ')
    event_tracer = pd.read_csv(event_tracer_file)
    match_type = input('Enter the match type (1,2,3): '
                       '1. IG source'
                       '2. Product Name'
                       '3. Purchase Date')
    if match_type == '1':
        igsource = input('Enter the igsource (If Cant get then skip this): ')
        event_tracer['Match'] = event_tracer['igsource'].str.contains(igsource)
    elif match_type == '2':
        product_name = input('Enter the product name: ')
        event_tracer = event_tracer[event_tracer['product_name'] == product_name]
    elif match_type == '3':
        purchase_date = input('Enter the purchase date: ')
