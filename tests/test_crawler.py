from unittest.mock import patch, Mock
from brawlstars.crawler import Crawler


@patch("utils.downloader.Downloader")
def test_crawler(downloader_mock, brawlers_html, brawler_html):
    url = "https://www.starlist.pro/"
    page = "brawlers/"
    html1 = Mock(text=brawlers_html)
    html2 = Mock(text=brawler_html)

    downloader = downloader_mock.return_value
    downloader.get.return_value = html1

    crawler = Crawler(url, downloader, page)
    content = crawler.download()
