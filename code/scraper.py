#!python
"""
Utilities for scraping Reddit

NOTES: Need selenium for this if not using API since all post content is
loaded dynamically as json, which cannot be accessed directly without
authentication.
"""

from selenium import webdriver

from time import sleep
from datetime import datetime

import json

# RedditReader default params
ASTROLOGY_URL = 'https://www.reddit.com/r/astrology/'

# By default I think the above goes to "hot" posts
# Try also URLs for
#   r/astrology/new (sorted by newest posts)
#   r/astrology/top/?t=all (top posts all time)
# Reddit API only allows 1000 max results per query. As far as I can tell
# there is no way to search by date to iterate over time periods. Third party
# resources are not giving me the most usable data.
#

class RedditReader:
    """
    A class to scrape Reddit. Using a class here to support 'with' call
    so I don't forget to quit the driver.

    URL is passed into constructor, so class will act like a container for
    all data pertaining to one URL.
    """
    def __init__(self, url = ASTROLOGY_URL):
        self.url = url
        self.driver = None
        self.sleep_time = 2
        self.src = ''

    ### AUTO-CONTROL ('with' statement handling)
    def __enter__(self):
        " start selenium driver ('with' syntax)"
        self.open()
        return self

    def __exit__(self, e_type, e_val, e_trace):
        " close selenium driver ('with' syntax) "
        self.close()
        return False # DO NOT IGNORE EXCEPTIONS - NEED THEM TO DEBUG

    ### DRIVER MANUAL CONTROL
    def open(self):
        " start selenium driver "
        self.driver = webdriver.Chrome()
        return self

    def close(self):
        " quit selenium driver "
        self.driver.quit()
        return self

    def get(self):
        " get url "
        self.driver.get(self.url)
        self.sleep()
        return self

    ### DOCUMENT CONTROL
    def scroll_to(self, to = -1):
        " scroll to document position "
        if to < 0:
            to = self.get_scroll_height()


        script = 'window.scrollTo({ left: 0, top: '\
            + str(to)\
            + ', behavior: "smooth"});'

        self.driver.execute_script(script)
        self.sleep()
        return self

    def scroll(self):
        " scroll to bottom (convenience method) "
        self.scroll_to(-1)
        return self

    def cache_page_source(self):
        " Cache page source text (to use with e.g. write_page_source() "
        self.src = self.driver.page_source
        return self

    def get_page_source(self):
        self.cache_page_source()
        " Get cached source code "
        return self.src

    def get_scroll_height(self):
        " Get page scroll height "
        return self.driver.execute_script("return document.body.scrollHeight;")

    ### UTILITIES
    def set_sleep_time(self, t = 1):
        " Set the default sleep time for processing "
        self.sleep_time = t
        return self

    def sleep(self, t = None):
        " Sleep for t seconds (wrapper for time.sleep()) "
        if t == None: t = self.sleep_time
        sleep(t)
        return self

    def write_page_source(self, prefix='scrape', ext='txt', dir='../scrapes/'):
        self.cache_page_source()
        " Write source to file with timestamp "
        src = self.src
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = prefix + '_' + timestamp + '.' + ext
        with open(dir + fn, 'w') as f:
            f.write(src)

        return self

# SELF-EXECUTE SCRAPER
if __name__ == '__main__':
    import sys
    import re
    import time

    # times
    GET_TIMEOUT_S = 4 # wait time for page load
    SCROLL_TIMEOUT_S = (60 * 10) # timeout for distance scrolling
    SCROLL_SLEEP_S = 8 # wait time per scroll

    re_arg = re.compile('^(n|h|t)(\d+)$')

    # type of measurement and amount as string <char><int>
    #   'n' number of scrolls
    #   'h' scrollheight
    #   't' time (seconds)
    dist = 't10' if len(sys.argv) <= 1 else sys.argv[1].strip()
    url = ASTROLOGY_URL if len(sys.argv) <= 2 else sys.argv[2].strip()

    re_arg_match = re_arg.match(dist)

    # the argument split into type and amount
    a_type = re_arg_match.group(1)
    a_amt = int(re_arg_match.group(2))



    with RedditReader(url) as rr:
        print("START", a_type, a_amt)

        rr.set_sleep_time(GET_TIMEOUT_S) # to be safe and allow page to load fully
        rr.get()
        print("Page Loaded")

        rr.set_sleep_time(SCROLL_SLEEP_S) # to be safe and allow dynamic load

        if a_type == 'n':
            # scroll a specified number of times
            print(f'Scrolling {a_amt} times...')
            for i in range(a_amt):
                print('> ' + str(i + 1))
                rr.scroll()
        elif a_type == 'h':
            # scroll until page has reached a max scrollHeight
            # let's have a timeout as well
            print(f'Scrolling to pageheight {a_amt}...')
            elapsed = 0
            while rr.get_scroll_height() < a_amt:
                time_start = time.time()
                rr.scroll()
                time_end = time.time()
                elapsed = elapsed + (time_end - time_start)
                print(f'> {rr.get_scroll_height()}')
        elif a_type == 't':
            # scroll until time's up
            print(f'Scrolling for {a_amt} seconds...')
            elapsed = 0
            while elapsed < a_amt:
                time_start = time.time()
                rr.scroll()
                time_end = time.time()
                elapsed = elapsed + (time_end - time_start)
                print(f'> {elapsed}')
        else:
            print("No Args - Exiting")

        print('Writing to file...')
        rr.write_page_source()
        print('DONE')

