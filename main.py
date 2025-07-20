from datetime import timedelta
from tweet_utils import get_time_left_and_progress, post_tweet_if_needed

# Track last posted percent to avoid duplicate tweets
LAST_POSTED_FILE = "last_posted.txt"

def read_last_posted():
    try:
        with open(LAST_POSTED_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return -1

def write_last_posted(percent):
    with open(LAST_POSTED_FILE, "w") as f:
        f.write(str(percent))

def main():
    time_left, percent_done = get_time_left_and_progress()
    rounded = int(percent_done // 10) * 10

    last_posted = read_last_posted()
    if rounded != last_posted and rounded % 10 == 0:
        print(f"Tweeting at {rounded}% progress")
        post_tweet_if_needed(time_left, percent_done)
        write_last_posted(rounded)
    else:
        print(f"Not time to tweet yet. Current progress: {percent_done:.1f}%")

if __name__ == "__main__":
    main()
