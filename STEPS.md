# 🚂 STEPS — Get this bot running on Railway in 5 minutes

> **Read this top-to-bottom. Do every step in order. Don't skip.**

---

## ✅ Step 1 — Verify what you extracted

After unzipping, you should see **all of these** at the root of the
extracted folder. If anything is missing, re-extract; the zip is broken on
your end, not the bundle.

```
✓ app/                    ← Python backend code
✓ bot/                    ← Telegram bot handlers
✓ deploy/                 ← deployment docs (reference only)
✓ boot.sh                 ← shell entrypoint
✓ Procfile
✓ nixpacks.toml
✓ railway.json
✓ requirements.txt        ← CRITICAL — Railway crashes if missing
✓ server.py
✓ README.md
✓ STEPS.md                ← (this file)
✓ .gitignore
✓ .env.example
```

> **No `Dockerfile`** — that was removed on purpose. Railway will use
> Nixpacks (defined in `nixpacks.toml`), which is more forgiving.

---

## ✅ Step 2 — Push EVERYTHING to GitHub

Whichever method you use, **upload the entire contents of the extracted
folder** (every file and subfolder above) — not just some of them.

### 🅰️ Method A — Drag-and-drop (easiest)

1. Create a new empty repo on github.com (don't tick "add README")
2. On the empty-repo page → click the link **"uploading an existing file"**
3. Open the extracted folder, **select all 13 items** (`Ctrl+A` / `Cmd+A`)
4. **Drag them all into GitHub's upload box at once**
5. Wait for every upload bar to turn green
6. Commit message: `Initial commit` → **Commit changes**

### 🅱️ Method B — Git CLI

```bash
cd /path/to/extracted/dataline-bot-github
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## ✅ Step 3 — Verify on GitHub

Open your repo's landing page on github.com. You **must** see all 13 items
listed. If you only see e.g. 4 files (Procfile, README.md, etc.), the upload
was partial. **Stop and re-upload the missing files** before continuing —
Railway WILL fail.

The most commonly forgotten items:

- ❗ `requirements.txt` (Railway crashes without it)
- ❗ `app/` folder (the bot needs its imports)
- ❗ `bot/` folder (this IS the bot)
- ❗ `boot.sh` (the entrypoint)

---

## ✅ Step 4 — Deploy on Railway

1. Go to https://railway.app → **New Project** → **Deploy from GitHub repo**
2. Pick the repo you just uploaded
3. **Add a Database:** click **+ New** → **Database** → **MongoDB**
   *(Railway auto-injects `MONGO_URL` into your service — leave that var alone)*
4. Click your bot service → **Variables** → **Raw Editor** → paste:

```env
MODE=bot
BOT_STANDALONE=1
BOT_TOKEN=YOUR-TELEGRAM-BOT-TOKEN-FROM-BOTFATHER
ADMIN_TG_IDS=YOUR-TELEGRAM-USER-ID
DB_NAME=dataline_store
STORM_API_KEY=YOUR-STORM-KEY-OR-LEAVE-BLANK
HANDYAPI_KEY=YOUR-HANDYAPI-KEY-OR-LEAVE-BLANK
```

5. Click **Deploy** (or Railway will start automatically once the build
   finishes).

---

## ✅ Step 5 — Watch the logs

Railway → your service → **Deployments** → click the latest →
**Deploy Logs** tab. You should see:

```
[boot] MODE=bot PORT=... BOT_STANDALONE=1
bot.standalone - INFO - Standalone runtime ready
bot - INFO - Starting DataLine bot — instance=railway bot_id=...
telegram.ext.Application - INFO - Application started
```

Then DM your bot `/start` on Telegram → 🎰 welcome screen → you're live.

---

## 🛠 Troubleshooting

| Error in deploy logs | Fix |
|---|---|
| `failed to compute checksum of "/requirements.txt": not found` | You forgot to upload `requirements.txt`. Add it to the repo. |
| `ModuleNotFoundError: No module named 'app'` | You forgot to upload the `app/` folder. Add it. |
| `ModuleNotFoundError: No module named 'bot'` | You forgot the `bot/` folder. Add it. |
| `pymongo.errors.ServerSelectionTimeoutError` | `MONGO_URL` is missing or wrong. Add Railway MongoDB plugin OR paste your Atlas SRV string. |
| `telegram.error.Conflict: terminated by other getUpdates request` | Two services are using the same `BOT_TOKEN`. Stop one or use a different token. |
| `Chat not found` warnings on startup | An admin in `ADMIN_TG_IDS` hasn't DM'd this bot yet. Send `/start` from that account. |

---

## 🎁 Need help?

Look at `README.md` for a fuller deep-dive, env var reference, and how to
run a backup bot in parallel.
