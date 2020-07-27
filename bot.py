import tweepy
from credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, ACCOUNT_NAME, ACCOUNT_ID
import json


class StdOutListener(tweepy.StreamListener):
    def on_status(self, data):
        tweet_id, tweet_text, tweet_author, tweet_author_id = getTweetData(
            data)
        responseTweet(tweet_text, tweet_author, tweet_id)

    def on_error(self, status_code):
        if status_code == 420:
            return False


def authenticate_user():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api, auth


def get_stream():
    api, auth = authenticate_user()
    listener = StdOutListener()

    stream = tweepy.Stream(auth, listener)
    stream.filter(follow=[ACCOUNT_ID], track=[ACCOUNT_NAME])


def responseTweet(tweet_text, tweet_author, tweet_id):
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


def postTweet(tweet_text, tweet_id):
    api, auth = authenticate_user()
    api.update_status(status=tweet_text, in_reply_to_status_id=tweet_id,
                      auto_populate_reply_metadata=True)
    print('replied to tweet')


def getTweetData(tweet):
    tweet_id = tweet.id_str
    tweet_text = tweet.text
    tweet_author = tweet.user.screen_name
    tweet_author_id = tweet.user.id

    return tweet_id, tweet_text, tweet_author, tweet_author_id


if __name__ == "__main__":
    get_stream()
