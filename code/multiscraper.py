#!python
"""
Utility script to perform a bunch of scrapes in one go
"""

from scraper import RedditReader
import csv
import itertools
from timer import Timer

# Get useful words
with open('../data/misc/useful_words_20220831145800.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    words = [row[0] for row in reader if row[0] != '']

# parse reddit r/astrology, searching for useful words in each parse
URL_BASE = 'https://www.reddit.com/r/astrology/search/'
SEARCH_ATTRS = {
    'q': words,
    'sort': [
        'top',
        #'relevance',
        'comments',
        'new',
        #'hot'
    ],
    't': [
        'all'
    ]
}

def make_url(base, params):
    """ utility to build url from query params """
    pass

def make_query(key, value):
    return str(key) + '=' + str(value)

# test

q = make_query('q', SEARCH_ATTRS['q'][0]) + '&'\
    + make_query('sort', SEARCH_ATTRS['sort'][0]) + '&'\
    + make_query('t', 'all')

url = URL_BASE + '?' + q

with RedditReader(url) as rr:

    rr.set_sleep_time(8)
    rr.get()

    timer = Timer()
    height_timer = Timer()
    height = rr.get_scroll_height()

    while timer.elapsed() < 1000:
        timer.start()
        height_timer.start()

        rr.scroll()

        if height < rr.get_scroll_height():
            height = rr.get_scroll_height()
            height_timer.restart()
        elif height_timer.elapsed() > 60:
            print("> height timeout")
            break;

        print(f'> {timer.elapsed()}, height {height}')


    print("DONE")
    prefix = 'scrape' + SEARCH_ATTRS['q'][0]
    rr.write_page_source(prefix=prefix)
