
import os, sys, requests, praw

ok = True

def has(name):
    v = os.getenv(name)
    print(f"{name}: {'SET' if v else 'MISSING'}")
    return bool(v)

print("Checking required secrets...")
ok &= has("REDDIT_CLIENT_ID")
ok &= has("REDDIT_CLIENT_SECRET")
ok &= has("REDDIT_USER_AGENT")
print("Optional:")
has("YOUTUBE_API_KEY")

if os.getenv("REDDIT_CLIENT_ID") and os.getenv("REDDIT_CLIENT_SECRET") and os.getenv("REDDIT_USER_AGENT"):
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
        )
        it = next(iter(reddit.subreddit("funny").top(time_filter="day", limit=1)), None)
        print("Reddit API test:", "OK" if it else "No items (still OK)")
    except Exception as e:
        ok = False
        print("Reddit API test FAILED:", e)

if os.getenv("YOUTUBE_API_KEY"):
    try:
        url = ("https://www.googleapis.com/youtube/v3/videos"
               "?part=snippet&chart=mostPopular&regionCode=US&maxResults=1&key=" + os.getenv("YOUTUBE_API_KEY"))
        r = requests.get(url, timeout=10)
        print("YouTube API test:", "OK" if r.ok else f"HTTP {r.status_code}")
        if not r.ok:
            ok = False
    except Exception as e:
        ok = False
        print("YouTube API test FAILED:", e)

if not ok:
    print("One or more checks failed. Fix your secrets and rerun.", file=sys.stderr)
    sys.exit(1)
else:
    print("All checks passed.")
