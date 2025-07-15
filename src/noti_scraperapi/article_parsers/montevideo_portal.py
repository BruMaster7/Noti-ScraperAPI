import requests
from bs4 import BeautifulSoup
from datetime import datetime

from noti_scraperapi.article_parsers.base import ArticleParser


class MontevideoPortalParser(ArticleParser):
    def get_header(article) -> str:
        header_elem = article.find("div", class_="kicker bold")
        return header_elem.text.strip() if header_elem else None

    def get_title(article) -> str:
        title_elem = article.find("h2", class_="title")
        return title_elem.text.strip() if title_elem else None

    def get_img(article) -> str:
        img_container = article.find("picture")
        if not img_container:
            return None

        img_elem = img_container.find("img")
        if not img_elem:
            return None

        return img_elem.get("src")

    def get_url(article) -> str:
        new_url = article.find("a")
        return new_url.attrs["href"] if new_url else None

    def get_category(article) -> list[str]:
        new_attrs = article.find("a")
        if not new_attrs:
            return
        second_URL = new_attrs["href"]
        second_response = requests.get(second_URL)
        html_URL2 = second_response.content
        soup2 = BeautifulSoup(html_URL2, "html.parser")
        category_container = soup2.find("ul", class_="categorias hidden-xs")
        if not category_container:
            return
        category_element = category_container.find_all("a")
        category_list = []
        for category in category_element:
            category_text = category.text.strip()
            if category_text != "Inicio":  # Excluir "Inicio"
                category_list.append(category_text)
        return category_list

    def get_date(article) -> str:
        new_attrs = article.find("a")
        if not new_attrs:
            return
        second_URL = new_attrs["href"]
        second_response = requests.get(second_URL)
        html_URL2 = second_response.content
        soup2 = BeautifulSoup(html_URL2, "html.parser")
        date = soup2.find("p", class_="fecha-hora")
        if date:
            date_text = date.text.strip()
            try:
                formatted_date = datetime.strptime(date_text, "%d.%m.%Y %H:%M")
                return formatted_date.strftime("%d/%m/%Y %H:%M")
            except ValueError:
                print(f"Formato de fecha inesperado: {date_text}")
                return None
        return None
