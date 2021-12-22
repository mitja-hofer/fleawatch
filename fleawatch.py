from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


browser = webdriver.Firefox()
try:
    keywords = "cestno kolo"
    browser.get(f"https://www.bolha.com/")
    browser.find_element(By.ID, "didomi-notice-agree-button").click()
    el = browser.find_element(By.CLASS_NAME, "SearchBox-input")
    el.click()
    el.send_keys(keywords + Keys.RETURN)

    ads = WebDriverWait(browser, 20).until(lambda d: d.find_elements_by_css_selector(".EntityList--Regular .EntityList-item--Regular"))
    for ad in ads:
        print(ad.text)

finally:
    browser.quit()