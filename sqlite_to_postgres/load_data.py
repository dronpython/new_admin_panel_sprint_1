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

    # ToDo: fix contenx manager
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

    def insert_data(self, table, columns, data):
        template = str(tuple(['%s' for _ in range(len(data))])).replace("'", "")
        columns = str(columns).replace("created_at", "created").replace("updated_at", "modified").replace("'", "")
        cur = self._conn.cursor()
        s = cur.mogrify("INSERT INTO {table} {vals} VALUES {template} ON CONFLICT (id) DO NOTHING".format(table=table,
                                                                                                          vals=columns,
                                                                                                          template=template), data)
        print(s)
        cur.execute(s)
        self._conn.commit()

    def insert_many_of_data(self, table, columns, data):
        columns = str(columns).replace("created_at", "created").replace("updated_at", "modified").replace("'", "")
        template = str(tuple(['%s' for _ in range(len(data[0]))])).replace("'", "")
        cur = self._conn.cursor()
        args_str = ','.join(cur.mogrify(template, tuple(x.values())).decode('utf-8') for x in data)
        strg = f"INSERT INTO {table} {columns} VALUES " + args_str + " ON CONFLICT (id) DO NOTHING"
        print(strg)
        cur.execute(strg)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    film_works_sql = sqlite_loader.load_data("film_work")
    for data in film_works_sql:
        postgres_saver.insert_many_of_data("content.film_work",
                                           tuple(data[0].keys()),
                                           data)

    persons_sql = sqlite_loader.load_data("person")
    for data in persons_sql:
        postgres_saver.insert_many_of_data("content.person", tuple(data[0].keys()), data)

    genres_sql = sqlite_loader.load_data("genre")
    for data in genres_sql:
        postgres_saver.insert_many_of_data("content.genre", tuple(data[0].keys()), data)

    genre_film_works_sql = sqlite_loader.load_data("genre_film_work")
    for data in genre_film_works_sql:
        postgres_saver.insert_many_of_data("content.genre_film_work", tuple(data[0].keys()), data)

    person_film_works_sql = sqlite_loader.load_data("person_film_work")
    for data in person_film_works_sql:
        postgres_saver.insert_many_of_data("content.person_film_work", tuple(data[0].keys()), data)

    film_works_psql = postgres_saver.load_data("content.film_work")
    persons_psql = postgres_saver.load_data("content.person")
    genres_psql = postgres_saver.load_data("content.genre")
    person_film_works_psql = postgres_saver.load_data("content.person_film_work")
    genre_film_works_psql = postgres_saver.load_data("content.genre_film_work")

    assert len(list(film_works_sql)) == len(list(film_works_psql)), \
        f"{str(len(list(film_works_sql)))} != {len(list(film_works_psql))}"

    assert len(list(persons_sql)) == len(persons_psql), \
        f"{str(len(list(persons_sql)))} != {len(list(persons_psql))}"

    assert len(list(genres_sql)) == len(genres_psql), \
        f"{str(len(list(genres_sql)))} != {len(list(genres_psql))}"

    assert len(list(genre_film_works_sql)) == len(genre_film_works_psql), \
        f"{str(len(list(genre_film_works_sql)))} != {len(list(genre_film_works_psql))}"

    assert len(list(person_film_works_sql)) == len(person_film_works_psql), \
        f"{str(len(list(persons_sql)))} != {len(list(persons_psql))}"

    #
    # for _ in range(len(list(film_works_psql))):
    #     assert film_works_sql[_]["id"] == film_works_psql[_]["id"], \
    #         f'\n{film_works_sql[_]["id"]}\n{film_works_psql[_]["id"]}'
    #
    #     assert film_works_sql[_]["title"] == film_works_psql[_]["title"], \
    #         f'\n{film_works_sql[_]["title"]}\n{film_works_psql[_]["title"]}'
    #
    #     assert film_works_sql[_]["description"] == film_works_psql[_]["description"], \
    #         f'\n{film_works_sql[_]["description"]}\n{film_works_psql[_]["description"]}'
    #
    #     assert film_works_sql[_]["creation_date"] == film_works_psql[_]["creation_date"], \
    #         f'\n{film_works_sql[_]["creation_date"]}\n{film_works_psql[_]["creation_date"]}'
    #
    #     assert film_works_sql[_]["file_path"] == film_works_psql[_]["file_path"], \
    #         f'\n{film_works_sql[_]["file_path"]}\n{film_works_psql[_]["file_path"]}'
    #
    #     assert film_works_sql[_]["rating"] == film_works_sql[_]["rating"], \
    #         f'\n{film_works_sql[_]["rating"]}\n{film_works_psql[_]["rating"]}'
    #
    #     assert film_works_sql[_]["type"] == film_works_sql[_]["type"], \
    #         f'\n{film_works_sql[_]["type"]}\n{film_works_psql[_]["type"]}'
    #
    #     assert film_works_sql[_]["created_at"].split(".")[0] == str(
    #         film_works_psql[_]["created"]).split(".")[0],\
    #         f'\n{film_works_sql[_]["created_at"].split(".")[0]}\n{str(film_works_psql[_]["created"]).split(".")[0]}'
    #
    #     assert film_works_sql[_]["updated_at"].split(".")[0] == str(film_works_psql[_]["modified"]).split(".")[0], \
    #         f'\n{film_works_sql[_]["updated_at"].split(".")[0]}\n{film_works_psql[_]["modified"].split(".")[0]}'
    #
    # assert len(persons_sql) == len(persons_psql)
    # assert len(genres_sql) == len(genres_psql)
    # assert len(genre_film_works_sql) == len(genre_film_works_psql)
    # assert len(person_film_works_sql) == len(person_film_works_psql)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_db', 'user': 'app', 'password': '123qwe',
           'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
