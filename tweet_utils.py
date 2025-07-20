import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

LAST_PERCENT_FILE = "last_percent.txt"

def get_last_percent():
    if os.path.exists(LAST_PERCENT_FILE):
        with open(LAST_PERCENT_FILE, "r") as f:
            return int(f.read().strip())
    return -1

def save_last_percent(p):
    with open(LAST_PERCENT_FILE, "w") as f:
        f.write(str(p))

def post_tweet(tweet_text):
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        raise ValueError("Twitter API credentials are missing or incomplete.")

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(tweet_text)
    print("✅ Tweet posted successfully!")
