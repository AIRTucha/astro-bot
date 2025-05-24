# AstroGPT — Telegram (Pseudo)Astrology Bot powered by LLMs ✨

AstroGPT is a learning-scale Telegram bot based LLM reasoning.

Behind the scenes the bot

1. **Parses free-form text** with an LLM (via LangChain) to recognize intent and extract dates, zodiac signs, etc.
2. **Runs actions** such as `get_daily_forecast`, `update_user_data`, or `unsubscribe`.
3. **Generates replies** with short forecasts, situational advice, or astrology jokes.
4. **Stores state** in Postgres so users can pick up the conversation later.

## Tech stack

* Python 
* Telegram Bot API (webhook mode)
* LangChain + OpenAI GPT-4o (can swap to any chat-completion model)
* Postgres + SQLAlchemy + Alembic
* Docker / docker-compose for local dev
* Deployment to GCP Cloud Run

## Get Started

## Telegram Bot Token Setup

To use this code, you need to obtain a Telegram Bot Token. Follow these steps to get your token:

1. Open Telegram and search for the **BotFather**.
2. Start a chat with the BotFather and use the `/start` command.
3. Use the `/newbot` command to create a new bot.
4. Follow the prompts to name your bot and choose a username for it.
5. Once the bot is created, the BotFather will provide you with a **bot token**. This token is required to authenticate your bot with the Telegram API.

**Important:** Keep your bot token secure and do not share it publicly.

Once you have your bot token, you can use it in the code to interact with the Telegram API.

## Run database migrations

 - Ensure you have Python and Alembic installed.
 - Add `DATABASE_URL` to your terminal session or export it as an environment variable:
   ```bash
   export DATABASE_URL=<your_postgres_connection_string>
   ```
 - Verify the connection by running:
   ```bash
   alembic current
   ```
   This should display the current migration state. If it fails, check your `DATABASE_URL` and ensure the Postgres server is running.
 - Run the following command to apply migrations:
   ```bash
   alembic upgrade head
   ```

### Run Locally

1. **Set up environment variables**:
    - Create a file named `dev.env` in the root directory.
    - Add the following variables to `dev.env`:
      ```
      DATABASE_URL=<your_postgres_connection_string>
      TG_BOT_TOKEN=<your_telegram_bot_token>
      OPEN_AI_KEY=<your_openai_api_key>
      ```

2. **Run database migrations**

3. **Start the bot locally**:
    - Use Docker Compose to start the services:
      ```bash
      docker-compose up
      ```

### Deployment to Cloud Run

1. **Set up environment variables**:
    - Create a file named `prod.cloudrun.env.yaml`.
    - Add the following variables to `prod.cloudrun.env.yaml`:
      ```yaml
      DATABASE_URL: <your_postgres_connection_string>
      TG_BOT_TOKEN: <your_telegram_bot_token>
      OPEN_AI_KEY: <your_openai_api_key>
      ```

2. **Run database migrations**

3. **Deploy to Cloud Run**:
    - Use the provided deployment script:
      ```bash
      ./deploy.sh
      ```

### Why this repo?

* Human-like ChatBot conversation UI
* Use LLM-reasoning instead rigid `/commands`.
* Minimal business logic - new skills are just new “actions” plus a prompt tweak.

Pull requests and feedback are welcome. Have fun, and may your planetary transits be favourable! 🪐