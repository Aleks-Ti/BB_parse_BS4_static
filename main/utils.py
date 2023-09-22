import pandas as pd
from settings import TEMPORARY_STORAGE

# Создайте DataFrame с вашими данными


def save_in_list_date(data):
    TEMPORARY_STORAGE.append(data)


def parse_data_save():
    df = pd.DataFrame(TEMPORARY_STORAGE)

    # Укажите путь к файлу Excel, в который хотите сохранить данные
    excel_file_path = 'product_date.xlsx'

    # Сохраните DataFrame в Excel
    df.to_excel(excel_file_path, index=True)  # Установите index=False, если не хотите сохранять индексы строк

    print(f"Данные сохранены в {excel_file_path}")
