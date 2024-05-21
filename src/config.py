import os

from dotenv import load_dotenv

env_name = os.getenv("ENV_NAME")

load_dotenv(dotenv_path=f"{env_name}.env")

tg_bot_token = os.getenv("TG_BOT_TOKEN")

if tg_bot_token is None:
    raise ValueError("TG_BOT_TOKEN is not set")

open_ai_key = os.getenv("OPEN_AI_KEY")

if open_ai_key is None:
    raise ValueError("OPEN_AI_KEY is not set")

database_url = os.getenv("DATABASE_URL")

if database_url is None:
    raise ValueError("DATABASE_URL is not set")
