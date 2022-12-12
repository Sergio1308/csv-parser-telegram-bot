import db_config as db

from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager

pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=db.DATABASE_URI)


@contextmanager
def get_connection():
    connection = pool.getconn()
    try:
        yield connection
    finally:
        pool.putconn(connection)
