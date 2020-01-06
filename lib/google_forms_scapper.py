# pip3 install selenium
# TODO: Make this work with new configuration
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import sys
from lib.config import get_config


def open_and_fill_form(url, link, mentor_email, student_email=""):
    try:
        _config = get_config()
        webdriver_name = _config["selenium"]["webdriver_name"]
        browser = _config["selenium"]["browser"]
        if browser == "Chrome":
            driver = webdriver.Chrome(webdriver_name)
        elif browser == "Firefox":
            driver = webdriver.Firefox(executable_path="./"+webdriver_name)
        elif browser == "Edge":
            driver = webdriver.Edge(webdriver_name)
        elif browser == "Safari":
            driver = webdriver.Safari(webdriver_name)
    except:
        print("Error happenede , browser: ", browser)
        webdriver_name = "./chromedriver"
        browser = "Chrome"
        driver = webdriver.Chrome(webdriver_name)

    driver.get(url)
    # Get my email input
    emails = driver.find_element_by_name("emailAddress")
    emails.click()
    emails.send_keys(mentor_email)

    # Get date input
    try:
        date = driver.find_element(By.XPATH, "//input[@type='date']")
        date.click()
        date.send_keys(datetime.today().strftime('%m/%d/%Y'))
    except NoSuchElementException:
        print("Cant find date with By.XPATH")

    # Get sharable link
    _link = driver.find_element_by_name("entry.1778266001")
    _link.click()
    _link.send_keys(link)

    # Get student email
    studentEmail = driver.find_element_by_name("entry.1553659285")
    studentEmail.click()
    studentEmail.send_keys(student_email)

    # Crazy way of leaving driver open until user closes the window
    while driver is not None:
        try:
            time.sleep(30)
            emails = driver.find_element_by_name("emailAddress")
        except:
            print("driver quit")
            driver.quit()
            break
    print("End line of google forms")
    return None
