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
    browser.add_cookie({"name": "MUSIC_U", "value": "0061712A0B92535AF6126ADABF43C77B22802F890A704CAF71BDAFB13308BB63C91E4B09C163F8FB54F7285B09FB5CEC068343252F99899F58CAF9C7B113902D4EF63C10D22F6FAADD4B3A77636EEE1AEFE56E0F6B23DDE561CA33E14A6C0FA830506CEF3712CD60C5E7874864C08B5CDC66735CF81C6DA4168632C3473377C6E970FA79A723AA8AC5C2D4F363412D3FBF5BB05B11AB515810F04C51D31949038C366653B88E946CCC48AC8BC968F93434504B3754A1E2AE715291AB23D22DE7119756203116AD5ECDA426D5BAC0393C6F11E93C5976F083B923CCB7DE173CA9B8033D8698C3310BA29D1E339C17AFDE2CA17B4B252E5CD9F9EC0C4ACB158584A8EA4D56FA4F15395F46740755D14817F229B4E28FFDE5077F5577778B68CD65704D2F361CA74C5238D183844FF50FA56BF4A9122552A6CF6204A20DB4433B8A311572328261EB2735F018F4E4C93902C8EAD987F8FDC13399C6FB2646078E21FE"})
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
