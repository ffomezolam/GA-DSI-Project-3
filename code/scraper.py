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

    ### AUTO-CONTROL ('with' statement handling)
    def __enter__(self):
        " start selenium driver ('with' syntax)"
        self.open()
        return self

    def __exit__(self):
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

    ### DOCUMENT CONTROL
    def scroll_to(self, to = -1):
        " scroll to document position "
        if to < 0: 
            to = self.get_scroll_height()

        script = f'window.scrollTo(0, {to}, behavior="smooth");'
        self.driver.execute_script(script)
        self.sleep()
        return self

    def get_page_source(self):
        " Get source code "
        return self.driver.page_source

    def get_scroll_height(self):
        " Get page scroll height "
        return self.driver.execute_script("return document.body.scrollHeight;")

    ### UTILITIES
    def set_sleep_time(self, t = 1):
        " Set the default sleep time for processing "
        self.sleep_time = t
        return self

    def sleep(self, t = self.sleep_time):
        " Sleep for t seconds (wrapper for time.sleep()) "
        time.sleep(t)
        return self
