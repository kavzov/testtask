#!/usr/bin/env python
import sys
from utils import db_table_size, reset_table


tables = {
    'cats': 'cats',
    'colors': 'cat_colors_info',
    'stat': 'cats_stat',
}


def main():
    try:
        arg = sys.argv[1]
        table = tables[arg]
    except IndexError:
        print('Error: no any parameter in the command')
        return
    except KeyError:
        print('Error: unknown parameter "{}"'.format(arg))
        return

    if db_table_size(table):
        reset_table(table)
        print('{} data have been deleted from the database'.format(arg.capitalize()))
    else:
        print('There is no {} data to delete in the database'.format(arg))


if __name__ == '__main__':
    main()
