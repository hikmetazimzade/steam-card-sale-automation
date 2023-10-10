from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options as ChromeOptions


import pickle
import time

inventory_url = "https://steamcommunity.com/id/xxx/inventory/"#Write Your Own Inventory Link

chrome_options = ChromeOptions()
chrome_options.add_extension("inventoryhelper.crx")

sold_products = 0
currency = "TL"#Write the currency you use in Steam

def DeleteProduct(products, number):
    steam_products = products.copy()
    steam_products.pop(number)

    write_products = open("cardprices.txt", "w")
    write_products.writelines(steam_products)

    write_products.close()


driver = webdriver.Chrome(options = chrome_options)
driver.maximize_window()

try:
    driver.get(inventory_url)

    cookies = pickle.load(open("steamcookies.pkl", "rb"))

    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except:
            pass

    driver.get(inventory_url)

    while True:
        number = 0
        product_file = open("cardprices.txt", "r")
        products = product_file.readlines()

        for i in products:
            price = float(i.split("=")[1])
            url = i.split("=")[0]

            driver.get(url)

            #In The Case Of Site Server Doesn't Respond
            try:
                shop_price = (WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="market_commodity_buyrequests"]/span[2]'))).text).split(currency)

            except:
                driver.refresh()
                shop_price = (WebDriverWait(driver, 10).until(ec.visibility_of_element_located(
                    (By.XPATH, '//*[@id="market_commodity_buyrequests"]/span[2]'))).text).split(currency)

            shop_price = float((shop_price[0][:-1]).replace(",", "."))

            #Selling Process if It is Greater than or equal to price we wanted
            if shop_price >= price:
                card_name = driver.current_url.split("-")[-1]
                card_name = card_name.replace("%20"," ")
                WebDriverWait(driver,15).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="sih_market_commodity_order_spread"]/div[1]/div[2]/div/div[1]/a/span'))).click()
                time.sleep(2)
                #According to the link we get name of the card we want to sale

                driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@class="modalContent_iFrame"]'))
                WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#filter_control'))).send_keys(card_name)
                time.sleep(1)

                tags = driver.find_elements(By.XPATH, '//*[@class="itemHolder"]')
                items = []

                for i in tags:
                    if i.get_attribute("style") == "" : items.append(i)
                element = items[-1]


                for k in range(items.count(element)):
                    element.click()
                    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="iteminfo0_item_market_actions"]/a/span[2]'))).click()
                    WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#market_sell_buyercurrency_input'))).send_keys(str(shop_price))

                    #Selling Phase
                    checkbox = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="market_sell_dialog_accept_ssa"]')))
                    if not checkbox.is_selected():
                        checkbox.click()

                    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="market_sell_dialog_accept"]/span'))).click()
                    time.sleep(1)
                    WebDriverWait(driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="market_sell_dialog_ok"]/span'))).click()

                    sold_products += 1
                    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#filter_control'))).clear()
                    time.sleep(1)

                DeleteProduct(products, number)
                number -= 1

            number += 1
            time.sleep(1)#Passing To Next Item

        product_file.close()
        time.sleep(1800)


except:
    print(f"{sold_products} Products Are Sold!")
    driver.quit()