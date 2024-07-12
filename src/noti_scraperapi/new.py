class New:
    def __init__(self, header, title, img, web, text, category, date):
        self.header = header
        self.title = title
        self.img = img
        self.web = web
        self.text = text
        self.category = category
        self.date = date

    def to_json(self):
        return {
            "header": self.header,
            "titulo": self.title,
            "img": self.img,
            "web": self.web,
            "texto": self.text,
            "categorias": self.category,
            "fecha": self.date,
        }
