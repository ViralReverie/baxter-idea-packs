# fetch_top10_trending.py
# Creates: public/trending.json and public/trending.html
# Needs: YOUTUBE_API_KEY (required for YouTube section), Reddit secrets optional.

import os, json, datetime as dt, requests, re, pathlib
from typing import List, Dict

YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")

# Optional Reddit (we'll only use it if creds exist)
REDDIT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_UA = os.getenv("REDDIT_USER_AGENT", "baxter-trends/1.0")

OUTDIR = "public"
pathlib.Path(OUTDIR).mkdir(parents=True, exist_ok=True)

def iso_24h_ago():
    t = dt.datetime.utcnow() - dt.timedelta(days=1)
    return t.replace(microsecond=0).isoformat("T") + "Z"

def yt_top10_funny_last24h() -> List[Dict]:
    if not YOUTUBE_KEY:
        return []
    base_search = "https://www.googleapis.com/youtube/v3/search"
    base_videos = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "type": "video",
        "q": "funny OR comedy",
        "order": "viewCount",
        "maxResults": 50,
        "videoDuration": "short",    # < 4 minutes; we’ll still pick the funniest/most-viewed
        "publishedAfter": iso_24h_ago(),
        "regionCode": "US",
        "relevanceLanguage": "en",
        "key": YOUTUBE_KEY
    }
    r = requests.get(base_search, params=params, timeout=20)
    r.raise_for_status()
    items = r.json().get("items", [])
    ids = [it["id"]["videoId"] for it in items if "id" in it and "videoId" in it["id"]]
    if not ids:
        return []
    # Get stats for view counts
    r2 = requests.get(base_videos, params={
        "part": "snippet,contentDetails,statistics",
        "id": ",".join(ids),
        "key": YOUTUBE_KEY
    }, timeout=20)
    r2.raise_for_status()
    vids = []
    for v in r2.json().get("items", []):
        vid = {
            "platform": "youtube",
            "id": v["id"],
            "title": v["snippet"]["title"],
            "channel": v["snippet"]["channelTitle"],
            "views": int(v.get("statistics", {}).get("viewCount", 0)),
            "url": f"https://www.youtube.com/watch?v={v['id']}",
            "thumb": f"https://img.youtube.com/vi/{v['id']}/hqdefault.jpg",
            "publishedAt": v["snippet"].get("publishedAt", "")
        }
        vids.append(vid)
    vids.sort(key=lambda x: x["views"], reverse=True)
    return vids[:10]

def reddit_top_funny_last_day() -> List[Dict]:
    # Lightweight, no PRAW (so it runs even without deps). Uses Reddit JSON.
    # If you have secrets, it’s still fine; this endpoint is public.
    subs = ["funny", "funnyvideos", "ContagiousLaughter", "MadeMeSmile"]
    out = []
    for s in subs:
        url = f"https://www.reddit.com/r/{s}/top.json?t=day&limit=25"
        try:
            r = requests.get(url, headers={"User-Agent": REDDIT_UA}, timeout=15)
            data = r.json().get("data", {}).get("children", [])
            for c in data:
                p = c.get("data", {})
                title = p.get("title", "")
                link = "https://redd.it/" + p.get("id", "")
                # Prefer posts that look like short videos (yt or v.redd.it)
                domain = p.get("domain", "")
                is_videoish = ("youtube" in domain) or ("youtu.be" in domain) or ("v.redd.it" in domain)
                out.append({
                    "platform": "reddit",
                    "subreddit": s,
                    "title": title,
                    "score": p.get("score", 0),
                    "url": link,
                    "domain": domain,
                    "is_video": bool(is_videoish)
                })
        except Exception:
            continue
    # Prioritize items that are likely videos, then by score
    out.sort(key=lambda x: (not x["is_video"], -int(x.get("score", 0))))
    return out[:10]

def write_outputs(data: Dict):
    # JSON
    with open(os.path.join(OUTDIR, "trending.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # HTML
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    yt = data.get("youtube", [])
    rd = data.get("reddit", [])
    def yt_card(v):
        return f"""
        <div class="card">
          <img src="{v['thumb']}" alt="thumb" />
          <div>
            <b>{v['title']}</b><br/>
            <span class="small">Channel: {v.get('channel','?')} • Views: {v.get('views',0):,}</span><br/>
            <a href="{v['url']}" target="_blank">Open video</a>
          </div>
        </div>"""

    def rd_card(p):
        tag = "video-ish" if p["is_video"] else p["domain"]
        return f"""
        <div class="card">
          <div>
            <b>{p['title']}</b><br/>
            <span class="small">r/{p['subreddit']} • Score: {p.get('score',0):,} • {tag}</span><br/>
            <a href="{p['url']}" target="_blank">Open post</a>
          </div>
        </div>"""

    html = f"""<!doctype html><meta charset="utf-8">
<title>Top 10 Funny — Last 24h</title>
<style>
body{{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;max-width:1000px;margin:24px auto;padding:0 16px}}
h1{{margin:0 0 8px}} .small{{color:#555;font-size:13px}}
.grid{{display:grid;grid-template-columns:1fr;gap:12px}}
.card{{display:flex;gap:12px;border:1px solid #ddd;border-radius:12px;padding:12px;align-items:flex-start}}
.card img{{width:160px;height:90px;object-fit:cover;border-radius:8px;border:1px solid #ccc}}
.section{{margin-top:24px}}
</style>
<h1>Top 10 Funny — Last 24h</h1>
<p class="small">Generated: {ts}. YouTube sorted by views; Reddit sorted by “is video” + score.</p>

<div class="section">
  <h2>YouTube (most viewed, short videos, last 24h)</h2>
  <div class="grid">
    {''.join(yt_card(v) for v in yt) if yt else '<p>No YouTube key or no results.</p>'}
  </div>
</div>

<div class="section">
  <h2>Reddit (top today)</h2>
  <div class="grid">
    {''.join(rd_card(p) for p in rd)}
  </div>
</div>

<p class="small">Pick any 1–3 you find funniest and paste their links here. I’ll turn them into 10-second Baxter prompts with one strong gag and Baxter’s end caption.</p>
"""
    with open(os.path.join(OUTDIR, "trending.html"), "w", encoding="utf-8") as f:
        f.write(html)

def main():
    out = {}
    try:
        out["youtube"] = yt_top10_funny_last24h()
    except Exception as e:
        out["youtube"] = []
    try:
        out["reddit"] = reddit_top_funny_last_day()
    except Exception as e:
        out["reddit"] = []
    write_outputs(out)
    print("Wrote public/trending.json and public/trending.html")

if __name__ == "__main__":
    main()
