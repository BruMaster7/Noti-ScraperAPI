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

    def get_category(article) -> list[str]:
        category_element = article.find("a", class_="abstract-taxonomy")
        return category_element.get_text() if category_element else None
