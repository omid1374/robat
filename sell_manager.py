"""
sell_manager.py

Sell order manager.
"""

import logging
from typing import Any

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
