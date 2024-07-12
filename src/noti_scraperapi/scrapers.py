from noti_scraperapi.article_parsers.montevideo_portal import MontevideoPortalParser
from noti_scraperapi.article_parsers.xataka import XatakaArticleParser
from noti_scraperapi.util import ScraperSettings, run_scraper

SCRAPERS = {
    "Xataka": ScraperSettings(
        url="https://www.xataka.com/",
        html_tag="article",
        class_name="recent-abstract abstract-article",
        article_parser=XatakaArticleParser,
        filename="xataka",
        web_name="Xataka",
    ),
    "Montevideo Portal": ScraperSettings(
        url="https://www.montevideo.com.uy/",
        html_tag="article",
        class_name="noticia",
        article_parser=MontevideoPortalParser,
        filename="montevideo_portal",
        web_name="Montevideo Portal",
    ),
}


def run_xataka_scraper():
    run_scraper(SCRAPERS["Xataka"])


def run_montevideo_portal_scraper():
    run_scraper(SCRAPERS["Montevideo Portal"])
