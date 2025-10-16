
import json, random, os, datetime, pathlib

def load_cat():
    return json.load(open("cat.json", "r", encoding="utf-8"))

CAT = load_cat()

def load_seeds():
    path = "seeds.json"
    if os.path.exists(path):
        try:
            return json.load(open(path, "r", encoding="utf-8"))
        except Exception:
            return None
    return None

SEEDS = load_seeds()
patterns = (SEEDS or {}).get("patterns", {})

DEFAULT_SETTINGS = ["office", "elevator", "subway", "taxi", "coffee cart", "boardroom", "lobby", "bodega", "corridor"]
DEFAULT_GAGS = ["sticky note trick", "chair swap", "fake button", "phantom typing", "reserved seat", "auto-approve", "door close", "snack audit"]

def pick_seed_or_default(key, default_list, weight=0.7):
    arr = patterns.get(key)
    if arr and random.random() < weight:
        return random.choice(arr)
    return random.choice(default_list)

def build_one():
    duration = 10
    setting = pick_seed_or_default("settings", DEFAULT_SETTINGS, 0.85)
    gag = pick_seed_or_default("formats", DEFAULT_GAGS, 0.85)

    comment_captions = ["Noted.", "Understood.", "Meeting adjourned.", "Carry on.", "Proceed."]
    comment = random.choice(comment_captions)

    title = f"Baxter — {gag.title()} in {setting.title()}"

    setup = f"Wide: in a {setting}, Baxter ({CAT['coat']}, tie) prepares a subtle gag."
    gag_beat = f"Medium: the gag — {gag} — hits (one funny beat, readable and visual)."
    twist = f"Close: Baxter does a tiny {random.choice(['approving nod','dramatic espresso sip'])}; caption card: “{comment}”."

    prompt = f"""title: {title}
character: {CAT['name']} — {CAT['coat']}, {CAT['eyes']}; accessories: {CAT['accessories']}
personality: {CAT['personality']}; voice: executive silent-film (no spoken dialogue; use brief on-screen captions)
beats:
  - {setup}
  - {gag_beat}
  - {twist}
camera: wide → medium → close
audio: no dialogue; small cue at gag moment
duration_s: {duration}
aspect_ratio: 16:9
Continuity: single cat only, simple motion, no tiny text, avoid crowds/brands.
"""
    return {"title": title, "prompt_for_sora": prompt, "trend_note": {
        "used_seeds": bool(SEEDS),
        "setting_pool": patterns.get("settings", []),
        "format_pool": patterns.get("formats", [])
    }}

def build_pack(n=30):
    return [build_one() for _ in range(n)]

def write_pack(ideas, out="public"):
    pathlib.Path(out).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(out, "latest.json"), "w", encoding="utf-8") as f:
        json.dump(ideas, f, ensure_ascii=False, indent=2)
    with open(os.path.join(out, "latest.txt"), "w", encoding="utf-8") as f:
        for i, it in enumerate(ideas, 1):
            f.write(f"#{i} — {it['title']}\n{it['prompt_for_sora']}\n---\n")
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Idea Pack — {now}</title>
<style>body{{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;max-width:900px;margin:24px auto;padding:0 16px}}
.card{{border:1px solid #ddd;border-radius:12px;padding:16px;margin:12px 0}}button{{padding:8px 12px;border-radius:10px;border:1px solid #ccc;cursor:pointer}}</style>
</head><body>
<h1>Idea Pack — {now}</h1>
<p><b>Rules:</b> 10s total • one funny beat • Baxter caption at the end • same voice always.</p>
<p><button id="copyBtn">Copy Next</button> <a href="latest.txt" download>Download TXT</a></p>
<p id="trendInfo"></p>
<div id="list"></div>
<script>
let ideas=[], idx=0;
async function load(){{
  ideas = await (await fetch('latest.json')).json();
  const info = ideas[0]?.trend_note;
  document.getElementById('trendInfo').textContent = info && info.used_seeds ? 
    ('Trending influence ON — settings: '+(info.setting_pool||[]).join(', ')+' | formats: '+(info.format_pool||[]).join(', ')) :
    'Trending influence OFF (falling back to defaults).';
  document.getElementById('list').innerHTML = ideas.map((it,i)=>`<div class="card"><b>#${{i+1}} — ${{it.title}}</b><pre>${{it.prompt_for_sora}}</pre></div>`).join('');
}}
async function copyNext(){{
  if (idx>=ideas.length) return;
  await navigator.clipboard.writeText(ideas[idx].prompt_for_sora);
  idx++;
}}
document.getElementById('copyBtn').onclick = copyNext;
load();
</script></body></html>"""
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    ideas = build_pack(30)
    write_pack(ideas)
