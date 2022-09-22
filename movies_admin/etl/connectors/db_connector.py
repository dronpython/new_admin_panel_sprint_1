import logging
from psycopg2.extras import _connection, _cursor, DictCursor
from psycopg2 import connect
from etl.misc.funcs import backoff
from etl.creeds import Settings
from contextlib import contextmanager

logger = logging.getLogger("elk")


class DB:
    def __init__(self, database_config: dict):
        self.config: dict = database_config

    @backoff(start_sleep_time=0.2, factor=2, border_sleep_time=10, max_attempt_count=30)
    @contextmanager
    def _connect(self):
        conn: _connection = connect(**self.config)
        yield conn
        logger.info("Closing connection")
        conn.close()

    def load_all_data(self, table: str, state: str, size: int):
        """
        Выгружаем данные из указанной таблицы пачками

        :param table: сокращенное название таблицы из sql запроса. fw-film_work, p-person, g-genre
        :param state: время последнего обновления записей
        :param size: количество записей
        :return: объект генератора
        """
        with self._connect() as conn:
            cur: _cursor = conn.cursor(cursor_factory=DictCursor)
            cur.execute(Settings().dict()["universal_query"].format(table, state))
            logger.info(f"Loading data from {table}")
            while data := cur.fetchmany(size):
                yield data
