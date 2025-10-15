
import json, random, datetime, os, pathlib

random.seed()

def load_cat_canon(path="cat.json"):
  default = {
  "name": "Baxter von Pounce",
  "coat": "plush grey with white muzzle, chest, and paws",
  "eyes": "oversized bright green",
  "size": "small, plush, round-faced",
  "accessories": "navy tie with white diagonal stripes; tiny espresso cup; pen",
  "voice": "executive silent-film vibe (no dialogue; occasional approving hum)",
  "personality": "decisive, mildly smug, caffeine-powered; consummate boardroom boss",
  "signature_moves": [
    "dramatic espresso sip",
    "slow tail flick before a decision",
    "pressing the desk intercom",
    "approving nod"
  ],
  "disallowed": ["more than one cat", "crowded scenes", "tiny unreadable text", "real company logos/brands", "overt politics"],
  "one_liner": "A plush grey-and-white executive cat with huge green eyes and a navy striped tie, ruling a NYC boardroom."
}
  if os.path.exists(path):
    try:
      with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
      default.update({k:v for k,v in data.items() if v})
    except Exception:
      pass
  return default

CAT = load_cat_canon()

STYLES = [
  "deadpan physical comedy", "wholesome cringe", "surreal slice-of-life",
  "awkward domestic humor", "silent physical gag", "mock nature documentary"
]
SETTINGS = [
  "glass-walled boardroom on a high floor", "Wall Street lobby turnstiles",
  "Midtown elevator", "open-plan office with skyline view",
  "coffee cart on a Manhattan sidewalk", "bodega aisle", "subway car",
  "yellow taxi back seat", "revolving door in a corporate lobby"
]
OBJECTS = ["banana", "sticky note", "umbrella", "rolling chair", "water bottle",
           "paper airplane", "backpack", "mop", "cardboard box"]
MOTIFS = ["unexpected echo", "polite escalation", "mistimed wave", "synchronized oops",
          "fake-out ending", "overly literal sign", "slow-burn stare", "prop betrayal"]
CAMERA = [
  "wide establishing → medium → close; quick cuts",
  "locked-off wide shot; subtle push-in on punchline",
  "handheld, mild jitter; whip-pan to reaction"
]
AUDIO = [
  "room tone; clothes rustle; one soft comedic sound at the end",
  "no dialogue; single chime on punchline",
  "ambient office murmur; tiny paw sounds; elevator ding"
]

CONTINUITY_RULES = (
  f"Continuity: single cat only ({CAT['name']}); on-model appearance at all times — {CAT['coat']}, "
  f"{CAT['eyes']}, {CAT['size']}, accessories: {CAT['accessories']}. Maintain {CAT['voice']}; "
  f"preferred actions include {', '.join(CAT['signature_moves'])}. Avoid: {', '.join(CAT['disallowed'])}. "
  "≤2 human extras if needed; simple, readable motion; no tiny text; avoid crowds and complex staging."
)

def make_idea():
  style = random.choice(STYLES)
  setting = random.choice(SETTINGS)
  obj = random.choice(OBJECTS)
  motif = random.choice(MOTIFS)
  duration = random.choice([10,11,12,13,14,15,16,17,18,19,20])

  title = f"{CAT['name']} vs. the {setting.title()} {motif.title()}"
  beats = [
    f"Wide: in a {setting}, {CAT['name']} ({CAT['coat']}, {CAT['accessories']}) notices a {obj}.",
    f"Medium: escalation built on {motif}; {CAT['name']} uses a signature move.",
    "Close: deadpan punchline; 0.5s hold; cut."
  ]
  camera = random.choice(CAMERA)
  audio = random.choice(AUDIO)
  prompt_for_sora = (
    f"title: {title}\n"
    f"character: {CAT['name']} — {CAT['coat']}, {CAT['eyes']}, {CAT['size']}; accessories: {CAT['accessories']}\n"
    f"personality: {CAT['personality']}; voice: {CAT['voice']}\n"
    f"beats: {beats[0]} | {beats[1]} | {beats[2]}\n"
    f"camera: {camera}\n"
    f"audio: {audio}\n"
    f"duration_s: {duration}\n"
    f"aspect_ratio: 16:9\n"
    f"{CONTINUITY_RULES}\n"
    "Rules: clear silhouette; readable action; avoid tiny text; simple background."
  )

  return {
    "title": title,
    "style": style,
    "beats": beats,
    "camera": camera,
    "audio": audio,
    "duration_s": duration,
    "aspect_ratio": "16:9",
    "prompt_for_sora": prompt_for_sora
  }

def dedupe_keep_first(items, key):
  seen = set(); out = []
  for it in items:
    k = it[key].lower().strip()
    if k in seen: continue
    seen.add(k); out.append(it)
  return out

def build_pack(n=60, keep=30):
  ideas = [make_idea() for _ in range(n)]
  ideas = dedupe_keep_first(ideas, "title")[:keep]
  return ideas

def write_pack(ideas, outdir="public"):
  pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
  ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
  json_path = os.path.join(outdir, "latest.json")
  txt_path  = os.path.join(outdir, "latest.txt")
  html_path = os.path.join(outdir, "index.html")

  with open(json_path, "w", encoding="utf-8") as f:
    json.dump(ideas, f, ensure_ascii=False, indent=2)

  with open(txt_path, "w", encoding="utf-8") as f:
    f.write(f"CAT CANON — {CAT['name']}: {CAT['one_liner']}\n")
    f.write(CONTINUITY_RULES + "\n\n")
    for i, it in enumerate(ideas, 1):
      f.write(f"#{i} — {it['title']}\n{it['prompt_for_sora']}\n---\n")

  html = f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>{'{'}CAT['name']{'}'} Idea Pack — {ts}</title>
<style>
body{{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;max-width:900px;margin:24px auto;padding:0 16px}}
.card{{border:1px solid #ddd;border-radius:12px;padding:16px;margin:12px 0}}
button{{padding:8px 12px;border-radius:10px;border:1px solid #ccc;cursor:pointer}}
#counter{{font-weight:600}}
.small{{color:#444;font-size:13px}}
pre{{white-space:pre-wrap}}
</style>
</head>
<body>
<h1>{'{'}CAT['name']{'}'} Idea Pack — {ts}</h1>
<p class="small">Canon: {'{'}CAT['one_liner']{'}'}</p>
<p class="small">{'{'}CONTINUITY_RULES{'}'}</p>
<p>Click <b>Copy Next</b>, then paste into Sora and hit Generate. Repeat.</p>
<p>Remaining: <span id="counter"></span></p>
<div id="controls" class="card">
  <button id="copyBtn">Copy Next</button>
  <a href="latest.txt" download style="margin-left:8px">Download .txt</a>
</div>
<div id="list"></div>
<script>
let ideas = []; let idx = 0;
async function load() {{
  const r = await fetch('latest.json'); ideas = await r.json();
  idx = 0; updateCounter();
  const list = document.getElementById('list');
  list.innerHTML = ideas.map((it,i)=>`<div class="card"><b>#${{i+1}} — ${{it.title}}</b><pre>${{it.prompt_for_sora}}</pre></div>`).join('');
}}
function updateCounter() {{ document.getElementById('counter').textContent = (ideas.length - idx); }}
async function copyNext() {{
  if (idx >= ideas.length) return;
  await navigator.clipboard.writeText(ideas[idx].prompt_for_sora);
  idx++; updateCounter();
}}
document.getElementById('copyBtn').addEventListener('click', copyNext);
load();
</script>
</body></html>"""
  with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

if __name__ == "__main__":
  pack = build_pack(n=60, keep=30)
  write_pack(pack)
