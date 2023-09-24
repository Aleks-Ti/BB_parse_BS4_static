import asyncio
from http import HTTPStatus
import aiohttp
from aiohttp import ClientSession
from tqdm import tqdm
import logging
from settings import ADDRES, HEADER, PAYLOAD, TABLE_SCHEMA
from utils import parse_data_save, save_in_list_date


async def sizes_price(date: list[dict]) -> list:
    """Получает размеры изделия и цены, если есть вариантивность."""
    result = []
    for attr in date:
        result.append(f'Size: {str(attr["Size"])}: {round(attr["MSRP"], 2)}')
    return result


async def video_data(product_info: dict) -> dict:
    """Парс ссылок на видео товара."""
    result = {}
    product_video_path = product_info.get('Video')
    if product_video_path:
        prefics = product_video_path.get('FileName')
        if prefics:
            result['Video'] = (
                'https://images.jewelers.services/0/Videos/' + prefics
            )
    else:
        result['Video'] = 'Отсутствует'

    return result


async def images_data(product_info: dict) -> dict:
    """Парс фото товара."""
    result = {}
    product_image_path = product_info.get('Images')
    result_links_image = []
    for image_date in product_image_path:
        prefics = image_date.get('FileName')
        if prefics:
            result_links_image.append(
                'https://images.jewelers.services/qgrepo/' + prefics,
            )
    result['Images'] = result_links_image

    return result


async def attributesnamed_data(product_info: dict) -> dict:
    """Парс побочных данных товара по ключу 'AttributesNamed'."""
    result = {}
    product_attr_name = product_info.get('AttributesNamed')
    for attr in product_attr_name:
        qwer = attr['AttributeDescription']
        if qwer in TABLE_SCHEMA:
            result[qwer] = attr['AttributeValue']

    return result


async def specifications_data(product_info: dict) -> dict:
    """Парс побочных данных товара по ключу 'Specifications'."""
    result = {}
    product_detail = product_info.get('Specifications')
    for attr in product_detail:
        qwer = attr['Specification']
        if qwer in TABLE_SCHEMA:
            result[qwer] = attr['Value']

    return result


async def product_data(product_info: dict) -> dict:
    """Парс поверхностных данных товара по ключу 'Product'."""
    result = {}
    product = product_info.get('Product')
    for attr in product:
        if attr == 'InStock':
            if product[attr] < 1:
                result[attr] = 'Out of Stock'
                break
        if attr in TABLE_SCHEMA:
            result[attr] = product[attr]

    return result


async def detail(links: list, session: ClientSession) -> None:
    """Основной цикл парсинга данных.

    dp - date links in index page
    """
    result = {}
    # num = 0
    for link in tqdm(links, desc='Прогресс парсинга'):
        # num += 1
        url = 'https://jewelers.services/productcore/api'
        url = url + link + '/'
        try:
            async with session.get(url=url, headers=HEADER) as response:
                if response.status == HTTPStatus.OK and 'family' not in url:
                    product_info_detail = await response.json()

                    result.update(await product_data(product_info_detail))
                    result.update(
                        await specifications_data(product_info_detail)
                    )
                    result.update(
                        await attributesnamed_data(product_info_detail)
                    )
                    result.update(await images_data(product_info_detail))
                    result.update(await video_data(product_info_detail))
                    if date := product_info_detail.get('Sizes'):
                        result['Sizes'] = await sizes_price(date)
                    # print(f'control_async{num}')

                elif 'family' in url:
                    result['Error'] = 'Товар под заказ, нет конкретных данных.'

                else:
                    print(f'Битая ссылка {url}')
        except BaseException as err:
            logging.error('Ошибка', err)
            print(f'Ошибка {err}')

        save_in_list_date(result)
        result = {}


async def parse_links_product(session: ClientSession) -> None:
    """Получает json с данными и достаёт ссылки на товар."""
    product_links = []
    tasks = []
    for addres in ADDRES:
        url = 'https://jewelers.services/productcore/api/pl/' + addres
        try:
            async with session.post(
                url=url, headers=HEADER, json=PAYLOAD
            ) as response:
                if response.status == HTTPStatus.OK:
                    products_info_page = await response.json()
                    links = products_info_page.get('IndexedProducts')[
                        'Results'
                    ]
                    for link in links:
                        product_links.append(
                            '/pd/'
                            + link.get('URLDescription')
                            + '/'
                            + link.get('Style'),
                        )
                else:
                    logging.warning(
                        f'Сайт не доступен, статус {response.status}'
                    )
            tasks.append(detail(product_links, session))
        except BaseException as err:
            logging.error(f'Возникла ошибка: {err}')
    await asyncio.gather(*tasks)
    parse_data_save()
