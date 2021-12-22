from selenium import webdriver
import selenium
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
        self.tel = self.getTel(content)
        
    def __str__(self):
        return f"{self.title}\nŠifra oglasa:\t{self.id}\nCena:\t{self.price}\nLokacija:\t{self.location}\nTel:\t{self.tel}\n\n"
    
    def getImage(self, content):
        img_cls = content.find_element_by_class_name("ClassifiedDetailGallery-slideImage")
        return img_cls.screenshot_as_png

    def getTel(self, content):    
        content.find_element_by_class_name("link-tel--faux-teaser").click()
        return content.find_element_by_class_name("ClassifiedDetailOwnerDetails-contactEntryLink").text
        
browser = webdriver.Firefox()
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
    ad_hrefs = [ad_link.get_attribute("href") for ad_link in ad_links]
    for ad_href in ad_hrefs:
        browser.get(ad_href)
        try: #new ad view
            content = browser.find_element_by_class_name("content-main")
            a = bolhaAd(content, ad_href)
            print(a)
        except selenium.common.exceptions.NoSuchElementException:
            browser.find_element_by_class_name("base-entity")
            print("old ad")

finally:
    browser.quit()