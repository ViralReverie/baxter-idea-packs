import json, random, os, datetime, pathlib

# Load Baxter canon
def load_cat():
    return json.load(open("cat.json", "r", encoding="utf-8"))

CAT = load_cat()

# Try to load trending seeds (optional)
def load_seeds():
    path = "seeds.json"
    if os.path.exists(path):
        try:
            return json.load(open(path, "r", encoding="utf-8"))
        except:
            return None
    return None

SEEDS = load_seeds()
patterns = (SEEDS or {}).get("patterns", {})

# Fallback lists
DEFAULT_SETTINGS = ["office", "elevator", "subway", "taxi", "coffee cart", "boardroom", "lobby", "bodega", "corridor"]
DEFAULT_GAGS = ["sticky note trick", "chair swap", "fake button", "phantom typing", "reserved seat", "auto-approve", "door close", "snack audit"]

def pick_seed_or_default(key, default_list):
    arr = patterns.get(key)
    if arr and random.random() < 0.7:
        return random.choice(arr)
    return random.choice(default_list)

def build_one():
    # always 10s
    duration = 10
    setting = pick_seed_or_default("settings", DEFAULT_SETTINGS)
    gag = pick_seed_or_default("formats", DEFAULT_GAGS)
    # One funny moment is the gag itself
    # Baxter’s comment (caption) after
    comment_captions = ["Noted.", "Understood.", "Meeting adjourned.", "Carry on.", "Proceed."]
    comment = random.choice(comment_captions)

    title = f"Baxter — {gag.title()} in {setting.title()}"

    # Beats:
    # 1) Setup (first ~2s)
    # 2) Gag moment (middle ~6s)
    # 3) Baxter comment (last ~1-2s)
    setup = f"Wide: in a {setting}, Baxter ({CAT['coat']}, tie) prepares a subtle gag."
    gag_beat = f"Medium: the gag — {gag} — surprises someone."
    twist = f"Close: final reaction, Baxter’s comment caption: “{comment}”."

    prompt = f"""title: {title}
character: {CAT['name']} — {CAT['coat']}, {CAT['eyes']}; accessories: {CAT['accessories']}
personality: {CAT['personality']}; voice: executive silent-film (no spoken dialogue)
beats:
  - {setup}
  - {gag_beat}
  - {twist}
camera: wide → medium → close
audio: no dialogue; small cue at gag moment
duration_s: {duration}
aspect_ratio: 16:9
**comment_caption:** {comment}
Continuity: single cat only, simple motion, no tiny text."""
    return {
        "title": title,
        "prompt_for_sora": prompt
    }

def build_pack(n=30):
    return [build_one() for _ in range(n)]

def write_pack(ideas, out="public"):
    pathlib.Path(out).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(out, "latest.json"), "w", encoding="utf-8") as f:
        json.dump(ideas, f, ensure_ascii=False, indent=2)
    with open(os.path.join(out, "latest.txt"), "w", encoding="utf-8") as f:
        for i, it in enumerate(ideas, 1):
            f.write(f"#{i} — {it['title']}\n{it['prompt_for_sora']}\n---\n")
    # simple HTML with Copy Next
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Idea Pack</title></head><body>
<h1>Idea Pack — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</h1>
<p>Click Copy Next, paste into Sora, Generate</p>
<button id="copyBtn">Copy Next</button> <a href="latest.txt">Download TXT</a>
<div id="list"></div>
<script>
let ideas = []; let idx = 0;
async function load() {{
  ideas = await (await fetch('latest.json')).json();
  const list = document.getElementById('list');
  list.innerHTML = ideas.map((it,i)=>`<div><b>#${{i+1}} — ${{it.title}}</b><pre>${{it.prompt_for_sora}}</pre></div>`).join('');
}}
function copyNext() {{
  if (idx>=ideas.length) return;
  navigator.clipboard.writeText(ideas[idx].prompt_for_sora);
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
