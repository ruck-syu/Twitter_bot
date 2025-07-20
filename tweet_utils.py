# tweet_utils.py

import os
import tweepy

def create_twitter_client():
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    access_token = os.environ.get("ACCESS_TOKEN")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

    # Check for missing credentials
    if not all([api_key, api_secret, access_token, access_token_secret]):
        raise EnvironmentError("One or more Twitter API credentials are missing.")

    # Set up authentication
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    return tweepy.API(auth)

def post_tweet(message):
    client = create_twitter_client()
    client.update_status(status=message)
