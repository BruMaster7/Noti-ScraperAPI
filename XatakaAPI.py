import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime

DATE = str(datetime.now())
URL = 'https://www.xataka.com/'


response = requests.get(URL)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")

articles = soup.find_all("article", class_='recent-abstract abstract-article')

class News:
    def __init__(self, header, title, img, web, text, category, date):
        self.header = header
        self.title = title
        self.img = img
        self.web = web
        self.text = text
        self.category = category
        self.date = date
        
    def to_json(self):
        return {
            "header": self.header,
            "titulo": self.title,
            "img": self.img,
            "web": self.web,
            "texto": self.text,
            "categorias": self.category,
            "fecha": self.date
        }

news = []

for article in articles:
    header_elem = article.find("h2", class_="abstract-title")
    title_elem = article.find("p")
    category_element = article.find("a", class_="abstract-taxonomy")
    img_container = article.find('picture')
    if header_elem and title_elem and category_element and img_container:
        a_element = header_elem.find('a')
        title = title_elem.text.strip()
        category = category_element.get_text()
        img_container = article.find('picture')

        if a_element and img_container:
            img_elem = img_container.find('img')
            header = a_element.get_text()
            if img_elem:
                img_url = img_elem.attrs['src']
        new = News(header=header, title=title, img=img_url, web="Xataka", text="", category=category, date=DATE)
        news.append(new)

with open('newsXataka.json', 'w') as f:
    json.dump([n.to_json() for n in news], f, ensure_ascii=False, indent=4)
    print('JSON realizado con exito')
