class bcolors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


MIN_IN_SEC = 60
"""Для конвертации минут в секунды:
    Пример:
        - 1 минуты * 60 = 60 секунд
        - 5 минут * 60 = 300 секунд
"""


RETRY_PERIOD_DEFAULT = 60
"""Период за которой происходит повторный запуск программы:
   и парс данных с сайта.

   Default - 1 час
"""


EXIT_COMMANDS = ('exit', 'q', 'quit', 'c', 'cancel', 'z', 'ex')
"""Тригер команды для выхода или отмены ввода."""


MESSAGE_POSITIVE_INT = (
    'Количество, должно быть положительным целым числом: 1, 2, 3, ...'
)


MESSAGE_EXIT_PROGRAM = 'Ручная остановка программы.'
"""Сообщение об остановки программы."""


START_MESSAGE = (
    'Нажмите ввод(enter) пустой строки для дефолтного значения в 1 час.\n'
    '\tили\n'
    ' введите нужное количество минут N\n'
    ' N - периодичность запроса к сайту:'
)
"""Стартовое сообщение при запуске программы."""


HEADER = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'Authorization': '',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Host': 'jewelers.services',
    'Origin': 'https://qgold.com',
    'Referer': 'https://qgold.com/',
    'Sec-Ch-Ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Trailerid': '820242c8-4abc-4a1c-be4e-ee4c5ff9b7f1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36',
}


TABLE_SCHEMA = (
    'Description',  # Product
    'Style',  # Product
    'MSRP',  # Product
    'InStock',  # Product
    'Size',  # Product
    'Product Type',  # Specifications
    'Jewelry Type',  # Specifications
    'Ring Type',  # Specifications
    'Material: Primary',  # Specifications
    'Material: Primary - Color',  # Specifications
    'Material: Primary - Purity',  # Specifications
    'Sold By Unit',  # Specifications
    'CountryOfOrigin',  # AttributesNamed
    'Metal',  # AttributesNamed
    'Average Weight',  # AttributesNamed
    'Feature',  # Specifications
    'Feature 2',  # Specifications
    'Finish',  # Specifications
    'Manufacturing Process',  # Specifications
    'Profile Type',  # Specifications
    'Ring Shape',  # Specifications
    'FileName',  # Images
)
"""Структура и ключи соответствия для получаемых данных из json."""


ADDRES = (
    'Jewelry-Rings-Adjustable/',
    'Jewelry-Rings-2·Stone-Rings/',
)
"""Ссылки для распарса данных."""


TEMPORARY_STORAGE = []
"""Собирает список словарей с данными."""


PAYLOAD = {
    'filters': [{'key': 'ItemsPerPage', 'value': '36'}],
    'page': 1,
    'sortCode': 5,
    'path': 'Jewelry-Rings-2·Stone-Rings',
}
