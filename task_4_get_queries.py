import json
import psycopg2
import psycopg2.extras
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from db_connect import connect


def param_in_query(param, query):
    return query.get(param, None)


def multivalued_param(params_list):
    return len(params_list) > 1


class TestTaskHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def response(self, content):
        # Send response
        self._set_headers()
        self.wfile.write(json.dumps(content).encode('utf-8'))

    def parse_query(self):
        # Return full query path and GET query params
        parsed_url = urlparse(self.path)
        query_path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        return query_path, query_params

    def get_attr_names(self):
        with connect() as conn:
            with conn.cursor() as cur:
                query = 'SELECT * FROM cats'
                try:
                    cur.execute(query)
                except psycopg2.Error as e:
                    print("Psycopg2 error: ", e)
        return [desc[0] for desc in cur.description]

    def get_dbtable_size(self, table_name):
        with connect() as conn:
            with conn.cursor() as cur:
                query = 'SELECT COUNT(*) FROM {}'.format(table_name)
                try:
                    cur.execute(query)
                except psycopg2.Error as e:
                    print("Psycopg2 error: ", e)
                res = cur.fetchone()
        return res[0]

    def valid_path(self, path, valid_path):
        return path.startswith(valid_path)

    def valid_param(self, param, valid_params):
        return param in valid_params

    def valid_attr(self, attr, valid_attrs):
        return attr in valid_attrs

    def do_GET(self):
        valid_path = '/cats'
        valid_query_param_names = ['attribute', 'color', 'limit', 'offset', 'order']
        valid_attr_values = self.get_attr_names()
        valid_order_values = ['asc', 'desc']
        messages = []

        # Get query path and params
        query_path, query_params = self.parse_query()

        # CHECK ERRORS
        # check query path
        # if it not starts with '/cats'
        if not self.valid_path(query_path, valid_path):
            messages.append("Error: invalid path '{}'. Expected '{}'".
                            format(query_path, valid_path))

        # check query param names
        for param_name in query_params:
            if not self.valid_param(param_name, valid_query_param_names):
                messages.append("Error: invalid query parameter '{}'. Allowed parameters: {}".
                                format(param_name, ', '.join(valid_query_param_names)))

        # check valid attributes
        if param_in_query('attribute', query_params):
            for attr in query_params['attribute']:
                if not self.valid_attr(attr, valid_attr_values):
                    messages.append("Error: invalid attribute '{}'. Allowed attributes: {}".
                                    format(attr, ', '.join(valid_attr_values)))

        # check valid order
        # if query_params.get('order', None):
        if param_in_query('order', query_params):
            # 1> order parameters given
            if len(query_params['order']) > 1:
                messages.append("Error: {} order parameters given. 1 expected".format(len(query_params['order'])))
            else:
                order = query_params['order'][0]
                # order not 'asc' or 'desc'
                if order not in valid_order_values:
                    messages.append("Error: invalid order '{}'. Allowed values: {}.".
                                    format(order, ', '.join(valid_order_values)))

        # check valid offset
        if param_in_query('offset', query_params):
            # 1> offset parameters given
            if multivalued_param(query_params['offset']):
                messages.append("Error: {} 'offset' parameters given. 1 expected".format(len(query_params['offset'])))
            else:
                offset = query_params['offset'][0]
                # offset is not integer
                if not offset.isdigit():
                    messages.append("Error: invalid offset '{}'. Integer expected.".format(offset))
                else:
                    # offset (single and it int number) >= records in table
                    cats_number = self.get_dbtable_size('cats')
                    if int(offset) >= cats_number:
                        messages.append("Warning: empty set because of given offset {} greater than allowed {}".
                                        format(offset, cats_number-1))

        # check valid limit
        if param_in_query('limit', query_params):
            # 1> offset parameters given
            if multivalued_param(query_params['limit']):
                messages.append("Error: {} 'limit' parameters given. 1 expected".format(len(query_params['limit'])))
            else:
                limit = query_params['limit'][0]
                # limit is not integer
                if not limit.isdigit():
                    messages.append("Error: invalid limit '{}'. Integer expected.".format(limit))

        if messages:
            self.response(messages)
            return

        # all right - do query
        query = 'SELECT * FROM cats'

        # attributes in query string
        if query_params.get('attribute', None):
            query += ' ORDER BY '
            # may be 1>= attrs
            for attr in query_params['attribute']:
                query += '{}, '.format(attr)
            query = query.rstrip(', ')

        # order in query string
        if query_params.get('order', None):
            order = query_params['order'][0]
            query += ' {}'.format(order.upper())

        # offset in query string
        if query_params.get('offset', None):
            offset = query_params['offset'][0]
            query += ' OFFSET {}'.format(offset)

        # limit in query string
        if query_params.get('limit', None):
            limit = query_params['limit'][0]
            query += ' LIMIT {}'.format(limit)

        # query
        with connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                try:
                    cur.execute(query)
                except psycopg2.Error as e:
                    print("Psycopg2 error: ", e)
                res = cur.fetchall()

        self.response(res)


def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, TestTaskHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
