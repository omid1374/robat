"""
telegram/bot_controller.py
"""

import logging
from typing import Optional



logger = logging.getLogger(__name__)


class BotController:
    _instance: Optional["BotController"] = None

    @classmethod
    def instance(cls) -> "BotController":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):

        if BotController._instance is not None:
            raise RuntimeError("BotController is a singleton.")

        self.engine = None
        
    def bind_engine(self, engine):

        self.engine = engine
    
    @property
    def is_running(self):

        if self.engine is None:
            return False

        return self.engine.running
        
    @property
    def task_count(self):

        if self.engine is None:
            return 0

        return 1 if self.engine.engine_task else 0

    async def start(self):

        if self.engine.running:
            return

        logger.info("Starting Trading Engine...")

        await self.engine.start()

    async def stop(self):

        if not self.engine.running:
            return

        logger.info("Stopping Trading Engine...")

        await self.engine.stop()

    async def restart(self):

        logger.info("Restarting Trading Engine...")

        await self.stop()
        await self.start()

    async def shutdown(self):

        await self.stop()
