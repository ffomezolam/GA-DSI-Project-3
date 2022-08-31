#!python
"""
Utilities for parsing Reddit html
"""

from bs4 import BeautifulSoup

from datetime import datetime, timedelta

import json
import re

import pandas as pd

import random

### REDDITPARSER CLASS
class RedditParser:
    """
    Class to parse Reddit source html and convert to dataframe and write
    to csv
    """

    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            src = f.read()

        self.file = file_path
        self.soup = None
        self.nposts = 0
        self.tags = None

        with open('./tags.json', 'r') as tags:
            self.tags = json.loads(tags.read())
            print("loaded tags:")
            print(self.tags)

        if src: self.load(src)

    def load(self, src):
        self.soup = BeautifulSoup(src, 'lxml')
        return self

    def go(self):
        posts = self.get_content('post')
        types = ['title','time','comments','body-text']
        out = dict()
        for type in types:
            out[type] = [self.get_content(type, post) for post in posts]

        return out

    def get_content(self, type='post', container=None):
        " get content from html, optionally from inner container "
        tag = self.tags[type]['tag']
        attrs = self.tags[type]['attrs']
        while len(attrs) > 1: attrs.popitem()

        if not container: return self.soup.find_all(tag, attrs)
        else:
            html = container.find(tag, attrs)
            if not html: return ''
            else: return self.process(type, html.text)

    def process(self, type, text):
        # TODO: do whatever trimming based on content type
        text = text.strip()
        if type == 'comments':
            text = int(text.split(' ')[0])
        if type == 'time':
            # convert time string to seconds
            num, desc = text.split(' ')[0:2]
            if desc.endswith('s'): desc = desc[:-1]
            secs = time_to_seconds(int(num), desc) or 0
            secs = timedelta(seconds=secs)

            # subtract seconds from file date
            scrape_time = get_file_timestamp(self.file)

            post_date = scrape_time - secs
            text = post_date.strftime('%Y-%m-%d')

        return text

### UTILITY FUNCTIONS
def time_to_seconds(amt, unit):
    " Utility function to convert a stated amount of time into absolute seconds "
    if unit == 'day':
        return amt * 60 * 60 * 24
    if unit == 'month':
        return amt * 60 * 60 * 24 * 30
    if unit == 'year':
        return amt * 60 * 60 * 24 * 30 * 12

def get_file_timestamp(fn):
    " Utility function to get a timestamp from one of my scrape files "
    ts_re = re.compile('\d+_\d+')
    ts = ts_re.search(fn).group()
    dt = datetime.strptime(ts, '%Y%m%d_%H%M%S')
    return dt.date()

# TEST PARSER
if __name__ == '__main__':
    # use one of the scrape files for testing
    test_file = '../scrapes/scrape_20220829_164748.txt'

    # get and parse html from scrape file
    rp = RedditParser(test_file)
    result = rp.go()

    # check entries
    NUM_CHECKS = 10
    for _ in range(NUM_CHECKS): # get N entries
        n = random.randint(0, len(result['title']))

        # make it look nice :)
        print('\n***' + ('*' * 10) + ' ' + str(_) + ' ' + ('*' * 10) + '***\n')

        # get the items
        for k,v in result.items():
            print(f'{k}: {v[n]}')
