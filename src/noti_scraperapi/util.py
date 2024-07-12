import json
from datetime import datetime
from typing import Iterable, NamedTuple


import requests
from bs4 import BeautifulSoup

from noti_scraperapi.article_parsers.base import ArticleParser
from noti_scraperapi.new import New


class ScraperSettings(NamedTuple):
    url: str
    html_tag: str
    class_name: str
    article_parser: ArticleParser
    filename: str
    web_name: str


def fetch_articles(url, html_tag, class_name) -> Iterable[BeautifulSoup]:
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.find_all(html_tag, class_=class_name)


def save_file(filename, news):
    with open((f"{filename}.json"), "w") as f:
        json.dump([n.to_json() for n in news], f, ensure_ascii=False, indent=4)
    print("JSON realizado con exito")


def run_scraper(scraper_settings: ScraperSettings):
    DATE = str(datetime.now())
    articles = fetch_articles(
        scraper_settings.url, scraper_settings.html_tag, scraper_settings.class_name
    )
    news = []
    for article in articles:
        header = scraper_settings.article_parser.get_header(article)
        title = scraper_settings.article_parser.get_title(article)
        img_url = scraper_settings.article_parser.get_img(article)
        category_list = scraper_settings.article_parser.get_category(article)
        if header and title and img_url and category_list:
            news.append(
                New(
                    header=header,
                    title=title,
                    img=img_url,
                    web=scraper_settings.web_name,
                    text="",
                    category=category_list,
                    date=DATE,
                )
            )
    save_file(scraper_settings.filename, news)
