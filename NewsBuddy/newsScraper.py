
#
import json
import feedparser
import justext
import pickle
import requests
import sys
import pprint
import time
import praw
#from bs4 import BeautifulSoup
reddit = praw.Reddit(client_id='SZVF0BoCDrUdpg',
                     client_secret='wVR1_UU1mvdru1uAlGj4YxAbUhg',
                     password='dysfunctional',
                     user_agent='RedditCog2:v1.0.0 (by /u/CogGroup2)',
                     username='CogGroup2')


def get_text(link):
    response = requests.get(link)
    paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
    text = "\n\n".join([p.text for p in paragraphs if not p.is_boilerplate])
    return text
def getNews(subText, n=20):
    submissions = []
    for submission in reddit.subreddit(subText).hot(limit=n):
        submissions.append((submission.title, submission.url))
    return submissions
def formatNews(subreddit='news',articles= 40):
    subs = getNews('news', 40)
    newslist = []
    for e in subs:
        
        #newstring = newstring +  get_text(e[1]) + ' '*500
        newslist.append(get_text(e[1]))
    return newslist
        


    
    
    