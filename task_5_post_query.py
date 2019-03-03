import re
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from db import db_query, db_table_column_names, dict_to_db
from cats_colors_info import get_colors


DB_TABLE = 'cats'


class PostQuery:
    """
    Class for handle POST query.
    Provides methods for checking POST query .
    """
    @staticmethod
    def _validate_json(post_data):
        """ Check string for valid JSON. Return error message if it not valid """
        json_error = ''
        post_data_dict = {}
        try:
            post_data_dict = json.loads(post_data)
        except json.JSONDecodeError:
            json_error = 'Error: invalid JSON'
        return json_error, post_data_dict

    @staticmethod
    def _validate_attrs(post_data, valid_attrs):
        """ Check attributes by comparing with the valid attributes list """
        # sort for correct compare
        valid_attrs = sorted(valid_attrs)
        user_attrs = sorted(list(post_data))

        if not user_attrs == valid_attrs:
            return 'Error: invalid attributes. Expected exactly these: {}'.\
                format(', '.join("'{}'".format(attr) for attr in valid_attrs))

    @staticmethod
    def _check_length(post_data, items):
        """ Check tail and whiskers length. They must be positive integer """
        for item in items:
            length = post_data[item]
            if length <= 0:
                return 'Error: {} is not positive integer'.format(item)

    @staticmethod
    def _name_correct(name):
        """ Name must contain at least one letter, digits, space, '_' or '-' symbols """
        return re.match("""^[a-zA-z][a-zA-Z0-9 _-]*$""", name)

    def validate(self, post_data, valid_attrs, valid_colors):
        """ Validates POST query parameters """
        res = {'dict': {}, 'error': ''}
        # validate json
        json_error, post_data_dict = self._validate_json(post_data)
        if json_error:
            res['error'] = json_error
            return res

        # validate attributes: all required
        attrs_error = self._validate_attrs(post_data_dict, valid_attrs)
        if attrs_error:
            res['error'] = attrs_error
            return res

        # validate name
        if not re.match('^[a-zA-Z][a-zA-Z0-9 -]*$', post_data_dict['name']):
            res['error'] = "Error: invalid name." \
                           "Expected nonempty string contained letters, digits, space and dash symbols"
            return res

        # validate color
        if post_data_dict['color'] not in valid_colors:
            res['error'] = "Error: invalid color. Expected exactly these: {}".\
                format(', '.join("'{}'".format(clr) for clr in valid_colors))
            return res

        # validate tail and whiskers type
        for length in ['tail_length', 'whiskers_length']:
            if not isinstance(post_data_dict[length], int):
                res['error'] = "Error: {} not a number".format(length)
                return res

        res['dict'] = post_data_dict
        return res

    def check(self, post_data_dict, is_namesake):
        """
        Check parameters values of POST query
        """
        if is_namesake:
            return 'Error: cat {} already exists'. format(post_data_dict['name'])

        length_error = self._check_length(post_data_dict, ['tail_length', 'whiskers_length'])
        if length_error:
            return length_error


class WGTestHTTPRequestHandler(BaseHTTPRequestHandler):
    """ HTTP Request handler """
    def __init__(self, *args, **kwargs):
        self.query = PostQuery()
        super().__init__(*args, **kwargs)

    def response(self, content):
        """ Send response to client """
        self.wfile.write(json.dumps(content).encode('utf-8'))

    # ---- POST request handle ---- #

    @staticmethod
    def _get_valid_attrs():
        """ Return allowed attributes list """
        return db_table_column_names(DB_TABLE)

    @staticmethod
    def _get_valid_colors():
        """ Return allowed colors list """
        return get_colors()

    @staticmethod
    def _exist_namesake(name):
        """ Return QueryDict with the same name cat """
        return db_query("SELECT name FROM {} WHERE name='{}'".format(DB_TABLE, name), many=False)

    def do_POST(self):
        """ Handles POST request """
        VALID_PATH = '/cat'

        if self.path != VALID_PATH:
            self.response("Wrong path '{}'. Expected '{}'".format(self.path, VALID_PATH))
            return

        # get POST query
        data_length = int(self.headers['Content-Length'])
        post_data_json = self.rfile.read(data_length).decode('utf-8')

        validation_res = self.query.validate(post_data_json, self._get_valid_attrs(), self._get_valid_colors())
        if validation_res.get('error'):
            self.response(validation_res['error'])
            return

        post_data_dict = validation_res['dict']

        # if query is valid - check remaining values
        errors = self.query.check(post_data_dict, self._exist_namesake(post_data_dict['name']))

        if errors:
            self.response(errors)
        else:
            dict_to_db(DB_TABLE, post_data_dict) and \
                self.response("Success: cat {} stored to database".format(post_data_dict['name']))


def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, WGTestHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
