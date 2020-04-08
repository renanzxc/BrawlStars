from urllib.parse import urljoin
from .parser import Parser


class Crawler:
    def __init__(self, default_url, downloader, page) -> None:
        self.default_url = urljoin(default_url, page)
        self.downloader = downloader
        self.parser = Parser()
        self._brawlers = []

    def download(self):
        response = self.downloader.get(self.default_url)
        params = self.parser.extractUrlParams(response)

        try:
            for param in params:
                response_brawler = self.getBrawlerPage(param)
                self._brawlers.append(self.parser.parse(response_brawler))

        except StopIteration:
            pass

        return self

    def getBrawlerPage(self, param):
        url = urljoin(self.default_url, param)
        return self.downloader.get(url)
