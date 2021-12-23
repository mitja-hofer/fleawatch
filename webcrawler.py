from datetime import datetime
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from bolha_ads import *

class WebCrawler(object):
    def __init__(self):
        self.browser = webdriver.Firefox()
    
    def search_bolha(self, keywords, seen_ad_ids):
        self.browser.get(f"https://www.bolha.com/")
        self.browser.find_element(By.ID, "didomi-notice-agree-button").click()
        el = self.browser.find_element(By.CLASS_NAME, "SearchBox-input")
        el.click()
        el.send_keys(keywords + Keys.RETURN)

        # wait for async loading of ads
        ad_links = WebDriverWait(self.browser, 20).until(
            lambda d: d.find_elements_by_css_selector(".EntityList--Regular .EntityList-item--Regular h3 > a.link")
        )
        ad_hrefs = [{"href":ad_link.get_attribute("href"), "id":ad_link.get_attribute("name")} for ad_link in ad_links]
        found_ads = BolhaAds(keywords, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        for ad_href in ad_hrefs:
            if ad_href["id"] not in seen_ad_ids:
                self.browser.get(ad_href["href"])
                try: #new ad view
                    content = self.browser.find_element_by_class_name("content-main")
                    a = BolhaAd(content, ad_href)
                    print(a)
                    found_ads.ads.append(a)
                except selenium.common.exceptions.NoSuchElementException:
                    self.browser.find_element_by_class_name("base-entity")
                    print("old ad")
        return found_ads
