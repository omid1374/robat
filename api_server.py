"""
api_server.py
"""

from fastapi import FastAPI
import uvicorn

from telegram.balance_service import BalanceService
from telegram.bot_controller import BotController
from exchange import client


app = FastAPI(title="Trading Bot API", version="1.0.0")

balance_service = BalanceService(client)


@app.get("/")
async def home():
    return {"name": "Trading Bot API", "status": "online"}


@app.get("/status")
async def status():

    controller = BotController.instance()

    return {
        "running": controller.is_running,
        "task_count": controller.task_count,
    }


@app.get("/balance")
async def balance():

    return await balance_service.get_balance()


def start_api():

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_level="info",
    )


if __name__ == "__main__":
    start_api()
