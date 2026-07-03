"""
core/bot_controller.py
"""

import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class BotController:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.is_running = False
        self.main_task: Optional[asyncio.Task] = None

    @property
    def task_count(self):
        if self.main_task and not self.main_task.done():
            return 1
        return 0

    async def start(self):
        """شروع ربات"""

        if self.is_running:
            return

        self.is_running = True

        self.main_task = asyncio.create_task(self._run())

        logger.info("Bot Started")

    async def stop(self):
        """توقف کامل ربات"""

        if not self.is_running:
            return

        self.is_running = False

        if self.main_task:
            self.main_task.cancel()

            try:
                await self.main_task
            except asyncio.CancelledError:
                pass

            self.main_task = None

        logger.info("Bot Stopped")

    async def restart(self):
        """ریستارت کامل"""

        await self.stop()
        await asyncio.sleep(1)
        await self.start()

    async def _run(self):
        """
        حلقه اصلی ربات

        بعداً موتور ترید داخل این تابع قرار می‌گیرد.
        """

        try:
            while self.is_running:
                # بعداً اینجا:
                #
                # await trading_engine.run_cycle()
                #
                # یا:
                # await strategy.execute()

                await asyncio.sleep(1)

        except asyncio.CancelledError:
            logger.info("Main Task Cancelled")

        except Exception as e:
            logger.exception(e)

        finally:
            self.is_running = False
