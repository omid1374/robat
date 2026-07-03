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
            # ---------------------------------
            # Signal Validation
            # ---------------------------------

            if not signal.get("sell", False):
                return False

            # ---------------------------------
            # Existing Position
            # ---------------------------------

            if await self.exchange.has_open_position(symbol):
                logger.info(
                    "%s already has an open position.",
                    symbol,
                )

                return False

            # ---------------------------------
            # Existing Pending Order
            # ---------------------------------

            if await self.exchange.has_pending_sell_order(symbol):
                logger.info(
                    "%s already has a pending sell order.",
                    symbol,
                )

                return False

            order_size = self.risk_manager.calculate_position_size(
                entry_price=signal["entry"],
                stop_loss=signal["stop_loss"],
            )

            if order_size <= 0:
                logger.warning("Calculated order size is zero.")

                return False
            order_size = await self.exchange.amount_to_precision(
                symbol,
                order_size,
            )

            entry_price = await self.exchange.price_to_precision(
                symbol,
                signal["entry"],
            )
            if not await self.exchange.validate_order(
                symbol=symbol,
                amount=order_size,
                price=entry_price,
            ):
                logger.warning(
                    "%s | Order validation failed.",
                    symbol,
                )
                return False
            # ---------------------------------
            # Create Order
            # ---------------------------------

            order = await self.exchange.create_limit_order(
                symbol=symbol,
                side="sell",
                amount=order_size,
                price=entry_price,
            )

            if not order:
                logger.warning("Exchange returned empty order.")

                return False

            logger.info(
                "%s | SELL %.8f @ %.8f",
                symbol,
                order_size,
                entry_price,
            )
            return True

        except Exception:
            logger.exception("Sell manager failed.")

            return False
