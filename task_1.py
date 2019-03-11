#!/usr/bin/env python
from utils import db_query_realdict, dict_items_to_db, db_table_size, reset_table
from settings import CATS_TABLE


def main():
    CATS_COLORS_TABLE = 'cat_colors_info'

    # get list of dicts {color: count}
    data = db_query_realdict('SELECT color, COUNT(*) FROM {} GROUP BY color ORDER BY color DESC'.format(CATS_TABLE))

    # convert to one dict (for dict_items_to_db())
    counters = {d['color']: d['count'] for d in data}

    msg = 'Cats color info have been '
    # if is data in the db, reset it
    colors_info = db_table_size(CATS_COLORS_TABLE)
    if colors_info:
        reset_table(CATS_COLORS_TABLE)
        msg += 'updated'
    else:
        msg += 'added to the database'

    # add or update colors info in the database
    dict_items_to_db(CATS_COLORS_TABLE, ('color', 'count'), counters)
    print(msg)


if __name__ == '__main__':
    main()
