
# Baxter von Pounce — Idea Packs (Free)

This repo builds **twice-daily** packs of 30 Sora-ready prompts about your CEO cat, **Baxter von Pounce**.

## Files
- `cat.json` — Baxter's canon (appearance, vibe). Edit anytime.
- `generate_prompts.py` — Free, template-based idea generator (no API keys).
- `.github/workflows/schedule.yml` — GitHub Actions workflow (cron + Pages deploy).
- `public/index.html` — "Copy Next" page (auto-generated).
- `public/latest.json` / `public/latest.txt` — Current pack (auto-generated).

## How it works
The workflow runs at **7am & 7pm ET** (11:00 & 23:00 UTC), generates 30 prompts, and publishes them to GitHub Pages.

## Local run
```
python generate_prompts.py
```

Then open `public/index.html` in a browser.
