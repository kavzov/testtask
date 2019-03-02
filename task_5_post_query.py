import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from db_connect import db_query_realdict, db_table_column_names, dict_to_db
from cats_colors_info import get_colors


DB_TABLE = 'cats'


class NotPositiveIntegerError(Exception):
    pass


class PostQuery:
    """
    Class for handle POST query.
    Provides is_valid method for POST query string.
    """
    VALID_PATH = '/cats'
    VALID_QUERY_PARAMS = ['attribute', 'limit', 'offset', 'order']
    VALID_ORDER_VALUES = ['asc', 'desc']

    def __init__(self):
        self.messages = []
        self.post_data = {}

    def _exist_namesake(self):
        """ Return QueryDict with the same name cat """
        namesake = db_query_realdict("SELECT * FROM {} WHERE name='{}'".format(DB_TABLE, self.post_data['name']))
        if namesake:
            return True

    def _valid_json(self):
        """ Validates string for JSON view. Return python dict if valid JSON, None otherwise """
        try:
            self.post_data = json.loads(self.post_data)
            return True
        except json.JSONDecodeError:
            self.messages.append('Error: invalid JSON')

    def _valid_attrs(self, valid_attrs):
        """ Validates attrs by comparing with valid attrs list """
        attrs = sorted(list(self.post_data))
        valid_attrs = sorted(valid_attrs)
        if not attrs == valid_attrs:
            self.messages.append('Error: invalid attributes')
            return False
        else:
            return True

    def _valid_color(self, colors):
        """ Validates color. It must be one of valid colors list """
        if self.post_data['color'] not in colors:
            self.messages.append('Error: invalid color')
            return False
        else:
            return True

    def _valid_length(self, items):
        is_valid_length = True
        for item in items:
            length = self.post_data['{}_length'.format(item)]
            try:
                length = int(length)
                if length <= 0:
                    raise NotPositiveIntegerError
            except (ValueError, NotPositiveIntegerError):
                self.messages.append('Error: {} length is not positive integer'.format(item))
                is_valid_length = False
        return is_valid_length

    def _valid_name(self):
        cat_name = self.post_data['name']
        if not isinstance(cat_name, str):
            self.messages.append('Error: cat name not a string')
            return False

        if cat_name == '':
            self.messages.append('Error: empty name')
            return False

        if self._exist_namesake():
            self.messages.append('Error: cat {} already exists'. format(cat_name))
            return False

        return True

    def is_valid(self, valid_attrs, valid_colors):
        """
        Validates POST query
        """
        self.messages = []

        if not self._valid_json():
            return False

        if not self._valid_attrs(valid_attrs):
            return False

        if not self._valid_color(valid_colors):
            return False

        if not self._valid_length(['tail', 'whiskers']):
            return False

        if not self._valid_name():
            return False

        return True


class WGTestHTTPRequestHandler(BaseHTTPRequestHandler):
    DB_TABLE = 'cats'

    def __init__(self, *args, **kwargs):
        self.query = PostQuery()
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def response(self, content):
        # Send response
        self._set_headers()
        self.wfile.write(json.dumps(content).encode('utf-8'))

    # ----------------------------- #
    # POST request handle

    def do_POST(self):
        """ Handles POST request """
        valid_attr_values = db_table_column_names(self.DB_TABLE)
        valid_colors = get_colors()

        # get POST query
        data_length = int(self.headers['Content-Length'])
        self.query.post_data = self.rfile.read(data_length).decode('utf-8')

        # if query is valid - store data to db and send success message to client
        if self.query.is_valid(valid_attr_values, valid_colors):
            # Store cat info to db
            dict_to_db(self.DB_TABLE, self.query.post_data) and \
                self.response("Cat {} stored to database.\n".format(self.query.post_data['name']))
        else:
            # if errors occurred in the query send error message
            self.response(self.query.messages)
            return


def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, WGTestHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
