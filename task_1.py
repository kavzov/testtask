#!/usr/bin/env python
from collections import Counter
from utils import db_query, dict_items_to_db, db_table_size, reset_table
from settings import CATS_TABLE


def get_cats_colors():
    """ Gets all colors of cats and return them as list """
    data = db_query('SELECT color FROM {}'.format(CATS_TABLE))
    return [color[0] for color in data]


def main():
    CATS_COLORS_TABLE = 'cat_colors_info'
    cats_colors = get_cats_colors()

    # count up colors
    counter = Counter()
    for color in cats_colors:
        counter[color] += 1

    msg = 'Cats color info have been '
    # if is data in the db, reset it
    colors_info = db_table_size(CATS_COLORS_TABLE)
    if colors_info:
        reset_table(CATS_COLORS_TABLE)
        msg += 'updated'
    else:
        msg += 'added to the database'

    # add or update colors info in the database
    dict_items_to_db(CATS_COLORS_TABLE, ('color', 'count'), dict(counter))
    print(msg)


if __name__ == '__main__':
    main()
