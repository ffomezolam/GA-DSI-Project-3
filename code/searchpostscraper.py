#!python

"""
Script to get post urls from search results and scrape origin post for each
result. Necessary due to search results not having body text. Need to load each
post separately and scrape individually.
"""

from bs4 import BeautifulSoup
import os
import time
from scraper import RedditReader

# STEP 0: GET SCRAPE FILES
SCRAPE_DIR = '../scrapes/search/'
scrape_files = os.listdir(SCRAPE_DIR)

# STEP 1: GET ALL URLS
urls = set()

start_time = time.time()
for file in scrape_files:
    path = SCRAPE_DIR + file
    with open(path, 'r') as f:
        print(f'opening file: {file}', end='')
        s = BeautifulSoup(f.read(), 'lxml')

    links = s.find_all('a', {'data-click-id': 'body'})
    for link in links:
        url = link.attrs['href']
        urls.add(url)

    print(f'\t> {len(links)} links')

print(f'> num unique urls: {len(urls)}', end=' ')
print(f'(elapsed time: {time.time() - start_time} seconds)')
print()

# STEP 2: OPEN SELENIUM AND GET SOURCE FOR EACH POST
rr = RedditReader()

for url in list(urls)[:3]:
    print("> " + url)
    rr.url(url)
    rr.get()
    rr.write_page_source(prefix='scrape_page', dir='../scrapes/page/')
    rr.sleep(5)
