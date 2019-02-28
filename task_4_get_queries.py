import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from db_connect import db_query_realdict, db_table_column_names, db_table_size


def param_in_query(param, query):
    return query.get(param, None)


def multivalued_param(params_list):
    return len(params_list) > 1


class Checker:
    """ Class checker for query string """
    def __init__(self):
        self.DB_TABLE = 'cats'
        self.VALID_PATH = '/cats'
        self.VALID_QUERY_PARAMS = ['attribute', 'limit', 'offset', 'order']
        self.VALID_ATTR_VALUES = db_table_column_names(self.DB_TABLE)
        self.VALID_ORDER_VALUES = ['asc', 'desc']
        self.messages = []

    @staticmethod
    def parse_query(query_string):
        # Return query path as string and GET query params as dict like {'param_name': ['val1', 'val2']}
        parsed_url = urlparse(query_string)
        query_path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        return query_path, query_params

    def _valid_path(self, path):
        """ Return whether path starts with valid string """
        return path.startswith(self.VALID_PATH)

    def _valid_param(self, param):
        """ Return whether param in valid query params list """
        return param in self.VALID_QUERY_PARAMS

    def _valid_attr(self, attr):
        """ Return whether attribute in valid attributes list """
        return attr in self.VALID_ATTR_VALUES

    def _valid_order(self, order):
        """ Return whether order 'asc' or 'desc' """
        return order in self.VALID_ORDER_VALUES

    # --- Check functions add error/warning messages in messages list if errors occurs --- #
    def _check_path(self, path):
        """ Add error message if invalid path """
        if not self._valid_path(path):
            self.messages.append("Error: invalid path '{}'. Expected '{}'".
                                 format(path, self.VALID_PATH))

    def _check_query_params(self, params):
        """ Check every query parameter and add error message for every invalid value """
        for param in params:
            if not self._valid_param(param):
                self.messages.append("Error: invalid query parameter '{}'. Allowed parameters: {}".
                                     format(param, ', '.join(self.VALID_QUERY_PARAMS)))

    def _check_attributes(self, attrs):
        """ Check every 'attribute' parameter and add error message for every invalid value """
        for attr in attrs:
            if not self._valid_attr(attr):
                self.messages.append("Error: invalid attribute '{}'. Allowed attributes: {}".
                                     format(attr, ', '.join(self.VALID_ATTR_VALUES)))

    def _check_order(self, query_params):
        """ Check 'order' parameter and add error message for every invalid case """
        # 'order' must be only with 'attribute'
        if not param_in_query('attribute', query_params):
            self.messages.append("Error: 'order' parameter must be only with sorting parameter 'attribute'")
        else:
            # 'order' must be only one
            if multivalued_param(query_params['order']):
                self.messages.append("Error: {} 'order' parameters given. 1 expected".
                                     format(len(query_params['order'])))
            else:
                # 'order' must have only 'asc' or 'desc' value
                order = query_params['order'][0]
                if not self._valid_order(order):
                    self.messages.append("Error: invalid order '{}'. Allowed values: {}.".
                                         format(order, ', '.join(self.VALID_ORDER_VALUES)))

    def _check_offset(self, offset_list):
        """ Check 'offset' parameter and add error message for every invalid case """
        # 'offset' must be only one
        if multivalued_param(offset_list):
            self.messages.append("Error: {} 'offset' parameters given. 1 expected".format(len(offset_list)))
        else:
            offset = offset_list[0]
            # 'offset' must be integer
            if not offset.isdigit():
                self.messages.append("Error: invalid offset '{}'. Integer expected.".format(offset))
            else:
                # 'offset' must be < records in table otherwise nothing to output
                cats_number = db_table_size(self.DB_TABLE)
                if int(offset) >= cats_number:
                    self.messages.append(
                        "Warning: There is no results because given offset {} greater than allowed {}".
                        format(offset, cats_number - 1)
                    )

    def _check_limit(self, limit_list):
        """ Check 'limit' parameter and add error message for every invalid case """
        # 'limit' must be only one
        if multivalued_param(limit_list):
            self.messages.append("Error: {} 'limit' parameters given. 1 expected".format(len(limit_list)))
        else:
            limit = limit_list[0]
            # 'limit' must be integer
            if not limit.isdigit():
                self.messages.append("Error: invalid limit '{}'. Integer expected.".format(limit))

    def check_query_errors(self, query_string):
        """
        Check query parameters for errors
        Return errors messages list
        """
        self.messages = []
        query_path, query_params = self.parse_query(query_string)

        # check query path - it must starts with '/cats'
        self._check_path(query_path)

        # check query parameters - they must be from VALID_QUERY_PARAMS list
        self._check_query_params(query_params)

        # check parameter 'attribute' - its values must be from VALID_ATTR_VALUES list
        if param_in_query('attribute', query_params):
            self._check_attributes(query_params['attribute'])

        # check valid order
        if param_in_query('order', query_params):
            self._check_order(query_params)

        # check valid offset
        if param_in_query('offset', query_params):
            self._check_offset(query_params['offset'])

        # check valid limit
        if param_in_query('limit', query_params):
            self._check_limit(query_params['limit'])

        return self.messages


class TestTaskHTTPRequestHandler(BaseHTTPRequestHandler):
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
        query = 'SELECT * FROM cats'
        # attributes in query string
        if param_in_query('attribute', query_params):
            query += ' ORDER BY '
            # may be 1>= attrs
            for attr in query_params['attribute']:
                query += '{}, '.format(attr)
            query = query.rstrip(', ')

        # order in query string
        if param_in_query('order', query_params):
            order = query_params['order'][0]
            query += ' {}'.format(order.upper())

        # offset in query string
        if param_in_query('offset', query_params):
            offset = query_params['offset'][0]
            query += ' OFFSET {}'.format(offset)

        # limit in query string
        if param_in_query('limit', query_params):
            limit = query_params['limit'][0]
            query += ' LIMIT {}'.format(limit)

        return query

    def do_GET(self):
        """ Handles GET query """
        # get query path and params

        # get errors/warnings messages
        # messages = self.checker.check_query_errors(query_path, query_params)
        messages = self.checker.check_query_errors(self.path)

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


def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, TestTaskHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
