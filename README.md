# Project 3

General Assembly DSI Project 3: Classification Modeling

*This is a data science project done for the General Assembly Data Science
Immersive cohort starting July 25, 2022*

## Problem Statement

I am to create a classification model to predict engagement on Reddit.

Engagement is split into high and low engagement, determined by number of
comments above and below median number of comments.

For this project, I am focusing on the /r/astrology subreddit, to try and
predict engagement on the astrology forums. To the stars!

## Summary

This project was performed in python, using jupyter notebook as primary
processor.

In order to complete this project I performed the following:

1. **Web Scraping:** I scraped the /r/astrology Reddit page for information
   including:
   - Title text
   - Number of comments
   - Date posted (or time elapsed since posted)
   - Body text

2. **Cleaning and EDA:** I compiled all data into a pandas dataframe and ensured
   no missing entries and proper formatting of data.

3. **Modeling:** I ended up using Random Forest classifier and Multinomial
   Naive Bayes classifier as the primary models. Random Forest performed best
   so it was used for reporting results.

4. **Reporting:** I analyzed and interpreted the model results and predictions
   using various metrics and reports.

## 0. Packages Etc.

In order to perform this task, I created a number of scripts to help with
repetitive tasks (all located in `code` folder):

- `parser.py`: exports a class which handles parsing of the reddit html
documents, using BeautifulSoup python package as underlying parser
- `scraper.py`: exports a class which handles scraping of reddit and exporting
to a text file, using Selenium as the back-end. This script also runs the main
page scrape if run from the command line.
- `pmawscraper.py`: *NOT USED* - I wrote this to try the Pushshift api, but the
majority of results led to deleted posts, so I ended up scrapping the idea
- `multiscraper.py`: a script which uses `scraper.py` to scrape Reddit search
pages - it handled search queries and writing html source to disk
- `searchpostscraper.py`: a script which was used on the output of
`multiscraper.py` to get content of posts found (because search results do not
show body text)
- `ipynb_utils.py`: a set of definitions and functions that automated
repetitive tasks needed in completing the jupyter notebooks

NTLK package was used for stopwords and attempts at stemming. The rest of the
packages used are standard data science packages (pandas, scikit-learn, etc.)

## 1. Web Scraping

I limited myself early on to manually scraping the html from the [Reddit web
site](https://www.reddit.com). A lot of code was written for this task
before realizing that there were post-count limits (scrolling down a Reddit page
cannot be performed indefinitely - it is limited to about 1000 posts).
Therefore, I found workarounds rather than moving to an API.

My one API exploration ended in disaster when, while using the Pushshift API
(pmaw), I discovered that a majority of the posts it was giving me were deleted
on Reddit. I therefore abandoned it.

I have not tried the official Reddit API (or the praw wrapper).

I discovered that using search terms under a subreddit would give posts that
would otherwise not be discoverable by plain browsing, so as a workaround to
the scroll limit, I used search terms that were arbitrarily chosen and chosen
via exploration into the most common words used in Reddit posts and titles
(taken from /r/astrology main page scrapes). A combination of regular main page
scraping and search term scraping eventually got me over 10,000 posts.

## 1a. Parsing

I used BeautifulSoup to parse all scraped content. See various `tags.json`
files in `code` directory for tags used to extract content. See also
`parser.py` script for main parsing script.

## 2. Cleaning and EDA

Minimal cleaning was necessary, as parsing stage had ensured proper values and
no missing values.

Minimal EDA necessary. I generated a few features (word- and character-count
related), predicting they might come in handy.

## 3. Modeling

Modeling involved some exploration. After reviewing a number of models
I determined that Random Forest classification model was most accurate, with
Multinomial Naive Bayes classifier next in line. Most modeling was focused on
the Random Forest model, with Naive Bayes acting as backup to check that scores
were consistent.

Scikit-Learn's CountVectorizer was used along with NLTK's stopwords list to
vectorize the text tokens in body and title. These were stored and used
throughout the modeling process.

I started by modeling the vectorized title text and the vectorized body text
against the binary target of "comment count greater than median comment count".
Both models scored higher than baseline, but provided good insight into
predictor words.

I then attempted modeling with more features, settling finally on the following
features:
- title text vectorized
- body text vectorized
- title word and character counts
- body word and character counts
- month of post
- year of post

This resulted in the highest accuracy model, at 72% accuracy. However, the
predictive results it gave back were mostly nonsense, with the body predictors
being mainly numbers (such as "00").

Exploration of other features' relationships to target showed little predictive
value as separate predictors. Though there were some curiosities:
- Thursdays are apparently a big day for comments, with a huge spike in
comments on Thursdays
- September is apparently a big month for comments, with a huge spike in
comments in September

I have not explored why these spikes appear. Due to the method of obtaining the
data, I am skeptical about the date distributions (I was not able to obtain
data chronologically over a long period of time, so I do not know the actual
distribution of Reddit posts over time).

## 4. Reporting

In short, after doing the above modeling, I concluded that the simpler model
was the most effective at providing guidelines, despite the lesser predictive
accuracy.

The no-holds-barred many-features model had the highest accuracy (72%) but gave
me very little to go on if I was to be using it to guide how I write my next
engaging post on the /r/astrology subreddit. However, the less-accurate
word-vector-only posts gave quite good information. Words and phrases such as
the following came up as quite strong preditors:
- "anyone else"
- "question"
- "think"
- "sagittarius"

In conclusion, I would use the simpler models to guide future posts on Reddit,
seeing as calls to action ("question', "anyone else") and specific category
references ("sagittarius") have shown to be stronger predictors in these models
and are quite transparent and interpretable. So in the next post, I would start
with "QUESTION: Is anyone else a sagittarius?"!
