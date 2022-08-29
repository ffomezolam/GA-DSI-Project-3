"""
Utilities for scraping Reddit r/astrology

NOTES: Need selenium for this if not using API since all post content is loaded dynamically as json, which cannot be accessed directly without authentication.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

astrology_url = 'https://www.reddit.com/r/astrology/'

class RedditReader:
    """
    Use class here to support 'with' call so I don't forget to quit the
    driver
    """
    def __init__(self, url = astrology_url):
        self.url = url
        self.driver = None
        self.sleep_time = 1

    def __enter__(self):
        self.driver = webdriver.Chrome()
        sleep(self.sleep_time)
        return self

    def set_sleep_time(self, t = 1):
        self.sleep_time = t
        return self

    # allow control here
    def scroll_to(self, to = -1):
        if to < 0: pass # scroll to bottom
        else: pass #scroll to position
        # remember to sleep to allow this to work

    def get_source(self):
        return self.driver.page_source

    def __exit__(self):
        self.driver.quit()
