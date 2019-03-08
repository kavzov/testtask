#!/usr/bin/env python
import re
import json
from http.server import BaseHTTPRequestHandler
from utils import db_query, db_table_column_names, dict_to_db, run_server
from settings import CATS_TABLE


class POSTQuery:
    """
    Class for handle POST query.
    Provides methods for checking POST query .
    """
    def _check_json(self, post_data):
        """ Check string for valid JSON. Return error message if it not valid """
        json_error = ''
        post_data_dict = {}
        try:
            post_data_dict = json.loads(post_data)
        except json.JSONDecodeError:
            json_error = 'Error: invalid JSON'
        return json_error, post_data_dict

    def _check_attrs(self, post_data, valid_attrs):
        """ Check attributes by comparing with the valid attributes list """
        # sort for correct compare
        valid_attrs = sorted(valid_attrs)
        user_attrs = sorted(list(post_data))

        if not user_attrs == valid_attrs:
            return 'Error: invalid attributes. Expected exactly these: {}'.\
                format(', '.join("'{}'".format(attr) for attr in valid_attrs))

    def check(self, post_data, valid_attrs, valid_colors):
        """
        Check POST query parameters
        Return dict with POST query as dict and error if occur
        """
        res = {'dict': {}, 'error': ''}
        # json
        json_error, post_data_dict = self._check_json(post_data)
        if json_error:
            res['error'] = json_error
            return res

        # attributes: all required
        attrs_error = self._check_attrs(post_data_dict, valid_attrs)
        if attrs_error:
            res['error'] = attrs_error
            return res

        # name
        if not re.match('^[a-zA-Z][a-zA-Z0-9 -]*$', post_data_dict['name']):
            res['error'] = "Error: invalid name." \
                           "Expected nonempty string contained letters, digits, space and dash symbols"
            return res

        # color
        if post_data_dict['color'] not in valid_colors:
            res['error'] = "Error: invalid color. Expected exactly these: {}".\
                format(', '.join("'{}'".format(clr) for clr in valid_colors))
            return res

        # tail and whiskers type
        for length in ['tail_length', 'whiskers_length']:
            if not isinstance(post_data_dict[length], int):
                res['error'] = "Error: {} is not a number".format(length)
                return res
            if post_data_dict[length] <= 0:
                res['error'] = "Error: {} is not positive integer".format(length)
                return res

        res['dict'] = post_data_dict
        return res

    def check_namesake(self, namesake):
        """ Return error message if cat with the same name already exist """
        if namesake:
            return 'Error: cat {} already exists'. format(namesake[0])


class Task5RequestHandler(BaseHTTPRequestHandler):
    """ HTTP Request handler """
    def __init__(self, *args, **kwargs):
        self.query = POSTQuery()
        super().__init__(*args, **kwargs)

    def response(self, content):
        """ Send response to client """
        self.wfile.write(json.dumps(content).encode('utf-8'))

    def _get_valid_attrs(self):
        """ Return allowed attributes list """
        return db_table_column_names(CATS_TABLE)

    def _get_valid_colors(self):
        """ Return allowed colors list """
        data = db_query('SELECT unnest(enum_range(NULL::cat_color))')
        return [color[0] for color in data]

    def _namesake(self, name):
        """ Check whether cat with the same name already exist in db """
        return db_query("SELECT name FROM {} WHERE name='{}'".format(CATS_TABLE, name), many=False)

    def do_POST(self):
        """ Handles POST request """
        VALID_PATH = '/cat'

        if self.path != VALID_PATH:
            self.response("Wrong path '{}'. Expected '{}'".format(self.path, VALID_PATH))
            return

        # get POST query
        data_length = int(self.headers['Content-Length'])
        post_data_json = self.rfile.read(data_length).decode('utf-8')

        check_results = self.query.check(post_data_json, self._get_valid_attrs(), self._get_valid_colors())
        if check_results['error']:
            self.response(check_results['error'])
            return

        post_data_dict = check_results['dict']

        # if query is valid - check for namesake
        namesake_error = self.query.check_namesake(self._namesake(post_data_dict['name']))
        if namesake_error:
            self.response(namesake_error)
            return

        # all right - store cat info to db and send success info to client
        if dict_to_db(CATS_TABLE, post_data_dict):
            self.response("Success: cat {} added to database".format(post_data_dict['name']))


if __name__ == '__main__':
    run_server(task=5, handler=Task5RequestHandler)
