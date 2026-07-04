"""
engine.py

FINAL ARCHITECTURE (Multi-Timeframe Based Engine)
"""

from datetime import datetime, timezone
import asyncio
import logging
from position_manager import PositionManager
from indicators_engine.calculate_live_indicators import (
    calculate_live_indicators,
)

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

        self.initialized = False

        self.engine_task = None
        self.initialized = False
        self.last_reset_date = None
        self.loop_delay = 2

        self.risk_manager = RiskManager()

        self.buy_manager = BuyManager(
            self.client,
            self.risk_manager,
        )
        self.position_manager = PositionManager(
            self.client,
            self.risk_manager,
        )
        self.sell_manager = SellManager(
            self.client,
            self.risk_manager,
        )

        # نگهداری Taskهای هر سیکل
        self.symbol_tasks = []

    # --------------------------------------------------
    # Initialize
    # --------------------------------------------------

    async def initialize(self):

        if self.initialized:
            return

        logger.info("Starting Trading Engine...")

        await self.client.connect()

        logger.info("Trading Engine initialized.")

    async def _check_daily_reset(self):
        """
        Reset daily risk statistics once per UTC day.
        """

        today = datetime.now(timezone.utc).date()

        if self.last_reset_date is None:
            self.last_reset_date = today
            return

        if today != self.last_reset_date:
            logger.info("New UTC day detected. Resetting daily risk statistics.")

            self.risk_manager.reset_daily()

            self.last_reset_date = today

    

    # --------------------------------------------------
    # Start / Stop
    # --------------------------------------------------

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
                logger.info("Engine task cancelled.")

            self.engine_task = None

    # --------------------------------------------------
    # Main Loop
    # --------------------------------------------------

    async def run(self):

        logger.info("Engine loop started.")

        while self.running:
            try:
                await self._check_daily_reset()
                await self.process_all_symbols()

                await asyncio.sleep(self.loop_delay)

            except asyncio.CancelledError:
                logger.info("Engine loop cancelled.")

                break

            except Exception:
                logger.exception("Engine loop failed.")

                await asyncio.sleep(3)

    # --------------------------------------------------
    # Process All Symbols
    # --------------------------------------------------

    async def process_all_symbols(self):

        # -----------------------------
        # Update balance ONCE
        # -----------------------------

        try:
            balance = await self.client.fetch_balance()

            balance_value = (
                balance.get("USDT", {}).get("free")
                or balance.get("free", {}).get("USDT")
                or balance.get("USDT", {}).get("total")
                or balance.get("total", {}).get("USDT")
                or balance.get("USDT", {}).get("available")
                or balance.get("available", {}).get("USDT")
            )

            if balance_value is not None:
                self.risk_manager.update_balance(float(balance_value))

        except Exception:
            logger.exception("Failed updating balance.")

        # -----------------------------
        # Process symbols concurrently
        # -----------------------------

        self.symbol_tasks = []

        for symbol in self.symbols:
            self.symbol_tasks.append(asyncio.create_task(self.process_symbol(symbol)))

        await asyncio.gather(
            *self.symbol_tasks,
            return_exceptions=True,
        )

        self.symbol_tasks.clear()

    # --------------------------------------------------
    # Process Symbol
    # --------------------------------------------------

    async def process_symbol(
        self,
        symbol: str,
    ):

        try:
            logger.info(
                "Processing %s",
                symbol,
            )

            signal = await calculate_live_indicators(
                client=self.client,
                symbol=symbol,
            )

            if not signal:
                return

            await self.position_manager.manage(symbol)

            logger.info(
                "%s | BUY=%s SELL=%s CONF=%s",
                symbol,
                signal["buy"],
                signal["sell"],
                signal["confidence"],
            )

            if not signal.get("buy") and not signal.get("sell"):
                logger.debug(
                    "%s | No trading signal",
                    symbol,
                )

                return

            # -------------------------
            # Risk Check
            # -------------------------

            if not self.risk_manager.can_open_trade():
                logger.info(
                    "%s | Risk blocked trade",
                    symbol,
                )

                return

            # -------------------------
            # BUY
            # -------------------------

            if signal.get("buy"):
                await self.buy_manager.execute(
                    symbol=symbol,
                    signal=signal,
                )

                return

            # -------------------------
            # SELL
            # -------------------------

            if signal.get("sell"):
                await self.sell_manager.execute(
                    symbol=symbol,
                    signal=signal,
                )

                return

        except Exception:
            logger.exception(
                "Error processing %s",
                symbol,
            )

    # --------------------------------------------------
    # Shutdown
    # --------------------------------------------------

    async def shutdown(self):

        logger.info("Shutting down Trading Engine...")

        await self.stop()

        try:
            await self.client.close()

        except Exception:
            logger.exception("Failed closing exchange.")

        logger.info("Trading Engine stopped.")
