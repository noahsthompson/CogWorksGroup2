
#
import json
import feedparser
import justext
import pickle
import requests
import sys
import pprint
import time

def get_text(link):
    response = requests.get(link)
    print(response)
    paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
    text = "\n\n".join([p.text for p in paragraphs if not p.is_boilerplate])
    return text

def collect(url, filename):
    # read RSS feed
    d = feedparser.parse(url)
    # grab each article
    texts = {}
    for entry in d["entries"]:
        time.sleep(3)
        link = entry["link"]
        print("downloading: " + link)
        text = get_text(link)
        texts[link] = text
    
    # pickle
    pickle.dump(texts, open(filename, "wb"))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python collect_rss.py <url> <filename>")
        sys.exit(1)
    
    # https://www.reuters.com/tools/rss
    # http://feeds.reuters.com/Reuters/domesticNews
    url = sys.argv[1]
    filename = sys.argv[2]
    collect(url, filename)


    
    
import requests
from bs4 import BeautifulSoup
session = requests.Session()
url = "http://www.nytimes.com/2015/01/02/world/europe/turkey-police-thwart-attack-on-prime-ministers-office.html"
req = session.get(url)
soup = BeautifulSoup(req.text, 'lxml')
paragraphs = soup.find_all('p', class_='story-body-text story-content')

article = ''
    
for p in paragraphs:
    article = article + p.get_text()

    
import praw

reddit = praw.Reddit(client_id='SZVF0BoCDrUdpg',
                     client_secret='wVR1_UU1mvdru1uAlGj4YxAbUhg',
                     password='dysfunctional',
                     user_agent='RedditCog2:v1.0.0 (by /u/CogGroup2)',
                     username='CogGroup2')

import time
for submission in reddit.subreddit('jokes').hot(limit=3):
    print('-'*100, '\n\n')
    print(submission.title, '\n\n') #' ', submission.score, ' upvotes\n\n')
    time.sleep(4)
    print(submission.selftext)
    time.sleep(5)
    
    
jokeList = []
for submission in reddit.subreddit('jokes').hot(limit=5):
    jokeList.append(submission)

print(jokeList[count])#.over_18))  
    
jokesTold = 0
count = 0
while jokesTold < 3:
    if not(jokeList[count].over_18):
        print('-'*100, '\n\n')
        print(submission.title, '\n\n') #' ', submission.score, ' upvotes\n\n')
        time.sleep(2 + (len(submission.title)/40))
        print(submission.selftext)
        time.sleep(5)
        jokesTold +=1
    count +=1

def getTopPosts(subText, n=100):
    for submission in reddit.subreddit(subText).hot(limit=1000):
        yield submission
    '''time.sleep(4)
    print(submission.selftext)
    time.sleep(5)'''
    '''top_level_comments = list(submission.comments)
    for comment in top_level_comments[1:5]:
        print(comment.body)
    for i in range(5):
        print(top_level_comments[i].body)
        print('\n\n')
        time.sleep(1)'''
    
def getNews(subText, n=20):
    submissions = []
    for submission in reddit.subreddit(subText).hot(limit=n):
        submissions.append((submission.title, submission.url))
    return submissions

subs = getNews('news', 40)

newstring = ''
for e in subs:
    newstring = newstring +  get_text(e[1]) + ' '*500

with open('news.txt', 'a') as f:
    f.write(newstring)
f.close()
    
import requests
from bs4 import BeautifulSoup
#import urllib2

linkURL = subs[0][1]
print(get_text(linkURL))
session = requests.Session()
req = session.get('http://www.bbc.co.uk/news/world-us-canada-40750071')# linkURL)


soup = BeautifulSoup(req.text, 'lxml')
#print(soup)




paragraphs = soup.find_all('p', class_='story-body-text story-content')

print(paragraphs)
article = ''
    
for p in paragraphs:
    article = article + p.get_text()

print(article)

import pytesseract
from PIL import Image
print(pytesseract.image_to_string(Image.open('test.jpeg')))


def getTopPosts(subText, n=100):
    for submission in reddit.subreddit(subText).hot(limit=1000):
        yield submission
    '''time.sleep(4)
    print(submission.selftext)
    time.sleep(5)'''
    '''top_level_comments = list(submission.comments)
    for comment in top_level_comments[1:5]:
        print(comment.body)
    for i in range(5):
        print(top_level_comments[i].body)
        print('\n\n')
        time.sleep(1)'''
    
def getNews(subText, n=20):
    submissions = []
    for submission in reddit.subreddit(subText).hot(limit=n):
        submissions.append((submission.title, submission.url))
    return submissions

subs = getNews('news', 40)

newstring = ''
for e in subs:
    newstring = newstring +  get_text(e[1]) + ' '*500

with open('news.txt', 'a') as f:
    f.write(newstring)
f.close()
    
    
    
    
    

