CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone default now(),
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone default now(),
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES content.film_work(id),
    person_id uuid NOT NULL REFERENCES content.person(id),
    role VARCHAR(100) NOT NULL,
    created timestamp with time zone default now()
);

CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date);

CREATE INDEX person_full_name_idx ON content.person(full_name);

CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created TIMESTAMP WITH TIME ZONE default now(),
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid primary key,
    genre_id uuid not null references content.genre(id),
    film_work_id uuid not null references content.film_work(id),
    created timestamp with time zone default now()
);
