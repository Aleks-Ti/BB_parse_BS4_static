import requests
from bs4 import BeautifulSoup
import asyncio
import tracemalloc
import tls_client
import aiohttp
from requests_html import HTMLSession

header = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
}

session = HTMLSession()

def parse_date_rings():
    url = 'https://qgold.com/pl/Jewelry-Rings-Adjustable/'
    response = session.get(url)
    response.html.render(sleep=5)
    soup = BeautifulSoup(response.html.html, 'lxml')
    swagger = soup.find("div", {"class": "row product-list"})
    print(swagger.text)
    

def parse_date_adjustable():

    url = 'https://qgold.com/pl/Jewelry-Rings-Adjustable/'
    response = session.get(url)
    response.html.render(sleep=5)
    special_div = response.html.find('div.row.product-list', first=True)
    if special_div:
        print(special_div.text)
        print(special_div.links)
    else:
        print('НЕ НАЙДЕНО')

# parse_date_rings()
parse_date_adjustable()
