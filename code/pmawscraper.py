#!python

from pmaw import PushshiftAPI
import time

from scraper import RedditReader

# connect to pushift api and get lots of posts

api = PushshiftAPI()
posts = api.search_submissions(subreddit='astrology', limit=3000)
plist = [p for p in posts]
links = [p['full_link'] for p in plist]

print(f'{len(links)} links')

with RedditReader() as rr:
    for num, url in enumerate(links):
        print(f'{num}: {url}')
        rr.set_url(url)
        rr.get()
        rr.write_page_source(prefix='scrape_page', dir='../scrapes/page/')
        rr.sleep(2)

