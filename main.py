from src.start_bot import Bot

from fastapi import FastAPI, Request

from contextlib import asynccontextmanager

import os

bot = Bot(os.environ["TG_BOT_TOKEN"])


@asynccontextmanager
async def lifespan(_: FastAPI):
    await bot.start()
    yield
    await bot.stop()


app = FastAPI(
    lifespan=lifespan,
)


@app.post("/tg_webhook")
async def process_update(request: Request):
    req = await request.json()
    await bot.process_update(req)


@app.post("/sent_daily_forecast")
async def send_daily_forecast():
    await bot.send_daily_forecast()


@app.post("/ready")
async def ready():
    return {"status": "ready"}


@app.post("/health")
async def health():
    return {"status": "ok"}
