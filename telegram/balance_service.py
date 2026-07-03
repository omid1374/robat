"""
telegram/balance_service.py
"""

from datetime import datetime, timedelta

from exchange import client


class BalanceService:

    def __init__(self, exchange_client=client):
        self.client = exchange_client

        self._cache = None
        self._cache_time = None

        # مدت اعتبار کش
        self.cache_seconds = 5

    async def get_balance(self, force=False):

        # اگر کش معتبر است همان را برگردان
        if (
            not force
            and self._cache is not None
            and self._cache_time is not None
            and datetime.utcnow() - self._cache_time
            < timedelta(seconds=self.cache_seconds)
        ):
            return self._cache

        # اگر هنوز به صرافی وصل نشده‌ایم
        if self.client.exchange is None:
            await self.client.connect()

        balance = await self.client.fetch_balance()

        # ---------- BloFin / CCXT ----------

        total = balance.get("total", {})
        free = balance.get("free", {})
        used = balance.get("used", {})

        usdt_total = float(total.get("USDT", 0))
        usdt_free = float(free.get("USDT", 0))
        usdt_used = float(used.get("USDT", 0))

        info = balance.get("info", {})

        unrealized = 0.0
        equity = usdt_total

        try:

            data = info.get("data")

            if isinstance(data, list) and len(data):

                acc = data[0]

                unrealized = float(
                    acc.get("upl", 0)
                )

                equity = float(
                    acc.get("equity", usdt_total)
                )

        except Exception:
            pass

        result = {

            "wallet_balance": usdt_total,

            "available_balance": usdt_free,

            "used_balance": usdt_used,

            "equity": equity,

            "unrealized_pnl": unrealized,

            "timestamp": datetime.utcnow().isoformat()

        }

        self._cache = result
        self._cache_time = datetime.utcnow()

        return result

    async def refresh(self):
        return await self.get_balance(force=True)