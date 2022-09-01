#!python
"""
Utility script to perform a bunch of scrapes in one go
"""

from scraper import RedditReader
import csv
import itertools
from timer import Timer
import time

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
        'relevance',
        #'comments',
        'new',
        #'hot'
    ],
    't': [
        'all'
    ]
}

WORD_START = 0
N_WORDS = 10

def make_url(base, params):
    """ utility to build url from query params """
    pass

def make_query(key, value):
    return str(key) + '=' + str(value)

def scrape(url, attr_prefix):
    with RedditReader(url) as rr:
        print("> Starting scraper")
        rr.set_sleep_time(8)
        rr.get()

        timer = Timer()
        height_timer = Timer()
        height = rr.get_scroll_height()

        print("> got URL; scrolling...")

        while timer.elapsed() < 1000:
            timer.start()
            height_timer.start()

            rr.scroll()

            if height < rr.get_scroll_height():
                height = rr.get_scroll_height()
                height_timer.restart()
            elif height_timer.elapsed() > 60:
                print("> height timeout")
                break

            print(f'> {timer.elapsed()}, height {height}')


        print("DONE")
        prefix = 'scrape_' + attr_prefix
        rr.write_page_source(prefix=prefix)

# test

# run a scrape on a search for each work using various sort methods
# hack the loop - too lazy to figure out a cool way to do it
for word in SEARCH_ATTRS['q'][WORD_START:WORD_START + N_WORDS]:
    q = make_query('q', word)

    for sort in SEARCH_ATTRS['sort']:
        s = make_query('s', sort)
        t = make_query('t', 'all')

        qs = '&'.join([q,s,t])

        url = URL_BASE + '?' + qs
        prefix = word + sort

        print(f'scraping {url}')
        scrape(url, prefix)
        time.sleep(10)
