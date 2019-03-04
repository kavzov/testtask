import json
from http.server import BaseHTTPRequestHandler
from utils import db_query_realdict, db_table_column_names, db_table_size, parse_query, run_server
from settings import CATS_TABLE


class GETQuery:
    """
    Class for query string.
    Provides the method for query string checking.
    """
    VALID_PATH = '/cats'
    VALID_QUERY_PARAMS = ['attribute', 'limit', 'offset', 'order']
    VALID_ORDER_VALUES = ['asc', 'desc']

    # --- Check functions add error/warning messages in messages list if errors occurs --- #
    def _check_path(self, path):
        """ Validate query path and add error message if it invalid """
        # query path must starts with '/cats'
        if not path.startswith(self.VALID_PATH):
            return "Error: invalid path '{}'. Expected '{}'".format(path, self.VALID_PATH)

    def _check_params(self, params):
        """ Validate every query parameter and add error message for every invalid value """
        # query parameters must be from the valid query parameters list
        for param in params:
            if not (param in self.VALID_QUERY_PARAMS):
                return "Error: invalid query parameter '{}'. Allowed parameters: {}".\
                    format(param, ', '.join(self.VALID_QUERY_PARAMS))

    def _check_attrs(self, attrs, valid_attrs):
        """ Validate every 'attribute' value and add error message for every invalid value """
        # values of parameter 'attribute' must be from the valid attributes values list
        for attr in attrs:
            if not (attr in valid_attrs):
                return "Error: invalid attribute '{}'. Allowed attributes: {}".format(attr, ', '.join(valid_attrs))

    def _check_order(self, query_params):
        """ Validate 'order' value and add error message for every invalid case """
        # 'order' must be only with 'attribute'
        if not query_params.get('attribute'):
            return "Error: 'order' parameter must be only with sorting parameter 'attribute'"
        else:
            # 'order' must be only one
            if len(query_params['order']) > 1:
                return "Error: {} 'order' parameters given. 1 expected".format(len(query_params['order']))
            else:
                # 'order' must have only 'asc' or 'desc' value
                order = query_params['order'][0]
                if not (order in self.VALID_ORDER_VALUES):
                    return "Error: invalid order '{}'. Allowed values: {}.".\
                        format(order, ', '.join(self.VALID_ORDER_VALUES))

    def _check_offset(self, offset_list, cats_number):
        """ Check 'offset' value and add error message for every invalid case """
        # 'offset' must be only one
        if len(offset_list) > 1:
            return "Error: {} 'offset' parameters given. 1 expected".format(len(offset_list))
        else:
            offset = offset_list[0]
            # 'offset' must be integer
            if not offset.isdigit():
                return "Error: invalid offset '{}'. Integer expected.".format(offset)
            else:
                # 'offset' must be < records in table otherwise nothing to output
                if int(offset) >= cats_number:
                    return "Warning: There is no results because offset {} greater than the maximum of {}".\
                        format(offset, cats_number - 1)

    def _check_limit(self, limit_list):
        """ Check 'limit' value and add error message for every invalid case """
        # 'limit' must be only one
        if len(limit_list) > 1:
            return "Error: {} 'limit' parameters given. 1 expected".format(len(limit_list))
        else:
            limit = limit_list[0]
            # 'limit' must be integer
            if not limit.isdigit():
                return "Error: invalid limit '{}'. Integer expected.".format(limit)

    def check(self, query_string, valid_attrs, cats_number):
        """
        Check GET query parameters
        """
        query_path, query_params = parse_query(query_string)

        # path
        path_error = self._check_path(query_path)
        if path_error:
            return path_error

        # parameters
        params_error = self._check_params(query_params)
        if params_error:
            return params_error

        # 'attribute' parameter
        if query_params.get('attribute'):
            attr_error = self._check_attrs(query_params['attribute'], valid_attrs)
            if attr_error:
                return attr_error

        # 'order' parameter
        if query_params.get('order'):
            order_error = self._check_order(query_params)
            if order_error:
                return order_error

        # 'offset' parameter
        if query_params.get('offset'):
            offset_error = self._check_offset(query_params['offset'], cats_number)
            if offset_error:
                return offset_error

        # 'limit' parameter
        if query_params.get('limit'):
            limit_error = self._check_limit(query_params['limit'])
            if limit_error:
                return limit_error


class Task4RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.query = GETQuery()
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
        query = 'SELECT * FROM {}'.format(CATS_TABLE)
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
        valid_attr_values = db_table_column_names(CATS_TABLE)
        cats_number = db_table_size(CATS_TABLE)

        error = self.query.check(self.path, valid_attr_values, cats_number)
        if error:
            self.response(error)
        else:
            # set sql query
            query_params = parse_query(self.path)[1]
            query = self._set_sql_query(query_params)

            # get data from db
            data = db_query_realdict(query)

            # send data to client
            self.response(data)


if __name__ == '__main__':
    run_server(handler=Task4RequestHandler)
