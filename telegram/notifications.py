"""
telegram/notifications.py

Centralized notification service for the trading bot.

All Telegram messages must be sent through this service.
"""

from __future__ import annotations
import asyncio
import logging
from datetime import datetime
from typing import Optional

from telegram import Bot
from telegram.constants import ParseMode

from config import TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Singleton notification service.

    TelegramBot binds the Application.bot once at startup,
    then every module uses this service.
    """

    def __init__(self):

        self.bot: Optional[Bot] = None

        self.chat_id = TELEGRAM_CHAT_ID

        self.enabled = False
        self.queue = asyncio.Queue()

        self.worker_task = None

        self.running = False

    # -------------------------------------------------
    # Initialization
    # -------------------------------------------------

    def bind(self, bot: Bot):
        """
        Bind Application.bot.

        Called once from telegram/bot.py
        """

        self.bot = bot

        self.enabled = True

        logger.info("Notification service initialized.")

    # -------------------------------------------------

    # -------------------------------------------------

    # Worker
    # -------------------------------------------------

    async def start(self):

        if self.running:
            return

        self.running = True

        self.worker_task = asyncio.create_task(self._worker())

        logger.info("Notification worker started.")

    async def stop(self):

        self.running = False

        if self.worker_task:
            self.worker_task.cancel()

            try:
                await self.worker_task

            except asyncio.CancelledError:
                pass

            self.worker_task = None

        logger.info("Notification worker stopped.")

    async def _worker(self):

        while self.running:
            try:
                job = await self.queue.get()

                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=job["text"],
                    parse_mode=job["parse_mode"],
                    disable_notification=job["disable"],
                )

            except asyncio.CancelledError:
                break

            except Exception:
                logger.exception("Notification worker failed.")

        def disable(self):

            self.enabled = False

            logger.warning("Notifications disabled.")

    # -------------------------------------------------

    def enable(self):

        if self.bot:
            self.enabled = True

            logger.info("Notifications enabled.")

    # -------------------------------------------------

    @property
    def is_ready(self):

        return self.enabled and self.bot is not None and self.chat_id is not None

    # -------------------------------------------------
    # Core Send
    # -------------------------------------------------

    async def send(
        self,
        text,
        parse_mode=ParseMode.HTML,
        disable_notification=False,
    ):

        if not self.is_ready:
            return False

        await self.queue.put(
            {
                "text": text,
                "parse_mode": parse_mode,
                "disable": disable_notification,
            }
        )

        return True

    # -------------------------------------------------
    # Formatting Helpers
    # -------------------------------------------------

    @staticmethod
    def line():

        return "────────────────"

    # -------------------------------------------------

    @staticmethod
    def timestamp():

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # -------------------------------------------------

    @staticmethod
    def money(value):

        try:
            return f"{float(value):,.2f}"

        except Exception:
            return str(value)

    # -------------------------------------------------

    @staticmethod
    def percent(value):

        try:
            return f"{float(value):.2f}%"

        except Exception:
            return str(value)

    # -------------------------------------------------

    @staticmethod
    def price(value):

        try:
            return f"{float(value):,.4f}"

        except Exception:
            return str(value)

    # -------------------------------------------------

    @staticmethod
    def quantity(value):

        try:
            return f"{float(value):,.6f}"

        except Exception:
            return str(value)

    # -------------------------------------------------
    # Internal Builder
    # -------------------------------------------------

    def build(
        self,
        title: str,
        body: str,
        icon: str = "ℹ️",
    ) -> str:

        return (
            f"{icon} <b>{title}</b>\n{self.line()}\n{body}\n\n<i>{self.timestamp()}</i>"
        )

    # -------------------------------------------------
    # Singleton
    # -------------------------------------------------
    # -------------------------------------------------
    # Engine Notifications
    # -------------------------------------------------

    async def send_start(self):

        await self.send(
            self.build(
                "Trading Engine Started",
                "Trading engine is now running.",
                "🟢",
            )
        )

    # -------------------------------------------------

    async def send_stop(self):

        await self.send(
            self.build(
                "Trading Engine Stopped",
                "Trading engine has been stopped.",
                "🔴",
            )
        )

    # -------------------------------------------------

    async def send_restart(self):

        await self.send(
            self.build(
                "Trading Engine Restarted",
                "Trading engine restarted successfully.",
                "♻️",
            )
        )

    # -------------------------------------------------

    async def send_status(
        self,
        running: bool,
        symbols: int,
        balance: float | None = None,
    ):

        body = f"Running : {'YES' if running else 'NO'}\nSymbols : {symbols}\n"

        if balance is not None:
            body += f"Balance : {self.money(balance)}"

        await self.send(
            self.build(
                "Engine Status",
                body,
                "📊",
            )
        )

    # -------------------------------------------------
    # Orders
    # -------------------------------------------------

    async def send_buy(
        self,
        symbol,
        price,
        amount,
    ):

        body = (
            f"Symbol : {symbol}\n"
            f"Entry : {self.price(price)}\n"
            f"Amount : {self.quantity(amount)}"
        )

        await self.send(
            self.build(
                "BUY Executed",
                body,
                "🟢",
            )
        )

    # -------------------------------------------------

    async def send_sell(
        self,
        symbol,
        price,
        amount,
    ):

        body = (
            f"Symbol : {symbol}\n"
            f"Entry : {self.price(price)}\n"
            f"Amount : {self.quantity(amount)}"
        )

        await self.send(
            self.build(
                "SELL Executed",
                body,
                "🔴",
            )
        )

    # -------------------------------------------------

    async def send_position_closed(
        self,
        symbol,
        pnl,
    ):

        body = f"Symbol : {symbol}\nPnL : {self.money(pnl)}"

        await self.send(
            self.build(
                "Position Closed",
                body,
                "✅",
            )
        )

    # -------------------------------------------------

    async def send_take_profit(
        self,
        symbol,
        pnl,
    ):

        body = f"Symbol : {symbol}\nProfit : {self.money(pnl)}"

        await self.send(
            self.build(
                "Take Profit Hit",
                body,
                "🎯",
            )
        )

    # -------------------------------------------------

    async def send_stop_loss(
        self,
        symbol,
        pnl,
    ):

        body = f"Symbol : {symbol}\nLoss : {self.money(pnl)}"

        await self.send(
            self.build(
                "Stop Loss Hit",
                body,
                "🛑",
            )
        )

    # -------------------------------------------------
    # Balance
    # -------------------------------------------------

    async def send_balance(
        self,
        balance: dict,
    ):

        body = (
            f"Wallet : {self.money(balance['wallet_balance'])}\n"
            f"Available : {self.money(balance['available_balance'])}\n"
            f"Equity : {self.money(balance['equity'])}\n"
            f"Unrealized : {self.money(balance['unrealized_pnl'])}"
        )

        await self.send(
            self.build(
                "Wallet Balance",
                body,
                "💰",
            )
        )

    # -------------------------------------------------
    # Heartbeat
    # -------------------------------------------------

    async def send_heartbeat(self):

        await self.send(
            self.build(
                "Heartbeat",
                "Trading engine is alive.",
                "💚",
            ),
            disable_notification=True,
        )

    # -------------------------------------------------
    # Warning
    # -------------------------------------------------

    async def send_warning(
        self,
        message: str,
    ):

        await self.send(
            self.build(
                "Warning",
                message,
                "⚠️",
            )
        )

    # -------------------------------------------------
    # Error
    # -------------------------------------------------

    async def send_error(
        self,
        message: str,
    ):

        await self.send(
            self.build(
                "Error",
                message,
                "❌",
            )
        )

    # -------------------------------------------------

    async def send_exception(
        self,
        exc: Exception,
    ):

        body = f"Type : {type(exc).__name__}\nMessage : {exc}"

        await self.send(
            self.build(
                "Unhandled Exception",
                body,
                "💥",
            )
        )


notifications = NotificationService()
