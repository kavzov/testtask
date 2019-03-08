#!/usr/bin/env python
from collections import Counter
from utils import db_query, dict_items_to_db
from settings import CATS_TABLE


def get_cats_colors():
    """ Gets all colors of cats and return them as list """
    data = db_query('SELECT color FROM {}'.format(CATS_TABLE))
    return [color[0] for color in data]


def main():
    cats_colors = get_cats_colors()

    # count up colors
    counter = Counter()
    for color in cats_colors:
        counter[color] += 1

    # insert colors info to db
    if dict_items_to_db('cat_colors_info', ('color', 'count'), dict(counter)):
        print('Cats colors info have been successfully added to the database')


if __name__ == '__main__':
    main()
