
# Baxter Simple Pipeline (10s Sora prompts)

**What it does**
- Generates 30 prompts (exactly **10 seconds** each)
- One funny beat per video; Baxter shows a final caption comment
- Optional trend influence from Reddit/YouTube (last 24h)
- Publishes a "Copy Next" page via GitHub Pages

## Quick start
1. Create a GitHub repo and upload these files (keep folder structure).
2. Go to **Settings → Pages → Source = GitHub Actions**.
3. Add secrets (Settings → Secrets and variables → Actions → New repository secret):
   - `REDDIT_CLIENT_ID`
   - `REDDIT_CLIENT_SECRET`
   - `REDDIT_USER_AGENT` (e.g., `baxter-trends/1.0 by u/YourRedditName`)
   - (optional) `YOUTUBE_API_KEY`
4. **Actions tab → Baxter Secrets Check → Run workflow**.
   - If green: your secrets are good.
5. **Actions tab → Baxter Pages Simple → Run workflow**.
6. Open your Pages URL: `https://<you>.github.io/<repo>/`

If secrets are missing or wrong, the pipeline still runs using defaults (no trend influence).

## Change schedule
Edit cron in `.github/workflows/baxter_pages_simple.yml`:
`0 11,23 * * *` = 7am & 7pm ET.
