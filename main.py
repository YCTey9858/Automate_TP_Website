import os
from dotenv import load_dotenv
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
import time


def start_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_extension('/path/to/extension.crx')
    driver = webdriver.Chrome(options=options)
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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    driver.get('chrome://settings/clearBrowserData')
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, 'body').send_keys('\ue007')
    time.sleep(3)
    print("Cleared cache")

def iprice_website(tp_wesbite):
    driver.get(tp_wesbite)
    tabs = driver.window_handles
    time.sleep(5)
    print("Number of tabs: ", len(tabs))

    driver.find_element(By.CSS_SELECTOR, 'a[data-ga-trigger="ga-conversion"]').click()
    time.sleep(5)
    print(driver.current_url)

    # redirect to merchant website
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])
    print(driver.current_url)
    print("Number of tabs: ", len(tabs))
    driver.find_element(By.CSS_SELECTOR, 'div[class="redirect"]').click()

    return redirection_urls

def extract_information(data):
    # Step 4: Open the website and perform the action.
    redirection_url = data[0]
    # find a substring start from ig to &
    igsource = redirection_url[redirection_url.find("utm_content=----ig"):redirection_url.find("&")]
    igsource.strip("utm_content=----ig")
    print(igsource)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()
    driver = start_driver()
    # enable_vpn(driver)

    clear_cache(driver)

    example_link = "https://iprice.sg/compare/epson-ecotank-l3250-a4-wi-fi-all-in-one-ink-tank-printer/"
    url_record = iprice_website(example_link)
    extract_information(url_record)

    time.sleep(60)

    # recorder.close()
    driver.quit()
    print('Done')

