import psycopg2


def db_connect():
    return psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='wg_forge_db',
        user='wg_forge',
        password='42a'
    )
