class URLManager:
    def __init__(self):
        self.homepage = "https://www.google.com"

    def get_homepage(self):
        return self.homepage

    def set_homepage(self, url):
        self.homepage = url
