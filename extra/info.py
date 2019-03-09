#!/usr/bin/env python
import sys
from utils import db_query_realdict


items = {
    'cats': {
        'title': 'cats',
        'table': 'cats',
        'line': '| {name:8}  | {color:20} |  {tail_length:^11} |  {whiskers_length:^16} |'
    },
    'colors': {
        'title': 'colors',
        'table': 'cat_colors_info',
        'line': '| {color:20}  | {count:^5} |'
    },
    'lengths': {
        'title': 'lengths',
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
    print(item['title'].capitalize())


def print_item_lines(item, data):
    first_line = True
    if item['title'] == 'lengths':
        line_len = len(item['line'].format('', '')) - 2
        for title, value in data.items():
            if first_line:
                hr = get_hr(line_len, '=')
                print(hr)
                print(item['line'].format('Parameter', 'Value'))
                print(hr)
            hr = get_hr(line_len)
            print(item['line'].format(conv_title(title), conv_list(value)))
            print(hr)
            first_line = False
    else:
        line_len = len(item['line'].format(**data[0])) - 2
        for obj in data:
            if first_line:
                hr = get_hr(line_len, '=')
                print(hr)
                print(item['line'].format(**{k: conv_title(k) for k in obj.keys()}))
                print(hr)
            if not data:
                return
            hr = get_hr(line_len)
            print(item['line'].format(**obj))
            print(hr)
            first_line = False


def print_item(item):
    data = db_query_realdict('SELECT * FROM {}'.format(item['table']), many=get_many(item['title']))
    if not data:
        print('There is no {} info in the database'.format(item['title']))
        return

    print_header(item)
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
