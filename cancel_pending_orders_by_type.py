"""
cancel_pending_orders_by_type.py

Cancel pending orders by side and type.
"""

import asyncio
import logging

logger = logging.getLogger(__name__)


async def cancel_pending_orders_by_type(
    exchange,
    symbol: str,
    side: str | None = None,
    order_type: str | None = None,
):
    """
    Cancel pending orders filtered by side and/or order type.

    Parameters
    ----------
    exchange
        Exchange instance.

    symbol
        Trading symbol.

    side
        buy / sell / None

    order_type
        limit / stop / trigger / None

    Returns
    -------
    int
        Number of cancelled orders.
    """

    cancelled = 0

    try:
        orders = await exchange.fetch_open_orders(symbol)

    except Exception as e:
        logger.exception("Unable to fetch open orders: %s", e)

        return cancelled

    for order in orders:
        try:
            if side:
                if order.get("side", "").lower() != side.lower():
                    continue

            if order_type:
                if order.get("type", "").lower() != order_type.lower():
                    continue

            order_id = order["id"]

            await exchange.cancel_order(order_id, symbol)

            cancelled += 1

            logger.info(
                "Cancelled order %s (%s %s)",
                order_id,
                order.get("side"),
                order.get("type"),
            )

            await asyncio.sleep(0.1)

        except Exception as e:
            logger.exception(
                "Failed to cancel order %s : %s",
                order.get("id"),
                e,
            )

    logger.info("%d pending orders cancelled.", cancelled)

    return cancelled
