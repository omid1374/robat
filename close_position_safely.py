"""
close_position_safely.py

Safely closes an opened position.
"""

import asyncio
import logging

logger = logging.getLogger(__name__)


async def close_position_safely(
    exchange,
    symbol: str,
    side: str,
    size: float,
    max_retry: int = 3,
):
    """
    Close a position safely.

    Parameters
    ----------
    exchange
        Exchange instance.
    symbol
        Trading symbol.
    side
        Current position side (buy/sell).
    size
        Position size.
    max_retry
        Number of retries.

    Returns
    -------
    bool
    """

    if size <= 0:
        logger.warning("Position size is zero.")
        return False

    close_side = "sell" if side.lower() == "buy" else "buy"

    for attempt in range(1, max_retry + 1):
        try:
            logger.info(
                "Closing %s position (%s) attempt %d/%d",
                symbol,
                side,
                attempt,
                max_retry,
            )

            result = await exchange.create_market_order(
                symbol=symbol,
                side=close_side,
                size=size,
                reduce_only=True,
            )

            logger.info("Position closed successfully.")

            return result

        except Exception as e:
            logger.exception(
                "Close position failed (%d/%d): %s",
                attempt,
                max_retry,
                e,
            )

            await asyncio.sleep(2)

    logger.error("Unable to close position after retries.")

    return False
