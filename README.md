# 🎰 DataLine Bot — Standalone

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template?template=https://github.com/YOUR_USERNAME/YOUR_REPO&envs=BOT_TOKEN,ADMIN_TG_IDS,MONGO_URL,DB_NAME&optionalEnvs=STORM_API_KEY,HANDYAPI_KEY,USDT_TRC20_WALLET,LTC_WALLET)

Production-grade Telegram CVV store bot, designed to run as a single Railway
service (or any Docker / Nixpacks host). Standalone mode means the bot talks
to MongoDB directly — no separate API server, no orchestrator, zero glue.

---

## 🚀 Deploy to Railway in 90 seconds

### Option 1 — One-click template button

1. **Click the "Deploy on Railway" badge above.** (Edit the button URL in this
   file first to point at *your* GitHub repo — see the final section below.)
2. Railway prompts you for the required env vars:
   - `BOT_TOKEN` (from [@BotFather](https://t.me/BotFather))
   - `ADMIN_TG_IDS` (your Telegram user ID — DM [@userinfobot](https://t.me/userinfobot) to find it)
   - `MONGO_URL` (Atlas SRV string — [free M0 cluster](https://www.mongodb.com/cloud/atlas/register))
   - `DB_NAME` (e.g. `dataline_store`)
3. Click **Deploy.** Railway builds with Nixpacks, runs `boot.sh`, bot starts
   polling Telegram within ~60 s.

### Option 2 — Connect GitHub repo manually

1. **Fork / push** this repo to your GitHub.
2. Railway → **New Project** → **Deploy from GitHub repo** → pick yours.
3. Add a **MongoDB** plugin (or paste your Atlas URI as `MONGO_URL`).
4. In **Variables**, open the **Raw Editor** and paste:

   ```env
   MODE=bot
   BOT_STANDALONE=1

   BOT_TOKEN=123456789:AA-your-token-from-botfather
   ADMIN_TG_IDS=8295276273
   MONGO_URL=mongodb+srv://USER:PASS@cluster0.xxx.mongodb.net
   DB_NAME=dataline_store

   # Optional — unlocks the full feature set
   STORM_API_KEY=
   HANDYAPI_KEY=
   USDT_TRC20_WALLET=TCGjtfZnsWt3JDccm3Y1uk2QvLmvM3Yt2x
   LTC_WALLET=Lak56Y1JhwiW26YwcnXdgMSEMDjSUgp7PB
   ```

5. Hit **Deploy**. Done.

---

## 🧪 Verify it's working

Check the **Deploy logs** in Railway — you should see:

```
[boot] MODE=bot PORT=8001 BOT_STANDALONE=1
bot.standalone - INFO - Standalone runtime ready
bot - INFO - Starting DataLine bot — instance=railway bot_id=123456789
telegram.ext.Application - INFO - Application started
```

Send `/start` to your bot on Telegram. You should see the welcome card with your
username, user ID, and balance. That's it — you're live. 🎉

---

## 📦 What's in this repo

```
├── app/              # shared backend code (DB, models, parser, refund, watchers)
├── bot/              # Telegram bot handlers
├── deploy/           # extra deployment docs
├── boot.sh           # unified entrypoint — picks role from MODE env var
├── server.py         # FastAPI entry (only used if MODE=web/both)
├── requirements.txt
├── railway.json      # Railway build + start config
├── nixpacks.toml     # Railway / Nixpacks build phases
├── Dockerfile        # for Docker-based hosts
├── Procfile          # for Heroku-style hosts
├── .env.example      # the full list of env vars you need
└── .gitignore
```

You don't need to touch any of it — `boot.sh` handles everything based on the
`MODE` environment variable.

---

## 🌐 Running a second bot token for redundancy

Telegram lets a single person run multiple bots. For a hot-backup deployment:

1. Create a **second bot** with @BotFather → copy its token.
2. Create a **second Railway service** in the same project using this exact repo.
3. In the new service's **Variables**, paste the **same** env vars *except*:
   ```env
   BOT_TOKEN=<your-second-bot-token-here>
   BOT_INSTANCE_LABEL=backup
   ```
4. Both services share the same MongoDB → same users, balances, stock, orders.
   Whichever bot your user DMs, the response is consistent.

If one token gets banned, or Railway auto-scales one service down for any
reason, your customers are still served by the other.

---

## 🖥 Running locally (dev / test)

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# 2. Python 3.10+
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# edit .env — paste your BOT_TOKEN, ADMIN_TG_IDS, MONGO_URL

# 4. Run
sh boot.sh                         # or: MODE=bot python -m bot.bot
```

Stop with **Ctrl+C**. Relaunching picks up any code edits instantly.

---

## 🔧 Editing the bot & API keys later

All external config is in **environment variables** — you never edit source
code to rotate secrets. On Railway, change them in the **Variables** tab and
the service auto-redeploys. Locally, edit `.env` and restart `boot.sh`.

The actual bot source lives in **`bot/bot.py`**. To customise:

- Welcome text: admin panel `/start` → 👑 Admin Panel → Edit Welcome
  *(or edit `WELCOME_TEMPLATE` in `bot/bot.py` for the code default)*
- Add/remove features: modify handlers in `bot/bot.py`
- Parse different upload formats: edit `app/parser.py`
- Swap checker API: edit `app/refund.py`

---

## 🛠 Troubleshooting

| Symptom | Fix |
|---|---|
| `telegram.error.Conflict: terminated by other getUpdates request` | Another process is polling the same token. Stop all but one, or use a separate token for each. |
| `Chat not found` warnings at startup | An admin in `ADMIN_TG_IDS` hasn't DM'd the bot yet. Send `/start` from that account once. |
| Blockcypher 429 rate-limit warnings | Free tier limit. LTC auto-credit may be delayed. Upgrade Blockcypher or set a longer `POLL_INTERVAL_S`. |
| Bot starts but no reply to `/start` | Verify `BOT_TOKEN` matches the actual bot you're DM'ing. Check Railway logs for errors. |
| `ModuleNotFoundError: bot` | Make sure Railway's build succeeded — `pip install -r requirements.txt` should complete without errors. |

---

## 📬 Updating the deploy-button link

**Before you push this repo** to GitHub, edit this file's deploy-button URL
(top of the file). Replace:

```
https://github.com/YOUR_USERNAME/YOUR_REPO
```

…with your actual repo's HTTPS URL, e.g.:

```
https://github.com/alice/dataline-bot
```

After that single edit, the Railway deploy button on your repo's landing page
becomes a literal 1-click deploy for anyone who visits.

---

## 📝 License

Use this at your own risk. No warranty expressed or implied.
