"""
telegram_logger.py

ارسال پیام به تلگرام
"""

import logging
import aiohttp

from config import (
    TELEGRAM_ENABLED,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
)

logger = logging.getLogger(__name__)


class TelegramLogger:
    def __init__(self):

        self.enabled = TELEGRAM_ENABLED and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID

    async def send(self, message):

        if not self.enabled:
            return

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=10,
                ) as response:
                    if response.status != 200:
                        logger.error(f"Telegram Error : {response.status}")

        except Exception as e:
            logger.error(f"Telegram Exception : {e}")

    async def startup(self):

        await self.send("🚀 ربات مارکت میکر BloFin راه‌اندازی شد.")

    async def shutdown(self):

        await self.send("🛑 ربات متوقف شد.")

    async def order_created(
        self,
        side,
        price,
        amount,
    ):

        await self.send(f"📌 {side.upper()} LIMIT\nPrice : {price}\nAmount : {amount}")

    async def position_closed(
        self,
        pnl,
    ):

        await self.send(f"✅ Position Closed\nPnL : {pnl:.2f} USDT")

    async def emergency_stop(
        self,
        pnl,
    ):

        await self.send(f"🚨 Emergency Stop\nPnL : {pnl:.2f} USDT")

    async def cooldown_started(
        self,
        minutes,
    ):

        await self.send(f"⏳ Cooldown Started\n{minutes} Minutes")


telegram = TelegramLogger()
