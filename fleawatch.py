from html_gen import *
from send_mail import *
from webcrawler import *

def main():
    seen_ad_ids = get_seen_ad_ids()
    crawler = WebCrawler()
    try:
        keywords_list = ["cestno kolo"]
        ad_lists = ""
        for keywords in keywords_list:
            found_ads = crawler.search_bolha(keywords, seen_ad_ids)
            ad_ids = [ad.id for ad in found_ads.ads]
            seen_ad_ids.extend(ad_ids)
            save_ad_ids(seen_ad_ids)
            ad_lists += create_ads_list(found_ads)
        
        #create and send email
        msg_html = create_msg_html(ad_lists)
        message = create_message("mh7289@student.uni-lj.si", "test", msg_html)
        send_msg(message)

    finally:
        crawler.browser.quit()

if __name__ == "__main__":
    main()