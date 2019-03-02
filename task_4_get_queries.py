import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from db_connect import db_query_realdict, db_table_column_names, db_table_size


class Checker:
    """ Class checker for query string """
    VALID_PATH = '/cats'
    VALID_QUERY_PARAMS = ['attribute', 'limit', 'offset', 'order']
    VALID_ORDER_VALUES = ['asc', 'desc']

    def __init__(self):
        self.messages = []

    @staticmethod
    def parse_query(query_string):
        """
        Return string query_path and GET query parameters as dict like
        {'param_name1': ['val1', 'val2'], 'param_name2': ['val1'], ...}
        """
        parsed_url = urlparse(query_string)
        query_path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        return query_path, query_params

    # --- Check functions add error/warning messages in messages list if errors occurs --- #
    def _check_path(self, path):
        """ Add error message if invalid path """
        if not path.startswith(self.VALID_PATH):
            self.messages.append("Error: invalid path '{}'. Expected '{}'".
                                 format(path, self.VALID_PATH))

    def _check_query_params(self, params):
        """ Check every query parameter and add error message for every invalid value """
        for param in params:
            if not (param in self.VALID_QUERY_PARAMS):
                self.messages.append("Error: invalid query parameter '{}'. Allowed parameters: {}".
                                     format(param, ', '.join(self.VALID_QUERY_PARAMS)))

    def _check_attributes(self, attrs, valid_attrs):
        """ Check every 'attribute' parameter and add error message for every invalid value """
        for attr in attrs:
            if not (attr in valid_attrs):
                self.messages.append("Error: invalid attribute '{}'. Allowed attributes: {}".
                                     format(attr, ', '.join(valid_attrs)))

    def _check_order(self, query_params):
        """ Check 'order' parameter and add error message for every invalid case """
        # 'order' must be only with 'attribute'
        if not query_params.get('attribute', None):
            self.messages.append("Error: 'order' parameter must be only with sorting parameter 'attribute'")
        else:
            # 'order' must be only one
            if len(query_params['order']) > 1:
                self.messages.append("Error: {} 'order' parameters given. 1 expected".
                                     format(len(query_params['order'])))
            else:
                # 'order' must have only 'asc' or 'desc' value
                order = query_params['order'][0]
                if not (order in self.VALID_ORDER_VALUES):
                    self.messages.append("Error: invalid order '{}'. Allowed values: {}.".
                                         format(order, ', '.join(self.VALID_ORDER_VALUES)))

    def _check_offset(self, offset_list, cats_number):
        """ Check 'offset' parameter and add error message for every invalid case """
        # 'offset' must be only one
        if len(offset_list) > 1:
            self.messages.append("Error: {} 'offset' parameters given. 1 expected".format(len(offset_list)))
        else:
            offset = offset_list[0]
            # 'offset' must be integer
            if not offset.isdigit():
                self.messages.append("Error: invalid offset '{}'. Integer expected.".format(offset))
            else:
                # 'offset' must be < records in table otherwise nothing to output
                if int(offset) >= cats_number:
                    self.messages.append(
                        "Warning: There is no results because offset {} greater than the maximum of {}".
                        format(offset, cats_number - 1)
                    )

    def _check_limit(self, limit_list):
        """ Check 'limit' parameter and add error message for every invalid case """
        # 'limit' must be only one
        if len(limit_list) > 1:
            self.messages.append("Error: {} 'limit' parameters given. 1 expected".format(len(limit_list)))
        else:
            limit = limit_list[0]
            # 'limit' must be integer
            if not limit.isdigit():
                self.messages.append("Error: invalid limit '{}'. Integer expected.".format(limit))

    def check_query(self, query_string, valid_attrs, cats_number):
        """
        Check query parameters for errors
        Return errors messages list
        """
        self.messages = []
        query_path, query_params = self.parse_query(query_string)

        # query path starts with '/cats'
        self._check_path(query_path)

        # query parameters must be from the valid query parameters list
        self._check_query_params(query_params)

        # values of parameter 'attribute' must be from the valid attributes values list
        if query_params.get('attribute'):
            self._check_attributes(query_params['attribute'], valid_attrs)

        # 'order' must be only with 'attribute' parameter, only one and integer
        if query_params.get('order'):
            self._check_order(query_params)

        # 'offset' must be only one, integer and not greater than records in table
        if query_params.get('offset'):
            self._check_offset(query_params['offset'], cats_number)

        # 'limit' must be only one and integer
        if query_params.get('limit'):
            self._check_limit(query_params['limit'])

        return self.messages


class WGTestHTTPRequestHandler(BaseHTTPRequestHandler):
    DB_TABLE = 'cats'

    def __init__(self, *args, **kwargs):
        self.checker = Checker()
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def response(self, content):
        # Send response
        self._set_headers()
        self.wfile.write(json.dumps(content).encode('utf-8'))

    def _set_sql_query(self, query_params):
        """ Return sql query string from valid query params """
        query = 'SELECT * FROM {}'.format(self.DB_TABLE)
        # attributes in query string
        if query_params.get('attribute'):
            query += ' ORDER BY '
            # may be 1>= attrs
            for attr in query_params['attribute']:
                query += '{}, '.format(attr)
            query = query.rstrip(', ')

        # order in query string
        if query_params.get('order'):
            order = query_params['order'][0]
            query += ' {}'.format(order.upper())

        # offset in query string
        if query_params.get('offset'):
            offset = query_params['offset'][0]
            query += ' OFFSET {}'.format(offset)

        # limit in query string
        if query_params.get('limit'):
            limit = query_params['limit'][0]
            query += ' LIMIT {}'.format(limit)

        return query

    def do_GET(self):
        """ Handles GET query """
        valid_attr_values = db_table_column_names(self.DB_TABLE)
        cats_number = db_table_size(self.DB_TABLE)

        # get errors/warnings messages
        messages = self.checker.check_query(self.path, valid_attr_values, cats_number)

        # query has errors => send messages to client and halt
        if messages:
            self.response(messages)
            return

        # set sql query
        query_params = self.checker.parse_query(self.path)[1]
        query = self._set_sql_query(query_params)

        # get data from db
        data = db_query_realdict(query)

        # send data to client
        self.response(data)

    def do_POST(self):
        """ Handles POST query """
        print(self.path)
        pass


def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, WGTestHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
