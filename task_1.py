import psycopg2.extras
from utils import db_connect, db_query
from settings import DB_TABLE_NAME


def get_colors():
    """ Get available cats colors from 'cat_color_info' type of db and return them as list """
    data = db_query('SELECT unnest(enum_range(NULL::cat_color))')
    return [color[0] for color in data]


def get_cats_colors():
    """ Get all cats colors and return them as list """
    data = db_query('SELECT color FROM {}'.format(DB_TABLE_NAME))
    return [color[0] for color in data]


def colors_info_to_db(counters):
    """ Insert cats colors stat info to db """
    with db_connect() as conn:
        with conn.cursor() as cur:
            query = 'INSERT INTO cat_colors_info (color, count) VALUES %s'
            try:
                psycopg2.extras.execute_values(cur, query, counters.items())
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)


def main():
    colors = get_colors()
    cats_colors = get_cats_colors()

    # dict with cats colors counters init with 0 like {'black': 0, 'white': 0, ...}
    colors_counters = dict.fromkeys(colors, 0)

    # iter by cats colors and inc corresponding color counter
    for color in cats_colors:
        colors_counters[color] += 1

    # insert colors info to db
    colors_info_to_db(colors_counters)


if __name__ == '__main__':
    main()
