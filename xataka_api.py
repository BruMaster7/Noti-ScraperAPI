from datetime import datetime
from new import New
from util import *


DATE = str(datetime.now())
URL = 'https://www.xataka.com/'
html_tag = 'article'
class_name = 'recent-abstract abstract-article'

articles = fetch_articles(URL, html_tag, class_name)

def get_xataka_news(articles) -> list[New]:
    news = []
    for article in articles:
        header = get_header(article, 'h2', 'abstract-title')
        title = get_title(article, 'p', '')
        img_url = get_img(article, 'picture', 'img', '', 'src')
        category = get_category(article, 'a', 'abstract-taxonomy') 
        if header and title and img_url and category:
            news.append(New(
                header=header, 
                title=title, 
                img=img_url, 
                web="Xataka", 
                text="", 
                category=category, 
                date=DATE)
            )
    return news

    
news = get_xataka_news(articles)

save_file('xataka', news)
