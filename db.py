import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_config():
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "dbname": os.getenv("DB_NAME", "resume_screening"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
    }


@contextmanager
def get_connection():
    connection = psycopg2.connect(**get_db_config())
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def fetch_all(query, params=None):
    with get_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()


def fetch_one(query, params=None):
    with get_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()


def execute(query, params=None):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())


def execute_returning_id(query, params=None):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()[0]
