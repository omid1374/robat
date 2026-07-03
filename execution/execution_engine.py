"""
execution_engine.py

Production-grade execution layer.
Handles order safety, retries, validation.
"""

import asyncio
import time


class ExecutionEngine:

    def __init__(self, client):

        self.client = client

        self.max_retries = 3

        self.retry_delay = 1.5

        self.slippage_tolerance = 0.15  # %

    # -----------------------------------------------------
    # MARKET ORDER
    # -----------------------------------------------------

    async def execute_market_order(
        self,
        symbol: str,
        side: str,
        size: float,
    ):

        for attempt in range(self.max_retries):

            try:

                order = await self.client.create_market_order(
                    symbol=symbol,
                    side=side,
                    size=size,
                )

                # verify order
                if await self.verify_order(order):

                    return order

            except Exception as e:

                print(f"Order failed attempt {attempt+1}: {e}")

                await asyncio.sleep(self.retry_delay)

        return None

    # -----------------------------------------------------
    # LIMIT ORDER (SAFE ENTRY)
    # -----------------------------------------------------

    async def execute_limit_order(
        self,
        symbol: str,
        side: str,
        size: float,
        price: float,
    ):

        for attempt in range(self.max_retries):

            try:

                order = await self.client.create_limit_order(
                    symbol=symbol,
                    side=side,
                    size=size,
                    price=price,
                )

                if await self.verify_order(order):

                    return order

            except Exception as e:

                print(f"Limit order failed: {e}")

                await asyncio.sleep(self.retry_delay)

        return None

    # -----------------------------------------------------
    # ORDER VERIFICATION
    # -----------------------------------------------------

    async def verify_order(self, order):

        if not order:

            return False

        order_id = order.get("id")

        await asyncio.sleep(0.5)

        status = await self.client.fetch_order_status(order_id)

        return status in ["filled", "open"]

    # -----------------------------------------------------
    # SAFE PRICE CHECK
    # -----------------------------------------------------

    async def check_slippage(
        self,
        symbol: str,
        expected_price: float,
    ):

        ticker = await self.client.fetch_last_price(symbol)

        diff = abs(ticker - expected_price) / expected_price * 100

        return diff <= self.slippage_tolerance