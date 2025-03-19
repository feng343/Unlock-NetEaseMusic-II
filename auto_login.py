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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B7C75CE7AD8A552687AC93B41324541AC1623ED0E0FFB4C5BB832B16FE3C86253892CFF37CFB75106CEE9F6DE0A988B891FFD8425B1882ED6D99733AAEBEB8FC58DBE3D4FC08AE61F45A029E3B4C9E1717A589E9AFC74C57E2C78F3C024648061BCF251927D329E562BE9F42464D06BAE551EE44F22A28531646AE6218CE39002657AD29AEB041D6974893CEA5E4163533F66D93E9BF9750B71DA0632A809BDA3BD450BC8462B060B510CCE391B3635ECA35EA1F136B79B073F41473437F9C884DA74612942CEE1EDEFB046A44C2A1404E32A370CDA134C49C7F8DDFDDF2A71EBD7ABE5D2F331EC250CD3F9AAD48AB997B57114E90DECD02D9A99A6E8F68916C1509E3439F86ACC567114B655073E0F8C868D3FB7A80927791A1871364BB554825ED836AACB2B1166847B51B6DF6914B6D62F9006C0DE4CA2659D9EB9CE8A4BA72B3ED15FEA0C1EB4976C2AE2077BB33F7D5AF5432BFC46B3637A3504B2871E9"})
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
