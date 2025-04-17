# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "006DB1AA11091ACEBDD1D9BAAAE2B3082BB3B5CB6F89557B17998D2C45CE08ADF0580AC371F74D534BA23A1A4357523D1057E5F5912987F2C69A17DE42969C47963DC3DE35ED087782026AB3C209DAF82279357C0F6828DCF639834F1A5C2B39FA2BA6D4A67ACBA3FBC4152A4835EA704DBD0B8E263E2C9150DE746BFDBFFFC97842D10A4E3D43F425823E6B22EE54D2A21B5C868CCA0DA44594F25CA4B14763CC5F1D8F8B934EED0DDE6D2506211B830AD6787A370CB1F7F6B357C94CF7440CAAA618B738762907182FC9DA2D40261902FE6582C63D3E990A614C563C0818FDE95386BD748AB3FB2BF36BC27DA81AAF0DD2C2BCD8A1C59B37651045EC515CE8356BAE061579AAB975D14205D6F2230CBCEC4C23CC75DF41115885718189C5C19FC700AB1B1B8174F2F22C9A7811F3A935A3B8DE7DFC2CCBC815B2C9B6B3DC701595B4FC0D356DAD4C08B6EAF9BC3659CA98C6BA229A088F90FC18C73B6836404A"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
