import requests
from bs4 import BeautifulSoup
import asyncio
import tracemalloc
from http import HTTPStatus
from pprint import pprint
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 "
                  "Safari/537.36"
}

session = requests.Session()
session.headers.update(HEADERS)


def parse_page_rings():
    url = 'https://jewelers.services/productcore/api/pl/Jewelry-Rings-2·Stone-Rings'
    response = session.get(url)
    if (status := response.status_code) == HTTPStatus.OK:
        d = response.json()
        pprint(d)
    print(status)


def parse_page_adjustable():
    response = requests.get(
        'https://qgold.com/pl/Jewelry-Rings-Adjustable/', HEADERS
    )
    soup = BeautifulSoup(response.text, features='lxml')
    print(soup)


parse_date_rings()
# parse_date_adjustable()
