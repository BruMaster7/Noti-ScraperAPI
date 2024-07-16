import requests
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

        if href:
            article_response = requests.get(href)
            article_soup = BeautifulSoup(article_response.content, "html.parser")
            img_tag = None
            page_lead_div = article_soup.find("div", class_="Page-lead")
            if page_lead_div:
                img_tag = page_lead_div.find("img", class_="Image")
        return img_tag["src"] if img_tag and "src" in img_tag.attrs else None

    def get_category(article) -> str:
        category_div = article.find("div", class_="Promo-category")
        if category_div:
            category_a_tag = category_div.find("a", class_="Link")
            return category_a_tag.get_text() if category_a_tag else None
