# pip installs (locally): pip install requests pytrends praw python-dotenv
import os, time, json, re, datetime as dt
from collections import Counter
import requests
from pytrends.request import TrendReq
import praw

YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
REDDIT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_UA = os.getenv("REDDIT_USER_AGENT", "baxter-trends/1.0")

OUT_PATH = "seeds.json"
NOW = dt.datetime.utcnow()

def normalize(s):
    s = re.sub(r"[#@]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def yt_trending(region="US", max_items=40):
    # YouTube "mostPopular" chart
    url = ("https://www.googleapis.com/youtube/v3/videos"
           "?part=snippet,statistics&chart=mostPopular"
           f"&regionCode={region}&maxResults=50&key={YOUTUBE_KEY}")
    r = requests.get(url, timeout=20); r.raise_for_status()
    items = r.json().get("items", [])[:max_items]
    seeds = []
    for it in items:
        sn = it["snippet"]
        title = normalize(sn["title"])
        tags = [normalize(t) for t in sn.get("tags", [])][:6] if sn.get("tags") else []
        desc = normalize(sn.get("description",""))[:180]
        seeds.append({"source":"youtube","title":title,"tags":tags,"desc":desc})
    return seeds

def reddit_top_last_day(subs=("funny","contagiouslaughter","MadeMeSmile"), limit=40):
    reddit = praw.Reddit(
        client_id=REDDIT_ID, client_secret=REDDIT_SECRET,
        user_agent=REDDIT_UA
    )
    seeds=[]
    for s in subs:
        for p in reddit.subreddit(s).top(time_filter="day", limit=limit):
            title = normalize(p.title)
            seeds.append({"source":f"r/{s}","title":title,"tags":[], "desc":""})
    return seeds

def google_trends_hot(n=20):
    # lightweight: rising queries for "funny", "prank", "cat" in US
    pytrends = TrendReq(hl="en-US", tz=0)
    topics = []
    for kw in ["funny", "prank", "cat", "office", "elevator"]:
        try:
            pytrends.build_payload([kw], timeframe="now 1-d", geo="US")
            related = pytrends.related_queries()
            rising = related.get(kw, {}).get("rising", None)
            if rising is not None:
                for _, row in rising.head(10).iterrows():
                    topics.append(row["query"])
        except Exception:
            pass
    return [{"source":"google-trends","title":normalize(t), "tags":[], "desc":""} for t in topics[:n]]

def extract_patterns(items):
    hooks = []
    settings = []
    objects = []
    formats = []
    # simple heuristics
    for it in items:
        t = (it["title"] + " " + " ".join(it["tags"])).lower()
        if t.startswith(("pov","first day","when you")) or "pov" in t:
            hooks.append("POV-style cold open")
        if any(w in t for w in ["elevator","subway","office","meeting","boardroom","taxi","bodega"]):
            settings += re.findall(r"(elevator|subway|office|meeting|boardroom|taxi|bodega)", t)
        if any(w in t for w in ["prank","switch","swap","fake","sticker","label"]):
            formats.append("prank / bait-and-switch")
        if any(w in t for w in ["banana","chair","box","sticky note","post-it","coffee"]):
            objects += re.findall(r"(banana|chair|box|sticky note|post-it|coffee)", t)
    top = lambda xs, n=5: [k for k,_ in Counter(xs).most_common(n)]
    return {
        "hooks": top(hooks, 3) or ["POV-style cold open"],
        "settings": top(settings, 5) or ["elevator","office","boardroom","bodega","subway"],
        "objects": top(objects, 5) or ["sticky note","banana","cardboard box","rolling chair","coffee"],
        "formats": top(formats, 3) or ["prank / bait-and-switch"]
    }

def build_seeds():
    pool = []
    if YOUTUBE_KEY:
        pool += yt_trending()
    if REDDIT_ID and REDDIT_SECRET:
        pool += reddit_top_last_day()
    pool += google_trends_hot()
    patterns = extract_patterns(pool)
    # return compact "seeds" for the generator
    return {"generated_at_utc": NOW.isoformat()+"Z", "raw_count": len(pool), "patterns": patterns}

if __name__ == "__main__":
    seeds = build_seeds()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(seeds, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUT_PATH}")
