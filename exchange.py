import aiohttp
import ccxt.pro as ccxt
import time
from config import (
    API_KEY,
    API_SECRET,
    API_PASSWORD,
    DEFAULT_TYPE,
    ENABLE_RATE_LIMIT,
    VERIFY_SSL,
    USE_IPV4,
)
import logging
import aiohttp
import ccxt.pro as ccxt
import time
import asyncio


logger = logging.getLogger(__name__)


class BloFinClient:
    def __init__(self):
        self.exchange = None
        self._balance_cache = None

        self._balance_cache_time = 0

        self._balance_cache_ttl = 5

    async def connect(self):
        """
        ایجاد اتصال به صرافی
        """

        if self.exchange is not None:
            return self.exchange

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

    async def ensure_connected(self):
        """
        Ensure exchange connection is available.
        """

        if self.exchange is None:
            await self.connect()

    async def close(self):
        if self.exchange is not None:
            await self.exchange.close()
            self.exchange = None
            logger.info("Exchange connection closed.")

    async def _safe_api_call(
        self,
        func,
        *args,
        **kwargs,
    ):
        """
        Execute an exchange API call with automatic reconnect and retry.
        """

        retries = 3

        for attempt in range(1, retries + 1):
            try:
                await self.ensure_connected()

                return await func(
                    *args,
                    **kwargs,
                )

            except (
                ccxt.NetworkError,
                ccxt.RequestTimeout,
            ):
                logger.warning(
                    "Exchange API failed (%d/%d). Reconnecting...",
                    attempt,
                    retries,
                )

                try:
                    await self.close()
                except Exception:
                    pass

                await asyncio.sleep(attempt)

            except Exception:
                raise

        raise RuntimeError("Exchange API unavailable after retries.")

    async def _safe_trade_call(
        self,
        func,
        *args,
        **kwargs,
    ):
        """
        Execute trade-related API calls.

        Never retry automatically to avoid duplicate orders.
        """

        try:
            await self.ensure_connected()

            return await func(
                *args,
                **kwargs,
            )

        except (
            ccxt.NetworkError,
            ccxt.RequestTimeout,
        ):
            logger.error(
                "Trade request failed due to network error. No automatic retry performed."
            )

            raise

        except Exception:
            raise

    async def fetch_balance(self):
        await self.ensure_connected()

        now = time.time()

        # استفاده از Cache اگر هنوز معتبر باشد
        if (
            self._balance_cache is not None
            and now - self._balance_cache_time < self._balance_cache_ttl
        ):
            return self._balance_cache

        # دریافت موجودی از صرافی
        balance = await self._safe_api_call(
            self.exchange.fetch_balance,
        )

        # ذخیره در Cache
        self._balance_cache = balance
        self._balance_cache_time = now

        return balance

    async def fetch_open_orders(self, symbol):

        return await self._safe_api_call(
            self.exchange.fetch_open_orders,
            symbol,
        )

    async def fetch_positions(self, symbol):

        return await self._safe_api_call(
            self.exchange.fetch_positions,
            [symbol],
        )

    async def cancel_order(self, order_id, symbol):

        return await self._safe_api_call(
            self.exchange.cancel_order,
            order_id,
            symbol,
        )

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

        return await self._safe_trade_call(
            self.exchange.create_order,
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
        return await self._safe_trade_call(
            self.exchange.create_order,
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

    async def amount_to_precision(
        self,
        symbol: str,
        amount: float,
    ) -> float:
        """
        Convert order amount to the exchange-supported precision.
        """

        amount = self.exchange.amount_to_precision(
            symbol,
            amount,
        )

        return float(amount)

    async def price_to_precision(
        self,
        symbol: str,
        price: float,
    ) -> float:
        """
        Convert order price to the exchange-supported precision.
        """

        price = self.exchange.price_to_precision(
            symbol,
            price,
        )

        return float(price)

    async def validate_order(
        self,
        symbol: str,
        amount: float,
        price: float,
    ) -> bool:
        """
        Validate order against exchange market limits.
        """

        try:
            market = self.exchange.market(symbol)

            limits = market.get("limits", {})

            # -------------------------
            # Minimum Amount
            # -------------------------

            min_amount = limits.get("amount", {}).get("min")

            if min_amount is not None and amount < min_amount:
                logger.warning(
                    "%s | Amount %.8f < Min Amount %.8f",
                    symbol,
                    amount,
                    min_amount,
                )

                return False

            # -------------------------
            # Minimum Notional
            # -------------------------

            min_cost = limits.get("cost", {}).get("min")

            cost = amount * price

            if min_cost is not None and cost < min_cost:
                logger.warning(
                    "%s | Order Cost %.4f < Min Cost %.4f",
                    symbol,
                    cost,
                    min_cost,
                )

                return False

            return True

        except Exception:
            logger.exception("Order validation failed.")

            return False


# Singleton
client = BloFinClient()
