import psycopg2
import psycopg2.extras


def connect():
    return psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='wg_forge_db',
        user='wg_forge',
        password='42a'
    )


def db_query_realdict(query):
    with connect() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            try:
                cur.execute(query)
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)
            res = cur.fetchall()
    return res
