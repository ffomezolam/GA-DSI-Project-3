#!python

"""
Script to get post urls from search results and scrape origin post for each
result. Necessary due to search results not having body text. Need to load each
post separately and scrape individually.
"""

from bs4 import BeautifulSoup
import os
from scraper import RedditReader
from timer import Timer

# STEP 0: GET SCRAPE FILES
SCRAPE_DIR = '../scrapes/search/'
scrape_files = os.listdir(SCRAPE_DIR)

# STEP 1: GET ALL URLS
urls = set()

timer = Timer()
timer.start()
for file in scrape_files:
    path = SCRAPE_DIR + file
    with open(path, 'r') as f:
        print(f'opening file: {file[:40]:<40}', end='')
        s = BeautifulSoup(f.read(), 'lxml')

    links = s.find_all('a', {'data-click-id': 'body'})
    for link in links:
        url = link.attrs['href']
        urls.add(url)

    print(f'\t> {len(links)} links')

print(f'> num unique urls: {len(urls)}', end=' ')
print(f'(elapsed time: {timer.elapsed()} seconds)')
print()

# STEP 2: OPEN SELENIUM AND GET SOURCE FOR EACH POST
with RedditReader() as rr:
    print("***--- START SCRAPE ---***")
    timer.restart()
    for num, url in enumerate(list(urls)):
        full_url = 'https://www.reddit.com/' + url
        print(f'> {num}: {url}')
        rr.set_url(full_url)
        rr.get()
        rr.write_page_source(prefix='scrape_page', dir='../scrapes/page/')
        rr.sleep(3)

    print(f"* COMPLETED. Elapsed Time: {timer.elapsed()}")
