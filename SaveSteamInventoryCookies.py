from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import pickle
import time

username = input("Input Username:")
password = input("Input Password:")

driver = webdriver.Chrome()
driver.maximize_window()

inventory_url = "https://steamcommunity.com/id/xxx/inventory/"#Write Your Own Inventory Link

driver.get(inventory_url)

driver.find_element(By.XPATH,'//*[@id="global_action_menu"]/a[2]').click()

WebDriverWait(driver,5).until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#base'))).click()#Remember Me Button

WebDriverWait(driver,5).until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#responsive_page_template_content > div.page_content > div:nth-child(1) > div > div > div > div.newlogindialog_FormContainer_3jLIH > div > form > div:nth-child(1) > input'))).send_keys(username)
WebDriverWait(driver,5).until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#responsive_page_template_content > div.page_content > div:nth-child(1) > div > div > div > div.newlogindialog_FormContainer_3jLIH > div > form > div:nth-child(2) > input'))).send_keys(password)
WebDriverWait(driver,5).until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#responsive_page_template_content > div.page_content > div:nth-child(1) > div > div > div > div.newlogindialog_FormContainer_3jLIH > div > form > div.newlogindialog_SignInButtonContainer_14fsn > button'))).click()

time.sleep(15)

cookies = driver.get_cookies()
pickle.dump(cookies, open("steamcookies.pkl", "wb"))

driver.quit()