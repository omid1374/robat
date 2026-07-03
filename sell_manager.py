"""
sell_manager.py

Sell order manager.
"""

import logging
from typing import Any
from calculate_live_indicators import calculate_live_indicators

logger = logging.getLogger(__name__)


class SellManager:
    """
    Handles short entry logic.
    """

    def __init__(self, exchange, risk_manager):
        self.exchange = exchange
        self.risk_manager = risk_manager

    async def execute(
        self,
        symbol: str,
        signal: dict[str, Any],
    ) -> bool:
        """
        Execute a sell order if conditions are satisfied.
        """

        try:
            if not signal.get("sell", False):
                return False

            if await self.exchange.has_open_position(symbol):
                logger.info("%s already has an open position.", symbol)
                return False

            if await self.exchange.has_pending_sell_order(symbol):
                logger.info("%s already has a pending sell order.", symbol)
                return False

            balance = await self.exchange.fetch_balance()

            order_size = self.risk_manager.calculate_position_size(
                balance=balance,
                entry_price=signal["entry"],
                stop_loss=signal["stop_loss"],
            )

            if order_size <= 0:
                logger.warning("Calculated order size is zero.")
                return False

            order = await self.exchange.create_limit_order(
                symbol=symbol,
                side="sell",
                amount=order_size,
                price=signal["entry"],
            )

            logger.info(
                "SELL order created | %s | %.6f @ %.4f",
                symbol,
                order_size,
                signal["entry"],
            )

            return bool(order)

        except Exception:
            logger.exception("Sell manager failed.")
            return False


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
        
async def manage_open_orders(self, symbol: str):
    """
    Manage existing pending orders.
    Cancel expired or invalid orders.
    """

    try:

        orders = await self.client.fetch_open_orders(symbol)

        if not orders:
            return

        logger.info(
            "%s : %d pending orders found.",
            symbol,
            len(orders),
        )

        current_price = await self.client.fetch_last_price(
            symbol
        )

        for order in orders:

            order_id = order.get("id")
            side = order.get("side")
            price = float(order.get("price", 0))

            # فاصله سفارش از قیمت فعلی (درصد)
            distance = abs(
                current_price - price
            ) / current_price * 100

            # اگر سفارش خیلی از بازار فاصله گرفته باشد
            if distance > 2:

                logger.info(
                    "%s : Cancel stale order %s",
                    symbol,
                    order_id,
                )

                await self.client.cancel_order(
                    order_id,
                    symbol,
                )

    except Exception:

        logger.exception(
            "manage_open_orders failed."
        )


async def manage_open_position(self, symbol: str):
    """
    Manage an active position.
    """

    try:

        position = await self.client.fetch_position(
            symbol
        )

        if not position:
            return

        pnl = float(
            position.get("unrealizedPnl", 0)
        )

        logger.info(
            "%s Unrealized PnL : %.4f",
            symbol,
            pnl,
        )

        # مثال ساده:
        # اگر سود از 5 درصد بیشتر شد
        # می‌توان اینجا Trailing Stop فعال کرد.

        if pnl >= 5:

            logger.info(
                "%s Profit reached target.",
                symbol,
            )

            # در آینده:
            # await self.client.move_stop_loss(...)

    except Exception:

        logger.exception(
            "manage_open_position failed."
        )


async def health_check(self):
    """
    Periodic engine health check.
    """

    try:

        balance = await self.client.fetch_balance()

        logger.info(
            "Current Balance : %s",
            balance,
        )

    except Exception:

        logger.exception(
            "Health check failed."
        )


async def heartbeat(self):
    """
    Send heartbeat to telegram.
    """

    try:

        await self.telegram.send(
            "💚 Trading Engine Running..."
        )

    except Exception:

        logger.exception(
            "Heartbeat failed."
        )
        
        
async def shutdown(self):
    """
    Gracefully shutdown the engine.
    """

    logger.info("=" * 60)
    logger.info("Stopping Trading Engine...")
    logger.info("=" * 60)

    self.running = False

    try:

        # Cancel remaining tasks if needed

        await self.telegram.send(
            "🛑 Trading Engine Stopped."
        )

    except Exception:

        logger.exception(
            "Failed sending shutdown notification."
        )

    try:

        await self.client.close()

        logger.info(
            "Exchange connection closed."
        )

    except Exception:

        logger.exception(
            "Failed closing exchange connection."
        )

    logger.info("Engine shutdown complete.")


async def emergency_shutdown(
    self,
    reason: str,
):
    """
    Emergency stop.
    """

    logger.error(
        "Emergency shutdown: %s",
        reason,
    )

    try:

        await self.telegram.send(
            f"🚨 Emergency Stop\n{reason}"
        )

    except Exception:

        pass

    await self.shutdown()


async def get_engine_status(self):
    """
    Return current engine status.
    """

    return {

        "running": self.running,

        "symbols": len(self.symbols),

        "last_run": self.last_run,

        "loop_delay": self.loop_delay,

    }


async def print_status(self):

    status = await self.get_engine_status()

    logger.info("-" * 50)

    logger.info(
        "Running : %s",
        status["running"],
    )

    logger.info(
        "Symbols : %d",
        status["symbols"],
    )

    logger.info(
        "Loop Delay : %ss",
        status["loop_delay"],
    )

    logger.info(
        "Last Run : %s",
        status["last_run"],
    )

    logger.info("-" * 50)


async def reload_config(self):
    """
    Reload runtime configuration.
    """

    logger.info(
        "Reload configuration requested."
    )

    # Future implementation
    return True