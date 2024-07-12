from abc import ABC, abstractmethod


class ArticleParser(ABC):
    @abstractmethod
    def get_header(article, header_tag, header_class) -> str:
        pass

    @abstractmethod
    def get_title(article, title_tag, title_class) -> str:
        pass

    @abstractmethod
    def get_img(article, container_tag, img_tag, class_name, attr_url) -> str:
        pass

    @abstractmethod
    def get_category(article, category_tag, category_class) -> list[str]:
        pass
