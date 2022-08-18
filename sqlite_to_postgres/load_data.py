import sqlite3

import psycopg2
import uuid
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from dataclasses import dataclass, field


# @dataclass
# class Movie:
#     type: str
#     updated_at: str
#     created_at: str
#     file_path: str
#     creation_date: str
#     title: str
#     description: str
#     rating: float = field(default=0.0)
#     id: uuid.UUID = field(default_factory=uuid.uuid4)


class SQLiteLoader:
    def __init__(self, conn):
        self._conn = conn

    @contextmanager
    def conn_context(self, db_path: str):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn  # С конструкцией yield вы познакомитесь в следующем модуле
        # Пока воспринимайте её как return, после которого код может продолжить выполняться дальше
        conn.close()

    def load_data(self, table):
        with self._conn:
            self._conn.row_factory = sqlite3.Row
            curs = self._conn.cursor()
            curs.execute(f"SELECT * FROM {table};")
            data = curs.fetchall()
            return data


class PostgresSaver:

    def __init__(self, conn):
        self._conn = conn

    def insert_data(self, table, columns, data: tuple):
        cur = self._conn.cursor()
        data = list(data)

        for item in data:
            item_index = data.index(item)
            if isinstance(item, str):
                data[item_index] = item.replace('"', "'").replace("None", "Null").replace("'", "''")

        data = tuple(data)
        insert_string = "INSERT INTO {} {} VALUES {} ON CONFLICT (id) DO NOTHING".format(table, columns, data)
        print(insert_string)
        cur.execute(insert_string)
        self._conn.commit()

    # def insert_data_film_work(self, data: tuple):
    #     cur = self._conn.cursor()
    #     data = list(data)
    #
    #     for item in data:
    #         item_index = data.index(item)
    #         if isinstance(item, str):
    #             data[item_index] = item.replace('"', "'").replace("None", "Null").replace("'", "''")
    #
    #     data = tuple(data)
    #     insert_string = "INSERT INTO content.film_work " \
    #                     "(id, title, description, creation_date, " \
    #                     "file_path, rating, type, created, modified) " \
    #                     "VALUES {} ON CONFLICT (id) DO NOTHING".format(data)
    #     insert_string = insert_string.replace("None", "Null").replace('"', "'")
    #     print(insert_string)
    #     cur.execute(insert_string)
    #     self._conn.commit()

    # def insert_data_person(self, data):
    #     cur = self._conn.cursor()
    #     data = list(data)
    #     for item in data:
    #         item_index = data.index(item)
    #         if isinstance(item, str):
    #             data[item_index] = item.replace('"', "'").replace("None", "Null").replace("'", "''")
    #     data = tuple(data)
    #     insert_string = "INSERT INTO content.person " \
    #                     "(id, full_name, created, modified) " \
    #                     "VALUES {} ON CONFLICT (id) DO NOTHING".format(data)
    #     insert_string = insert_string.replace("None", "Null").replace('"', "'")
    #     print(insert_string)
    #     cur.execute(insert_string)
    #     self._conn.commit()

    # def insert_data_genre(self, data):
    #     cur = self._conn.cursor()
    #     data = list(data)
    #     for item in data:
    #         item_index = data.index(item)
    #         if isinstance(item, str):
    #             data[item_index] = item.replace('"', "'").replace("None", "Null").replace("'", "''")
    #     data = tuple(data)
    #     insert_string = "INSERT INTO content.genre " \
    #                     "(id, name, description, created, modified) " \
    #                     "VALUES {} ON CONFLICT (id) DO NOTHING".format(data)
    #     insert_string = insert_string.replace("None", "Null").replace('"', "'")
    #     print(insert_string)
    #     cur.execute(insert_string)
    #     self._conn.commit()

    # def insert_data_genre_film_work(self, data: tuple):
    #     cur = self._conn.cursor()
    #     data = list(data)
    #     for item in data:
    #         item_index = data.index(item)
    #         if isinstance(item, str):
    #             data[item_index] = item.replace('"', "'").replace("None", "Null").replace("'", "''")
    #     data = tuple(data)
    #     insert_string = "INSERT INTO content.genre_film_work " \
    #                     "(id, film_work_id, genre_id, created) " \
    #                     "VALUES {} ON CONFLICT (id) DO NOTHING".format(data)
    #     insert_string = insert_string.replace("None", "Null").replace('"', "'")
    #     print(insert_string)
    #     cur.execute(insert_string)
    #     self._conn.commit()
    #
    # def insert_data_person_film_work(self, data):
    #     cur = self._conn.cursor()
    #     data = list(data)
    #     for item in data:
    #         item_index = data.index(item)
    #         if isinstance(item, str):
    #             data[item_index] = item.replace('"', "'").replace("None", "Null").replace("'", "''")
    #     data = tuple(data)
    #     insert_string = "INSERT INTO content.person_film_work " \
    #                     "(id, film_work_id, person_id, role, created) " \
    #                     "VALUES {} ON CONFLICT (id) DO NOTHING".format(data)
    #     insert_string = insert_string.replace("None", "Null").replace('"', "'")
    #     print(insert_string)
    #     cur.execute(insert_string)
    #     self._conn.commit()

    def save_all_film_works(self, data):
        cols = "(id, title, description, creation_date, file_path, rating, type, created, modified)"
        for row in data:
            self.insert_data("content.film_work", cols, tuple(row))

    def save_all_persons(self, data):
        cols = "(id, full_name, created, modified)"
        for row in data:
            self.insert_data("content.person", cols, tuple(row))

    def save_all_genres(self, data):
        cols = "(id, name, description, created, modified)"
        for row in data:
            self.insert_data("content.genre", cols, tuple(row))

    def save_all_genre_film_works(self, data):
        cols = "(id, film_work_id, genre_id, created)"
        for row in data:
            self.insert_data("content.genre_film_work", cols, tuple(row))

    def save_all_person_film_works(self, data):
        cols = "(id, film_work_id, person_id, role, created)"
        for row in data:
            self.insert_data("content.person_film_work", cols, tuple(row))


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn  # С конструкцией yield вы познакомитесь в следующем модуле
    # Пока воспринимайте её как return, после которого код может продолжить выполняться дальше
    conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    film_works = sqlite_loader.load_data("film_work")
    postgres_saver.save_all_film_works(film_works)

    persons = sqlite_loader.load_data("person")
    postgres_saver.save_all_persons(persons)

    genres = sqlite_loader.load_data("genre")
    postgres_saver.save_all_genres(genres)
    #
    genre_film_works = sqlite_loader.load_data("genre_film_work")
    postgres_saver.save_all_genre_film_works(genre_film_works)

    person_film_works = sqlite_loader.load_data("person_film_work")
    postgres_saver.save_all_person_film_works(person_film_works)




if __name__ == '__main__':
    dsl = {'dbname': 'movies_db', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
