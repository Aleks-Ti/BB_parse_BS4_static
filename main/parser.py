import requests
from bs4 import BeautifulSoup
import asyncio
import tracemalloc
from requests_html import HTMLSession
from http import HTTPStatus
from settings import HEADER, TABLE_SCHEMA, ADDRES
import requests_cache
import time
import random

requests_cache.install_cache('my_cache', expire_after=3600)
session = HTMLSession()


def sizes_price(date: list[dict]) -> list:
    result = []
    for attr in date:
        result.append({'Size: ' + str(attr['Size']): round(attr['MSRP'], 2)})
    return result


def video_data(dp: dict) -> dict:
    """Парс ссылок на видео товара."""

    result = {}
    product_video_path = dp.get('Video')
    if product_video_path:
        prefics = product_video_path.get('FileName')
        if prefics:
            result['Video'] = (
                'https://images.jewelers.services/0/Videos/' + prefics
            )
    else:
        result['Video'] = 'Отсутствует'

    return result


def images_data(dp: dict) -> dict:
    """Парс фото товара."""

    result = {}
    product_image_path = dp.get('Images')
    result_links_image = []
    for image_date in product_image_path:
        prefics = image_date.get('FileName')
        if prefics:
            result_links_image.append(
                'https://images.jewelers.services/qgrepo/' + prefics
            )
    result['Images'] = result_links_image

    return result


def attributesnamed_data(dp: dict) -> dict:
    """Парс побочных данных товара по ключу 'AttributesNamed'."""

    result = {}
    product_attr_name = dp.get('AttributesNamed')
    for attr in product_attr_name:
        qwer = attr['AttributeDescription']
        if qwer in TABLE_SCHEMA:
            result[qwer] = attr['AttributeValue']

    return result


def specifications_data(dp: dict) -> dict:
    """Парс побочных данных товара по ключу 'Specifications'."""

    result = {}
    product_detail = dp.get('Specifications')
    for attr in product_detail:
        qwer = attr['Specification']
        if qwer in TABLE_SCHEMA:
            result[qwer] = attr['Value']

    return result


def product_data(dp: dict) -> dict:
    """Парс поверхностных данных товара по ключу 'Product'."""

    result = {}
    product = dp.get('Product')
    for attr in product:
        if attr == 'InStock':
            if product[attr] < 1:
                result[attr] = 'Out of Stock'
                break
        if attr in TABLE_SCHEMA:
            result[attr] = product[attr]

    return result


def detail(links: set) -> None:
    '''Основной цикл парсинга данных.

    Atributs:
        dp - date page product in json file
    '''

    result = {}
    for link in links:
        url = 'https://jewelers.services/productcore/api'
        url = url + link + '/'
        response = session.get(url=url, headers=HEADER)
        if response.status_code == HTTPStatus.OK and 'family' not in url:
            dp: dict = response.json()

            result.update(product_data(dp))

            result.update(specifications_data(dp))

            result.update(attributesnamed_data(dp))

            result.update(images_data(dp))

            result.update(video_data(dp))

            if date := dp.get('Sizes'):
                result['Sizes'] = sizes_price(date)

            time.sleep(random.randint(1, 5))
            print('control')

        elif 'family' in url:
            result['Error'] = 'Товар под заказ, нет конкретных данных.'

        else:
            print(f'Битая ссылка {url}')

        result = {}

    print('control end')


def parse_links_product():
    """Получение ссылок со страницы на детализацию товаров."""

    for addres in ADDRES:
        url = 'https://qgold.com/pl/' + addres
        response = session.get(url)
        if response.status_code == HTTPStatus.OK:
            response.html.render(sleep=10)
            special_div = response.html.find('div.row.product-list', first=True)
            if special_div:
                # special_div.text
                links = special_div.links
                detail(links)
            else:
                print(f'НЕ НАЙДЕНО {special_div} по адресу: {url}')
        else:
            print(f'Сайт не доступен {url}')


parse_links_product()
