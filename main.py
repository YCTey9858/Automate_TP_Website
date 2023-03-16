import os
from dotenv import load_dotenv
# from seleniumwire import webdriver
# from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import random


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
    options.add_argument('--allow-running-insecure-content')

    # options.add_argument(r"--user-data-dir=/Users/yichuantey/Library/Application Support/Google/Chrome")
    # options.add_argument(r"--profile-directory=Profile 1")
    driver = Chrome(options=options)
    return driver


def enable_vpn(driver):
    # Step 1: Open ExpressVPN login page, login and turn on the VPN.
    driver.get('https://www.expressvpn.com/sign-in')
    time.sleep(2)  # Wait for the page to load

    # Replace the code below with your specific login and VPN connection process
    # For example:
    driver.find_element(By.CSS_SELECTOR, '#email').send_keys(os.getenv('EXPRESS_VPN'))
    driver.find_element(By.CSS_SELECTOR, '#password').send_keys(os.getenv('EXPRESS_VPN_PASSWORD'))
    time.sleep(2)  # Wait for the page to load
    driver.find_element(By.CSS_SELECTOR, 'input[name=commit]').click()
    time.sleep(2)  # Wait for the page to load
    driver.find_element(By.CSS_SELECTOR, '#country-selector').click()
    driver.find_element(By.CSS_SELECTOR, '.country-option[data-country="United States"]').click()
    driver.find_element(By.CSS_SELECTOR, '#connect-button').click()


# def start_recording():

def clear_cache(driver):
    # Step 3: Open Chrome and clear the cache.
    driver.get('chrome://settings/clearBrowserData')
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, 'body').send_keys('\ue007')
    time.sleep(3)
    print("Cleared cache")


