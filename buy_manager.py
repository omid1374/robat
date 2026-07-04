"""
buy_manager.py

Buy order manager.
"""

import logging
from typing import Any
from exceptions import TradeExecutionUnknown


logger = logging.getLogger(__name__)


class BuyManager:
    """
    Handles long entry logic.
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
        Execute a buy order if conditions are satisfied.
        """

        try:
            if not signal.get("buy", False):
                return False

            if await self.exchange.has_open_position(symbol):
                logger.info("%s already has an open position.", symbol)
                return False

            if await self.exchange.has_pending_buy_order(symbol):
                logger.info("%s already has a pending buy order.", symbol)
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

            # Validate order before sending it to the exchange
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
            order = await self.exchange.create_limit_order(
                symbol=symbol,
                side="buy",
                amount=order_size,
                price=entry_price,
            )

            logger.info(
                "%s | BUY %.8f @ %.8f",
                symbol,
                order_size,
                entry_price,
            )

            return bool(order)

        except TradeExecutionUnknown:

            logger.warning(
                "%s | Trade status unknown. Verification required.",
                symbol,
            )

            raise

        except Exception:

            logger.exception(
                "Buy manager failed.",
            )

            return False