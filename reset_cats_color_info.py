import psycopg2
from db_settings import host, port, db_name, db_user, db_user_passw


def reset_cat_color_info():
    """ Delete all info from 'cat_color_info' table """
    conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_user_passw, host=host, port=port)
    query = 'DELETE FROM cat_colors_info'
    with conn.cursor() as cur:
        try:
            cur.execute(query)
        except psycopg2.Error as e:
            print(e)
        conn.commit()
    conn.close()


if __name__ == '__main__':
    reset_cat_color_info()
