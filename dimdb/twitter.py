import tweepy
from flask import current_app, g

def get_api():
    if "twitter_api" not in g:
        consumer_key = current_app.config["TWITTER_CONSUMER_KEY"]
        consumer_secret = current_app.config["TWITTER_CONSUMER_SECRET"]
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        g.twitter_api = tweepy.API(auth)
    return g.twitter_api

def search_tweets(query, count=10):
    return get_api().search(query, lang="en", rpp=count)
