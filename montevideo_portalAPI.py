import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime

DATE = str(datetime.now())
URL = 'https://www.montevideo.com.uy/'


response = requests.get(URL)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")

articles = soup.find_all("article", class_='noticia')

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
    header_elem = article.find("div", class_="kicker bold")
    title_elem = article.find("h2", class_="title")
    img_container = article.find('picture')
    new_attrs = article.find('a')

    if new_attrs:
        second_URL = new_attrs['href']
        second_response = requests.get(second_URL)
        html_URL2 = second_response.content
        soup2 = BeautifulSoup(html_URL2, "html.parser")
        category_container = soup2.find("ul", class_="categorias hidden-xs")
        if category_container:
            category_element = category_container.find_all("a")
            category_list = []
            for category in category_element:
                category_text = category.text.strip()
                if category_text != "Inicio":  # Excluir "Inicio"
                    category_list.append(category_text)
              
         
    
    if img_container:
        img_elem = img_container.find('img', class_='lazyload')
        if img_elem:
            img_url = img_elem.attrs['data-src']

    if header_elem and title_elem:
        header = header_elem.text.strip()
        title = title_elem.text.strip()
        
        new = News(header=header, title=title, img=img_url, web="Montevideo Portal", text="", category=category_list, date=DATE)
        news.append(new)

with open('news.json', 'w') as f:
    json.dump([n.to_json() for n in news], f, ensure_ascii=False, indent=4)
    print('JSON realizado con exito')

