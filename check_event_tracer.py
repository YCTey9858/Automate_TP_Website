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

    driver.get('https://partner.ipricegroup.com/admin/stats/event_tracer')

    username = input('Enter your username: ')
    password = input('Enter your password: ')
    driver.find_element(By.XPATH, '//*[@id="UserEmail"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="UserPassword"]').send_keys(password)

    driver.find_element(By.XPATH, '//*[@id="loginButton"]').click()

    time.sleep(5)

    driver.get('https://partner.ipricegroup.com/admin/stats/event_tracer')

    driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[3]/span/input').click()
    driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[4]/span/input').click()
    driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[5]/span/input').click()
    driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[6]/span/input').click()
    driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[7]/span/input').click()
    driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[2]/div[2]/div/ul/li[8]/span/input').click()

    driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[4]/div[2]/div/ul/li[3]/span/input').click()
    driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[4]/div[2]/div/ul/li[4]/span/input').click()
    driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[4]/div[2]/div/ul/li[5]/span/input').click()
    driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[4]/div[2]/div/ul/li[6]/span/input').click()
    driver.find_element(By.XPATH, '//*[@id="qed"]/div/div/div[1]/div/div/div[1]/form/div[2]/div[2]/div/ul/div[4]/div[2]/div/ul/li[7]/span/input').click()

    driver.find_element(By.XPATH, '//*[@id="run-eventLog"]').click()

    driver.find_element(By.XPATH, '//*[@id="export-eventLog"]').click()

    print(driver.page_source)