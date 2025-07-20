# main.py

from datetime import datetime, timedelta
from tweet_utils import post_tweet
import os

STATE_FILE = "last_percentage.txt"

def get_time_until_friday_night():
    now = datetime.now()
    friday_6pm = now + timedelta((4 - now.weekday()) % 7)
    friday_6pm = friday_6pm.replace(hour=18, minute=0, second=0, microsecond=0)
    if now > friday_6pm:
        friday_6pm += timedelta(days=7)
    return friday_6pm - now

def format_countdown_message(time_left, percent_done):
    green_boxes = "🟩" * int(percent_done / 10) + "⬜" * (10 - int(percent_done / 10))
    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return (
        f"{green_boxes} {percent_done:.0f}% complete\n"
        f"⏳ {days}d {hours}h {minutes}m until Friday night! 🎉"
    )

def load_last_percentage():
    if not os.path.exists(STATE_FILE):
        return -10  # Force first tweet at 0%
    with open(STATE_FILE, "r") as file:
        return int(file.read().strip())

def save_last_percentage(percentage):
    with open(STATE_FILE, "w") as file:
        file.write(str(percentage))

def main():
    time_left = get_time_until_friday_night()
    total_minutes = 4 * 24 * 60 + 18 * 60  # Monday 00:00 to Friday 18:00
    minutes_left = time_left.total_seconds() / 60
    percent_done = ((total_minutes - minutes_left) / total_minutes) * 100
    current_rounded = int(percent_done // 10) * 10

    last_posted = load_last_percentage()

    if current_rounded > last_posted:
        save_last_percentage(current_rounded)
        message = format_countdown_message(time_left, current_rounded)
        post_tweet(message)
    else:
        print(f"[INFO] Not time to tweet yet. Current progress: {percent_done:.1f}%")

if __name__ == "__main__":
    main()
