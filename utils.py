import psycopg2
import psycopg2.extras
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler


def run_server(server_address=('', 8080), handler=BaseHTTPRequestHandler):
    httpd = HTTPServer(server_address, handler)
    httpd.serve_forever()


def parse_query(query_string):
    """
    Parses query string.
    Return tuple of string query_path, GET query parameters as dict
    like {'param_name1': ['val1', 'val2'], 'param_name2': ['val1'], ...}.
    """
    parsed_url = urlparse(query_string)
    query_path = parsed_url.path
    query_params = parse_qs(parsed_url.query)
    return query_path, query_params


def db_connect():
    """ Connect with the WG Forge test database """
    return psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='wg_forge_db',
        user='wg_forge',
        password='42a'
    )


def db_query(query, many=True):
    """ Query results """
    with db_connect() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(query)
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)
            return cur.fetchall() if many else cur.fetchone()


def db_query_realdict(query, many=True):
    """ Query results as dict: {'key': ['val1', 'val2',...], ...} """
    with db_connect() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            try:
                cur.execute(query)
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)
            return cur.fetchall() if many else cur.fetchone()


def db_table_size(table_name):
    """ Count of records in table """
    with db_connect() as conn:
        with conn.cursor() as cur:
            query = 'SELECT COUNT(*) FROM {}'.format(table_name)
            try:
                cur.execute(query)
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)
            res = cur.fetchone()
    return res[0]


def db_table_column_names(table_name):
    """ Column names of table """
    with db_connect() as conn:
        with conn.cursor() as cur:
            query = 'SELECT * FROM {}'.format(table_name)
            try:
                cur.execute(query)
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)
    return [desc[0] for desc in cur.description]


def dict_to_db(table, data):
    """ Insert query data (as dict) into db """
    columns = ', '.join("%({})s".format(key) for key in data.keys())
    query = 'INSERT INTO {} VALUES ({})'.format(table, columns)

    # convert possible integer values to string
    data = dict((key, str(val)) for key, val in data.items())

    with db_connect() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(query, data)
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)
                return False
            else:
                conn.commit()
                return True
