import sqlite3
from os import environ

import psycopg2
import pytest
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

tables_columns = {
    'film_work': {
        'sqlite': 'id,title,description,creation_date,rating,type,created_at,'
                  'updated_at',
        'pg': 'id,title,description,creation_date,rating,type,created,modified'
    },
    'genre': {
        'sqlite': 'id,name,description,created_at,updated_at',
        'pg': 'id,name,description,created,modified'
    },
    'person': {
        'sqlite': 'id,full_name,created_at,updated_at',
        'pg': 'id,full_name,created,modified'
    },
    'genre_film_work': {
        'sqlite': 'id,genre_id,film_work_id,created_at',
        'pg': 'id,genre_id,film_work_id,created'
    },
    'person_film_work': {
        'sqlite': 'id,film_work_id,person_id,role,created_at',
        'pg': 'id,film_work_id,person_id,role,created'
    },
}


@pytest.fixture
def sqlite_cursor():
    db_path = './db.sqlite'
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        yield cursor
    finally:
        cursor.close()
        conn.close()


@pytest.fixture
def pg_cursor():
    load_dotenv()
    dsl = {
        'dbname': environ.get('DB_NAME'),
        'user': environ.get('DB_USER'),
        'password': environ.get('DB_PASSWORD'),
        'host': environ.get('DB_HOST'),
        'port': int(environ.get('DB_PORT')),
        'options': '-c search_path=content'
    }
    with psycopg2.connect(
            **dsl,
            cursor_factory=DictCursor
    ) as pg_conn:
        yield pg_conn.cursor()


def get_count_of_elements_in_table(cursor, table_name) -> int:
    print(cursor)
    query = f'SELECT COUNT(*) FROM {table_name};'
    cursor.execute(query)
    return cursor.fetchone()[0]


def test_row_numbers(sqlite_cursor, pg_cursor):
    """Checks if number of rows are the same in both PG and SQLITE tables."""
    sqlite_rows_number = [
        get_count_of_elements_in_table(sqlite_cursor, table_name)
        for table_name in tables_columns
    ]
    postgres_rows_number = [
        get_count_of_elements_in_table(pg_cursor, table_name)
        for table_name in tables_columns
    ]
    assert sqlite_rows_number == postgres_rows_number


def extract_data_from_db(cursor, fields, table_name):
    query = f"""
    SELECT {fields} FROM {table_name};
    """
    cursor.execute(query)
    for row in cursor.fetchall():
        yield row


def test_data_equality(sqlite_cursor, pg_cursor):
    for table, fields in tables_columns.items():
        sqlite_data = extract_data_from_db(sqlite_cursor, fields['sqlite'],
                                           table)
        pg_data = extract_data_from_db(sqlite_cursor, fields['sqlite'], table)
        for sqlite_row in sqlite_data:
            assert tuple(sqlite_row) == tuple(next(pg_data))
