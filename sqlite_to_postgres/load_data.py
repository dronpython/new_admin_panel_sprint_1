import sqlite3
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from new_admin_panel_sprint_1.sqlite_to_postgres.tests.check_consistency import *


class SQLiteLoader:
    def __init__(self, conn):
        self._conn = conn

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @contextmanager
    def conn_context(self, use_factory=False):
        if use_factory:
            self._conn.row_factory = self.dict_factory
        yield self._conn
        # self._conn.close()

    def load_data(self, table):
        with self.conn_context(use_factory=True) as conn:
            curs = conn.cursor()
            curs.execute(f"SELECT * FROM {table};")
            while True:
                data = curs.fetchmany(100)
                if not data:
                    break
                yield data

    def load_all_data(self, table):
        with self.conn_context(use_factory=True) as conn:
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

    def insert_many_of_data(self, table, columns, data):
        columns = str(columns).replace(
            "created_at", "created").replace(
            "updated_at", "modified").replace(
            "'", "")
        template = str(tuple(['%s' for _ in range(len(data[0]))])).replace("'", "")
        cur = self._conn.cursor()
        args_str = ','.join(cur.mogrify(template, tuple(x.values())).decode('utf-8') for x in data)
        strg = f"INSERT INTO {table} {columns} VALUES " + args_str + " ON CONFLICT (id) DO NOTHING"
        cur.execute(strg)


def load_from_sqlite(connection: sqlite3.Connection, pg_connection: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_connection)
    sqlite_loader = SQLiteLoader(connection)

    # Fill "film_work" table of data
    film_works_sql = sqlite_loader.load_data("film_work")
    for data in film_works_sql:
        postgres_saver.insert_many_of_data("content.film_work",
                                           tuple(data[0].keys()),
                                           data)

    # Fill "person" table of data
    persons_sql = sqlite_loader.load_data("person")
    for data in persons_sql:
        postgres_saver.insert_many_of_data("content.person", tuple(data[0].keys()), data)

    # Fill "genre" table of data
    genres_sql = sqlite_loader.load_data("genre")
    for data in genres_sql:
        postgres_saver.insert_many_of_data("content.genre", tuple(data[0].keys()), data)

    # Fill "genre_film_work" table of data
    genre_film_works_sql = sqlite_loader.load_data("genre_film_work")
    for data in genre_film_works_sql:
        postgres_saver.insert_many_of_data("content.genre_film_work", tuple(data[0].keys()), data)

    # Fill "film_work" table of data
    person_film_works_sql = sqlite_loader.load_data("person_film_work")
    for data in person_film_works_sql:
        postgres_saver.insert_many_of_data("content.person_film_work", tuple(data[0].keys()), data)

    # Grab all data for tests from sql tables
    film_works_sql = sqlite_loader.load_all_data("film_work")
    persons_sql = sqlite_loader.load_all_data("person")
    genres_sql = sqlite_loader.load_all_data("genre")
    person_film_works_sql = sqlite_loader.load_all_data("person_film_work")
    genre_film_works_sql = sqlite_loader.load_all_data("genre_film_work")

    # Grab all data for tests from psql tables
    film_works_psql = postgres_saver.load_data("content.film_work")
    persons_psql = postgres_saver.load_data("content.person")
    genres_psql = postgres_saver.load_data("content.genre")
    person_film_works_psql = postgres_saver.load_data("content.person_film_work")
    genre_film_works_psql = postgres_saver.load_data("content.genre_film_work")

    # Check data consistence
    check_consistence_of_film_works(film_works_sql, film_works_psql)
    check_consistence_of_person(persons_sql, persons_psql)
    check_consistence_of_genre(genres_sql, genres_psql)
    check_consistence_of_person_film_work(person_film_works_sql, person_film_works_psql)
    check_consistence_of_genre_film_work(genre_film_works_sql, genre_film_works_psql)


if __name__ == '__main__':
    load_dotenv("../movies_admin/config/.env")
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    dsl = {'dbname': db_name, 'user': db_user, 'password': db_password,
           'host': db_host, 'port': db_port}
    with sqlite3.connect('db.sqlite') as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
