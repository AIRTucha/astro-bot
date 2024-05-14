from src.start_bot import Bot

# from typing import Union

from fastapi import FastAPI

from contextlib import asynccontextmanager

bot = Bot("7189953918:AAEHKCoCuYW62FLZPt2lC1VqE_h0MaBKCaQ")


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
