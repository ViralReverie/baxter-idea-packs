
import os, json, re, requests
from collections import Counter
import praw

YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
REDDIT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_UA = os.getenv("REDDIT_USER_AGENT", "baxter-trends/1.0")

def normalize(s):
    import re as _re
    s = _re.sub(r"[#@]", "", s or "")
    s = _re.sub(r"\s+", " ", s).strip()
    return s

def yt_trending(region="US", max_items=30):
    if not YOUTUBE_KEY: return []
    url = ("https://www.googleapis.com/youtube/v3/videos"
           "?part=snippet&chart=mostPopular"
           f"&regionCode={region}&maxResults=50&key={YOUTUBE_KEY}")
    try:
        r = requests.get(url, timeout=20); r.raise_for_status()
        items = r.json().get("items", [])[:max_items]
        out = []
        for it in items:
            sn = it.get("snippet", {})
            out.append({"source":"youtube", "title":normalize(sn.get("title","")), "desc":normalize(sn.get("description",""))[:160]})
        return out
    except Exception:
        return []

def reddit_top_day(subs=("funny","contagiouslaughter","MadeMeSmile"), limit=30):
    if not (REDDIT_ID and REDDIT_SECRET): return []
    try:
        reddit = praw.Reddit(client_id=REDDIT_ID, client_secret=REDDIT_SECRET, user_agent=REDDIT_UA)
        out = []
        for s in subs:
            for p in reddit.subreddit(s).top(time_filter="day", limit=limit):
                out.append({"source":f"r/{s}", "title": normalize(p.title)})
        return out
    except Exception:
        return []

def extract_patterns(items):
    hooks, settings, objects, formats = [], [], [], []
    for it in items:
        t = (it.get("title","") + " " + it.get("desc","")).lower()
        if "pov" in t:
            hooks.append("POV-style cold open")
        if any(w in t for w in ["office","elevator","subway","boardroom","taxi","bodega","lobby","corridor","coffee cart"]):
            import re as _re
            settings += _re.findall(r"(office|elevator|subway|boardroom|taxi|bodega|lobby|corridor|coffee cart)", t)
        if any(w in t for w in ["prank","trick","swap","fake","sticker","duet","reaction","meme"]):
            formats.append("prank / bait-and-switch")
        if any(w in t for w in ["banana","bagel","chair","box","note","coffee","badge","briefcase"]):
            import re as _re
            objects += _re.findall(r"(banana|bagel|chair|box|note|coffee|badge|briefcase)", t)
    top = lambda xs, n=6: [k for k,_ in Counter(xs).most_common(n)]
    return {
        "hooks": top(hooks,3) or ["POV-style cold open"],
        "settings": top(settings,6) or ["office","elevator","subway","boardroom","bodega","taxi"],
        "objects": top(objects,6) or ["banana","chair","box","note","coffee","briefcase"],
        "formats": top(formats,3) or ["prank / bait-and-switch"]
    }

def main():
    pool = []
    pool += yt_trending()
    pool += reddit_top_day()
    patterns = extract_patterns(pool)
    seeds = {"generated_from": len(pool), "patterns": patterns}
    with open("seeds.json","w",encoding="utf-8") as f:
        json.dump(seeds, f, ensure_ascii=False, indent=2)
    print("Wrote seeds.json with", seeds["generated_from"], "items")

if __name__ == "__main__":
    main()
