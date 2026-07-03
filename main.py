"""
main.py

Entry point of the trading bot.
"""

import asyncio
import logging
import signal
import sys
from telegram.bot_controller import BotController
from engine import TradingEngine
from telegram.bot import TelegramBot
from config import TELEGRAM_TOKEN


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class BotApplication:
    def __init__(self):
        self.engine = TradingEngine()

        self.telegram = TelegramBot(TELEGRAM_TOKEN)
        self.tasks = []
        BotController.instance().bind_engine(self.engine)

        self.running = True

    async def start(self):
        logger.info("======================================")
        logger.info("Starting Trading Bot...")
        logger.info("======================================")

        try:
            await self.engine.initialize()
            await self.telegram.start()
            engine_task = asyncio.create_task(self.engine.run())

            self.tasks = [
                engine_task,
            ]

            await asyncio.gather(*self.tasks)

        except asyncio.CancelledError:
            logger.info("Bot cancelled.")

        except Exception:
            logger.exception("Fatal error occurred.")

        finally:
            await self.shutdown()

    async def shutdown(self):
        if not self.running:
            return

        self.running = False

        logger.info("Stopping bot...")

        try:
            await self.telegram.stop()
        except Exception:
            logger.exception("Error stopping Telegram.")

        try:
            await self.engine.shutdown()
        except Exception:
            logger.exception("Error while shutting down.")


async def main():
    app = BotApplication()

    loop = asyncio.get_running_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(app.shutdown()))
        except NotImplementedError:
            pass

    await app.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
