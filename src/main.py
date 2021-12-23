import json
import os

from html_gen import *
from send_mail import *
from webcrawler import *

def main():
    with open(os.path.dirname(__file__) + "/../subscribers.json", "r") as f:
        subscribers = json.load(f)

    crawler = WebCrawler()
    try:
        for subscriber in subscribers:
            seen_ad_ids = get_seen_ad_ids(subscriber["id"])
            ad_lists = ""
            for keywords in subscriber["keywords_list"]:
                found_ads = crawler.search_bolha(keywords, seen_ad_ids)
                ad_ids = [ad.id for ad in found_ads.ads]
                seen_ad_ids.extend(ad_ids)
                save_ad_ids(seen_ad_ids, subscriber["id"])
                ad_lists += create_ads_list(found_ads)
            
            #create and send email
            msg_html = create_msg_html(ad_lists)
            message = create_message(subscriber["address"], "test", msg_html)
            send_msg(subscriber["address"], message)

    finally:
        crawler.browser.quit()

if __name__ == "__main__":
    main()