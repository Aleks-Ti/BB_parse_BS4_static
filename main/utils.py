import pandas as pd
import time
import functools

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
        print(f"{bc.OK_CYAN}Данные сохранены в {excel_file_path}")
    except BaseException as err:
        print(f'{bc.FAIL}Ошибка записи данных: {err}{bc.WARNING}')


def progress_bar(total):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            print("Progress:")
            for i in range(total):
                percent_complete = i / total * 100
                elapsed_time = time.time() - start_time
                remaining_time = (
                    (elapsed_time / (i + 1)) * (total - i - 1) if i > 0 else 0
                )
                print(
                    f"[{'#' * int(percent_complete / 5):20s}] "
                    f"{percent_complete:.1f}% "
                    f"({i + 1}/{total}) Elapsed: "
                    f"{elapsed_time:.1f}s Remaining: {remaining_time:.1f}s",
                    end='\r',
                )
                result = func(*args, **kwargs)
            print("\nComplete!")
            return result

        return wrapper

    return decorator
