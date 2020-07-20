import tweepy
from credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from utils import get_weekday
from manage_id import FILE_NAME, FILE_NAME_MESSAGE, store_last_seen_id, retrieve_last_seen_id, store_last_message_id, retrieve_last_message_id
from threading import Thread
import time


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def reply_to_tweets():
    print('Searching for tweets...')
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mention_tweets = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    try:
        for mention in reversed(mention_tweets):
            last_tweet = mention.id
            store_last_seen_id(last_tweet, FILE_NAME)
            api.create_friendship(mention.user.id)
            api.create_favorite(last_tweet)
            api.retweet(last_tweet)
            api.update_status(
                '@{} Happy {}!'.format(mention.user.name, get_weekday()), mention.id)
            print('Successfully replied to tweet')
    except tweepy.TweepError as e:
        print(e)
        print('Unable to reply to tweet')


def reply_to_message():
    print('Replying to DMs...')
    last_seen_id = retrieve_last_message_id(FILE_NAME_MESSAGE)
    all_messages = api.list_direct_messages()

    try:
        for message in all_messages:
            recent_message = message.id
            store_last_message_id(recent_message, FILE_NAME_MESSAGE)
            if message_create['sender_id'] == recent_message:
                return
            else:
                api.send_direct_message(
                    message.message_create['sender_id'], 'Hello! I am a bot that was created by @KhovinL. Please contact him with any questions!')
                print('Successfully replied to message')
    except tweepy.TweepError as e:
        print(e)
        print('Unable to reply to message')


while True:
    Thread(target=reply_to_message()).start()
    Thread(target=reply_to_tweets()).start()
    time.sleep(5)
