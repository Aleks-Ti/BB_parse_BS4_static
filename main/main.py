import asyncio
import logging
import os
import sys

from tqdm import tqdm

from pars_site import parse_links_product
from settings import (
    EXIT_COMMANDS,
    MESSAGE_EXIT_PROGRAM,
    MESSAGE_POSITIVE_INT,
    MIN_IN_SEC,
    RETRY_PERIOD_DEFAULT,
    START_MESSAGE,
)
from settings import bcolors as bc

logging.basicConfig(
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename=os.path.join(os.path.dirname(__file__), 'program.log'),
    encoding='utf-8',
)


async def parse_date():
    """Запускает парсинг данных."""
    try:
        await parse_links_product()
    except Exception as err:
        logging.error(err)


def main():
    """Стартовая функция и ожидание ввода пользователя.

    Constants:
        - RETRY_PERIOD_DEFAULT: время ожидания в минутах
    """

    RETRY_PERIOD = RETRY_PERIOD_DEFAULT
    while True:
        try:
            user_input = input(f'{bc.OK_GREEN} {START_MESSAGE}')

            if user_input in EXIT_COMMANDS:
                print(f'{bc.OK_CYAN} Завершение программы.')
                sys.exit(1)

            if user_input == '':
                break

            RETRY_PERIOD = int(user_input)
            if RETRY_PERIOD >= 1:
                break
            else:
                print(f'{bc.FAIL}{MESSAGE_POSITIVE_INT}')
                pass

        except (ValueError, TypeError) as err:
            logging.error(
                f'Не корректные входные данные от пользователя: {err}'
            )
            print(f'{bc.FAIL}{MESSAGE_POSITIVE_INT}')
            pass

        except EOFError:
            logging.info(MESSAGE_EXIT_PROGRAM)
            print(f'{bc.OK_CYAN} {MESSAGE_EXIT_PROGRAM}')
            sys.exit(1)

    async def run_parse():
        """Вспомогательная функция, запускающая цикл событий."""
        while True:
            logging.info('Старт программы.')
            print('Старт программы.')
            await parse_date()
            logging.info('Данные обработы!')
            print('Данные обработы!')
            for _ in tqdm(
                range(RETRY_PERIOD * MIN_IN_SEC),
                desc='До следующего запроса осталось',
                unit='сек',
            ):
                await asyncio.sleep(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_parse())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info(MESSAGE_EXIT_PROGRAM)
        print(f'{bc.WARNING} {MESSAGE_EXIT_PROGRAM}')
