import requests
from bs4 import BeautifulSoup
import asyncio
import tracemalloc
from requests_html import HTMLSession
from http import HTTPStatus
from settings import HEADER, TABLE_SCHEMA
import requests_cache
requests_cache.install_cache('my_cache', expire_after=3600)
session = HTMLSession()


def detail(links):
    result = {}
    for link in links:
        url = 'https://jewelers.services/productcore/api'
        url = url + link + '/'
        response = session.get(url=url, headers=HEADER)
        if response.status_code == HTTPStatus.OK:
            q = response.json()

            product = q.get('Product')
            for attr in product:
                if attr == 'InStock':
                    if product[attr] < 1:
                        result[attr] = 'Out of Stock'
                        break
                if attr in TABLE_SCHEMA:
                    result[attr] = product[attr]


            product_detail = q.get('Specifications')
            for attr in product_detail:
                qwer = attr['Specification']
                if qwer in TABLE_SCHEMA:
                    result[qwer] = attr['Value']

            product_attr_name = q.get('AttributesNamed')
            for attr in product_attr_name:
                qwer = attr['AttributeDescription']
                if qwer in TABLE_SCHEMA:
                    result[qwer] = attr['AttributeValue']


# def detail(links):
#     for link in links:
#         url = 'https://qgold.com'
#         url = url + link + '/'
#         response = session.get(url=url)
#         response.html.render(sleep=10)
#         # qwas = response.html.find('div.row.info-details-wrapper', first=False)
#         qwas = response.html.find('div.specs-table-wrapper', first=False)
#         print(qwas)
#         for li in qwas:
#             li_elements = li.find('li.trow.ng-star-inserted', first=False)
#             for li in li_elements:
#                 print(li.text)
#             li_elements = li.find('div.price-tag', first=False)
#             for p in li_elements:
#                 print(p.text)


def parse_date_adjustable():
    url = 'https://qgold.com/pl/Jewelry-Rings-Adjustable/'
    response = session.get(url)
    response.html.render(sleep=10)
    special_div = response.html.find('div.row.product-list', first=True)
    if special_div:
        # special_div.text
        links = special_div.links
        detail(links)
    else:
        print('НЕ НАЙДЕНО')


def parse_date_rings():
    url = 'https://qgold.com/pl/Jewelry-Rings-2·Stone-Rings/'
    response = session.get(url)
    response.html.render(sleep=10)
    special_div = response.html.find('div.row.product-list', first=True)
    if special_div:
        # special_div.text
        links = special_div.links
        detail(links)
    else:
        print('НЕ НАЙДЕНО')


# parse_date_rings()
parse_date_adjustable()
