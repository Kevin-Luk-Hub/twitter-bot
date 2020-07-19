import tweepy
from random import randint
import datetime
import time
import os
import requests
import json
import covid_data

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(str(tweet.id) + '-' + tweet.text + '\n')


def reply_to_tweets():
    try:
        print('retrieving tweets at...')
        mention_tweets = api.mentions_timeline()
        for mention in reversed(mention_tweets):
            print(mention.text)
            recent_mention = mention.id
            api.create_favorite(recent_mention)
            api.retweet(recent_mention)
            api.update_status('@' + mention.user.screen_name +
                              ' ' + '{}'.format(randint(0, 100000)), mention.id)
    except tweepy.TweepError as e:
        print(e.response.text)


def random_number():
    return str(randint(-100000, 100000))


def get_time():
    return str(datetime.datetime.now())


def get_Quote():
    params = {
        'method': 'getQuote',
        'lang': 'en',
        'format': 'json'
    }
    res = requests.get('http://api.forismatic.com/api/1.0/', params)
    jsonText = json.loads(res.text)
    return jsonText["quoteText"], jsonText["quoteAuthor"]


def live_tweet():
    api.update_status('{}, {}, {}'.format(
        get_Quote(), get_time(), random_number()))


while True:
    print('tweeting...')
    live_tweet()
    time.sleep(5)
