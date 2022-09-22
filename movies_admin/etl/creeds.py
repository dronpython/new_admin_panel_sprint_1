import os
from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):

    envs_file = os.path.abspath(".env")
    load_dotenv(envs_file)

    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")

    es_server = os.environ.get("ES_SERVER")

    dsl = {'dbname': db_name, 'user': db_user, 'password': db_password,
           'host': db_host, 'port': db_port}

    universal_query = """
SELECT
   fw.id,
   fw.title,
   fw.description,
   fw.rating as imdb_rating,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null and pfw.role = 'actor'),
       '[]'
   ) as actors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null and pfw.role = 'writer'),
       '[]'
   ) as writers,
   array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director') as director,
   array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor') as actors_names,
   array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') as writers_names,
   array_agg(DISTINCT g.name) as genre
FROM content.film_work fw
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
WHERE {}.modified > '{}'
GROUP BY fw.id
ORDER BY fw.modified;
"""