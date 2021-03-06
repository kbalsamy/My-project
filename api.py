from selenium import webdriver
import selenium
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as BS
from openpyxl import Workbook
import sqlite3
from xlsxwriter import Workbook
from constants import *


def scrape(uname, pword, month, year):
    " webdriver created herewith "
    options = Options()
    options.headless = True
    binary = FirefoxBinary("C:/Program Files/Firefox Nightly/firefox.exe")
    driver = webdriver.Firefox(options=options, firefox_binary=binary)
    try:
        browser = driver.get(url)
        login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-0")))
        login.send_keys(uname)
        password = driver.find_element_by_id("mat-input-1")
        password.send_keys(pword)
        submit = driver.find_element_by_css_selector(".mat-raised-button").click()
        try:
            reading = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mat-list-item:nth-child(2) span:nth-child(1)")))
            reading.click()
            menu_selector = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mat-select-1 .mat-select-arrow"))).click()
            element = driver.find_element_by_css_selector(".ng-trigger-transformPanel")
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            select_month = driver.find_element_by_css_selector(month_dict.get(month)).click()

            enter_year = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-5")))
            enter_year.clear()
            enter_year.send_keys(year)
            try:
                enter_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".primary > .mat-button-wrapper"))).click()

                fetch_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mr-1 > .mat-button-wrapper"))).click()
                soup = BS(driver.page_source, "lxml")
                html = soup.prettify()
                status = "Successfully extracted the values for {}".format(uname)

                result = extract_values(uname, html, month, year, status)

                logout_menu = driver.find_element_by_css_selector(".ml-xs .mat-icon").click()
                logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                         ".mat-menu-item:nth-child(5) > .mat-menu-ripple")))
                logout.click()
                driver.quit()
                return result

            except selenium.common.exceptions.TimeoutException as e:
                status = "Readings are not found for {}.".format(uname)
                result = extract_values(uname, None, month, year, status)
                return result
                # driver.close()

        except selenium.common.exceptions.TimeoutException as e:
            status = "consumer {} not found.".format(uname)
            result = extract_values(uname, None, month, year, status)
            return result
            # driver.close()

    except (selenium.common.exceptions.WebDriverException, selenium.common.exceptions.TimeoutException) as e:
        print("Check your network settings")
        driver.quit()
        return None


def extract_values(ID, html, month, year, status):
    "processing the scrapped values"

    CID = ID
    tablename = month + str(year)
    if html:
        print('extracting values for {}'.format(ID))
        soup = BS(html, "html.parser")
        tab = soup.find("ngx-datatable")
        headers = tab.find_all("span")
        t_list = []
        f_list = []
        for i in headers:
            t_list.append(i.text.strip())
        for i in t_list:
            if i not in f_list and i != "":
                f_list.append(i)
        val = tab.find_all("datatable-body-cell")
        val_list = []
        for i in val:
            val_list.append(i.text.strip())
        results = [val_list[i:i + 9] for i in range(0, len(val_list), 9)]
        data = []
        data.append(CID)
        imp = [val[4] for val in results]
        exp = [val[8] for val in results]
        dif = []
        for i in range(len(imp)):
            d = float(exp[i]) - float(imp[i])
            dif.append(d)
        data.append(imp + exp + dif)
        return data

    else:
        print(status)
        with open('failed summary.txt', 'a+') as file:
            file.write("{} failed to get values\n".format(CID))
            file.close()
        return None
