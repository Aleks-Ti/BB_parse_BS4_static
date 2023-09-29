import pandas as pd

from settings import TEMPORARY_STORAGE
from settings import bcolors as bc


def save_in_list_date(data: dict) -> None:
    """Добавляет данные в виде словаря в список."""
    TEMPORARY_STORAGE.append(data)


def parse_data_save() -> None:
    """Сохраняет данные в таблице excel."""
    df = pd.DataFrame(TEMPORARY_STORAGE)

    excel_file_path = 'product_date.xlsx'
    try:
        df.to_excel(excel_file_path, index=True)
        print(f'{bc.OK_CYAN}Данные сохранены в {excel_file_path}')
    except BaseException as err:
        print(f'{bc.FAIL}Ошибка записи данных: {err}{bc.WARNING}')
