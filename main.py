from src.start_bot import Bot

from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.config import tg_bot_token

bot = Bot(tg_bot_token)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.start()
    yield
    await bot.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/sent_daily_forecast")
async def send_daily_forecast():
    await bot.send_daily_forecast()
