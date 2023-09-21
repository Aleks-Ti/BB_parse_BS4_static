import logging
import os
import time
from settings import (
    bcolors as bc,
    MIN_IN_SEC,
    EXIT_COMMANDS,
    MESSAGE_EXIT_PROGRAM,
    START_MESSAGE,
)
import asyncio
import tracemalloc
import sys
from parser import parse_page_rings, parse_page_adjustable


logging.basicConfig(
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename=os.path.join(os.path.dirname(__file__), 'program.log'),
    encoding='utf-8',
)


async def progress_bar(retry_period):
    total_time = retry_period
    bar_length = 40
    update_interval = total_time / bar_length

    for i in range(bar_length + 1):
        progress = i / bar_length
        bar = "[" + "#" * i + " " * (bar_length - i) + "]"
        sys.stdout.write(
            "\rОжидание до следующего запроса: [{:<40}] {:.0%}".format(
                bar, progress
            )
        )
        sys.stdout.flush()
        await asyncio.sleep(update_interval)

    sys.stdout.write("\n")


async def parse_date(retry_period):
    while True:
        try:
            await parse_page_rings()
            await parse_page_adjustable()
        except Exception as err:
            logging.error(err)
        # finally:
        #     await progress_bar(retry_period)


def main():
    RETRY_PERIOD = 1  # Одна минута
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
                print(
                    f'{bc.FAIL}Количество, должно быть '
                    f'положительным целым числом: 1, 2, 3, ...'
                )
                pass

        except (ValueError, TypeError) as err:
            logging.error(
                f'Не корректные входные данные от пользователя: {err}'
            )
            print(
                f'{bc.FAIL}Количество, должно быть '
                f'положительным целым числом: 1, 2, 3, ...'
            )
            pass

        except EOFError:
            logging.info(MESSAGE_EXIT_PROGRAM)
            print(f'{bc.OK_CYAN} {MESSAGE_EXIT_PROGRAM}')
            sys.exit(1)

    while True:
        tracemalloc.start()
        asyncio.run(parse_date(RETRY_PERIOD * MIN_IN_SEC))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info(MESSAGE_EXIT_PROGRAM)
        print(f'{bc.WARNING} {MESSAGE_EXIT_PROGRAM}')
