
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
    try:
        response = requests.get(link)
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
        text = "\n\n".join([p.text for p in paragraphs if not p.is_boilerplate])
        print("Success")
        return text
    except:
        print("failed")
        return("")

def getNews(subText, n=20):
    submissions = []
    for submission in reddit.subreddit(subText).hot(limit=n):
        print(submission.url)
        submissions.append((submission.title, submission.url))
    return submissions
def formatNews(subreddit='news',articles= 40):
    print("getting news")
    subs = getNews('news', 40)
    print("Done")
    newslist = []
    for e in subs:
        
        #newstring = newstring +  get_text(e[1]) + ' '*500
        print(e[1])
        newslist.append(get_text(e[1]))
    return newslist
        


    
    
    