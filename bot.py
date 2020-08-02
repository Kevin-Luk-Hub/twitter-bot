import tweepy
from credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, ACCOUNT_NAME, ACCOUNT_ID
from utils import STATE_NAME, STATE_NAME_LOWER, STATE_ABBREV, STATE_NAME_ABBREV, CITY_COUNTRY, KEY_WORDS, CNN, CNN_ID, CDC, CDC_ID, WHO, WHO_ID, WASHINGTON_POST, WASHINGTON_POST_ID, WALL_STREET_JOURNAL, WALL_STREET_JOURNAL_ID, NEW_YORK_TIMES, NEW_YORK_TIMES_ID
from covid_data import getCovidData, create_graph, create_state_tweet, getUSData, getCityData, create_city_tweet
from logger import *
import schedule
import time
import os
from threading import Thread


class TwitterAuthentication():
    def authenticate_user(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api, auth


class StdOutListener(tweepy.StreamListener):
    def on_status(self, data):
        tweet_id, tweet_text, tweet_author, tweet_author_id = getTweetData(
            data)

        if tweet_author.lower() != ACCOUNT_NAME.lower():
            logging.info('Tweet ID: {}'.format(tweet_id))
            logging.info('Tweet author: @{}'.format(tweet_author))
            logging.info('Tweet author ID: {}'.format(tweet_author_id))
            logging.info('Tweet text: {}'.format(tweet_text))

            analyzeTweet(tweet_text, tweet_author, tweet_id)

    def on_error(self, status_code):
        if status_code == 420:
            logging.info('420 ERROR: STOPPED STREAM')
            return False


def followTwitterStream():
    api, auth = TwitterAuthentication().authenticate_user()
    listener = StdOutListener()
    stream = tweepy.Stream(auth, listener)
    stream.filter(follow=[ACCOUNT_ID])


def getTweetData(tweet):
    tweet_id = tweet.id_str
    tweet_text = tweet.text
    tweet_author = tweet.user.screen_name
    tweet_author_id = tweet.user.id

    return tweet_id, tweet_text, tweet_author, tweet_author_id


def analyzeTweet(tweet_text, tweet_author, tweet_id):
    tweet_lower = []
    for word in tweet_text.split():
        tweet_lower.append(word.lower())

    tweet_lower.pop(0)
    new_string = ' '.join(tweet_lower)

    if any(word in new_string for word in KEY_WORDS and STATE_NAME_LOWER):
        if any(word in tweet_text for word in CITY_COUNTRY):
            for city in CITY_COUNTRY:
                if city in tweet_text:
                    cityTweet(city.title(), tweet_id)
        else:
            for state in STATE_NAME_LOWER:
                if state in new_string:
                    stateTweet(state.title(), tweet_id)
    elif any(word in tweet_text for word in KEY_WORDS and STATE_ABBREV):
        for state in STATE_ABBREV:
            if state in tweet_text:
                stateTweet(STATE_NAME_ABBREV.get(state), tweet_id)
    else:
        genericTweet(tweet_text, tweet_author, tweet_id)


def stateTweet(state, tweet_id):
    api, auth = TwitterAuthentication().authenticate_user()
    df = getCovidData(state)
    create_graph(df, state)
    tweet = create_state_tweet(df, state)
    img_id = media_id(state)

    postTweetwithMedia(tweet, tweet_id, img_id)


def cityTweet(city, tweet_id):
    api, auth = TwitterAuthentication().authenticate_user()
    tweet = create_city_tweet(city)

    postTweet(tweet, tweet_id)


def media_id(state):
    api, auth = TwitterAuthentication().authenticate_user()
    media = []

    res = api.media_upload('{}.png'.format(state))
    media.append(res.media_id)
    os.remove('{}.png'.format(state))

    return media


def genericTweet(tweet_text, tweet_author, tweet_id):
    if tweet_author.lower() != ACCOUNT_NAME.lower():
        if 'symptoms' in tweet_text.lower() or 'symptom' in tweet_text.lower():
            tweet = 'The symptoms of COVID-19 include fever or chills, cough, and sore throat. These symptoms may appear 2-14 days after exposure to the virus. Visit https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html to see a complete list of symptoms that you should be aware of.'
            postTweet(tweet, tweet_id)
        elif 'testing' in tweet_text.lower() or 'test' in tweet_text.lower() or 'tested' in tweet_text.lower():
            tweet = 'If you are experiencing any of the symptoms that are associated with COVID-19, stay away from others and monitor your health for the next 14 days. To learn more about getting tested, visit https://www.cdc.gov/coronavirus/2019-ncov/if-you-are-sick/quarantine.html.'
            postTweet(tweet, tweet_id)
        elif 'protect' in tweet_text.lower() or 'safe' in tweet_text.lower():
            tweet = 'Some ways to protect yourself and others from contracting or spreading the virus are following #CDC guidelines, #SocialDistancing , wearing a mask, and washing your hands often. Read about more ways to prevent the spread of the virus at https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/prevention.html.'
            postTweet(tweet, tweet_id)
        elif 'what is covid-19' in tweet_text.lower() or 'what is coronavirus' in tweet_text.lower():
            tweet = 'A novel coronavirus is a new coronavirus that has not been previously identified. The virus causing #COVID19, is not the same as the coronaviruses that commonly circulate among humans and cause mild illness. Learn more about coronaviruses at https://www.cdc.gov/coronavirus/2019-ncov/faq.html.'
            postTweet(tweet, tweet_id)
        else:
            logging.info('Unable to understand: {} from {}'.format(
                tweet_text, tweet_author))


def retweetNews():
    api, auth = TwitterAuthentication().authenticate_user()

    CNN_tweets = api.user_timeline(CNN_ID)
    CDC_tweets = api.user_timeline(CDC_ID)
    WHO_tweets = api.user_timeline(WHO_ID)
    WP_tweets = api.user_timeline(WASHINGTON_POST_ID)
    WS_tweets = api.user_timeline(WALL_STREET_JOURNAL_ID)
    NY_tweets = api.user_timeline(NEW_YORK_TIMES_ID)

    for tweet in CNN_tweets:
        if 'covid-19' in tweet.text.lower() or 'covid19' in tweet.text.lower() or 'coronavirus' in tweet.text.lower():
            api.create_favorite(tweet.id)
            api.retweet(tweet.id)

    for tweet in CDC_tweets:
        if 'covid-19' in tweet.text.lower() or 'covid19' in tweet.text.lower() or 'coronavirus' in tweet.text.lower():
            api.create_favorite(tweet.id)
            api.retweet(tweet.id)

    for tweet in WHO_tweets:
        if 'covid-19' in tweet.text.lower() or 'covid19' in tweet.text.lower() or 'coronavirus' in tweet.text.lower():
            api.create_favorite(tweet.id)
            api.retweet(tweet.id)

    for tweet in WP_tweets:
        if 'covid-19' in tweet.text.lower() or 'covid19' in tweet.text.lower() or 'coronavirus' in tweet.text.lower():
            api.create_favorite(tweet.id)
            api.retweet(tweet.id)

    for tweet in WS_tweets:
        if 'covid-19' in tweet.text.lower() or 'covid19' in tweet.text.lower() or 'coronavirus' in tweet.text.lower():
            api.create_favorite(tweet.id)
            api.retweet(tweet.id)

    for tweet in NY_tweets:
        if 'covid-19' in tweet.text.lower() or 'coronavirus' in tweet.text.lower():
            api.create_favorite(tweet.id)
            api.retweet(tweet.id)


def dailyUpdate():
    tweet = getUSData()
    publishUpdate(tweet)

    schedule.every().day.at("07:00").do(dailyUpdate)


def postTweet(tweet_text, tweet_id):
    api, auth = TwitterAuthentication().authenticate_user()
    api.update_status(status=tweet_text, in_reply_to_status_id=tweet_id,
                      auto_populate_reply_metadata=True)
    logging.info('Replied to tweet: {}'.format(tweet_id))


def postTweetwithMedia(tweet_text, tweet_id, media):
    api, auth = TwitterAuthentication().authenticate_user()
    api.update_status(status=tweet_text, in_reply_to_status_id=tweet_id, media_ids=media,
                      auto_populate_reply_metadata=True)
    logging.info('Replied to tweet: {}, {}'.format(tweet_text, tweet_id))


def publishUpdate(tweet):
    api, auth = TwitterAuthentication().authenticate_user()
    api.update_status(status=tweet)


def publishUpdateHelp():
    schedule.every().day.at("08:40").do(publishUpdate)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    followTwitterStream()
