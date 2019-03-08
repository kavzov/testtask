#!/usr/bin/env python
import statistics
from collections import Counter
from utils import db_query_realdict, db_table_size, dict_to_db, reset_table


def get_tail_and_whiskers_lengths():
    """ Return tails and whiskers lengths as list of dicts """
    return db_query_realdict('SELECT tail_length, whiskers_length FROM cats')


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


def main():
    CATS_STAT_TABLE = 'cats_stat'
    # tails and whiskers lengths
    tails_and_whiskers = get_tail_and_whiskers_lengths()

    # tails lengths
    tails = [tail['tail_length'] for tail in tails_and_whiskers]
    # whiskers lengths
    whiskers = [wh['whiskers_length'] for wh in tails_and_whiskers]

    # Statistics dictionary
    stat = dict()

    # Means
    stat['tail_length_mean'] = get_length_mean(tails)
    stat['whiskers_length_mean'] = get_length_mean(whiskers)

    # Medians
    stat['tail_length_median'] = statistics.median(tails)
    stat['whiskers_length_median'] = statistics.median(whiskers)

    # Modes
    stat['tail_length_mode'] = get_length_mode(tails)
    stat['whiskers_length_mode'] = get_length_mode(whiskers)

    # if is data in the db, reset it
    stat_info = db_table_size(CATS_STAT_TABLE)
    if stat_info:
        reset_table(CATS_STAT_TABLE)

    # Store values to db
    dict_to_db(CATS_STAT_TABLE, stat)
    print('Statistics have been successfully added to the database')


if __name__ == '__main__':
    main()
