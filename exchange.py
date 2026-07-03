import aiohttp
import ccxt.pro as ccxt

from config import (
    API_KEY,
    API_SECRET,
    API_PASSWORD,
    DEFAULT_TYPE,
    ENABLE_RATE_LIMIT,
    VERIFY_SSL,
    USE_IPV4,
)


class BloFinClient:
    def __init__(self):
        self.exchange = None

    async def connect(self):
        """
        ایجاد اتصال به صرافی
        """

        connector = aiohttp.TCPConnector(
            family=4 if USE_IPV4 else 0,
            resolver=aiohttp.ThreadedResolver(),
            verify_ssl=VERIFY_SSL,
        )

        self.exchange = ccxt.blofin(
            {
                "apiKey": API_KEY,
                "secret": API_SECRET,
                "password": API_PASSWORD,
                "enableRateLimit": ENABLE_RATE_LIMIT,
                "aiohttp_trust_env": False,
                "connector": connector,
                "options": {
                    "defaultType": DEFAULT_TYPE,
                },
            }
        )

        await self.exchange.load_markets()

        return self.exchange

    async def close(self):
        if self.exchange is not None:
            await self.exchange.close()

    async def fetch_balance(self):
        return await self.exchange.fetch_balance()

    async def fetch_positions(self, symbol):
        return await self.exchange.fetch_positions([symbol])

    async def fetch_open_orders(self, symbol):
        return await self.exchange.fetch_open_orders(symbol)

    async def cancel_order(self, order_id, symbol):
        return await self.exchange.cancel_order(order_id, symbol)

    async def cancel_all_orders(self, symbol):
        """
        حذف تمام سفارش‌های باز
        """

        orders = await self.fetch_open_orders(symbol)

        for order in orders:
            try:
                await self.cancel_order(order["id"], symbol)
            except Exception:
                pass

    async def create_limit_order(
        self,
        symbol,
        side,
        amount,
        price,
        post_only=True,
    ):
        params = {}

        if post_only:
            params["postOnly"] = True

        return await self.exchange.create_order(
            symbol=symbol,
            type="limit",
            side=side,
            amount=amount,
            price=price,
            params=params,
        )

    async def create_market_order(
        self,
        symbol,
        side,
        amount,
    ):
        return await self.exchange.create_order(
            symbol=symbol,
            type="market",
            side=side,
            amount=amount,
        )

    async def watch_orderbook(self, symbol):
        return await self.exchange.watch_order_book(symbol)

    async def watch_trades(self, symbol):
        return await self.exchange.watch_trades(symbol)

    async def fetch_orderbook(self, symbol):
        return await self.exchange.fetch_order_book(symbol)

    async def fetch_ticker(self, symbol):
        return await self.exchange.fetch_ticker(symbol)

    async def fetch_ohlcv(
        self,
        symbol,
        timeframe="1m",
        limit=500,
    ):
        return await self.exchange.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
        )


# Singleton
client = BloFinClient()
