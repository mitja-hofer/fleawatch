import pickle
import os
import selenium

class BolhaAds(object):
    def __init__(self, keywords, timestamp):
        self.ads = [] #empty list to append ads to
        self.keywords = keywords
        self.timestamp = timestamp

class BolhaAd(object):
    def __init__(self, content, ad_href):
        self.url = ad_href
        self.title = content.find_element_by_class_name("ClassifiedDetailSummary-title").text
        self.id = content.find_element_by_class_name("ClassifiedDetailSummary-adCode").text.split(" ")[-1]
        self.price = content.find_element_by_class_name("ClassifiedDetailSummary-priceDomestic").text
        self.description = content.find_element_by_class_name("ClassifiedDetailDescription-text").text
        self.type = content.find_elements_by_css_selector("dd.ClassifiedDetailBasicDetails-listDefinition")[0].text
        self.location = content.find_elements_by_css_selector("dd.ClassifiedDetailBasicDetails-listDefinition")[1].text
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
    

def save_ad_ids(ad_ids, recipient_id):
    with open(os.path.dirname(__file__) +f"/../ads/ads_{recipient_id}", "wb") as file:
        pickle.dump(ad_ids, file)

def get_seen_ad_ids(recipient_id):
    if os.path.isfile(os.path.dirname(__file__) + f"/../ads/ads_{recipient_id}"):
        with open(os.path.dirname(__file__) + f"/../ads/ads_{recipient_id}", "rb") as file:
            return pickle.load(file)
    return []




    