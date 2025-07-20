from datetime import datetime, timedelta
from tweet_utils import post_tweet, get_last_percent, save_last_percent

def get_time_until_friday_night():
    now = datetime.now()
    # Target: Friday 6:00 PM
    weekday = now.weekday()
    days_until_friday = (4 - weekday) % 7
    target = (now + timedelta(days=days_until_friday)).replace(hour=18, minute=0, second=0, microsecond=0)
    if weekday > 4 or (weekday == 4 and now.hour >= 18):
        # After Friday 6PM, target next week's Friday
        target += timedelta(days=7)
    return target - now

def format_countdown_message(time_left, percent_done):
    days = time_left.days
    hours, rem = divmod(time_left.seconds, 3600)
    minutes = rem // 60

    # Green box progress bar
    blocks = 10
    filled = int((percent_done / 100) * blocks)
    progress_bar = "🟩" * filled + "⬜" * (blocks - filled)

    return (
        f"{days}d {hours}h {minutes}m until Friday night! 🎉\n"
        f"{progress_bar} {percent_done:.1f}%\n"
        f"Friday is {percent_done:.1f}% closer! #FridayFeeling"
    )

def main():
    time_left = get_time_until_friday_night()
    total_minutes = (4 * 24 + 18) * 60  # 4140 minutes from Sat 00:00 to Fri 18:00
    minutes_left = time_left.total_seconds() / 60
    minutes_passed = max(0, total_minutes - minutes_left)

    percent_done = round((minutes_passed / total_minutes) * 100, 1)
    current_percent = int(percent_done)
    last_percent = get_last_percent()

    if current_percent % 10 == 0 and current_percent != last_percent:
        tweet = format_countdown_message(time_left, percent_done)
        post_tweet(tweet)
        save_last_percent(current_percent)
    else:
        print(f"Current: {current_percent}%, Last posted: {last_percent}%. No tweet posted.")

if __name__ == "__main__":
    main()
