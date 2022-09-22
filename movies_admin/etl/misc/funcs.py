import logging
from functools import wraps
from time import sleep

from psycopg2 import OperationalError

logger = logging.getLogger("elk")


def prepare_data(data: list):
    """
    Подготовка данных для загрузки в индекс elasticsearch

    :param data: List[dict] - список с данными из таблицы
    :return: List[dict] - список с данными в подготовленном для elasticsearch формате
    """
    logger.info(f"Compare data for elastic. Got {len(data)} rows")
    actual_data = []
    for value in data:
        temp_data = {k: v for k, v in value.items()}

        full_data = [{'index':
                      {'_index': 'movies',
                       '_id': value['id']}
                      },
                     temp_data]
        actual_data.extend(full_data)
    logger.info("Data successfully compared")
    return actual_data


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, max_attempt_count=20):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor)
    до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param max_attempt_count: максимальное кол-во попыток

    :return: результат выполнения функции
    """

    def func_wrapper(func):
        n = 0
        t = 0

        @wraps(func)
        def inner(self, *args, **kwargs):
            nonlocal n, t
            a = None
            while not a:
                if n == max_attempt_count:
                    logger.info("Rich max attempt connection count. Close program.")
                    raise Exception("Connect exception error")
                try:
                    logger.info("Trying to connect to db")
                    a = func(self, **kwargs)
                    logger.info("DB successfully connected")
                except OperationalError:
                    n += 1
                    t = start_sleep_time * factor ** n if t < border_sleep_time else border_sleep_time
                    logger.error("Connection error", exc_info=True)
                    sleep(t)
            return a
        return inner
    return func_wrapper
