"""
Utilities for scraping Reddit r/astrology

NOTES: Need selenium for this if not using API since all post content is
loaded dynamically as json, which cannot be accessed directly without
authentication.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from datetime import datetime

astrology_url = 'https://www.reddit.com/r/astrology/'

class RedditReader:
    """
    A class to scrape Reddit. Using a class here to support 'with' call
    so I don't forget to quit the driver.

    URL is passed into constructor, so class will act like a container for
    all data pertaining to one URL.
    """
    def __init__(self, url = astrology_url):
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
        return True # ignore exceptions

    ### DRIVER MANUAL CONTROL
    def open(self):
        " start selenium driver "
        self.driver = webdriver.Chrome()
        sleep(self.sleep_time)
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
        src = self.src
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = prefix + '_' + timestamp + '.' + ext
        with open(dir + fn, 'w') as f:
            f.write(src)

        return self
