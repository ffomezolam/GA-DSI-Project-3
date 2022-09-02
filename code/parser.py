#!python
"""
Utilities for parsing Reddit html

DISCLAIMER: THIS IS NOT PRODUCTION-READY CODE. DO NOT USE UNLESS YOUR NAME IS
ANDREW MALOZEMOFF AND/OR YOU AGREE TO ASSUME ANY AND ALL RISK!
"""

from bs4 import BeautifulSoup

from datetime import datetime, timedelta

import json
import re

### REDDITPARSER CLASS
class RedditParser:
    """
    Class to parse Reddit source html and convert to dataframe and write
    to csv
    """

    def __init__(self, file_path, tags_file = 'tags.json'):
        with open(file_path, 'r') as f:
            src = f.read()

        self.file = file_path
        self.soup = None
        self.nposts = 0
        self.tags = None

        # make sure tags file name is properly formatted
        if not tags_file.endswith('.json'): tags_file += '.json'

        # load relevant tag info
        with open(tags_file, 'r') as tags:
            self.tags = json.loads(tags.read())

        if src: self.load(src)

        self.result_ = None
        self.result_len_ = None

    def load(self, src):
        self.soup = BeautifulSoup(src, 'lxml')
        return self

    def go(self):
        " Run the parser and capture all data into a dictionary "

        posts = self.get_content('post')
        types = ['title','time','comments','body-text', 'media']

        # initialize result dictionary
        self.result_ = dict()

        # put all content into results dictionary
        for type in types:
            self.result_[type] = [self.get_content(type, post)
                                  for post in posts]

        self.result_len_ = len(self.result_[types[0]])

        # make a derived ID for each post
        self.result_['uid'] = list()
        for ix in range(self.result_len_):
            title = self.result_['title'][ix]
            title_len = len(title)
            body = self.result_['body-text'][ix]
            body_len = len(body)
            no_whitespace_re = re.compile(r'\s+')
            uid = str(title_len)\
                + re.sub(no_whitespace_re, '', title)\
                + str(body_len)

            self.result_['uid'].append(uid)

        return self.result_

    def get_content(self, type='post', container=None):
        " get content from html, optionally from inner container "

        tag = self.tags[type]['tag']
        attrs = self.tags[type]['attrs']

        # Remove any extra attributes from json
        # Those were there just in case I needed them
        while len(attrs) > 1: attrs.popitem()

        # Process all relevant tags
        if not container: return self.soup.find_all(tag, attrs)
        else:
            # get html in container
            html = container.find(tag, attrs)

            if not html:
                # return if no result
                return ''
            else:
                if type == 'media':
                    # special case for media element - a little hacky because
                    # tacked on after everything else was already done.
                    # need to check to make sure we actually have media, then
                    # return a boolean
                    return "True"
                else:
                    # process text
                    return self.process(type, html.text)

    def process(self, type, text):
        " Process obtained string depending on data type "

        # strip all start/end whitespace
        text = text.strip()

        # handle any special cases
        if type == 'comments':
            text = text.split(' ')[0]
            if text.endswith('k'):
                text = float(text[:-1]) * 1000

            text = int(text)

        if type == 'time':
            # convert time string to seconds
            num, desc = text.split(' ')[0:2]
            if desc.endswith('s'): desc = desc[:-1]
            secs = time_to_seconds(int(num), desc) or 0
            secs = timedelta(seconds=secs)

            # get the time of the scrape
            scrape_time = get_file_timestamp(self.file)

            # subtract post relative timing from scrape time...
            post_date = scrape_time - secs

            # gives us the approximate date of the post
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
    import random
    import os
    from sklearn.feature_extraction.text import CountVectorizer
    import numpy as np
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    import pandas as pd

    # use one of the scrape files for testing
    scrape_dir = '../scrapes/'
    scrape_files = os.listdir(scrape_dir)
    test_file = scrape_dir + scrape_files[0]

    print("\n***--- TESTING PARSER ---***\n")
    # get and parse html from scrape file
    rp = RedditParser(test_file)
    result = rp.go()

    NUM_CHECKS = 6

    # check entries
    for _ in range(NUM_CHECKS): # get N entries
        n = random.randint(0, len(result['title']))

        # make it look nice :)
        print('\n***' + ('*' * 10) + ' ' + str(_) + ' ' + ('*' * 10) + '***\n')

        # get the items
        for k,v in result.items():
            print(f'{k}: {v[n]}')

    print("\n\n***--- COUNTING WORDS (title + body) ---***\n")
    # get word counts
    alltext = [result['title'][i] + ' ' + result['body-text'][i]
               for i in range(len(result['title']))]
    cv = CountVectorizer(stop_words = stopwords.words('english'))
    words = cv.fit_transform(alltext)
    wdf = pd.DataFrame(words.todense(), columns=cv.get_feature_names_out())
    print(wdf.sum().sort_values(ascending=False))
