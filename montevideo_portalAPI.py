import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime

DATE = str(datetime.now())
URL = 'https://www.montevideo.com.uy/'
#URL_IMG = 'https://imagenes.montevideo.com.uy/'

response = requests.get(URL)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")

articles = soup.find_all("article", class_='noticia')
#titles = soup.find_all("h2", class_="title")
#headers = soup.find_all("div", class_="kicker bold")


class News:
    def __init__(self, header, title, author, img, date):
        self.header = header
        self.title = title
        self.author = author
        self.img = img
        self.date = date
        

    def to_json(self):
        return {
            "header": self.header,
            "titulo": self.title,
            "autor": self.author,
            "img": self.img,
            "fecha": self.date
        }

news = []

for article in articles:
    header_elem = article.find("div", class_="kicker bold")
    title_elem = article.find("h2", class_="title")
    img_container = article.find('picture')
    #print(img_container)

    
    if img_container:
        img_elem = img_container.find('img', class_='lazyload')
        print(img_elem)
        if img_elem:
            img_url = img_elem.attrs['data-src']
            print(img_url)

    if header_elem and title_elem:
        header = header_elem.text.strip()
        title = title_elem.text.strip()
        
        new = News(header=header, title=title, author="", img=img_url, date=DATE)
        news.append(new)



for n in news:
    print('------------------------')
    print("Encabezado:", n.header)
    print("Título:", n.title)
    print('Link imagen:', n.img)
    print("Fecha extraido:", n.date)
    print('------------------------')

with open('news.json', 'w') as f:
    json.dump([n.to_json() for n in news], f, ensure_ascii=False, indent=4)
    print('JSON realizado con exito')

