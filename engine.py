"""
engine.py

FINAL ARCHITECTURE (Multi-Timeframe Based Engine)
"""

import asyncio
import logging
from datetime import datetime

from indicators_engine.calculate_live_indicators import calculate_live_indicators

from buy_manager import BuyManager
from sell_manager import SellManager
from risk_manager import RiskManager

from exchange import client
from config import SYMBOLS


logger = logging.getLogger(__name__)


class TradingEngine:
    def __init__(self):

        self.client = client

        self.symbols = SYMBOLS

        self.running = False

        self.risk_manager = RiskManager()

        self.buy_manager = BuyManager(self.client, self.risk_manager)

        self.sell_manager = SellManager(self.client, self.risk_manager)

        self.loop_delay = 2

        self.engine_task = None

        self.initialized = False

    # -----------------------------------------------------
    # INIT
    # -----------------------------------------------------

    async def initialize(self):

        if self.initialized:
            return

        logger.info("Starting Engine...")

        await self.client.connect()
        await self.client.load_markets()

        self.initialized = True

        logger.info("Engine initialized successfully.")

    # -----------------------------------------------------
    # MAIN LOOP
    # -----------------------------------------------------

    async def start(self):

        if self.running:
            return

        await self.initialize()

        self.running = True

        self.engine_task = asyncio.create_task(self.run())

    async def stop(self):

        self.running = False

        if self.engine_task:
            self.engine_task.cancel()

            try:
                await self.engine_task
            except asyncio.CancelledError:
                pass

            self.engine_task = None

    async def run(self):

        logger.info("Engine loop started.")

        while self.running:
            try:
                await self.process_all_symbols()

                await asyncio.sleep(self.loop_delay)

            except Exception as e:
                logger.exception(f"Engine loop error: {e}")

                await asyncio.sleep(3)

    # -----------------------------------------------------
    # PROCESS ALL SYMBOLS
    # -----------------------------------------------------

    async def process_all_symbols(self):

        tasks = []

        for symbol in self.symbols:
            tasks.append(self.process_symbol(symbol))

        await asyncio.gather(*tasks, return_exceptions=True)

    # -----------------------------------------------------
    # PROCESS SINGLE SYMBOL
    # -----------------------------------------------------

    async def process_symbol(self, symbol: str):

        try:
            logger.info(f"Processing {symbol}")

            # 1. GET SIGNAL FROM MTF ENGINE
            signal = await calculate_live_indicators(
                client=self.client,
                symbol=symbol,
            )

            if not signal:
                return

            logger.info(
                f"{symbol} | Signal: "
                f"BUY={signal['buy']} "
                f"SELL={signal['sell']} "
                f"CONF={signal['confidence']}"
            )

            # 2. RISK CHECK
            if not self.risk_manager.can_open_trade():
                logger.info(f"{symbol} | Risk blocked trade")

                return

            # 3. BUY LOGIC
            if signal["buy"]:
                await self.buy_manager.execute(
                    symbol=symbol,
                    signal=signal,
                )

                return

            # 4. SELL LOGIC
            if signal["sell"]:
                await self.sell_manager.execute(
                    symbol=symbol,
                    signal=signal,
                )

                return

        except Exception as e:
            logger.exception(f"Error processing {symbol}: {e}")

    # -----------------------------------------------------
    # SHUTDOWN
    # -----------------------------------------------------

    async def shutdown(self):

        logger.info("Shutting down engine...")

        self.running = False

        try:
            await self.client.close()

        except Exception:
            pass

        logger.info("Engine stopped.")
