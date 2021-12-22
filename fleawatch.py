import pickle
import os

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class bolhaAd(object):
    def __init__(self, content, ad_href):
        self.url = ad_href
        self.title = content.find_element_by_class_name("ClassifiedDetailSummary-title").text
        self.id = content.find_element_by_class_name("ClassifiedDetailSummary-adCode").text.split(" ")[-1]
        self.price = content.find_element_by_class_name("ClassifiedDetailSummary-priceDomestic").text
        self.description = content.find_element_by_class_name("ClassifiedDetailDescription-text").text
        self.type = content.find_elements_by_css_selector("dd.ClassifiedDetailBasicDetails-listDefinition")[0].text
        self.location =content.find_elements_by_css_selector("dd.ClassifiedDetailBasicDetails-listDefinition")[1].text
        self.condition = content.find_elements_by_css_selector("dd.ClassifiedDetailBasicDetails-listDefinition")[2].text
        self.contact = self.getContact(content)
        #self.img = self.getImage(content)
        
    def __str__(self):
        return f"{self.title}\nŠifra oglasa:\t{self.id}\nCena:\t{self.price}\nLokacija:\t{self.location}\nContact:\t{self.contact}\n\n"
    
    def getImage(self, content):
        img_cls = content.find_element_by_class_name("ClassifiedDetailGallery-slideImage")
        return img_cls.screenshot_as_png

    def getContact(self, content):    
        try:
            content.find_element_by_class_name("link-tel--faux-teaser").click()
            return content.find_element_by_class_name("ClassifiedDetailOwnerDetails-contactEntryLink").text
        except selenium.common.exceptions.NoSuchElementException:
            return None


def save_ad_ids(ad_ids):
    with open("ads", "wb") as file:
        pickle.dump(ad_ids, file)

def get_seen_ad_ids():
    if os.path.getsize("ads") > 0:
        with open("ads", "rb") as file:
            return pickle.load(file)
    return []
    

def main():
    browser = webdriver.Firefox()
    seen_ad_ids = get_seen_ad_ids()
    try:
        keywords = "cestno kolo"
        browser.get(f"https://www.bolha.com/")
        browser.find_element(By.ID, "didomi-notice-agree-button").click()
        el = browser.find_element(By.CLASS_NAME, "SearchBox-input")
        el.click()
        el.send_keys(keywords + Keys.RETURN)

        # wait for async loading of ads
        ad_links = WebDriverWait(browser, 20).until(
            lambda d: d.find_elements_by_css_selector(".EntityList--Regular .EntityList-item--Regular h3 > a.link")
        )
        ad_hrefs = [{"href":ad_link.get_attribute("href"), "id":ad_link.get_attribute("name")} for ad_link in ad_links]
        ads = []
        for ad_href in ad_hrefs:
            if ad_href["id"] not in seen_ad_ids:
                browser.get(ad_href["href"])
                try: #new ad view
                    content = browser.find_element_by_class_name("content-main")
                    a = bolhaAd(content, ad_href)
                    print(a)
                    ads.append(a)
                except selenium.common.exceptions.NoSuchElementException:
                    browser.find_element_by_class_name("base-entity")
                    print("old ad")
        ad_ids = [ad.id for ad in ads]
        seen_ad_ids.extend(ad_ids)
        save_ad_ids(seen_ad_ids)

    finally:
        browser.quit()

if __name__ == "__main__":
    main()