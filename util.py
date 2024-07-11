import json
import requests

from typing import Iterable
from bs4 import BeautifulSoup


def fetch_articles (url, html_tag, class_name) -> Iterable[BeautifulSoup]:
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.find_all(html_tag, class_=class_name)

def get_header (article, header_tag, header_class) -> str:
    header_elem = article.find(header_tag, class_=header_class)
    return header_elem.text.strip() if header_elem else None

def get_title (article, title_tag, title_class) -> str:
    title_elem = article.find(title_tag, class_=title_class)
    return title_elem.text.strip() if title_elem else None

def get_img (article, container_tag, img_tag, class_name, attr_url) -> str:
    img_container = article.find(container_tag, class_=class_name)
    img_elem = img_container.find(img_tag) if img_container else None
    return img_elem.attrs[attr_url] if img_elem else None

def get_category (article, category_tag, category_class) -> [str]:
     category_element = article.find(category_tag, class_=category_class)
     return category_element.get_text() if category_element else None

def save_file (filename, news):
    with open((f'{filename}.json'), 'w') as f:
        json.dump([n.to_json() for n in news], f, ensure_ascii=False, indent=4)
    print('JSON realizado con exito')





    
