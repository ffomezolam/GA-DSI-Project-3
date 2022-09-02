#!python

"""
Script to get post urls from search results and scrape origin post for each
result. Necessary due to search results not having body text. Need to load each
post separately and scrape individually.
"""

from bs4 import BeautifulSoup
import os

# STEP 0: GET SCRAPE FILES
SCRAPE_DIR = '../scrapes/search/'
scrape_files = os.listdir(SCRAPE_DIR)

# STEP 1: GET ALL URLS
urls = set()

for file in scrape_files:
    path = SCRAPE_DIR + file
    with open(path, 'r') as f:
        print(f'opening file: {file}')
        s = BeautifulSoup(f.read(), 'lxml')

    links = s.find_all('a', {'data-click-id': 'body'})
    for link in links:
        url = link.attrs['href']
        urls.add(url)

    print(f'{len(links)} links')

print(f'num urls: {len(urls)}')
