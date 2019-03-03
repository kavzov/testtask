import psycopg2
import psycopg2.extras
from db import connect


def get_colors():
    """ Extract available cats colors from 'cat_color_info' type of db and return them as list """
    with connect() as conn:
        with conn.cursor() as cur:
            query = 'SELECT unnest(enum_range(NULL::cat_color))'
            try:
                cur.execute(query)
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)
            # results as singleton tuples list
            res = cur.fetchall()
    # return results as colors list
    return [color[0] for color in res]


def get_cats_colors():
    """ Get all cats colors and return them as list """
    with connect() as conn:
        with conn.cursor() as cur:
            query = 'SELECT color FROM cats'
            try:
                cur.execute(query)
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)
            # results as singleton tuples list
            res = cur.fetchall()
    # return results as cats colors list
    return [color[0] for color in res]


def cats_colors_info_to_db(counters):
    """ Insert cats colors stat info to db """
    with connect() as conn:
        with conn.cursor() as cur:
            query = 'INSERT INTO cat_colors_info (color, count) VALUES %s'
            try:
                psycopg2.extras.execute_values(cur, query, counters.items())
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)


# ----------- Main ----------- #

def run():
    colors = get_colors()
    cats_colors = get_cats_colors()

    # dict with cats colors counters init with 0 like {'black': 0, 'white': 0, ...}
    cats_colors_counters = dict.fromkeys(colors, 0)

    # iter by cats colors and inc corresponding color counter
    for color in cats_colors:
        cats_colors_counters[color] += 1

    # insert colors info to db
    cats_colors_info_to_db(cats_colors_counters)


if __name__ == '__main__':
    run()
