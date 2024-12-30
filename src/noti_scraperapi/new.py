class New:
    def __init__(self, header, title, img, web, url, category, date):
        self.header = header
        self.title = title
        self.img = img
        self.web = web
        self.url = url
        self.category = category
        self.date = date

    def to_json(self):
        return {
            "header": self.header,
            "title": self.title,
            "img": self.img,
            "web": self.web,
            "url": self.url,
            "category": self.category,
            "date": self.date
        }
