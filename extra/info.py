#!/usr/bin/env python
import re
import sys
from utils import db_query_realdict


items = {
    'cats': {
        'title': 'cats',
        'header': 'cats',
        'table': 'cats',
        'string': '| {name:9} | {color:20} | {tail_length:^12} | {whiskers_length:^16} |'
    },
    'colors': {
        'title': 'colors',
        'header': 'cat colors',
        'table': 'cat_colors_info',
        'string': '| {color:21} | {count:^5} |'
    },
    'stat': {
        'title': 'lengths',
        'header': 'statistics',
        'table': 'cats_stat',
        'string': '| {parameter:23} | {value:^8} |'
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


def get_hr(str_ptn, sign='~'):
    """ Horizontal line """
    CROSS = '+'
    # set list of cell widths from an item string pattern
    lengths = map(int, re.findall(r'\d+', str_ptn))
    line = CROSS
    for l in lengths:
        line += sign*(l+2) + CROSS
    return line


def print_string(str_ptn, obj, hr):
    """ Prints a single table string """
    print(str_ptn.format(**obj))
    print(hr)


def print_item_strings(item, data):
    """ Prints string by string an item data """
    first_line = True
    if item['title'] == 'lengths':
        # Because 'lengths' is a single dict record, convert it to list of dicts like 'cats' and 'colors' to proper display
        data = [{'parameter': conv_title(item[0]), 'value': conv_list(item[1])} for item in data.items()]
    for obj in data:
        if first_line:
            hr = get_hr(item['string'], '=')
            header = {k: conv_title(k) for k in obj.keys()}
            print(hr)
            print_string(item['string'], header, hr)
        hr = get_hr(item['string'])
        print_string(item['string'], obj, hr)
        first_line = False


def display_item(item):
    """ Displays the table with items data """
    data = db_query_realdict('SELECT * FROM {}'.format(item['table']), many=get_many(item['title']))
    if not data:
        print('There is no {} data in the database'.format(item['header']))
        return

    print('\n{}'.format(item['header'].capitalize()))
    print_item_strings(item, data)
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

    display_item(item)


if __name__ == '__main__':
    main()
