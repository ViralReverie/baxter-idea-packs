import json, random, datetime, os, pathlib

random.seed()

# ---- Load CAT CANON (unchanged; uses your cat.json) ----
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

# ---- Comedy knobs (no APIs) ----
NYC_SETTINGS = [
  "glass-walled boardroom on a high floor", "Wall Street lobby turnstiles",
  "Midtown elevator", "open-plan office with skyline view",
  "coffee cart on a Manhattan sidewalk", "bodega aisle", "subway car",
  "yellow taxi back seat", "revolving door in a corporate lobby"
]

PROPS = [
  "sticky note", "banana", "rolling chair", "paper airplane", "rubber stamp",
  "cardboard box", "mini whiteboard", "binder clip chain", "desk intercom"
]  # no laser pointer

PRANKS = [
  # harmless, visual pranks that film easily
  ("Decoy Button", "Baxter places a sticky note labeled 'ANY KEY' on a keyboard"),
  ("Chair Swap", "Baxter replaces a squeaky chair with a comically tiny stool"),
  ("Phantom Elevator", "Baxter posts a neat sign: 'Elevator speaks cat only'"),
  ("Meeting Timer", "Baxter sets an oversized sand timer in the boardroom"),
  ("VIP Rope", "Baxter adds a velvet rope around his espresso cup"),
  ("Auto-Approve", "Baxter stamps 'APPROVED' on blank paper, deadpan"),
  ("Door Close", "Baxter sticks a fake 'DOOR CLOSE (faster)' label"),
  ("Reserved Seat", "Baxter marks a chair 'For Baxter Only' with a tidy placard"),
  ("Snack Audit", "Baxter inventories snacks with a tiny clipboard, very serious"),
  ("Ghost Typist", "Baxter sets a fan so papers slide like ‘invisible typing’")
]

COMEDY_DEVICES = [
  "rule-of-three escalation",
  "bait-and-switch twist",
  "callback to an earlier beat",
  "overly literal interpretation",
  "confident misread that becomes right by accident"
]

AUDIO = [
  "room tone; gentle office murmur; one soft comedic sound at the end",
  "no dialogue; intercom ping once for a caption card",
  "ambient city hush; small paw thumps; tiny desk click"
]

CAMERA = [
  "wide establishing → medium → close; quick, readable cuts",
  "locked-off wide; subtle push-in on punchline",
  "handheld, mild jitter; whip-pan to reaction"
]

def tiny_caption(options):
  # brief on-screen text / intercom text (<= 6 words) to keep voice consistent
  return random.choice(options)

CAPTIONS_SETUP = [
  "Quarterly efficiencies", "Operational excellence", "Executive initiative",
  "Q3 morale booster", "Pilot program", "Beta test"
]
CAPTIONS_TWIST = [
  "Approved.", "Request denied.", "Morale: up.", "It worked.", "As planned.", "Budget neutral."
]
CAPTIONS_BUTTON = [
  "Meeting adjourned.", "Carry on.", "Next item.", "Noted.", "We’re done here."
]

