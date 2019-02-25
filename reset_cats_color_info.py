import psycopg2
from db_connect import db_connect


def reset_cat_color_info():
    """ Delete all info from 'cat_color_info' table """
    with db_connect() as conn:
        with conn.cursor() as cur:
            query = 'DELETE FROM cat_colors_info'
            try:
                cur.execute(query)
            except psycopg2.Error as e:
                print(e)
            else:
                conn.commit()


if __name__ == '__main__':
    reset_cat_color_info()
