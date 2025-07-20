import os
import tweepy
from datetime import datetime, timedelta, timezone

def get_time_left_and_progress():
    now = datetime.now(timezone.utc)

    # Find previous Saturday 00:00 UTC
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    while start.weekday() != 5:
        start -= timedelta(days=1)

    # End is next Friday 18:00 UTC
    end = start + timedelta(days=6, hours=18)

    total_minutes = (end - start).total_seconds() / 60
    minutes_passed = (now - start).total_seconds() / 60

    percent_done = (minutes_passed / total_minutes) * 100
    percent_done = max(0, min(100, percent_done))  # Clamp between 0 and 100

    time_left = end - now
    return time_left, percent_done

def format_countdown_message(time_left, percent_done):
    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes = remainder // 60

    progress_blocks = int(percent_done // 10)
    empty_blocks = 10 - progress_blocks
    bar = "🟩" * progress_blocks + "⬜" * empty_blocks

    return (
        f"Friday is {percent_done:.0f}% closer!\n\n"
        f"{bar}\n"
        f"{days}d {hours}h {minutes}m until Friday night! 🎉\n"
        f"#FridayFeeling #Countdown"
    )

def post_tweet_if_needed(time_left, percent_done):
    tweet = format_countdown_message(time_left, percent_done)

    # Use secrets from environment variables
    api_key = os.environ["API_KEY"]
    api_secret = os.environ["API_SECRET"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        api.update_status(tweet)
        print("Tweet posted successfully!")
    except Exception as e:
        print(f"Error posting tweet: {e}")
