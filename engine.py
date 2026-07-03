"""
engine.py

Core trading engine.
"""

from __future__ import annotations

import asyncio
import logging
import traceback
from datetime import datetime

from exchange import client
from config import SYMBOLS
from buy_manager import BuyManager
from sell_manager import SellManager
from risk_manager import RiskManager
from telegram_logger import TelegramLogger

logger = logging.getLogger(__name__)


class TradingEngine:

    def __init__(self):

        self.client = client

        self.running = False

        self.buy_manager = BuyManager(
            self.client,
            RiskManager(),
        )

        self.sell_manager = SellManager(
            self.client,
            RiskManager(),
        )

        self.telegram = TelegramLogger()

        self.symbols = SYMBOLS

        self.loop_delay = 2

        self.last_run = None

    async def initialize(self):

        logger.info("=" * 60)
        logger.info("Initializing Trading Engine...")
        logger.info("=" * 60)

        try:

            await self.client.connect()

            logger.info("Exchange Connected.")

            markets = await self.client.load_markets()

            logger.info(
                "%d markets loaded.",
                len(markets),
            )

            self.running = True

            await self.telegram.send(
                "🤖 Trading Engine Started."
            )

        except Exception:

            logger.exception("Initialization failed.")

            raise

    async def run(self):

        logger.info("Engine loop started.")

        while self.running:

            try:

                self.last_run = datetime.utcnow()

                await self.process_all_symbols()

                await asyncio.sleep(
                    self.loop_delay
                )

            except asyncio.CancelledError:

                raise

            except Exception:

                logger.error(traceback.format_exc())

                await asyncio.sleep(5)

    async def process_all_symbols(self):

        tasks = []

        for symbol in self.symbols:

            tasks.append(
                self.process_symbol(symbol)
            )

        await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )
        
from calculate_live_indicators import calculate_live_indicators


    async def process_symbol(self, symbol: str):

        logger.info("------------------------------------------")
        logger.info("Processing %s", symbol)

        try:

            # ---------------------------------
            # Check Exchange Connection
            # ---------------------------------

            if not await self.client.ping():

                logger.warning(
                    "%s : Exchange unavailable.",
                    symbol,
                )

                return

            # ---------------------------------
            # Get Current Position
            # ---------------------------------

            position = await self.client.fetch_position(
                symbol
            )

            # ---------------------------------
            # Get Open Orders
            # ---------------------------------

            open_orders = await self.client.fetch_open_orders(
                symbol
            )

            logger.info(
                "%s | Position=%s | Orders=%d",
                symbol,
                bool(position),
                len(open_orders),
            )

            # ---------------------------------
            # Calculate Indicators
            # ---------------------------------

            signal = await calculate_live_indicators(
                client=self.client,
                symbol=symbol,
            )

            if signal is None:

                logger.warning(
                    "%s : Indicator returned None",
                    symbol,
                )

                return

            # ---------------------------------
            # Risk Validation
            # ---------------------------------

            risk = RiskManager()

            if not risk.can_open_trade():

                logger.info(
                    "%s : Risk manager rejected trade.",
                    symbol,
                )

                return

            # ---------------------------------
            # Existing Position
            # ---------------------------------

            if position:

                logger.info(
                    "%s : Position already exists.",
                    symbol,
                )

                return

            # ---------------------------------
            # BUY Signal
            # ---------------------------------

            if signal.get("buy"):

                logger.info(
                    "%s : BUY signal detected.",
                    symbol,
                )

                await self.buy_manager.execute(
                    symbol=symbol,
                    signal=signal,
                )

                return

            # ---------------------------------
            # SELL Signal
            # ---------------------------------

            if signal.get("sell"):

                logger.info(
                    "%s : SELL signal detected.",
                    symbol,
                )

                await self.sell_manager.execute(
                    symbol=symbol,
                    signal=signal,
                )

                return

            logger.info(
                "%s : No trading signal.",
                symbol,
            )

        except Exception:

            logger.exception(
                "process_symbol() failed for %s",
                symbol,
            )

            await self.telegram.send(
                f"❌ Engine Error ({symbol})"
            )