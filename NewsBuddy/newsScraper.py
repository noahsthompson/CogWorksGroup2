
import json
import feedparser
import justext
import pickle
import requests
import sys
import pprint
import time
import praw

#Global reddit api key
reddit = praw.Reddit(client_id='SZVF0BoCDrUdpg',
                     client_secret='wVR1_UU1mvdru1uAlGj4YxAbUhg',
                     password='dysfunctional',
                     user_agent='RedditCog2:v1.0.0 (by /u/CogGroup2)',
                     username='CogGroup2')


def get_text(link):
    """Gets text of an article given a link
        Params
        ------
        link(str): string representation of link
        Returns
        -------
        (str):text from website
        Note
        ----
        This function eats an exception because of a potential bad handshake error, which happens because some websites use a
        depreciated  certificates which certifi removed. It only happens rarely, but it will crash the app if an article links to
        a website that uses those certificates."""
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
    """Gets the n top hot links on the subtext
        Params:
        subText(str):the name of the subreddit
        n(int(optional,default=10)): number of posts to get from the subtext subreddit
        Returns:
        List of top n hot submissions on subText subreddit"""
    submissions = []
    for submission in reddit.subreddit(subText).hot(limit=n):
        print(submission.url)
        submissions.append((submission.title, submission.url))
    return submissions

def formatNews(subreddit='news',articles= 40):
    """Takes name of subreddit and number of articles, returns text from top n submissions in subreddit
        Params
        ------
        subreddit(str(optional, default=news)):Name of subreddit to scrape
        articles(int(optional, default-40)): Number of submissions on subreddit to scrape
        Returns
        -------
        (list(str)): text from top n submissions on subreddit"""
    print("getting news")
    subs = getNews('news', 40)
    print("Done")
    newslist = []
    for e in subs:
        print(e[0])
        newslist.append((e[0],get_text(e[1])))
    return newslist
        


    
    
    