import asyncio
from http import HTTPStatus

from requests_html import AsyncHTMLSession
from tqdm import tqdm

from settings import ADDRES, HEADER, PAYLOAD, TABLE_SCHEMA
from utils import parse_data_save, save_in_list_date

session = AsyncHTMLSession()


async def sizes_price(date: list[dict]) -> list:
    """Получает размеры изделия и цены, если есть вариантивность."""
    result = []
    for attr in date:
        result.append(f'Size: {str(attr["Size"])}: {round(attr["MSRP"], 2)}')
    return result


async def video_data(dp: dict) -> dict:
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


async def images_data(dp: dict) -> dict:
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


async def attributesnamed_data(dp: dict) -> dict:
    """Парс побочных данных товара по ключу 'AttributesNamed'."""
    result = {}
    product_attr_name = dp.get('AttributesNamed')
    for attr in product_attr_name:
        qwer = attr['AttributeDescription']
        if qwer in TABLE_SCHEMA:
            result[qwer] = attr['AttributeValue']

    return result


async def specifications_data(dp: dict) -> dict:
    """Парс побочных данных товара по ключу 'Specifications'."""
    result = {}
    product_detail = dp.get('Specifications')
    for attr in product_detail:
        qwer = attr['Specification']
        if qwer in TABLE_SCHEMA:
            result[qwer] = attr['Value']

    return result


async def product_data(dp: dict) -> dict:
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


async def detail(links: set) -> None:
    """Основной цикл парсинга данных.

    dp - date links in index page
    """
    result = {}
    # num = 0
    for link in tqdm(links, desc='Прогресс парсинга'):
        # num += 1
        url = 'https://jewelers.services/productcore/api'
        url = url + link + '/'
        response = await session.get(url=url, headers=HEADER)
        if response.status_code == HTTPStatus.OK and 'family' not in url:
            dp = response.json()

            result.update(await product_data(dp))
            result.update(await specifications_data(dp))
            result.update(await attributesnamed_data(dp))
            result.update(await images_data(dp))
            result.update(await video_data(dp))
            if date := dp.get('Sizes'):
                result['Sizes'] = await sizes_price(date)
            # print(f'control_async{num}')

        elif 'family' in url:
            result['Error'] = 'Товар под заказ, нет конкретных данных.'

        else:
            print(f'Битая ссылка {url}')

        save_in_list_date(result)
        result = {}


async def parse_links_product() -> None:
    """Получает json с данными и достаёт ссылки на товар."""
    links = []
    tasks = []
    for addres in ADDRES:
        url = 'https://jewelers.services/productcore/api/pl/' + addres
        response = await session.post(url=url, headers=HEADER, json=PAYLOAD)
        if response.status_code == HTTPStatus.OK:
            dp = response.json()
            qwer = dp.get('IndexedProducts')['Results']
            for url in qwer:
                links.append(
                    '/pd/' + url.get('URLDescription') + '/' + url.get('Style')
                )
        tasks.append(detail(links))
    await asyncio.gather(*tasks)
    parse_data_save()
