import os
from dotenv import load_dotenv
# from seleniumwire import webdriver
# from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
import time
from datetime import datetime


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
    driver.get(tp_wesbite)
    time.sleep(5)

    start_catch = datetime.now()
    driver.find_element(By.CSS_SELECTOR, 'a[data-ga-trigger="ga-conversion"]').click()
    print("Click on the first product")
    time.sleep(5)

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

    print("IG Source")
    print(extract_information(list))

    print("Affiliate Source")
    print(extract_information(list, start_str="&aff_id"))

    time.sleep(10)
    print("Click on the Buy Now button")
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[20]/div/div[1]/div/section/div/div/section/div/button[3]').click()
    time.sleep(2)

    print("Click on the Checkout button")
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div[20]/div/div[1]/div/section/div/div/div[4]/div[1]/div[1]/div/div/div[6]/button').click()
    time.sleep(2)


    print("Start Login")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[19]/div/div[1]/div/section/div/div/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/input").send_keys("tpid2021@gmail.com")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[19]/div/div[1]/div/section/div/div/div[2]/div/div/div/div/div[2]/div/div[1]/div[2]/input").send_keys("@Testingid2021")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[19]/div/div[1]/div/section/div/div/div[2]/div/div/div/div/div[2]/div/div[3]/button").click()
    time.sleep(2)
    return list

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
    end_pointer = redirection_url.find("&", start_pointer+1)
    content = redirection_url[start_pointer+1:end_pointer]
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
    load_dotenv()
    driver = start_driver()
    # enable_vpn(driver)

    clear_cache(driver)

    example_link = "https://iprice.co.id/perhiasan/?store=blibli&sort=price.net_asc"
    url_record = iprice_website(driver, example_link)
    # extract_information(url_record)

    time.sleep(60)

    # recorder.close()
    driver.quit()
    print('Done')
