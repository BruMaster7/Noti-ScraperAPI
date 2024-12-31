from datetime import datetime

from noti_scraperapi.article_parsers.base import ArticleParser


class XatakaArticleParser(ArticleParser):
    def get_header(article) -> str:
        header_elem = article.find("h2", class_="abstract-title")
        return header_elem.text.strip() if header_elem else None

    def get_title(article) -> str:
        title_elem = article.find("p")
        return title_elem.text.strip() if title_elem else None

    def get_img(article) -> str:
        img_container = article.find("picture")
        img_elem = img_container.find("img") if img_container else None
        return img_elem.attrs["src"] if img_elem else None

    def get_url(article):
        url_elem = article.find("a")
        return url_elem["href"] if url_elem else None

    def get_category(article) -> list[str]:
        category_element = article.find("a", class_="abstract-taxonomy")
        return category_element.get_text() if category_element else None

    def get_date(article):
        date_elem = article.find("time")
        if date_elem:
            try:
                date = date_elem["datetime"]
                date_formatted = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
                return date_formatted.strftime("%d/%m/%Y %H:%M")
            except ValueError:
                print(f"Formato de fecha inesperado: {date}")
                return None
        return None
