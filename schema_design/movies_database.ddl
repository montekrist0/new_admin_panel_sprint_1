BEGIN;

CREATE SCHEMA IF NOT EXISTS content;

DROP TYPE IF EXISTS FILM_TYPE;
CREATE TYPE FILM_TYPE AS ENUM ('movie', 'tv_show');

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type FILM_TYPE NOT NULL,
    created timestamp with time zone DEFAULT NOW(),
    modified timestamp with time zone DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone DEFAULT NOW(),
    modified timestamp with time zone DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created timestamp with time zone DEFAULT NOW(),
    modified timestamp with time zone DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    created timestamp with time zone DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    person_id uuid NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    created timestamp with time zone DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);

CREATE INDEX IF NOT EXISTS title_at_film_work_idx ON content.film_work (title);
CREATE INDEX IF NOT EXISTS creation_date_and_rating_at_film_work_idx ON content.film_work (creation_date, rating);

CREATE INDEX IF NOT EXISTS film_work_id_at_genre_film_work_idx ON content.genre_film_work (film_work_id);
CREATE INDEX IF NOT EXISTS genre_id_at_genre_film_work_idx ON content.genre_film_work (genre_id);

CREATE INDEX IF NOT EXISTS genre_film_work_unique_idx ON content.genre_film_work (film_work_id, genre_id);

CREATE INDEX IF NOT EXISTS film_work_id_at_person_film_work_idx ON content.person_film_work (film_work_id);
CREATE INDEX IF NOT EXISTS person_id_at_person_film_work_idx ON content.person_film_work (person_id);

COMMIT;
