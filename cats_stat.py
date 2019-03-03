import psycopg2
import psycopg2.extras
import statistics
from collections import Counter
from db import connect


def get_tail_and_whiskers_lengths():
    """ Fetch tails and whiskers lengths and return them as list of dicts """
    with connect() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            query = 'SELECT tail_length, whiskers_length FROM cats'
            try:
                cur.execute(query)
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)
            res = cur.fetchall()
    return res


def get_length_mean(lengths):
    """ Return average value of lengths """
    length_mean = sum(lengths)/len(lengths)
    return round(length_mean, 1)


def get_length_median(lengths):
    """ Return median of lengths """
    return statistics.median(lengths)


def get_length_mode(lengths):
    """ Return modes lengths list """
    # list of tuples (value, count) SORTED BY COUNT
    counts = Counter(lengths).most_common()

    # first element of the counts list - max count
    # its value to modes list
    modes = [counts[0][0]]

    # max count of the value
    max_count = counts[0][1]

    # check for other values is modes too (its count equals max_count)
    # append them to stat_mode
    if len(counts) > 1:
        for i in range(1, len(counts)):
            if counts[i][1] == max_count:
                modes.append(counts[i][0])
            else:
                break
    return modes


def stat_to_db(*values):
    """ Insert stat to db """
    with connect() as conn:
        with conn.cursor() as cur:
            query = "INSERT INTO cats_stat VALUES (%s, %s, %s, %s, %s, %s)"
            try:
                cur.execute(query, values)
            except psycopg2.Error as e:
                print("Psycopg2 error: ", e)
            else:
                conn.commit()


# ----------- Main ----------- #


def run():
    # tails and whiskers lengths
    tails_and_whiskers = get_tail_and_whiskers_lengths()

    # tails lengths
    tails = [tail['tail_length'] for tail in tails_and_whiskers]
    # whiskers lengths
    whiskers = [wh['whiskers_length'] for wh in tails_and_whiskers]

    # Means
    tail_length_mean = get_length_mean(tails)
    whiskers_length_mean = get_length_mean(whiskers)

    # Medians
    tail_length_median = statistics.median(tails)
    whiskers_length_median = statistics.median(whiskers)

    # Modes
    tail_length_mode = get_length_mode(tails)
    whiskers_length_mode = get_length_mode(whiskers)

    # Store the values to db
    stat_to_db(tail_length_mean, tail_length_median, tail_length_mode,
               whiskers_length_mean, whiskers_length_median, whiskers_length_mode)


if __name__ == '__main__':
    run()
