import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

from noti_scraperapi.article_parsers.base import ArticleParser


class ElPaisParser(ArticleParser):
    def get_header(article):
        title_h2 = article.find("h2", class_="Promo-title")
        if title_h2:
            title_a_tag = title_h2.find("a", class_="Link")
            href = (
                title_a_tag["href"]
                if title_a_tag and "href" in title_a_tag.attrs
                else None
            )
        else:
            href = None

        article_header = None
        if href:
            # Obtener el contenido de la página web del artículo
            article_response = requests.get(href)
            article_soup = BeautifulSoup(article_response.content, "html.parser")
            article_header = article_soup.find("h1", class_="Page-headline")
        return article_header.get_text() if article_header else None

    def get_title(article):
        title_h2 = article.find("h2", class_="Promo-title")
        if title_h2:
            title_a_tag = title_h2.find("a", class_="Link")
            href = (
                title_a_tag["href"]
                if title_a_tag and "href" in title_a_tag.attrs
                else None
            )
        else:
            href = None

        article_title = None
        if href:
            article_response = requests.get(href)
            article_soup = BeautifulSoup(article_response.content, "html.parser")
            article_title = article_soup.find("h2", class_="Page-subHeadline")
        return article_title.get_text() if article_title else None

    def get_img(article):
        title_h2 = article.find("h2", class_="Promo-title")
        if title_h2:
            title_a_tag = title_h2.find("a", class_="Link")
            href = (
                title_a_tag["href"]
                if title_a_tag and "href" in title_a_tag.attrs
                else None
            )
        else:
            href = None

        img_tag = None
        if href:
            article_response = requests.get(href)
            article_soup = BeautifulSoup(article_response.content, "html.parser")
            page_lead_div = article_soup.find("div", class_="Page-lead")
            if page_lead_div:
                img_tag = page_lead_div.find("img", class_="Image")
        return img_tag["src"] if img_tag and "src" in img_tag.attrs else None

    def get_url(article) -> str:
        title_h2 = article.find("h2", class_="Promo-title")
        if title_h2:
            title_a_tag = title_h2.find("a", class_="Link")
            if title_h2:
                title_a_tag = title_h2.find("a", class_="Link")
                href = (
                    title_a_tag["href"]
                    if title_a_tag and "href" in title_a_tag.attrs
                    else None
                )
                return href
        return None

    def get_category(article) -> str:
        category_div = article.find("div", class_="Promo-category")
        if category_div:
            category_a_tag = category_div.find("a", class_="Link")
            return category_a_tag.get_text() if category_a_tag else None

    def get_date(article):
        title_h2 = article.find("h2", class_="Promo-title")
        if title_h2:
            title_a_tag = title_h2.find("a", class_="Link")
            href = (
                title_a_tag["href"]
                if title_a_tag and "href" in title_a_tag.attrs
                else None
            )
        else:
            href = None

        article_date = None
        if href:
            article_response = requests.get(href)
            article_soup = BeautifulSoup(article_response.content, "html.parser")
            article_date = article_soup.find("div", class_="Page-datePublished")
            cleaned_date_str = ""

            if article_date:
                date_str = article_date.get_text().strip()
                # Limpiar la cadena de fecha: eliminar cualquier coma inicial y espacios
                cleaned_date_str = re.sub(r"^,\s*", "", date_str)
            try:
                # Intentar parsear con hora
                if "," in cleaned_date_str:
                    formatted_date = datetime.strptime(
                        cleaned_date_str, "%d/%m/%Y, %H:%M"
                    )
                else:
                    # Si no tiene hora, intentar solo con la fecha
                    formatted_date = datetime.strptime(cleaned_date_str, "%d/%m/%Y")

                return formatted_date.strftime("%d/%m/%Y %H:%M")
            except ValueError:
                print(f"Formato de fecha inesperado: {cleaned_date_str}")
                return None
        return None
