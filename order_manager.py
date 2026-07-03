"""
order_manager.py

مدیریت سفارش‌های BloFin
"""

import logging

from exchange import client
from config import (
    SYMBOL,
    BASE_ORDER_SIZE,
)

logger = logging.getLogger(__name__)


class OrderManager:
    def __init__(self):

        self.buy_order_id = None
        self.sell_order_id = None

    # -------------------------
    # دریافت سفارش‌های باز
    # -------------------------

    async def get_open_orders(self):

        return await client.fetch_open_orders(SYMBOL)

    # -------------------------
    # لغو تمام سفارش‌ها
    # -------------------------

    async def cancel_all(self):

        orders = await self.get_open_orders()

        for order in orders:
            try:
                await client.cancel_order(order["id"], SYMBOL)

            except Exception as e:
                logger.error(e)

        self.buy_order_id = None
        self.sell_order_id = None

    # -------------------------
    # لغو سفارش Buy
    # -------------------------

    async def cancel_buy(self):

        orders = await self.get_open_orders()

        for order in orders:
            if order["side"].lower() == "buy":
                try:
                    await client.cancel_order(order["id"], SYMBOL)

                except Exception as e:
                    logger.error(e)

        self.buy_order_id = None

    # -------------------------
    # لغو سفارش Sell
    # -------------------------

    async def cancel_sell(self):

        orders = await self.get_open_orders()

        for order in orders:
            if order["side"].lower() == "sell":
                try:
                    await client.cancel_order(order["id"], SYMBOL)

                except Exception as e:
                    logger.error(e)

        self.sell_order_id = None

    # -------------------------
    # ثبت سفارش Buy
    # -------------------------

    async def place_buy(self, price, amount=BASE_ORDER_SIZE):

        await self.cancel_buy()

        order = await client.create_limit_order(
            symbol=SYMBOL,
            side="buy",
            amount=amount,
            price=price,
            post_only=True,
        )

        self.buy_order_id = order["id"]

        logger.info(f"BUY LIMIT -> {price}")

        return order

    # -------------------------
    # ثبت سفارش Sell
    # -------------------------

    async def place_sell(self, price, amount=BASE_ORDER_SIZE):

        await self.cancel_sell()

        order = await client.create_limit_order(
            symbol=SYMBOL,
            side="sell",
            amount=amount,
            price=price,
            post_only=True,
        )

        self.sell_order_id = order["id"]

        logger.info(f"SELL LIMIT -> {price}")

        return order

    # -------------------------
    # جایگزینی هوشمند Buy
    # -------------------------

    async def replace_buy(self, price, amount=BASE_ORDER_SIZE):

        orders = await self.get_open_orders()

        current = None

        for order in orders:
            if order["side"].lower() == "buy":
                current = order

                break

        if current:
            old_price = float(current["price"])

            if abs(old_price - price) < 1e-10:
                return current

        return await self.place_buy(price, amount)

    # -------------------------
    # جایگزینی هوشمند Sell
    # -------------------------

    async def replace_sell(self, price, amount=BASE_ORDER_SIZE):

        orders = await self.get_open_orders()

        current = None

        for order in orders:
            if order["side"].lower() == "sell":
                current = order

                break

        if current:
            old_price = float(current["price"])

            if abs(old_price - price) < 1e-10:
                return current

        return await self.place_sell(price, amount)

    # -------------------------
    # ثبت همزمان دو سمت بازار
    # -------------------------

    async def quote(
        self,
        bid_price,
        ask_price,
    ):

        await self.replace_buy(bid_price)

        await self.replace_sell(ask_price)


order_manager = OrderManager()
