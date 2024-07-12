import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime

from new import New

DATE = str(datetime.now())
URL = "https://www.elpais.com.uy/"

response = requests.get(URL)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")
articles = soup.find_all("div", class_="PromoBasic-content")

news = []

for article in articles:
    # Extraer link del articulo, desde el h2 Promo-title
    title_h2 = article.find("h2", class_="Promo-title")
    if title_h2:
        title_a_tag = title_h2.find("a", class_="Link")
        href = (
            title_a_tag["href"] if title_a_tag and "href" in title_a_tag.attrs else None
        )
    else:
        href = None

    # Extraer el texto del Promo-category
    category_div = article.find("div", class_="Promo-category")
    if category_div:
        category_a_tag = category_div.find("a", class_="Link")
        category_text = category_a_tag.get_text() if category_a_tag else None
    else:
        category_text = None

    if href:
        # Obtener el contenido de la página web del artículo
        article_response = requests.get(href)
        article_soup = BeautifulSoup(article_response.content, "html.parser")

        # Extraer el header del artículo
        article_header = article_soup.find("h1", class_="Page-headline")
        article_title = article_soup.find("h2", class_="Page-subHeadline")

        article_header_text = article_header.get_text() if article_header else None
        article_title_text = article_title.get_text() if article_title else None

        # Extraer la URL de la imagen
        img_tag = None
        page_lead_div = article_soup.find("div", class_="Page-lead")
        if page_lead_div:
            img_tag = page_lead_div.find("img", class_="Image")
        img_url = img_tag["src"] if img_tag and "src" in img_tag.attrs else None

        # Extraer el texto del body del artículo
        body_text = None
        body_div = article_soup.find("div", class_="Page-articleBody")
        if body_div:
            body_content = body_div.find(
                "div", class_="RichTextArticleBody RichTextBody"
            )
            body_text = (
                body_content.get_text(separator=" ", strip=True)
                if body_content
                else None
            )
    else:
        article_header_text = None
        article_title_text = None
        img_url = None
        body_text = None

    new_object = New(
        header=article_header_text,
        title=article_title_text,
        img=img_url,
        web="El país",
        text=body_text,
        category=category_text,
        date=DATE,
    )
    news.append(new_object)

with open("el_pais.json", "w") as f:
    json.dump([n.to_json() for n in news], f, ensure_ascii=False, indent=4)
    print("JSON realizado con exito")
