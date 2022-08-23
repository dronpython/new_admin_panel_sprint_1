

def check_consistence_of_film_works(film_works_sql, film_works_psql):

    assert len(film_works_sql) == len(film_works_psql), \
        f"{str(len(list(film_works_sql)))} != {len(list(film_works_psql))}"

    for _ in range(len(list(film_works_psql))):
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
            f'\n{film_works_sql[_]["created_at"].split(".")[0]}\n' \
            f'{str(film_works_psql[_]["created"]).split(".")[0]}'

        assert film_works_sql[_]["updated_at"].split(".")[0] == str(
            film_works_psql[_]["modified"]).split(".")[0], \
            f'\n{film_works_sql[_]["updated_at"].split(".")[0]}\n' \
            f'{film_works_psql[_]["modified"].split(".")[0]}'


def check_consistence_of_person(persons_sql, persons_psql):
    #
    # persons_sql = sqlite_loader.load_all_data("person")
    # persons_psql = postgres_saver.load_data("content.person")

    assert len(persons_sql) == len(persons_psql), \
        f"{str(len(list(persons_sql)))} != {len(list(persons_psql))}"

    for _ in range(len(list(persons_psql))):
        assert persons_sql[_]["id"] == persons_psql[_]["id"], \
            f'\n{persons_sql[_]["id"]}\n{persons_psql[_]["id"]}'

        assert persons_sql[_]["full_name"] == persons_psql[_]["full_name"], \
            f'\n{persons_psql[_]["full_name"]}\n{persons_psql[_]["full_name"]}'

        assert persons_sql[_]["created_at"].split(".")[0] == str(
            persons_psql[_]["created"]).split(".")[0],\
            f'\n{persons_sql[_]["created_at"].split(".")[0]}\n' \
            f'{str(persons_psql[_]["created"]).split(".")[0]}'

        assert persons_sql[_]["updated_at"].split(".")[0] == str(
            persons_psql[_]["modified"]).split(".")[0], \
            f'\n{persons_sql[_]["updated_at"].split(".")[0]}\n' \
            f'{persons_psql[_]["modified"].split(".")[0]}'


def check_consistence_of_genre(genre_sql, genre_psql):

    # genre_sql = sqlite_loader.load_all_data("genre")
    # genre_psql = postgres_saver.load_data("content.genre")

    assert len(genre_sql) == len(genre_psql), \
        f"{str(len(list(genre_sql)))} != {len(list(genre_psql))}"

    for _ in range(len(list(genre_psql))):
        assert genre_sql[_]["id"] == genre_psql[_]["id"], \
            f'\n{genre_sql[_]["id"]}\n{genre_psql[_]["id"]}'

        assert genre_sql[_]["name"] == genre_psql[_]["name"], \
            f'\n{genre_sql[_]["name"]}\n{genre_psql[_]["name"]}'

        assert genre_sql[_]["description"] == genre_psql[_]["description"], \
            f'\n{genre_sql[_]["description"]}\n{genre_psql[_]["description"]}'

        assert genre_sql[_]["created_at"].split(".")[0] == str(
            genre_psql[_]["created"]).split(".")[0],\
            f'\n{genre_sql[_]["created_at"].split(".")[0]}\n' \
            f'{str(genre_psql[_]["created"]).split(".")[0]}'

        assert genre_sql[_]["updated_at"].split(".")[0] == str(
            genre_psql[_]["modified"]).split(".")[0], \
            f'\n{genre_sql[_]["updated_at"].split(".")[0]}\n' \
            f'{genre_psql[_]["modified"].split(".")[0]}'


def check_consistence_of_person_film_work(person_film_work_sql, person_film_work_psql):
    # person_film_work_sql = sqlite_loader.load_all_data("person_film_work")
    # person_film_work_psql = postgres_saver.load_data("content.person_film_work")

    assert len(person_film_work_sql) == len(person_film_work_psql), \
        f"{str(len(list(person_film_work_sql)))} != {len(list(person_film_work_psql))}"

    for _ in range(len(list(person_film_work_psql))):
        assert person_film_work_sql[_]["id"] == person_film_work_psql[_]["id"], \
            f'\n{person_film_work_sql[_]["id"]}\n{person_film_work_psql[_]["id"]}'

        assert person_film_work_sql[_]["film_work_id"] == person_film_work_psql[_]["film_work_id"], \
            f'\n{person_film_work_sql[_]["film_work_id"]}\n{person_film_work_psql[_]["film_work_id"]}'

        assert person_film_work_sql[_]["person_id"] == person_film_work_psql[_]["person_id"], \
            f'\n{person_film_work_sql[_]["person_id"]}\n{person_film_work_psql[_]["person_id"]}'

        assert person_film_work_sql[_]["role"] == person_film_work_psql[_]["role"], \
            f'\n{person_film_work_sql[_]["role"]}\n{person_film_work_psql[_]["role"]}'

        assert person_film_work_sql[_]["created_at"].split(".")[0] == str(
            person_film_work_psql[_]["created"]).split(".")[0], \
            f'\n{person_film_work_sql[_]["created_at"].split(".")[0]}\n' \
            f'{str(person_film_work_psql[_]["created"]).split(".")[0]}'


def check_consistence_of_genre_film_work(genre_film_work_sql, genre_film_work_psql):
    # genre_film_work_sql = sqlite_loader.load_all_data("genre_film_work")
    # genre_film_work_psql = postgres_saver.load_data("content.genre_film_work")

    assert len(genre_film_work_sql) == len(genre_film_work_sql), \
        f"{str(len(list(genre_film_work_sql)))} != {len(list(genre_film_work_psql))}"

    for _ in range(len(list(genre_film_work_sql))):
        assert genre_film_work_sql[_]["id"] == genre_film_work_psql[_]["id"], \
            f'\n{genre_film_work_sql[_]["id"]}\n{genre_film_work_psql[_]["id"]}'

        assert genre_film_work_sql[_]["film_work_id"] == genre_film_work_psql[_]["film_work_id"], \
            f'\n{genre_film_work_sql[_]["film_work_id"]}\n{genre_film_work_psql[_]["film_work_id"]}'

        assert genre_film_work_sql[_]["genre_id"] == genre_film_work_psql[_]["genre_id"], \
            f'\n{genre_film_work_sql[_]["genre_id"]}\n{genre_film_work_psql[_]["genre_id"]}'

        assert genre_film_work_sql[_]["created_at"].split(".")[0] == str(
            genre_film_work_psql[_]["created"]).split(".")[0], \
            f'\n{genre_film_work_sql[_]["created_at"].split(".")[0]}\n' \
            f'{str(genre_film_work_psql[_]["created"]).split(".")[0]}'
