import sqlite3
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from contextlib import contextmanager


class SQLiteLoader:
    def __init__(self, conn):
        self._conn = conn

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @contextmanager
    def conn_context(self):
        self._conn.row_factory = self.dict_factory
        yield self._conn  # С конструкцией yield вы познакомитесь в следующем модуле
        # Пока воспринимайте её как return, после которого код может продолжить выполняться дальше
        self._conn.close()

    def load_data(self, table):
        with self.conn_context() as conn:
            curs = conn.cursor()
            curs.execute(f"SELECT * FROM {table};")
            data = curs.fetchall()
            return data


class PostgresSaver:

    def __init__(self, conn):
        self._conn = conn

    def load_data(self, table):
        cur = self._conn.cursor()
        cur.execute(f"SELECT * FROM {table};")
        data = cur.fetchall()
        return data

    def insert_data(self, table, columns, data: tuple):
        cur = self._conn.cursor()
        data = list(data)

        for item in data:
            item_index = data.index(item)
            if isinstance(item, str):
                data[item_index] = item.replace('"', "'").replace("None", "Null").replace("'", "''")

        data = tuple(data)
        insert_string = "INSERT INTO {} {} VALUES {} ON CONFLICT (id) DO NOTHING".format(table, columns, data)
        insert_string = insert_string.replace('"', "'").replace("None", "Null").replace('"', "'")
        print(insert_string)
        cur.execute(insert_string)
        self._conn.commit()

    def save_all_film_works(self, data):
        cols = "(id, title, description, creation_date, file_path, rating, type, created, modified)"
        for row in data:
            self.insert_data("content.film_work", cols, row.values())

    def save_all_persons(self, data):
        cols = "(id, full_name, created, modified)"
        for row in data:
            self.insert_data("content.person", cols, row.values())

    def save_all_genres(self, data):
        cols = "(id, name, description, created, modified)"
        for row in data:
            self.insert_data("content.genre", cols, row.values())

    def save_all_genre_film_works(self, data):
        cols = "(id, film_work_id, genre_id, created)"
        for row in data:
            self.insert_data("content.genre_film_work", cols, row.values())

    def save_all_person_film_works(self, data):
        cols = "(id, film_work_id, person_id, role, created)"
        for row in data:
            self.insert_data("content.person_film_work", cols, row.values())


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    film_works_sql = sqlite_loader.load_data("film_work")
    postgres_saver.save_all_film_works(film_works_sql)
    film_works_psql = postgres_saver.load_data("content.film_work")

    persons_sql = sqlite_loader.load_data("person")
    postgres_saver.save_all_persons(persons_sql)
    persons_psql = postgres_saver.load_data("content.person")

    genres_sql = sqlite_loader.load_data("genre")
    postgres_saver.save_all_genres(genres_sql)
    genres_psql = postgres_saver.load_data("content.genres")

    genre_film_works_sql = sqlite_loader.load_data("genre_film_work")
    postgres_saver.save_all_genre_film_works(genre_film_works_sql)
    genre_film_works_psql = postgres_saver.load_data("content.genre_film_work")

    person_film_works_sql = sqlite_loader.load_data("person_film_work")
    postgres_saver.save_all_person_film_works(person_film_works_sql)
    person_film_works_psql = postgres_saver.load_data("content.person_film_work")

    assert len(film_works_sql) == len(film_works_psql)

    for _ in range(len(film_works_psql)):
        assert film_works_sql[_]["id"] == film_works_psql[_]["id"], \
            f'\n{film_works_sql[_]["id"]}\n{film_works_psql[_]["id"]}'

        assert film_works_sql[_]["title"] == film_works_psql[_]["title"], \
            f'\n{film_works_sql[_]["title"]}\n{film_works_psql[_]["title"]}'

        assert film_works_sql[_]["description"] == film_works_psql[_]["description"], \
            f'\n{film_works_sql[_]["description"]}\n{film_works_psql[_]["description"]}'

        assert film_works_sql[_]["creation_date"] == film_works_psql[_]["creation_date"], \
            f'\n{film_works_sql[_]["creation_date"]}\n{film_works_psql[_]["creation_date"]}'

        assert film_works_sql[_]["file_path"] == film_works_psql[_]["file_path"], \
            f'\n{film_works_sql[_]["file_path"]}\n{film_works_psql[_]["file_path"]}'

        assert film_works_sql[_]["rating"] == film_works_sql[_]["rating"], \
            f'\n{film_works_sql[_]["rating"]}\n{film_works_psql[_]["rating"]}'

        assert film_works_sql[_]["type"] == film_works_sql[_]["type"], \
            f'\n{film_works_sql[_]["type"]}\n{film_works_psql[_]["type"]}'

        assert film_works_sql[_]["created_at"].split(".")[0] == str(
            film_works_psql[_]["created"]).split(".")[0],\
            f'\n{film_works_sql[_]["created_at"].split(".")[0]}\n{str(film_works_psql[_]["created"]).split(".")[0]}'

        assert film_works_sql[_]["updated_at"].split(".")[0] == str(film_works_psql[_]["modified"]).split(".")[0], \
            f'\n{film_works_sql[_]["updated_at"].split(".")[0]}\n{film_works_psql[_]["modified"].split(".")[0]}'

    assert len(persons_sql) == len(persons_psql)
    assert len(genres_sql) == len(genres_psql)
    assert len(genre_film_works_sql) == len(genre_film_works_psql)
    assert len(person_film_works_sql) == len(person_film_works_psql)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_db', 'user': 'app', 'password': '123qwe',
           'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
