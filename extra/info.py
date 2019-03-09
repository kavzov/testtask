#!/usr/bin/env python
import sys
from utils import db_query_realdict


items = {
    'cats': {
        'table': 'cats',
        'line': '| {name:8}  | {color:20} |  {tail_length:^11} |  {whiskers_length:^16} |'
    },
    'colors': {
        'table': 'cat_colors_info',
        'line': '| {color:20}  | {count:^5} |'
    },
    'lengths': {
        'table': 'cats_stat',
        'line': '| {:23} |  {:^7}  |'
    }
}


def conv_title(title):
    return title.replace('_', ' ').capitalize()


def conv_list(val):
    if isinstance(val, list):
        return ', '.join(str(s) for s in val)
    else:
        return str(val)


def get_many(item):
    return item != 'lengths'


def get_hr(line_len, sign='-'):
    return '+{}+'.format(sign * line_len)


def print_header(item):
    print()
    print(item.capitalize())


def print_item_lines(item, data):
    first_line = True
    if item == 'lengths':
        line_len = len(items[item]['line'].format('', '')) - 2
        for title, value in data.items():
            if first_line:
                hr = get_hr(line_len, '=')
                print(hr)
                print(items[item]['line'].format('Parameter', 'Value'))
                print(hr)
            hr = get_hr(line_len)
            print(items[item]['line'].format(conv_title(title), conv_list(value)))
            print(hr)
            first_line = False
    else:
        line_len = len(items[item]['line'].format(**data[0])) - 2
        for obj in data:
            if first_line:
                hr = get_hr(line_len, '=')
                print(hr)
                print(items[item]['line'].format(**{k: conv_title(k) for k in obj.keys()}))
                print(hr)
            if not data:
                return
            hr = get_hr(line_len)
            print(items[item]['line'].format(**obj))
            print(hr)
            first_line = False


def print_item(item):
    data = db_query_realdict('SELECT * FROM {}'.format(items[item]['table']), many=get_many(item))
    if not data:
        print('There is no {} info in the database'.format(item))
        return

    print_header(item)
    print_item_lines(item, data)
    print()


def main():
    try:
        item = sys.argv[1]
    except IndexError:
        print('Error: no any parameter in the command')
        return
    except KeyError:
        print('Error: unknown parameter "{}"'.format(item))
        return

    print_item(item)


if __name__ == '__main__':
    main()
