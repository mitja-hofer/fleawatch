def create_ads_list(ads):
    list = f"""
    <h3>{ads.keywords}</h3>
    <h4>{ads.timestamp}</h4>
    """
    list += f"""<dl>"""
    for ad in ads.ads:
        list += f"""
        <dt>{ad.title}</dt>
        <dd>Cena: {ad.price}</dd>
        <dd>Lokacija: {ad.location}</dd>
        <dd>Kontakt: {ad.contact}</dd>
        <dd>Opis: {ad.description[:50]}</dd>
        """
    list += "</dl>"
    return list

def create_msg_html(ad_lists):
    html = f"""<html>
    <body>
    {ad_lists}
    </body>
    </html>"""
    return html



