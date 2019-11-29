# pip3 install selenium
# TODO: Make this work with new configuration
from selenium.webdriver import Chrome
# from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import sys


def open_and_fill_form(url, link, mentor_email, student_email=""):
    # TODO: make this come from the CONSTANTS
    webdriver = "chromedriver"
    driver = Chrome(webdriver)
    driver.get(url)
    # Get my email input
    emails = driver.find_element_by_name("emailAddress")
    emails.click()
    emails.send_keys(mentor_email)

    # Get date input
    date = driver.find_element(By.XPATH, "//input[@type='date']")
    date.click()
    date.send_keys(datetime.today().strftime('%m/%d/%Y'))

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
