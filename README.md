# AstroGPT — Telegram (Pseudo)Astrology Bot powered by LLMs ✨

AstroGPT is a learning-scale Telegram bot based LLM reasoning.

Behind the scenes the bot

1. **Parses free-form text** with an LLM (via LangChain) to recognize intent and extract dates, zodiac signs, etc.
2. **Runs actions** such as `get_daily_forecast`, `update_user_data`, or `unsubscribe`.
3. **Generates replies** with short forecasts, situational advice, or astrology jokes.
4. **Stores state** in Postgres so users can pick up the conversation later.

### Tech stack

* Python 
* Telegram Bot API (webhook mode)
* LangChain + OpenAI GPT-4o (can swap to any chat-completion model)
* Postgres + SQLAlchemy
* Docker / docker-compose for local dev
* Deployment to GCP Cloud Run

### Why this repo?

* Human-like ChatBot conversation UI
* Use LLM-reasoning instead rigid `/commands`.
* Minimal business logic - new skills are just new “actions” plus a prompt tweak.

Pull requests and feedback are welcome. Have fun, and may your planetary transits be favourable! 🪐