import os
from lib.crwaler import Crawler
import requests

BASE_URL = "https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=qdz07i&f1=1"


if __name__ == '__main__':
    r = requests.get(BASE_URL)
    crawler = Crawler(BASE_URL)
    crawler.run()