def iprice_website(driver, tp_wesbite):
    # Step 2: Open the website and perform the action.
    detail = {}

    # Step 2.1: Open the website and perform the action.
    driver.get(tp_wesbite)
    time.sleep(5)

    # Step 2.2: Click on the first product
    start_catch = datetime.now()
    driver.find_element(By.CSS_SELECTOR, 'a[data-ga-trigger="ga-conversion"]').click()
    print("Click on the first product")
    time.sleep(10)

    # Step 2.3: Switch to the second tab#
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])
    time.sleep(5)
    print("Switch to the second tab")

    # If the redirection happened before the robot know
    try:
        driver.find_element(By.CSS_SELECTOR, 'div[class="redirect"]').click()
        print("Click on the redirect button")
    except:
        print("Auto redirect")

    end_catch = datetime.now()
    # redirection_urls = extract_url(driver, start_catch, end_catch)
    current_url = driver.current_url

    # Step 2.4: Catch the request
    start_save = False
    list = []
    for request in driver.requests:
        if request.response and start_catch < request.response.date < end_catch:
            if request.url.__contains__("ipricegroup.go2cloud.org"):
                start_save = True
            if start_save:
                list.append(
                    {'url': request.url,
                     'status': request.response.status_code,
                     'content': request.response.headers['Content-Type']
                     })
            if request.url == current_url:
                break
    print("Done Catching")

    # Step 2.5: Extract the information
    ig_Source = extract_information(list)
    detail['IG'] = ig_Source
    print("IG Source is " + ig_Source)

    aff_id = extract_information(list, start_str="&aff_id")
    detail['Affiliate ID'] = aff_id
    print("Affiliate ID is " + aff_id)
    time.sleep(10)

    # Step 2.6: Click on the Buy Now button
    try:
        # driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[20]/div/div[1]/div/section/div/div/section/div/button[3]').click()
        driver.find_element(By.XPATH, "//button[@class='blu-btn b-primary btn-checkout']").click()
        print("Click on the Buy Now button")
        time.sleep(15)
    except:
        pass

    # Step 2.7: Click on the Checkout button
    try:
        # driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[20]/div/div[1]/div/section/div/div/div[4]/div[1]/div[1]/div/div/div[6]/button').click()
        driver.find_element(By.XPATH, "//button[@class='blu-btn b-icon b-primary add-btn mode-small']").click()
        print("Click on the Checkout button")
        time.sleep(10)
    except:
        pass

    # Step 2.8: Click on the Login button (Google)
    try:
        print("Start Login")
        driver.find_element(By.XPATH, "//div[@class='login__third-party-google']").click()
        driver.switch_to.window(driver.window_handles[2])
        time.sleep(10)

        driver.find_element(By.XPATH, '//*[@id="credentials-picker"]/div[1]').click()
        print("Click on the Google Account")
        time.sleep(10)

        driver.switch_to.window(driver.window_handles[1])
    except:
        print("Already Login")

    # Step 2.9: Bypass phone number checkup
    try:
        driver.find_element(By.XPATH, "//button[@class='blu-btn footer__btn b-ghost b-secondary']").click()
        print("Click on the phone number checkup")
        time.sleep(10)
    except:
        pass

    # Step 2.10: Click on the Beli Now button
    try:
        driver.find_element(By.XPATH, "//button[@class='blu-btn b-primary btn-checkout']").click()
        print("Click on the Beli Now button")
        time.sleep(10)
    except:
        pass

    # Step 2.11: Extract the item name
    try:
        item_name = driver.find_element(By.XPATH,
                                        '//*[@id="pdp-gateway"]/div/div[4]/div[1]/div[1]/div/div/div[1]/span[1]').text
        print("Item Name: " + item_name)
        detail['Item Name'] = item_name
        time.sleep(10)
    except:
        pass

    # Step 2.12: Click on the Checkout button
    try:
        driver.find_element(By.XPATH, "//button[@class='blu-btn b-icon b-primary add-btn mode-small']").click()
        print("Click on the Checkout button")
        time.sleep(10)
    except:
        pass

    # Step 2.13: Phone number check up
    try:
        ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, 'button')).click(driver.find_element(By.CSS_SELECTOR, 'button')).perform()
        print("Phone number check up")
        time.sleep(10)
    except:
        pass

    # Step 2.13: Click on the Final Checkout Button at review page
    try:
        driver.find_element(By.XPATH, "//button[@class='blu-btn checkout-button b-primary next-btn']").click()
        print("Click on the Final Checkout Button at review page")
        time.sleep(10)
    except:
        pass

    # Step 2.13: Click on the Pay now button
    try:
        driver.find_element(By.XPATH, '//*[@id="step2_gdn-order-summary-div"]/div[2]/div/div[2]').click()
        print("Pay now")
        time.sleep(10)
    except:
        pass

    # Step 2.14: Extract the order information
    item_name = driver.find_element(By.XPATH, '//*[@id="blibli-main-ctrl"]/section/div/div/div[1]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div/div/div[1]').text
    print("Item Name: ", item_name)
    detail['Item Name'] = item_name

    order_id = driver.find_element(By.XPATH, '//div[@class="payment-info-button__label-subtitle"]').text
    print("Order ID: ", order_id)
    detail['Order ID'] = order_id

    total_payment = driver.find_element(By.XPATH, '//span[@class="payment-detail__summary--total-value"]').text
    print("Total Payment: ", total_payment)
    detail['Total Payment'] = total_payment

    order_date = driver.find_element(By.XPATH, '//span[@class="order-detail__header-date"]').text
    print("Order Date: ", order_date)
    detail['Order Date'] = order_date
    return detail


def click_button(driver, condition, pointer):
    driver.find_element(condition, pointer).click()
    time.sleep(5)
    return driver


def switch_tab(driver, tab_number):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tab_number])
    time.sleep(5)
    print("Number of tabs: ", len(tabs))
    return driver


def extract_information(data, start_str="=ig"):
    # Step 4: Open the website and perform the action.
    redirection_url = data[0]['url']

    # find a substring start from text wanted to &
    start_pointer = redirection_url.find(start_str)
    end_pointer = redirection_url.find("&", start_pointer + 1)
    content = redirection_url[start_pointer + 1:end_pointer]
    return content


def extract_url(driver, start_time=None, end_time=None):
    list = []
    for request in driver.requests:
        if request.response and start_time < request.response.date < end_time:
            list.append(
                {'url': request.url,
                 'status': request.response.status_code,
                 'content': request.response.headers['Content-Type']
                 })
    return list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    record = {'tp_acc': 'tpid2021@gmail.com', 'tp_pass': '@Testingid2021', 'Payment method': 'Pay at Store'}

    load_dotenv()
    driver = start_driver()
    # enable_vpn(driver)

    # clear_cache(driver)
    driver.get('https://accounts.google.com/signin/chrome/sync/identifier?ssp=1&continue=https%3A%2F%2Fwww.google.com%2F&flowName=GlifDesktopChromeSync')
    time.sleep(30)
    example_link = "https://iprice.co.id/perhiasan/?store=blibli&sort=price.net_asc"
    detail_record = iprice_website(driver, example_link)
    full_record = {**record, **detail_record}

    time.sleep(60)

    driver.quit()
    print('Done')

