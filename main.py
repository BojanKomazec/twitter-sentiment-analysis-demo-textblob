'''
This script uses TweePy package to read a number of tweets which contain given 
string and then performs sentiment analysis on them by using textblob package 
API.

Script arguments:
    <security_settings_file> - path to the JSON file which contains Twitter App 
        security settings. Use twitter_app_security_settings.json.template as 
        its template. Visit https://apps.twitter.com to create an app and all 
        security tokens.
    <topic> - topic (term) for which script determines the sentiment

Script output:
    The average sentiment (in range between -1 and 1) on the given term obtained 
    from all direct tweets (not retweets) for which subjectivity is less than 
    0.5.

Author: Bojan Komazec
'''

import sys
import json
import tweepy

from sys import argv
from pprint import pprint
from tweepy.error import TweepError
from textblob import TextBlob

class TwitterAppSecuritySettings:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

def load_app_security_settings(settings_file):
    with open(settings_file) as json_data:
        data = json.load(json_data)
        pprint(data)
        for item in data:
            print(item)
        security_settings = TwitterAppSecuritySettings(
            data["consumer_key"],
            data["consumer_secret"],
            data["access_token"],
            data["access_token_secret"]
        )
        return security_settings

def create_auth_handler(security_settings):
    auth = tweepy.OAuthHandler(security_settings.consumer_key, security_settings.consumer_secret)
    auth.set_access_token(security_settings.access_token, security_settings.access_token_secret)
    return auth

def main():
    if len(argv) != 3:
        print("Usage: main.py <security_settings_file> <topic>")
        return

    try:
        security_settings = load_app_security_settings(argv[1])
        auth = create_auth_handler(security_settings)

        api = tweepy.API(auth)
        TWEETS_COUNT_MAX = 500 # can be 9999999
        #search_result_tweets = api.search(q = argv[2], lang = "en", rpp = 100, count = TWEETS_COUNT_MAX, tweet_mode = "extended")
        search_result_tweets = tweepy.Cursor(api.search, q = argv[2] + " -filter:retweets", lang = "en", tweet_mode = "extended").items(TWEETS_COUNT_MAX) 

        polarity_total = 0
        objective_sentiments_count = 0
        for tweet in search_result_tweets: 
            print(tweet.full_text)
            analysis = TextBlob(tweet.full_text)
            print(analysis.sentiment)
            print()
            if (analysis.sentiment.subjectivity < 0.5) :
                polarity_total += analysis.sentiment.polarity
                objective_sentiments_count += 1
        print()
        print("Average polarity: " + str(polarity_total / objective_sentiments_count))
    except TweepError as error:
        print(repr(error))

if __name__ == "__main__":
    main()