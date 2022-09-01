#!python
"""
Utility script to perform a bunch of scrapes in one go
"""

from scraper import RedditReader
import csv
import time
import itertools

# Get useful words
with open('../data/misc/useful_words_20220831145800.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    words = [row[0] for row in reader if row[0] != '']

# parse reddit r/astrology, searching for useful words in each parse
URL_BASE = 'https://www.reddit.com/r/astrology/search/?'
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