def build_idea():
  setting = random.choice(NYC_SETTINGS)
  prank_name, prank_setup = random.choice(PRANKS)
  prop = random.choice(PROPS)
  device = random.choice(COMEDY_DEVICES)
  duration = random.choice([11,12,13,14,15,16,17,18,19,20])

  title = f"Baxter’s {prank_name} — {device.title()}"

  # Beats using setup → escalation 1 → escalation 2 → twist → button
  setup = (
    f"Wide: {setting}. Baxter ({CAT['coat']}, {CAT['accessories']}) prepares a prank: {prank_setup}. "
    f"On-screen caption (intercom ping): “{tiny_caption(CAPTIONS_SETUP)}”."
  )
  esc1 = (
    f"Medium: First pass works mildly: a human hesitates; Baxter performs a {random.choice(CAT['signature_moves'])}. "
    f"Rule-of-three begins with small success."
  )
  esc2 = (
    f"Medium: Second pass escalates: add a {prop} to sell it. Confidence rises; Baxter’s tail flicks once."
  )
  twist = (
    f"Close: Bait-and-switch twist: {random.choice(['the prank backfires elegantly on Baxter', 'an accidental real approval happens', 'the sign becomes true by coincidence', 'security camera pans to reveal Baxter’s tidy toolkit'])}. "
    f"On-screen caption: “{tiny_caption(CAPTIONS_TWIST)}”."
  )
  button = (
    f"Insert: Baxter does a tiny {random.choice(['approving nod','dramatic espresso sip'])}; intercom pings a final card: “{tiny_caption(CAPTIONS_BUTTON)}”."
  )

  beats = [setup, esc1, esc2, twist, button]
  camera = random.choice(CAMERA)
  audio = random.choice(AUDIO)

  # Compose the prompt block Sora likes (concise but specific)
  prompt_for_sora = (
    f"title: {title}\n"
    f"character: {CAT['name']} — {CAT['coat']}, {CAT['eyes']}, {CAT['size']}; accessories: {CAT['accessories']}\n"
    f"personality: {CAT['personality']}; voice: {CAT['voice']} (if any words, use brief on-screen captions/intercom text only)\n"
    f"setup: {setup}\n"
    f"beat_2: {esc1}\n"
    f"beat_3: {esc2}\n"
    f"twist: {twist}\n"
    f"button: {button}\n"
    f"camera: {camera}\n"
    f"audio: {audio}\n"
    f"duration_s: {duration}\n"
    f"aspect_ratio: 16:9\n"
    "Continuity: single cat only; simple readable motion; no tiny text; avoid crowds and brands."
  )

  return {
    "title": title,
    "style": "prank-forward deadpan office comedy",
    "beats": beats,
    "device": device,
    "camera": camera,
    "audio": audio,
    "duration_s": duration,
    "aspect_ratio": "16:9",
    "prompt_for_sora": prompt_for_sora
  }

# ---- Lightweight “funny” scoring to keep better ideas ----
def score_idea(idea):
  s = 0
  text = " ".join(idea["beats"]).lower()
  # clarity: has setup + twist words
  if "setup" in idea["prompt_for_sora"] and "twist" in idea["prompt_for_sora"]:
    s += 2
  # escalation markers
  if "rule-of-three" in text or "escalat" in text:
    s += 2
  # prank presence
  if "prank" in text:
    s += 2
  # brevity of captions (avoid long dialogue)
  captions_ok = all(len(word) <= 12 for word in idea["prompt_for_sora"].split())
  s += 1 if captions_ok else 0
  # NYC flavor
  if any(k in text for k in ["elevator","boardroom","bodega","subway","wall street","midtown"]):
    s += 1
  return s

def dedupe_keep_first(items, key):
  seen = set(); out = []
  for it in items:
    k = it[key].lower().strip()
    if k in seen: continue
    seen.add(k); out.append(it)
  return out

def build_pack(n=80, keep=30):
  pool = [build_idea() for _ in range(n)]
  pool = dedupe_keep_first(pool, "title")
  scored = sorted(pool, key=score_idea, reverse=True)
  return scored[:keep]

def write_pack(ideas, outdir="public"):
  pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
  ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
  json_path = os.path.join(outdir, "latest.json")
  txt_path  = os.path.join(outdir, "latest.txt")
  html_path = os.path.join(outdir, "index.html")

  with open(json_path, "w", encoding="utf-8") as f:
    json.dump(ideas, f, ensure_ascii=False, indent=2)

  # TXT: human-friendly, Sora-ready blocks
  with open(txt_path, "w", encoding="utf-8") as f:
    f.write(f"CAT CANON — {CAT['name']}: {CAT['one_liner']}\n")
    f.write("VOICE: executive silent-film vibe; if any words, use brief on-screen captions/intercom text only.\n\n")
    for i, it in enumerate(ideas, 1):
      f.write(f"#{i} — {it['title']}\n{it['prompt_for_sora']}\n---\n")

  # HTML “Copy Next” page
  html = f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>{CAT['name']} Idea Pack — {ts}</title>
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
<h1>{CAT['name']} Idea Pack — {ts}</h1>
<p class="small">Canon: {CAT['one_liner']}</p>
<p class="small">Voice rule: executive silent-film vibe; any words appear only as very brief on-screen captions/intercom text.</p>
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
  pack = build_pack(n=80, keep=30)
  write_pack(pack)
