#!/usr/bin/env python
import re
import sys
from utils import db_query_realdict


items = {
    'cats': {
        'title': 'cats',
        'header': 'cats',
        'table': 'cats',
        'line': '| {name:9} | {color:20} | {tail_length:^12} | {whiskers_length:^16} |'
    },
    'colors': {
        'title': 'colors',
        'header': 'cat colors',
        'table': 'cat_colors_info',
        'line': '| {color:21} | {count:^5} |'
    },
    'stat': {
        'title': 'lengths',
        'header': 'statistics',
        'table': 'cats_stat',
        'line': '| {:23} | {:^8} |'
    }
}


def conv_title(title):
    """ Converts 'solid_string' to 'Solid string' """
    return title.replace('_', ' ').capitalize()


def conv_list(val):
    if isinstance(val, list):
        return ', '.join(str(s) for s in val)
    else:
        return str(val)


def get_many(item):
    """ Return parameter 'many' for db query. Single record has only 'cats_stat' table """
    return item != 'lengths'


def get_hr(string, sign='-'):
    """ Return horizontal line """
    cross = '+'
    lengths = map(int, re.findall(r'\d+', string))
    line = cross
    for l in lengths:
        line += sign*(l+2) + cross
    return line


def print_item_lines(item, data):
    """ Displays line by line every record of an item data """
    first_line = True
    if item['title'] == 'lengths':
        for title, value in data.items():
            if first_line:
                hr = get_hr(item['line'], '=')
                print(hr)
                print(item['line'].format('Parameter', 'Value'))
                print(hr)
            hr = get_hr(item['line'])
            print(item['line'].format(conv_title(title), conv_list(value)))
            print(hr)
            first_line = False
    else:
        for obj in data:
            if first_line:
                hr = get_hr(item['line'], '=')
                print(hr)
                print(item['line'].format(**{k: conv_title(k) for k in obj.keys()}))
                print(hr)
            hr = get_hr(item['line'])
            print(item['line'].format(**obj))
            print(hr)
            first_line = False


def print_item(item):
    """ Displays the table with items info """
    data = db_query_realdict('SELECT * FROM {}'.format(item['table']), many=get_many(item['title']))
    if not data:
        print('There is no {} data in the database'.format(item['header']))
        return

    print('\n{}'.format(item['header'].capitalize()))
    print_item_lines(item, data)
    print()


def main():
    try:
        arg = sys.argv[1]
        item = items[arg]
    except IndexError:
        print('Error: no any parameter in the command')
        return
    except KeyError:
        print('Error: unknown parameter "{}"'.format(arg))
        return
    print_item(item)


if __name__ == '__main__':
    main()
