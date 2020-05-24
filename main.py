from utils.downloader import Downloader
from brawlstars.crawler import Crawler


def main():
    downloader = Downloader()
    url = "https://www.starlist.pro/"
    page = "brawlers/"
    crawler = Crawler(url, downloader, page)
    content = crawler.download()
    crawler.save()


if __name__ == "__main__":
    main()
